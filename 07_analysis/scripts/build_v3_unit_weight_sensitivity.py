#!/usr/bin/env python3
"""Build third-edition sensitivity outputs for alternative analysis-unit weights."""

from __future__ import annotations

import csv
import re
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "07_analysis/data/第35至42届科学思维第三版唯一编码表.csv"
OUTPUT_DIR = ROOT / "07_analysis/results/第三版正式结果/敏感性分析"
MANUSCRIPT_FIGURE_DIR = ROOT / "08_manuscript/figures/第三版正式结果"

DIMENSIONS = ["模型建构", "科学推理", "科学论证", "质疑创新"]
LEVELS = ["L1", "L2", "L3", "L4"]
SCHEMES = [
    ("分析单元等权", "analysis_unit_weight"),
    ("原始小问等权", "original_subquestion_weight"),
    ("大题等权", "major_question_weight"),
]
COLORS = {
    "原始小问等权": "#2A6F97",
    "大题等权": "#C15F3C",
}
ROMAN_SPLIT_RE = re.compile(r"^\d+-[ivxlcdm]+$", re.IGNORECASE)


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 884:
        raise ValueError(f"Expected 884 dimension records, found {len(rows)}")
    return rows


def original_subquestion_key(row: dict[str, str]) -> str:
    """Merge only researcher-created Roman-suffix splits."""
    if ROMAN_SPLIT_RE.fullmatch(row["subquestion_no"]):
        return row["item_id"].rsplit("_", 1)[0]
    return row["item_id"]


def major_question_key(row: dict[str, str]) -> str:
    return f"CPHO{int(row['competition_no']):02d}-Q{int(row['question_no']):02d}"


