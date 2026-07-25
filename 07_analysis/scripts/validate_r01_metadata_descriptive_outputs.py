#!/usr/bin/env python3
"""Validate reproducible R01 descriptive tables stratified by metadata component counts."""

from __future__ import annotations

import csv
import hashlib
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CODING = ROOT / "07_analysis/data/final_coding_r01_correction_v1.csv"
ITEM_INDEX = ROOT / "03_corpus/item_index.csv"
OUTPUT_DIR = ROOT / "07_analysis/results/formal_rater_r01/correction_v1"
OUTPUT_CSV = ROOT / "09_quality/r01_metadata_descriptive_outputs_qa_v1.csv"
OUTPUT_MD = ROOT / "09_quality/r01_metadata_descriptive_outputs_qa_v1.md"
DIMENSIONS = ["模型建构", "科学推理", "科学论证", "质疑创新"]
SPECS = {
    "representation": ("representation_component_count", "final_representation_component_dimension_presence.csv"),
    "math_tools": ("math_tools_component_count", "final_math_tools_component_dimension_presence.csv"),
}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def add(checks: list[tuple[str, str, str, str, bool, str]], item: str, expected: str, actual: str, passed: bool, source: str) -> None:
    checks.append((f"MDQA-{len(checks) + 1:02d}", item, expected, actual, passed, source))


def main() -> None:
    coding = read_rows(CODING)
    index = read_rows(ITEM_INDEX)
    coding_sha = sha256(CODING)
    index_sha = sha256(ITEM_INDEX)
    by_item: dict[str, dict[str, dict[str, str]]] = defaultdict(dict)
    for row in coding:
        by_item[row["item_id"]][row["dimension"]] = row
    item_meta = {row["item_id"]: row for row in index}
    checks: list[tuple[str, str, str, str, bool, str]] = []
    add(checks, "唯一分析单位数", "219", str(len(item_meta)), len(item_meta) == 219 and set(by_item) == set(item_meta), "item_index;final_coding")
    add(checks, "编码记录数", "876", str(len(coding)), len(coding) == 876, "final_coding")

    for field, (count_column, filename) in SPECS.items():
        output_path = OUTPUT_DIR / filename
        output_rows = read_rows(output_path)
        expected: dict[tuple[int, str], tuple[int, int]] = {}
        groups: dict[int, list[str]] = defaultdict(list)
        for item_id, meta in item_meta.items():
            parts = [part.strip() for part in meta[field].split("；") if part.strip()]
            groups[len(parts)].append(item_id)
        for count, item_ids in groups.items():
            for dimension in DIMENSIONS:
                expected[(count, dimension)] = (
                    sum(by_item[item_id][dimension]["present"] == "1" for item_id in item_ids),
                    len(item_ids),
                )
        observed = {(int(row[count_column]), row["dimension"]): row for row in output_rows}
        add(checks, f"{field}分层键覆盖", str(len(expected)), str(len(observed)), set(expected) == set(observed), filename)
        add(
            checks,
            f"{field}分层样本数",
            "219",
            str(sum(len(item_ids) for item_ids in groups.values())),
            sum(len(item_ids) for item_ids in groups.values()) == 219,
            "item_index",
        )
        for key, (present, total) in sorted(expected.items()):
            row = observed.get(key, {})
            passed = (
                row.get("items_present") == str(present)
                and row.get("total_items") == str(total)
                and row.get("source_final_coding_sha256") == coding_sha
                and row.get("source_item_index_sha256") == index_sha
                and row.get("counting_rule") == "以全角分号；分隔的非空元数据要素计数"
            )
            add(checks, f"{field}要素数{key[0]}的{key[1]}", f"{present}/{total}", f"{row.get('items_present', '缺失')}/{row.get('total_items', '缺失')}", passed, filename)

    with OUTPUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["check_id", "check_item", "expected", "actual", "status", "source"])
        for check in checks:
            writer.writerow([*check[:4], "通过" if check[4] else "不通过", check[5]])
    failures = [check[0] for check in checks if not check[4]]
    OUTPUT_MD.write_text(
        "# R01元数据要素数分层描述输出QA\n\n"
        f"共{len(checks)}项检查，{'全部通过' if not failures else '不通过：' + '、'.join(failures)}。\n\n"
        "本QA只验证以全角分号分隔的元数据要素计数及其与当前编码表的逐层频数对应。"
        "要素数是索引记录的结构计数，不是题目难度、认知负荷、学生能力、因果效应或统计显著性的测量。\n",
        encoding="utf-8",
    )
    if failures:
        raise SystemExit("元数据描述输出QA失败：" + ", ".join(failures))
    print(f"R01元数据要素数分层描述输出QA：{len(checks)}/{len(checks)}通过")


if __name__ == "__main__":
    main()
