#!/usr/bin/env python3
"""Build the two manuscript flow diagrams from the current R01 evidence boundary."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = ROOT / "08_manuscript/figures"
FONT = "Hiragino Sans GB"
COLORS = {
    "source": "#DDEAF7",
    "process": "#E2F0D9",
    "boundary": "#FFF2CC",
    "result": "#FCE4D6",
    "line": "#486581",
    "text": "#1F2933",
}


def setup(figsize: tuple[float, float]):
    plt.rcParams.update({"font.family": FONT, "axes.unicode_minus": False})
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    return fig, ax


def box(ax, x: float, y: float, width: float, height: float, text: str, color: str, size: float = 10.5):
    patch = FancyBboxPatch(
        (x - width / 2, y - height / 2), width, height,
        boxstyle="round,pad=0.012,rounding_size=0.016",
        linewidth=1.0, edgecolor=COLORS["line"], facecolor=color,
    )
    ax.add_patch(patch)
    ax.text(x, y, text, ha="center", va="center", fontsize=size, color=COLORS["text"], linespacing=1.35)
    return (x, y, width, height)


def arrow(ax, upper, lower):
    start = (upper[0], upper[1] - upper[3] / 2 - 0.007)
    end = (lower[0], lower[1] + lower[3] / 2 + 0.007)
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=11, linewidth=1.15, color=COLORS["line"]))


def output(fig, stem: str):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for suffix, dpi in (("png", 240), ("pdf", None)):
        fig.savefig(OUTPUT_DIR / f"{stem}.{suffix}", dpi=dpi, bbox_inches="tight", pad_inches=0.08)
    plt.close(fig)


def build_technical_route():
    fig, ax = setup((8.2, 13.0))
    steps = [
        ("第35至42届复赛试题与参考答案", "source"),
        ("小问级语料库\n219个分析单元", "source"),
        ("题干、解答与图件核对入口\n保留项目内定位证据", "process"),
        ("科学思维四维度与\nSOLO启发的任务结构等级", "process"),
        ("RATER-A/B 独立编码\n过程按自声明归档", "process"),
        ("ADJ-01裁决、ADJ-02更正与\nR01逐条补证", "process"),
        ("唯一版本化编码表与证据链\n876条当前编码记录", "result"),
        ("维度分布、等级构成、共现与\n典型任务结构的描述性输出", "result"),
        ("结果—任务—支架—评价\n教学转化设计建议", "boundary"),
        ("教师或课堂研究\n仅在取得真实材料后条件性补充", "boundary"),
    ]
    items = []
    for y, (text, category) in zip([0.94, 0.845, 0.75, 0.655, 0.56, 0.465, 0.37, 0.275, 0.18, 0.085], steps):
        items.append(box(ax, 0.5, y, 0.76, 0.068, text, COLORS[category]))
    for current, following in zip(items, items[1:]):
        arrow(ax, current, following)
    output(fig, "figure_1_1_r01_technical_route_v1")


def build_framework():
    fig, ax = setup((11.2, 7.2))
    a = box(ax, 0.22, 0.90, 0.34, 0.12, "课程标准与科学思维文献\nCS-001；ST-002/ST-003限边界引用", COLORS["source"], 10)
    c = box(ax, 0.78, 0.90, 0.34, 0.12, "SOLO理论与任务分析文献\n仍待关键全文核验", COLORS["boundary"], 10)
    b = box(ax, 0.22, 0.68, 0.34, 0.11, "科学思维四维度\n模型建构、科学推理、科学论证、质疑创新", COLORS["process"], 10)
    d = box(ax, 0.78, 0.68, 0.34, 0.11, "任务认知结构要求等级\nL1至L4", COLORS["process"], 10.5)
    e = box(ax, 0.5, 0.46, 0.42, 0.115, "小问级两层编码框架\n维度存在性 + 结构等级", COLORS["process"], 11)
    f = box(ax, 0.5, 0.27, 0.42, 0.105, "第35至42届复赛试题语料库\n219个分析单元", COLORS["source"], 11)
    g = box(ax, 0.5, 0.10, 0.42, 0.10, "R01版本化编码、证据链与\n描述性结果输出", COLORS["result"], 10.5)
    h = box(ax, 0.15, 0.10, 0.23, 0.10, "分布、共现与\n典型任务结构", COLORS["result"], 9.5)
    i = box(ax, 0.85, 0.10, 0.23, 0.10, "教学转化设计建议\n待真实教学证据", COLORS["boundary"], 9.5)
    arrow(ax, a, b)
    arrow(ax, c, d)
    ax.add_patch(FancyArrowPatch((b[0] + b[2] / 2, b[1] - b[3] / 2), (e[0] - e[2] / 2, e[1] + e[3] / 2), arrowstyle="-|>", mutation_scale=11, linewidth=1.15, color=COLORS["line"]))
    ax.add_patch(FancyArrowPatch((d[0] - d[2] / 2, d[1] - d[3] / 2), (e[0] + e[2] / 2, e[1] + e[3] / 2), arrowstyle="-|>", mutation_scale=11, linewidth=1.15, color=COLORS["line"]))
    arrow(ax, e, f)
    arrow(ax, f, g)
    ax.add_patch(FancyArrowPatch((g[0] - g[2] / 2, g[1]), (h[0] + h[2] / 2, h[1]), arrowstyle="-|>", mutation_scale=11, linewidth=1.15, color=COLORS["line"]))
    ax.add_patch(FancyArrowPatch((g[0] + g[2] / 2, g[1]), (i[0] - i[2] / 2, i[1]), arrowstyle="-|>", mutation_scale=11, linewidth=1.15, color=COLORS["line"]))
    output(fig, "figure_2_1_r01_theoretical_framework_v1")


if __name__ == "__main__":
    build_technical_route()
    build_framework()
