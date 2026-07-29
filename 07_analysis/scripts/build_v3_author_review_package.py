#!/usr/bin/env python3
"""Build the blank author substantive-review package for V3 candidates."""

from __future__ import annotations

from collections import Counter, defaultdict

from build_v3_cross_year_audit import (
    AUDIT,
    CANDIDATE_FIELDS,
    MERGED,
    ROOT,
    read_rows,
    write_rows,
)


OUTPUT = ROOT / "07_analysis/data/第35至42届科学思维V3作者实质复核回填表_空白.csv"
ITEM_INDEX = ROOT / "07_analysis/results/reviewed/第35至42届V3作者实质复核题目索引.csv"

PACKAGE_FIELDS = [
    "review_row_id",
    "review_priority",
    "priority_reason",
    "linked_audit_ids",
    "linked_audit_types",
    *CANDIDATE_FIELDS,
]

REVIEW_FIELDS = [
    "actual_author_reviewer_or_code",
    "actual_review_date",
    "source_checked",
    "question_evidence_decision",
    "solution_evidence_decision",
    "candidate_review_decision",
    "rechecked_present_label",
    "rechecked_level",
    "adjacent_level_review",
    "correction_reason",
    "post_review_evidence_location",
    "reviewer_statement",
    "author_review_status",
]

PRIORITY_ORDER = {"P0": 0, "P1": 1, "P2": 2}
UNIFORM_TYPE = "同题标签整齐复制风险"
PAIR_AUDIT_TYPES = {
    "模型建构重复计数复审",
    "论证关键词假阳性复审",
    "创新关键词假阳性复审",
    "质疑创新正例跨届复审",
}
ADDED_TYPE = "新增分析单元下游影响"


def split_items(value: str) -> list[str]:
    return [part.strip() for part in value.split("；") if part.strip().startswith("CPHO")]


def build_audit_links(
    audit_rows: list[dict[str, str]],
) -> tuple[
    dict[str, list[dict[str, str]]],
    dict[tuple[str, str], list[dict[str, str]]],
]:
    by_item: dict[str, list[dict[str, str]]] = defaultdict(list)
    by_pair: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for audit in audit_rows:
        item_ids = split_items(audit["item_or_group"])
        for item_id in item_ids:
            by_item[item_id].append(audit)
            if audit["audit_type"] in PAIR_AUDIT_TYPES and audit["dimension"]:
                by_pair[(item_id, audit["dimension"])].append(audit)
            elif audit["audit_type"] == UNIFORM_TYPE:
                for dimension in ("模型建构", "科学推理"):
                    by_pair[(item_id, dimension)].append(audit)
            elif audit["audit_type"] == ADDED_TYPE:
                for dimension in ("模型建构", "科学推理", "科学论证", "质疑创新"):
                    by_pair[(item_id, dimension)].append(audit)
    return by_item, by_pair


def assign_priority(
    row: dict[str, str],
    pair_audits: list[dict[str, str]],
) -> tuple[str, str]:
    reasons: list[str] = []
    audit_types = {audit["audit_type"] for audit in pair_audits}

    if ADDED_TYPE in audit_types:
        reasons.append("G8-77新增分析单元，必须确认边界和四维候选")
    if row["dimension"] == "科学论证" and row["present_label"] == "是":
        reasons.append("科学论证正例，触发V3强制实质复核")
    if row["dimension"] == "质疑创新" and row["present_label"] == "是":
        reasons.append("质疑创新正例，触发V3强制实质复核")
    if row["dimension"] == "模型建构" and row["present_label"] == "否":
        reasons.append("模型建构未出现，需核对是否只是调用题给或前问模型")
    if "论证关键词假阳性复审" in audit_types:
        reasons.append("题干含论证触发词但候选未出现，需区分背景与任务要求")
    if "创新关键词假阳性复审" in audit_types:
        reasons.append("题干含创新触发词但候选未出现，需区分变量范围与开放任务")
    if UNIFORM_TYPE in audit_types:
        reasons.append("同题多个小问标签完全相同，需排除整题复制")

    if reasons:
        return "P0", "；".join(reasons)
    if row["level"] == "L3":
        return "P1", "当前候选为L3，需核对是否满足多关系、多阶段或系统证据门槛"
    return "P2", "常规存在性、L1/L2或未出现边界复核"


