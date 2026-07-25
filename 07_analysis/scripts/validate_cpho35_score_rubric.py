#!/usr/bin/env python3
"""Validate the internal consistency and stated limits of the CPHO35 score ledger."""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
INDEX = ROOT / "03_corpus/item_index.csv"
LEDGER = ROOT / "03_corpus/cpho35_score_rubric_v1.csv"
OUTPUT = ROOT / "09_quality/cpho35_score_rubric_qa_v1.csv"
REPORT = ROOT / "09_quality/cpho35_score_rubric_qa_v1.md"
SOURCE_SHA256 = "6d622000fafa9c736e136ffd96a0f984a92c551381bac8b29ca48038c2b896cf"
EXPECTED = {1: (15, 25), 2: (12, 8, 11, 9), 3: (5, 23, 7, 5), 4: (10, 10, 8, 12), 5: (20, 9, 11), 6: (13, 12, 15), 7: (25, 15), 8: (12, 8, 12, 8)}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    ledger = read_csv(LEDGER)
    index = read_csv(INDEX)
    checks: list[tuple[str, str, bool, str]] = []

    def check(check_id: str, item: str, passed: bool, source: str) -> None:
        checks.append((check_id, item, passed, source))

    expected_ids = {f"CPHO35-Q{q:02d}-{s}" for q, scores in EXPECTED.items() for s in range(1, len(scores) + 1)}
    ledger_ids = {row["item_id"] for row in ledger}
    index_scores = {row["item_id"]: row["score"] for row in index if row["competition_no"] == "35"}
    check("SCORE35-QA-01", "台账恰有26行", len(ledger) == 26, LEDGER.name)
    check("SCORE35-QA-02", "台账与第35届分析单元一一对应", ledger_ids == expected_ids == set(index_scores), f"{LEDGER.name}; {INDEX.name}")
    check("SCORE35-QA-03", "来源哈希一致", all(row["source_sha256"] == SOURCE_SHA256 for row in ledger), LEDGER.name)
    check("SCORE35-QA-04", "来源页码、位置与E1边界完整", all(row["score_source_pdf_page"] and row["score_source_location"] and row["evidence_level"] == "E1" for row in ledger), LEDGER.name)
    check("SCORE35-QA-05", "未误称官网附件已逐文件核验", all("404" in row["provenance_status"] and "未逐文件核验" in row["provenance_status"] for row in ledger), LEDGER.name)
    check("SCORE35-QA-06", "记录用户官网来源声明与附件不可复查边界", all("用户声明" in row["user_source_declaration"] and "官网" in row["user_source_declaration"] and "404" in row["user_source_declaration"] for row in ledger), LEDGER.name)
    check("SCORE35-QA-07", "限制跨届与学生推断", all("跨届" in row["not_usable_for"] and "学生" in row["not_usable_for"] for row in ledger), LEDGER.name)

    by_question: dict[int, list[int]] = defaultdict(list)
    for row in ledger:
        by_question[int(row["question_no"])].append(int(row["subquestion_score"]))
    for question_no, expected_scores in EXPECTED.items():
        actual = tuple(by_question[question_no])
        check(f"SCORE35-QA-{question_no + 7:02d}", f"第{question_no}题分问分值与台账规则一致且合计40分", actual == expected_scores and sum(actual) == 40, LEDGER.name)
    check("SCORE35-QA-16", "八题合计320分", sum(int(row["subquestion_score"]) for row in ledger) == 320, LEDGER.name)
    check("SCORE35-QA-17", "item_index分值与台账一致", all(index_scores.get(row["item_id"]) == row["subquestion_score"] for row in ledger), INDEX.name)
    check("SCORE35-QA-18", "第5题替代解法不重复计分", tuple(by_question[5]) == (20, 9, 11), LEDGER.name)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(("check_id", "check_item", "status", "source"))
        for check_id, item, passed, source in checks:
            writer.writerow((check_id, item, "通过" if passed else "不通过", source))
    failures = [check_id for check_id, _, passed, _ in checks if not passed]
    REPORT.write_text(
        "# 第35届评分标准台账QA\n\n"
        f"检查结果：{len(checks) - len(failures)}/{len(checks)}通过。\n\n"
        "本QA只验证项目内26个分析单元、分问分值、总分、来源哈希、页码字段及使用边界的一致性。"
        "它不独立验证用户提供PDF的发布者、授权、官方版本链或任何人工过程；分值不得用于跨届比较、趋势、学生成绩或能力推断。\n",
        encoding="utf-8",
    )
    if failures:
        raise SystemExit("第35届评分台账QA未通过：" + ", ".join(failures))
    print(f"第35届评分标准台账QA：{len(checks)}/{len(checks)}通过")


if __name__ == "__main__":
    main()
