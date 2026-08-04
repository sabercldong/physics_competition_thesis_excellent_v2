#!/usr/bin/env python3
"""Compute reproducible agreement between V3 labels and an anonymous return."""

from __future__ import annotations

import argparse
import csv
import hashlib
import math
import random
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RETURN = ROOT / (
    "07_analysis/data/v3_independent_validation/incoming/RATER-F/"
    "第35至42届第三版匿名盲评编码表_RATER-F_300行.csv"
)
DEFAULT_KEY = ROOT / (
    "07_analysis/data/v3_independent_validation/author_only/"
    "独立盲评抽样与V3对照密钥_不得交评分者.csv"
)
DEFAULT_FINAL = ROOT / "07_analysis/data/第35至42届科学思维第三版唯一编码表.csv"
DEFAULT_DECLARATION = ROOT / (
    "07_analysis/data/v3_independent_validation/incoming/RATER-F/"
    "RATER-F匿名独立性声明.md"
)
DEFAULT_OUTPUT = ROOT / "07_analysis/results/第三版匿名盲评RATER-F一致性"

DIMENSIONS = ["模型建构", "科学推理", "科学论证", "质疑创新"]
PRESENCE_LABELS = ["否", "是"]
LEVEL_LABELS = ["L1", "L2", "L3", "L4"]
COMBINED_LABELS = ["未出现", "L1", "L2", "L3", "L4"]
REGULAR_STRATUM = "各届常规补充"
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


def exact_agreement(a: list[str], b: list[str]) -> float | None:
    if not a:
        return None
    return sum(x == y for x, y in zip(a, b)) / len(a)


def cohen_kappa(a: list[str], b: list[str], categories: list[str]) -> float | None:
    if not a:
        return None
    n = len(a)
    po = exact_agreement(a, b)
    count_a = Counter(a)
    count_b = Counter(b)
    pe = sum((count_a[c] / n) * (count_b[c] / n) for c in categories)
    if math.isclose(1.0 - pe, 0.0):
        return None
    return ((po or 0.0) - pe) / (1.0 - pe)


def gwet_ac1(a: list[str], b: list[str], categories: list[str]) -> float | None:
    if not a:
        return None
    n = len(a)
    q = len(categories)
    if q < 2:
        return None
    po = exact_agreement(a, b)
    count_a = Counter(a)
    count_b = Counter(b)
    pooled = {c: (count_a[c] + count_b[c]) / (2 * n) for c in categories}
    pe = sum(pooled[c] * (1.0 - pooled[c]) for c in categories) / (q - 1)
    if math.isclose(1.0 - pe, 0.0):
        return 1.0 if math.isclose(po or 0.0, 1.0) else None
    return ((po or 0.0) - pe) / (1.0 - pe)


def quadratic_weighted_kappa(
    a: list[str], b: list[str], categories: list[str]
) -> float | None:
    if not a:
        return None
    n = len(a)
    q = len(categories)
    if q < 2:
        return None
    index = {label: i for i, label in enumerate(categories)}
    count_a = Counter(a)
    count_b = Counter(b)
    denominator = float((q - 1) ** 2)
    observed = sum(((index[x] - index[y]) ** 2) / denominator for x, y in zip(a, b)) / n
    expected = 0.0
    for x in categories:
        for y in categories:
            weight = ((index[x] - index[y]) ** 2) / denominator
            expected += weight * (count_a[x] / n) * (count_b[y] / n)
    if math.isclose(expected, 0.0):
        return None
    return 1.0 - observed / expected


def percentile(values: list[float], probability: float) -> float | None:
    clean = sorted(v for v in values if math.isfinite(v))
    if not clean:
        return None
    position = (len(clean) - 1) * probability
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return clean[lower]
    fraction = position - lower
    return clean[lower] * (1 - fraction) + clean[upper] * fraction


