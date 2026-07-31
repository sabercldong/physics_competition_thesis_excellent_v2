#!/usr/bin/env python3
"""Rebuild the CPHO35 score-weight sensitivity analysis from the V3 dataset."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
V3_CODING = ROOT / "07_analysis/data/第35至42届科学思维V3唯一编码表.csv"
RUBRIC = ROOT / "03_corpus/cpho35_score_rubric_v1.csv"
OUT_DIR = ROOT / "07_analysis/results/v3_final/敏感性分析"
DIMENSIONS = ["模型建构", "科学推理", "科学论证", "质疑创新"]
LEVELS = ["L1", "L2", "L3", "L4"]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
            extrasaction="ignore",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    coding = [
        row for row in read_csv(V3_CODING) if row["competition_no"] == "35"
    ]
    rubric = read_csv(RUBRIC)
    weights = {row["item_id"]: int(row["subquestion_score"]) for row in rubric}
    item_ids = {row["item_id"] for row in coding}

    if len(coding) != 104 or len(item_ids) != 26:
        raise ValueError(
            f"Expected 104 records and 26 items, found {len(coding)} and {len(item_ids)}"
        )
    if item_ids != set(weights):
        missing_in_rubric = sorted(item_ids - set(weights))
        missing_in_coding = sorted(set(weights) - item_ids)
        raise ValueError(
            f"Item mismatch; missing in rubric={missing_in_rubric}, "
            f"missing in V3={missing_in_coding}"
        )
    if sum(weights.values()) != 320:
        raise ValueError("The CPHO35 rubric weights must total 320 points")
    if any(row["present"] not in {"0", "1"} for row in coding):
        raise ValueError("V3 present values must be 0 or 1")

    source_coding_sha = hashlib.sha256(V3_CODING.read_bytes()).hexdigest()
    source_rubric_sha = hashlib.sha256(RUBRIC.read_bytes()).hexdigest()
    common = {
        "数据版本": "V3唯一编码表",
        "编码表SHA256": source_coding_sha,
        "第35届评分台账SHA256": source_rubric_sha,
    }

    item_rows: list[dict] = []
    for row in sorted(
        coding,
        key=lambda value: (
            value["item_id"],
            DIMENSIONS.index(value["dimension"]),
        ),
    ):
        item_rows.append(
            {
                "分析单元编号": row["item_id"],
                "维度": row["dimension"],
                "是否出现": row["present_label"],
                "等级": row["level"],
                "小问分值": weights[row["item_id"]],
                **common,
            }
        )

    presence_rows: list[dict] = []
    level_rows: list[dict] = []
    for dimension in DIMENSIONS:
        rows = [row for row in coding if row["dimension"] == dimension]
        equal_present = sum(row["present"] == "1" for row in rows)
        weighted_present = sum(
            weights[row["item_id"]]
            for row in rows
            if row["present"] == "1"
        )
        equal_proportion = equal_present / 26
        weighted_proportion = weighted_present / 320
        presence_rows.append(
            {
                "维度": dimension,
                "等权出现单元数": equal_present,
                "小问总数": 26,
                "等权出现比例_百分数": f"{100 * equal_proportion:.4f}",
                "分值加权出现分值": weighted_present,
                "总分值": 320,
                "分值加权出现比例_百分数": f"{100 * weighted_proportion:.4f}",
                "分值加权减等权_百分点": f"{100 * (weighted_proportion - equal_proportion):.4f}",
                **common,
            }
        )
        for level in LEVELS:
            equal_count = sum(
                row["present"] == "1" and row["level"] == level for row in rows
            )
            weighted_count = sum(
                weights[row["item_id"]]
                for row in rows
                if row["present"] == "1" and row["level"] == level
            )
            level_rows.append(
                {
                    "维度": dimension,
                    "等级": level,
                    "等权单元数": equal_count,
                    "等权等级构成_百分数": f"{100 * equal_count / equal_present:.4f}"
                    if equal_present
                    else "",
                    "分值加权分值": weighted_count,
                    "分值加权等级构成_百分数": f"{100 * weighted_count / weighted_present:.4f}"
                    if weighted_present
                    else "",
                    **common,
                }
            )

    expected_presence = {
        "模型建构": (25, 315),
        "科学推理": (26, 320),
        "科学论证": (3, 31),
        "质疑创新": (1, 8),
    }
    for row in presence_rows:
        expected = expected_presence[row["维度"]]
        observed = (row["等权出现单元数"], row["分值加权出现分值"])
        if observed != expected:
            raise ValueError(
                f"V3 CPHO35 sensitivity mismatch for {row['维度']}: "
                f"{observed} vs {expected}"
            )

    write_csv(
        OUT_DIR / "第35届V3分值加权逐单元记录.csv",
        [
            "分析单元编号",
            "维度",
            "是否出现",
            "等级",
            "小问分值",
            "数据版本",
            "编码表SHA256",
            "第35届评分台账SHA256",
        ],
        item_rows,
    )
    write_csv(
        OUT_DIR / "第35届V3等权与分值加权出现比例.csv",
        [
            "维度",
            "等权出现单元数",
            "小问总数",
            "等权出现比例_百分数",
            "分值加权出现分值",
            "总分值",
            "分值加权出现比例_百分数",
            "分值加权减等权_百分点",
            "数据版本",
            "编码表SHA256",
            "第35届评分台账SHA256",
        ],
        presence_rows,
    )
    write_csv(
        OUT_DIR / "第35届V3等权与分值加权等级构成.csv",
        [
            "维度",
            "等级",
            "等权单元数",
            "等权等级构成_百分数",
            "分值加权分值",
            "分值加权等级构成_百分数",
            "数据版本",
            "编码表SHA256",
            "第35届评分台账SHA256",
        ],
        level_rows,
    )

    report_lines = [
        "# 第35届V3分值权重敏感性说明",
        "",
        "本表以V3唯一编码表中的第35届26个分析单元和评分台账中的320分为同一批数据，比较小问等权与分值加权结果。旧版基于早期编码生成的第35届敏感性表不再用于论文或结论。",
        "",
        "| 维度 | 等权出现比例 | 分值加权出现比例 | 差值 |",
        "|---|---:|---:|---:|",
    ]
    for row in presence_rows:
        report_lines.append(
            f"| {row['维度']} | {float(row['等权出现比例_百分数']):.2f}% | "
            f"{float(row['分值加权出现比例_百分数']):.2f}% | "
            f"{float(row['分值加权减等权_百分点']):+.2f}个百分点 |"
        )
    report_lines.extend(
        [
            "",
            "四个维度的最大绝对变化为2.28个百分点。第35届内部的分值权重没有改变科学推理、模型建构、科学论证、质疑创新的相对排序。",
            "",
            "该结果仅用于确认第35届内部的权重敏感性。全样本仍采用分析单元等权口径，正文不把第35届单独写成全样本规律。",
            "",
        ]
    )
    (OUT_DIR / "第35届V3分值权重敏感性说明.md").write_text(
        "\n".join(report_lines),
        encoding="utf-8",
    )

    print("PASS: CPHO35 V3 score-weight sensitivity outputs built")
    for row in presence_rows:
        print(
            f"{row['维度']}: equal={float(row['等权出现比例_百分数']):.4f}% "
            f"score_weighted={float(row['分值加权出现比例_百分数']):.4f}% "
            f"delta={float(row['分值加权减等权_百分点']):+.4f}pp"
        )


if __name__ == "__main__":
    main()
