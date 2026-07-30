#!/usr/bin/env python3
"""Validate a blank or completed V3 author substantive-review return."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from build_v3_author_review_package import (
    OUTPUT,
    PACKAGE_FIELDS,
    REVIEW_FIELDS,
    ROOT,
    build_package_rows,
)
from build_v3_cross_year_audit import read_rows


DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ALLOWED = {
    "source_checked": {"是", "否"},
    "question_evidence_decision": {"充分", "需补充", "不可定位"},
    "solution_evidence_decision": {"充分", "需补充", "不可定位"},
    "candidate_review_decision": {"保持当前候选", "更正候选", "待核实"},
    "rechecked_present_label": {"是", "否", "待核实"},
    "rechecked_level": {"L1", "L2", "L3", "L4", "未出现", "待核实"},
    "adjacent_level_review": {
        "认可当前相邻等级排除",
        "修改相邻等级排除（详见更正理由）",
        "维度未出现，不进入等级复核",
        "待核实",
    },
    "author_review_status": {"已完成", "待补证", "待裁决"},
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", type=Path, default=OUTPUT)
    parser.add_argument("--mode", choices=("template", "filled"), default="template")
    parser.add_argument(
        "--item-priority",
        choices=("P0", "P1", "P2"),
        help="只校验题目级最高优先级对应的分批文件",
    )
    parser.add_argument(
        "--review-row-ids-file",
        type=Path,
        help="按CSV中的review_row_id校验自定义子集，与--item-priority互斥",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = args.input if args.input.is_absolute() else ROOT / args.input
    fields, rows = read_rows(input_path)
    expected_rows, item_rows = build_package_rows()
    if args.item_priority and args.review_row_ids_file:
        raise SystemExit("--item-priority与--review-row-ids-file不能同时使用")
    if args.item_priority:
        item_ids = {
            row["item_id"]
            for row in item_rows
            if row["item_priority"] == args.item_priority
        }
        expected_rows = [
            row for row in expected_rows if row["item_id"] in item_ids
        ]
    scope_name = args.item_priority or "ALL"
    if args.review_row_ids_file:
        scope_path = (
            args.review_row_ids_file
            if args.review_row_ids_file.is_absolute()
            else ROOT / args.review_row_ids_file
        )
        scope_fields, scope_rows = read_rows(scope_path)
        if "review_row_id" not in scope_fields:
            raise SystemExit("自定义范围CSV缺少review_row_id字段")
        scope_ids = [row["review_row_id"].strip() for row in scope_rows]
        if any(not row_id for row_id in scope_ids):
            raise SystemExit("自定义范围CSV含空review_row_id")
        if len(scope_ids) != len(set(scope_ids)):
            raise SystemExit("自定义范围CSV含重复review_row_id")
        known_ids = {row["review_row_id"] for row in expected_rows}
        unknown_ids = sorted(set(scope_ids) - known_ids)
        if unknown_ids:
            raise SystemExit(
                f"自定义范围CSV含未知review_row_id: {unknown_ids[:10]}"
            )
        scope_id_set = set(scope_ids)
        expected_rows = [
            row for row in expected_rows if row["review_row_id"] in scope_id_set
        ]
        scope_name = f"CUSTOM:{scope_path}"
    expected_fields = [*PACKAGE_FIELDS, *REVIEW_FIELDS]
    errors: list[str] = []

    if fields != expected_fields:
        errors.append("表头与G8-79规范不一致")
    if len(rows) != len(expected_rows):
        errors.append(f"应为{len(expected_rows)}行，实际为{len(rows)}行")

    for position, (actual, expected) in enumerate(
        zip(rows, expected_rows),
        start=2,
    ):
        for field in PACKAGE_FIELDS:
            if actual.get(field, "") != expected[field]:
                errors.append(f"第{position}行不可变字段被修改: {field}")
                break

        if args.mode == "template":
            nonblank = [field for field in REVIEW_FIELDS if actual.get(field, "")]
            if nonblank:
                errors.append(
                    f"第{position}行模板回填字段应为空: {','.join(nonblank)}"
                )
            continue

        missing = [field for field in REVIEW_FIELDS if not actual.get(field, "").strip()]
        if missing:
            errors.append(f"第{position}行缺少回填字段: {','.join(missing)}")
            continue

        if not DATE_PATTERN.fullmatch(actual["actual_review_date"]):
            errors.append(f"第{position}行复核日期必须为YYYY-MM-DD")
        for field, allowed in ALLOWED.items():
            if actual[field] not in allowed:
                errors.append(f"第{position}行{field}取值非法: {actual[field]}")

        decision = actual["candidate_review_decision"]
        present = actual["rechecked_present_label"]
        level = actual["rechecked_level"]
        status = actual["author_review_status"]
        question_evidence = actual["question_evidence_decision"]
        solution_evidence = actual["solution_evidence_decision"]

        if decision == "保持当前候选":
            if (present, level) != (actual["present_label"], actual["level"]):
                errors.append(f"第{position}行保持候选但复核标签与候选不一致")
            if actual["source_checked"] != "是":
                errors.append(f"第{position}行保持候选但未确认核对来源")
            if question_evidence != "充分" or solution_evidence != "充分":
                errors.append(f"第{position}行保持候选但双侧证据未判充分")
            if status != "已完成":
                errors.append(f"第{position}行保持候选但状态不是已完成")
        elif decision == "更正候选":
            if present == "待核实" or level == "待核实":
                errors.append(f"第{position}行更正候选但新标签仍为待核实")
            if (present, level) == (actual["present_label"], actual["level"]):
                errors.append(f"第{position}行更正候选但标签没有变化")
            if len(actual["correction_reason"].strip()) < 8:
                errors.append(f"第{position}行更正理由少于8个字符")
            if status != "已完成":
                errors.append(f"第{position}行更正候选但状态不是已完成")
        else:
            if present != "待核实" or level != "待核实":
                errors.append(f"第{position}行待核实但复核标签未同步为待核实")
            if status not in {"待补证", "待裁决"}:
                errors.append(f"第{position}行待核实但状态不是待补证或待裁决")

        if present == "是" and level not in {"L1", "L2", "L3", "L4"}:
            errors.append(f"第{position}行判定出现但等级非法")
        if present == "否" and level != "未出现":
            errors.append(f"第{position}行判定未出现但等级不是未出现")
        if present == "待核实" and level != "待核实":
            errors.append(f"第{position}行存在性待核实但等级未同步")

        adjacent = actual["adjacent_level_review"]
        if present == "是" and adjacent == "维度未出现，不进入等级复核":
            errors.append(f"第{position}行维度出现但相邻等级复核标为不适用")
        if present == "否" and adjacent != "维度未出现，不进入等级复核":
            errors.append(f"第{position}行维度未出现但相邻等级复核填写不一致")
        if present == "待核实" and adjacent != "待核实":
            errors.append(f"第{position}行标签待核实但相邻等级复核未同步")

        if (
            actual["source_checked"] == "否"
            or question_evidence != "充分"
            or solution_evidence != "充分"
        ) and decision != "待核实":
            errors.append(f"第{position}行证据未闭合但未选择待核实")
        if len(actual["post_review_evidence_location"].strip()) < 8:
            errors.append(f"第{position}行复核后证据位置少于8个字符")
        if len(actual["reviewer_statement"].strip()) < 12:
            errors.append(f"第{position}行复核声明少于12个字符")

    print(f"file={input_path}")
    print(f"mode={args.mode}")
    print(f"item_priority={args.item_priority or 'ALL'}")
    print(f"scope={scope_name}")
    print(f"rows={len(rows)}")
    print(f"errors={len(errors)}")
    for error in errors[:100]:
        print(f"ERROR: {error}")
    if len(errors) > 100:
        print(f"ERROR: 其余{len(errors) - 100}项省略")
    raise SystemExit(1 if errors else 0)


if __name__ == "__main__":
    main()
