#!/usr/bin/env python3
"""Validate the bounded six-item candidate reference list."""

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
EXPECTED_IDS = ["CS-001", "ST-002", "ST-003", "ST-005", "ST-006", "METH-004"]


def main() -> None:
    text = REFERENCE_PATH.read_text(encoding="utf-8")
    numbers = [int(value) for value in re.findall(r"^\[(\d+)\]", text, flags=re.MULTILINE)]
    with MAPPING_PATH.open(encoding="utf-8-sig", newline="") as handle:
        mapped = list(csv.DictReader(handle))
    bib = BIB_PATH.read_text(encoding="utf-8")
    with SCHOOL_PATH.open(encoding="utf-8-sig", newline="") as handle:
        requirements = {row["requirement_id"]: row for row in csv.DictReader(handle)}
    mapped_ids = [row["source_id"] for row in mapped]
    rows = [
        ("REF-QA-01", "候选条目数与连续编号", "1至6", str(numbers), numbers == list(range(1, 7))),
        ("REF-QA-02", "来源ID集合", ";".join(EXPECTED_IDS), ";".join(mapped_ids), mapped_ids == EXPECTED_IDS),
        ("REF-QA-03", "候选来源均有BibTeX键", "6/6", f"{sum('@' in bib and row['bib_key'] in bib for row in mapped)}/6", all(row["bib_key"] in bib for row in mapped)),
        ("REF-QA-04", "待读全文来源未混入", "Biggs/PCOMP/METH-001至003均不出现", "通过" if all(item not in text for item in ["Biggs", "PCOMP", "METH-001", "METH-002", "METH-003"]) else "不通过", all(item not in text for item in ["Biggs", "PCOMP", "METH-001", "METH-002", "METH-003"])),
        ("REF-QA-05", "学校公开格式基线", "GB/T 7714-2015", requirements["REQ-04"]["summary"], "GB/T7714-2015" in requirements["REQ-04"]["summary"]),
        ("REF-QA-06", "不足30篇的缺口已明示", "必须明示", "通过" if "不少于30篇" in text else "不通过", "不少于30篇" in text),
    ]
    with OUTPUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["check_id", "check_item", "expected", "actual", "status"])
        for row in rows:
            writer.writerow([*row[:4], "通过" if row[4] else "不通过"])
    failures = [row[0] for row in rows if not row[4]]
    OUTPUT_MD.write_text(
        "# G8-02-R01-CANDIDATE-REFERENCES：候选参考文献 QA（V1）\n\n"
        f"共检查 {len(rows)} 项，{'全部通过' if not failures else '不通过：' + ', '.join(failures)}。"
        "该清单仅含六项限边界候选来源，不是最终参考文献表；在补齐合法全文阅读、版本页码和至少30篇合格文献前，不得作为最终提交版。\n",
        encoding="utf-8",
    )
    if failures:
        raise SystemExit("候选参考文献QA失败：" + ", ".join(failures))
    print(f"候选参考文献QA：{len(rows)}/{len(rows)}通过。")


if __name__ == "__main__":
    main()
