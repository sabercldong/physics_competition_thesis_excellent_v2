#!/usr/bin/env python3
"""Validate that the final-reference backfill template is blank and aligned to its queue."""

from __future__ import annotations

import csv
from pathlib import Path

from build_r01_final_reference_backfill_template import BACKFILL_FIELDS, ROOT, read_rows, write_csv


QUEUE = ROOT / "09_quality/r01_final_reference_action_queue_20260725.csv"
TEMPLATE = ROOT / "09_quality/r01_final_reference_backfill_template_20260725.csv"
OUTPUT_CSV = ROOT / "09_quality/r01_final_reference_backfill_template_qa_20260725.csv"
OUTPUT_MD = ROOT / "09_quality/r01_final_reference_backfill_template_qa_20260725.md"


def main() -> None:
    queue_rows = read_rows(QUEUE)
    template_rows = read_rows(TEMPLATE)
    queue_keys = [(row["reference_number"], row["source_id"], row["bib_key"], row["priority"]) for row in queue_rows]
    template_keys = [(row["reference_number"], row["source_id"], row["bib_key"], row["priority"]) for row in template_rows]
    p1_count = sum(row["priority"] == "P1" for row in template_rows)
    p2_count = sum(row["priority"] == "P2" for row in template_rows)
    queue_p1_count = sum(row["priority"] == "P1" for row in queue_rows)
    queue_p2_count = sum(row["priority"] == "P2" for row in queue_rows)
    blank_count = sum(not any(row[field].strip() for field in BACKFILL_FIELDS) for row in template_rows)
    rows = [
        {"check_id": "RFR-BF-QA-01", "check_item": "队列与模板行数", "status": "通过" if len(template_rows) == len(queue_rows) == 39 else "不通过", "detail": f"模板{len(template_rows)}；队列{len(queue_rows)}"},
        {"check_id": "RFR-BF-QA-02", "check_item": "固定键与队列一致", "status": "通过" if template_keys == queue_keys else "不通过", "detail": f"一致{sum(a == b for a, b in zip(template_keys, queue_keys))}/{len(queue_keys)}"},
        {"check_id": "RFR-BF-QA-03", "check_item": "优先级分布与队列一致", "status": "通过" if p1_count == queue_p1_count and p2_count == queue_p2_count else "不通过", "detail": f"模板P1={p1_count}、P2={p2_count}；队列P1={queue_p1_count}、P2={queue_p2_count}"},
        {"check_id": "RFR-BF-QA-04", "check_item": "真实回填字段保持空白", "status": "通过" if blank_count == len(template_rows) else "不通过", "detail": f"{blank_count}/{len(template_rows)}行"},
        {"check_id": "RFR-BF-QA-05", "check_item": "模板和放行状态", "status": "通过" if all(row["template_status"] == "空白模板：待真实核对" and row["release_status"] == "不放行：待独立QA" for row in template_rows) else "不通过", "detail": "所有行保持空白模板与不放行"},
        {"check_id": "RFR-BF-QA-06", "check_item": "实际核对字段列完整", "status": "通过" if all(field in template_rows[0] for field in BACKFILL_FIELDS) else "不通过", "detail": f"{len(BACKFILL_FIELDS)}项字段"},
        {"check_id": "RFR-BF-QA-07", "check_item": "候选著录与用途边界继承", "status": "通过" if all(row["candidate_gbt_7714_working_entry"] and row["allowed_use_boundary"] and row["blocked_use_boundary"] for row in template_rows) else "不通过", "detail": f"完整{sum(bool(row['candidate_gbt_7714_working_entry'] and row['allowed_use_boundary'] and row['blocked_use_boundary']) for row in template_rows)}/{len(template_rows)}行"},
    ]
    write_csv(OUTPUT_CSV, rows)
    failures = [row for row in rows if row["status"] != "通过"]
    OUTPUT_MD.write_text(
        "# R01 最终参考文献回填模板 QA（2026-07-25）\n\n"
        f"{len(rows) - len(failures)}/{len(rows)}通过。该QA只验证模板与当前行动队列的结构一致和真实字段留空；不验证任何文献内容、版本、页码、学校格式或放行资格。\n",
        encoding="utf-8",
    )
    if failures:
        raise SystemExit("回填模板QA失败：" + ", ".join(row["check_id"] for row in failures))
    print(f"最终参考文献回填模板QA：{len(rows)}/{len(rows)}通过。")


if __name__ == "__main__":
    main()
