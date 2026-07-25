from __future__ import annotations

import csv
import hashlib
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DIMENSIONS = ["模型建构", "科学推理", "科学论证", "质疑创新"]
LEVELS = ["L1", "L2", "L3", "L4"]
CURRENT = ROOT / "07_analysis/data/final_coding_r01_correction_v1.csv"
CHAIN = ROOT / "07_analysis/data/final_coding_evidence_r01_v1.csv"
OUTPUT_DIR = ROOT / "07_analysis/results/formal_rater_r01/correction_v1"
RELIABILITY = ROOT / "07_analysis/results/formal_rater_r01/r01_reliability_by_dimension.csv"
DISAGREEMENTS = ROOT / "07_analysis/results/formal_rater_r01/r01_reliability_disagreements.csv"
CORRECTIONS = ROOT / "07_analysis/results/formal_rater_r01/r01_correction_adjudication_change_manifest_v1.csv"
CHAPTER = ROOT / "08_manuscript/04_results.md"
METHODS = ROOT / "08_manuscript/03_methods.md"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = ["check_id", "check_item", "expected", "actual", "status", "source"]
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def add_check(rows: list[dict[str, str]], check_id: str, item: str, expected: str, actual: str, passed: bool, source: str) -> None:
    rows.append({
        "check_id": check_id,
        "check_item": item,
        "expected": expected,
        "actual": actual,
        "status": "通过" if passed else "不通过",
        "source": source,
    })


