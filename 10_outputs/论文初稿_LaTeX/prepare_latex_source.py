#!/usr/bin/env python3
"""Create a clean, numbered LaTeX manuscript from the Markdown chapters."""

from __future__ import annotations

import csv
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = ROOT / "10_outputs/论文初稿_LaTeX"
COMBINED_MD = OUTPUT_DIR / "论文初稿_合并源稿.md"
TEX_FILE = OUTPUT_DIR / "全国中学生物理竞赛复赛试题的科学思维要求与教学启示.tex"
REFERENCE_MAPPING = ROOT / "09_quality/r01_candidate_references_mapping_v1.csv"
METADATA_FILE = OUTPUT_DIR / "华东师范大学论文元数据.json"
SOURCES = [
    ROOT / "08_manuscript/00_abstract_content_draft.md",
    ROOT / "08_manuscript/00_abstract_en_content_draft.md",
    ROOT / "08_manuscript/01_introduction.md",
    ROOT / "08_manuscript/02_theory.md",
    ROOT / "08_manuscript/03_methods.md",
    ROOT / "08_manuscript/04_results.md",
    ROOT / "08_manuscript/05_cases_and_diagnosis.md",
    ROOT / "08_manuscript/06_conclusion.md",
    ROOT / "08_manuscript/08_appendices.md",
    ROOT / "08_manuscript/07_candidate_references.md",
]


def load_reference_numbers() -> dict[str, str]:
    """Read the controlled source-to-number mapping used by the manuscript."""
    with REFERENCE_MAPPING.open(encoding="utf-8-sig", newline="") as handle:
        return {
            row["source_id"]: row["reference_number"]
            for row in csv.DictReader(handle)
        }


REFERENCE_NUMBERS = load_reference_numbers()


def load_thesis_metadata() -> dict[str, str]:
    """Load verified cover metadata while leaving unavailable fields empty."""
    with METADATA_FILE.open(encoding="utf-8") as handle:
        data = json.load(handle)
    return {key: str(value).strip() for key, value in data.items() if value is not None}


def nonempty_rows(metadata: dict[str, str], fields: list[tuple[str, str]]) -> str:
    rows = []
    for label, key in fields:
        value = metadata.get(key, "")
        if value:
            rows.append(rf"{label} & {value} \\")
    return "\n".join(rows)


def build_school_frontmatter(metadata: dict[str, str]) -> str:
    """Build Chinese and English inner covers from known metadata only."""
    title_cn = metadata["论文题目"]
    title_cn_tex = title_cn.replace("的科学思维", "的\\\\[0.45em]科学思维", 1)
    title_en = metadata["英文题目"]
    mode = metadata.get("培养方式", "")
    school_code = metadata.get("学校代码", "10269")
    chinese_rows = nonempty_rows(
        metadata,
        [
            ("院系名称：", "培养单位"),
            ("专业学位类别：", "专业学位类别"),
            ("专业学位领域：", "专业学位领域"),
            ("学位申请人：", "作者姓名"),
            ("指导教师：", "校内导师"),
        ],
    )
    english_rows = nonempty_rows(
        metadata,
        [
            ("Department/School:", "培养单位英文"),
            ("Category:", "专业学位类别英文"),
            ("Field:", "专业学位领域英文"),
            ("Candidate:", "作者姓名英文"),
            ("Supervisor:", "校内导师英文"),
        ],
    )
    completion_cn = metadata.get("完成时间", "")
    completion_en = metadata.get("完成时间英文", "")
    cohort = metadata.get("毕业届次", "")
    cohort_line = f"{cohort}届硕士专业学位研究生学位论文" if cohort else "硕士专业学位研究生学位论文"
    if mode:
        cohort_line += f"（{mode}）"
    return rf"""
\frontmatter
\begin{{titlepage}}
\thispagestyle{{empty}}
\begin{{flushleft}}
\zihao{{-4}} {cohort_line}
\hfill 学校代码：{school_code}
\end{{flushleft}}
\vspace*{{2.2cm}}
\begin{{center}}
{{\heiti\zihao{{1}}\bfseries 华东师范大学\par}}
\vspace{{0.7cm}}
{{\heiti\zihao{{2}}\bfseries 硕士专业学位论文\par}}
\vspace{{2.8cm}}
{{\songti\zihao{{1}}\bfseries {title_cn_tex}\par}}
\vfill
\renewcommand{{\arraystretch}}{{1.55}}
\begin{{tabular}}{{r l}}
{chinese_rows}
\end{{tabular}}
\vfill
{{\zihao{{-3}} {completion_cn}\par}}
\end{{center}}
\clearpage
\thispagestyle{{empty}}
\begin{{flushright}}
\zihao{{-4}} University code: {school_code}
\end{{flushright}}
\vspace*{{2.3cm}}
\begin{{center}}
{{\bfseries\fontsize{{21pt}}{{28pt}}\selectfont East China Normal University\par}}
\vspace{{0.7cm}}
{{\bfseries\fontsize{{18pt}}{{24pt}}\selectfont Master's Degree Thesis (Professional)\par}}
\vspace{{2.7cm}}
{{\bfseries\fontsize{{16pt}}{{23pt}}\selectfont {title_en}\par}}
\vfill
\renewcommand{{\arraystretch}}{{1.55}}
\begin{{tabular}}{{r l}}
{english_rows}
\end{{tabular}}
\vfill
{{\fontsize{{12pt}}{{16pt}}\selectfont {completion_en}\par}}
\end{{center}}
\end{{titlepage}}

\pagenumbering{{Roman}}
\setcounter{{page}}{{1}}
\pagestyle{{fancy}}
\zihao{{-4}}
\setstretch{{1.72}}
"""


