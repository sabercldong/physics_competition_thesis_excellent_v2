#!/usr/bin/env python3
"""Generate a restricted CPHO35 equal-weight versus score-weight sensitivity analysis."""

from __future__ import annotations

import csv
import hashlib
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FINAL_CODING = ROOT / "07_analysis/data/final_coding.csv"
RUBRIC = ROOT / "03_corpus/cpho35_score_rubric_v1.csv"
OUT_DIR = ROOT / "07_analysis/results/reviewed"
DIMENSIONS = ["模型建构", "科学推理", "科学论证", "质疑创新"]
LEVELS = ["L1", "L2", "L3", "L4"]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    coding = [row for row in read_csv(FINAL_CODING) if row["competition_no"] == "35"]
    rubric = read_csv(RUBRIC)
    weights = {row["item_id"]: int(row["subquestion_score"]) for row in rubric}
    expected_records = len(weights) * len(DIMENSIONS)
    if len(weights) != 26 or len(coding) != expected_records:
        raise ValueError(f"需要26个第35届小问及{expected_records}条编码，实际为{len(weights)}和{len(coding)}")
    if {row["item_id"] for row in coding} != set(weights):
        raise ValueError("第35届编码与评分台账的小问集合不一致")
    if any(row["dimension"] not in DIMENSIONS for row in coding):
        raise ValueError("编码中存在未知维度")
    if any(row["present"] not in {"0", "1"} for row in coding):
        raise ValueError("编码的present字段必须为0或1")

    final_sha = hashlib.sha256(FINAL_CODING.read_bytes()).hexdigest()
    rubric_sha = hashlib.sha256(RUBRIC.read_bytes()).hexdigest()
    total_items = len(weights)
    total_score = sum(weights.values())
    common = {
        "scope": "仅第35届；E1用户提供评分标准副本；非跨届统计",
        "source_final_coding_sha256": final_sha,
        "source_score_rubric_sha256": rubric_sha,
    }

    item_rows: list[dict[str, object]] = []
    for row in sorted(coding, key=lambda value: (value["item_id"], DIMENSIONS.index(value["dimension"]))):
        item_rows.append({
            "item_id": row["item_id"],
            "dimension": row["dimension"],
            "present": row["present"],
            "level": row["level"],
            "subquestion_score": weights[row["item_id"]],
            **common,
        })

    presence_rows: list[dict[str, object]] = []
    level_rows: list[dict[str, object]] = []
    for dimension in DIMENSIONS:
        rows = [row for row in coding if row["dimension"] == dimension]
        equal_present = sum(row["present"] == "1" for row in rows)
        weighted_present = sum(weights[row["item_id"]] for row in rows if row["present"] == "1")
        equal_prop = equal_present / total_items
        weighted_prop = weighted_present / total_score
        presence_rows.append({
            "dimension": dimension,
            "equal_weight_items_present": equal_present,
            "total_items": total_items,
            "equal_weight_proportion": round(equal_prop, 6),
            "score_weighted_points_present": weighted_present,
            "total_score_points": total_score,
            "score_weighted_proportion": round(weighted_prop, 6),
            "weighted_minus_equal_percentage_points": round((weighted_prop - equal_prop) * 100, 3),
            **common,
        })
        for level in LEVELS:
            equal_count = sum(row["present"] == "1" and row["level"] == level for row in rows)
            weighted_count = sum(weights[row["item_id"]] for row in rows if row["present"] == "1" and row["level"] == level)
            level_rows.append({
                "dimension": dimension,
                "level": level,
                "equal_weight_items": equal_count,
                "equal_weight_proportion_among_present": round(equal_count / equal_present, 6) if equal_present else "",
                "score_weighted_points": weighted_count,
                "score_weighted_proportion_among_present": round(weighted_count / weighted_present, 6) if weighted_present else "",
                **common,
            })

    outputs = {
        "cpho35_score_weighted_item_records_v1.csv": (
            ["item_id", "dimension", "present", "level", "subquestion_score", "scope", "source_final_coding_sha256", "source_score_rubric_sha256"],
            item_rows,
        ),
        "cpho35_score_weighted_presence_sensitivity_v1.csv": (
            ["dimension", "equal_weight_items_present", "total_items", "equal_weight_proportion", "score_weighted_points_present", "total_score_points", "score_weighted_proportion", "weighted_minus_equal_percentage_points", "scope", "source_final_coding_sha256", "source_score_rubric_sha256"],
            presence_rows,
        ),
        "cpho35_score_weighted_level_sensitivity_v1.csv": (
            ["dimension", "level", "equal_weight_items", "equal_weight_proportion_among_present", "score_weighted_points", "score_weighted_proportion_among_present", "scope", "source_final_coding_sha256", "source_score_rubric_sha256"],
            level_rows,
        ),
    }
    for name, (fieldnames, rows) in outputs.items():
        write_csv(OUT_DIR / name, fieldnames, rows)

    report = OUT_DIR / "cpho35_score_weighted_sensitivity_report_v1.md"
    report.write_text(
        "# 第35届分值加权敏感性分析\n\n"
        f"分析对象：第35届26个独立小问、{len(coding)}条裁决后维度编码；小问分值总计{total_score}分。\n\n"
        "## 目的\n\n"
        "本分析将同一批第35届小问的等权描述比例与按评分标准分值加权的描述比例并列，检查结论是否对权重口径敏感。它不是跨届比较、显著性检验或题目质量评价。\n\n"
        "## 解释边界\n\n"
        "用户声明该第35届答案/评分标准为官方副本。评分标准仍按E1登记：该声明已记录，但发布者、授权及官方版本链未由项目独立核验。"
        "因此，输出只能描述该副本所对应的第35届任务要求编码，不能推断学生成绩、能力、命题质量、教学效果或其他届次的分值结构。"
        "等权结果仍是全样本主分析的唯一口径；加权结果仅作本届敏感性材料。\n\n"
        "## 输出\n\n"
        + "\n".join(f"- `{name}`" for name in outputs)
        + "\n",
        encoding="utf-8",
    )
    print(f"第35届分值加权敏感性分析已生成：{len(item_rows)}条记录，{total_score}分")


if __name__ == "__main__":
    main()
