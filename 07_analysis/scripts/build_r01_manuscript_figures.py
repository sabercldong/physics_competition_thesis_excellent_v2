#!/usr/bin/env python3
"""Build thesis-ready descriptive figures from the approved R01 outputs."""

from __future__ import annotations

import argparse
import csv
import hashlib
from collections import Counter
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RESULTS_DIR = PROJECT_ROOT / "07_analysis/results/formal_rater_r01/correction_v1"
EXPECTED_CODING_SHA256 = "3da0ec26a25b7b78bd62088dabccbc948dc62c7435fb8672d6daaf97e59af852"
DIMENSIONS = ["模型建构", "科学推理", "科学论证", "质疑创新"]
LEVELS = ["L1", "L2", "L3", "L4"]
DIMENSION_COLORS = ["#3B6B8E", "#2D8C7C", "#B85C38", "#8E6C9C"]
LEVEL_COLORS = ["#BFD7EA", "#78A6C8", "#3B6B8E", "#173F5F"]


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def configure_fonts() -> None:
    plt.rcParams["font.family"] = "Hiragino Sans GB"
    plt.rcParams["font.sans-serif"] = [
        "Hiragino Sans GB",
        "Songti SC",
        "Noto Sans CJK SC",
        "Microsoft YaHei",
        "Arial Unicode MS",
    ]
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["pdf.fonttype"] = 42
    plt.rcParams["ps.fonttype"] = 42


def save_figure(fig: plt.Figure, output_dir: Path, stem: str) -> tuple[Path, Path]:
    png_path = output_dir / f"{stem}.png"
    pdf_path = output_dir / f"{stem}.pdf"
    jpg_path = output_dir / f"{stem}.jpg"
    fig.savefig(png_path, dpi=300, bbox_inches="tight", facecolor="white")
    fig.savefig(pdf_path, bbox_inches="tight", facecolor="white")
    fig.savefig(jpg_path, dpi=220, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return png_path, pdf_path


def polish_axis(axis: plt.Axes) -> None:
    """Use a quiet, print-friendly visual language across result figures."""
    axis.set_facecolor("#FFFFFF")
    axis.set_axisbelow(True)
    axis.tick_params(labelsize=10)
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)


def export_case_image(source_path: Path, output_dir: Path, stem: str) -> Path:
    """Provide Word-compatible copies of the two source figures used in Chapter 5."""
    target_path = output_dir / f"{stem}.jpg"
    with Image.open(source_path) as image:
        image.convert("RGB").save(target_path, quality=95, optimize=True)
    return target_path


def build_presence_figure(rows: list[dict[str, str]], output_dir: Path) -> tuple[Path, Path]:
    by_dimension = {row["dimension"]: row for row in rows}
    values = [float(by_dimension[dimension]["proportion"]) * 100 for dimension in DIMENSIONS]
    counts = [int(by_dimension[dimension]["items_present"]) for dimension in DIMENSIONS]

    fig, axis = plt.subplots(figsize=(7.4, 3.7))
    bars = axis.barh(DIMENSIONS, values, color=DIMENSION_COLORS, height=0.58)
    axis.set_xlim(0, 112)
    axis.set_xlabel("出现比例（%）")
    axis.xaxis.grid(True, color="#E3E7EA", linewidth=0.8)
    polish_axis(axis)
    axis.spines["left"].set_visible(False)
    axis.tick_params(axis="y", length=0)
    axis.invert_yaxis()
    for bar, value, count in zip(bars, values, counts):
        axis.text(value + 1.8, bar.get_y() + bar.get_height() / 2, f"{count}个（{value:.2f}%）", va="center", fontsize=10)
    return save_figure(fig, output_dir, "figure_4_1_dimension_presence_r01_v1")


