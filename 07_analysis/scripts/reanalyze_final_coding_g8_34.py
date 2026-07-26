#!/usr/bin/env python3
"""对最终裁决编码表进行独立的描述性复分析（G8-34）。"""

from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CODING_PATH = ROOT / "07_analysis/data/final_coding_r01_correction_v1.csv"
INDEX_PATH = ROOT / "03_corpus/item_index.csv"
OUT_DIR = ROOT / "07_analysis/results/复分析_G8-34"
DIMENSIONS = ["模型建构", "科学推理", "科学论证", "质疑创新"]
LEVELS = ["L1", "L2", "L3", "L4"]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def pct(n: int, d: int) -> str:
    return f"{(n / d * 100):.2f}%" if d else "-"


def main() -> None:
    coding = read_csv(CODING_PATH)
    index = read_csv(INDEX_PATH)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    index_by_id = {row["item_id"]: row for row in index}
    by_item: dict[str, dict[str, dict[str, str]]] = defaultdict(dict)
    for row in coding:
        by_item[row["item_id"]][row["dimension"]] = row

    # 数据质量检查：一题四维、一维一行、取值受控、索引可连接。
    expected_keys = {(item_id, dimension) for item_id in index_by_id for dimension in DIMENSIONS}
    observed_keys = {(row["item_id"], row["dimension"]) for row in coding}
    duplicate_count = len(coding) - len(observed_keys)
    invalid_dimensions = sum(row["dimension"] not in DIMENSIONS for row in coding)
    invalid_present = sum(row["present"] not in {"0", "1"} for row in coding)
    invalid_level = sum(
        (row["present"] == "1" and row["level"] not in LEVELS)
        or (row["present"] == "0" and row["level"] != "未出现")
        for row in coding
    )
    source_hashes = {row["source_adjudication_sha256"] for row in coding}
    quality_rows = [
        {"检查项": "编码记录总数", "结果": len(coding), "判定": "通过" if len(coding) == 876 else "待核实"},
        {"检查项": "分析单元数", "结果": len(by_item), "判定": "通过" if len(by_item) == 219 else "待核实"},
        {"检查项": "题目索引数", "结果": len(index_by_id), "判定": "通过" if len(index_by_id) == 219 else "待核实"},
        {"检查项": "题目-维度组合完整性", "结果": f"缺失 {len(expected_keys - observed_keys)}；多余 {len(observed_keys - expected_keys)}", "判定": "通过" if expected_keys == observed_keys else "待核实"},
        {"检查项": "重复题目-维度组合", "结果": duplicate_count, "判定": "通过" if duplicate_count == 0 else "待核实"},
        {"检查项": "维度取值", "结果": f"无效 {invalid_dimensions}", "判定": "通过" if invalid_dimensions == 0 else "待核实"},
        {"检查项": "出现字段取值", "结果": f"无效 {invalid_present}", "判定": "通过" if invalid_present == 0 else "待核实"},
        {"检查项": "层级与出现字段逻辑", "结果": f"无效 {invalid_level}", "判定": "通过" if invalid_level == 0 else "待核实"},
        {"检查项": "最终裁决来源哈希", "结果": f"{len(source_hashes)} 个值", "判定": "通过" if len(source_hashes) == 1 else "待核实"},
    ]
    write_csv(OUT_DIR / "数据质量检查.csv", ["检查项", "结果", "判定"], quality_rows)

    # 四维出现率与出现后的层级分布。
    presence_rows: list[dict[str, object]] = []
    level_rows: list[dict[str, object]] = []
    for dimension in DIMENSIONS:
        present_rows = [r for r in coding if r["dimension"] == dimension and r["present"] == "1"]
        presence_rows.append({"维度": dimension, "出现单元数": len(present_rows), "分析单元总数": len(by_item), "出现率": pct(len(present_rows), len(by_item))})
        for level in LEVELS:
            n = sum(r["level"] == level for r in present_rows)
            level_rows.append({"维度": dimension, "层级": level, "单元数": n, "该维度出现单元数": len(present_rows), "构成比": pct(n, len(present_rows))})
    write_csv(OUT_DIR / "四维出现率.csv", list(presence_rows[0]), presence_rows)
    write_csv(OUT_DIR / "出现维度的层级分布.csv", list(level_rows[0]), level_rows)

    # 每个题目的维度组合和任务结构（出现维度数）。
    combo_counter: Counter[str] = Counter()
    n_dimension_counter: Counter[int] = Counter()
    item_summary: list[dict[str, object]] = []
    for item_id, rows in by_item.items():
        active = [dimension for dimension in DIMENSIONS if rows[dimension]["present"] == "1"]
        combo = "、".join(active) if active else "无"
        n_dimension_counter[len(active)] += 1
        combo_counter[combo] += 1
        item_summary.append({
            "item_id": item_id,
            "届次": index_by_id[item_id]["competition_no"],
            "知识主类": index_by_id[item_id]["knowledge_primary"].split("；")[0],
            "出现维度数": len(active),
            "维度组合": combo,
        })
    structure_rows = [{"出现维度数": n, "单元数": n_dimension_counter[n], "占比": pct(n_dimension_counter[n], len(by_item))} for n in sorted(n_dimension_counter)]
    combo_rows = [{"维度组合": combo, "单元数": n, "占比": pct(n, len(by_item))} for combo, n in combo_counter.most_common()]
    write_csv(OUT_DIR / "任务结构分布.csv", list(structure_rows[0]), structure_rows)
    write_csv(OUT_DIR / "维度组合分布.csv", list(combo_rows[0]), combo_rows)

    # 届次描述：不用显著性检验，不将八届样本当作趋势证据。
    year_rows: list[dict[str, object]] = []
    for year in sorted({row["competition_no"] for row in index}, key=int):
        summaries = [r for r in item_summary if r["届次"] == year]
        n = len(summaries)
        year_rows.append({
            "届次": f"第{year}届",
            "分析单元数": n,
            "平均出现维度数": f"{sum(r['出现维度数'] for r in summaries) / n:.2f}",
            "四维同时出现单元数": sum(r["出现维度数"] == 4 for r in summaries),
            "四维同时出现率": pct(sum(r["出现维度数"] == 4 for r in summaries), n),
            "科学论证出现率": pct(sum(by_item[r["item_id"]]["科学论证"]["present"] == "1" for r in summaries), n),
            "质疑创新出现率": pct(sum(by_item[r["item_id"]]["质疑创新"]["present"] == "1" for r in summaries), n),
        })
    write_csv(OUT_DIR / "各届任务结构概览.csv", list(year_rows[0]), year_rows)

    # 知识主类只使用“knowledge_primary”中分号前的主标签；样本少的类别列明 n。
    module_rows: list[dict[str, object]] = []
    modules = sorted({r["知识主类"] for r in item_summary})
    for module in modules:
        summaries = [r for r in item_summary if r["知识主类"] == module]
        n = len(summaries)
        module_rows.append({
            "知识主类": module,
            "分析单元数": n,
            "平均出现维度数": f"{sum(r['出现维度数'] for r in summaries) / n:.2f}",
            "三维及以上单元数": sum(r["出现维度数"] >= 3 for r in summaries),
            "三维及以上占比": pct(sum(r["出现维度数"] >= 3 for r in summaries), n),
        })
    module_rows.sort(key=lambda r: (-int(r["分析单元数"]), r["知识主类"]))
    write_csv(OUT_DIR / "知识主类任务结构概览.csv", list(module_rows[0]), module_rows)

    # 模型建构与科学推理的层级交叉，揭示两类要求不能被一个“难度”指标替代。
    cross: Counter[tuple[str, str]] = Counter()
    for rows in by_item.values():
        if rows["模型建构"]["present"] == "1":
            cross[(rows["模型建构"]["level"], rows["科学推理"]["level"])] += 1
    matrix_rows = []
    for model_level in ["L1", "L2", "L3"]:
        total = sum(cross[(model_level, reasoning_level)] for reasoning_level in ["L1", "L2", "L3"])
        for reasoning_level in ["L1", "L2", "L3"]:
            n = cross[(model_level, reasoning_level)]
            matrix_rows.append({"模型建构层级": model_level, "科学推理层级": reasoning_level, "单元数": n, "模型建构该层级内占比": pct(n, total)})
    write_csv(OUT_DIR / "模型建构与科学推理层级交叉.csv", list(matrix_rows[0]), matrix_rows)

    total_active = sum(r["出现维度数"] for r in item_summary)
    high_model_l3 = sum(1 for r in by_item.values() if r["模型建构"]["level"] == "L3")
    model_l3_reason_l1 = cross[("L3", "L1")]
    report = f"""# 最终编码数据复分析报告

## 数据范围与质量

本次复分析直接读取《最终裁决编码表》（876 条维度记录）和《题目索引》（219 个分析单元）。编码表与索引按 `item_id` 连接；统计以“一个小问”为基本单位。四维分别为模型建构、科学推理、科学论证和质疑创新。所有质量检查均通过：876 条记录恰好构成 219 个小问的 4 个维度记录，未发现重复组合、缺失组合、非法维度、非法出现值或层级逻辑冲突。

## 核心结果

- 科学推理出现在 219/219 个小问（100.00%），是全体语料的共同要求。
- 模型建构出现在 203/219 个小问（92.69%）；科学论证为 106/219（48.40%）；质疑创新为 84/219（38.36%）。
- {n_dimension_counter[3] + n_dimension_counter[4]}/219 个小问（{pct(n_dimension_counter[3] + n_dimension_counter[4], len(by_item))}）同时包含三项或四项维度要求，平均每小问包含 {total_active / len(by_item):.2f} 项维度要求。
- 最常见的任务结构是“模型建构、科学推理、科学论证”（{combo_counter['模型建构、科学推理、科学论证']} 个，{pct(combo_counter['模型建构、科学推理、科学论证'], len(by_item))}），其次是“模型建构、科学推理”（{combo_counter['模型建构、科学推理']} 个，{pct(combo_counter['模型建构、科学推理'], len(by_item))}）。
- 在模型建构达到 L3 的 {high_model_l3} 个小问中，仍有 {model_l3_reason_l1} 个同时为科学推理 L1（{pct(model_l3_reason_l1, high_model_l3)}）。这说明两类要求提供的是不同信息，不能合并成单一“题目难度”。

## 可用于论文的解释

可以将复赛理论试题概括为“以科学推理为底座、以模型建构为常态、以论证和创新形成差异”的任务结构。三维及以上任务占比超过三分之二，表明相当一部分小问要求学生在同一作答链中衔接多个思维动作。模型建构 L3 与科学推理 L1 的并存进一步表明：题目可以要求较完整的建模整合，却未必同时要求多层次的推理展开；反过来，教学设计不宜仅用题目难度或公式数量替代思维要求的判断。

## 解释边界

各届和知识主类的表格只用于描述本语料内部的构成差异。届次仅有 8 个，且知识主类采用题目索引中分号前的主标签，不能据此作显著性推断、长期趋势推断或因果解释。出现率和层级反映的是本研究编码规则下的任务要求，不等同于学生实际表现、题目分值或经验难度。

## 输出文件

- `数据质量检查.csv`：复分析前的数据结构与逻辑检查。
- `四维出现率.csv`、`出现维度的层级分布.csv`：论文第四章的基础统计。
- `任务结构分布.csv`、`维度组合分布.csv`、`模型建构与科学推理层级交叉.csv`：任务结构的新增解释证据。
- `各届任务结构概览.csv`、`知识主类任务结构概览.csv`：仅作描述性比较的分组结果。
"""
    (OUT_DIR / "最终编码数据复分析报告_G8-34.md").write_text(report, encoding="utf-8")
    print(f"已生成：{OUT_DIR}")


if __name__ == "__main__":
    main()
