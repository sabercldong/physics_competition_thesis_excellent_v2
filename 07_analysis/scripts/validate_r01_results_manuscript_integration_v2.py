#!/usr/bin/env python3
"""Validate that the current Chapter 4 and figures use the ADJ-02 corrected results."""

from __future__ import annotations

import csv
import hashlib
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CODING = ROOT / "07_analysis/data/final_coding_r01_correction_v1.csv"
OUTPUT_DIR = ROOT / "07_analysis/results/formal_rater_r01/correction_v1"
CHAPTER = ROOT / "08_manuscript/04_results.md"
FIGURE_MANIFEST = ROOT / "08_manuscript/figures/r01_manuscript_figures_manifest_v1.csv"
LEGACY_QA = ROOT / "09_quality/r01_results_manuscript_integration_qa_v1.csv"
OUTPUT_CSV = ROOT / "09_quality/r01_results_manuscript_integration_qa_v2.csv"
OUTPUT_MD = ROOT / "09_quality/r01_results_manuscript_integration_qa_v2.md"
DIMENSIONS = ["模型建构", "科学推理", "科学论证", "质疑创新"]
LEVELS = ["L1", "L2", "L3", "L4"]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def add(
    checks: list[tuple[str, str, str, str, bool, str]],
    item: str,
    expected: str,
    actual: str,
    passed: bool,
    source: str,
) -> None:
    checks.append((f"MRQA2-{len(checks) + 1:02d}", item, expected, actual, passed, source))


def main() -> None:
    chapter = CHAPTER.read_text(encoding="utf-8")
    coding_hash = sha256(CODING)
    coding = read_rows(CODING)
    by_item: dict[str, dict[str, dict[str, str]]] = defaultdict(dict)
    for row in coding:
        by_item[row["item_id"]][row["dimension"]] = row
    presence = {row["dimension"]: row for row in read_rows(OUTPUT_DIR / "final_dimension_presence.csv")}
    levels = {(row["dimension"], row["level"]): row for row in read_rows(OUTPUT_DIR / "final_level_distribution.csv")}
    cooccurrence = {(row["dimension_a"], row["dimension_b"]): row for row in read_rows(OUTPUT_DIR / "final_dimension_cooccurrence.csv")}
    figures = read_rows(FIGURE_MANIFEST)
    legacy = (ROOT / "09_quality/r01_results_manuscript_integration_qa_v1.csv").read_text(encoding="utf-8-sig")
    checks: list[tuple[str, str, str, str, bool, str]] = []

    add(checks, "当前编码行数和分析单元", "876/219", f"{len(coding)}/{len(by_item)}", len(coding) == 876 and len(by_item) == 219, "final_coding_r01_correction_v1.csv")
    for dimension in DIMENSIONS:
        count = sum(row[dimension]["present"] == "1" for row in by_item.values())
        expected_row = f"| {dimension} | {count} | 219 | {count / 219:.2%} |"
        stat = presence.get(dimension, {})
        add(
            checks,
            f"{dimension}出现数、统计输出与正文表",
            expected_row,
            "存在" if expected_row in chapter else "缺失",
            stat.get("items_present") == str(count) and stat.get("total_items") == "219" and expected_row in chapter,
            "final_dimension_presence.csv;08_manuscript/04_results.md",
        )
        for level in LEVELS:
            count = sum(row[dimension]["level"] == level for row in by_item.values())
            stat = levels.get((dimension, level), {})
            add(
                checks,
                f"{dimension}{level}等级数与统计输出",
                str(count),
                stat.get("count", "缺失"),
                stat.get("count") == str(count) and stat.get("source_final_coding_sha256") == coding_hash,
                "final_level_distribution.csv",
            )
    pair = ("科学论证", "质疑创新")
    both = sum(row[pair[0]]["present"] == "1" and row[pair[1]]["present"] == "1" for row in by_item.values())
    either = sum(row[pair[0]]["present"] == "1" or row[pair[1]]["present"] == "1" for row in by_item.values())
    jaccard = both / either
    phrase = f"科学论证与质疑创新共同出现{both}次，两者并集为{either}个单元，Jaccard系数为{jaccard:.4f}"
    stat = cooccurrence[pair]
    add(
        checks,
        "科学论证与质疑创新共现、统计输出与正文",
        phrase,
        "存在" if phrase in chapter else "缺失",
        stat["items_both_present"] == str(both) and stat["items_either_present"] == str(either) and float(stat["jaccard"]) == round(jaccard, 6) and phrase in chapter,
        "final_dimension_cooccurrence.csv;08_manuscript/04_results.md",
    )
    for figure in figures:
        png = ROOT / figure["png_path"]
        pdf = ROOT / figure["pdf_path"]
        figure_id = figure["figure_id"]
        add(
            checks,
            f"{figure_id}图件与当前编码哈希",
            coding_hash,
            figure.get("input_coding_sha256", "缺失"),
            figure["input_coding_sha256"] == coding_hash
            and png.is_file() and pdf.is_file()
            and sha256(png) == figure["png_sha256"]
            and sha256(pdf) == figure["pdf_sha256"]
            and figure_id in chapter,
            "r01_manuscript_figures_manifest_v1.csv;08_manuscript/04_results.md",
        )
    for phrase in ["不代表学生实际能力", "不代表教学效果", "不进行显著性检验", "不进行分值加权", "项目无法独立验证"]:
        add(checks, "第四章边界语句", phrase, "存在" if phrase in chapter else "缺失", phrase in chapter, "08_manuscript/04_results.md")
    add(
        checks,
        "历史V1更正前基线识别",
        "含87项与153项基线值",
        "存在" if "| 质疑创新 | 87 | 219 | 39.73% |" in legacy and "153个单元" in legacy else "缺失",
        "| 质疑创新 | 87 | 219 | 39.73% |" in legacy and "153个单元" in legacy,
        "09_quality/r01_results_manuscript_integration_qa_v1.csv",
    )

    with OUTPUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["check_id", "check_item", "expected", "actual", "status", "source"])
        for check in checks:
            writer.writerow([*check[:4], "通过" if check[4] else "不通过", check[5]])
    failures = [check[0] for check in checks if not check[4]]
    OUTPUT_MD.write_text(
        "# R01第四章当前结果整合QA（V2）\n\n"
        f"共完成{len(checks)}项检查，{'全部通过' if not failures else '不通过：' + '、'.join(failures)}。"
        "V2只允许当前ADJ-02更正版本进入第四章和图4-1/图4-2；"
        "`r01_results_manuscript_integration_qa_v1.csv`保留为更正前87项质疑创新、153项并集的历史基线，不得作为当前正文或图件依据。"
        "本QA不验证评分者身份或过程独立性，也不把描述统计外推为学生能力、教学效果、显著性或因果结论。\n",
        encoding="utf-8",
    )
    if failures:
        raise SystemExit("第四章当前结果整合QA失败：" + ", ".join(failures))
    print(f"R01第四章当前结果整合QA V2：{len(checks)}/{len(checks)}通过")


if __name__ == "__main__":
    main()
