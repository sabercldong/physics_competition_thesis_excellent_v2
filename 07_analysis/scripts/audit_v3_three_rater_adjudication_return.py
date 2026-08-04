#!/usr/bin/env python3
"""Audit a completed V3/F/G disagreement adjudication workbook."""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path


DECISION_FIELDS = [
    "是否已核对原文",
    "裁决后存在性",
    "裁决后等级",
    "裁决依据",
    "复核后证据位置",
    "裁决置信度",
    "待补材料",
    "裁决状态",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = ["裁决序号", "blind_row_id", "item_id", "维度", "问题代码", "问题说明"]
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("filled_file", type=Path)
    parser.add_argument("--template", type=Path, required=True)
    parser.add_argument("--worklist", type=Path, required=True)
    parser.add_argument(
        "--candidate-mode",
        action="store_true",
        help="Audit a non-human candidate file without treating it as completed adjudication.",
    )
    args = parser.parse_args()

    filled = read_csv(args.filled_file)
    template = read_csv(args.template)
    issues: list[dict[str, str]] = []

    def add(row: dict[str, str], code: str, detail: str) -> None:
        issues.append(
            {
                "裁决序号": row.get("裁决序号", ""),
                "blind_row_id": row.get("blind_row_id", ""),
                "item_id": row.get("item_id", ""),
                "维度": row.get("维度", ""),
                "问题代码": code,
                "问题说明": detail,
            }
        )

    if len(filled) != 146:
        add({}, "ROW_COUNT", f"实测{len(filled)}行，预期146行")
    if len(template) != 146:
        raise ValueError(f"模板行数异常：{len(template)}")
    fixed_fields = [field for field in template[0] if field not in DECISION_FIELDS]
    template_by_id = {row["裁决序号"]: row for row in template}
    if len(template_by_id) != 146:
        raise ValueError("模板裁决序号不唯一")
    filled_ids = [row.get("裁决序号", "").strip() for row in filled]
    if len(filled_ids) != len(set(filled_ids)):
        add({}, "DUPLICATE_ID", "回填表存在重复裁决序号")
    if set(filled_ids) != set(template_by_id):
        add({}, "ID_SET", "回填表与模板裁决序号集合不一致")

    for row in filled:
        row_id = row.get("裁决序号", "").strip()
        original = template_by_id.get(row_id)
        if original is None:
            continue
        changed = [field for field in fixed_fields if row.get(field, "") != original.get(field, "")]
        if changed:
            add(row, "FIXED_FIELDS_CHANGED", "固定字段被修改：" + "、".join(changed))
        status = row.get("裁决状态", "").strip()
        checked = row.get("是否已核对原文", "").strip()
        present = row.get("裁决后存在性", "").strip()
        level = row.get("裁决后等级", "").strip()
        reason = row.get("裁决依据", "").strip()
        location = row.get("复核后证据位置", "").strip()
        confidence = row.get("裁决置信度", "").strip()
        material = row.get("待补材料", "").strip()
        if args.candidate_mode:
            if status != "模型辅助候选，待研究者确认":
                add(row, "INVALID_CANDIDATE_STATUS", "候选模式状态必须明确为待研究者确认")
                continue
            if checked != "否（仅核对材料包清晰证据摘录）":
                add(row, "CANDIDATE_PROVENANCE", "候选模式不得声称已逐条核对原文")
            valid = (present == "否" and level == "未出现") or (
                present == "是" and level in {"L1", "L2", "L3", "L4"}
            )
            if not valid:
                add(row, "INVALID_LABEL", f"非法组合：{present}/{level}")
            if len(reason) < 30:
                add(row, "REASON_TOO_SHORT", "候选裁决依据少于30字符")
            if not location:
                add(row, "LOCATION_BLANK", "候选证据位置为空")
            if confidence not in {"高", "中", "低"}:
                add(row, "INVALID_CONFIDENCE", "候选置信度应为高、中或低")
            if "待研究者" not in material:
                add(row, "RESEARCHER_CONFIRMATION_MISSING", "待补材料字段必须保留研究者确认要求")
            continue
        if status not in {"已裁决", "待核实"}:
            add(row, "INVALID_STATUS", "裁决状态应为已裁决或待核实")
            continue
        if checked != "是":
            add(row, "SOURCE_NOT_CHECKED", "是否已核对原文必须填写是")
        if status == "已裁决":
            valid = (present == "否" and level == "未出现") or (
                present == "是" and level in {"L1", "L2", "L3", "L4"}
            )
            if not valid:
                add(row, "INVALID_LABEL", f"非法组合：{present}/{level}")
            if len(reason) < 30:
                add(row, "REASON_TOO_SHORT", "裁决依据少于30字符")
            if not location:
                add(row, "LOCATION_BLANK", "复核后证据位置为空")
            if confidence not in {"高", "中", "低"}:
                add(row, "INVALID_CONFIDENCE", "已裁决行置信度应为高、中或低")
            if not material:
                add(row, "MATERIAL_BLANK", "待补材料无缺项时也应填写无")
        else:
            if present != "待核实" or level != "待核实":
                add(row, "PENDING_LABEL", "待核实行应填写待核实/待核实")
            if not reason or not material or material == "无":
                add(row, "PENDING_REASON", "待核实行必须说明原因和具体待补材料")
            if confidence != "待核实":
                add(row, "PENDING_CONFIDENCE", "待核实行置信度应为待核实")

    write_csv(args.worklist, issues)
    statuses = Counter(row.get("裁决状态", "").strip() for row in filled)
    print(f"ROWS={len(filled)}")
    print(f"ADJUDICATED={statuses['已裁决']}")
    print(f"PENDING={statuses['待核实']}")
    print(f"CANDIDATE={statuses['模型辅助候选，待研究者确认']}")
    print(f"ISSUES={len(issues)}")
    if issues:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
