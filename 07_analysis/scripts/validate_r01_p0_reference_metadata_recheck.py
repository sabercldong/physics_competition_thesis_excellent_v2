#!/usr/bin/env python3
"""Validate the bounded metadata recheck for six priority references."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "09_quality/r01_p0_reference_metadata_recheck_20260725.csv"
OUTPUT_CSV = ROOT / "09_quality/r01_p0_reference_metadata_recheck_qa_v1.csv"
OUTPUT_MD = ROOT / "09_quality/r01_p0_reference_metadata_recheck_qa_v1.md"
EXPECTED_IDS = {"CS-001", "ST-002", "ST-003", "ST-005", "ST-006", "METH-004"}


def main() -> None:
    with INPUT.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    ids = {row["source_id"] for row in rows}
    required_fields = [
        "metadata_recheck_status", "metadata_source", "metadata_source_url",
        "full_text_or_primary_version_status", "location_status", "allowed_use",
        "final_reference_ready", "remaining_requirement",
    ]
    checks = [
        ("P0META-QA-01", "六项来源覆盖", ids == EXPECTED_IDS, f"{len(ids)}/6"),
        ("P0META-QA-02", "来源唯一", len(rows) == len(ids), f"{len(rows)}行/{len(ids)}个ID"),
        ("P0META-QA-03", "元数据复核状态", all(row["metadata_recheck_status"] == "已复核" for row in rows), "六项均已登记"),
        ("P0META-QA-04", "最终参考文献边界", all(row["final_reference_ready"] == "否" for row in rows), "六项均未提前放行"),
        ("P0META-QA-05", "字段完整", all(all(row[field].strip() for field in required_fields) for row in rows), "关键字段非空"),
        ("P0META-QA-06", "ST-002补充材料边界", "SOM" in next(row["remaining_requirement"] for row in rows if row["source_id"] == "ST-002"), "需另核官方补充材料"),
        ("P0META-QA-07", "ST-003图表边界", "图表" in next(row["remaining_requirement"] for row in rows if row["source_id"] == "ST-003"), "具体图表另行定位"),
        ("P0META-QA-08", "METH-004版本边界", "postprint" in next(row["full_text_or_primary_version_status"] for row in rows if row["source_id"] == "METH-004"), "仓储版不等于VOR"),
        ("P0META-QA-09", "课程框架禁推断", all("外部效度" not in row["allowed_use"] for row in rows if row["source_id"] in {"CS-001", "ST-006"}), "允许用途未越界"),
    ]
    qa_rows = [
        {"check_id": check_id, "check_item": item, "status": "通过" if passed else "不通过", "detail": detail}
        for check_id, item, passed, detail in checks
    ]
    with OUTPUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(qa_rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(qa_rows)
    failures = [row["check_id"] for row in qa_rows if row["status"] != "通过"]
    OUTPUT_MD.write_text(
        "# R01 六项优先来源公开元数据复核 QA（V1）\n\n"
        f"{len(qa_rows) - len(failures)}/{len(qa_rows)}通过。"
        "本QA仅核验台账覆盖、字段和边界，不核验学校当期规则、全文版本逐页一致性或最终参考文献资格。\n",
        encoding="utf-8",
    )
    if failures:
        raise SystemExit("P0来源公开元数据复核QA失败：" + ", ".join(failures))
    print(f"R01六项优先来源公开元数据复核QA：{len(qa_rows)}/{len(qa_rows)}通过")


if __name__ == "__main__":
    main()
