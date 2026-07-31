#!/usr/bin/env python3
"""Build the full V3 analysis-unit to manuscript-case selection matrix."""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "07_analysis/data/第35至42届科学思维V3唯一编码表.csv"
OUTPUT_DIR = ROOT / "07_analysis/results/v3_final/案例选择"
DIMENSIONS = ["模型建构", "科学推理", "科学论证", "质疑创新"]

SELECTIONS = {
    "CPHO41-Q06-3": ("主案例一", "条件—关系链；模型与推理L3"),
    "CPHO41-Q07-4": ("主案例二", "状态分类—比较；科学论证正例"),
    "CPHO42-Q04-2": ("主案例三", "近似条件建模；模型与推理L3"),
    "CPHO37-Q06-3": ("主案例四", "同对象比较；模型与推理L3"),
    "CPHO40-Q03-1_i": ("主案例五（组内）", "多对象约束；模型与推理L3"),
    "CPHO40-Q03-1_ii": (
        "主案例五（组内对照）",
        "同一原始小问内模型未出现、推理L1",
    ),
    "CPHO40-Q03-1_iii": ("主案例五（组内）", "同一原始小问内模型与推理L2"),
    "CPHO40-Q03-1_iv": ("主案例五（组内）", "同一原始小问内模型与推理L2"),
    "CPHO40-Q03-1_v": ("主案例五（组内）", "同一原始小问内模型L1、推理L2"),
    "CPHO40-Q07-3": ("主案例六", "阈值判断；科学论证正例"),
    "CPHO35-Q08-3": (
        "相邻小问对照A",
        "需要说明共振不发生；论证出现、质疑创新未出现",
    ),
    "CPHO35-Q08-4": (
        "相邻小问对照B",
        "设计频移测量原理；质疑创新正例",
    ),
}


def read_rows() -> list[dict[str, str]]:
    with INPUT.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 884:
        raise ValueError(f"Expected 884 records, found {len(rows)}")
    return rows


def write_csv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def boundary_tags(codes: dict[str, tuple[str, str]]) -> str:
    tags: list[str] = []
    if codes["质疑创新"][0] == "是":
        tags.append("质疑创新正例")
    if codes["科学论证"][0] == "是":
        tags.append("科学论证正例")
    if codes["模型建构"][0] == "否":
        tags.append("模型建构未出现")
    if codes["科学推理"][1] == "L1":
        tags.append("科学推理L1")
    if (
        codes["模型建构"][1] == "L3"
        and codes["科学推理"][1] == "L3"
    ):
        tags.append("模型—推理高整合")
    if not tags:
        tags.append("常规维度组合")
    return "；".join(tags)


def main() -> None:
    rows = read_rows()
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row["item_id"]].append(row)
    if len(grouped) != 221:
        raise ValueError(f"Expected 221 analysis units, found {len(grouped)}")

    output: list[dict] = []
    for item_id, item_rows in sorted(grouped.items()):
        first = item_rows[0]
        codes = {
            row["dimension"]: (row["present_label"], row["level"])
            for row in item_rows
        }
        if set(codes) != set(DIMENSIONS):
            raise ValueError(f"Missing dimension in {item_id}")
        selection_role, selection_reason = SELECTIONS.get(
            item_id,
            ("未入选正文", "保留于全样本统计，不承担正文案例解释"),
        )
        output.append(
            {
                "分析单元编号": item_id,
                "届次": first["competition_no"],
                "年份": first["year"],
                "题号": first["question_no"],
                "小问号": first["subquestion_no"],
                "任务输出": first["required_output"],
                "模型建构": (
                    codes["模型建构"][1]
                    if codes["模型建构"][0] == "是"
                    else "未出现"
                ),
                "科学推理": (
                    codes["科学推理"][1]
                    if codes["科学推理"][0] == "是"
                    else "未出现"
                ),
                "科学论证": (
                    codes["科学论证"][1]
                    if codes["科学论证"][0] == "是"
                    else "未出现"
                ),
                "质疑创新": (
                    codes["质疑创新"][1]
                    if codes["质疑创新"][0] == "是"
                    else "未出现"
                ),
                "边界类型": boundary_tags(codes),
                "是否入选正文": "是" if item_id in SELECTIONS else "否",
                "正文角色": selection_role,
                "选择或未选说明": selection_reason,
                "题目文本路径": first["item_text_path"],
            }
        )

    selected = [row for row in output if row["是否入选正文"] == "是"]
    if len(selected) != 12:
        raise ValueError(f"Expected 12 selected units, found {len(selected)}")
    if not any(row["质疑创新"] != "未出现" for row in selected):
        raise ValueError("Selected cases must include an innovation-positive unit")
    if not any(row["模型建构"] == "未出现" for row in selected):
        raise ValueError("Selected cases must include a model-absent contrast")
    if not any(row["科学推理"] == "L1" for row in selected):
        raise ValueError("Selected cases must include a reasoning-L1 contrast")

    write_csv(
        OUTPUT_DIR / "221个分析单元案例选择矩阵_V3.csv",
        [
            "分析单元编号",
            "届次",
            "年份",
            "题号",
            "小问号",
            "任务输出",
            "模型建构",
            "科学推理",
            "科学论证",
            "质疑创新",
            "边界类型",
            "是否入选正文",
            "正文角色",
            "选择或未选说明",
            "题目文本路径",
        ],
        output,
    )

    summary = [
        "# V3案例选择矩阵说明",
        "",
        "- 全样本：221个分析单元。",
        "- 正文主案例：6组，涉及10个分析单元。",
        "- 相邻小问对照：1组，涉及2个分析单元。",
        "- 覆盖：模型—推理L3、科学论证正例、质疑创新正例、模型建构未出现、科学推理L1。",
        "- 案例用于解释任务机制，不按入选案例频数推断全样本分布。",
        "",
        "输出：`221个分析单元案例选择矩阵_V3.csv`。",
        "",
    ]
    (OUTPUT_DIR / "V3案例选择矩阵说明.md").write_text(
        "\n".join(summary),
        encoding="utf-8",
    )
    print(
        "PASS: V3 case-selection matrix built "
        f"(all_units={len(output)}, selected_units={len(selected)})"
    )


if __name__ == "__main__":
    main()
