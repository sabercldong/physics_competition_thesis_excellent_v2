from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
KEYS = ["item_id", "competition_no", "year", "question_no", "subquestion_no", "dimension"]
WORK_FIELDS = [
    "reviewer_id",
    "review_date",
    "source_checked",
    "question_trigger_quote",
    "question_location",
    "solution_step_quote",
    "solution_location",
    "evidence_sufficiency",
    "rechecked_present",
    "rechecked_level",
    "adjacent_level_exclusion",
    "recheck_decision",
    "reviewer_statement",
]


def resolve(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="生成R01全量逐条证据补正回填表；不改动任何裁决。")
    parser.add_argument("--final", default="07_analysis/data/final_coding.csv")
    parser.add_argument("--item-index", default="03_corpus/item_index.csv")
    parser.add_argument("--output", default="07_analysis/data/rater_returns/templates/R01/r01_evidence_supplement_template.csv")
    args = parser.parse_args()
    final_path, index_path, output_path = map(resolve, (args.final, args.item_index, args.output))
    final_rows, index_rows = read(final_path), read(index_path)
    if len(final_rows) != 876 or len(index_rows) != 219:
        raise ValueError("补正包只接受876条最终编码与219条分析单位索引。")
    index = {row["item_id"]: row for row in index_rows}
    if len(index) != 219:
        raise ValueError("分析单位索引存在重复或缺失item_id。")
    final_sha = hashlib.sha256(final_path.read_bytes()).hexdigest()
    rows = []
    for row in final_rows:
        item_id = row["item_id"]
        if item_id not in index:
            raise ValueError(f"无法在分析单位索引中定位：{item_id}")
        meta = index[item_id]
        question_id = item_id.rsplit("-", 1)[0]
        rows.append({
            "packet_version": "G4-08-R01-2026-07-23",
            **{key: row[key] for key in KEYS},
            "item_text_path": f"03_corpus/item_texts/{question_id}.md",
            "paper_pages": meta["page_paper"],
            "solution_pages": meta["page_solution"],
            "current_present": row["present_label"],
            "current_level": row["level"],
            "current_adjudication_reason": row["adjudication_reason"],
            "source_final_coding_sha256": final_sha,
            **{field: "" for field in WORK_FIELDS},
        })
    fields = [
        "packet_version", *KEYS, "item_text_path", "paper_pages", "solution_pages",
        "current_present", "current_level", "current_adjudication_reason", "source_final_coding_sha256", *WORK_FIELDS,
    ]
    write(output_path, fields, rows)
    print(f"wrote {len(rows)} rows to {output_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
