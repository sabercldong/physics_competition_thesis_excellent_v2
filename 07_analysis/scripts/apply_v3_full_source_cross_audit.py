#!/usr/bin/env python3
"""Apply the adversarial cross-audit to 26 changed full-source decisions."""

from __future__ import annotations

import csv
import hashlib
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BASE = (
    ROOT
    / "07_analysis/data/v3_independent_validation/adjudication"
    / "完整原文复核_146行_20260803"
)
MERGED_DIR = BASE / "合并结果"
FIRST_PASS = MERGED_DIR / "完整原文模型辅助候选裁决表_146行.csv"
FIRST_CHANGES = MERGED_DIR / "相对原候选修正清单.csv"
MASTER = ROOT / "07_analysis/data/第35至42届科学思维第三版唯一编码表.csv"
AUDITS = [
    BASE / "第二轮交叉审计_模型建构与质疑创新_13行.csv",
    BASE / "第二轮交叉审计_科学推理与科学论证_13行.csv",
]
OUT = BASE / "第二轮交叉审计后结果"
AUDIT_FIELDS = [
    "裁决序号",
    "item_id",
    "维度",
    "原候选标签",
    "第一轮完整原文标签",
    "第二轮审核结论",
    "第二轮建议标签",
    "第二轮审核理由",
    "第二轮证据位置",
    "置信度",
]
VALID_LABELS = {"未出现", "L1", "L2", "L3", "L4"}


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def write_csv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_label(row: dict[str, str], prefix: str) -> str:
    return "未出现" if row[f"{prefix}存在性"] == "否" else row[f"{prefix}等级"]


def candidate_label(row: dict[str, str]) -> str:
    return "未出现" if row["裁决后存在性"] == "否" else row["裁决后等级"]


def pair(value: str) -> tuple[str, str, str]:
    if value == "未出现":
        return "0", "否", "未出现"
    return "1", "是", value


