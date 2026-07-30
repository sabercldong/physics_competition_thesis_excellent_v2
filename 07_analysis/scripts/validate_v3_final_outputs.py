#!/usr/bin/env python3
"""Independently validate the accepted V3 unique table, result tables, and figures."""

from __future__ import annotations

import argparse
import csv
import hashlib
from collections import Counter, defaultdict
from decimal import Decimal
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
DIMENSIONS = ("模型建构", "科学推理", "科学论证", "质疑创新")
LEVELS = ("L1", "L2", "L3", "L4", "未出现")
EXPECTED_ROWS = 884
EXPECTED_ITEMS = 221
QA_FIELDS = ("检查编号", "检查项目", "状态", "说明")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--coding", type=Path, required=True)
    parser.add_argument("--results-dir", type=Path, required=True)
    parser.add_argument("--figures-dir", type=Path, required=True)
    parser.add_argument("--qa-output", type=Path, required=True)
    return parser.parse_args()


def resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def ratio(numerator: int, denominator: int) -> Decimal:
    return (Decimal(numerator) / Decimal(denominator)).quantize(Decimal("0.000001"))


def main() -> None:
    args = parse_args()
    coding_path = resolve(args.coding)
    results_dir = resolve(args.results_dir)
    figures_dir = resolve(args.figures_dir)
    qa_path = resolve(args.qa_output)
    checks: list[dict[str, str]] = []

    def add_check(item: str, passed: bool, detail: str) -> None:
        checks.append(
            {
                "检查编号": f"G8-68-QA-{len(checks) + 1:02d}",
                "检查项目": item,
                "状态": "通过" if passed else "不通过",
                "说明": detail,
            }
        )

    rows = read_rows(coding_path)
    coding_hash = sha256(coding_path)
    add_check("唯一编码表记录数", len(rows) == EXPECTED_ROWS, f"实际{len(rows)}行")

    keys = [(row["item_id"], row["dimension"]) for row in rows]
    add_check(
        "分析单元×维度唯一键",
        len(set(keys)) == EXPECTED_ROWS,
        f"唯一键{len(set(keys))}个",
    )
    by_item: dict[str, dict[str, dict[str, str]]] = defaultdict(dict)
    for row in rows:
        by_item[row["item_id"]][row["dimension"]] = row
    complete_items = sum(set(item_rows) == set(DIMENSIONS) for item_rows in by_item.values())
    add_check(
        "221个分析单元四维覆盖",
        len(by_item) == EXPECTED_ITEMS and complete_items == EXPECTED_ITEMS,
        f"分析单元{len(by_item)}个，四维完整{complete_items}个",
    )

    label_errors = [
        row
        for row in rows
        if (row["present"] == "1") != (row["present_label"] == "是")
        or (row["present"] == "1" and row["level"] not in LEVELS[:4])
        or (row["present"] == "0" and row["level"] != "未出现")
    ]
    add_check("存在性与等级逻辑", not label_errors, f"异常{len(label_errors)}行")

    corrections = [
        row
        for row in rows
        if row["author_review_decision"] == "更正候选"
    ]
    changed = [
        row
        for row in rows
        if row["candidate_present_label"] != row["present_label"]
        or row["candidate_level"] != row["level"]
    ]
    add_check(
        "15项人工更正落表",
        len(corrections) == 15 and len(changed) == 15
        and {row["review_row_id"] for row in corrections}
        == {row["review_row_id"] for row in changed},
        f"更正决定{len(corrections)}行，标签变化{len(changed)}行",
    )

    source_review_hashes = {row["source_author_review_sha256"] for row in rows}
    source_acceptance_hashes = {
        row["source_g8_80_acceptance_sha256"] for row in rows
    }
    add_check(
        "来源哈希全表唯一",
        len(source_review_hashes) == 1 and len(source_acceptance_hashes) == 1,
        f"作者复核哈希{len(source_review_hashes)}个，验收哈希{len(source_acceptance_hashes)}个",
    )

    presence_rows = read_rows(results_dir / "总体维度出现分布.csv")
    presence_by_dimension = {row["维度"]: row for row in presence_rows}
    presence_errors = []
    for dimension in DIMENSIONS:
        count = sum(item_rows[dimension]["present"] == "1" for item_rows in by_item.values())
        result = presence_by_dimension.get(dimension, {})
        if (
            result.get("出现题目数") != str(count)
            or result.get("全部题目数") != str(EXPECTED_ITEMS)
            or result.get("出现比例") != f"{ratio(count, EXPECTED_ITEMS):.6f}"
            or result.get("源唯一编码表SHA256") != coding_hash
        ):
            presence_errors.append(dimension)
    add_check(
        "总体维度分布独立复算",
        not presence_errors and len(presence_rows) == 4,
        "4个维度一致" if not presence_errors else "不一致：" + "、".join(presence_errors),
    )

    level_rows = read_rows(results_dir / "各维度等级分布.csv")
    level_by_key = {(row["维度"], row["层级"]): row for row in level_rows}
    level_errors = []
    for dimension in DIMENSIONS:
        counts = Counter(item_rows[dimension]["level"] for item_rows in by_item.values())
        present_count = EXPECTED_ITEMS - counts["未出现"]
        for level in LEVELS:
            result = level_by_key.get((dimension, level), {})
            expected_present_ratio = (
                f"{ratio(counts[level], present_count):.6f}"
                if level != "未出现"
                else ""
            )
            if (
                result.get("题目数") != str(counts[level])
                or result.get("维度出现题目数") != str(present_count)
                or result.get("全部题目数") != str(EXPECTED_ITEMS)
                or result.get("占维度出现题目比例") != expected_present_ratio
                or result.get("占全部题目比例")
                != f"{ratio(counts[level], EXPECTED_ITEMS):.6f}"
                or result.get("源唯一编码表SHA256") != coding_hash
            ):
                level_errors.append(f"{dimension}/{level}")
    add_check(
        "各维度等级分布独立复算",
        not level_errors and len(level_rows) == 20,
        "20个维度×层级单元一致"
        if not level_errors
        else "不一致：" + "、".join(level_errors),
    )

    year_presence_rows = read_rows(results_dir / "分届次维度出现分布.csv")
    year_groups: dict[tuple[str, str], list[dict[str, dict[str, str]]]] = defaultdict(list)
    for item_rows in by_item.values():
        example = next(iter(item_rows.values()))
        year_groups[(example["year"], example["competition_no"])].append(item_rows)
    year_result_by_key = {
        (row["年份"], row["竞赛届次"], row["维度"]): row
        for row in year_presence_rows
    }
    year_errors = []
    for (year, competition_no), items in year_groups.items():
        for dimension in DIMENSIONS:
            count = sum(item[dimension]["present"] == "1" for item in items)
            result = year_result_by_key.get((year, competition_no, dimension), {})
            if (
                result.get("出现题目数") != str(count)
                or result.get("该届题目数") != str(len(items))
                or result.get("出现比例") != f"{ratio(count, len(items)):.6f}"
                or result.get("源唯一编码表SHA256") != coding_hash
            ):
                year_errors.append(f"{competition_no}/{dimension}")
    add_check(
        "分届次维度分布独立复算",
        not year_errors and len(year_presence_rows) == 32 and len(year_groups) == 8,
        "8届×4维共32行一致"
        if not year_errors
        else "不一致：" + "、".join(year_errors),
    )

    year_level_rows = read_rows(results_dir / "分届次维度等级分布.csv")
    year_level_by_key = {
        (row["年份"], row["竞赛届次"], row["维度"], row["层级"]): row
        for row in year_level_rows
    }
    year_level_errors = []
    for (year, competition_no), items in year_groups.items():
        for dimension in DIMENSIONS:
            counts = Counter(item[dimension]["level"] for item in items)
            for level in LEVELS:
                result = year_level_by_key.get(
                    (year, competition_no, dimension, level),
                    {},
                )
                if (
                    result.get("题目数") != str(counts[level])
                    or result.get("该届题目数") != str(len(items))
                    or result.get("占该届全部题目比例")
                    != f"{ratio(counts[level], len(items)):.6f}"
                    or result.get("源唯一编码表SHA256") != coding_hash
                ):
                    year_level_errors.append(f"{competition_no}/{dimension}/{level}")
    add_check(
        "分届次等级分布独立复算",
        not year_level_errors and len(year_level_rows) == 160,
        "8届×4维×5层级共160行一致"
        if not year_level_errors
        else f"不一致{len(year_level_errors)}项",
    )

    combination_rows = read_rows(results_dir / "维度组合分布.csv")
    expected_combinations: Counter[str] = Counter()
    for item_rows in by_item.values():
        present_dimensions = [
            dimension
            for dimension in DIMENSIONS
            if item_rows[dimension]["present"] == "1"
        ]
        label = "＋".join(present_dimensions) if present_dimensions else "四维均未出现"
        expected_combinations[label] += 1
    actual_combinations = {
        row["维度组合"]: int(row["题目数"]) for row in combination_rows
    }
    combination_sources = {
        row["源唯一编码表SHA256"] for row in combination_rows
    }
    add_check(
        "维度组合分布独立复算",
        actual_combinations == dict(expected_combinations)
        and sum(actual_combinations.values()) == EXPECTED_ITEMS
        and combination_sources == {coding_hash},
        f"组合{len(actual_combinations)}类，合计{sum(actual_combinations.values())}题",
    )

    cooccurrence_rows = read_rows(results_dir / "维度共现分布.csv")
    cooccurrence_by_key = {
        (row["维度甲"], row["维度乙"]): row for row in cooccurrence_rows
    }
    cooccurrence_errors = []
    for left_index, left in enumerate(DIMENSIONS):
        for right in DIMENSIONS[left_index + 1 :]:
            left_items = {
                item_id
                for item_id, item_rows in by_item.items()
                if item_rows[left]["present"] == "1"
            }
            right_items = {
                item_id
                for item_id, item_rows in by_item.items()
                if item_rows[right]["present"] == "1"
            }
            both = len(left_items & right_items)
            union = len(left_items | right_items)
            result = cooccurrence_by_key.get((left, right), {})
            if (
                result.get("共同出现题目数") != str(both)
                or result.get("至少一个出现题目数") != str(union)
                or result.get("共同出现占全部比例")
                != f"{ratio(both, EXPECTED_ITEMS):.6f}"
                or result.get("Jaccard系数") != f"{ratio(both, union):.6f}"
                or result.get("源唯一编码表SHA256") != coding_hash
            ):
                cooccurrence_errors.append(f"{left}/{right}")
    add_check(
        "维度共现分布独立复算",
        not cooccurrence_errors and len(cooccurrence_rows) == 6,
        "6个维度对一致"
        if not cooccurrence_errors
        else "不一致：" + "、".join(cooccurrence_errors),
    )

    source_rows = read_rows(results_dir / "结果数据来源登记.csv")
    source = source_rows[0] if len(source_rows) == 1 else {}
    add_check(
        "统计来源登记",
        len(source_rows) == 1
        and source.get("唯一编码表SHA256") == coding_hash
        and source.get("分析单元数") == str(EXPECTED_ITEMS)
        and source.get("编码记录数") == str(EXPECTED_ROWS),
        f"来源登记{len(source_rows)}行，唯一表SHA-256={coding_hash}",
    )

    manifest_rows = read_rows(figures_dir / "V3结果图件来源登记.csv")
    figure_errors = []
    for row in manifest_rows:
        png_path = resolve(Path(row["PNG文件"]))
        pdf_path = resolve(Path(row["PDF文件"]))
        if (
            row["源唯一编码表SHA256"] != coding_hash
            or not png_path.is_file()
            or not pdf_path.is_file()
            or (png_path.is_file() and sha256(png_path) != row["PNG文件SHA256"])
            or (pdf_path.is_file() and sha256(pdf_path) != row["PDF文件SHA256"])
        ):
            figure_errors.append(row.get("图号", "未知"))
            continue
        with Image.open(png_path) as image:
            extrema = image.convert("RGB").getextrema()
            nonblank = any(low != high for low, high in extrema)
            if image.width < 1200 or image.height < 700 or not nonblank:
                figure_errors.append(row.get("图号", "未知"))
    add_check(
        "正式图件来源、哈希与非空检查",
        not figure_errors and len(manifest_rows) == 4,
        "4幅PNG/PDF图件通过"
        if not figure_errors
        else "异常：" + "、".join(figure_errors),
    )

    qa_path.parent.mkdir(parents=True, exist_ok=True)
    with qa_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=QA_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(checks)
    failures = [check for check in checks if check["状态"] != "通过"]
    print(f"checks={len(checks)}")
    print(f"failures={len(failures)}")
    print(f"coding_sha256={coding_hash}")
    print(f"qa={qa_path}")
    if failures:
        raise SystemExit("G8-68正式结果复算存在失败项")


if __name__ == "__main__":
    main()
