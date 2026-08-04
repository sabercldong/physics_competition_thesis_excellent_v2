#!/usr/bin/env python3
"""Compute pairwise and three-rater agreement for V3, RATER-F, and RATER-G."""

from __future__ import annotations

import argparse
import csv
import hashlib
import math
import random
from collections import Counter, defaultdict
from pathlib import Path

from compute_v3_anonymous_blind_agreement import (
    COMBINED_LABELS,
    DIMENSIONS,
    LEVEL_LABELS,
    PRESENCE_LABELS,
    enrich_metric_row,
    metric_fields,
)


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_F = ROOT / (
    "07_analysis/data/v3_independent_validation/incoming/RATER-F/"
    "第35至42届第三版匿名盲评编码表_RATER-F_300行.csv"
)
DEFAULT_G = ROOT / (
    "07_analysis/data/v3_independent_validation/incoming/RATER-G/"
    "第35至42届第三版匿名盲评编码表_RATER-G_300行.csv"
)
DEFAULT_KEY = ROOT / (
    "07_analysis/data/v3_independent_validation/author_only/"
    "独立盲评抽样与V3对照密钥_不得交评分者.csv"
)
DEFAULT_FINAL = ROOT / "07_analysis/data/第35至42届科学思维第三版唯一编码表.csv"
DEFAULT_OUTPUT = ROOT / "07_analysis/results/第三版与RATER-F-G三方一致性"
BOOTSTRAP_SEED = 20260803
BOOTSTRAP_ITERATIONS = 2000


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fmt(value: float | None) -> str:
    if value is None or not math.isfinite(value):
        return ""
    return f"{value:.6f}"


def percentile(values: list[float], probability: float) -> float | None:
    clean = sorted(value for value in values if math.isfinite(value))
    if not clean:
        return None
    position = (len(clean) - 1) * probability
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return clean[lower]
    fraction = position - lower
    return clean[lower] * (1 - fraction) + clean[upper] * fraction


def fleiss_kappa(label_sets: list[list[str]], categories: list[str]) -> float | None:
    if not label_sets:
        return None
    rater_count = len(label_sets[0])
    if rater_count < 2 or any(len(labels) != rater_count for labels in label_sets):
        raise ValueError("Fleiss kappa要求每条记录具有相同且不少于2名评分者")
    item_agreements: list[float] = []
    totals = Counter()
    for labels in label_sets:
        if any(label not in categories for label in labels):
            raise ValueError(f"发现非法标签：{labels}")
        counts = Counter(labels)
        totals.update(labels)
        item_agreements.append(
            (sum(count * count for count in counts.values()) - rater_count)
            / (rater_count * (rater_count - 1))
        )
    observed = sum(item_agreements) / len(item_agreements)
    total_ratings = len(label_sets) * rater_count
    expected = sum((totals[label] / total_ratings) ** 2 for label in categories)
    if math.isclose(1.0 - expected, 0.0):
        return None
    return (observed - expected) / (1.0 - expected)


def all_equal_rate(label_sets: list[list[str]]) -> float | None:
    if not label_sets:
        return None
    return sum(len(set(labels)) == 1 for labels in label_sets) / len(label_sets)


def mean_pairwise_agreement(label_sets: list[list[str]]) -> float | None:
    if not label_sets:
        return None
    agreed = 0
    compared = 0
    for labels in label_sets:
        for left in range(len(labels)):
            for right in range(left + 1, len(labels)):
                agreed += labels[left] == labels[right]
                compared += 1
    return agreed / compared if compared else None