def render_citation_markers(text: str) -> str:
    """Convert internal source markers into reader-facing numbered citations."""
    def replace(match: re.Match[str]) -> str:
        source_ids = [part.strip() for part in match.group(1).split("；", 1)[0].split("、")]
        missing = [source_id for source_id in source_ids if source_id not in REFERENCE_NUMBERS]
        if missing:
            raise ValueError(f"Missing reference number for: {', '.join(missing)}")
        numbers = ", ".join(REFERENCE_NUMBERS[source_id] for source_id in source_ids)
        return rf"\textsuperscript{{[{numbers}]}}"

    return re.sub(r"\[引文占位：([^\]]+)\]", replace, text)


def normalise_headings(text: str, source: Path) -> str:
    """Let LaTeX control hierarchy numbering rather than duplicate Markdown labels."""
    if source.name == "04_results.md":
        # Keep this provenance list in the editable source, not in the reader-facing thesis.
        text = text.split("## 数据来源", 1)[0]
    if source.name == "07_candidate_references.md":
        text = text.split("## 使用边界", 1)[0]
        text = re.sub(r"(?ms)^>\s.*?(?=\n\n)", "", text, count=1)
        text = text.replace("# 参考文献（候选工作稿）", "# 参考文献")
        text = re.sub(r"(?m)^(\[\d+\])", r"\n\1", text)
        text = re.sub(r"(https?://[^\s]+)", r"<\1>", text)
    text = re.sub(r"^#\s+第[一二三四五六七八九十]+章\s+(.+)$", r"# \1", text, flags=re.MULTILINE)
    text = re.sub(r"^(#{2,3})\s+\d+(?:\.\d+)+\s+(.+)$", r"\1 \2", text, flags=re.MULTILINE)
    # The manuscript supplies complete Chinese captions in the paragraph after each image.
    # Empty alt text prevents Pandoc from emitting a second automatic figure caption.
    text = re.sub(r"!\[[^\]]*\]\(([^)]+)\)", r"![](\1)", text)
    return render_citation_markers(text)


