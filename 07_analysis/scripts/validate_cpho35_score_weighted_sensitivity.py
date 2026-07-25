#!/usr/bin/env python3
"""Validate CPHO35 score-weighted sensitivity outputs and their scope limits."""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "07_analysis/results/reviewed/cpho35_score_weighted_item_records_v1.csv"
PRESENCE = ROOT / "07_analysis/results/reviewed/cpho35_score_weighted_presence_sensitivity_v1.csv"
LEVELS = ROOT / "07_analysis/results/reviewed/cpho35_score_weighted_level_sensitivity_v1.csv"
REPORT = ROOT / "07_analysis/results/reviewed/cpho35_score_weighted_sensitivity_report_v1.md"
OUTPUT = ROOT / "09_quality/cpho35_score_weighted_sensitivity_qa_v1.csv"
QA_REPORT = ROOT / "09_quality/cpho35_score_weighted_sensitivity_qa_v1.md"
DIMENSIONS = ["模型建构", "科学推理", "科学论证", "质疑创新"]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    items, presence, levels = read_csv(ITEMS), read_csv(PRESENCE), read_csv(LEVELS)
    checks: list[tuple[str, str, bool, str]] = []

    def check(check_id: str, item: str, passed: bool, source: str) -> None:
        checks.append((check_id, item, passed, source))

    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in items:
        grouped[row["dimension"]].append(row)
    check("SCORE35-SENS-QA-01", "项目记录为26小问乘4维度共104行", len(items) == 104, ITEMS.name)
    check("SCORE35-SENS-QA-02", "每个维度均为26个小问", all(len(grouped[d]) == 26 for d in DIMENSIONS), ITEMS.name)
    check("SCORE35-SENS-QA-03", "每个小问在四维度均唯一出现", len({(row["item_id"], row["dimension"]) for row in items}) == 104, ITEMS.name)
    check("SCORE35-SENS-QA-04", "每个维度的小问分值总和为320", all(sum(int(row["subquestion_score"]) for row in grouped[d]) == 320 for d in DIMENSIONS), ITEMS.name)
    check("SCORE35-SENS-QA-05", "四维存在性表完整", [row["dimension"] for row in presence] == DIMENSIONS, PRESENCE.name)
    check("SCORE35-SENS-QA-06", "存在性表总权重均为320", all(row["total_score_points"] == "320" and row["total_items"] == "26" for row in presence), PRESENCE.name)
    check("SCORE35-SENS-QA-07", "加权比例可由点数重算", all(abs(float(row["score_weighted_proportion"]) - int(row["score_weighted_points_present"]) / 320) < 0.000001 for row in presence), PRESENCE.name)
    check("SCORE35-SENS-QA-08", "等权比例可由小问数重算", all(abs(float(row["equal_weight_proportion"]) - int(row["equal_weight_items_present"]) / 26) < 0.000001 for row in presence), PRESENCE.name)
    check("SCORE35-SENS-QA-09", "等级表为4维乘4等级", len(levels) == 16 and {(row["dimension"], row["level"]) for row in levels} == {(d, level) for d in DIMENSIONS for level in ("L1", "L2", "L3", "L4")}, LEVELS.name)
    scope_text = REPORT.read_text(encoding="utf-8") if REPORT.is_file() else ""
    check("SCORE35-SENS-QA-10", "报告明确用户声明、E1与非跨届边界", "用户声明" in scope_text and "E1" in scope_text and "跨届" in scope_text and "学生成绩" in scope_text, REPORT.name)
    check("SCORE35-SENS-QA-11", "报告明确等权为主分析、加权仅敏感性材料", "等权结果仍是全样本主分析的唯一口径" in scope_text, REPORT.name)

    with OUTPUT.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(("check_id", "check_item", "status", "source"))
        for row in checks:
            writer.writerow((row[0], row[1], "通过" if row[2] else "不通过", row[3]))
    failures = [check_id for check_id, _, passed, _ in checks if not passed]
    QA_REPORT.write_text(
        "# 第35届分值加权敏感性分析QA\n\n"
        f"检查结果：{len(checks) - len(failures)}/{len(checks)}通过。\n\n"
        "本QA只验证第35届受限分析的行数、映射、权重、比例和文字边界。"
        "它不验证评分标准发布者、人工编码过程或任何学生/教学事实，也不支持跨届或推断性结论。\n",
        encoding="utf-8",
    )
    if failures:
        raise SystemExit("第35届分值加权敏感性QA未通过：" + ", ".join(failures))
    print(f"第35届分值加权敏感性QA：{len(checks)}/{len(checks)}通过")


if __name__ == "__main__":
    main()
