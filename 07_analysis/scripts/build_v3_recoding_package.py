#!/usr/bin/env python3
"""Build the V3 blank recoding sheet and the separate P0 review package."""

from __future__ import annotations

import csv
import hashlib
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
INDEX = ROOT / "03_corpus/item_index.csv"
SCREENING = ROOT / "09_quality/正式编码边界冲突程序筛查_G8-63.csv"
BLANK_OUTPUT = ROOT / "07_analysis/data/科学思维正式重编码空白表_V3.csv"
P0_OUTPUT = ROOT / "09_quality/高风险边界案例实质复审包_V3.csv"
DIMENSIONS = ("模型建构", "科学推理", "科学论证", "质疑创新")


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def item_text_path(item_id: str) -> Path:
    match = re.match(r"(CPHO\d+-Q\d+)", item_id)
    if not match:
        raise ValueError(f"无法从item_id解析材料编号: {item_id}")
    return ROOT / "03_corpus/item_texts" / f"{match.group(1)}.md"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
            lineterminator="\n",
            extrasaction="ignore",
        )
        writer.writeheader()
        writer.writerows(rows)


def build_blank_rows(index_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for item in index_rows:
        source = item_text_path(item["item_id"])
        if not source.exists():
            raise FileNotFoundError(source)
        source_relative = str(source.relative_to(ROOT))
        source_hash = sha256(source)
        for dimension in DIMENSIONS:
            rows.append(
                {
                    "item_id": item["item_id"],
                    "competition_no": item["competition_no"],
                    "year": item["year"],
                    "question_no": item["question_no"],
                    "subquestion_no": item["subquestion_no"],
                    "dimension": dimension,
                    "analysis_unit": item["analysis_unit"],
                    "item_text_path": source_relative,
                    "item_text_sha256": source_hash,
                    "page_paper": item["page_paper"],
                    "page_solution": item["page_solution"],
                    "required_output": "",
                    "question_quote": "",
                    "question_location": "",
                    "solution_quote": "",
                    "solution_location": "",
                    "necessary_cognitive_activity": "",
                    "present_label": "",
                    "level": "",
                    "decision_reason": "",
                    "adjacent_level_exclusion": "",
                    "confidence": "",
                    "coder_id": "",
                    "coding_date": "",
                    "review_status": "",
                    "notes": "",
                }
            )
    return rows


def build_p0_rows(screening_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in screening_rows:
        if row["priority"] != "P0":
            continue
        source = item_text_path(row["item_id"])
        rows.append(
            {
                "priority": row["priority"],
                "item_id": row["item_id"],
                "dimension": row["dimension"],
                "historical_present": row["current_present"],
                "historical_level": row["current_level"],
                "screening_reason": row["flag_reason"],
                "item_text_path": str(source.relative_to(ROOT)),
                "question_quote_for_screening": row["question_quote"],
                "answer_structure_for_screening": row["answer_structure"],
                "reviewed_question_quote": "",
                "reviewed_question_location": "",
                "reviewed_solution_quote": "",
                "reviewed_solution_location": "",
                "necessary_cognitive_activity": "",
                "v3_present_label": "",
                "v3_level": "",
                "v3_decision_reason": "",
                "adjacent_level_exclusion": "",
                "reviewer_id": "",
                "review_date": "",
                "review_status": "",
            }
        )
    return rows


def main() -> None:
    index_rows = read_rows(INDEX)
    if len(index_rows) != 219:
        raise ValueError(f"item_index应为219行，实际为{len(index_rows)}行")
    if len({row["item_id"] for row in index_rows}) != 219:
        raise ValueError("item_index存在重复item_id")

    blank_rows = build_blank_rows(index_rows)
    blank_fields = list(blank_rows[0])
    write_rows(BLANK_OUTPUT, blank_fields, blank_rows)

    p0_rows = build_p0_rows(read_rows(SCREENING))
    if len(p0_rows) != 21:
        raise ValueError(f"P0复审包应为21行，实际为{len(p0_rows)}行")
    write_rows(P0_OUTPUT, list(p0_rows[0]), p0_rows)

    print(f"blank_rows={len(blank_rows)}")
    print(f"p0_rows={len(p0_rows)}")
    print(BLANK_OUTPUT.relative_to(ROOT))
    print(P0_OUTPUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
