#!/usr/bin/env python3
"""Verify that the Chinese abstract draft matches the frozen R01 results and boundaries."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ABSTRACT = ROOT / "08_manuscript/00_abstract_content_draft.md"
ENGLISH_ABSTRACT = ROOT / "08_manuscript/00_abstract_en_content_draft.md"
CODING = ROOT / "07_analysis/data/final_coding_r01_correction_v1.csv"
OUTPUT_CSV = ROOT / "09_quality/r01_abstract_alignment_qa_v1.csv"
OUTPUT_MD = ROOT / "09_quality/r01_abstract_alignment_qa_v1.md"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    text = ABSTRACT.read_text(encoding="utf-8")
    english_text = ENGLISH_ABSTRACT.read_text(encoding="utf-8")
    rows = read_rows(CODING)
    dimensions = ["模型建构", "科学推理", "科学论证", "质疑创新"]
    expected_presence = {"模型建构": 203, "科学推理": 219, "科学论证": 106, "质疑创新": 84}
    expected_levels = {
        "模型建构": {"L1": 109, "L2": 22, "L3": 72},
        "科学推理": {"L1": 121, "L2": 81, "L3": 17},
        "科学论证": {"L1": 79, "L2": 16, "L3": 11},
        "质疑创新": {"L1": 20, "L2": 51, "L3": 5, "L4": 8},
    }
    checks: list[tuple[str, str, str, str, bool]] = []
    checks.append(("AA-QA-01", "编码记录数", "876", str(len(rows)), len(rows) == 876))
    item_count = len({row["item_id"] for row in rows})
    checks.append(("AA-QA-02", "分析单元数", "219", str(item_count), item_count == 219))
    for index, dimension in enumerate(dimensions, start=3):
        values = [row for row in rows if row["dimension"] == dimension]
        present = [row for row in values if row["present"] == "1"]
        actual_levels = dict(Counter(row["level"] for row in present))
        checks.append((
            f"AA-QA-{index:02d}",
            f"{dimension}冻结结果",
            f"出现{expected_presence[dimension]}；等级{expected_levels[dimension]}",
            f"出现{len(present)}；等级{actual_levels}",
            len(values) == 219 and len(present) == expected_presence[dimension] and actual_levels == expected_levels[dimension],
        ))
    argument = {row["item_id"] for row in rows if row["dimension"] == "科学论证" and row["present"] == "1"}
    innovation = {row["item_id"] for row in rows if row["dimension"] == "质疑创新" and row["present"] == "1"}
    model = {row["item_id"] for row in rows if row["dimension"] == "模型建构" and row["present"] == "1"}
    reasoning = {row["item_id"] for row in rows if row["dimension"] == "科学推理" and row["present"] == "1"}
    checks.extend([
        ("AA-QA-07", "模型建构与科学推理共现", "203", str(len(model & reasoning)), len(model & reasoning) == 203),
        ("AA-QA-08", "科学论证与质疑创新共现", "40", str(len(argument & innovation)), len(argument & innovation) == 40),
        ("AA-QA-09", "科学论证与质疑创新并集", "150", str(len(argument | innovation)), len(argument | innovation) == 150),
    ])
    required_text = [
        "建立219个分析单元",
        "形成876条当前编码记录",
        "分别出现于203、219、106和84个分析单元",
        "均以L1占比最高，质疑创新以L2占比最高",
        "共同出现于203个分析单元",
        "共同出现于40个分析单元，二者并集为150个单元",
        "不能推断学生实际能力、教学效果、因果关系、长期趋势或第35届试题分值差异",
        "身份、独立性及实际人工过程仅按自声明登记",
        "项目未采集教师、学生或课堂数据",
    ]
    for index, term in enumerate(required_text, start=10):
        checks.append((f"AA-QA-{index:02d}", "摘要必要表述", term, "存在" if term in text else "缺失", term in text))
    english_required = [
        "219 analysis units",
        "876 records",
        "203, 219, 106, and 84 analysis units",
        "L1 was the most frequent level",
        "L2 was the most frequent level for questioning and innovation",
        "co-occurred in 203 analysis units",
        "co-occurred in 40 analysis units, with a union of 150 units",
        "do not indicate students' actual capabilities, instructional effectiveness, causal effects, long-term trends, or score differences for the 35th edition",
        "recorded only through self-declarations",
        "No teacher, student, or classroom data were collected",
    ]
    for index, term in enumerate(english_required, start=19):
        checks.append((f"AA-QA-{index:02d}", "英文摘要必要表述", term, "存在" if term in english_text else "缺失", term in english_text))
    with OUTPUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["check_id", "check_item", "expected", "actual", "status"])
        for check in checks:
            writer.writerow([*check[:4], "通过" if check[4] else "不通过"])
    failures = [check[0] for check in checks if not check[4]]
    OUTPUT_MD.write_text(
        "# R01 中英文摘要与冻结结果对齐 QA（V1）\n\n"
        f"共完成{len(checks)}项检查，{'全部通过' if not failures else '不通过：' + '、'.join(failures)}。"
        "本QA只核验中英文摘要工作底稿与当前冻结编码的数值、等级判断、共现关系及禁止外推边界；"
        "不验证评分者身份或过程、理论外部效度、学生能力、教学效果、学校格式、官方英文赛事名或人类参与者事实。\n",
        encoding="utf-8",
    )
    if failures:
        raise SystemExit("摘要对齐QA失败：" + ", ".join(failures))
    print(f"R01中英文摘要对齐QA：{len(checks)}/{len(checks)}通过")


if __name__ == "__main__":
    main()
