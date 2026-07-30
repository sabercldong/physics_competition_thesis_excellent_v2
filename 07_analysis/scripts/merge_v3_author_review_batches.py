#!/usr/bin/env python3
"""Merge three completed V3 author-review batches in canonical row order."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from build_v3_author_review_package import (
    PACKAGE_FIELDS,
    REVIEW_FIELDS,
    ROOT,
    build_package_rows,
)
from build_v3_cross_year_audit import read_rows, write_rows


EXPECTED_FIELDS = [*PACKAGE_FIELDS, *REVIEW_FIELDS]
PRIORITIES = ("P0", "P1", "P2")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("p0", type=Path)
    parser.add_argument("p1", type=Path)
    parser.add_argument("p2", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--mode", choices=("template", "filled"), default="filled")
    return parser.parse_args()


def resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def main() -> None:
    args = parse_args()
    paths = dict(zip(PRIORITIES, (args.p0, args.p1, args.p2)))
    resolved_paths = {priority: resolve(path) for priority, path in paths.items()}
    output = resolve(args.output)
    if output in resolved_paths.values():
        raise SystemExit("输出路径不能覆盖任一分批输入文件")
    canonical_rows, item_rows = build_package_rows()
    priority_by_item = {
        row["item_id"]: row["item_priority"] for row in item_rows
    }
    merged_by_id: dict[str, dict[str, str]] = {}

    for priority, path in resolved_paths.items():
        fields, rows = read_rows(path)
        expected_rows = [
            row
            for row in canonical_rows
            if priority_by_item[row["item_id"]] == priority
        ]
        if fields != EXPECTED_FIELDS:
            raise SystemExit(f"{priority}表头与G8-79规范不一致: {path}")
        if len(rows) != len(expected_rows):
            raise SystemExit(
                f"{priority}应为{len(expected_rows)}行，实际为{len(rows)}行: {path}"
            )

        for position, (actual, expected) in enumerate(
            zip(rows, expected_rows),
            start=2,
        ):
            for field in PACKAGE_FIELDS:
                if actual.get(field, "") != expected[field]:
                    raise SystemExit(
                        f"{priority}第{position}行不可变字段被修改: {field}"
                    )
            row_id = actual["review_row_id"]
            if row_id in merged_by_id:
                raise SystemExit(f"批次之间存在重复review_row_id: {row_id}")
            merged_by_id[row_id] = actual

    canonical_ids = [row["review_row_id"] for row in canonical_rows]
    missing = [row_id for row_id in canonical_ids if row_id not in merged_by_id]
    extra = [row_id for row_id in merged_by_id if row_id not in set(canonical_ids)]
    if missing or extra:
        raise SystemExit(
            f"批次并集不完整: missing={len(missing)}, extra={len(extra)}"
        )

    merged_rows = [merged_by_id[row_id] for row_id in canonical_ids]
    write_rows(output, EXPECTED_FIELDS, merged_rows)

    validator = ROOT / "07_analysis/scripts/validate_v3_author_review.py"
    command = [
        sys.executable,
        str(validator),
        str(output),
        "--mode",
        args.mode,
    ]
    result = subprocess.run(command, cwd=ROOT, check=False)
    if result.returncode:
        output.unlink(missing_ok=True)
        raise SystemExit("合并文件未通过全量校验，已删除失败输出")
    print(f"merged_rows={len(merged_rows)}")
    print(f"output={output}")


if __name__ == "__main__":
    main()
