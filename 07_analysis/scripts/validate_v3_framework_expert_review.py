#!/usr/bin/env python3
"""Validate one completed V3 framework expert-review form."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = (
    ROOT
    / "07_analysis/data/v3_framework_expert_review/handoff_EXPERTS"
    / "V3框架专家内容效度审查表_20项.csv"
)
FIXED_FIELDS = (
    "review_item_id",
    "维度",
    "判定层级",
    "必要证据",
    "最低充分判据",
    "明确排除",
    "向上升级条件",
    "强制复核条件",
)
RATING_FIELDS = (
    "relevance_1_4",
    "clarity_1_4",
    "dimension_level_separation_1_4",
    "operability_1_4",
)
TEXT_FIELDS = (
    "expert_id",
    "review_date",
    "review_decision",
    "suggested_revision",
    "physics_example_or_counterexample",
    "expert_statement",
)


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def validate(path: Path, mode: str) -> list[str]:
    template_fields, template_rows = read_csv(TEMPLATE)
    fields, rows = read_csv(path)
    errors: list[str] = []
    if fields != template_fields:
        return ["表头与模板不一致"]
    if len(rows) != 20:
        return [f"行数应为20，实际为{len(rows)}"]

    template_by_id = {row["review_item_id"]: row for row in template_rows}
    for line_no, row in enumerate(rows, start=2):
        template_row = template_by_id.get(row["review_item_id"])
        if template_row is None:
            errors.append(f"第{line_no}行：review_item_id非法")
            continue
        for field in FIXED_FIELDS:
            if row[field] != template_row[field]:
                errors.append(f"第{line_no}行：固定字段{field}被修改")
        if mode == "template":
            for field in (*RATING_FIELDS, *TEXT_FIELDS):
                if row[field].strip():
                    errors.append(f"第{line_no}行：模板字段{field}应为空")
            continue
        for field in RATING_FIELDS:
            if row[field] not in {"1", "2", "3", "4"}:
                errors.append(f"第{line_no}行：{field}必须为1至4")
        for field in TEXT_FIELDS:
            if not row[field].strip():
                errors.append(f"第{line_no}行：{field}为空")
        if row["review_decision"] not in {"接受", "修改后接受", "删除/重建"}:
            errors.append(f"第{line_no}行：review_decision取值非法")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", type=Path, default=TEMPLATE)
    parser.add_argument("--mode", choices=("template", "filled"), default="template")
    args = parser.parse_args()
    errors = validate(args.path.resolve(), args.mode)
    if errors:
        print(f"FAIL errors={len(errors)}")
        for error in errors[:100]:
            print(error)
        raise SystemExit(1)
    print(f"PASS mode={args.mode} rows=20 file={args.path.resolve()}")


if __name__ == "__main__":
    main()