def unique_units(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    by_item: dict[str, dict[str, str]] = {}
    dimensions_by_item: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        by_item.setdefault(row["item_id"], row)
        dimensions_by_item[row["item_id"]].add(row["dimension"])
    if any(value != set(DIMENSIONS) for value in dimensions_by_item.values()):
        raise ValueError("Each analysis unit must contain exactly the four dimensions")
    if len(by_item) != 221:
        raise ValueError(f"Expected 221 analysis units, found {len(by_item)}")
    return list(by_item.values())


def add_keys_and_weights(
    rows: list[dict[str, str]], units: list[dict[str, str]]
) -> list[dict[str, str | float | int]]:
    subquestion_size = Counter(original_subquestion_key(row) for row in units)
    major_size = Counter(major_question_key(row) for row in units)
    n_units = len(units)
    n_subquestions = len(subquestion_size)
    n_major = len(major_size)

    enriched: list[dict[str, str | float | int]] = []
    for row in rows:
        sub_key = original_subquestion_key(row)
        major_key = major_question_key(row)
        enriched.append(
            {
                **row,
                "original_subquestion_key": sub_key,
                "major_question_key": major_key,
                "analysis_units_in_original_subquestion": subquestion_size[sub_key],
                "analysis_units_in_major_question": major_size[major_key],
                "analysis_unit_weight": 1 / n_units,
                "original_subquestion_weight": 1
                / (n_subquestions * subquestion_size[sub_key]),
                "major_question_weight": 1 / (n_major * major_size[major_key]),
            }
        )

    if n_subquestions != 209:
        raise ValueError(f"Expected 209 original subquestions, found {n_subquestions}")
    if n_major != 60:
        raise ValueError(f"Expected 60 major questions, found {n_major}")
    split_groups = [key for key, size in subquestion_size.items() if size > 1]
    split_units = sum(subquestion_size[key] for key in split_groups)
    if len(split_groups) != 6 or split_units != 18:
        raise ValueError(
            f"Expected 6 split subquestions and 18 split units, found "
            f"{len(split_groups)} and {split_units}"
        )
    return enriched


def write_csv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def calculate_presence(enriched: list[dict]) -> list[dict]:
    output: list[dict] = []
    for dimension in DIMENSIONS:
        subset = [row for row in enriched if row["dimension"] == dimension]
        for scheme_name, weight_field in SCHEMES:
            denominator = sum(float(row[weight_field]) for row in subset)
            numerator = sum(
                float(row[weight_field])
                for row in subset
                if row["present_label"] == "是"
            )
            output.append(
                {
                    "统计口径": scheme_name,
                    "维度": dimension,
                    "加权出现量": f"{numerator:.8f}",
                    "加权总量": f"{denominator:.8f}",
                    "出现比例": f"{numerator / denominator:.8f}",
                    "出现比例_百分数": f"{100 * numerator / denominator:.4f}",
                }
            )
    return output


def calculate_levels(enriched: list[dict]) -> list[dict]:
    output: list[dict] = []
    for dimension in DIMENSIONS:
        subset = [
            row
            for row in enriched
            if row["dimension"] == dimension and row["present_label"] == "是"
        ]
        for scheme_name, weight_field in SCHEMES:
            denominator = sum(float(row[weight_field]) for row in subset)
            for level in LEVELS:
                numerator = sum(
                    float(row[weight_field])
                    for row in subset
                    if row["level"] == level
                )
                output.append(
                    {
                        "统计口径": scheme_name,
                        "维度": dimension,
                        "等级": level,
                        "加权等级量": f"{numerator:.8f}",
                        "该维度加权出现量": f"{denominator:.8f}",
                        "等级构成比例": f"{numerator / denominator:.8f}"
                        if denominator
                        else "",
                        "等级构成比例_百分数": f"{100 * numerator / denominator:.4f}"
                        if denominator
                        else "",
                    }
                )
    return output


def unit_weight_rows(enriched: list[dict]) -> list[dict]:
    seen: set[str] = set()
    output: list[dict] = []
    for row in enriched:
        if row["item_id"] in seen:
            continue
        seen.add(row["item_id"])
        output.append(
            {
                "分析单元编号": row["item_id"],
                "届次": row["competition_no"],
                "年份": row["year"],
                "题号": row["question_no"],
                "小问号": row["subquestion_no"],
                "原始小问键": row["original_subquestion_key"],
                "大题键": row["major_question_key"],
                "原始小问内分析单元数": row[
                    "analysis_units_in_original_subquestion"
                ],
                "大题内分析单元数": row["analysis_units_in_major_question"],
                "分析单元等权": f"{float(row['analysis_unit_weight']):.10f}",
                "原始小问等权": f"{float(row['original_subquestion_weight']):.10f}",
                "大题等权": f"{float(row['major_question_weight']):.10f}",
            }
        )
    return output


def edition_rows(units: list[dict[str, str]]) -> list[dict]:
    by_edition: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in units:
        by_edition[row["competition_no"]].append(row)

    output: list[dict] = []
    for edition in sorted(by_edition, key=int):
        subset = by_edition[edition]
        sub_sizes = Counter(original_subquestion_key(row) for row in subset)
        output.append(
            {
                "届次": edition,
                "年份": subset[0]["year"],
                "大题数": len({major_question_key(row) for row in subset}),
                "原始小问数": len(sub_sizes),
                "分析单元数": len(subset),
                "发生研究者拆分的原始小问数": sum(
                    1 for size in sub_sizes.values() if size > 1
                ),
                "由拆分形成的分析单元数": sum(
                    size for size in sub_sizes.values() if size > 1
                ),
                "拆分净增分析单元数": sum(
                    size - 1 for size in sub_sizes.values() if size > 1
                ),
            }
        )
    return output


def configure_plotting() -> None:
    plt.rcParams.update(
        {
            "font.sans-serif": [
                "Hiragino Sans GB",
                "Heiti SC",
                "Songti SC",
                "Noto Sans CJK SC",
                "Microsoft YaHei",
                "Arial Unicode MS",
            ],
            "axes.unicode_minus": False,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "font.size": 10,
            "axes.titlesize": 12,
            "axes.labelsize": 10,
        }
    )


def build_sensitivity_figure(presence_rows: list[dict]) -> None:
    values = {
        (row["统计口径"], row["维度"]): float(row["出现比例_百分数"])
        for row in presence_rows
    }
    comparison_schemes = ["原始小问等权", "大题等权"]
    offsets = [-0.12, 0.12]

    configure_plotting()
    fig, ax = plt.subplots(figsize=(8.2, 4.7))
    y_positions = list(range(len(DIMENSIONS)))
    ax.axvline(0, color="#777777", linewidth=0.9, zorder=1)

    plotted_deltas: list[float] = []
    for scheme, offset in zip(comparison_schemes, offsets):
        deltas = [
            values[(scheme, dimension)] - values[("分析单元等权", dimension)]
            for dimension in DIMENSIONS
        ]
        plotted_deltas.extend(deltas)
        shifted_y = [position + offset for position in y_positions]
        ax.scatter(
            deltas,
            shifted_y,
            s=58,
            color=COLORS[scheme],
            label=scheme,
            zorder=3,
        )
        for delta, y in zip(deltas, shifted_y):
            ax.plot([0, delta], [y, y], color=COLORS[scheme], linewidth=1.2, zorder=2)
            horizontal_alignment = "left" if delta >= 0 else "right"
            text_offset = 0.055 if delta >= 0 else -0.055
            ax.text(
                delta + text_offset,
                y,
                f"{delta:+.2f}",
                va="center",
                ha=horizontal_alignment,
                color=COLORS[scheme],
                fontsize=9,
            )

    max_abs = max(abs(value) for value in plotted_deltas)
    limit = max(0.5, max_abs + 0.35)
    ax.set_xlim(-limit, limit)
    ax.set_yticks(y_positions, DIMENSIONS)
    ax.invert_yaxis()
    ax.set_xlabel("相对分析单元等权口径的变化（百分点）")
    ax.set_title("不同权重口径下四维出现比例的变化")
    ax.xaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value:.1f}"))
    ax.grid(axis="x", color="#DDDDDD", linewidth=0.7)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.legend(frameon=False, loc="lower right")
    fig.text(
        0.01,
        0.01,
        "注：正值表示该权重口径的出现比例高于分析单元等权口径。",
        fontsize=8.5,
        color="#555555",
    )
    fig.tight_layout(rect=(0, 0.05, 1, 1))

    figure_name = "图4-5_不同权重口径相对分析单元口径的比例变化_第三版"
    MANUSCRIPT_FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    for target_dir in (OUTPUT_DIR, MANUSCRIPT_FIGURE_DIR):
        stem = target_dir / figure_name
        fig.savefig(stem.with_suffix(".png"), dpi=320, bbox_inches="tight")
        fig.savefig(stem.with_suffix(".pdf"), bbox_inches="tight")
    plt.close(fig)