def validate_inputs(
    f_rows: list[dict[str, str]],
    g_rows: list[dict[str, str]],
    key_rows: list[dict[str, str]],
    final_rows: list[dict[str, str]],
) -> tuple[list[dict[str, str]], list[dict[str, object]]]:
    checks: list[dict[str, object]] = []

    def add(name: str, passed: bool, detail: str) -> None:
        checks.append({"检查项": name, "结果": "通过" if passed else "失败", "说明": detail})
        if not passed:
            raise ValueError(f"{name}: {detail}")

    for label, rows, reviewer_id in [
        ("RATER-F", f_rows, "RATER-F"),
        ("RATER-G", g_rows, "RATER-G"),
    ]:
        ids = [row["blind_row_id"].strip() for row in rows]
        add(f"{label}行数", len(rows) == 300, f"实测{len(rows)}行")
        add(f"{label}主键唯一", len(ids) == len(set(ids)), "blind_row_id无重复")
        reviewer_ids = {row["independent_reviewer_id"].strip() for row in rows}
        add(f"{label}代号一致", reviewer_ids == {reviewer_id}, f"实测{reviewer_ids}")
        required = list(rows[0])[10:]
        blanks = sum(not row[field].strip() for row in rows for field in required)
        add(f"{label}后10列完整", blanks == 0, f"空白单元格{blanks}个")

    f_by_id = {row["blind_row_id"].strip(): row for row in f_rows}
    g_by_id = {row["blind_row_id"].strip(): row for row in g_rows}
    key_by_id = {row["blind_row_id"].strip(): row for row in key_rows}
    add("对照密钥行数与主键", len(key_rows) == 300 == len(key_by_id), "300个主键唯一")
    add(
        "三份文件主键集合一致",
        set(f_by_id) == set(g_by_id) == set(key_by_id),
        "300个blind_row_id完全配对",
    )

    final_by_id = {row["review_row_id"].strip(): row for row in final_rows}
    final_mismatches = 0
    fixed_mismatches = 0
    invalid_labels = 0
    merged: list[dict[str, str]] = []
    for f_row in f_rows:
        blind_id = f_row["blind_row_id"].strip()
        g_row = g_by_id[blind_id]
        key_row = key_by_id[blind_id]
        source = final_by_id.get(key_row["source_review_row_id"].strip())
        if source is None or any(
            [
                source["item_id"].strip() != key_row["item_id"].strip(),
                source["dimension"].strip() != key_row["dimension"].strip(),
                source["present_label"].strip() != key_row["v3_present_label"].strip(),
                source["level"].strip() != key_row["v3_level"].strip(),
            ]
        ):
            final_mismatches += 1
        fixed_fields = list(f_row)[:10]
        if any(f_row[field].strip() != g_row[field].strip() for field in fixed_fields):
            fixed_mismatches += 1
        for row in (f_row, g_row):
            present = row["review_present"].strip()
            level = row["review_level"].strip()
            if not (
                (present == "否" and level == "未出现")
                or (present == "是" and level in LEVEL_LABELS)
            ):
                invalid_labels += 1
        merged.append(
            {
                "blind_row_id": blind_id,
                "blind_unit_no": f_row["blind_unit_no"].strip(),
                "item_id": f_row["item_id"].strip(),
                "dimension": f_row["dimension"].strip(),
                "selection_stratum": key_row["selection_stratum"].strip(),
                "第三版存在性": key_row["v3_present_label"].strip(),
                "第三版等级": key_row["v3_level"].strip(),
                "RATER-F存在性": f_row["review_present"].strip(),
                "RATER-F等级": f_row["review_level"].strip(),
                "RATER-G存在性": g_row["review_present"].strip(),
                "RATER-G等级": g_row["review_level"].strip(),
            }
        )
    add("RATER-F与RATER-G固定字段一致", fixed_mismatches == 0, f"不一致{fixed_mismatches}行")
    add("密钥标签与第三版唯一表一致", final_mismatches == 0, f"不一致{final_mismatches}行")
    add("两份匿名回填标签合法", invalid_labels == 0, f"非法组合{invalid_labels}行")
    add(
        "75单元四维度齐全",
        len({row["blind_unit_no"] for row in merged}) == 75
        and all(
            {row["dimension"] for row in merged if row["blind_unit_no"] == unit}
            == set(DIMENSIONS)
            for unit in {row["blind_unit_no"] for row in merged}
        ),
        "75个单元，每单元4行",
    )
    return merged, checks


def pairwise_rows(
    rows: list[dict[str, str]], iterations: int, seed: int
) -> list[dict[str, object]]:
    sources = ["第三版", "RATER-F", "RATER-G"]
    output: list[dict[str, object]] = []
    pair_no = 0
    for left_index, left in enumerate(sources):
        for right in sources[left_index + 1 :]:
            pair_no += 1
            transformed = [
                {
                    "blind_unit_no": row["blind_unit_no"],
                    "v3_present_label": row[f"{left}存在性"],
                    "review_present": row[f"{right}存在性"],
                    "v3_level": row[f"{left}等级"],
                    "review_level": row[f"{right}等级"],
                }
                for row in rows
            ]
            result = enrich_metric_row(
                f"{left}—{right}", transformed, iterations, seed + pair_no
            )
            result["编码对"] = result.pop("分析范围")
            output.append(result)
    return output


MULTI_CI_METRICS = [
    "存在性三方完全一致率",
    "存在性平均两两一致率",
    "存在性Fleiss_Kappa",
    "组合标签三方完全一致率",
    "组合标签平均两两一致率",
    "组合标签Fleiss_Kappa",
    "三方均出现时等级完全一致率",
    "三方均出现时等级Fleiss_Kappa",
]


