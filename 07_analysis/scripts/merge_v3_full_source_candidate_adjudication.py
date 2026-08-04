#!/usr/bin/env python3
"""Merge and audit four full-source candidate adjudication batches."""

from __future__ import annotations

import csv
import hashlib
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ADJ_ROOT = ROOT / "07_analysis/data/v3_independent_validation/adjudication"
SOURCE_DIR = ADJ_ROOT / "完整原文复核_146行_20260803"
CANDIDATE = (
    ADJ_ROOT
    / "模型辅助候选裁决_146行_20260803"
    / "三方分歧模型辅助候选裁决表_146行_待研究者确认.csv"
)
MASTER = ROOT / "07_analysis/data/第35至42届科学思维第三版唯一编码表.csv"
OUTPUT_DIR = SOURCE_DIR / "合并结果"
PARTS = [
    (SOURCE_DIR / "批次_第35至36届_18行.csv", 18),
    (SOURCE_DIR / "批次_第37至38届_31行.csv", 31),
    (SOURCE_DIR / "批次_第39至40届_37行.csv", 37),
    (SOURCE_DIR / "批次_第41至42届_60行.csv", 60),
]
PART_FIELDS = [
    "裁决序号",
    "item_id",
    "届次",
    "小问",
    "维度",
    "完整原文已核对",
    "完整原文裁决标签",
    "完整原文裁决依据",
    "完整原文证据位置",
    "裁决置信度",
    "与原候选关系",
    "复核说明",
]
VALID_LABELS = {"未出现", "L1", "L2", "L3", "L4", "待核实"}


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
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def label(row: dict[str, str], prefix: str) -> str:
    return "未出现" if row[f"{prefix}存在性"] == "否" else row[f"{prefix}等级"]


def candidate_label(row: dict[str, str]) -> str:
    return "未出现" if row["裁决后存在性"] == "否" else row["裁决后等级"]


def pair(value: str) -> tuple[str, str, str]:
    if value == "未出现":
        return "0", "否", "未出现"
    return "1", "是", value


