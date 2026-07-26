#!/usr/bin/env python3
"""Create a clean, numbered LaTeX manuscript from the Markdown chapters."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = ROOT / "10_outputs/论文初稿_LaTeX"
COMBINED_MD = OUTPUT_DIR / "论文初稿_合并源稿.md"
TEX_FILE = OUTPUT_DIR / "中学生物理竞赛复赛试题的科学思维要求与教学转化研究.tex"
SOURCES = [
    ROOT / "08_manuscript/00_abstract_content_draft.md",
    ROOT / "08_manuscript/00_abstract_en_content_draft.md",
    ROOT / "08_manuscript/01_introduction.md",
    ROOT / "08_manuscript/02_theory.md",
    ROOT / "08_manuscript/03_methods.md",
    ROOT / "08_manuscript/04_results.md",
    ROOT / "08_manuscript/05_cases_and_diagnosis.md",
    ROOT / "08_manuscript/06_conclusion.md",
    ROOT / "08_manuscript/07_candidate_references.md",
]


def normalise_headings(text: str, source: Path) -> str:
    """Let LaTeX control hierarchy numbering rather than duplicate Markdown labels."""
    if source.name == "07_candidate_references.md":
        text = text.split("## 使用边界", 1)[0]
        text = text.replace("# 参考文献（候选工作稿）", "# 参考文献")
        text = re.sub(r"(?m)^(\[\d+\])", r"\n\1", text)
        text = re.sub(r"(https?://[^\s]+)", r"<\1>", text)
    text = re.sub(r"^#\s+第[一二三四五六七八九十]+章\s+(.+)$", r"# \1", text, flags=re.MULTILINE)
    text = re.sub(r"^(#{2,3})\s+\d+(?:\.\d+)+\s+(.+)$", r"\1 \2", text, flags=re.MULTILINE)
    # The manuscript supplies complete Chinese captions in the paragraph after each image.
    # Empty alt text prevents Pandoc from emitting a second automatic figure caption.
    text = re.sub(r"!\[[^\]]*\]\(([^)]+)\)", r"![](\1)", text)
    return text


def main() -> None:
    combined = "\n\n".join(normalise_headings(path.read_text(encoding="utf-8"), path) for path in SOURCES)
    COMBINED_MD.write_text(combined + "\n", encoding="utf-8")
    command = [
        "pandoc", "--from", "markdown", "--to", "latex", "--standalone", "--toc", "--number-sections",
        "--top-level-division=chapter", "--metadata", "title=中学生物理竞赛复赛试题的科学思维要求与教学转化研究",
        "--metadata", "author=董兴习", "--metadata", "date=2026年7月", "-V", "documentclass=ctexbook",
        "-V", "classoption=a4paper", "-V", "CJKmainfont=Songti SC", "-V", "CJKsansfont=Hiragino Sans GB",
        "-V", "geometry:top=2.5cm", "-V", "geometry:bottom=2.5cm", "-V", "geometry:left=3cm",
        "-V", "geometry:right=2.6cm", "-V", "fontsize=12pt", "-V", "linestretch=1.5", "-V", "colorlinks=true",
        "-V", "linkcolor=black", "-V", "urlcolor=blue", "-o", str(TEX_FILE), str(COMBINED_MD),
    ]
    subprocess.run(command, check=True)
    tex = TEX_FILE.read_text(encoding="utf-8")
    for title in ("摘要", "ABSTRACT", "参考文献"):
        tex = tex.replace(
            f"\\chapter{{{title}}}",
            f"\\chapter*{{{title}}}\\addcontentsline{{toc}}{{chapter}}{{{title}}}",
            1,
        )
    tex = tex.replace(
        r"\setlength{\emergencystretch}{3em} % prevent overfull lines",
        r"\setlength{\emergencystretch}{3em} % prevent overfull lines\n\sloppy",
    )
    TEX_FILE.write_text(tex, encoding="utf-8")


if __name__ == "__main__":
    main()
