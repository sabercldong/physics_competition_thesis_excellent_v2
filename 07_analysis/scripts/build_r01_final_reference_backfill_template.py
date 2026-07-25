#!/usr/bin/env python3
"""Build a blank, auditable backfill template for the current final-reference queue."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
QUEUE = ROOT / "09_quality/r01_final_reference_action_queue_20260725.csv"
MAPPING = ROOT / "09_quality/r01_candidate_references_mapping_v1.csv"
OUTPUT_CSV = ROOT / "09_quality/r01_final_reference_backfill_template_20260725.csv"
OUTPUT_MD = ROOT / "09_quality/r01_final_reference_backfill_instructions_20260725.md"

BACKFILL_FIELDS = [
    "actual_reviewer_or_code",
    "actual_review_date",
    "access_channel_or_copy_locator",
    "version_checked",
    "stable_locator_or_file_checksum",
    "pages_or_sections_checked",
    "manuscript_citation_location_checked",
    "bibliographic_fields_verified",
    "page_or_section_support_verified",
    "school_format_rule_locator",
    "review_decision",
    "remaining_issue",
    "evidence_attachment_or_notes_path",
    "reviewer_statement",
]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    queue_rows = read_rows(QUEUE)
    mapping_rows = read_rows(MAPPING)
    mapping_by_source = {row["source_id"]: row for row in mapping_rows}

    rows: list[dict[str, str]] = []
    for queue in queue_rows:
        source_id = queue["source_id"]
        mapping = mapping_by_source[source_id]
        row = {
            "reference_number": queue["reference_number"],
            "source_id": source_id,
            "bib_key": queue["bib_key"],
            "priority": queue["priority"],
            "current_final_status": queue["current_final_status"],
            "remaining_verification": queue["remaining_verification"],
            "minimum_next_action": queue["minimum_next_action"],
            "completion_evidence_required": queue["completion_evidence_required"],
            "prohibited_shortcut": queue["prohibited_shortcut"],
            "candidate_gbt_7714_working_entry": mapping["gbt_7714_candidate_entry"],
            "allowed_use_boundary": mapping["allowed_use"],
            "blocked_use_boundary": mapping["blocked_use"],
            "template_status": "空白模板：待真实核对",
            "release_status": "不放行：待独立QA",
        }
        row.update({field: "" for field in BACKFILL_FIELDS})
        rows.append(row)

    write_csv(OUTPUT_CSV, rows)
    p1_count = sum(row["priority"] == "P1" for row in rows)
    p2_count = sum(row["priority"] == "P2" for row in rows)
    lines = [
        "# R01 最终参考文献真实核对回填说明（2026-07-25）", "",
        "## 用途与边界", "",
        f"本说明对应 {len(rows)} 项当前候选参考文献（P1={p1_count}，P2={p2_count}）。它只提供真实核对后的回填入口，不构成最终参考文献表，也不替代学院当期格式要求、作者或导师决定。", "",
        "不得根据候选编号、BibTeX、DOI、摘要、搜索结果、工作稿渲染或智能体输出填写任何实际核对字段。取得材料、阅读或登记的行为本身也不等于可放行。", "",
        "## 回填步骤", "",
        "1. 仅在合法访问或持有可核验副本后复制本CSV，固定字段不得修改。",
        "2. 每行登记实际核对人或代号、实际日期、版本/稳定定位、所核页码或章节、正文引用位置和学校格式规则来源。",
        "3. `review_decision` 只能填：`充分支持最终著录`、`需补充材料`、`不支持当前著录` 或 `待核实`。没有真实证据时填 `待核实`，不得留作默认通过。",
        "4. `page_or_section_support_verified` 只说明本论文实际使用的主张或定位是否可回查；不能据此扩展为理论、方法或教学结论。",
        "5. 回填后交由独立QA检查。只有格式、来源、版本、正文定位和学院规则均通过时，才可另设任务生成最终文后表。", "",
        "## 必填条件", "",
        "所有实际回填字段都必须基于真实核对。P1项至少需完成版本、页码/章节、正文定位和支持范围核对；P2项仍需待学院当期格式规则取得后完成著录格式核对。涉及受限副本时只登记合法访问渠道或私有定位，不将受版权保护全文复制进项目仓库。", "",
        "## 当前不可声称", "",
        f"当前 {len(rows)} 项均为候选且未最终放行。不得称参考文献已经定稿、学院格式已合规、页码已核验，或由此推断评分过程独立性、框架效度、学生能力或教学效果。",
    ]
    OUTPUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"生成最终参考文献回填模板：{len(rows)}项；P1={p1_count}，P2={p2_count}。")


if __name__ == "__main__":
    main()