def main() -> None:
    candidate_fields, candidate_rows = read_csv(CANDIDATE)
    master_fields, master_rows = read_csv(MASTER)
    issues: list[dict[str, str]] = []
    merged_parts: list[dict[str, str]] = []

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

    for path, expected in PARTS:
        if not path.is_file():
            issue({}, "PART_MISSING", f"缺少批次文件：{path.name}")
            continue
        fields, rows = read_csv(path)
        if fields != PART_FIELDS:
            issue({}, "PART_FIELDS", f"{path.name}字段不符合规范")
        if len(rows) != expected:
            issue({}, "PART_ROWS", f"{path.name}应为{expected}行，实测{len(rows)}行")
        merged_parts.extend(rows)

    candidate_by_id = {row["裁决序号"]: row for row in candidate_rows}
    if len(candidate_rows) != 146 or len(candidate_by_id) != 146:
        raise ValueError("候选裁决基线应为146条唯一记录")
    part_ids = [row.get("裁决序号", "").strip() for row in merged_parts]
    if len(part_ids) != len(set(part_ids)):
        issue({}, "DUPLICATE_ID", "批次文件存在重复裁决序号")
    if set(part_ids) != set(candidate_by_id):
        missing = sorted(set(candidate_by_id) - set(part_ids))
        extra = sorted(set(part_ids) - set(candidate_by_id))
        issue({}, "ID_SET", f"缺少{len(missing)}条，多出{len(extra)}条")

    full_by_id: dict[str, dict[str, str]] = {}
    for row in merged_parts:
        row_id = row.get("裁决序号", "").strip()
        source = candidate_by_id.get(row_id)
        if source is None:
            continue
        full_by_id[row_id] = row
        for field, expected in (
            ("item_id", source["item_id"]),
            ("届次", source["届次"]),
            ("小问", source["小问"]),
            ("维度", source["维度"]),
        ):
            if row.get(field, "") != expected:
                issue(row, "LOCKED_FIELD", f"{field}应为{expected}，实测{row.get(field, '')}")
        if row.get("完整原文已核对") != "是":
            issue(row, "SOURCE_NOT_CHECKED", "完整原文已核对必须为是")
        final = row.get("完整原文裁决标签", "")
        if final not in VALID_LABELS:
            issue(row, "INVALID_LABEL", f"非法标签：{final}")
        expected_relation = (
            "待核实"
            if final == "待核实"
            else "保持候选"
            if final == candidate_label(source)
            else "修正候选"
        )
        if row.get("与原候选关系") != expected_relation:
            issue(row, "RELATION_MISMATCH", f"与原候选关系应为{expected_relation}")
        reason = row.get("完整原文裁决依据", "").strip()
        if len(reason) < 40:
            issue(row, "REASON_TOO_SHORT", "完整原文裁决依据少于40字符")
        location = row.get("完整原文证据位置", "").strip()
        if source["源文件"] not in location:
            issue(row, "LOCATION_INCOMPLETE", f"证据位置必须包含{source['源文件']}")
        if row.get("裁决置信度") not in {"高", "中", "低", "待核实"}:
            issue(row, "INVALID_CONFIDENCE", "裁决置信度不合法")
        if "完整原文模型辅助候选" not in row.get("复核说明", ""):
            issue(row, "PROVENANCE_MISSING", "复核说明必须保留模型辅助候选来源")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    audit_path = OUTPUT_DIR / "完整原文复核审计问题清单.csv"
    write_csv(
        audit_path,
        ["裁决序号", "item_id", "维度", "问题代码", "问题说明"],
        issues,
    )
    if issues:
        print(f"ROWS={len(merged_parts)}")
        print(f"ISSUES={len(issues)}")
        raise SystemExit(1)

    combined_fields = candidate_fields + [field for field in PART_FIELDS[5:]]
    combined_rows: list[dict[str, str]] = []
    for source in candidate_rows:
        full = full_by_id[source["裁决序号"]]
        combined_rows.append({**source, **{field: full[field] for field in PART_FIELDS[5:]}})
    combined_path = OUTPUT_DIR / "完整原文模型辅助候选裁决表_146行.csv"
    write_csv(combined_path, combined_fields, combined_rows)

    original_candidate_changes: list[dict[str, str]] = []
    v3_changes: list[dict[str, str]] = []
    for row in combined_rows:
        new = row["完整原文裁决标签"]
        old_candidate = candidate_label(row)
        old_v3 = label(row, "第三版")
        compact = {
            "裁决序号": row["裁决序号"],
            "第三版源记录": row["第三版源记录"],
            "item_id": row["item_id"],
            "维度": row["维度"],
            "第三版标签": old_v3,
            "原候选标签": old_candidate,
            "完整原文裁决标签": new,
            "完整原文裁决依据": row["完整原文裁决依据"],
            "完整原文证据位置": row["完整原文证据位置"],
            "裁决置信度": row["裁决置信度"],
        }
        if new != old_candidate:
            original_candidate_changes.append(compact)
        if new != old_v3:
            v3_changes.append(compact)
    change_fields = [
        "裁决序号",
        "第三版源记录",
        "item_id",
        "维度",
        "第三版标签",
        "原候选标签",
        "完整原文裁决标签",
        "完整原文裁决依据",
        "完整原文证据位置",
        "裁决置信度",
    ]
    write_csv(OUTPUT_DIR / "相对原候选修正清单.csv", change_fields, original_candidate_changes)
    write_csv(OUTPUT_DIR / "相对第三版变更清单.csv", change_fields, v3_changes)

    final_by_review_id = {
        row["第三版源记录"]: row["完整原文裁决标签"] for row in combined_rows
    }
    simulation_rows: list[dict[str, str]] = []
    for row in master_rows:
        updated = dict(row)
        final = final_by_review_id.get(row["review_row_id"])
        if final and final != "待核实":
            present, present_label, level_value = pair(final)
            updated["present"] = present
            updated["present_label"] = present_label
            updated["level"] = level_value
            updated["candidate_present_label"] = present_label
            updated["candidate_level"] = level_value
        simulation_rows.append(updated)
    simulation_path = OUTPUT_DIR / "若采纳完整原文候选裁决的884行模拟表.csv"
    write_csv(simulation_path, master_fields, simulation_rows)

    dimension_counts = Counter()
    label_counts = Counter()
    confidence_counts = Counter()
    for row in combined_rows:
        dimension_counts[(row["维度"], row["完整原文裁决标签"])] += 1
        label_counts[row["完整原文裁决标签"]] += 1
        confidence_counts[row["裁决置信度"]] += 1
    summary_rows = []
    for dimension in ("模型建构", "科学推理", "科学论证", "质疑创新"):
        for level_value in ("未出现", "L1", "L2", "L3", "L4", "待核实"):
            summary_rows.append(
                {
                    "维度": dimension,
                    "标签": level_value,
                    "数量": str(dimension_counts[(dimension, level_value)]),
                }
            )
    write_csv(OUTPUT_DIR / "完整原文裁决标签分布.csv", ["维度", "标签", "数量"], summary_rows)

    report = OUTPUT_DIR / "完整原文复核汇总.md"
    report.write_text(
        "# 三方分歧完整原文复核汇总\n\n"
        "> 本轮由模型逐条读取完整题目与参考解答后形成，作者已授权项目完成该工作。"
        "它不冒充独立真人裁决；正式第三版主表保持不变，884行文件仅为采纳情景模拟。\n\n"
        f"- 完整原文复核：{len(combined_rows)}条；\n"
        f"- 相对原候选修正：{len(original_candidate_changes)}条；\n"
        f"- 相对第三版变更：{len(v3_changes)}条；\n"
        f"- 待核实：{label_counts['待核实']}条；\n"
        f"- 置信度：高{confidence_counts['高']}、中{confidence_counts['中']}、"
        f"低{confidence_counts['低']}、待核实{confidence_counts['待核实']}；\n"
        f"- 合并表SHA-256：`{sha256(combined_path)}`；\n"
        f"- 模拟表SHA-256：`{sha256(simulation_path)}`。\n\n"
        "## 数据门禁\n\n"
        "本目录可用于比较标签和重算敏感性结果，但不得表述为新增真人评分者或真人逐行裁决。"
        "在研究方法中如采用本结果，必须如实说明计算辅助及作者责任。\n",
        encoding="utf-8",
    )
    print(f"ROWS={len(combined_rows)}")
    print(f"ISSUES={len(issues)}")
    print(f"CHANGED_FROM_ORIGINAL_CANDIDATE={len(original_candidate_changes)}")
    print(f"CHANGED_FROM_V3={len(v3_changes)}")
    print(f"PENDING={label_counts['待核实']}")
    print(f"COMBINED={combined_path}")
    print(f"SIMULATION={simulation_path}")


if __name__ == "__main__":
    main()
