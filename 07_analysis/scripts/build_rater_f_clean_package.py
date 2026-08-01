#!/usr/bin/env python3
"""Build a self-contained RATER-F package from the curated LaTeX atlas."""

from __future__ import annotations

import csv
import hashlib
import re
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ATLAS = ROOT / "10_outputs/全量复赛题干解析与TikZ图册"
INDEX_SOURCE = (
    ROOT
    / "07_analysis/data/v3_independent_validation/handoff_RATER-C"
    / "独立盲评材料索引_75单元.csv"
)
DOWNLOADS = Path.home() / "Downloads"
PACKAGE_NAME = "RATER-F真实独立盲评材料包_清洗版_20260801"
PACKAGE = DOWNLOADS / PACKAGE_NAME
ZIP_PATH = DOWNLOADS / f"{PACKAGE_NAME}.zip"

DIMENSIONS = ("模型建构", "科学推理", "科学论证", "质疑创新")
REVIEW_FIELDS = (
    "independent_reviewer_id",
    "review_date",
    "review_present",
    "review_level",
    "question_evidence_quote",
    "solution_evidence_quote",
    "evidence_location",
    "adjacent_level_exclusion",
    "confidence",
    "reviewer_statement",
)
PRIVATE_USE = re.compile(r"[\ue000-\uf8ff]")
FIGURE_ENV = re.compile(r"\\begin\{figure\}.*?\\end\{figure\}", re.DOTALL)

