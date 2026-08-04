#!/usr/bin/env python3
"""Compare the accepted V3 table with the full-source candidate simulation."""

from __future__ import annotations

import argparse
import csv
import hashlib
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BASELINE_DEFAULT = ROOT / "07_analysis/data/第35至42届科学思维第三版唯一编码表.csv"
CANDIDATE_DEFAULT = (
    ROOT
    / "07_analysis/data/v3_independent_validation/adjudication"
    / "完整原文复核_146行_20260803/合并结果"
    / "若采纳完整原文候选裁决的884行模拟表.csv"
)
OUT_DEFAULT = (
    ROOT
    / "07_analysis/results/第三版三方分歧完整原文候选敏感性"
)
DIMENSIONS = ("模型建构", "科学推理", "科学论证", "质疑创新")
LEVELS = ("未出现", "L1", "L2", "L3", "L4")


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", type=Path, default=BASELINE_DEFAULT)
    parser.add_argument("--candidate", type=Path, default=CANDIDATE_DEFAULT)
    parser.add_argument("--output-dir", type=Path, default=OUT_DEFAULT)
    return parser.parse_args()


def resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def main() -> None:
    args = parse_args()
    baseline_path = resolve(args.baseline)
    candidate_path = resolve(args.candidate)
    output_dir = resolve(args.output_dir)
    baseline_fields, baseline = read_csv(baseline_path)
    candidate_fields, candidate = read_csv(candidate_path)
    if baseline_fields != candidate_fields:
        raise ValueError("基线与候选模拟表字段不一致")
    if len(baseline) != 884 or len(candidate) != 884:
        raise ValueError("两张表都必须为884行")
    key = lambda row: row["review_row_id"]
    baseline_by_id = {key(row): row for row in baseline}
    candidate_by_id = {key(row): row for row in candidate}
    if set(baseline_by_id) != set(candidate_by_id):
        raise ValueError("两张表的review_row_id集合不一致")

    dimension_rows: list[dict[str, str]] = []
    for dimension in DIMENSIONS:
        baseline_subset = [row for row in baseline if row["dimension"] == dimension]
        candidate_subset = [row for row in candidate if row["dimension"] == dimension]
        for level in LEVELS:
            before = sum(row["level"] == level for row in baseline_subset)
            after = sum(row["level"] == level for row in candidate_subset)
            dimension_rows.append(
                {
                    "维度": dimension,
                    "标签": level,
                    "第三版数量": str(before),
                    "完整原文候选数量": str(after),
                    "变化量": str(after - before),
                }
            )
    write_csv(
        output_dir / "总体维度标签变化.csv",
        ["维度", "标签", "第三版数量", "完整原文候选数量", "变化量"],
        dimension_rows,
    )

    transitions = Counter()
    changed_rows: list[dict[str, str]] = []
    for row_id, before in baseline_by_id.items():
        after = candidate_by_id[row_id]
        if before["level"] == after["level"]:
            continue
        transitions[(before["dimension"], before["level"], after["level"])] += 1
        changed_rows.append(
            {
                "review_row_id": row_id,
                "item_id": before["item_id"],
                "届次": before["competition_no"],
                "维度": before["dimension"],
                "第三版标签": before["level"],
                "完整原文候选标签": after["level"],
            }
        )
    transition_rows = [
        {
            "维度": dimension,
            "第三版标签": before,
            "完整原文候选标签": after,
            "数量": str(count),
        }
        for (dimension, before, after), count in sorted(
            transitions.items(), key=lambda item: (-item[1], item[0])
        )
    ]
    write_csv(
        output_dir / "标签转移汇总.csv",
        ["维度", "第三版标签", "完整原文候选标签", "数量"],
        transition_rows,
    )
    write_csv(
        output_dir / "884行标签变化明细.csv",
        ["review_row_id", "item_id", "届次", "维度", "第三版标签", "完整原文候选标签"],
        changed_rows,
    )

    years = sorted({row["competition_no"] for row in baseline}, key=int)
    year_rows: list[dict[str, str]] = []
    for year in years:
        for dimension in DIMENSIONS:
            before_rows = [
                row for row in baseline
                if row["competition_no"] == year and row["dimension"] == dimension
            ]
            after_rows = [
                row for row in candidate
                if row["competition_no"] == year and row["dimension"] == dimension
            ]
            before = sum(row["present"] == "1" for row in before_rows)
            after = sum(row["present"] == "1" for row in after_rows)
            year_rows.append(
                {
                    "届次": year,
                    "维度": dimension,
                    "分析单元数": str(len(before_rows)),
                    "第三版出现数": str(before),
                    "完整原文候选出现数": str(after),
                    "出现数变化": str(after - before),
                }
            )
    write_csv(
        output_dir / "分届次维度出现变化.csv",
        ["届次", "维度", "分析单元数", "第三版出现数", "完整原文候选出现数", "出现数变化"],
        year_rows,
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    report = output_dir / "完整原文候选敏感性说明.md"
    report.write_text(
        "# 完整原文候选裁决敏感性说明\n\n"
        f"- 第三版基线SHA-256：`{sha256(baseline_path)}`；\n"
        f"- 884行候选模拟表SHA-256：`{sha256(candidate_path)}`；\n"
        f"- 发生标签变化的编码记录：{len(changed_rows)}行。\n\n"
        "该目录只比较第三版正式表与完整原文模型辅助候选的统计差异。"
        "它不把候选模拟表替换为正式主数据，也不把模型复核表述为真人裁决。\n",
        encoding="utf-8",
    )
    print(f"CHANGED_ROWS={len(changed_rows)}")
    print(f"TRANSITIONS={len(transition_rows)}")
    print(f"OUTPUT={output_dir}")


if __name__ == "__main__":
    main()