def metric_bundle(rows: list[dict[str, str]]) -> dict[str, float | int | None]:
    v3_presence = [row["v3_present_label"] for row in rows]
    reviewer_presence = [row["review_present"] for row in rows]
    both_present = [
        row for row in rows if row["v3_present_label"] == "是" and row["review_present"] == "是"
    ]
    v3_levels = [row["v3_level"] for row in both_present]
    reviewer_levels = [row["review_level"] for row in both_present]
    v3_combined = [row["v3_level"] for row in rows]
    reviewer_combined = [row["review_level"] for row in rows]
    return {
        "行数": len(rows),
        "单元数": len({row["blind_unit_no"] for row in rows}),
        "双方均判出现行数": len(both_present),
        "存在性原始一致率": exact_agreement(v3_presence, reviewer_presence),
        "存在性Cohen_Kappa": cohen_kappa(v3_presence, reviewer_presence, PRESENCE_LABELS),
        "存在性Gwet_AC1": gwet_ac1(v3_presence, reviewer_presence, PRESENCE_LABELS),
        "双方均出现时等级原始一致率": exact_agreement(v3_levels, reviewer_levels),
        "双方均出现时等级名义Kappa": cohen_kappa(v3_levels, reviewer_levels, LEVEL_LABELS),
        "双方均出现时等级二次加权Kappa": quadratic_weighted_kappa(
            v3_levels, reviewer_levels, LEVEL_LABELS
        ),
        "双方均出现时等级相差不超过一级比例": (
            sum(abs(LEVEL_LABELS.index(x) - LEVEL_LABELS.index(y)) <= 1 for x, y in zip(v3_levels, reviewer_levels))
            / len(v3_levels)
            if v3_levels
            else None
        ),
        "组合标签原始一致率": exact_agreement(v3_combined, reviewer_combined),
        "组合标签名义Kappa": cohen_kappa(v3_combined, reviewer_combined, COMBINED_LABELS),
        "组合标签二次加权Kappa": quadratic_weighted_kappa(
            v3_combined, reviewer_combined, COMBINED_LABELS
        ),
    }


CI_METRICS = [
    "存在性原始一致率",
    "存在性Cohen_Kappa",
    "存在性Gwet_AC1",
    "双方均出现时等级原始一致率",
    "双方均出现时等级二次加权Kappa",
    "组合标签原始一致率",
    "组合标签二次加权Kappa",
]


def cluster_bootstrap_ci(
    rows: list[dict[str, str]], iterations: int, seed: int
) -> dict[str, tuple[float | None, float | None, int]]:
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        groups[row["blind_unit_no"]].append(row)
    units = sorted(groups)
    if not units:
        return {metric: (None, None, 0) for metric in CI_METRICS}
    rng = random.Random(seed)
    values: dict[str, list[float]] = {metric: [] for metric in CI_METRICS}
    for _ in range(iterations):
        sampled_rows: list[dict[str, str]] = []
        for unit in rng.choices(units, k=len(units)):
            sampled_rows.extend(groups[unit])
        bundle = metric_bundle(sampled_rows)
        for metric in CI_METRICS:
            value = bundle[metric]
            if isinstance(value, (int, float)) and math.isfinite(value):
                values[metric].append(float(value))
    return {
        metric: (percentile(vals, 0.025), percentile(vals, 0.975), len(vals))
        for metric, vals in values.items()
    }


def enrich_metric_row(
    label: str,
    rows: list[dict[str, str]],
    iterations: int,
    seed: int,
) -> dict[str, object]:
    bundle = metric_bundle(rows)
    ci = cluster_bootstrap_ci(rows, iterations, seed)
    result: dict[str, object] = {"分析范围": label}
    for key, value in bundle.items():
        result[key] = value if isinstance(value, int) else fmt(value)
        if key in CI_METRICS:
            lower, upper, valid = ci[key]
            result[f"{key}_95%CI下限"] = fmt(lower)
            result[f"{key}_95%CI上限"] = fmt(upper)
            result[f"{key}_有效重复数"] = valid
    return result


