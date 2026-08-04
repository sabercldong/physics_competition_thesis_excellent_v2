#!/usr/bin/env python3
"""从当前论文阅读版生成华东师大2025格式装配版LaTeX源文件。"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "10_outputs/论文初稿_LaTeX/全国中学生物理竞赛复赛试题的科学思维要求与教学启示.tex"
OUTPUT_DIR = ROOT / "10_outputs/华东师大2025格式论文"
OUTPUT = OUTPUT_DIR / "全国中学生物理竞赛复赛试题的科学思维要求与教学启示.tex"

OLD_TITLE = "全国中学生物理竞赛复赛试题的科学思维要求与教学启示"
TITLE = "全国中学生物理竞赛复赛试题的科学思维要求与教学启示"
OLD_TITLE_EN = (
    "Scientific-Thinking Requirements and Teaching Implications of Second-Round "
    "Problems in the National High School Physics Competition"
)
TITLE_EN = (
    "Scientific-Thinking Requirements and Teaching Implications of Second-Round "
    "Problems in the National High School Physics Competition"
)


def frontmatter() -> str:
    """Return the four-page professional-degree front matter plus pagination setup."""
    return rf"""\frontmatter
\begin{{titlepage}}
\thispagestyle{{empty}}
\zihao{{-4}}
\noindent\makebox[\textwidth][l]{{\rule{{1.8cm}}{{0.4pt}}届硕士专业学位研究生学位论文}}

\vspace{{1.1cm}}
\noindent
\begin{{tabular*}}{{\textwidth}}{{@{{}}l@{{\extracolsep{{\fill}}}}l@{{}}}}
分\ 类\ 号：\underline{{\makebox[4.0cm][l]{{}}}} & 学校代码：\quad 10269 \\
密\qquad 级：\underline{{\makebox[4.0cm][l]{{}}}} & 学\qquad 号：\underline{{\makebox[4.0cm][l]{{}}}}
\end{{tabular*}}

