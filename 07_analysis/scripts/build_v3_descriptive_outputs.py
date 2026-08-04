#!/usr/bin/env python3
"""Build Chinese-named descriptive result tables from a validated 884-row table."""

from __future__ import annotations

import argparse
import hashlib
from collections import Counter, defaultdict
from pathlib import Path

from build_v3_author_review_package import ROOT
from build_v3_cross_year_audit import read_rows, write_rows
from build_v3_final_coding import OUTPUT_FIELDS


DIMENSIONS = ("模型建构", "科学推理", "科学论证", "质疑创新")
LEVELS = ("L1", "L2", "L3", "L4", "未出现")
EXPECTED_ROWS = 884
EXPECTED_ITEMS = 221


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument(
        "--item-index",
        type=Path,
        default=Path("03_corpus/item_index.csv"),
    )
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--version-label", default="第三版")
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def ratio(numerator: int, denominator: int) -> str:
    return f"{numerator / denominator:.6f}" if denominator else ""


def main() -> None:
    args = parse_args()
    input_path = resolve(args.input)
    index_path = resolve(args.item_index)
    output_dir = resolve(args.output_dir)
    fields, rows = read_rows(input_path)
    _, index_rows = read_rows(index_path)

    if fields != OUTPUT_FIELDS:
        raise SystemExit("输入编码表字段与G8-68-PREP规范不一致")
    if len(rows) != EXPECTED_ROWS:
        raise SystemExit(f"输入编码表应为{EXPECTED_ROWS}行，实际为{len(rows)}行")
    if len(index_rows) != EXPECTED_ITEMS:
        raise SystemExit(f"题目索引应为{EXPECTED_ITEMS}行，实际为{len(index_rows)}行")
    if output_dir.exists() and not output_dir.is_dir():
        raise SystemExit(f"输出目录路径已被普通文件占用: {output_dir}")
    if output_dir.exists() and any(output_dir.iterdir()) and not args.force:
        raise SystemExit(f"输出目录非空；如确认替换须使用--force: {output_dir}")

    index_by_item = {row["item_id"]: row for row in index_rows}
    rows_by_item: dict[str, dict[str, dict[str, str]]] = defaultdict(dict)
    for row in rows:
        item_id = row["item_id"]
        dimension = row["dimension"]
        if item_id not in index_by_item:
            raise SystemExit(f"唯一表存在无法映射题目索引的item_id: {item_id}")
        if dimension not in DIMENSIONS:
            raise SystemExit(f"未知维度: {dimension}")
        if dimension in rows_by_item[item_id]:
            raise SystemExit(f"重复item_id×dimension: {item_id}/{dimension}")
        if row["present"] not in {"0", "1"}:
            raise SystemExit(f"present必须为0/1: {item_id}/{dimension}")
        if row["present"] == "1" and row["level"] not in LEVELS[:4]:
            raise SystemExit(f"维度出现但等级非法: {item_id}/{dimension}")
        if row["present"] == "0" and row["level"] != "未出现":
            raise SystemExit(f"维度未出现但等级不是未出现: {item_id}/{dimension}")
        rows_by_item[item_id][dimension] = row
    if set(rows_by_item) != set(index_by_item):
        raise SystemExit("唯一表与题目索引的item_id集合不一致")
    if any(set(dimensions) != set(DIMENSIONS) for dimensions in rows_by_item.values()):
        raise SystemExit("每个分析单元必须恰有四个维度")

    source_hash = hashlib.sha256(input_path.read_bytes()).hexdigest()
    total_items = len(rows_by_item)
    common_source = {"源唯一编码表SHA256": source_hash}

    presence_rows: list[dict[str, str]] = []
    level_rows: list[dict[str, str]] = []
    for dimension in DIMENSIONS:
        dimension_rows = [
            item_rows[dimension] for item_rows in rows_by_item.values()
        ]
        present_count = sum(row["present"] == "1" for row in dimension_rows)
        presence_rows.append(
            {
                "维度": dimension,
                "出现题目数": str(present_count),
                "全部题目数": str(total_items),
                "出现比例": ratio(present_count, total_items),
                **common_source,
            }
        )
        counts = Counter(row["level"] for row in dimension_rows)
        for level in LEVELS:
            count = counts[level]
            level_rows.append(
                {
                    "维度": dimension,
                    "层级": level,
                    "题目数": str(count),
                    "维度出现题目数": str(present_count),
                    "全部题目数": str(total_items),
                    "占维度出现题目比例": (
                        ratio(count, present_count) if level != "未出现" else ""
                    ),
                    "占全部题目比例": ratio(count, total_items),
                    **common_source,
                }
            )

    cooccurrence_rows: list[dict[str, str]] = []
    for position, left in enumerate(DIMENSIONS):
        for right in DIMENSIONS[position + 1 :]:
            left_count = sum(
                item_rows[left]["present"] == "1"
                for item_rows in rows_by_item.values()
            )
            right_count = sum(
                item_rows[right]["present"] == "1"
                for item_rows in rows_by_item.values()
            )
            both_count = sum(
                item_rows[left]["present"] == "1"
                and item_rows[right]["present"] == "1"
                for item_rows in rows_by_item.values()
            )
            union_count = left_count + right_count - both_count
            cooccurrence_rows.append(
                {
                    "维度甲": left,
                    "维度乙": right,
                    "共同出现题目数": str(both_count),
                    "至少一个出现题目数": str(union_count),
                    "全部题目数": str(total_items),
                    "共同出现占全部比例": ratio(both_count, total_items),
                    "Jaccard系数": ratio(both_count, union_count),
                    **common_source,
                }
            )

    year_presence_rows: list[dict[str, str]] = []
    year_level_rows: list[dict[str, str]] = []
    items_by_year: dict[str, list[str]] = defaultdict(list)
    for item_id, metadata in index_by_item.items():
        items_by_year[metadata["year"]].append(item_id)
    for year in sorted(items_by_year):
        item_ids = items_by_year[year]
        for dimension in DIMENSIONS:
            dimension_rows = [
                rows_by_item[item_id][dimension] for item_id in item_ids
            ]
            present_count = sum(row["present"] == "1" for row in dimension_rows)
            year_presence_rows.append(
                {
                    "年份": year,
                    "竞赛届次": index_by_item[item_ids[0]]["competition_no"],
                    "维度": dimension,
                    "出现题目数": str(present_count),
                    "该届题目数": str(len(item_ids)),
                    "出现比例": ratio(present_count, len(item_ids)),
                    **common_source,
                }
            )
            level_counts = Counter(row["level"] for row in dimension_rows)
            for level in LEVELS:
                count = level_counts[level]
                year_level_rows.append(
                    {
                        "年份": year,
                        "竞赛届次": index_by_item[item_ids[0]][
                            "competition_no"
                        ],
                        "维度": dimension,
                        "层级": level,
                        "题目数": str(count),
                        "该届题目数": str(len(item_ids)),
                        "占该届全部题目比例": ratio(count, len(item_ids)),
                        **common_source,
                    }
                )

    combination_counts: Counter[str] = Counter()
    for item_rows in rows_by_item.values():
        present_dimensions = [
            dimension
            for dimension in DIMENSIONS
            if item_rows[dimension]["present"] == "1"
        ]
        label = "＋".join(present_dimensions) if present_dimensions else "四维均未出现"
        combination_counts[label] += 1
    combination_rows = [
        {
            "维度组合": combination,
            "题目数": str(count),
            "全部题目数": str(total_items),
            "比例": ratio(count, total_items),
            **common_source,
        }
        for combination, count in sorted(
            combination_counts.items(),
            key=lambda pair: (-pair[1], pair[0]),
        )
    ]

    source_review_hashes = {row["source_author_review_sha256"] for row in rows}
    source_acceptance_hashes = {
        row["source_g8_80_acceptance_sha256"] for row in rows
    }
    if len(source_review_hashes) != 1 or len(source_acceptance_hashes) != 1:
        raise SystemExit("唯一表内来源哈希不唯一")
    source_rows = [
        {
            "结果表来源": str(input_path),
            "唯一编码表SHA256": source_hash,
            "作者复核文件SHA256": next(iter(source_review_hashes)),
            "G8-80验收决定SHA256": next(iter(source_acceptance_hashes)),
            "分析单元数": str(total_items),
            "编码记录数": str(len(rows)),
            "统计边界": "描述试题任务要求，不推断学生能力、教学效果或因果关系",
        }
    ]

    outputs = {
        "总体维度出现分布.csv": (
            ["维度", "出现题目数", "全部题目数", "出现比例", "源唯一编码表SHA256"],
            presence_rows,
        ),
        "各维度等级分布.csv": (
            [
                "维度",
                "层级",
                "题目数",
                "维度出现题目数",
                "全部题目数",
                "占维度出现题目比例",
                "占全部题目比例",
                "源唯一编码表SHA256",
            ],
            level_rows,
        ),
        "维度共现分布.csv": (
            [
                "维度甲",
                "维度乙",
                "共同出现题目数",
                "至少一个出现题目数",
                "全部题目数",
                "共同出现占全部比例",
                "Jaccard系数",
                "源唯一编码表SHA256",
            ],
            cooccurrence_rows,
        ),
        "分届次维度出现分布.csv": (
            [
                "年份",
                "竞赛届次",
                "维度",
                "出现题目数",
                "该届题目数",
                "出现比例",
                "源唯一编码表SHA256",
            ],
            year_presence_rows,
        ),
        "分届次维度等级分布.csv": (
            [
                "年份",
                "竞赛届次",
                "维度",
                "层级",
                "题目数",
                "该届题目数",
                "占该届全部题目比例",
                "源唯一编码表SHA256",
            ],
            year_level_rows,
        ),
        "维度组合分布.csv": (
            ["维度组合", "题目数", "全部题目数", "比例", "源唯一编码表SHA256"],
            combination_rows,
        ),
        "结果数据来源登记.csv": (
            [
                "结果表来源",
                "唯一编码表SHA256",
                "作者复核文件SHA256",
                "G8-80验收决定SHA256",
                "分析单元数",
                "编码记录数",
                "统计边界",
            ],
            source_rows,
        ),
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    for filename, (output_fields, output_rows) in outputs.items():
        write_rows(output_dir / filename, output_fields, output_rows)

    report = output_dir / "描述统计生成说明.md"
    with report.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(
            f"# {args.version_label}描述统计生成说明\n\n"
            f"- 输入唯一编码表：`{input_path}`\n"
            f"- 唯一编码表SHA-256：`{source_hash}`\n"
            f"- 分析单元：{total_items}个\n"
            f"- 编码记录：{len(rows)}行\n"
            f"- 届次：{len(items_by_year)}届\n\n"
            "本目录只报告描述性分布。统计对象是复赛理论试题的任务要求，"
            "不能用于推断学生实际科学思维水平、教学效果、因果关系或统计显著性。\n\n"
            "## 输出文件\n\n"
            + "\n".join(f"- `{filename}`" for filename in outputs)
            + "\n"
        )
    print(f"items={total_items}")
    print(f"coding_rows={len(rows)}")
    print(f"years={len(items_by_year)}")
    print(f"tables={len(outputs)}")
    print(f"output_dir={output_dir}")


if __name__ == "__main__":
    main()