def multi_bundle(rows: list[dict[str, str]]) -> dict[str, int | float | None]:
    presence = [
        [row["第三版存在性"], row["RATER-F存在性"], row["RATER-G存在性"]]
        for row in rows
    ]
    combined = [
        [row["第三版等级"], row["RATER-F等级"], row["RATER-G等级"]]
        for row in rows
    ]
    all_present = [
        labels
        for labels, present in zip(combined, presence)
        if all(label == "是" for label in present)
    ]
    return {
        "行数": len(rows),
        "单元数": len({row["blind_unit_no"] for row in rows}),
        "三方均判出现行数": len(all_present),
        "存在性三方完全一致率": all_equal_rate(presence),
        "存在性平均两两一致率": mean_pairwise_agreement(presence),
        "存在性Fleiss_Kappa": fleiss_kappa(presence, PRESENCE_LABELS),
        "组合标签三方完全一致率": all_equal_rate(combined),
        "组合标签平均两两一致率": mean_pairwise_agreement(combined),
        "组合标签Fleiss_Kappa": fleiss_kappa(combined, COMBINED_LABELS),
        "三方均出现时等级完全一致率": all_equal_rate(all_present),
        "三方均出现时等级Fleiss_Kappa": fleiss_kappa(all_present, LEVEL_LABELS),
    }


def multi_with_ci(
    label: str,
    rows: list[dict[str, str]],
    iterations: int,
    seed: int,
) -> dict[str, object]:
    bundle = multi_bundle(rows)
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        groups[row["blind_unit_no"]].append(row)
    units = sorted(groups)
    rng = random.Random(seed)
    samples: dict[str, list[float]] = {metric: [] for metric in MULTI_CI_METRICS}
    for _ in range(iterations):
        sampled: list[dict[str, str]] = []
        for unit in rng.choices(units, k=len(units)):
            sampled.extend(groups[unit])
        sample_bundle = multi_bundle(sampled)
        for metric in MULTI_CI_METRICS:
            value = sample_bundle[metric]
            if isinstance(value, (int, float)) and math.isfinite(value):
                samples[metric].append(float(value))
    result: dict[str, object] = {"分析范围": label}
    for metric, value in bundle.items():
        result[metric] = value if isinstance(value, int) else fmt(value)
        if metric in MULTI_CI_METRICS:
            result[f"{metric}_95%CI下限"] = fmt(percentile(samples[metric], 0.025))
            result[f"{metric}_95%CI上限"] = fmt(percentile(samples[metric], 0.975))
            result[f"{metric}_有效重复数"] = len(samples[metric])
    return result


def multi_fields() -> list[str]:
    fields = ["分析范围", "行数", "单元数", "三方均判出现行数"]
    for metric in MULTI_CI_METRICS:
        fields.extend(
            [
                metric,
                f"{metric}_95%CI下限",
                f"{metric}_95%CI上限",
                f"{metric}_有效重复数",
            ]
        )
    return fields


