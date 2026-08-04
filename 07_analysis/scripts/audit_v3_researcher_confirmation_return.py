#!/usr/bin/env python3
"""Audit a returned researcher confirmation workbook."""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path


RESEARCHER_FIELDS = [
    "是否完整阅读原题与解答",
    "研究者决定",
    "最终存在性",
    "最终等级",
    "研究者裁决依据",
    "研究者证据定位",
    "研究者置信度",
    "待补材料",
    "确认状态",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    fields = ["工作序号", "裁决序号", "item_id", "维度", "问题代码", "问题说明"]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def expected_pair(label: str) -> tuple[str, str]:
    return ("否", "未出现") if label == "未出现" else ("是", label)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("filled_file", type=Path)
    parser.add_argument("--template", type=Path, required=True)
    parser.add_argument("--issues", type=Path, required=True)
    parser.add_argument(
        "--template-mode",
        action="store_true",
        help="Check that the generated template is locked and all researcher fields are blank.",
    )
    args = parser.parse_args()

    filled = read_csv(args.filled_file)
    template = read_csv(args.template)
    issues: list[dict[str, str]] = []

    def add(row: dict[str, str], code: str, detail: str) -> None:
        issues.append(
            {
                "工作序号": row.get("工作序号", ""),
                "裁决序号": row.get("裁决序号", ""),
                "item_id": row.get("item_id", ""),
                "维度": row.get("维度", ""),
                "问题代码": code,
                "问题说明": detail,
            }
        )

    if len(template) != 146:
        raise ValueError(f"模板应为146行，实测{len(template)}行")
    if len(filled) != 146:
        add({}, "ROW_COUNT", f"回填表应为146行，实测{len(filled)}行")
    fixed_fields = [field for field in template[0] if field not in RESEARCHER_FIELDS]
    template_by_id = {row["裁决序号"]: row for row in template}
    filled_ids = [row.get("裁决序号", "").strip() for row in filled]
    if len(filled_ids) != len(set(filled_ids)):
        add({}, "DUPLICATE_ID", "裁决序号存在重复")
    if set(filled_ids) != set(template_by_id):
        add({}, "ID_SET", "回填表与模板裁决序号集合不一致")

    for row in filled:
        row_id = row.get("裁决序号", "").strip()
        original = template_by_id.get(row_id)
        if original is None:
            continue
        changed = [field for field in fixed_fields if row.get(field, "") != original.get(field, "")]
        if changed:
            add(row, "FIXED_FIELDS_CHANGED", "前27列被修改：" + "、".join(changed))
        values = {field: row.get(field, "").strip() for field in RESEARCHER_FIELDS}
        if args.template_mode:
            nonblank = [field for field, value in values.items() if value]
            if nonblank:
                add(row, "TEMPLATE_NOT_BLANK", "研究者字段应为空：" + "、".join(nonblank))
            continue

        status = values["确认状态"]
        if not status:
            add(row, "NOT_REVIEWED", "本行尚未确认")
            continue
        if status not in {"已确认", "待核实"}:
            add(row, "INVALID_STATUS", "确认状态只允许已确认或待核实")
            continue
        if values["是否完整阅读原题与解答"] != "是":
            add(row, "SOURCE_NOT_READ", "必须完整阅读原题与解答后才能确认")

        decision = values["研究者决定"]
        present = values["最终存在性"]
        level = values["最终等级"]
        reason = values["研究者裁决依据"]
        location = values["研究者证据定位"]
        confidence = values["研究者置信度"]
        material = values["待补材料"]

        if status == "待核实":
            if decision != "待核实" or present != "待核实" or level != "待核实":
                add(row, "PENDING_LABEL", "待核实行必须填待核实/待核实/待核实")
            if confidence != "待核实":
                add(row, "PENDING_CONFIDENCE", "待核实行置信度必须填待核实")
            if len(reason) < 10 or not material or material == "无":
                add(row, "PENDING_DETAIL", "待核实行必须说明原因和具体待补材料")
            continue

        if decision not in {"确认候选", "保留第三版", "另行裁决"}:
            add(row, "INVALID_DECISION", "已确认行的研究者决定不合法")
        valid_pair = (present == "否" and level == "未出现") or (
            present == "是" and level in {"L1", "L2", "L3", "L4"}
        )
        if not valid_pair:
            add(row, "INVALID_LABEL", f"非法最终标签组合：{present}/{level}")
        if decision == "确认候选" and (present, level) != expected_pair(row["候选裁决标签"]):
            add(row, "CANDIDATE_MISMATCH", "确认候选时最终标签必须等于候选裁决标签")
        if decision == "保留第三版" and (present, level) != expected_pair(row["第三版标签"]):
            add(row, "V3_MISMATCH", "保留第三版时最终标签必须等于第三版标签")
        if len(reason) < 30:
            add(row, "REASON_TOO_SHORT", "研究者裁决依据少于30字符")
        source_name = Path(row["完整题目与解答文件"]).name
        if not location or source_name not in location:
            add(row, "LOCATION_INCOMPLETE", f"证据定位必须包含{source_name}")
        if confidence not in {"高", "中", "低"}:
            add(row, "INVALID_CONFIDENCE", "已确认行置信度只允许高、中或低")
        if not material:
            add(row, "MATERIAL_BLANK", "无待补材料时填写无")

    write_csv(args.issues, issues)
    statuses = Counter(row.get("确认状态", "").strip() for row in filled)
    decisions = Counter(row.get("研究者决定", "").strip() for row in filled)
    print(f"ROWS={len(filled)}")
    print(f"CONFIRMED={statuses['已确认']}")
    print(f"PENDING={statuses['待核实']}")
    print(f"UNREVIEWED={statuses['']}")
    print(f"ACCEPT_CANDIDATE={decisions['确认候选']}")
    print(f"RETAIN_V3={decisions['保留第三版']}")
    print(f"NEW_DECISION={decisions['另行裁决']}")
    print(f"ISSUES={len(issues)}")
    if issues:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