def validate_and_merge(
    return_rows: list[dict[str, str]],
    key_rows: list[dict[str, str]],
    final_rows: list[dict[str, str]],
    reviewer_id: str,
) -> tuple[list[dict[str, str]], list[dict[str, object]]]:
    checks: list[dict[str, object]] = []

    def add(name: str, passed: bool, detail: str) -> None:
        checks.append({"检查项": name, "结果": "通过" if passed else "失败", "说明": detail})
        if not passed:
            raise ValueError(f"{name}: {detail}")

    add("匿名回填行数", len(return_rows) == 300, f"实测{len(return_rows)}行，预期300行")
    add("密钥行数", len(key_rows) == 300, f"实测{len(key_rows)}行，预期300行")
    return_ids = [row["blind_row_id"].strip() for row in return_rows]
    key_ids = [row["blind_row_id"].strip() for row in key_rows]
    add("匿名回填主键唯一", len(return_ids) == len(set(return_ids)), "blind_row_id无重复")
    add("密钥主键唯一", len(key_ids) == len(set(key_ids)), "blind_row_id无重复")
    add("匿名回填与密钥主键集合一致", set(return_ids) == set(key_ids), "300个blind_row_id完全配对")
    required_fields = [
        "independent_reviewer_id",
        "review_date",
        "review_present",
        "review_level",
        "question_evidence_quote",
        "solution_evidence_quote",
        "evidence_location",
        "adjacent_level_exclusion",
        "confidence",
        "reviewer_statement",
    ]
    blank_required = sum(
        not row.get(field, "").strip() for row in return_rows for field in required_fields
    )
    add("匿名回填必填字段完整", blank_required == 0, f"空白单元格{blank_required}个")
    reviewer_ids = {
        row.get("independent_reviewer_id", "").strip() for row in return_rows
    }
    add(
        "匿名评分者代号一致",
        reviewer_ids == {reviewer_id},
        f"实测代号：{','.join(sorted(reviewer_ids)) or '空'}；预期：{reviewer_id}",
    )

    final_by_id = {row["review_row_id"].strip(): row for row in final_rows}
    add(
        "第三版唯一编码表主键唯一",
        len(final_by_id) == len(final_rows),
        f"实测{len(final_rows)}行，review_row_id无重复",
    )
    key_by_id = {row["blind_row_id"].strip(): row for row in key_rows}
    merged: list[dict[str, str]] = []
    key_mismatches = 0
    final_mismatches = 0
    invalid_labels = 0
    missing_final_ids = 0
    units: set[str] = set()
    unit_dimensions: dict[str, set[str]] = defaultdict(set)
    for raw in return_rows:
        row = {key: value.strip() for key, value in raw.items()}
        key_row = key_by_id[row["blind_row_id"]]
        if row["item_id"] != key_row["item_id"].strip() or row["dimension"] != key_row["dimension"].strip():
            key_mismatches += 1
        source_id = key_row["source_review_row_id"].strip()
        final_row = final_by_id.get(source_id)
        if final_row is None:
            missing_final_ids += 1
        else:
            expected_present = final_row["present_label"].strip()
            expected_level = final_row["level"].strip()
            if (
                key_row["item_id"].strip() != final_row["item_id"].strip()
                or key_row["dimension"].strip() != final_row["dimension"].strip()
                or key_row["v3_present_label"].strip() != expected_present
                or key_row["v3_level"].strip() != expected_level
            ):
                final_mismatches += 1
        present = row["review_present"]
        level = row["review_level"]
        valid = (
            (present == "否" and level == "未出现")
            or (present == "是" and level in LEVEL_LABELS)
        )
        if not valid:
            invalid_labels += 1
        row.update(
            {
                "selection_stratum": key_row["selection_stratum"].strip(),
                "v3_present_label": key_row["v3_present_label"].strip(),
                "v3_level": key_row["v3_level"].strip(),
                "source_review_row_id": source_id,
            }
        )
        merged.append(row)
        units.add(row["blind_unit_no"])
        unit_dimensions[row["blind_unit_no"]].add(row["dimension"])

    add("匿名表固定字段与密钥一致", key_mismatches == 0, f"不一致{key_mismatches}行")
    add("密钥标签与第三版唯一表一致", final_mismatches == 0, f"不一致{final_mismatches}行")
    add("密钥源记录均存在", missing_final_ids == 0, f"缺失{missing_final_ids}行")
    add("匿名回填标签合法", invalid_labels == 0, f"非法组合{invalid_labels}行")
    add("分析单元数量", len(units) == 75, f"实测{len(units)}个，预期75个")
    complete_units = sum(unit_dimensions[unit] == set(DIMENSIONS) for unit in units)
    add("每单元四维度齐全", complete_units == 75, f"完整{complete_units}/75个")
    return merged, checks


