#!/usr/bin/env python3
"""Render every current TikZ figure and build a Markdown figure catalogue."""

from pathlib import Path
import re
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parent
TIKZ_DIR = ROOT / "tikz"
ASSET_DIR = ROOT / "markdown" / "assets"

QUESTION_DIR = ROOT / "questions"


def question_id(stem: str) -> str:
    match = re.match(r"(CPHO\d{2}-Q\d{2})", stem)
    if not match:
        raise ValueError(f"Unrecognised figure filename: {stem}")
    return match.group(1)


def question_title(question: str) -> str:
    source = QUESTION_DIR / f"{question}.tex"
    text = source.read_text(encoding="utf-8")
    match = re.search(r"\\section\{([^}]+)\}", text)
    return match.group(1) if match else question


def write_catalogue(stems: list[str]) -> None:
    groups: dict[str, list[str]] = {}
    for stem in stems:
        groups.setdefault(question_id(stem), []).append(stem)
    lines = [
        "# 已完成题目的TikZ图件总览",
        "",
        "本页集中展示当前已完成图册条目的原题图和解析辅助图。图片均由 tikz 目录中的可编辑源文件生成。",
        "",
    ]
    for question in sorted(groups):
        lines.extend([f"## {question_title(question)}", ""])
        for stem in sorted(groups[question]):
            kind = "解析辅助图" if "-solution-" in stem else "原题图"
            lines.extend(
                [
                    f"**{kind}：** {stem}.tex",
                    "",
                    f"![{stem}](assets/{stem}.png)",
                    "",
                ]
            )
    (ROOT / "markdown" / "图件总览.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def main() -> None:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp_name:
        tmp_dir = Path(tmp_name)
        sources = sorted(TIKZ_DIR.glob("CPHO*.tex"))
        for source in sources:
            stem = source.stem
            wrapper = tmp_dir / f"{stem}.tex"
            wrapper.write_text(
                "\n".join(
                    [
                        r"\documentclass[tikz,border=4pt]{standalone}",
                        r"\usepackage{xeCJK}",
                        r"\setCJKmainfont{Songti SC}",
                        r"\usetikzlibrary{arrows.meta,calc,decorations.pathmorphing,positioning,shapes.symbols}",
                        r"\begin{document}",
                        rf"\input{{{source.as_posix()}}}",
                        r"\end{document}",
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            subprocess.run(
                ["xelatex", "-interaction=nonstopmode", "-halt-on-error", wrapper.name],
                cwd=tmp_dir,
                check=True,
                stdout=subprocess.DEVNULL,
            )
            pdf_path = tmp_dir / f"{stem}.pdf"
            prefix = tmp_dir / stem
            subprocess.run(
                ["pdftocairo", "-singlefile", "-png", "-r", "180", str(pdf_path), str(prefix)],
                check=True,
            )
            shutil.copyfile(prefix.with_suffix(".png"), ASSET_DIR / f"{stem}.png")
    write_catalogue([source.stem for source in sources])


if __name__ == "__main__":
    main()
