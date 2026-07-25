#!/usr/bin/env python3
"""Validate the bounded intake of the six user-provided external PDFs."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
INTAKE = ROOT / "02_literature/user_provided_fulltext_intake_20260725.csv"
LEDGER = ROOT / "02_literature/reference_verification.csv"
MATRIX = ROOT / "02_literature/literature_matrix.csv"
OUTPUT_CSV = ROOT / "09_quality/user_provided_fulltext_intake_qa_20260725.csv"
OUTPUT_MD = ROOT / "09_quality/user_provided_fulltext_intake_qa_20260725.md"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    intake = {row["source_id"]: row for row in read_csv(INTAKE)}
    ledger = {row["id"]: row for row in read_csv(LEDGER)}
    matrix = {row["id"].removeprefix("LM-"): row for row in read_csv(MATRIX)}
    expected = {"SOLO-001", "SOLO-002", "PCOMP-001", "METH-001", "METH-002", "METH-003"}
    checks = [
        ("UPFT-QA-01", "六份来源完整登记", expected == set(intake)),
        ("UPFT-QA-02", "所有副本不作为最终著录", all(row["formal_reference_status"] != "最终参考文献" for row in intake.values())),
        ("UPFT-QA-03", "SOLO-001仅去重", intake["SOLO-001"]["reading_status"].startswith("不重复登记")),
        ("UPFT-QA-04", "METH-001版本不匹配保留", intake["METH-001"]["record_match"].startswith("不匹配") and ledger["METH-001"]["relevant_passage_checked"] == "否"),
        ("UPFT-QA-05", "四个版本匹配来源已读", all(ledger[source]["relevant_passage_checked"] == "是" for source in {"SOLO-002", "PCOMP-001", "METH-002", "METH-003"})),
        ("UPFT-QA-06", "矩阵状态与台账一致", all((matrix[source]["full_text_read"] == "是") == (ledger[source]["relevant_passage_checked"] == "是") for source in expected)),
        ("UPFT-QA-07", "METH-002不设阈值", "通过线" in intake["METH-002"]["prohibited_project_use"]),
        ("UPFT-QA-08", "METH-003不设阈值", "阈值" in intake["METH-003"]["prohibited_project_use"]),
        ("UPFT-QA-09", "SOLO-002不外推框架效度", "框架效度" in intake["SOLO-002"]["prohibited_project_use"]),
        ("UPFT-QA-10", "PCOMP-001不迁移预赛结论", "预赛数据" in intake["PCOMP-001"]["prohibited_project_use"]),
    ]
    with OUTPUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["check_id", "check_item", "status"])
        for check_id, item, passed in checks:
            writer.writerow([check_id, item, "通过" if passed else "不通过"])
    failures = [check_id for check_id, _, passed in checks if not passed]
    OUTPUT_MD.write_text(
        "# 用户提供外部全文接收 QA（2026-07-25）\n\n"
        f"共{len(checks)}项检查，{'全部通过' if not failures else '不通过：' + '、'.join(failures)}。"
        "本QA只验证项目内登记、版本差异和禁止迁移边界；不核验外部副本的授权、发布链或任何研究结论。\n",
        encoding="utf-8",
    )
    if failures:
        raise SystemExit("用户提供外部全文接收QA失败：" + ", ".join(failures))
    print(f"用户提供外部全文接收QA：{len(checks)}/{len(checks)}通过")


if __name__ == "__main__":
    main()
