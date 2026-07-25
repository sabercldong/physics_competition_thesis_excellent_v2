#!/usr/bin/env python3
"""Build the CPHO35 subquestion score ledger from the user-provided rubric record."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
INDEX = ROOT / "03_corpus/item_index.csv"
OUTPUT = ROOT / "03_corpus/cpho35_score_rubric_v1.csv"

SOURCE_FILE = "/Users/dongxingxi/Downloads/2018年第35届全国中学生理复赛试题答案.pdf"
SOURCE_SHA256 = "6d622000fafa9c736e136ffd96a0f984a92c551381bac8b29ca48038c2b896cf"
SOURCE_LABEL = "用户提供的第35届评分标准副本"

# PDF pages are counted from the first page of the supplied 28-page PDF.  The
# Q05 alternate-solution pages are not used to duplicate its subquestion marks.
SCORES = {
    1: (3, (15, 25)),
    2: (6, (12, 8, 11, 9)),
    3: (9, (5, 23, 7, 5)),
    4: (12, (10, 10, 8, 12)),
    5: (15, (20, 9, 11)),
    6: (22, (13, 12, 15)),
    7: (25, (25, 15)),
    8: (28, (12, 8, 12, 8)),
}


def read_csv(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader), list(reader.fieldnames or [])


def main() -> None:
    rows, fieldnames = read_csv(INDEX)
    score_rows: list[dict[str, str]] = []
    expected_ids: set[str] = set()

    for question_no, (pdf_page, values) in SCORES.items():
        for subquestion_no, score in enumerate(values, start=1):
            item_id = f"CPHO35-Q{question_no:02d}-{subquestion_no}"
            expected_ids.add(item_id)
            score_rows.append(
                {
                    "item_id": item_id,
                    "competition_no": "35",
                    "year": "2018",
                    "question_no": str(question_no),
                    "subquestion_no": str(subquestion_no),
                    "question_score": "40",
                    "subquestion_score": str(score),
                    "score_source_pdf_page": str(pdf_page),
                    "score_source_location": f"第{question_no}题评分标准，第（{subquestion_no}）问",
                    "source_label": SOURCE_LABEL,
                    "source_file_external": SOURCE_FILE,
                    "source_sha256": SOURCE_SHA256,
                    "evidence_level": "E1",
                    "user_source_declaration": "用户声明该第35届答案/评分标准为官方副本；项目未独立核验发布链",
                    "provenance_status": "用户提供副本；发布/官方版本链未独立核验",
                    "usable_for": "第35届本项目题目级/小问级描述性分值元数据与受限敏感性分析",
                    "not_usable_for": "跨届分值比较或趋势、学生成绩/能力推断、发布者或官方版本真实性证明",
                    "notes": "第5题按主评分标准登记20/9/11；另列的替代解法评分不得重复计分。" if question_no == 5 else "按该题主评分标准登记。",
                }
            )

    index_ids = {row["item_id"] for row in rows if row["competition_no"] == "35"}
    if index_ids != expected_ids:
        missing = sorted(expected_ids - index_ids)
        extra = sorted(index_ids - expected_ids)
        raise SystemExit(f"第35届索引与评分台账不一致；缺失={missing}，多余={extra}")

    by_id = {row["item_id"]: row for row in score_rows}
    for row in rows:
        score = by_id.get(row["item_id"])
        if score is None:
            continue
        row["score"] = score["subquestion_score"]
        old_note = row.get("notes", "").strip()
        marker = "；G1-06-SCORE-RUBRIC-20260725："
        if marker in old_note:
            old_note = old_note.split(marker, 1)[0]
        note = (
            f"G1-06-SCORE-RUBRIC-20260725：{SOURCE_LABEL}，PDF第{score['score_source_pdf_page']}页，"
            f"第{score['question_no']}题第（{score['subquestion_no']}）问{score['subquestion_score']}分；"
            "仅作第35届项目内分值元数据。来源发布/官方版本链未独立核验，不作跨届比较、趋势或学生推断。"
        )
        row["notes"] = f"{old_note}；{note}" if old_note else note

    with OUTPUT.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(score_rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(score_rows)
    with INDEX.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    print(f"已生成{OUTPUT.relative_to(ROOT)}：{len(score_rows)}行；第35届小问分值已同步至item_index.csv")


if __name__ == "__main__":
    main()
