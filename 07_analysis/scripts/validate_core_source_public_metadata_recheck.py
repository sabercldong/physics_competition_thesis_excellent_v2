#!/usr/bin/env python3
"""Validate public-metadata corrections without treating them as full-text evidence."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / "02_literature/reference_verification.csv"
MATRIX = ROOT / "02_literature/literature_matrix.csv"
RECHECK = ROOT / "02_literature/core_source_public_metadata_recheck_20260725.md"
OUTPUT_CSV = ROOT / "09_quality/core_source_public_metadata_recheck_qa_v1.csv"
OUTPUT_MD = ROOT / "09_quality/core_source_public_metadata_recheck_qa_v1.md"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    ledger = {row["id"]: row for row in read_csv(LEDGER)}
    matrix = {row["id"]: row for row in read_csv(MATRIX)}
    text = RECHECK.read_text(encoding="utf-8")
    checks = [
        ("META-QA-01", "SOLO-002仍非全文", ledger["SOLO-002"]["relevant_passage_checked"] != "是"),
        ("META-QA-02", "PCOMP-001题录已核验", ledger["PCOMP-001"]["metadata_verified"].startswith("是")),
        ("META-QA-03", "PCOMP-001仍待读", ledger["PCOMP-001"]["relevant_passage_checked"] == "否"),
        ("META-QA-04", "PCOMP-005作者更正", ledger["PCOMP-005"]["authors"] == "张彦；杜宁；赵松峰"),
        ("META-QA-05", "PCOMP-005原始著录更正", ledger["PCOMP-005"]["raw_reference"].startswith("张彦,")),
        ("META-QA-06", "PCOMP-005矩阵作者一致", matrix["LM-PCOMP-005"]["authors"] == "张彦；杜宁；赵松峰"),
        ("META-QA-07", "PCOMP-005仍待读", ledger["PCOMP-005"]["relevant_passage_checked"] == "否"),
        ("META-QA-08", "公开入口记录完整", all(token in text for token in ["journals.sagepub.com", "did=2021", "did=2022"])),
        ("META-QA-09", "边界未升级", "不以摘要或目录替代实际阅读" in text),
    ]
    with OUTPUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["check_id", "check_item", "status"])
        for check_id, item, passed in checks:
            writer.writerow([check_id, item, "通过" if passed else "不通过"])
    failures = [check_id for check_id, _, passed in checks if not passed]
    OUTPUT_MD.write_text(
        "# 核心来源公开元数据复核 QA\n\n"
        f"共{len(checks)}项检查，{'全部通过' if not failures else '不通过：' + '、'.join(failures)}。"
        "本QA只核验项目内元数据更正与全文限制语，不验证外部发布链、全文内容或理论效度。\n",
        encoding="utf-8",
    )
    if failures:
        raise SystemExit("核心来源公开元数据复核QA失败：" + ", ".join(failures))
    print(f"核心来源公开元数据复核QA：{len(checks)}/{len(checks)}通过")


if __name__ == "__main__":
    main()