PDF_SOURCES = (
    ("03_corpus/raw_papers/cpho_35_2018_fusai_paper_solution_candidate.pdf", "第35届复赛试题与参考解答_原始PDF.pdf"),
    ("03_corpus/raw_papers/cpho_36_2019_fusai_paper_solution_candidate.pdf", "第36届复赛试题与参考解答_原始PDF.pdf"),
    ("03_corpus/raw_papers/cpho_37_2020_fusai_paper_solution_candidate.pdf", "第37届复赛试题与参考解答_原始PDF.pdf"),
    ("03_corpus/raw_papers/cpho_38_2021_fusai_paper_solution_candidate.pdf", "第38届复赛试题与参考解答_原始PDF.pdf"),
    ("03_corpus/raw_papers/cpho_39_2022_fusai_paper_solution_candidate.pdf", "第39届复赛试题与参考解答_原始PDF.pdf"),
    ("03_corpus/raw_papers/cpho_40_2023_fusai_paper_solution_candidate.pdf", "第40届复赛试题与参考解答_原始PDF.pdf"),
    ("03_corpus/raw_papers/cpho_41_2024_fusai_paper_candidate.pdf", "第41届复赛试题_原始PDF.pdf"),
    ("03_corpus/raw_solutions/cpho_41_2024_fusai_solution_candidate.pdf", "第41届复赛参考解答_原始PDF.pdf"),
    ("03_corpus/raw_papers/cpho_42_2025_fusai_paper_candidate.pdf", "第42届复赛试题_原始PDF.pdf"),
    ("03_corpus/raw_solutions/cpho_42_2025_fusai_solution_candidate.pdf", "第42届复赛参考解答_原始PDF.pdf"),
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def question_id(item_id: str) -> str:
    match = re.match(r"^(CPHO\d{2}-Q\d{2})", item_id)
    if not match:
        raise ValueError(f"无法从item_id提取大题编号：{item_id}")
    return match.group(1)


def subquestion_anchor_candidates(value: str) -> tuple[str, ...]:
    if "-" in value:
        major, minor = value.split("-", 1)
        return (f"（{major}）（{minor}）", f"（{major}）{minor}", f"{major}-{minor}")
    return (f"（{value}）", f"第{value}问")


def clean_question_tex(text: str, qid: str) -> str:
    if qid != "CPHO40-Q08":
        text = re.sub(
            r"\n\\subsection\{(?:图件与)?转写依据\}.*\Z",
            "\n",
            text,
            flags=re.DOTALL,
        )
        text = re.sub(
            r"\n\\par\\smallskip\\noindent\\textbf\{(?:图件与)?转写依据[^}]*\}.*\Z",
            "\n",
            text,
            flags=re.DOTALL,
        )
    return text.rstrip() + "\n"


def render_tikz(source: Path, output: Path) -> None:
    with tempfile.TemporaryDirectory() as tmp_name:
        tmp = Path(tmp_name)
        wrapper = tmp / f"{source.stem}.tex"
        wrapper.write_text(
            "\n".join(
                [
                    r"\documentclass[tikz,border=4pt]{standalone}",
                    r"\usepackage{amsmath}",
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
            cwd=tmp,
            check=True,
            stdout=subprocess.DEVNULL,
        )
        subprocess.run(
            [
                "pdftocairo",
                "-singlefile",
                "-png",
                "-r",
                "180",
                str(tmp / f"{source.stem}.pdf"),
                str(tmp / source.stem),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
        )
        output.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(tmp / f"{source.stem}.png", output)


def markdown_from_tex(tex: str, qid: str, image_dir: Path) -> str:
    figures: list[tuple[str, list[str]]] = []

    def replace_figure(match: re.Match[str]) -> str:
        names = re.findall(r"\\input\{tikz/([^}]+)\}", match.group(0))
        token = f"FIGURETOKEN{len(figures):03d}"
        figures.append((token, names))
        return f"\n\n{token}\n\n"

    converted_source = FIGURE_ENV.sub(replace_figure, tex)
    converted_source = re.sub(r"\\ref\{[^}]+\}", "", converted_source)
    with tempfile.TemporaryDirectory() as tmp_name:
        source = Path(tmp_name) / f"{qid}.tex"
        source.write_text(converted_source, encoding="utf-8")
        result = subprocess.run(
            [
                "pandoc",
                "-f",
                "latex",
                "-t",
                "markdown+tex_math_dollars",
                "--wrap=none",
                str(source),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
    markdown = result.stdout
    for token, names in figures:
        images = []
        for name in names:
            stem = Path(name).stem
            images.append(f"![{stem}](图件/{stem}.png)")
        markdown = markdown.replace(token, "\n\n".join(images))
    header = (
        "> 本文件由项目已校订的LaTeX题干、参考解答和TikZ图件生成。"
        "评分时以本文件为主要阅读文本；需核对原始措辞时查看包内对应届次原始PDF。\n\n"
    )
    return header + markdown.strip() + "\n"


def build_blank_tables(index_rows: list[dict[str, str]]) -> None:
    normalized_index: list[dict[str, str]] = []
    blind_rows: list[dict[str, str]] = []
    progress_rows: list[dict[str, str]] = []
    for index_row in index_rows:
        qid = question_id(index_row["item_id"])
        source_name = f"{qid}.md"
        normalized = dict(index_row)
        normalized["source_text_file"] = source_name
        normalized["solution_text_file"] = source_name
        normalized_index.append(normalized)
        progress_rows.append(
            {
                "blind_unit_no": normalized["blind_unit_no"],
                "item_id": normalized["item_id"],
                "source_text_file": source_name,
                "题目与文件核对": "",
                "题干完整阅读": "",
                "参考解答完整阅读": "",
                "四维编码完成": "",
                "本单元自检完成": "",
                "完成日期": "",
                "备注": "",
            }
        )
        unit_number = int(normalized["blind_unit_no"].split("-")[1])
        for dimension_number, dimension in enumerate(DIMENSIONS, start=1):
            row = {
                "blind_row_id": f"BR-{unit_number:03d}-{dimension_number}",
                "blind_unit_no": normalized["blind_unit_no"],
                "item_id": normalized["item_id"],
                "competition_no": normalized["competition_no"],
                "year": normalized["year"],
                "question_no": normalized["question_no"],
                "subquestion_no": normalized["subquestion_no"],
                "dimension": dimension,
                "source_text_file": source_name,
                "solution_text_file": source_name,
            }
            row.update({field: "" for field in REVIEW_FIELDS})
            blind_rows.append(row)

    write_csv(PACKAGE / "独立盲评材料索引_75单元.csv", normalized_index, list(normalized_index[0]))
    write_csv(
        PACKAGE / "第35至42届独立盲评编码表_RATER-F_空白300行.csv",
        blind_rows,
        list(blind_rows[0]),
    )
    write_csv(PACKAGE / "05_75单元编码进度表.csv", progress_rows, list(progress_rows[0]))


def write_instructions() -> None:
    (PACKAGE / "00_开始前必读.md").write_text(
        """# RATER-F开始前必读

本材料包用于一名新的真实评分者完成独立盲评。包内没有既有标签、作者决定或统计结果。

请按以下顺序工作：

1. 阅读 `01_RATER-F评分者操作指令.md`；
2. 阅读 `编码规则` 中的编码手册和决策矩阵；
3. 按 `独立盲评材料索引_75单元.csv` 的顺序完成75个分析单元；
4. 主要阅读 `清晰排版题目与解答` 中的MD或43题PDF；
5. 图形、公式或原始措辞需要确认时，查看 `原始试卷证据` 中对应届次PDF；
6. 每完成一个单元，同步填写进度表；
7. 完成300行后执行自检，并填写独立性声明。

不要接收或查看论文结果、既有评分表、作者复核表或任何对照标签。
""",
        encoding="utf-8",
    )
    (PACKAGE / "01_RATER-F评分者操作指令.md").write_text(
        """# RATER-F真实独立盲评操作指令

## 一、评分者资格

评分者必须是真实存在、此前未参与本项目编码或裁决的人，并具备高中物理教学、物理竞赛教学或物理教育研究经验。开始前不得查看论文统计、既有标签或其他评分者结果。

## 二、逐单元工作流程

1. 按 `blind_unit_no` 从BU-001依次处理到BU-075，不得排序或跳行批量填写。
2. 核对 `item_id`、小问号和 `source_text_file`，打开同名MD。
3. 完整阅读题干、对应参考解答和全部TikZ图，再处理该分析单元。
4. 连续填写该单元的模型建构、科学推理、科学论证和质疑创新四行。
5. 题干引文和解答引文必须从本行指定MD逐字复制，不得改写、缩写、使用省略号或从其他题目复制。
6. `evidence_location` 必须写出MD文件名、小问号，以及段落、公式或图件锚点。
7. `adjacent_level_exclusion` 必须结合本题说明为何不取相邻等级；维度未出现时，要写明缺少哪项判定条件。
8. `confidence` 按实际把握填写高、中或低，不得机械地全部填写为高。
9. 清晰排版材料与原始PDF若出现实质差异，暂停该单元并在备注中记录，不得自行猜测。
10. 每完成一个单元，更新 `05_75单元编码进度表.csv`。

## 三、编码表填写范围

前10列是固定字段，不得修改。只填写后10列：评分者代号、日期、维度是否出现、等级、题干引文、解答引文、证据位置、相邻等级排除理由、置信度和逐行声明。

维度未出现时填写 `否/未出现`；维度出现时填写 `是/L1`、`是/L2`、`是/L3`或`是/L4`。逐行声明统一为：`本行为本人在未查看既有编码与统计结果的条件下独立判断。`

## 四、禁止事项

- 不得使用模板句批量填充引文或理由；
- 不得用脚本或自动生成方式代替逐题判断；
- 不得查看其他评分者文件或询问作者当前标签；
- 不得改动固定字段、增删行或重新排序；
- 不得只看题干而不看参考解答和题图。

## 五、交回材料

交回完成的300行编码表、75单元进度表、匿名独立性声明，以及私下交给作者的真实身份签名留存表。作者不得修改评分者交回的原始文件。
""",
        encoding="utf-8",
    )
    (PACKAGE / "02_RATER-F匿名独立性声明_回填.md").write_text(
        """# RATER-F匿名独立性声明

我声明：本文件由本人在未查看既有编码、作者复核结果和统计结果的条件下独立完成。本人逐题阅读了材料包中的题干、参考解答、TikZ图件和编码规则，所有判断均为本人意见，未使用模板或自动批量方式代填。

- 匿名评分者代号：
- 专业背景：
- 实际编码起止日期：
- 完成行数：
- 回填文件名：
- 签名或确认：
""",
        encoding="utf-8",
    )
    (PACKAGE / "03_RATER-F真实身份留存表_仅私下回传作者.md").write_text(
        """# RATER-F真实身份留存表

本文件只私下交给作者保存，不上传公开项目。

- 真实姓名：
- 工作单位或专业身份：
- 联系方式：
- 与作者的关系：
- 是否参与过本项目前期编码或裁决：
- 是否在编码前看过既有标签或统计结果：
- 本人确认独立完成75个单元、300行编码：
- 实际签名：
- 日期：
""",
        encoding="utf-8",
    )
    (PACKAGE / "04_完成前自检清单.md").write_text(
        """# RATER-F完成前自检清单

- [ ] 编码表正好300行，前10列未改动，后10列无空值；
- [ ] 75个分析单元均完成四个维度，进度表75行全部登记；
- [ ] 每条题干引文和解答引文均能在本行指定MD中逐字找到；
- [ ] 每个证据位置均包含正确文件名、小问号和具体锚点；
- [ ] 没有把其他题目的引文、公式或理由填入本题；
- [ ] 没有通用模板理由，没有用省略号替代引文；
- [ ] `否`只对应`未出现`，`是`只对应L1至L4；
- [ ] 置信度按实际判断填写，没有机械地全部标高；
- [ ] 已填写匿名声明和真实身份私下留存表；
- [ ] 交回文件未由作者或他人二次修改。
""",
        encoding="utf-8",
    )
    (PACKAGE / "06_材料来源与使用顺序.md").write_text(
        """# 材料来源与使用顺序

## 主要材料

`清晰排版题目与解答` 来自项目已经整理的逐题LaTeX文本，公式按数学格式重排，题图与必要解题图由TikZ重绘。该目录同时提供43题合订PDF和可复制的逐题MD。

## 原始证据

`原始试卷证据` 保存第35至42届试题及参考解答PDF，用于确认原始措辞、图号和公式。它们不是主要填写入口，不需要重新进行文字识别。

## 使用次序

先读逐题MD或43题PDF；再在需要时查原始PDF；最后把引文从对应MD逐字复制到编码表。不要从原始PDF的自动文本层复制乱码。
""",
        encoding="utf-8",
    )


def copy_rules_and_pdfs() -> None:
    rules = PACKAGE / "编码规则"
    rules.mkdir(parents=True, exist_ok=True)
    for source in (
        ROOT / "04_framework/科学思维编码手册_第三版.md",
        ROOT / "04_framework/科学思维编码决策矩阵_第三版.csv",
    ):
        shutil.copy2(source, rules / source.name)

    evidence = PACKAGE / "原始试卷证据"
    evidence.mkdir(parents=True, exist_ok=True)
    for source_name, target_name in PDF_SOURCES:
        source = ROOT / source_name
        if not source.is_file():
            raise SystemExit(f"缺少原始PDF：{source}")
        shutil.copy2(source, evidence / target_name)


def build_clean_sources(question_ids: list[str]) -> list[dict[str, str]]:
    readable = PACKAGE / "清晰排版题目与解答"
    image_dir = readable / "图件"
    latex_root = PACKAGE / "可编辑LaTeX源"
    question_out = latex_root / "questions"
    tikz_out = latex_root / "tikz"
    readable.mkdir(parents=True, exist_ok=True)
    image_dir.mkdir(parents=True, exist_ok=True)
    question_out.mkdir(parents=True, exist_ok=True)
    tikz_out.mkdir(parents=True, exist_ok=True)

    qa_rows: list[dict[str, str]] = []
    for qid in question_ids:
        source = ATLAS / "questions" / f"{qid}.tex"
        if not source.is_file():
            raise SystemExit(f"缺少清晰LaTeX题目：{source}")
        tex = clean_question_tex(source.read_text(encoding="utf-8"), qid)
        if "\\subsection{题干}" not in tex or "\\subsection{参考解答整理}" not in tex:
            raise SystemExit(f"题干或参考解答结构不完整：{qid}")
        if PRIVATE_USE.search(tex) or "�" in tex:
            raise SystemExit(f"LaTeX中存在不可识别字符：{qid}")
        (question_out / source.name).write_text(tex, encoding="utf-8")

        tikz_names = re.findall(r"\\input\{tikz/([^}]+)\}", tex)
        for name in tikz_names:
            tikz_source = ATLAS / "tikz" / name
            if not tikz_source.is_file():
                raise SystemExit(f"缺少TikZ源：{tikz_source}")
            shutil.copy2(tikz_source, tikz_out / name)
            png_source = ATLAS / "markdown/assets" / f"{Path(name).stem}.png"
            png_target = image_dir / png_source.name
            if png_source.is_file():
                shutil.copy2(png_source, png_target)
            else:
                render_tikz(tikz_source, png_target)
            if png_target.stat().st_size < 2000:
                raise SystemExit(f"图件文件异常：{png_target}")

        markdown = markdown_from_tex(tex, qid, image_dir)
        if PRIVATE_USE.search(markdown) or "�" in markdown:
            raise SystemExit(f"Markdown中存在不可识别字符：{qid}")
        md_path = readable / f"{qid}.md"
        md_path.write_text(markdown, encoding="utf-8")
        qa_rows.append(
            {
                "题目标识": qid,
                "清晰LaTeX": "通过",
                "题干结构": "通过",
                "参考解答结构": "通过",
                "TikZ图件数": str(len(tikz_names)),
                "不可识别字符数": "0",
                "逐题MD": md_path.name,
            }
        )

    master = latex_root / "独立盲评清晰排版图册_43题.tex"
    inputs = "\n\\bigskip\n".join(
        rf"\input{{questions/{qid}.tex}}" for qid in question_ids
    )
    master.write_text(
        "\n".join(
            [
                r"\documentclass[12pt,a4paper]{ctexart}",
                r"\usepackage[margin=2.4cm]{geometry}",
                r"\usepackage{amsmath,amssymb}",
                r"\usepackage{tikz}",
                r"\usepackage[hidelinks]{hyperref}",
                r"\usetikzlibrary{arrows.meta,calc,decorations.pathmorphing,positioning,shapes.symbols}",
                r"\setlength{\parindent}{2em}",
                r"\setlength{\parskip}{0pt}",
                r"\setlength{\emergencystretch}{3em}",
                r"\renewcommand{\arraystretch}{1.18}",
                r"\makeatletter",
                r"\renewenvironment{figure}[1][]{\par\medskip\noindent\begin{minipage}{\linewidth}\def\@captype{figure}}{\end{minipage}\par\medskip}",
                r"\makeatother",
                r"\title{第35至42届复赛独立盲评\\清晰排版题目与参考解答（43题）}",
                r"\author{}",
                r"\date{}",
                r"\begin{document}",
                r"\pagestyle{plain}",
                r"\maketitle",
                r"\tableofcontents",
                r"\clearpage",
                r"\section*{使用说明}",
                r"本图册仅包含75个盲评单元涉及的43道大题。题干与参考解答已重排，题图和必要解题图使用TikZ重绘；原始PDF另附于材料包供核对。",
                r"\clearpage",
                inputs,
                r"\end{document}",
                "",
            ]
        ),
        encoding="utf-8",
    )
    build = latex_root / "build"
    build.mkdir(parents=True, exist_ok=True)
    command = [
        "xelatex",
        "-interaction=nonstopmode",
        "-halt-on-error",
        f"-output-directory={build}",
        master.name,
    ]
    for _ in range(3):
        subprocess.run(command, cwd=latex_root, check=True, stdout=subprocess.DEVNULL)
    pdf = build / "独立盲评清晰排版图册_43题.pdf"
    if not pdf.is_file():
        raise SystemExit("43题清晰排版图册未生成")
    shutil.copy2(pdf, readable / "第35至42届独立盲评清晰排版题目与解答_43题.pdf")
    log = (build / "独立盲评清晰排版图册_43题.log").read_text(encoding="utf-8", errors="replace")
    bad_log_markers = (
        "overfull",
        "underfull",
        "undefined references",
        "undefined control sequence",
        "fatal error",
    )
    if any(marker in log.lower() for marker in bad_log_markers):
        raise SystemExit("43题清晰排版图册存在版面溢出、未定义引用或编译错误")

    write_csv(PACKAGE / "材料清洗质量报告_43题.csv", qa_rows, list(qa_rows[0]))
    return qa_rows


def validate_package(index_rows: list[dict[str, str]], qa_rows: list[dict[str, str]]) -> None:
    blind_path = PACKAGE / "第35至42届独立盲评编码表_RATER-F_空白300行.csv"
    blind_rows = read_csv(blind_path)
    if len(index_rows) != 75 or len(blind_rows) != 300 or len(qa_rows) != 43:
        raise SystemExit("75单元、300行或43题数量不符合预期")
    if any(row[field].strip() for row in blind_rows for field in REVIEW_FIELDS):
        raise SystemExit("空白编码表后10列存在非空值")
    if len({row["blind_row_id"] for row in blind_rows}) != 300:
        raise SystemExit("blind_row_id存在重复")
    if any(row["source_text_file"] != row["solution_text_file"] for row in blind_rows):
        raise SystemExit("清洗版仍存在题干与解答跨文件错位")
    clean_dir = PACKAGE / "清晰排版题目与解答"
    for row in blind_rows:
        if not (clean_dir / row["source_text_file"]).is_file():
            raise SystemExit(f"找不到行内清晰MD：{row['source_text_file']}")
    clean_texts: dict[str, str] = {}
    forbidden_clean_text = (
        "03_corpus",
        "manual_review",
        "OCR",
        "待复核",
        "待核实",
        "转写依据",
        "本整理不转抄",
        "见答案第",
    )
    for md_path in clean_dir.glob("*.md"):
        clean_text = md_path.read_text(encoding="utf-8")
        clean_texts[md_path.name] = clean_text
        if any(marker in clean_text for marker in forbidden_clean_text):
            raise SystemExit(f"清晰MD仍含内部路径或不完整说明：{md_path}")
        for image_name in re.findall(r"\]\(图件/([^\)]+)\)", clean_text):
            if not (clean_dir / "图件" / image_name).is_file():
                raise SystemExit(f"清晰MD图件链接失效：{md_path.name} -> {image_name}")
    for index_row in index_rows:
        qid = question_id(index_row["item_id"])
        clean_text = clean_texts[f"{qid}.md"]
        anchors = subquestion_anchor_candidates(index_row["subquestion_no"])
        if not any(anchor in clean_text for anchor in anchors):
            raise SystemExit(
                f"盲评单元缺少小问锚点：{index_row['blind_unit_no']} "
                f"{index_row['item_id']} {index_row['subquestion_no']}"
            )
    for text_path in PACKAGE.rglob("*.md"):
        text = text_path.read_text(encoding="utf-8")
        if PRIVATE_USE.search(text) or "�" in text or "{#{" in text or "QQAB" in text:
            raise SystemExit(f"材料包仍含乱码或残留标记：{text_path}")
    forbidden_names = ("RATER-C", "RATER-D", "RATER-E", "author_only", "对照密钥", "最终编码")
    for path in PACKAGE.rglob("*"):
        if any(value in path.name for value in forbidden_names):
            raise SystemExit(f"包内含禁止文件名：{path}")


def write_manifest_and_zip() -> str:
    manifest_rows: list[dict[str, str]] = []
    for path in sorted(PACKAGE.rglob("*")):
        if path.is_file() and path.name != "材料包清单与校验值.csv":
            manifest_rows.append(
                {
                    "相对路径": path.relative_to(PACKAGE).as_posix(),
                    "SHA-256": sha256(path),
                    "字节数": str(path.stat().st_size),
                }
            )
    write_csv(PACKAGE / "材料包清单与校验值.csv", manifest_rows, list(manifest_rows[0]))
    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(PACKAGE.rglob("*")):
            if path.is_file():
                archive.write(path, f"{PACKAGE.name}/{path.relative_to(PACKAGE).as_posix()}")
    return sha256(ZIP_PATH)


def main() -> None:
    if PACKAGE.exists():
        shutil.rmtree(PACKAGE)
    PACKAGE.mkdir(parents=True)
    index_rows = read_csv(INDEX_SOURCE)
    if len(index_rows) != 75:
        raise SystemExit(f"独立盲评索引应为75行，实际为{len(index_rows)}")
    question_ids = list(dict.fromkeys(question_id(row["item_id"]) for row in index_rows))
    if len(question_ids) != 43:
        raise SystemExit(f"盲评材料应涉及43道大题，实际为{len(question_ids)}")

    write_instructions()
    build_blank_tables(index_rows)
    copy_rules_and_pdfs()
    qa_rows = build_clean_sources(question_ids)
    validate_package(index_rows, qa_rows)
    zip_hash = write_manifest_and_zip()
    print(f"package={PACKAGE}")
    print(f"zip={ZIP_PATH}")
    print(f"zip_sha256={zip_hash}")
    print("units=75 blind_rows=300 questions=43")


if __name__ == "__main__":
    main()
