#!/usr/bin/env python3
"""Build thesis-ready figures from the accepted V3 unique coding table."""

from __future__ import annotations

import argparse
import csv
import hashlib
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[2]
DIMENSIONS = ("模型建构", "科学推理", "科学论证", "质疑创新")
LEVELS = ("L1", "L2", "L3", "L4")
DIMENSION_COLORS = ("#2A6F97", "#3A7D44", "#C15F3C", "#7A5195")
LEVEL_COLORS = ("#DCEAF3", "#9BC3D8", "#4E8FB5", "#1F5673")
EXPECTED_ROWS = 884
EXPECTED_ITEMS = 221


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def configure_fonts() -> None:
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = [
        "Hiragino Sans GB",
        "Heiti SC",
        "Songti SC",
        "Noto Sans CJK SC",
        "Microsoft YaHei",
        "Arial Unicode MS",
    ]
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["pdf.fonttype"] = 42
    plt.rcParams["ps.fonttype"] = 42
    plt.rcParams["figure.facecolor"] = "white"
    plt.rcParams["axes.facecolor"] = "white"


def style_axis(axis: plt.Axes) -> None:
    axis.set_axisbelow(True)
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)
    axis.tick_params(labelsize=9.5)


def save_figure(
    figure: plt.Figure,
    output_dir: Path,
    stem: str,
) -> tuple[Path, Path]:
    png_path = output_dir / f"{stem}.png"
    pdf_path = output_dir / f"{stem}.pdf"
    figure.savefig(
        png_path,
        dpi=320,
        bbox_inches="tight",
        pad_inches=0.08,
        facecolor="white",
    )
    figure.savefig(
        pdf_path,
        bbox_inches="tight",
        pad_inches=0.08,
        facecolor="white",
    )
    plt.close(figure)
    return png_path, pdf_path


def group_by_item(
    rows: list[dict[str, str]],
) -> dict[str, dict[str, dict[str, str]]]:
    grouped: dict[str, dict[str, dict[str, str]]] = defaultdict(dict)
    for row in rows:
        item_id = row["item_id"]
        dimension = row["dimension"]
        if dimension in grouped[item_id]:
            raise SystemExit(f"重复item_id×dimension: {item_id}/{dimension}")
        grouped[item_id][dimension] = row
    if len(grouped) != EXPECTED_ITEMS:
        raise SystemExit(f"分析单元应为{EXPECTED_ITEMS}个，实际为{len(grouped)}个")
    if any(set(item_rows) != set(DIMENSIONS) for item_rows in grouped.values()):
        raise SystemExit("每个分析单元必须恰有四个维度")
    return grouped


def build_presence_figure(
    grouped: dict[str, dict[str, dict[str, str]]],
    output_dir: Path,
) -> tuple[Path, Path]:
    counts = [
        sum(item_rows[dimension]["present"] == "1" for item_rows in grouped.values())
        for dimension in DIMENSIONS
    ]
    percentages = [count / EXPECTED_ITEMS * 100 for count in counts]
    figure, axis = plt.subplots(figsize=(7.4, 3.7))
    bars = axis.barh(
        DIMENSIONS,
        percentages,
        height=0.56,
        color=DIMENSION_COLORS,
    )
    axis.set_xlim(0, 108)
    axis.set_xlabel("出现比例（%）")
    axis.set_xticks(range(0, 101, 20))
    axis.xaxis.grid(True, color="#D9DEE3", linewidth=0.75)
    axis.spines["left"].set_visible(False)
    axis.tick_params(axis="y", length=0)
    axis.invert_yaxis()
    style_axis(axis)
    for bar, count, percentage in zip(bars, counts, percentages):
        axis.text(
            min(percentage + 1.3, 101.5),
            bar.get_y() + bar.get_height() / 2,
            f"{count}（{percentage:.1f}%）",
            va="center",
            fontsize=9.5,
            color="#263238",
        )
    figure.text(
        0.99,
        0.01,
        "注：N=221；同一分析单元可同时出现多个维度。",
        ha="right",
        va="bottom",
        fontsize=8.5,
        color="#4F5963",
    )
    return save_figure(figure, output_dir, "图4-1_四维度出现比例_V3")