def build_package_rows() -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    merged_fields, merged_rows = read_rows(MERGED)
    if merged_fields != CANDIDATE_FIELDS:
        raise ValueError("V3候选合并表字段与G8-78规范不一致")
    if len(merged_rows) != 884:
        raise ValueError(f"候选合并表应为884行，实际为{len(merged_rows)}行")

    _, audit_rows = read_rows(AUDIT)
    if len(audit_rows) != 57:
        raise ValueError(f"跨届审计表应为57行，实际为{len(audit_rows)}行")
    audit_by_item, audit_by_pair = build_audit_links(audit_rows)

    package_rows: list[dict[str, str]] = []
    rows_by_item: dict[str, list[dict[str, str]]] = defaultdict(list)
    for position, candidate in enumerate(merged_rows, start=1):
        item_id = candidate["item_id"]
        dimension = candidate["dimension"]
        pair_audits = audit_by_pair.get((item_id, dimension), [])
        priority, priority_reason = assign_priority(candidate, pair_audits)
        item_audits = audit_by_item.get(item_id, [])
        row = {
            "review_row_id": f"V3AR-{position:04d}",
            "review_priority": priority,
            "priority_reason": priority_reason,
            "linked_audit_ids": "；".join(
                dict.fromkeys(audit["audit_id"] for audit in item_audits)
            ),
            "linked_audit_types": "；".join(
                dict.fromkeys(audit["audit_type"] for audit in item_audits)
            ),
            **candidate,
            **{field: "" for field in REVIEW_FIELDS},
        }
        package_rows.append(row)
        rows_by_item[item_id].append(row)

    if len({(row["item_id"], row["dimension"]) for row in package_rows}) != 884:
        raise ValueError("作者复核表存在重复分析单元×维度键")
    if any(Counter(row["dimension"] for row in rows) != Counter(
        ("模型建构", "科学推理", "科学论证", "质疑创新")
    ) for rows in rows_by_item.values()):
        raise ValueError("作者复核表存在四维覆盖不完整的分析单元")

    item_rows: list[dict[str, str]] = []
    for item_rank, (item_id, rows) in enumerate(rows_by_item.items(), start=1):
        priorities = Counter(row["review_priority"] for row in rows)
        item_priority = min(
            priorities,
            key=lambda priority: PRIORITY_ORDER[priority],
        )
        audit_ids = "；".join(
            dict.fromkeys(
                audit["audit_id"] for audit in audit_by_item.get(item_id, [])
            )
        )
        audit_types = "；".join(
            dict.fromkeys(
                audit["audit_type"] for audit in audit_by_item.get(item_id, [])
            )
        )
        first = rows[0]
        candidate_summary = "；".join(
            f"{row['dimension']}={row['present_label']}/{row['level']}"
            for row in rows
        )
        item_rows.append(
            {
                "item_rank": f"{item_rank:03d}",
                "item_id": item_id,
                "competition_no": first["competition_no"],
                "year": first["year"],
                "question_no": first["question_no"],
                "subquestion_no": first["subquestion_no"],
                "item_priority": item_priority,
                "P0_dimension_rows": str(priorities["P0"]),
                "P1_dimension_rows": str(priorities["P1"]),
                "P2_dimension_rows": str(priorities["P2"]),
                "review_row_ids": "；".join(row["review_row_id"] for row in rows),
                "linked_audit_ids": audit_ids,
                "linked_audit_types": audit_types,
                "required_output": first["required_output"],
                "candidate_summary": candidate_summary,
                "item_text_path": first["item_text_path"],
                "solution_text_path": first["solution_text_path"],
                "question_location": first["question_location"],
                "solution_location": first["solution_location"],
                "current_status": "待作者逐维实质复核",
            }
        )

    if len(item_rows) != 221:
        raise ValueError(f"作者复核题目索引应为221行，实际为{len(item_rows)}行")
    return package_rows, item_rows


def main() -> None:
    package_rows, item_rows = build_package_rows()
    write_rows(OUTPUT, [*PACKAGE_FIELDS, *REVIEW_FIELDS], package_rows)
    write_rows(ITEM_INDEX, list(item_rows[0]), item_rows)
    priority_counts = Counter(row["review_priority"] for row in package_rows)
    item_priority_counts = Counter(row["item_priority"] for row in item_rows)
    print(f"review_rows={len(package_rows)}")
    print(f"item_rows={len(item_rows)}")
    print(f"dimension_priorities={dict(sorted(priority_counts.items()))}")
    print(f"item_priorities={dict(sorted(item_priority_counts.items()))}")
    print(OUTPUT.relative_to(ROOT))
    print(ITEM_INDEX.relative_to(ROOT))


if __name__ == "__main__":
    main()
