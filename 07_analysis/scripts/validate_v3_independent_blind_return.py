#!/usr/bin/env python3
"""Validate a blank or completed V3 independent blind-coding return."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = (
    ROOT
    / "07_analysis/data/v3_independent_validation/handoff_RATER-C"
    / "第35至42届V3独立盲评编码表_75单元300行.csv"
)
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
REQUIRED_FIELDS = (
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


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def validate(path: Path, mode: str, template: Path = TEMPLATE) -> list[str]:
    template_fields, template_rows = read_csv(template)
    fields, rows = read_csv(path)
    errors: list[str] = []

    if fields != template_fields:
        errors.append("表头与模板不一致")
        return errors
    if len(rows) != 300:
        errors.append(f"行数应为300，实际为{len(rows)}")
        return errors

    template_by_id = {row["blind_row_id"]: row for row in template_rows}
    seen: set[str] = set()
    for line_no, row in enumerate(rows, start=2):
        row_id = row["blind_row_id"]
        if row_id in seen:
            errors.append(f"第{line_no}行：blind_row_id重复")
            continue
        seen.add(row_id)
        template_row = template_by_id.get(row_id)
        if template_row is None:
            errors.append(f"第{line_no}行：blind_row_id不在模板")
            continue
        for field in FIXED_FIELDS:
            if row[field] != template_row[field]:
                errors.append(f"第{line_no}行：固定字段{field}被修改")

        if mode == "template":
            for field in REQUIRED_FIELDS:
                if row[field].strip():
                    errors.append(f"第{line_no}行：模板字段{field}应为空")
            continue

        for field in REQUIRED_FIELDS:
            if not row[field].strip():
                errors.append(f"第{line_no}行：必填字段{field}为空")
        if row["review_present"] not in {"是", "否"}:
            errors.append(f"第{line_no}行：review_present取值非法")
        if row["review_present"] == "否" and row["review_level"] != "未出现":
            errors.append(f"第{line_no}行：未出现维度的等级必须为未出现")
        if row["review_present"] == "是" and row["review_level"] not in {"L1", "L2", "L3", "L4"}:
            errors.append(f"第{line_no}行：出现维度的等级必须为L1至L4")
        if row["confidence"] not in {"高", "中", "低"}:
            errors.append(f"第{line_no}行：confidence取值非法")

    if seen != set(template_by_id):
        errors.append("返回文件与模板blind_row_id集合不一致")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", type=Path, default=TEMPLATE)
    parser.add_argument("--mode", choices=("template", "filled"), default="template")
    parser.add_argument(
        "--template",
        type=Path,
        default=TEMPLATE,
        help="用于核对固定字段的空白模板；新版交接包应传入包内模板。",
    )
    args = parser.parse_args()

    errors = validate(args.path.resolve(), args.mode, args.template.resolve())
    if errors:
        print(f"FAIL errors={len(errors)}")
        for error in errors[:100]:
            print(error)
        raise SystemExit(1)
    print(f"PASS mode={args.mode} rows=300 file={args.path.resolve()}")


if __name__ == "__main__":
    main()