def confusion_rows(
    rows: list[dict[str, str]], reviewer_id: str
) -> list[dict[str, object]]:
    output: list[dict[str, object]] = []
    scopes = [("全部", rows)] + [(dimension, [r for r in rows if r["dimension"] == dimension]) for dimension in DIMENSIONS]
    for scope, scoped in scopes:
        for metric_type, left_field, right_field, labels in [
            ("存在性", "v3_present_label", "review_present", PRESENCE_LABELS),
            ("组合标签", "v3_level", "review_level", COMBINED_LABELS),
        ]:
            counts = Counter((r[left_field], r[right_field]) for r in scoped)
            for left in labels:
                for right in labels:
                    output.append(
                        {
                            "分析范围": scope,
                            "指标类型": metric_type,
                            "第三版标签": left,
                            f"{reviewer_id}标签": right,
                            "行数": counts[(left, right)],
                        }
                    )
    return output


def distribution_rows(
    rows: list[dict[str, str]], reviewer_id: str
) -> list[dict[str, object]]:
    output: list[dict[str, object]] = []
    scopes = [("全部", rows)] + [(dimension, [r for r in rows if r["dimension"] == dimension]) for dimension in DIMENSIONS]
    for scope, scoped in scopes:
        for source, present_field, level_field in [
            ("第三版", "v3_present_label", "v3_level"),
            (reviewer_id, "review_present", "review_level"),
        ]:
            for kind, field, labels in [
                ("存在性", present_field, PRESENCE_LABELS),
                ("组合标签", level_field, COMBINED_LABELS),
            ]:
                counts = Counter(r[field] for r in scoped)
                for label in labels:
                    output.append(
                        {
                            "分析范围": scope,
                            "标签来源": source,
                            "指标类型": kind,
                            "标签": label,
                            "行数": counts[label],
                            "比例": fmt(counts[label] / len(scoped) if scoped else None),
                        }
                    )
    return output


def disagreement_rows(
    rows: list[dict[str, str]], reviewer_id: str
) -> list[dict[str, object]]:
    output: list[dict[str, object]] = []
    for row in rows:
        if row["v3_present_label"] != row["review_present"]:
            disagreement_type = "维度存在性"
            distance: object = ""
        elif row["v3_level"] != row["review_level"]:
            disagreement_type = "等级"
            distance = abs(LEVEL_LABELS.index(row["v3_level"]) - LEVEL_LABELS.index(row["review_level"]))
        else:
            continue
        output.append(
            {
                "blind_row_id": row["blind_row_id"],
                "blind_unit_no": row["blind_unit_no"],
                "item_id": row["item_id"],
                "届次": row["competition_no"],
                "年份": row["year"],
                "题号": row["question_no"],
                "小问": row["subquestion_no"],
                "维度": row["dimension"],
                "抽样层": row["selection_stratum"],
                "分歧类型": disagreement_type,
                "第三版存在性": row["v3_present_label"],
                "第三版等级": row["v3_level"],
                f"{reviewer_id}存在性": row["review_present"],
                f"{reviewer_id}等级": row["review_level"],
                "等级距离": distance,
                f"{reviewer_id}置信度": row["confidence"],
                "题干证据引文": row["question_evidence_quote"],
                "解答证据引文": row["solution_evidence_quote"],
                "证据位置": row["evidence_location"],
                "相邻等级排除理由": row["adjacent_level_exclusion"],
                "第三版源记录": row["source_review_row_id"],
            }
        )
    return output