def build_level_figure(
    grouped: dict[str, dict[str, dict[str, str]]],
    output_dir: Path,
) -> tuple[Path, Path]:
    present_counts = []
    level_percentages: dict[str, list[float]] = {level: [] for level in LEVELS}
    for dimension in DIMENSIONS:
        levels = [
            item_rows[dimension]["level"]
            for item_rows in grouped.values()
            if item_rows[dimension]["present"] == "1"
        ]
        present_counts.append(len(levels))
        counts = Counter(levels)
        for level in LEVELS:
            level_percentages[level].append(
                counts[level] / len(levels) * 100 if levels else 0.0
            )

    labels = [
        f"{dimension}（n={count}）"
        for dimension, count in zip(DIMENSIONS, present_counts)
    ]
    figure, axis = plt.subplots(figsize=(8.2, 4.2))
    left = np.zeros(len(DIMENSIONS))
    for level, color in zip(LEVELS, LEVEL_COLORS):
        values = np.array(level_percentages[level])
        bars = axis.barh(
            labels,
            values,
            left=left,
            height=0.56,
            color=color,
            label=level,
            edgecolor="white",
            linewidth=0.6,
        )
        for index, (bar, value) in enumerate(zip(bars, values)):
            if value >= 7.0:
                axis.text(
                    left[index] + value / 2,
                    bar.get_y() + bar.get_height() / 2,
                    f"{value:.1f}%",
                    ha="center",
                    va="center",
                    fontsize=8.5,
                    color="#17313F" if level in {"L1", "L2"} else "white",
                )
        left += values
    axis.set_xlim(0, 100)
    axis.set_xlabel("该维度出现单元中的等级构成（%）")
    axis.set_xticks(range(0, 101, 20))
    axis.xaxis.grid(True, color="#D9DEE3", linewidth=0.75)
    axis.spines["left"].set_visible(False)
    axis.tick_params(axis="y", length=0)
    axis.invert_yaxis()
    axis.legend(
        ncol=4,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.16),
        frameon=False,
        handlelength=1.6,
        columnspacing=1.6,
    )
    style_axis(axis)
    figure.text(
        0.99,
        0.01,
        "注：等级比例以各维度已经出现的分析单元为分母。",
        ha="right",
        va="bottom",
        fontsize=8.5,
        color="#4F5963",
    )
    return save_figure(figure, output_dir, "图4-2_四维度等级构成_V3")


def build_year_heatmap(
    grouped: dict[str, dict[str, dict[str, str]]],
    output_dir: Path,
) -> tuple[Path, Path]:
    items_by_year: dict[tuple[str, str], list[dict[str, dict[str, str]]]] = (
        defaultdict(list)
    )
    for item_rows in grouped.values():
        example = next(iter(item_rows.values()))
        items_by_year[(example["year"], example["competition_no"])].append(item_rows)
    year_keys = sorted(items_by_year)
    values = np.zeros((len(year_keys), len(DIMENSIONS)))
    counts = np.zeros_like(values, dtype=int)
    denominators = []
    for row_index, key in enumerate(year_keys):
        items = items_by_year[key]
        denominators.append(len(items))
        for column_index, dimension in enumerate(DIMENSIONS):
            count = sum(item[dimension]["present"] == "1" for item in items)
            counts[row_index, column_index] = count
            values[row_index, column_index] = count / len(items) * 100

    figure, axis = plt.subplots(figsize=(8.3, 5.0))
    image = axis.imshow(values, cmap="YlGnBu", vmin=0, vmax=100, aspect="auto")
    axis.set_xticks(range(len(DIMENSIONS)), DIMENSIONS)
    axis.set_yticks(
        range(len(year_keys)),
        [f"第{competition_no}届（{year}，n={n}）" for (year, competition_no), n in zip(year_keys, denominators)],
    )
    axis.tick_params(axis="x", top=True, bottom=False, labeltop=True, labelbottom=False)
    axis.tick_params(axis="both", length=0, labelsize=9.2)
    for row_index in range(len(year_keys)):
        for column_index in range(len(DIMENSIONS)):
            value = values[row_index, column_index]
            label = f"{counts[row_index, column_index]}\n{value:.1f}%"
            axis.text(
                column_index,
                row_index,
                label,
                ha="center",
                va="center",
                fontsize=8.3,
                color="white" if value >= 62 else "#263238",
            )
    colorbar = figure.colorbar(image, ax=axis, fraction=0.035, pad=0.025)
    colorbar.set_label("出现比例（%）")
    colorbar.ax.tick_params(labelsize=8.5)
    for spine in axis.spines.values():
        spine.set_visible(False)
    return save_figure(figure, output_dir, "图4-3_各届次维度出现比例_V3")


