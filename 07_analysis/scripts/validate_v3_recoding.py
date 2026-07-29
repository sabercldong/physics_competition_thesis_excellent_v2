#!/usr/bin/env python3
"""Validate the V3 recoding template or a completed V3 coding file."""

from __future__ import annotations

import argparse
import csv
import hashlib
import re
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = ROOT / "07_analysis/data/科学思维正式重编码空白表_V3.csv"
DIMENSIONS = ("模型建构", "科学推理", "科学论证", "质疑创新")
DECISION_FIELDS = (
    "required_output",
    "question_quote",
    "question_location",
    "solution_quote",
    "solution_location",
    "necessary_cognitive_activity",
    "present_label",
    "level",
    "decision_reason",
    "adjacent_level_exclusion",
    "confidence",
    "coder_id",
    "coding_date",
    "review_status",
)
FORBIDDEN_FRAGMENTS = (
    "待补",
    "见原文",
    "同上",
    "通用模板",
    "智能体判断",
    "程序判定",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--mode", choices=("template", "filled"), default="template")
    parser.add_argument(
        "--expected-items",
        type=int,
        default=219,
        help="Expected number of analysis units; use 26 for the year-35 batch.",
    )
    return parser.parse_args()


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalized(text: str) -> str:
    return re.sub(r"\s+", "", text)


def main() -> int:
    args = parse_args()
    path = args.input if args.input.is_absolute() else ROOT / args.input
    rows = read_rows(path)
    errors: list[str] = []
    warnings: list[str] = []

    expected_rows = args.expected_items * len(DIMENSIONS)
    if len(rows) != expected_rows:
        errors.append(f"总行数应为{expected_rows}，实际为{len(rows)}")

    keys = [(row.get("item_id", ""), row.get("dimension", "")) for row in rows]
    if len(set(keys)) != len(keys):
        errors.append("item_id与dimension组合存在重复")

    dimension_counts = Counter(row.get("dimension", "") for row in rows)
    for dimension in DIMENSIONS:
        if dimension_counts[dimension] != args.expected_items:
            errors.append(
                f"{dimension}应为{args.expected_items}行，"
                f"实际为{dimension_counts[dimension]}行"
            )

    source_cache: dict[str, str] = {}
    for line_no, row in enumerate(rows, start=2):
        prefix = f"第{line_no}行 {row.get('item_id', '')}/{row.get('dimension', '')}"
        source_rel = row.get("item_text_path", "")
        if not source_rel:
            errors.append(f"{prefix}: item_text_path为空")
            continue
        source = ROOT / source_rel
        if not source.exists():
            errors.append(f"{prefix}: 源文件不存在 {source_rel}")
            continue
        actual_hash = file_sha256(source)
        if row.get("item_text_sha256") != actual_hash:
            errors.append(f"{prefix}: item_text_sha256与当前源文件不一致")
        if source_rel not in source_cache:
            source_cache[source_rel] = source.read_text(encoding="utf-8-sig")

        solution_source_rel = row.get("solution_text_path", "").strip() or source_rel
        solution_source = ROOT / solution_source_rel
        if not solution_source.exists():
            errors.append(f"{prefix}: 解答源文件不存在 {solution_source_rel}")
            continue
        solution_hash = row.get("solution_text_sha256", "").strip()
        if solution_hash and solution_hash != file_sha256(solution_source):
            errors.append(f"{prefix}: solution_text_sha256与当前解答源文件不一致")
        if solution_source_rel not in source_cache:
            source_cache[solution_source_rel] = solution_source.read_text(
                encoding="utf-8-sig"
            )

        if args.mode == "template":
            dirty = [field for field in DECISION_FIELDS if row.get(field, "").strip()]
            if dirty:
                errors.append(f"{prefix}: 空白模板含已填写字段 {','.join(dirty)}")
            continue

        missing = [field for field in DECISION_FIELDS if not row.get(field, "").strip()]
        if missing:
            errors.append(f"{prefix}: 必填字段为空 {','.join(missing)}")

        present = row.get("present_label", "")
        level = row.get("level", "")
        if present not in {"是", "否", "待裁决"}:
            errors.append(f"{prefix}: present_label值无效 {present}")
        if present == "是" and level not in {"L1", "L2", "L3", "L4"}:
            errors.append(f"{prefix}: 判为是时level必须为L1-L4")
        if present == "否" and level != "未出现":
            errors.append(f"{prefix}: 判为否时level必须为未出现")
        if present == "待裁决" and level != "待裁决":
            errors.append(f"{prefix}: 待裁决时level必须为待裁决")
        if row.get("confidence") not in {"高", "中", "低"}:
            errors.append(f"{prefix}: confidence必须为高、中或低")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", row.get("coding_date", "")):
            errors.append(f"{prefix}: coding_date必须为YYYY-MM-DD")

        combined = "；".join(row.get(field, "") for field in DECISION_FIELDS)
        for fragment in FORBIDDEN_FRAGMENTS:
            if fragment in combined:
                errors.append(f"{prefix}: 含禁止占位文本“{fragment}”")
        if any(row.get(field, "").strip() == "略" for field in DECISION_FIELDS):
            errors.append(f"{prefix}: 含禁止占位文本“略”")

        quote_sources = {
            "question_quote": normalized(source_cache[source_rel]),
            "solution_quote": normalized(source_cache[solution_source_rel]),
        }
        for field, source_text in quote_sources.items():
            quote = row.get(field, "").strip()
            if len(normalized(quote)) < 8:
                errors.append(f"{prefix}: {field}少于8个非空白字符")
            elif normalized(quote) not in source_text:
                errors.append(f"{prefix}: {field}不能在源文件逐字定位")

        if present == "是" and level == "L4":
            warnings.append(f"{prefix}: L4必须进入强制实质复核")
        if present == "是" and row.get("dimension") in {"科学论证", "质疑创新"}:
            warnings.append(f"{prefix}: 该维度判是必须进入强制实质复核")
        if row.get("confidence") == "低" or present == "待裁决":
            warnings.append(f"{prefix}: 低置信度或待裁决记录必须进入裁决")

    if args.mode == "filled" and rows:
        for dimension in DIMENSIONS:
            dimension_rows = [row for row in rows if row.get("dimension") == dimension]
            present_count = sum(
                row.get("present_label") == "是" for row in dimension_rows
            )
            rate = present_count / len(dimension_rows)
            if rate >= 0.95 or rate <= 0.05:
                warnings.append(
                    f"{dimension}出现率为{rate:.1%}，触发饱和或稀疏性专项复审"
                )

    print(f"file={path}")
    print(f"mode={args.mode}")
    print(f"rows={len(rows)}")
    print(f"errors={len(errors)} warnings={len(warnings)}")
    for message in errors[:100]:
        print(f"ERROR: {message}")
    for message in warnings[:100]:
        print(f"WARNING: {message}")
    if len(errors) > 100:
        print(f"ERROR: 另有{len(errors) - 100}条错误未展开")
    if len(warnings) > 100:
        print(f"WARNING: 另有{len(warnings) - 100}条警告未展开")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
