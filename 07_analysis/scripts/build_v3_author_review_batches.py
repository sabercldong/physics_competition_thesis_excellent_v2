#!/usr/bin/env python3
"""Split the V3 author review template into item-preserving priority batches."""

from __future__ import annotations

from collections import Counter

from build_v3_author_review_package import (
    PACKAGE_FIELDS,
    REVIEW_FIELDS,
    ROOT,
    build_package_rows,
)
from build_v3_cross_year_audit import write_rows


OUTPUT_DIR = (
    ROOT / "10_outputs/material_package/V3作者实质复核分批包_G8-80-PREP"
)
MANIFEST = OUTPUT_DIR / "V3作者实质复核批次清单.csv"
BATCH_FILES = {
    "P0": OUTPUT_DIR / "P0_高优先级_89题356行_空白.csv",
    "P1": OUTPUT_DIR / "P1_L3边界_89题356行_空白.csv",
    "P2": OUTPUT_DIR / "P2_常规边界_43题172行_空白.csv",
}
EXPECTED_ITEM_COUNTS = {"P0": 89, "P1": 89, "P2": 43}
EXPECTED_ROW_COUNTS = {"P0": 356, "P1": 356, "P2": 172}
MANIFEST_FIELDS = [
    "batch_id",
    "item_priority",
    "item_count",
    "review_row_count",
    "first_review_row_id",
    "last_review_row_id",
    "output_path",
    "completion_status",
    "validation_command",
]


def build_batches() -> tuple[dict[str, list[dict[str, str]]], list[dict[str, str]]]:
    package_rows, item_rows = build_package_rows()
    priority_by_item = {
        row["item_id"]: row["item_priority"] for row in item_rows
    }
    batches = {
        priority: [
            row
            for row in package_rows
            if priority_by_item[row["item_id"]] == priority
        ]
        for priority in BATCH_FILES
    }

    item_counts = Counter(priority_by_item.values())
    for priority in BATCH_FILES:
        if item_counts[priority] != EXPECTED_ITEM_COUNTS[priority]:
            raise ValueError(
                f"{priority}应为{EXPECTED_ITEM_COUNTS[priority]}题，"
                f"实际为{item_counts[priority]}题"
            )
        if len(batches[priority]) != EXPECTED_ROW_COUNTS[priority]:
            raise ValueError(
                f"{priority}应为{EXPECTED_ROW_COUNTS[priority]}行，"
                f"实际为{len(batches[priority])}行"
            )

    all_ids = [row["review_row_id"] for rows in batches.values() for row in rows]
    expected_ids = [row["review_row_id"] for row in package_rows]
    if len(all_ids) != len(set(all_ids)):
        raise ValueError("分批结果存在重复review_row_id")
    if set(all_ids) != set(expected_ids):
        raise ValueError("分批结果未精确覆盖884行完整模板")

    manifest_rows = []
    for priority, path in BATCH_FILES.items():
        rows = batches[priority]
        manifest_rows.append(
            {
                "batch_id": f"G8-80-PREP-{priority}",
                "item_priority": priority,
                "item_count": str(EXPECTED_ITEM_COUNTS[priority]),
                "review_row_count": str(len(rows)),
                "first_review_row_id": rows[0]["review_row_id"],
                "last_review_row_id": rows[-1]["review_row_id"],
                "output_path": str(path.relative_to(ROOT)),
                "completion_status": "空白：待作者实质复核",
                "validation_command": (
                    "python3 07_analysis/scripts/validate_v3_author_review.py "
                    f"'{path.relative_to(ROOT)}' --mode filled "
                    f"--item-priority {priority}"
                ),
            }
        )
    return batches, manifest_rows


def main() -> None:
    batches, manifest_rows = build_batches()
    fields = [*PACKAGE_FIELDS, *REVIEW_FIELDS]
    for priority, path in BATCH_FILES.items():
        write_rows(path, fields, batches[priority])
        print(
            f"{priority}: items={EXPECTED_ITEM_COUNTS[priority]}, "
            f"rows={len(batches[priority])}, path={path.relative_to(ROOT)}"
        )
    write_rows(MANIFEST, MANIFEST_FIELDS, manifest_rows)
    print(f"manifest={MANIFEST.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