def main() -> None:
    metadata = load_thesis_metadata()
    combined = "\n\n".join(normalise_headings(path.read_text(encoding="utf-8"), path) for path in SOURCES)
    COMBINED_MD.write_text(combined.rstrip() + "\n", encoding="utf-8")
    command = [
        "pandoc", "--from", "markdown", "--to", "latex", "--standalone", "--toc", "--number-sections",
        "--top-level-division=chapter", "--metadata", f"title={metadata['论文题目']}",
        "--metadata", f"author={metadata['作者姓名']}", "--metadata", "date=", "-V", "documentclass=ctexbook",
        "-V", "classoption=a4paper,twoside,openany", "-V", "CJKmainfont=Songti SC",
        "-V", "CJKsansfont=Hiragino Sans GB", "-V", "geometry:top=2.54cm",
        "-V", "geometry:bottom=2.54cm", "-V", "geometry:inner=3.17cm",
        "-V", "geometry:outer=2.54cm", "-V", "fontsize=12pt", "-V", "linestretch=1.72",
        "-V", "colorlinks=true",
        "-V", "linkcolor=black", "-V", "urlcolor=black", "-o", str(TEX_FILE), str(COMBINED_MD),
    ]
    subprocess.run(command, check=True)
    tex = TEX_FILE.read_text(encoding="utf-8")
    for title in ("摘要", "ABSTRACT", "参考文献"):
        chapter_heading = f"\\chapter*{{{title}}}\\addcontentsline{{toc}}{{chapter}}{{{title}}}"
        if title == "参考文献":
            chapter_heading += (
                "\\markboth{参考文献}{参考文献}"
                "\\begingroup"
                "\\setlength{\\leftskip}{2em}"
                "\\setlength{\\parindent}{-2em}"
                "\\setlength{\\parskip}{3pt}"
            )
        elif title == "ABSTRACT":
            chapter_heading += "\\begingroup\\setstretch{1.56}"
        tex = tex.replace(
            f"\\chapter{{{title}}}",
            chapter_heading,
            1,
        )
    tex, front_count = re.subn(
        r"\\frontmatter.*?\\mainmatter\s*",
        lambda _: build_school_frontmatter(metadata),
        tex,
        count=1,
        flags=re.DOTALL,
    )
    if front_count != 1:
        raise RuntimeError("Could not replace Pandoc front matter")
    contents_block = r"""
\endgroup
\clearpage
\setcounter{tocdepth}{2}
\tableofcontents
\clearpage
\phantomsection
\addcontentsline{toc}{chapter}{插图清单}
\listoffigures
\clearpage
\phantomsection
\addcontentsline{toc}{chapter}{附表清单}
\listoftables
\mainmatter
\zihao{-4}
\setstretch{1.72}
"""
    tex = tex.replace(r"\chapter{绪论}", contents_block + "\n\\chapter{绪论}", 1)
    tex = tex.replace(
        r"\setlength{\emergencystretch}{3em} % prevent overfull lines",
        "\\setlength{\\emergencystretch}{3em} % prevent overfull lines\n"
        "\\sloppy\n"
        "\\setlength{\\parindent}{2em}\n"
        "\\setlength{\\parskip}{0pt}\n"
        "\\renewcommand{\\arraystretch}{1.22}\n"
        "\\setlength{\\tabcolsep}{4.8pt}\n"
        "\\usepackage{tikz}\n"
        "\\usetikzlibrary{arrows.meta,calc,decorations.pathreplacing,positioning,fit,matrix}\n"
        "\\usepackage{colortbl}\n"
        "\\usepackage{caption}\n"
        "\\usepackage{etoolbox}\n"
        "\\usepackage{float}\n"
        "\\usepackage{flafter}\n"
        "\\usepackage{fancyhdr}\n"
        "\\setlength{\\headheight}{15pt}\n"
        "\\pagestyle{fancy}\n"
        "\\fancyhf{}\n"
        "\\fancyhead[C]{\\zihao{-5} 华东师范大学硕士专业学位论文}\n"
        "\\fancyfoot[LE,RO]{\\thepage}\n"
        "\\renewcommand{\\headrulewidth}{0.4pt}\n"
        "\\fancypagestyle{plain}{\\fancyhf{}"
        "\\fancyhead[C]{\\zihao{-5} 华东师范大学硕士专业学位论文}"
        "\\fancyfoot[LE,RO]{\\thepage}\\renewcommand{\\headrulewidth}{0.4pt}}\n"
        "\\definecolor{ThesisNavy}{HTML}{244A64}\n"
        "\\definecolor{ThesisBlue}{HTML}{4E7896}\n"
        "\\definecolor{ThesisTeal}{HTML}{4F8A83}\n"
        "\\definecolor{ThesisRust}{HTML}{B7654A}\n"
        "\\definecolor{ThesisGold}{HTML}{C49A45}\n"
        "\\definecolor{ThesisLavender}{HTML}{80728F}\n"
        "\\definecolor{ThesisInk}{HTML}{25333C}\n"
        "\\definecolor{ThesisGrid}{HTML}{D8E0E5}\n"
        "\\definecolor{ThesisPale}{HTML}{EDF3F6}\n"
        "\\tikzset{every picture/.style={line cap=round,line join=round},"
        "thesisbox/.style={draw=ThesisNavy,line width=.65pt,rounded corners=2pt,"
        "fill=ThesisPale,text=ThesisInk,align=center,inner xsep=8pt,inner ysep=5pt},"
        "thesisarrow/.style={-{Stealth[length=2.2mm]},line width=.75pt,draw=ThesisNavy}}\n"
        "\\captionsetup{font=small,labelfont=bf,labelsep=quad,skip=6pt}\n"
        "\\renewcommand{\\thefigure}{\\thechapter-\\arabic{figure}}\n"
        "\\renewcommand{\\thetable}{\\thechapter-\\arabic{table}}\n"
        "\\setlength{\\LTpre}{6pt}\n"
        "\\setlength{\\LTpost}{9pt}\n"
        "\\AtBeginEnvironment{longtable}{\\small\\arrayrulecolor{ThesisNavy!55}}\n"
        "\\ctexset{chapter={format=\\centering\\heiti\\bfseries\\zihao{3},"
        "beforeskip=18pt,afterskip=20pt},"
        "section={format=\\heiti\\bfseries\\zihao{4},beforeskip=16pt,afterskip=10pt},"
        "subsection={format=\\heiti\\bfseries\\zihao{-4},beforeskip=12pt,afterskip=7pt}}\n"
        "\\let\\cleardoublepage\\clearpage\n",
    )
    tex = tex.replace(
        r"\Gscale@div\@tempb{\linewidth}{\wd\pandoc@box}%",
        r"\Gscale@div\@tempb{.86\linewidth}{\wd\pandoc@box}%",
    )
    tex = tex.replace(r"\pandocbounded{", r"\noindent\pandocbounded{")
    tex = tex.replace(
        "\\toprule\\noalign{}\n",
        "\\toprule\\noalign{}\n\\rowcolor{ThesisPale}\n",
    )
    tex = tex.replace(r"\end{document}", "\\endgroup\n\\end{document}", 1)
    TEX_FILE.write_text(tex, encoding="utf-8")


if __name__ == "__main__":
    main()