def write_explanation(
    presence_rows: list[dict],
    level_rows: list[dict],
    edition_summary: list[dict],
) -> None:
    values = {
        (row["统计口径"], row["维度"]): float(row["出现比例_百分数"])
        for row in presence_rows
    }
    max_change = max(
        abs(
            values[(scheme, dimension)]
            - values[("分析单元等权", dimension)]
        )
        for scheme, _ in SCHEMES[1:]
        for dimension in DIMENSIONS
    )
    split_editions = [
        f"第{row['届次']}届"
        for row in edition_summary
        if int(row["发生研究者拆分的原始小问数"]) > 0
    ]
    level_values = {
        (row["统计口径"], row["维度"], row["等级"]): float(
            row["等级构成比例_百分数"]
        )
        for row in level_rows
    }
    max_level_change = max(
        abs(
            level_values[(scheme, dimension, level)]
            - level_values[("分析单元等权", dimension, level)]
        )
        for scheme, _ in SCHEMES[1:]
        for dimension in DIMENSIONS
        for level in LEVELS
    )
    lines = [
        "# 分析单位权重敏感性说明",
        "",
        "## 分析目的",
        "",
        "主分析把221个分析单元等权处理。为检查研究者对复合小问的拆分是否放大某些题目的统计权重，本分析增加“原始小问等权”和“大题等权”两种口径，并以同一份第三版唯一编码表重新计算四维出现比例与等级构成。",
        "",
        "## 单位关系",
        "",
        "- 221个分析单元归属于209个原始小问和60道大题。",
        "- 6个原始小问被拆成18个分析单元，较不拆分口径净增12个单元。",
        f"- 研究者拆分只出现在{'、'.join(split_editions)}。",
        "- 原始题面明确列出的1.1、2.3等编号仍作为原始小问；只有项目中以罗马数字后缀标记的内部拆分单元被重新合并。",
        "",
        "## 三种权重",
        "",
        "1. 分析单元等权：每个分析单元权重为1/221。",
        "2. 原始小问等权：每个原始小问权重为1/209，同一原始小问拆出的单元均分该权重。",
        "3. 大题等权：每道大题权重为1/60，同一大题中的分析单元均分该权重。",
        "",
        "## 结果",
        "",
        "| 维度 | 分析单元等权 | 原始小问等权 | 大题等权 | 最大绝对变化 |",
        "|---|---:|---:|---:|---:|",
    ]
    for dimension in DIMENSIONS:
        baseline = values[("分析单元等权", dimension)]
        original = values[("原始小问等权", dimension)]
        major = values[("大题等权", dimension)]
        dimension_max = max(abs(original - baseline), abs(major - baseline))
        lines.append(
            f"| {dimension} | {baseline:.2f}% | {original:.2f}% | "
            f"{major:.2f}% | {dimension_max:.2f}个百分点 |"
        )
    lines.extend(
        [
            "",
            f"三种口径下，四维出现比例的最大绝对变化为{max_change:.2f}个百分点。模型建构始终居于高位，科学推理始终为100%，科学论证明显低于前两者，质疑创新仍接近零；因此，论文关于四维相对分布的核心描述不因分析单位权重改变而变化。",
            "",
            f"等级构成的最大绝对变化为{max_level_change:.2f}个百分点。模型建构和科学推理在三种口径下均以L3为主，质疑创新的两个正例均为L2；科学论证的L1与L2较为接近，分析单元等权和原始小问等权时L2略多，大题等权时则转为L1略多。因此，科学论证更稳妥的概括是“主要集中于L1至L2”，不宜把其中某一级写成稳定优势等级。",
            "",
            "等级构成表使用各口径下相应维度的加权出现量为分母，不能与全样本出现比例混用。",
            "",
            "## 输出文件",
            "",
            "- `三种分析单位权重下四维出现比例.csv`",
            "- `三种分析单位权重下等级构成.csv`",
            "- `分析单元归属与三种权重.csv`",
            "- `各届分析单位数量与拆分情况.csv`",
            "- `图4-5_不同权重口径相对分析单元口径的比例变化_第三版.png`",
            "- `图4-5_不同权重口径相对分析单元口径的比例变化_第三版.pdf`",
            "",
        ]
    )
    (OUTPUT_DIR / "分析单位权重敏感性说明.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def validate_outputs(
    enriched: list[dict], presence_rows: list[dict], level_rows: list[dict]
) -> None:
    for dimension in DIMENSIONS:
        subset = [row for row in enriched if row["dimension"] == dimension]
        for _, weight_field in SCHEMES:
            total = sum(float(row[weight_field]) for row in subset)
            if abs(total - 1) > 1e-9:
                raise ValueError(
                    f"Weights do not sum to 1 for {dimension}/{weight_field}: {total}"
                )

    values = {
        (row["统计口径"], row["维度"]): float(row["出现比例_百分数"])
        for row in presence_rows
    }
    expected_baseline = {
        "模型建构": 100 * 202 / 221,
        "科学推理": 100.0,
        "科学论证": 100 * 36 / 221,
        "质疑创新": 100 * 2 / 221,
    }
    for dimension, expected in expected_baseline.items():
        actual = values[("分析单元等权", dimension)]
        if abs(actual - expected) > 5e-5:
            raise ValueError(
                f"Baseline mismatch for {dimension}: {actual} vs {expected}"
            )

    for scheme_name, _ in SCHEMES:
        for dimension in DIMENSIONS:
            total = sum(
                float(row["等级构成比例"])
                for row in level_rows
                if row["统计口径"] == scheme_name
                and row["维度"] == dimension
                and row["等级构成比例"]
            )
            if abs(total - 1) > 1e-6:
                raise ValueError(
                    f"Level composition does not sum to 1 for "
                    f"{scheme_name}/{dimension}: {total}"
                )

    ordered = [
        "科学推理",
        "模型建构",
        "科学论证",
        "质疑创新",
    ]
    for scheme_name, _ in SCHEMES:
        observed = sorted(
            DIMENSIONS,
            key=lambda dimension: values[(scheme_name, dimension)],
            reverse=True,
        )
        if observed != ordered:
            raise ValueError(
                f"Dimension ordering changed under {scheme_name}: {observed}"
            )