def build_level_figure(rows: list[dict[str, str]], output_dir: Path) -> tuple[Path, Path]:
    by_key = {(row["dimension"], row["level"]): row for row in rows}
    fig, axis = plt.subplots(figsize=(8.1, 4.1))
    left = [0.0] * len(DIMENSIONS)
    for level, color in zip(LEVELS, LEVEL_COLORS):
        values = [float(by_key[(dimension, level)]["proportion_among_present"]) * 100 for dimension in DIMENSIONS]
        bars = axis.barh(DIMENSIONS, values, left=left, label=level, color=color, height=0.58)
        for index, (bar, value) in enumerate(zip(bars, values)):
            if value >= 7:
                axis.text(left[index] + value / 2, bar.get_y() + bar.get_height() / 2, f"{value:.1f}%", ha="center", va="center", fontsize=8)
        left = [current + value for current, value in zip(left, values)]
    axis.set_xlim(0, 100)
    axis.set_xlabel("在本维度出现单元中的构成（%）")
    axis.legend(ncol=4, loc="upper center", bbox_to_anchor=(0.5, -0.18), frameon=False)
    axis.xaxis.grid(True, color="#E3E7EA", linewidth=0.8)
    polish_axis(axis)
    axis.spines["left"].set_visible(False)
    axis.tick_params(axis="y", length=0)
    axis.invert_yaxis()
    return save_figure(fig, output_dir, "figure_4_2_level_distribution_r01_v1")


def build_level_pair_figure(coding: list[dict[str, str]], output_dir: Path) -> tuple[Path, Path]:
    """Show how model construction and scientific reasoning are paired per item."""
    by_item: dict[str, dict[str, dict[str, str]]] = {}
    for row in coding:
        by_item.setdefault(row["item_id"], {})[row["dimension"]] = row

    levels = ["L1", "L2", "L3"]
    matrix = [[0 for _ in levels] for _ in levels]
    for dimensions in by_item.values():
        model = dimensions["模型建构"]
        reasoning = dimensions["科学推理"]
        if model["present"] == "1" and model["level"] in levels and reasoning["level"] in levels:
            matrix[levels.index(model["level"])][levels.index(reasoning["level"])] += 1

    fig, axis = plt.subplots(figsize=(6.4, 4.7))
    image = axis.imshow(matrix, cmap="GnBu", vmin=0, vmax=max(max(row) for row in matrix))
    axis.set_xticks(range(len(levels)), levels)
    axis.set_yticks(range(len(levels)), levels)
    axis.set_xlabel("科学推理等级")
    axis.set_ylabel("模型建构等级")
    for row_index, row in enumerate(matrix):
        for column_index, value in enumerate(row):
            axis.text(column_index, row_index, str(value), ha="center", va="center", fontsize=12,
                      color="white" if value >= 30 else "#173F5F")
    colorbar = fig.colorbar(image, ax=axis, shrink=0.86)
    colorbar.set_label("分析单元数")
    return save_figure(fig, output_dir, "figure_4_3_model_reasoning_level_pair_r01_v1")


def build_pattern_figure(coding: list[dict[str, str]], output_dir: Path) -> tuple[Path, Path]:
    """Plot the five observed complete dimension combinations in Chinese."""
    by_item: dict[str, dict[str, dict[str, str]]] = {}
    for row in coding:
        by_item.setdefault(row["item_id"], {})[row["dimension"]] = row
    patterns = Counter(
        "、".join(dimension for dimension in DIMENSIONS if dimensions[dimension]["present"] == "1")
        for dimensions in by_item.values()
    )
    order = [
        "模型建构、科学推理、科学论证",
        "模型建构、科学推理",
        "模型建构、科学推理、质疑创新",
        "模型建构、科学推理、科学论证、质疑创新",
        "科学推理",
    ]
    labels = [label.replace("、", " - ") for label in order]
    values = [patterns[label] for label in order]
    colors = ["#3B6B8E", "#5A8DB5", "#2D8C7C", "#B85C38", "#9AA5B1"]
    fig, axis = plt.subplots(figsize=(8.5, 4.4))
    bars = axis.barh(labels, values, color=colors, height=0.56)
    axis.set_xlabel("分析单元数")
    axis.set_xlim(0, 76)
    axis.xaxis.grid(True, color="#E3E7EA", linewidth=0.8)
    polish_axis(axis)
    axis.spines["left"].set_visible(False)
    axis.tick_params(axis="y", length=0)
    axis.invert_yaxis()
    for bar, value in zip(bars, values):
        axis.text(value + 1.4, bar.get_y() + bar.get_height() / 2, f"{value}个（{value / 219:.2%}）",
                  ha="left", va="center", fontsize=10)
    return save_figure(fig, output_dir, "figure_4_4_dimension_patterns_r01_v1")


