#!/usr/bin/env python3
"""Merge four completed V3 migration-delta batches into the canonical 547 rows."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from build_v3_author_review_package import (
    PACKAGE_FIELDS,
    REVIEW_FIELDS,
    ROOT,
)
from build_v3_cross_year_audit import read_rows, write_rows
from build_v3_delta_review_batches import BATCHES, build_batches
from build_v3_prior_review_migration import DELTA_SCOPE, DELTA_TEMPLATE


EXPECTED_FIELDS = [*PACKAGE_FIELDS, *REVIEW_FIELDS]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch-35-36", type=Path, required=True)
    parser.add_argument("--batch-37-38", type=Path, required=True)
    parser.add_argument("--batch-39-40", type=Path, required=True)
    parser.add_argument("--batch-41-42", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--mode", choices=("template", "filled"), default="filled")
    return parser.parse_args()


def resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def main() -> None:
    args = parse_args()
    input_paths = {
        "Y35-36": resolve(args.batch_35_36),
        "Y37-38": resolve(args.batch_37_38),
        "Y39-40": resolve(args.batch_39_40),
        "Y41-42": resolve(args.batch_41_42),
    }
    output_path = resolve(args.output)
    if output_path in input_paths.values():
        raise SystemExit("输出路径不能覆盖任一分届输入文件")

    expected_templates, _, _ = build_batches()
    validator = ROOT / "07_analysis/scripts/validate_v3_author_review.py"
    merged_by_id: dict[str, dict[str, str]] = {}
    for batch_id, input_path in input_paths.items():
        config = BATCHES[batch_id]
        validation = subprocess.run(
            [
                sys.executable,
                str(validator),
                str(input_path),
                "--mode",
                args.mode,
                "--review-row-ids-file",
                str(config["scope"]),
            ],
            cwd=ROOT,
            check=False,
        )
        if validation.returncode:
            raise SystemExit(f"{batch_id}未通过{args.mode}模式校验")
        fields, rows = read_rows(input_path)
        if fields != EXPECTED_FIELDS:
            raise SystemExit(f"{batch_id}表头与V3作者复核规范不一致")
        expected_rows = expected_templates[batch_id]
        if len(rows) != len(expected_rows):
            raise SystemExit(f"{batch_id}行数与固定批次不一致")
        for actual, expected in zip(rows, expected_rows):
            for field in PACKAGE_FIELDS:
                if actual[field] != expected[field]:
                    raise SystemExit(
                        f"{batch_id}不可变字段被修改: "
                        f"{actual.get('review_row_id', '')}/{field}"
                    )
            row_id = actual["review_row_id"]
            if row_id in merged_by_id:
                raise SystemExit(f"分届批次存在重复review_row_id: {row_id}")
            merged_by_id[row_id] = actual

    _, canonical_rows = read_rows(DELTA_TEMPLATE)
    canonical_ids = [row["review_row_id"] for row in canonical_rows]
    if set(merged_by_id) != set(canonical_ids):
        raise SystemExit("四个分届批次并集未精确覆盖547行")
    merged_rows = [merged_by_id[row_id] for row_id in canonical_ids]
    write_rows(output_path, EXPECTED_FIELDS, merged_rows)
    full_validation = subprocess.run(
        [
            sys.executable,
            str(validator),
            str(output_path),
            "--mode",
            args.mode,
            "--review-row-ids-file",
            str(DELTA_SCOPE),
        ],
        cwd=ROOT,
        check=False,
    )
    if full_validation.returncode:
        output_path.unlink(missing_ok=True)
        raise SystemExit("合并后的547行文件未通过全量差异范围校验")
    print(f"merged_rows={len(merged_rows)}")
    print(f"mode={args.mode}")
    print(f"output={output_path}")


if __name__ == "__main__":
    main()