def main() -> int:
    output = ROOT / "09_quality/r01_results_eligibility_qa_v1.csv"
    checks: list[dict[str, str]] = []
    current = read_rows(CURRENT)
    chain = read_rows(CHAIN)
    current_by_key = {(row["item_id"], row["dimension"]): row for row in current}
    chain_by_key = {(row["item_id"], row["dimension"]): row for row in chain}
    add_check(checks, "RE-QA-01", "当前编码表记录和唯一键", "876/876", f"{len(current)}/{len(current_by_key)}", len(current) == len(current_by_key) == 876, CURRENT.relative_to(ROOT).as_posix())
    add_check(checks, "RE-QA-02", "当前证据链记录和唯一键", "876/876", f"{len(chain)}/{len(chain_by_key)}", len(chain) == len(chain_by_key) == 876, CHAIN.relative_to(ROOT).as_posix())
    add_check(checks, "RE-QA-03", "编码表与证据链键集合", "一致", "一致" if set(current_by_key) == set(chain_by_key) else "不一致", set(current_by_key) == set(chain_by_key), CHAIN.relative_to(ROOT).as_posix())
    values_match = all(
        (row["present_label"], row["level"]) == (chain_by_key[key]["current_present"], chain_by_key[key]["current_level"])
        for key, row in current_by_key.items() if key in chain_by_key
    )
    add_check(checks, "RE-QA-04", "当前编码值与证据链", "876条逐键一致", "一致" if values_match else "不一致", values_match, CHAIN.relative_to(ROOT).as_posix())
    sources = Counter(row["evidence_source"] for row in chain)
    expected_sources = {"R01-V6": 840, "R01-EVIDENCE-REPAIR-V2": 32, "ADJ-02-CORRECTION": 4}
    add_check(checks, "RE-QA-05", "证据链来源构成", str(expected_sources), str(dict(sources)), dict(sources) == expected_sources, CHAIN.relative_to(ROOT).as_posix())
    current_sha = hashlib.sha256(CURRENT.read_bytes()).hexdigest()
    presence = {row["dimension"]: row for row in read_rows(OUTPUT_DIR / "final_dimension_presence.csv")}
    levels = {(row["dimension"], row["level"]): row for row in read_rows(OUTPUT_DIR / "final_level_distribution.csv")}
    cooccurrence = {(row["dimension_a"], row["dimension_b"]): row for row in read_rows(OUTPUT_DIR / "final_dimension_cooccurrence.csv")}
    by_item: dict[str, dict[str, dict[str, str]]] = defaultdict(dict)
    for row in current:
        by_item[row["item_id"]][row["dimension"]] = row
    output_sha_ok = all(row["source_final_coding_sha256"] == current_sha for row in presence.values()) and all(row["source_final_coding_sha256"] == current_sha for row in levels.values()) and all(row["source_final_coding_sha256"] == current_sha for row in cooccurrence.values())
    add_check(checks, "RE-QA-06", "描述统计输出版本哈希", current_sha, "一致" if output_sha_ok else "不一致", output_sha_ok, "07_analysis/results/formal_rater_r01/correction_v1/")
    for index, dimension in enumerate(DIMENSIONS, start=1):
        present_count = sum(row[dimension]["present"] == "1" for row in by_item.values())
        row = presence.get(dimension, {})
        passed = row.get("items_present") == str(present_count) and row.get("total_items") == "219"
        add_check(checks, f"RE-QA-P{index}", f"{dimension}出现统计", f"{present_count}/219", f"{row.get('items_present', '')}/{row.get('total_items', '')}", passed, "final_dimension_presence.csv")
        for level in LEVELS:
            count = sum(row[dimension]["level"] == level for row in by_item.values())
            level_row = levels.get((dimension, level), {})
            add_check(checks, f"RE-QA-L{index}-{level}", f"{dimension} {level}等级统计", str(count), level_row.get("count", ""), level_row.get("count") == str(count), "final_level_distribution.csv")
    pair = ("科学论证", "质疑创新")
    both = sum(row[pair[0]]["present"] == "1" and row[pair[1]]["present"] == "1" for row in by_item.values())
    either = sum(row[pair[0]]["present"] == "1" or row[pair[1]]["present"] == "1" for row in by_item.values())
    pair_row = cooccurrence[pair]
    add_check(checks, "RE-QA-C1", "科学论证与质疑创新共现", f"{both}/{either}/0.266667", f"{pair_row['items_both_present']}/{pair_row['items_either_present']}/{pair_row['jaccard']}", pair_row["items_both_present"] == str(both) and pair_row["items_either_present"] == str(either) and pair_row["jaccard"] == "0.266667", "final_dimension_cooccurrence.csv")
    chapter_text = CHAPTER.read_text(encoding="utf-8")
    methods_text = METHODS.read_text(encoding="utf-8")
    reliability = {row["dimension"]: row for row in read_rows(RELIABILITY)}
    overall = reliability.get("全部", {})
    reliability_expected = [
        ("RE-QA-R1", "全体维度存在性一致率", "96.12%", f"{float(overall.get('presence_agreement', 'nan')):.2%}", "96.12%"),
        ("RE-QA-R2", "全体维度存在性Cohen kappa", "0.9053", f"{float(overall.get('presence_kappa', 'nan')):.4f}", "0.9053"),
        ("RE-QA-R3", "双方均判出现的等级比较数", "607", overall.get("n_level_pairs_both_present", ""), "607"),
        ("RE-QA-R4", "全体等级一致率", "82.21%", f"{float(overall.get('level_agreement', 'nan')):.2%}", "82.21%"),
        ("RE-QA-R5", "全体等级二次加权kappa", "0.8638", f"{float(overall.get('weighted_kappa_level', 'nan')):.4f}", "0.8638"),
    ]
    for check_id, item, expected, actual, phrase in reliability_expected:
        add_check(
            checks,
            check_id,
            item,
            expected,
            actual,
            actual == expected and phrase in chapter_text,
            "r01_reliability_by_dimension.csv;08_manuscript/04_results.md",
        )
    disagreements = read_rows(DISAGREEMENTS)
    add_check(
        checks,
        "RE-QA-R6",
        "A/B分歧记录数",
        "142",
        str(len(disagreements)),
        len(disagreements) == 142 and "142条分歧" in chapter_text,
        "r01_reliability_disagreements.csv;08_manuscript/04_results.md",
    )
    corrections = read_rows(CORRECTIONS)
    add_check(
        checks,
        "RE-QA-R7",
        "ADJ-02采纳更正数",
        "4",
        str(len(corrections)),
        len(corrections) == 4 and "ADJ-02采纳4条" in chapter_text,
        "r01_correction_adjudication_change_manifest_v1.csv;08_manuscript/04_results.md",
    )
    expected_chapter_rows = [
        "| 模型建构 | 203 | 219 | 92.69% |",
        "| 科学推理 | 219 | 219 | 100.00% |",
        "| 科学论证 | 106 | 219 | 48.40% |",
        "| 质疑创新 | 84 | 219 | 38.36% |",
        "| 模型建构 | 203 | 109 (53.69%) | 22 (10.84%) | 72 (35.47%) | 0 (0.00%) |",
        "| 科学推理 | 219 | 121 (55.25%) | 81 (36.99%) | 17 (7.76%) | 0 (0.00%) |",
        "| 科学论证 | 106 | 79 (74.53%) | 16 (15.09%) | 11 (10.38%) | 0 (0.00%) |",
        "| 质疑创新 | 84 | 20 (23.81%) | 51 (60.71%) | 5 (5.95%) | 8 (9.52%) |",
        "科学论证与质疑创新共同出现40次，两者并集为150个单元，Jaccard系数为0.2667",
    ]
    for index, expected in enumerate(expected_chapter_rows, start=1):
        add_check(checks, f"RE-QA-M{index}", "第四章结果值", expected, "存在" if expected in chapter_text else "缺失", expected in chapter_text, "08_manuscript/04_results.md")
    for index, phrase in enumerate(["不代表学生实际能力", "不代表教学效果", "不进行显著性检验", "全样本主分析不进行分值加权", "项目无法独立验证"], start=1):
        add_check(checks, f"RE-QA-B{index}", "第四章边界语句", phrase, "存在" if phrase in chapter_text else "缺失", phrase in chapter_text, "08_manuscript/04_results.md")
    for index, phrase in enumerate(["RATER-A/B", "项目无法独立验证", "可追溯描述性结果"], start=1):
        add_check(checks, f"RE-QA-ME{index}", "第三章编码过程表述", phrase, "存在" if phrase in methods_text else "缺失", phrase in methods_text, "08_manuscript/03_methods.md")
    write_rows(output, checks)
    failures = [row for row in checks if row["status"] != "通过"]
    print(f"R01结果资格QA：{len(checks) - len(failures)}/{len(checks)}通过")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