def main() -> None:
    rows = read_rows(INPUT)
    units = unique_units(rows)
    enriched = add_keys_and_weights(rows, units)
    presence_rows = calculate_presence(enriched)
    level_rows = calculate_levels(enriched)
    editions = edition_rows(units)
    validate_outputs(enriched, presence_rows, level_rows)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(
        OUTPUT_DIR / "三种分析单位权重下四维出现比例.csv",
        ["统计口径", "维度", "加权出现量", "加权总量", "出现比例", "出现比例_百分数"],
        presence_rows,
    )
    write_csv(
        OUTPUT_DIR / "三种分析单位权重下等级构成.csv",
        [
            "统计口径",
            "维度",
            "等级",
            "加权等级量",
            "该维度加权出现量",
            "等级构成比例",
            "等级构成比例_百分数",
        ],
        level_rows,
    )
    write_csv(
        OUTPUT_DIR / "分析单元归属与三种权重.csv",
        [
            "分析单元编号",
            "届次",
            "年份",
            "题号",
            "小问号",
            "原始小问键",
            "大题键",
            "原始小问内分析单元数",
            "大题内分析单元数",
            "分析单元等权",
            "原始小问等权",
            "大题等权",
        ],
        unit_weight_rows(enriched),
    )
    write_csv(
        OUTPUT_DIR / "各届分析单位数量与拆分情况.csv",
        [
            "届次",
            "年份",
            "大题数",
            "原始小问数",
            "分析单元数",
            "发生研究者拆分的原始小问数",
            "由拆分形成的分析单元数",
            "拆分净增分析单元数",
        ],
        editions,
    )
    build_sensitivity_figure(presence_rows)
    write_explanation(presence_rows, level_rows, editions)

    values = {
        (row["统计口径"], row["维度"]): float(row["出现比例_百分数"])
        for row in presence_rows
    }
    max_change = max(
        abs(
            values[(scheme, dimension)]
            - values[("分析单元等权", dimension)]
        )
        for scheme, _ in SCHEMES[1:]
        for dimension in DIMENSIONS
    )
    print("PASS: third-edition analysis-unit weight sensitivity outputs built")
    print("analysis_units=221 original_subquestions=209 major_questions=60")
    print(f"maximum_absolute_change={max_change:.4f} percentage points")
    for scheme_name, _ in SCHEMES:
        values_text = ", ".join(
            f"{dimension}={values[(scheme_name, dimension)]:.4f}%"
            for dimension in DIMENSIONS
        )
        print(f"{scheme_name}: {values_text}")


if __name__ == "__main__":
    main()