def build_laser_case_guide(output_dir: Path) -> Path:
    """Create a reader-facing schematic for the laser-acceleration case."""
    fig, axis = plt.subplots(figsize=(8.2, 3.5))
    axis.set_xlim(0, 10)
    axis.set_ylim(0, 4)
    axis.axis("off")
    axis.annotate("", xy=(9.1, 2), xytext=(0.9, 2), arrowprops={"arrowstyle": "->", "lw": 2.2, "color": "#B85C38"})
    axis.text(9.25, 2.15, "z轴\n激光传播方向", fontsize=10, color="#B85C38")
    for x in [1.6, 3.0, 4.4, 5.8, 7.2]:
        axis.plot([x, x], [1.1, 2.9], color="#3B6B8E", linewidth=1.5)
    axis.text(4.4, 3.2, "线偏振单色平面电磁波", ha="center", fontsize=12, weight="bold")
    axis.annotate("电子注入", xy=(3.8, 1.7), xytext=(1.2, 0.55), arrowprops={"arrowstyle": "->", "lw": 2, "color": "#2D8C7C"}, color="#2D8C7C", fontsize=11)
    axis.text(1.0, 3.55, "题设限定：在 x-z 平面内入射；入射角不大于 π/2；忽略辐射阻尼", fontsize=10.5,
              bbox={"boxstyle": "round,pad=0.35", "facecolor": "#EEF4F8", "edgecolor": "#A9C3D5"})
    axis.text(5.0, 0.35, "读图重点：哪些条件限制变量，哪些条件决定可用模型？", ha="center", fontsize=10.5, color="#4A5560")
    png_path, _ = save_figure(fig, output_dir, "figure_5_3_laser_acceleration_guide_v1")
    return png_path


def write_manifest(output_dir: Path, figure_pairs: list[tuple[str, Path, Path]], coding_hash: str) -> Path:
    manifest = output_dir / "r01_manuscript_figures_manifest_v1.csv"
    with manifest.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["figure_id", "description", "input_coding_sha256", "png_path", "png_sha256", "pdf_path", "pdf_sha256"],
            lineterminator="\n",
        )
        writer.writeheader()
        for figure_id, png_path, pdf_path in figure_pairs:
            writer.writerow(
                {
                    "figure_id": figure_id,
                    "description": "R01可追溯描述性结果图件；不用于学生能力、教学效果或因果推断",
                    "input_coding_sha256": coding_hash,
                    "png_path": png_path.relative_to(PROJECT_ROOT).as_posix(),
                    "png_sha256": sha256_file(png_path),
                    "pdf_path": pdf_path.relative_to(PROJECT_ROOT).as_posix(),
                    "pdf_sha256": sha256_file(pdf_path),
                }
            )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=PROJECT_ROOT / "08_manuscript/figures")
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    configure_fonts()

    coding_path = PROJECT_ROOT / "07_analysis/data/final_coding_r01_correction_v1.csv"
    coding_hash = sha256_file(coding_path)
    if coding_hash != EXPECTED_CODING_SHA256:
        raise SystemExit(f"unexpected coding SHA-256: {coding_hash}")

    presence_rows = read_rows(RESULTS_DIR / "final_dimension_presence.csv")
    level_rows = read_rows(RESULTS_DIR / "final_level_distribution.csv")
    coding_rows = read_rows(coding_path)
    for row in [*presence_rows, *level_rows]:
        if row["source_final_coding_sha256"] != coding_hash:
            raise SystemExit("descriptive CSV source hash does not match the current coding table")

    figure_pairs = [
        ("图4-1", *build_presence_figure(presence_rows, args.output_dir)),
        ("图4-2", *build_level_figure(level_rows, args.output_dir)),
        ("图4-3", *build_level_pair_figure(coding_rows, args.output_dir)),
        ("图4-4", *build_pattern_figure(coding_rows, args.output_dir)),
    ]
    build_laser_case_guide(args.output_dir)
    export_case_image(
        PROJECT_ROOT / "03_corpus/item_assets/CPHO41-Q06-figure1-page4-raw.png",
        args.output_dir,
        "figure_5_1_gravity_deflection_source_v1",
    )
    export_case_image(
        PROJECT_ROOT / "03_corpus/item_assets/CPHO41-Q07-figure7b-page4-recrop-v1.png",
        args.output_dir,
        "figure_5_2_quantum_ring_source_v1",
    )
    manifest = write_manifest(args.output_dir, figure_pairs, coding_hash)
    print(f"generated {len(figure_pairs)} figures and {manifest.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