def metric_fields(prefix: list[str]) -> list[str]:
    fields = prefix + ["行数", "单元数", "双方均判出现行数"]
    for metric in metric_bundle([]):
        if metric in {"行数", "单元数", "双方均判出现行数"}:
            continue
        fields.append(metric)
        if metric in CI_METRICS:
            fields.extend(
                [f"{metric}_95%CI下限", f"{metric}_95%CI上限", f"{metric}_有效重复数"]
            )
    return fields


def build_method_note(
    output_path: Path,
    metric_rows: list[dict[str, object]],
    disagreements: list[dict[str, object]],
    iterations: int,
    reviewer_id: str,
    reviewer_description: str,
) -> None:
    overall = metric_rows[0]
    presence_disagreements = sum(row["分歧类型"] == "维度存在性" for row in disagreements)
    level_disagreements = sum(row["分歧类型"] == "等级" for row in disagreements)
    display = lambda value: value if value not in {"", None} else "不可计算"
    dimension_table = "\n".join(
        "| {分析范围} | {存在性原始一致率} | {存在性Cohen_Kappa} | {存在性Gwet_AC1} | "
        "{双方均判出现行数} | {双方均出现时等级原始一致率} | "
        "{双方均出现时等级二次加权Kappa} | {组合标签原始一致率} | "
        "{组合标签二次加权Kappa} |".format(
            **{key: display(value) for key, value in row.items()}
        )
        for row in metric_rows
    )
    text = f"""# 第三版编码与{reviewer_id}匿名回填文件一致性统计说明

## 一、统计对象与表述范围

本结果比较项目第三版唯一编码表与{reviewer_id}匿名回填表在75个分析单元、4个科学思维维度上的标签相符程度，共300行。项目登记的评分者背景为：{reviewer_description}。公开材料仅保留匿名代号，不保存姓名、单位或联系方式。下列结果据此表述为第三版编码与匿名独立复核结果之间的一致性。

75个单元并非从221个单元中等概率随机抽取，其中59个为边界核心样本，16个为各届常规补充样本。总体比例和一致性指标用于诊断编码框架及分歧位置，不直接外推为全部试题的标签分布。

## 二、统计口径

1. 存在性：将“是/否”作为二分类，报告原始一致率、Cohen's kappa与Gwet's AC1。
2. 等级：仅在第三版与{reviewer_id}均判定该维度“出现”时比较L1-L4，报告原始一致率、名义kappa、二次加权kappa及相差不超过一级的比例。
3. 组合标签：将“未出现、L1、L2、L3、L4”视为五级标签，报告原始一致率、名义kappa与二次加权kappa。
4. 置信区间：以75个分析单元为聚类单位进行{iterations}次有放回自助抽样，使用2.5%和97.5%百分位数形成95%区间。四个维度随同一分析单元整体抽取。
5. 分层：分别计算59个边界核心单元和16个各届常规补充单元，避免边界样本富集掩盖常规材料表现。

其中，Cohen's kappa按 $\\kappa=(P_o-P_e)/(1-P_e)$ 计算；Gwet's AC1使用两份编码的平均边际概率估计偶然一致；二次加权kappa对相距越远的等级赋予越大的平方距离权重。若样本内双方标签均为同一类别，则Cohen's kappa或加权kappa的期望分歧为零，结果记为“不可计算”，不写成1。

## 三、总体结果

- 存在性原始一致率：{overall['存在性原始一致率']}；Cohen's kappa：{overall['存在性Cohen_Kappa']}；Gwet's AC1：{overall['存在性Gwet_AC1']}。
- 双方均判出现的行数：{overall['双方均判出现行数']}；等级原始一致率：{overall['双方均出现时等级原始一致率']}；等级二次加权kappa：{overall['双方均出现时等级二次加权Kappa']}。
- 五级组合标签原始一致率：{overall['组合标签原始一致率']}；组合标签二次加权kappa：{overall['组合标签二次加权Kappa']}。
- 分歧共{len(disagreements)}行，其中存在性分歧{presence_disagreements}行、双方均判出现后的等级分歧{level_disagreements}行。

| 分析范围 | 存在性一致率 | 存在性kappa | 存在性AC1 | 双方均出现行数 | 等级一致率 | 等级加权kappa | 组合标签一致率 | 组合标签加权kappa |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
{dimension_table}

## 四、解释注意事项

原始一致率、kappa和AC1应结合阅读。若某一维度中双方标签缺少变异，Cohen's kappa或加权kappa可能不可计算；若正例稀少，较高的原始一致率也不等于正例识别充分。各维度的存在性与等级边界分歧应根据《分歧明细.csv》逐条讨论，不能只凭总体系数自动改写第三版标签。

本统计不执行裁决，也不修改第三版唯一编码表。论文可将{reviewer_id}表述为具有上述背景的匿名独立复核者；姓名、单位和联系方式无需进入论文、数据附件或公开仓库。作者对复核者资格说明和独立过程陈述的真实性负责。

## 五、结果文件

- `总体与分维度一致性指标.csv`：总体及四维度指标与聚类自助法区间。
- `分层一致性指标.csv`：边界核心与常规补充样本的分层结果。
- `一致性混淆矩阵.csv`：存在性和五级组合标签的交叉计数。
- `编码标签分布对照.csv`：第三版与{reviewer_id}的标签边际分布。
- `分歧明细.csv`：全部存在性与等级分歧及{reviewer_id}证据字段。
- `输入文件与校验值.csv`：输入文件、行数和SHA-256。
- `一致性统计QA.csv`：主键、标签与第三版源表的一致性校验。
"""
    output_path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--return-file", type=Path, default=DEFAULT_RETURN)
    parser.add_argument("--key-file", type=Path, default=DEFAULT_KEY)
    parser.add_argument("--final-file", type=Path, default=DEFAULT_FINAL)
    parser.add_argument("--declaration-file", type=Path, default=DEFAULT_DECLARATION)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--reviewer-id", default="RATER-F")
    parser.add_argument(
        "--reviewer-description",
        default="具有高中物理教学和物理竞赛教学背景的匿名物理教师",
    )
    parser.add_argument("--bootstrap-iterations", type=int, default=BOOTSTRAP_ITERATIONS)
    parser.add_argument("--seed", type=int, default=BOOTSTRAP_SEED)
    args = parser.parse_args()

    return_rows = read_csv(args.return_file)
    key_rows = read_csv(args.key_file)
    final_rows = read_csv(args.final_file)
    reviewer_id = args.reviewer_id.strip()
    if not reviewer_id:
        raise ValueError("--reviewer-id不得为空")
    merged, checks = validate_and_merge(
        return_rows, key_rows, final_rows, reviewer_id
    )

    args.output_dir.mkdir(parents=True, exist_ok=True)
    metric_rows = [
        enrich_metric_row("全部", merged, args.bootstrap_iterations, args.seed),
        *[
            enrich_metric_row(
                dimension,
                [row for row in merged if row["dimension"] == dimension],
                args.bootstrap_iterations,
                args.seed + index,
            )
            for index, dimension in enumerate(DIMENSIONS, start=1)
        ],
    ]
    write_csv(
        args.output_dir / "总体与分维度一致性指标.csv",
        metric_fields(["分析范围"]),
        metric_rows,
    )

    stratified_rows: list[dict[str, object]] = []
    strata = [
        ("边界核心", [row for row in merged if row["selection_stratum"] != REGULAR_STRATUM]),
        ("各届常规补充", [row for row in merged if row["selection_stratum"] == REGULAR_STRATUM]),
    ]
    for stratum_index, (stratum, stratum_rows) in enumerate(strata, start=1):
        scope_rows = [("全部", stratum_rows)] + [
            (dimension, [row for row in stratum_rows if row["dimension"] == dimension])
            for dimension in DIMENSIONS
        ]
        for scope_index, (scope, scoped) in enumerate(scope_rows, start=1):
            result = enrich_metric_row(
                scope,
                scoped,
                args.bootstrap_iterations,
                args.seed + stratum_index * 100 + scope_index,
            )
            result = {"抽样分层": stratum, **result}
            stratified_rows.append(result)
    write_csv(
        args.output_dir / "分层一致性指标.csv",
        metric_fields(["抽样分层", "分析范围"]),
        stratified_rows,
    )

    write_csv(
        args.output_dir / "一致性混淆矩阵.csv",
        ["分析范围", "指标类型", "第三版标签", f"{reviewer_id}标签", "行数"],
        confusion_rows(merged, reviewer_id),
    )
    write_csv(
        args.output_dir / "编码标签分布对照.csv",
        ["分析范围", "标签来源", "指标类型", "标签", "行数", "比例"],
        distribution_rows(merged, reviewer_id),
    )
    disagreements = disagreement_rows(merged, reviewer_id)
    write_csv(
        args.output_dir / "分歧明细.csv",
        [
            "blind_row_id",
            "blind_unit_no",
            "item_id",
            "届次",
            "年份",
            "题号",
            "小问",
            "维度",
            "抽样层",
            "分歧类型",
            "第三版存在性",
            "第三版等级",
            f"{reviewer_id}存在性",
            f"{reviewer_id}等级",
            "等级距离",
            f"{reviewer_id}置信度",
            "题干证据引文",
            "解答证据引文",
            "证据位置",
            "相邻等级排除理由",
            "第三版源记录",
        ],
        disagreements,
    )

    input_rows: list[dict[str, object]] = []
    for role, path, row_count in [
        (f"{reviewer_id}匿名回填", args.return_file, len(return_rows)),
        ("第三版对照密钥", args.key_file, len(key_rows)),
        ("第三版唯一编码表", args.final_file, len(final_rows)),
        (f"{reviewer_id}匿名声明", args.declaration_file, ""),
    ]:
        input_rows.append(
            {
                "文件角色": role,
                "项目内相对路径": str(path.resolve().relative_to(ROOT)),
                "数据行数": row_count,
                "SHA-256": sha256(path),
            }
        )
    write_csv(
        args.output_dir / "输入文件与校验值.csv",
        ["文件角色", "项目内相对路径", "数据行数", "SHA-256"],
        input_rows,
    )
    checks.extend(
        [
            {
                "检查项": "存在性分歧计数",
                "结果": "记录",
                "说明": f"{sum(row['分歧类型'] == '维度存在性' for row in disagreements)}行",
            },
            {
                "检查项": "等级分歧计数",
                "结果": "记录",
                "说明": f"{sum(row['分歧类型'] == '等级' for row in disagreements)}行",
            },
            {
                "检查项": "统计表述边界",
                "结果": "通过",
                "说明": f"项目登记背景为：{args.reviewer_description}；公开材料仅保留匿名代号",
            },
        ]
    )
    write_csv(
        args.output_dir / "一致性统计QA.csv",
        ["检查项", "结果", "说明"],
        checks,
    )
    build_method_note(
        args.output_dir / "一致性统计说明.md",
        metric_rows,
        disagreements,
        args.bootstrap_iterations,
        reviewer_id,
        args.reviewer_description,
    )

    print(f"输出目录: {args.output_dir}")
    print(f"匿名回填: {len(return_rows)}行；分析单元: {len({r['blind_unit_no'] for r in merged})}个")
    print(f"分歧: {len(disagreements)}行")
    print(f"存在性kappa: {metric_rows[0]['存在性Cohen_Kappa']}")
    print(f"存在性AC1: {metric_rows[0]['存在性Gwet_AC1']}")
    print(f"组合标签二次加权kappa: {metric_rows[0]['组合标签二次加权Kappa']}")


if __name__ == "__main__":
    main()
