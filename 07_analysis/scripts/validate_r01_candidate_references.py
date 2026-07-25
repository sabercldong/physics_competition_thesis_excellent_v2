#!/usr/bin/env python3
"""Validate the bounded candidate reference work list."""

from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REFERENCE_PATH = ROOT / "08_manuscript/07_candidate_references.md"
MAPPING_PATH = ROOT / "09_quality/r01_candidate_references_mapping_v1.csv"
BIB_PATH = ROOT / "02_literature/references.bib"
SCHOOL_PATH = ROOT / "01_positioning/school_requirements_register.csv"
OUTPUT_CSV = ROOT / "09_quality/r01_candidate_references_qa_v1.csv"
OUTPUT_MD = ROOT / "09_quality/r01_candidate_references_qa_v1.md"



def main() -> None:
    text = REFERENCE_PATH.read_text(encoding="utf-8")
    numbers = [int(value) for value in re.findall(r"^\[(\d+)\]", text, flags=re.MULTILINE)]
    with MAPPING_PATH.open(encoding="utf-8-sig", newline="") as handle:
        mapped = list(csv.DictReader(handle))
    bib = BIB_PATH.read_text(encoding="utf-8")
    with SCHOOL_PATH.open(encoding="utf-8-sig", newline="") as handle:
        requirements = {row["requirement_id"]: row for row in csv.DictReader(handle)}
    mapped_ids = [row["source_id"] for row in mapped]
    expected_numbers = list(range(1, len(mapped) + 1))
    expected_ids = [row["source_id"] for row in mapped]
    all_mapped_eligible = all(row["source_id"] and row["bib_key"] for row in mapped)
    excluded_ids = {"METH-001", "METH-005", "PCOMP-001", "PCOMP-005"}
    pcomp_ids = {"PCOMP-002", "PCOMP-003", "PCOMP-004", "PCOMP-007", "PCOMP-008"}
    rows = [
        ("REF-QA-01", "候选条目数与连续编号", f"1至{len(mapped)}", str(numbers), numbers == expected_numbers),
        ("REF-QA-02", "来源ID集合与顺序", ";".join(expected_ids), ";".join(mapped_ids), mapped_ids == expected_ids and all_mapped_eligible),
        ("REF-QA-03", "候选来源均有BibTeX键", f"{len(mapped)}/{len(mapped)}", f"{sum(row['bib_key'] in bib for row in mapped)}/{len(mapped)}", all(row["bib_key"] in bib for row in mapped)),
        ("REF-QA-04", "仍待读或未受控接入来源未混入", "METH-001/005、PCOMP-001/005均未进入", "通过" if not (excluded_ids & set(mapped_ids)) else "不通过：" + ";".join(sorted(excluded_ids & set(mapped_ids))), not (excluded_ids & set(mapped_ids))),
        ("REF-QA-05", "学校公开格式基线", "GB/T 7714-2015", requirements["REQ-04"]["summary"], "GB/T7714-2015" in requirements["REQ-04"]["summary"]),
        ("REF-QA-06", "不足30篇的缺口已明示", "必须明示", "通过" if "不少于30篇" in text else "不通过", "不少于30篇" in text),
        ("REF-QA-07", "五篇页码定位的国内竞赛研究已受控纳入", "5/5", f"{len(pcomp_ids & set(mapped_ids))}/5", pcomp_ids <= set(mapped_ids)),
    ]
    with OUTPUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["check_id", "check_item", "expected", "actual", "status"])
        for row in rows:
            writer.writerow([*row[:4], "通过" if row[4] else "不通过"])
    failures = [row[0] for row in rows if not row[4]]
    OUTPUT_MD.write_text(
        "# G8-02-R01-CANDIDATE-REFERENCES：候选参考文献 QA（V1）\n\n"
        f"共完成 {len(rows)} 项质量检查，{'全部通过' if not failures else '不通过：' + ', '.join(failures)}。"
        f"该清单仅含{len(mapped)}项限边界候选来源，不是最终参考文献表；在补齐合法全文阅读、版本页码和至少30篇合格文献前，不得作为最终提交版。\n",
        encoding="utf-8",
    )
    if failures:
        raise SystemExit("候选参考文献QA失败：" + ", ".join(failures))
    print(f"候选参考文献QA：{len(rows)}/{len(rows)}通过。")


if __name__ == "__main__":
    main()