def main() -> None:
    first_fields, first_rows = read_csv(FIRST_PASS)
    _, first_changes = read_csv(FIRST_CHANGES)
    master_fields, master_rows = read_csv(MASTER)
    first_by_id = {row["裁决序号"]: row for row in first_rows}
    expected_ids = {row["裁决序号"] for row in first_changes}
    issues: list[dict[str, str]] = []
    audit_rows: list[dict[str, str]] = []

    def issue(row: dict[str, str], code: str, detail: str) -> None:
        issues.append(
            {
                "裁决序号": row.get("裁决序号", ""),
                "item_id": row.get("item_id", ""),
                "维度": row.get("维度", ""),
                "问题代码": code,
                "问题说明": detail,
            }
        )

    for path in AUDITS:
        if not path.is_file():
            issue({}, "AUDIT_MISSING", f"缺少第二轮文件：{path.name}")
            continue
        fields, rows = read_csv(path)
        if fields != AUDIT_FIELDS:
            issue({}, "AUDIT_FIELDS", f"{path.name}字段不符合规范")
        if len(rows) != 13:
            issue({}, "AUDIT_ROWS", f"{path.name}应为13行，实测{len(rows)}行")
        audit_rows.extend(rows)

    ids = [row.get("裁决序号", "").strip() for row in audit_rows]
    if len(ids) != len(set(ids)):
        issue({}, "DUPLICATE_ID", "第二轮文件存在重复裁决序号")
    if set(ids) != expected_ids:
        issue({}, "ID_SET", f"第二轮应覆盖{len(expected_ids)}条第一轮修正记录")

    audit_by_id: dict[str, dict[str, str]] = {}
    for row in audit_rows:
        row_id = row.get("裁决序号", "").strip()
        source = first_by_id.get(row_id)
        if source is None:
            continue
        audit_by_id[row_id] = row
        expected_old = candidate_label(source)
        expected_first = source["完整原文裁决标签"]
        for field, expected in (
            ("item_id", source["item_id"]),
            ("维度", source["维度"]),
            ("原候选标签", expected_old),
            ("第一轮完整原文标签", expected_first),
        ):
            if row.get(field, "") != expected:
                issue(row, "LOCKED_FIELD", f"{field}应为{expected}")
        conclusion = row.get("第二轮审核结论", "")
        suggestion = row.get("第二轮建议标签", "")
        if conclusion not in {"通过", "建议修正"}:
            issue(row, "INVALID_CONCLUSION", "第二轮审核结论只允许通过或建议修正")
        if suggestion not in VALID_LABELS:
            issue(row, "INVALID_LABEL", f"第二轮建议标签不合法：{suggestion}")
        if conclusion == "通过" and suggestion != expected_first:
            issue(row, "PASS_MISMATCH", "审核通过时建议标签必须等于第一轮标签")
        if conclusion == "建议修正" and suggestion == expected_first:
            issue(row, "REVISION_MISMATCH", "建议修正时建议标签必须不同于第一轮标签")
        if len(row.get("第二轮审核理由", "").strip()) < 50:
            issue(row, "REASON_TOO_SHORT", "第二轮审核理由少于50字符")
        if source["源文件"] not in row.get("第二轮证据位置", ""):
            issue(row, "LOCATION_INCOMPLETE", f"证据位置必须包含{source['源文件']}")
        if row.get("置信度") not in {"高", "中", "低"}:
            issue(row, "INVALID_CONFIDENCE", "第二轮置信度不合法")

    OUT.mkdir(parents=True, exist_ok=True)
    write_csv(
        OUT / "第二轮交叉审计问题清单.csv",
        ["裁决序号", "item_id", "维度", "问题代码", "问题说明"],
        issues,
    )
    if issues:
        print(f"AUDIT_ROWS={len(audit_rows)}")
        print(f"ISSUES={len(issues)}")
        raise SystemExit(1)

    extra_fields = [
        "第二轮是否触发",
        "第二轮审核结论",
        "第二轮审核理由",
        "第二轮证据位置",
        "第二轮置信度",
        "交叉审计后裁决标签",
        "交叉审计后裁决依据",
        "交叉审计后证据位置",
        "交叉审计后置信度",
        "交叉审计后状态",
    ]
    final_rows: list[dict[str, str]] = []
    second_revisions = 0
    for row in first_rows:
        audit = audit_by_id.get(row["裁决序号"])
        if audit:
            final_label = audit["第二轮建议标签"]
            final_reason = audit["第二轮审核理由"]
            final_location = audit["第二轮证据位置"]
            final_confidence = audit["置信度"]
            if audit["第二轮审核结论"] == "建议修正":
                second_revisions += 1
            second_values = {
                "第二轮是否触发": "是",
                "第二轮审核结论": audit["第二轮审核结论"],
                "第二轮审核理由": audit["第二轮审核理由"],
                "第二轮证据位置": audit["第二轮证据位置"],
                "第二轮置信度": audit["置信度"],
            }
        else:
            final_label = row["完整原文裁决标签"]
            final_reason = row["完整原文裁决依据"]
            final_location = row["完整原文证据位置"]
            final_confidence = row["裁决置信度"]
            second_values = {
                "第二轮是否触发": "否（第一轮未修正原候选）",
                "第二轮审核结论": "未触发",
                "第二轮审核理由": "第一轮完整原文标签与原候选一致，未进入26条对抗性复核。",
                "第二轮证据位置": row["完整原文证据位置"],
                "第二轮置信度": row["裁决置信度"],
            }
        final_rows.append(
            {
                **row,
                **second_values,
                "交叉审计后裁决标签": final_label,
                "交叉审计后裁决依据": final_reason,
                "交叉审计后证据位置": final_location,
                "交叉审计后置信度": final_confidence,
                "交叉审计后状态": "完整原文模型辅助候选，经作者授权采用；不冒充真人裁决",
            }
        )
    final_path = OUT / "第二轮交叉审计后完整原文候选裁决表_146行.csv"
    write_csv(final_path, first_fields + extra_fields, final_rows)

    compact_fields = [
        "裁决序号",
        "第三版源记录",
        "item_id",
        "维度",
        "第三版标签",
        "原候选标签",
        "第一轮完整原文标签",
        "交叉审计后裁决标签",
        "交叉审计后裁决依据",
        "交叉审计后证据位置",
        "交叉审计后置信度",
    ]
    v3_changes: list[dict[str, str]] = []
    original_changes: list[dict[str, str]] = []
    for row in final_rows:
        compact = {
            "裁决序号": row["裁决序号"],
            "第三版源记录": row["第三版源记录"],
            "item_id": row["item_id"],
            "维度": row["维度"],
            "第三版标签": source_label(row, "第三版"),
            "原候选标签": candidate_label(row),
            "第一轮完整原文标签": row["完整原文裁决标签"],
            "交叉审计后裁决标签": row["交叉审计后裁决标签"],
            "交叉审计后裁决依据": row["交叉审计后裁决依据"],
            "交叉审计后证据位置": row["交叉审计后证据位置"],
            "交叉审计后置信度": row["交叉审计后置信度"],
        }
        if compact["交叉审计后裁决标签"] != compact["第三版标签"]:
            v3_changes.append(compact)
        if compact["交叉审计后裁决标签"] != compact["原候选标签"]:
            original_changes.append(compact)
    write_csv(OUT / "相对第三版最终变更清单.csv", compact_fields, v3_changes)
    write_csv(OUT / "相对原候选最终修正清单.csv", compact_fields, original_changes)

    final_by_review_id = {
        row["第三版源记录"]: row["交叉审计后裁决标签"] for row in final_rows
    }
    simulation_rows: list[dict[str, str]] = []
    for row in master_rows:
        updated = dict(row)
        final_label = final_by_review_id.get(row["review_row_id"])
        if final_label:
            present, present_label, level = pair(final_label)
            updated["present"] = present
            updated["present_label"] = present_label
            updated["level"] = level
            updated["candidate_present_label"] = present_label
            updated["candidate_level"] = level
        simulation_rows.append(updated)
    simulation_path = OUT / "若采纳交叉审计后候选裁决的884行模拟表.csv"
    write_csv(simulation_path, master_fields, simulation_rows)

    label_counts = Counter(row["交叉审计后裁决标签"] for row in final_rows)
    confidence_counts = Counter(row["交叉审计后置信度"] for row in final_rows)
    report = OUT / "第二轮交叉审计汇总.md"
    report.write_text(
        "# 第二轮交叉审计汇总\n\n"
        "本轮只挑战第一轮相对原候选发生变化的26条记录，重点检查维度存在门槛、"
        "前问复用和科学论证过度识别风险。\n\n"
        f"- 第二轮审计：{len(audit_rows)}条；\n"
        f"- 第二轮再次修正：{second_revisions}条；\n"
        f"- 交叉审计后相对原候选修正：{len(original_changes)}条；\n"
        f"- 交叉审计后相对第三版变更：{len(v3_changes)}条；\n"
        f"- 标签分布：{dict(label_counts)}；\n"
        f"- 置信度：{dict(confidence_counts)}；\n"
        f"- 146行表SHA-256：`{sha256(final_path)}`；\n"
        f"- 884行模拟表SHA-256：`{sha256(simulation_path)}`。\n\n"
        "该结果仍是完整原文模型辅助候选，经作者授权采用，但不冒充新增真人裁决。\n",
        encoding="utf-8",
    )
    print(f"AUDIT_ROWS={len(audit_rows)}")
    print(f"ISSUES={len(issues)}")
    print(f"SECOND_PASS_REVISIONS={second_revisions}")
    print(f"CHANGED_FROM_ORIGINAL_CANDIDATE={len(original_changes)}")
    print(f"CHANGED_FROM_V3={len(v3_changes)}")
    print(f"FINAL_TABLE={final_path}")
    print(f"SIMULATION={simulation_path}")


if __name__ == "__main__":
    main()
