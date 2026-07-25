#!/usr/bin/env python3
"""Check current core-source status against the reconciliation boundary."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / "02_literature/reference_verification.csv"
CANDIDATES = ROOT / "09_quality/r01_candidate_references_mapping_v1.csv"
RECONCILIATION = ROOT / "09_quality/core_literature_status_reconciliation_20260725.md"
OUTPUT_CSV = ROOT / "09_quality/core_literature_status_reconciliation_qa_v1.csv"
OUTPUT_MD = ROOT / "09_quality/core_literature_status_reconciliation_qa_v1.md"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    ledger = {row["id"]: row for row in read_csv(LEDGER)}
    candidate_ids = {row["source_id"] for row in read_csv(CANDIDATES)}
    text = RECONCILIATION.read_text(encoding="utf-8")
    pcomp_read = {"PCOMP-002", "PCOMP-003", "PCOMP-004", "PCOMP-007", "PCOMP-008"}
    checks = [
        ("CORE-LIT-QA-01", "SOLO-001已读状态", ledger["SOLO-001"]["relevant_passage_checked"] == "是"),
        ("CORE-LIT-QA-02", "SOLO-001章节页码", "印刷页22至31" in ledger["SOLO-001"]["notes"]),
        ("CORE-LIT-QA-03", "SOLO-001进入候选链", "SOLO-001" in candidate_ids),
        ("CORE-LIT-QA-04", "SOLO-002仍非全文", ledger["SOLO-002"]["relevant_passage_checked"] != "是"),
        ("CORE-LIT-QA-05", "五篇PCOMP已读", all(ledger[source]["relevant_passage_checked"] == "是" for source in pcomp_read)),
        ("CORE-LIT-QA-06", "五篇PCOMP进入候选链", pcomp_read <= candidate_ids),
        ("CORE-LIT-QA-07", "PCOMP-001仍待读", ledger["PCOMP-001"]["relevant_passage_checked"] == "否"),
        ("CORE-LIT-QA-08", "PCOMP-005仍待读", ledger["PCOMP-005"]["relevant_passage_checked"] == "否"),
        ("CORE-LIT-QA-09", "对账保留E1边界", "E1页码级受限可用" in text),
        ("CORE-LIT-QA-10", "对账保留发布链边界", "独立发布链" in text),
        ("CORE-LIT-QA-11", "对账保留不外推边界", "学生能力、教学效果" in text),
    ]
    with OUTPUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["check_id", "check_item", "status"])
        for check_id, item, passed in checks:
            writer.writerow([check_id, item, "通过" if passed else "不通过"])
    failures = [check_id for check_id, _, passed in checks if not passed]
    OUTPUT_MD.write_text(
        "# 核心文献可读状态对账 QA\n\n"
        f"共{len(checks)}项检查，{'全部通过' if not failures else '不通过：' + '、'.join(failures)}。"
        "本QA只校验项目内来源状态、候选链和限制语的一致性，不验证副本授权、外部发布链、理论效度或人类参与者事实。\n",
        encoding="utf-8",
    )
    if failures:
        raise SystemExit("核心文献状态对账QA失败：" + ", ".join(failures))
    print(f"核心文献状态对账QA：{len(checks)}/{len(checks)}通过")


if __name__ == "__main__":
    main()