def build_combination_figure(
    grouped: dict[str, dict[str, dict[str, str]]],
    output_dir: Path,
) -> tuple[Path, Path]:
    counts: Counter[str] = Counter()
    for item_rows in grouped.values():
        present_dimensions = [
            dimension
            for dimension in DIMENSIONS
            if item_rows[dimension]["present"] == "1"
        ]
        label = "＋".join(present_dimensions) if present_dimensions else "四维均未出现"
        counts[label] += 1
    ordered = sorted(counts.items(), key=lambda pair: (pair[1], pair[0]))
    labels = [label.replace("＋", "＋\n") for label, _ in ordered]
    values = [count for _, count in ordered]
    colors = ["#9AA6B2", "#7A5195", "#C15F3C", "#4F8E66", "#2A6F97"][-len(values) :]
    figure, axis = plt.subplots(figsize=(8.4, 4.7))
    bars = axis.barh(labels, values, height=0.58, color=colors)
    axis.set_xlabel("分析单元数")
    axis.set_xlim(0, max(values) * 1.18)
    axis.xaxis.grid(True, color="#D9DEE3", linewidth=0.75)
    axis.spines["left"].set_visible(False)
    axis.tick_params(axis="y", length=0, labelsize=8.8)
    style_axis(axis)
    for bar, value in zip(bars, values):
        axis.text(
            value + max(values) * 0.015,
            bar.get_y() + bar.get_height() / 2,
            f"{value}（{value / EXPECTED_ITEMS:.1%}）",
            va="center",
            fontsize=9.2,
            color="#263238",
        )
    figure.text(
        0.99,
        0.01,
        "注：组合标签表示同一分析单元中同时出现的维度。",
        ha="right",
        va="bottom",
        fontsize=8.5,
        color="#4F5963",
    )
    return save_figure(figure, output_dir, "图4-4_维度组合分布_V3")


def write_manifest(
    output_dir: Path,
    figure_pairs: list[tuple[str, str, Path, Path]],
    source_path: Path,
    source_hash: str,
) -> Path:
    manifest = output_dir / "V3结果图件来源登记.csv"
    with manifest.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "图号",
                "图件说明",
                "源唯一编码表",
                "源唯一编码表SHA256",
                "PNG文件",
                "PNG文件SHA256",
                "PDF文件",
                "PDF文件SHA256",
                "解释边界",
            ],
            lineterminator="\n",
        )
        writer.writeheader()
        for figure_id, description, png_path, pdf_path in figure_pairs:
            writer.writerow(
                {
                    "图号": figure_id,
                    "图件说明": description,
                    "源唯一编码表": source_path.relative_to(ROOT).as_posix(),
                    "源唯一编码表SHA256": source_hash,
                    "PNG文件": png_path.relative_to(ROOT).as_posix(),
                    "PNG文件SHA256": file_sha256(png_path),
                    "PDF文件": pdf_path.relative_to(ROOT).as_posix(),
                    "PDF文件SHA256": file_sha256(pdf_path),
                    "解释边界": "描述试题任务要求，不推断学生能力、教学效果、因果关系或统计显著性",
                }
            )
    return manifest


def main() -> None:
    args = parse_args()
    input_path = resolve(args.input)
    output_dir = resolve(args.output_dir)
    if not input_path.is_file():
        raise SystemExit(f"唯一编码表不存在: {input_path}")
    if output_dir.exists() and not output_dir.is_dir():
        raise SystemExit(f"输出路径被普通文件占用: {output_dir}")
    if output_dir.exists() and any(output_dir.iterdir()) and not args.force:
        raise SystemExit(f"输出目录非空；如确认替换须使用--force: {output_dir}")

    rows = read_rows(input_path)
    if len(rows) != EXPECTED_ROWS:
        raise SystemExit(f"唯一编码表应为{EXPECTED_ROWS}行，实际为{len(rows)}行")
    grouped = group_by_item(rows)
    output_dir.mkdir(parents=True, exist_ok=True)
    configure_fonts()

    presence_png, presence_pdf = build_presence_figure(grouped, output_dir)
    level_png, level_pdf = build_level_figure(grouped, output_dir)
    year_png, year_pdf = build_year_heatmap(grouped, output_dir)
    combination_png, combination_pdf = build_combination_figure(grouped, output_dir)
    source_hash = file_sha256(input_path)
    manifest = write_manifest(
        output_dir,
        [
            ("图4-1", "四维度出现比例", presence_png, presence_pdf),
            ("图4-2", "四维度等级构成", level_png, level_pdf),
            ("图4-3", "各届次维度出现比例", year_png, year_pdf),
            ("图4-4", "维度组合分布", combination_png, combination_pdf),
        ],
        input_path,
        source_hash,
    )
    print(f"source_sha256={source_hash}")
    print("figures=4")
    print(f"output_dir={output_dir}")
    print(f"manifest={manifest}")


if __name__ == "__main__":
    main()