\vspace*{{1.5cm}}
\begin{{center}}
{{\bfseries\fontsize{{21pt}}{{28pt}}\selectfont East China Normal University\par}}
\vspace{{0.55cm}}
{{\heiti\zihao{{2}}\bfseries 硕士专业学位论文\par}}
{{\bfseries\fontsize{{14pt}}{{20pt}}\selectfont Master's Degree Thesis (Professional)\par}}

\vspace{{2.4cm}}
{{\songti\zihao{{1}}\bfseries 全国中学生物理竞赛复赛试题的\\[0.45em]科学思维要求与教学启示\par}}

\vfill
\renewcommand{{\arraystretch}}{{1.65}}
\begin{{tabular}}{{r@{{\quad}}l}}
院\qquad 系： & \underline{{\makebox[8.2cm][l]{{}}}} \\
专业学位类别： & \underline{{\makebox[8.2cm][l]{{}}}} \\
专业学位领域： & \underline{{\makebox[8.2cm][l]{{}}}} \\
学位申请人： & 董兴习 \\
指\ 导\ 教\ 师： & \underline{{\makebox[8.2cm][l]{{}}}}
\end{{tabular}}

\vfill
{{\zihao{{-3}}\rule{{1.4cm}}{{0.4pt}}年\rule{{1.0cm}}{{0.4pt}}月\par}}
\end{{center}}
\end{{titlepage}}

\begin{{titlepage}}
\thispagestyle{{empty}}
\noindent\makebox[\textwidth][l]{{Thesis for Master's Degree (Professional) in \rule{{1.8cm}}{{0.4pt}}}}

\vspace{{1.1cm}}
\begin{{flushright}}
University code: 10269\\[0.5em]
Student ID: \rule{{4.0cm}}{{0.4pt}}
\end{{flushright}}

\vspace*{{1.8cm}}
\begin{{center}}
{{\bfseries\fontsize{{21pt}}{{28pt}}\selectfont East China Normal University\par}}

\vspace{{2.3cm}}
\begin{{minipage}}{{0.88\textwidth}}
\centering
{{\bfseries\fontsize{{16pt}}{{23pt}}\selectfont {TITLE_EN}\par}}
\end{{minipage}}

\vfill
\renewcommand{{\arraystretch}}{{1.65}}
\begin{{tabular}}{{r@{{\quad}}l}}
Department/School: & \underline{{\makebox[7.2cm][l]{{}}}} \\
Category: & \underline{{\makebox[7.2cm][l]{{}}}} \\
Field: & \underline{{\makebox[7.2cm][l]{{}}}} \\
Candidate: & Dong Xingxi \\
Supervisor: & \underline{{\makebox[7.2cm][l]{{}}}}
\end{{tabular}}

\vfill
{{\fontsize{{12pt}}{{16pt}}\selectfont \rule{{1.4cm}}{{0.4pt}}, \rule{{1.8cm}}{{0.4pt}}\par}}
\end{{center}}
\end{{titlepage}}

\clearpage
\thispagestyle{{empty}}
\begin{{center}}
{{\heiti\zihao{{3}}\bfseries 华东师范大学学位论文原创性声明\par}}
\end{{center}}
\vspace{{0.8cm}}
\begingroup
\zihao{{-4}}
\setstretch{{1.65}}
\setlength{{\parindent}}{{2em}}
郑重声明：本人呈交的学位论文《{TITLE}》，是在华东师范大学攻读硕士学位期间，在导师的指导下进行的研究工作及取得的研究成果。除文中已经注明引用的内容外，本论文不包含其他个人已经发表或撰写过的研究成果。对本文的研究做出重要贡献的个人和集体，均已在文中作了明确说明并表示谢意。

\vspace{{0.8cm}}
\noindent 作者签名：\rule{{4.0cm}}{{0.4pt}}\hfill 日期：\rule{{1.0cm}}{{0.4pt}}年\rule{{0.8cm}}{{0.4pt}}月\rule{{0.8cm}}{{0.4pt}}日

\vspace{{1.4cm}}
\begin{{center}}
{{\heiti\zihao{{3}}\bfseries 华东师范大学学位论文著作权使用声明\par}}
\end{{center}}
\vspace{{0.6cm}}

《{TITLE}》系本人在华东师范大学攻读学位期间在导师指导下完成的硕士学位论文，本论文的著作权归本人所有。本人同意华东师范大学根据相关规定保留和使用此学位论文，并向主管部门和学校指定的相关机构送交学位论文的印刷版和电子版；允许学位论文进入华东师范大学图书馆及数据库被查阅、借阅；同意学校将学位论文加入全国博士、硕士学位论文共建单位数据库进行检索，将学位论文的标题和摘要汇编出版，采用影印、缩印或者其他方式合理复制学位论文。

本学位论文属于（请勾选）

（\quad）1. 经华东师范大学相关部门审查核定的“内部”或“涉密”学位论文，于\rule{{1.0cm}}{{0.4pt}}年\rule{{0.8cm}}{{0.4pt}}月\rule{{0.8cm}}{{0.4pt}}日解密，解密后适用上述授权。

（\quad）2. 不保密，适用上述授权。

\vspace{{0.6cm}}
\noindent 导师签名：\rule{{3.6cm}}{{0.4pt}}\hfill 作者签名：\rule{{3.6cm}}{{0.4pt}}

\vspace{{0.4cm}}
\hfill 日期：\rule{{1.0cm}}{{0.4pt}}年\rule{{0.8cm}}{{0.4pt}}月\rule{{0.8cm}}{{0.4pt}}日

\vfill
{{\zihao{{5}} *“涉密”学位论文应是已经华东师范大学学位管理办公室或保密委员会审定过的学位论文（需附获批的《华东师范大学研究生申请学位论文“涉密”审批表》方为有效），未经上述部门审定的学位论文均为公开学位论文。此声明栏不填写的，默认为公开学位论文，均适用上述授权。\par}}
\endgroup

\clearpage
\thispagestyle{{empty}}
\begin{{center}}
{{\heiti\zihao{{3}}\bfseries 《{TITLE}》硕士学位论文答辩委员会成员名单\par}}
\end{{center}}
\vspace{{1.1cm}}
\renewcommand{{\arraystretch}}{{2.0}}
\begin{{center}}
\begin{{tabular}}{{|p{{2.5cm}}|p{{2.6cm}}|p{{5.6cm}}|p{{2.3cm}}|}}
\hline
\centering 姓名 & \centering 职称 & \centering 单位 & \centering\arraybackslash 备注 \\
\hline
 & & & 主席 \\
\hline
 & & & \\
\hline
 & & & \\
\hline
 & & & \\
\hline
 & & & \\
\hline
\end{{tabular}}
\end{{center}}

\clearpage
\pagenumbering{{Roman}}
\setcounter{{page}}{{1}}
\pagestyle{{fancy}}
\zihao{{-4}}
\setstretch{{1.72}}
"""


def reorder_backmatter(tex: str) -> str:
    """Place references before appendices and reserve the official afterword page."""
    appendix_start = tex.index("\\appendix")
    references_start = tex.index("\\chapter*{参考文献}", appendix_start)
    backmatter_start = tex.index("\\backmatter", references_start)
    document_end = tex.index("\\end{document}", backmatter_start)

    prefix = tex[:appendix_start]
    appendix = tex[appendix_start:references_start].rstrip()
    references = tex[references_start:backmatter_start].rstrip()

    afterword = r"""
\backmatter
\clearpage
\chapter*{后记}\addcontentsline{toc}{chapter}{后记}\markboth{后记}{后记}
\thispagestyle{fancy}
\vspace*{1cm}
"""
    return (
        prefix.rstrip()
        + "\n\n"
        + references
        + "\n\\endgroup\n\n"
        + appendix
        + "\n"
        + afterword
        + "\n\\end{document}\n"
    )


def replace_english_abstract(tex: str) -> str:
    """Keep the English abstract and its keywords on one formal front-matter page."""
    abstract_start = tex.index("\\chapter*{ABSTRACT}")
    abstract_end = tex.index("\\endgroup", abstract_start)
    abstract = r"""\chapter*{ABSTRACT}\addcontentsline{toc}{chapter}{ABSTRACT}\begingroup\setstretch{1.50}\label{abstract}

This study investigates the scientific-thinking requirements of the
theoretical problems from the 35th to the 42nd editions of the National
Physics Competition for High School Students in China and derives
implications for instructional design. Subquestions with independent
response goals produced 221 analytical units and 884 coding records.
Each record retained evidence from the problem statement and reference
solution, source locations, and the rationale for excluding adjacent
levels. Two anonymous raters independently coded a stratified sample of
75 units. Agreement on dimension presence was 89.67\%, with Cohen's
Kappa of 0.790; the quadratic weighted Kappa for the five-category
labels was 0.752. The 146 records on which the baseline coding and the
two raters did not fully agree were re-examined against the full source texts before the formal
analysis table was established. Model construction, scientific
reasoning, scientific argumentation, and questioning and innovation
occurred in 192, 221, 25, and 2 units, respectively, accounting for
86.88\%, 100.00\%, 11.31\%, and 0.90\% of the sample. Within the units
where each dimension occurred, the L1/L2/L3 counts were 28/68/96 for
model construction, 27/68/126 for scientific reasoning, and 12/11/2
for scientific argumentation. Both questioning-and-innovation cases
were L2, and no L4 case occurred. Reweighting by original subquestion
and major problem changed the four rates by no more than 2.41
percentage points and did not alter their order. Six main cases and a
paired comparison of adjacent Mossbauer-effect subquestions revealed
condition-relation chains, state classification, approximation-based
modeling, same-object comparison, multi-object constraints, threshold
judgment, and measurement-scheme design. These results informed a
task-structure-to-feedback design chain, a 45-minute lesson, and a
four-dimension artifact rubric, providing traceable support for
competition-problem research and instructional design.

Keywords: physics competition; scientific thinking; content analysis;
task cognitive requirements; instructional design

"""
    return tex[:abstract_start] + abstract + tex[abstract_end:]


def main() -> None:
    tex = SOURCE.read_text(encoding="utf-8")
    tex = tex.replace(OLD_TITLE, TITLE)
    tex = tex.replace(OLD_TITLE_EN, TITLE_EN)

    front_start = tex.index("\\frontmatter")
    abstract_start = tex.index("\\chapter*{摘要}", front_start)
    tex = tex[:front_start] + frontmatter() + tex[abstract_start:]

    tex = tex.replace(
        "Cohen's\n\\(\\kappa\\)为0.790；五分类标签的加权\\(\\kappa\\)为0.752。",
        "Cohen's Kappa系数为0.790；五分类标签的加权Kappa系数为0.752。",
    )
    tex = tex.replace(
        "Their agreement was 89.67\\% for dimension presence (Cohen's\n"
        "\\(\\kappa=0.790\\)), and the weighted \\(\\kappa\\) for the five-category\n"
        "labels was 0.752.",
        "Their agreement was 89.67\\% for dimension presence, with a Cohen's Kappa\n"
        "coefficient of 0.790; the quadratic weighted Kappa coefficient for the\n"
        "five-category labels was 0.752.",
    )
    tex = replace_english_abstract(tex)

    tex = tex.replace(
        "基于SOLO分类理论的全国中学生物理竞赛复赛理论试题研究{[}D{]}.\n华中师范大学, 2020.",
        "基于SOLO分类理论的全国中学生物理竞赛复赛理论试题研究{[}D{]}.\n武汉：华中师范大学, 2020.",
    )
    tex = tex.replace(
        "唐路. 全国中学生物理竞赛试题研究{[}D{]}. 湖南师范大学, 2020.",
        "唐路. 全国中学生物理竞赛试题研究{[}D{]}. 长沙：湖南师范大学, 2020.",
    )
    tex = tex.replace(
        "基于数理核心素养的全国中学生物理竞赛预赛试题分析研究{[}D{]}.\n华中师范大学, 2020.",
        "基于数理核心素养的全国中学生物理竞赛预赛试题分析研究{[}D{]}.\n武汉：华中师范大学, 2020.",
    )
    tex = tex.replace(
        "基于综合难度模型的全国中学生物理竞赛复赛理论试题研究{[}D{]}.\n湖南师范大学, 2022.",
        "基于综合难度模型的全国中学生物理竞赛复赛理论试题研究{[}D{]}.\n长沙：湖南师范大学, 2022.",
    )

    tex = reorder_backmatter(tex)
    OUTPUT.write_text(tex, encoding="utf-8")


if __name__ == "__main__":
    main()
