#!/usr/bin/env python3
"""Compare two versions of a V3 independent blind-coding return by row id."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


FIXED_FIELDS = (
    "blind_row_id",
    "blind_unit_no",
    "item_id",
    "competition_no",
    "year",
    "question_no",
    "subquestion_no",
    "dimension",
    "source_text_file",
    "solution_text_file",
)
COMPARE_FIELDS = (
    "independent_reviewer_id",
    "review_date",
    "review_present",
    "review_level",
    "question_evidence_quote",
    "solution_evidence_quote",
    "evidence_location",
    "adjacent_level_exclusion",
    "confidence",
    "reviewer_statement",
)
OUTPUT_FIELDS = (
    "blind_row_id",
    "blind_unit_no",
    "item_id",
    "dimension",
    "changed_fields",
    "label_changed",
    "v1_review_present",
    "v1_review_level",
    "v2_review_present",
    "v2_review_level",
    "v1_confidence",
    "v2_confidence",
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def compare(v1: list[dict[str, str]], v2: list[dict[str, str]]) -> list[dict[str, str]]:
    if len(v1) != len(v2):
        raise ValueError(f"row count differs: {len(v1)} != {len(v2)}")
    output: list[dict[str, str]] = []
    for row1, row2 in zip(v1, v2):
        for field in FIXED_FIELDS:
            if row1[field] != row2[field]:
                raise ValueError(f"fixed field changed at {row1['blind_row_id']}: {field}")
        changed = [field for field in COMPARE_FIELDS if row1[field] != row2[field]]
        if not changed:
            continue
        label_changed = any(field in changed for field in ("review_present", "review_level"))
        output.append(
            {
                "blind_row_id": row1["blind_row_id"],
                "blind_unit_no": row1["blind_unit_no"],
                "item_id": row1["item_id"],
                "dimension": row1["dimension"],
                "changed_fields": "|".join(changed),
                "label_changed": "是" if label_changed else "否",
                "v1_review_present": row1["review_present"],
                "v1_review_level": row1["review_level"],
                "v2_review_present": row2["review_present"],
                "v2_review_level": row2["review_level"],
                "v1_confidence": row1["confidence"],
                "v2_confidence": row2["confidence"],
            }
        )
    return output


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("v1", type=Path)
    parser.add_argument("v2", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    rows = compare(read_csv(args.v1.resolve()), read_csv(args.v2.resolve()))
    write_csv(args.output.resolve(), rows)
    label_changes = sum(row["label_changed"] == "是" for row in rows)
    print(f"CHANGED_ROWS={len(rows)}")
    print(f"LABEL_CHANGED_ROWS={label_changes}")


if __name__ == "__main__":
    main()
