#!/usr/bin/env python3
"""Create readable, source-faithful question excerpts for Chapter 5."""

from pathlib import Path

from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parents[2]
RENDERS = ROOT / "03_corpus/manual_review_renders/G1-07-A1"
OUTPUT = ROOT / "08_manuscript/figures"


CASES = [
    (
        RENDERS / "CPHO41-Q06-paper-page-4.png",
        OUTPUT / "figure_5_1_question_excerpt_source.png",
        (170, 1080, 4100, 2180),
    ),
    (
        RENDERS / "CPHO41-Q07-paper-page-5.png",
        OUTPUT / "figure_5_2_question_excerpt_source.png",
        (180, 870, 4120, 2120),
    ),
    (
        RENDERS / "CPHO42-Q04-paper-page-3.png",
        OUTPUT / "figure_5_3_question_excerpt_source.png",
        (45, 560, 1200, 1335),
    ),
]


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for source, destination, box in CASES:
        image = Image.open(source).convert("RGB")
        excerpt = image.crop(box)
        excerpt = ImageOps.expand(excerpt, border=18, fill="white")
        excerpt.save(destination, quality=95)


if __name__ == "__main__":
    main()
