#!/usr/bin/env python3
"""Build the question-level production register for the full CPHO atlas."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ITEM_DIR = ROOT / "03_corpus" / "item_texts"
TRANSCRIPT_DIR = ROOT / "03_corpus" / "manual_review_transcripts"
ASSET_DIR = ROOT / "03_corpus" / "item_assets"
QUESTION_TEX_DIR = Path(__file__).with_name("questions")
TIKZ_DIR = Path(__file__).with_name("tikz")
OUTPUT = Path(__file__).with_name("全量转写与TikZ重绘清单.csv")


def main() -> None:
    item_ids = sorted(path.stem for path in ITEM_DIR.glob("CPHO*.md"))
    rows: list[dict[str, str]] = []
    for item_id in item_ids:
        figures = sorted(ASSET_DIR.glob(f"{item_id}-*.png"))
        transcript = TRANSCRIPT_DIR / f"{item_id}_transcription_v1.md"
        formula_check = TRANSCRIPT_DIR / f"{item_id}_formula_check_v1.csv"
        question_tex = QUESTION_TEX_DIR / f"{item_id}.tex"
        question_source = question_tex.read_text(encoding="utf-8") if question_tex.exists() else ""
        stem_status = "完成" if "% 题干转写：完成" in question_source else "待处理"
        solution_status = "完成" if "% 解析转写：完成" in question_source else "待处理"
        tikz_status = "不适用" if not figures else "完成" if list(TIKZ_DIR.glob(f"{item_id}-*.tex")) else "待处理"
        figure_check = "不适用" if not figures else "完成" if "% 图形核对：完成" in question_source else "待处理"
        rows.append(
            {
                "题目标识": item_id,
                "届次": item_id[4:6],
                "题号": item_id[-3:],
                "题干来源": str((ITEM_DIR / f"{item_id}.md").relative_to(ROOT)),
                "题面转写入口": str(transcript.relative_to(ROOT)) if transcript.exists() else "待从原题页转写",
                "解析与公式核对入口": str(formula_check.relative_to(ROOT)) if formula_check.exists() else "待从原答案页逐式转写",
                "题图数量": str(len(figures)),
                "题图来源": "；".join(str(path.relative_to(ROOT)) for path in figures) if figures else "无题图",
                "题干正式转写": stem_status,
                "解析正式转写": solution_status,
                "TikZ重绘": tikz_status,
                "图形一致性核对": figure_check,
                "备注": "不得使用原题截图；公式、下标、图号和方向均须回查原页。",
            }
        )
    with OUTPUT.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {len(rows)} records to {OUTPUT}")


if __name__ == "__main__":
    main()
