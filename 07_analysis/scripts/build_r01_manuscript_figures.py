#!/usr/bin/env python3
"""Build thesis-ready descriptive figures from the approved R01 outputs."""

from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


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
    fig.savefig(png_path, dpi=300, bbox_inches="tight", facecolor="white")
    fig.savefig(pdf_path, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return png_path, pdf_path


def build_presence_figure(rows: list[dict[str, str]], output_dir: Path) -> tuple[Path, Path]:
    by_dimension = {row["dimension"]: row for row in rows}
    values = [float(by_dimension[dimension]["proportion"]) * 100 for dimension in DIMENSIONS]
    counts = [int(by_dimension[dimension]["items_present"]) for dimension in DIMENSIONS]

    fig, axis = plt.subplots(figsize=(7.1, 4.2))
    bars = axis.barh(DIMENSIONS, values, color=DIMENSION_COLORS, height=0.58)
    axis.set_xlim(0, 100)
    axis.set_xlabel("出现比例（%）")
    axis.set_title("图4-1 四维度在分析单元中的出现比例（n=219）", pad=12)
    axis.xaxis.grid(True, color="#D9D9D9", linewidth=0.8)
    axis.set_axisbelow(True)
    axis.spines[["top", "right", "left"]].set_visible(False)
    axis.tick_params(axis="y", length=0)
    axis.invert_yaxis()
    for bar, value, count in zip(bars, values, counts):
        axis.text(value + 1.2, bar.get_y() + bar.get_height() / 2, f"{count}/219  {value:.2f}%", va="center", fontsize=9)
    return save_figure(fig, output_dir, "figure_4_1_dimension_presence_r01_v1")


def build_level_figure(rows: list[dict[str, str]], output_dir: Path) -> tuple[Path, Path]:
    by_key = {(row["dimension"], row["level"]): row for row in rows}
    fig, axis = plt.subplots(figsize=(8.1, 4.6))
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
    axis.set_title("图4-2 四维度的等级构成（仅计入该维度出现的单元）", pad=12)
    axis.legend(ncol=4, loc="upper center", bbox_to_anchor=(0.5, -0.15), frameon=False)
    axis.xaxis.grid(True, color="#D9D9D9", linewidth=0.8)
    axis.set_axisbelow(True)
    axis.spines[["top", "right", "left"]].set_visible(False)
    axis.tick_params(axis="y", length=0)
    axis.invert_yaxis()
    return save_figure(fig, output_dir, "figure_4_2_level_distribution_r01_v1")


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
    for row in [*presence_rows, *level_rows]:
        if row["source_final_coding_sha256"] != coding_hash:
            raise SystemExit("descriptive CSV source hash does not match the current coding table")

    figure_pairs = [
        ("图4-1", *build_presence_figure(presence_rows, args.output_dir)),
        ("图4-2", *build_level_figure(level_rows, args.output_dir)),
    ]
    manifest = write_manifest(args.output_dir, figure_pairs, coding_hash)
    print(f"generated {len(figure_pairs)} figures and {manifest.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
