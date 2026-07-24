#!/usr/bin/env python3
"""Validate the page-level SOLO-001 reading note and its evidence boundaries."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
NOTE = ROOT / "02_literature/solo_original_fulltext_reading_notes_20260725.md"
REFERENCE_LEDGER = ROOT / "02_literature/reference_verification.csv"
LITERATURE_MATRIX = ROOT / "02_literature/literature_matrix.csv"
CLAIMS = ROOT / "09_quality/claim_evidence_matrix.csv"
OUTPUT = ROOT / "09_quality/solo_original_fulltext_read_qa_v1.csv"
REPORT = ROOT / "09_quality/solo_original_fulltext_read_qa_v1.md"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    note = NOTE.read_text(encoding="utf-8-sig") if NOTE.is_file() else ""
    ledger = {row["id"]: row for row in read_csv(REFERENCE_LEDGER)}
    matrix = {row["id"]: row for row in read_csv(LITERATURE_MATRIX)}
    claims = {row["claim_id"]: row for row in read_csv(CLAIMS)}
    checks: list[tuple[str, str, bool, str]] = []

    def check(check_id: str, item: str, passed: bool, source: str) -> None:
        checks.append((check_id, item, passed, source))

    check("SOLO-READ-QA-01", "阅读记录存在", NOTE.is_file(), NOTE.name)
    check("SOLO-READ-QA-02", "记录身份哈希、PDF页与印刷页范围", all(token in note for token in ("733f5f84", "PDF共238页", "PDF页26至35", "印刷页22至31")), NOTE.name)
    check("SOLO-READ-QA-03", "记录HCS与特定反应结构的区分", "假设认知结构（HCS）" in note and "特定学习任务" in note, NOTE.name)
    check("SOLO-READ-QA-04", "记录五类反应且区分任务要求", all(token in note for token in ("前结构", "单点结构", "多点结构", "关联结构", "抽象拓展", "任务要求")), NOTE.name)
    check("SOLO-READ-QA-05", "明确前结构不进入任务等级", "项目不设置“前结构”任务要求等级" in note, NOTE.name)
    check("SOLO-READ-QA-06", "保留学生表现和外部效度边界", all(token in note for token in ("学生真实SOLO表现", "外部效度", "教学效果")), NOTE.name)
    solo = ledger.get("SOLO-001", {})
    check("SOLO-READ-QA-07", "文献台账登记可读全文与相关页", solo.get("full_text_available", "").startswith("是") and solo.get("relevant_passage_checked") == "是", REFERENCE_LEDGER.name)
    matrix_row = matrix.get("LM-SOLO-001", {})
    check("SOLO-READ-QA-08", "文献矩阵登记页码级边界", "印刷页22至31" in matrix_row.get("main_findings", "") and "任务要求" in matrix_row.get("limitations", ""), LITERATURE_MATRIX.name)
    claim = claims.get("C2-03A", {})
    check("SOLO-READ-QA-09", "主张矩阵升级为原书页码级证据", claim.get("evidence_level") == "E2" and "印刷页22至31" in claim.get("evidence_location", ""), CLAIMS.name)
    check("SOLO-READ-QA-10", "不将1989论文误记为已读", "SOLO-002" in note and "仍待获得" in note, NOTE.name)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(("check_id", "check_item", "status", "source"))
        for check_id, item, passed, source in checks:
            writer.writerow((check_id, item, "通过" if passed else "不通过", source))
    failures = [check_id for check_id, _, passed, _ in checks if not passed]
    REPORT.write_text(
        "# SOLO-001 原书关键章节阅读QA\n\n"
        f"检查结果：{len(checks) - len(failures)}/{len(checks)}通过。\n\n"
        "本QA只验证原书关键章节的页码阅读记录、台账与理论边界是否一致；"
        "不验证用户声明的图书馆授权过程，不证明1989年论文已读，也不验证本项目框架效度、学生能力或教学效果。\n",
        encoding="utf-8",
    )
    if failures:
        raise SystemExit("SOLO原书阅读QA未通过：" + ", ".join(failures))
    print(f"SOLO原书关键章节阅读QA：{len(checks)}/{len(checks)}通过")


if __name__ == "__main__":
    main()
