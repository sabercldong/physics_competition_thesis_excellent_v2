#!/usr/bin/env python3
"""Render supplemental TikZ figures used by the Markdown reading copies."""

from pathlib import Path
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parent
TIKZ_DIR = ROOT / "tikz"
ASSET_DIR = ROOT / "markdown" / "assets"

FIGURES = {
    "CPHO36-Q01-solution-forces": "CPHO36-Q01-solution-forces.tex",
    "CPHO36-Q02-solution-geometry": "CPHO36-Q02-solution-geometry.tex",
    "CPHO36-Q02-solution-forces": "CPHO36-Q02-solution-forces.tex",
    "CPHO36-Q05-solution-figures": "CPHO36-Q05-solution-figures.tex",
    "CPHO37-Q06-solution-sagnac": "CPHO37-Q06-solution-sagnac.tex",
    "CPHO38-Q01-solution-figures": "CPHO38-Q01-solution-figures.tex",
}


def main() -> None:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp_name:
        tmp_dir = Path(tmp_name)
        for stem, source_name in FIGURES.items():
            wrapper = tmp_dir / f"{stem}.tex"
            wrapper.write_text(
                "\n".join(
                    [
                        r"\documentclass[tikz,border=4pt]{standalone}",
                        r"\usepackage{xeCJK}",
                        r"\setCJKmainfont{Songti SC}",
                        r"\usetikzlibrary{arrows.meta,calc,positioning}",
                        r"\begin{document}",
                        rf"\input{{{(TIKZ_DIR / source_name).as_posix()}}}",
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


if __name__ == "__main__":
    main()