def label_detail_rows(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    output: list[dict[str, object]] = []
    for row in rows:
        presence = [row[f"{source}存在性"] for source in ["第三版", "RATER-F", "RATER-G"]]
        combined = [row[f"{source}等级"] for source in ["第三版", "RATER-F", "RATER-G"]]
        output.append(
            {
                **row,
                "存在性三方完全一致": "是" if len(set(presence)) == 1 else "否",
                "组合标签三方完全一致": "是" if len(set(combined)) == 1 else "否",
                "组合标签不同数": len(set(combined)),
            }
        )
    return output


def build_note(
    path: Path,
    pairwise: list[dict[str, object]],
    multi: list[dict[str, object]],
    iterations: int,
) -> None:
    overall = multi[0]
    pair_lines = "\n".join(
        "| {编码对} | {存在性原始一致率} | {存在性Cohen_Kappa} | {存在性Gwet_AC1} | "
        "{组合标签原始一致率} | {组合标签二次加权Kappa} |".format(**row)
        for row in pairwise
    )
    text = f"""# 第三版、RATER-F与RATER-G三方一致性统计说明

## 一、对象与用途

统计对象为同一75个分析单元的300行四维编码。三组标签分别来自第三版唯一编码表、RATER-F匿名回填和RATER-G匿名回填。样本包含59个边界核心单元和16个各届常规补充单元，因此这些系数用于检验编码规则和定位分歧，不直接代表第35至42届全部试题的总体标签分布。

## 二、方法

两两比较报告存在性原始一致率、Cohen's kappa、Gwet's AC1，以及五级组合标签原始一致率和二次加权kappa。三评分者比较报告三方完全一致率、平均两两一致率和Fleiss' kappa；等级Fleiss' kappa仅在三方均判断维度出现的记录上计算。95%区间以75个分析单元为聚类单位进行{iterations}次自助抽样。

## 三、主要结果

| 编码对 | 存在性一致率 | 存在性kappa | 存在性AC1 | 组合标签一致率 | 组合标签加权kappa |
|---|---:|---:|---:|---:|---:|
{pair_lines}

- 三方存在性完全一致率：{overall['存在性三方完全一致率']}；Fleiss' kappa：{overall['存在性Fleiss_Kappa']}。
- 三方组合标签完全一致率：{overall['组合标签三方完全一致率']}；Fleiss' kappa：{overall['组合标签Fleiss_Kappa']}。
- 三方均判出现的记录：{overall['三方均判出现行数']}行；其中等级完全一致率：{overall['三方均出现时等级完全一致率']}；等级Fleiss' kappa：{overall['三方均出现时等级Fleiss_Kappa']}。

## 四、解释限制

Fleiss' kappa把五级组合标签按名义类别处理，不利用等级距离；两两二次加权kappa补充反映相差一级与跨级分歧的差别。维度稀少或标签缺少变异时，kappa可能偏低或不可计算，应同时查看原始一致率、AC1、分维度结果和逐行标签表。任何分歧都需要回到题干、参考解答和编码手册裁决，不能按多数票自动改写第三版标签。

## 五、结果文件

- `三组两两一致性.csv`：第三版—F、第三版—G、F—G三组结果及聚类自助法区间；
- `三评分者一致性.csv`：总体和四维度三方完全一致率、平均两两一致率与Fleiss' kappa；
- `三方逐行标签与分歧.csv`：300行标签配对和三方一致标记；
- `三方一致性统计QA.csv`：输入结构、主键、标签和第三版来源校验；
- `输入文件与校验值.csv`：四份输入文件的SHA-256。
"""
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rater-f", type=Path, default=DEFAULT_F)
    parser.add_argument("--rater-g", type=Path, default=DEFAULT_G)
    parser.add_argument("--key-file", type=Path, default=DEFAULT_KEY)
    parser.add_argument("--final-file", type=Path, default=DEFAULT_FINAL)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--bootstrap-iterations", type=int, default=BOOTSTRAP_ITERATIONS)
    parser.add_argument("--seed", type=int, default=BOOTSTRAP_SEED)
    args = parser.parse_args()

    f_rows = read_csv(args.rater_f)
    g_rows = read_csv(args.rater_g)
    key_rows = read_csv(args.key_file)
    final_rows = read_csv(args.final_file)
    merged, checks = validate_inputs(f_rows, g_rows, key_rows, final_rows)

    pairwise = pairwise_rows(merged, args.bootstrap_iterations, args.seed)
    pair_fields = metric_fields(["编码对"])
    write_csv(args.output_dir / "三组两两一致性.csv", pair_fields, pairwise)

    scopes = [("全部", merged)] + [
        (dimension, [row for row in merged if row["dimension"] == dimension])
        for dimension in DIMENSIONS
    ]
    multi = [
        multi_with_ci(
            scope,
            rows,
            args.bootstrap_iterations,
            args.seed + 100 + index,
        )
        for index, (scope, rows) in enumerate(scopes)
    ]
    write_csv(args.output_dir / "三评分者一致性.csv", multi_fields(), multi)

    detail = label_detail_rows(merged)
    write_csv(
        args.output_dir / "三方逐行标签与分歧.csv",
        list(detail[0]),
        detail,
    )
    write_csv(
        args.output_dir / "三方一致性统计QA.csv",
        ["检查项", "结果", "说明"],
        checks,
    )
    input_rows = []
    for role, path, count in [
        ("RATER-F匿名回填", args.rater_f, len(f_rows)),
        ("RATER-G匿名回填", args.rater_g, len(g_rows)),
        ("第三版对照密钥", args.key_file, len(key_rows)),
        ("第三版唯一编码表", args.final_file, len(final_rows)),
    ]:
        input_rows.append(
            {
                "文件角色": role,
                "项目内相对路径": str(path.resolve().relative_to(ROOT)),
                "数据行数": count,
                "SHA-256": sha256(path),
            }
        )
    write_csv(
        args.output_dir / "输入文件与校验值.csv",
        ["文件角色", "项目内相对路径", "数据行数", "SHA-256"],
        input_rows,
    )
    build_note(
        args.output_dir / "三方一致性统计说明.md",
        pairwise,
        multi,
        args.bootstrap_iterations,
    )

    print(f"输出目录: {args.output_dir}")
    for row in pairwise:
        print(
            f"{row['编码对']}: 存在性kappa={row['存在性Cohen_Kappa']}, "
            f"组合标签加权kappa={row['组合标签二次加权Kappa']}"
        )
    print(
        f"三方: 存在性Fleiss kappa={multi[0]['存在性Fleiss_Kappa']}, "
        f"组合标签Fleiss kappa={multi[0]['组合标签Fleiss_Kappa']}"
    )


if __name__ == "__main__":
    main()
