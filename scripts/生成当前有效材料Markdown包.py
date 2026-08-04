#!/usr/bin/env python3
"""Generate readable Markdown companions for the current research materials."""

from __future__ import annotations

import csv
import re
import shutil
import subprocess
import sys
import zipfile
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "10_outputs/当前有效材料_Markdown版"
ATLAS = ROOT / "10_outputs/全量复赛题干解析与TikZ图册"
QUESTION_OUTPUT = OUTPUT / "02_试题题干与参考解答"
SCORE_OUTPUT = OUTPUT / "03_逐题评分标准"
CANONICAL_SCORE_OUTPUT = ROOT / "03_corpus/评分标准Markdown"
PDF_OUTPUT = OUTPUT / "04_原始PDF对应文本"
FRAMEWORK_OUTPUT = OUTPUT / "05_编码框架"
CODING_OUTPUT = OUTPUT / "06_正式编码"
RESULT_OUTPUT = OUTPUT / "07_统计结果"
SCHOOL_OUTPUT = OUTPUT / "10_学校格式模板"

DIMENSIONS = ("模型建构", "科学推理", "科学论证", "质疑创新")
QUESTION_COUNTS = {35: 8, 36: 7, 37: 8, 38: 8, 39: 7, 40: 8, 41: 7, 42: 7}
PDF_COMPANIONS = (
    ("03_corpus/raw_papers/cpho_35_2018_fusai_paper_solution_candidate.pdf", "第35届复赛试题与参考解答.md", 35, "combined"),
    ("03_corpus/raw_papers/cpho_36_2019_fusai_paper_solution_candidate.pdf", "第36届复赛试题与参考解答.md", 36, "combined"),
    ("03_corpus/raw_papers/cpho_37_2020_fusai_paper_solution_candidate.pdf", "第37届复赛试题与参考解答.md", 37, "combined"),
    ("03_corpus/raw_papers/cpho_38_2021_fusai_paper_solution_candidate.pdf", "第38届复赛试题与参考解答.md", 38, "combined"),
    ("03_corpus/raw_papers/cpho_39_2022_fusai_paper_solution_candidate.pdf", "第39届复赛试题与参考解答.md", 39, "combined"),
    ("03_corpus/raw_papers/cpho_40_2023_fusai_paper_solution_candidate.pdf", "第40届复赛试题与参考解答.md", 40, "combined"),
    ("03_corpus/raw_papers/cpho_41_2024_fusai_paper_candidate.pdf", "第41届复赛试题.md", 41, "question"),
    ("03_corpus/raw_solutions/cpho_41_2024_fusai_solution_candidate.pdf", "第41届复赛参考解答.md", 41, "solution"),
    ("03_corpus/raw_papers/cpho_42_2025_fusai_paper_candidate.pdf", "第42届复赛试题.md", 42, "question"),
    ("03_corpus/raw_solutions/cpho_42_2025_fusai_solution_candidate.pdf", "第42届复赛参考解答.md", 42, "solution"),
)


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def display_text(value: object) -> str:
    text = "" if value is None else str(value)
    text = text.replace("V3AR-", "第三版复核记录-")
    text = re.sub(r"(?i)v3", "第三版", text)
    text = text.replace("�", "")
    text = re.sub(r"[\ue000-\uf8ff]", "", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def table_cell(value: object) -> str:
    return display_text(value).replace("|", "\\|").replace("\n", "<br>")


def rows_to_markdown(title: str, source: Path, fields: list[str], rows: list[dict[str, str]]) -> str:
    lines = [f"# {title}", "", f"对应源文件：`{source.relative_to(ROOT)}`", ""]
    lines.append("| " + " | ".join(fields) + " |")
    lines.append("|" + "|".join("---" for _ in fields) + "|")
    for row in rows:
        lines.append("| " + " | ".join(table_cell(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines) + "\n"


def extract_docx_text(path: Path) -> str:
    with zipfile.ZipFile(path) as archive:
        xml = archive.read("word/document.xml")
    root = ElementTree.fromstring(xml)
    namespace = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    paragraphs: list[str] = []
    for paragraph in root.iter(f"{namespace}p"):
        parts = [node.text or "" for node in paragraph.iter(f"{namespace}t")]
        text = "".join(parts).strip()
        if text:
            paragraphs.append(text)
    return "\n\n".join(paragraphs)


def extract_pptx_text(path: Path) -> str:
    with zipfile.ZipFile(path) as archive:
        slide_names = sorted(
            (name for name in archive.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml", name)),
            key=lambda name: int(re.search(r"slide(\d+)", name).group(1)),
        )
        slides: list[str] = []
        for index, name in enumerate(slide_names, 1):
            root = ElementTree.fromstring(archive.read(name))
            texts = [node.text.strip() for node in root.iter() if node.tag.endswith("}t") and node.text and node.text.strip()]
            slides.append(f"## 第{index}页\n\n" + "\n\n".join(texts))
    return "\n\n".join(slides)


def split_question_markdown(text: str, mode: str) -> str:
    marker = "## 参考解答整理"
    if marker not in text:
        raise RuntimeError("逐题Markdown缺少参考解答标题")
    question, solution = text.split(marker, 1)
    if mode == "question":
        return question.rstrip() + "\n"
    if mode == "solution":
        heading = question.splitlines()[1] if len(question.splitlines()) > 1 else ""
        return f"# {heading.replace('#', '').strip()}参考解答\n\n{solution.strip()}\n"
    return text


def score_block_from_item_text(qid: str) -> str:
    path = ROOT / "03_corpus/item_texts" / f"{qid}.md"
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    candidates: list[str] = []
    for index, line in enumerate(lines):
        if not re.match(r"^\s*评分(?:标准|参考)\s*[：:]", line):
            continue
        block: list[str] = []
        blank_count = 0
        for current in lines[index : index + 24]:
            stripped = current.strip()
            if stripped.startswith("## ") or stripped == "```":
                if block:
                    break
                continue
            if not stripped:
                blank_count += 1
                if block and blank_count >= 2:
                    break
                continue
            blank_count = 0
            block.append(stripped)
        if block:
            candidates.append("\n".join(block))
    return max(candidates, key=len) if candidates else ""


def score_summary_from_formula_check(qid: str) -> list[dict[str, str]]:
    path = ROOT / "03_corpus/manual_review_transcripts" / f"{qid}_formula_check_v1.csv"
    _, rows = read_csv(path)
    selected: list[dict[str, str]] = []
    for row in rows:
        scope = str(row.get("source_scope", ""))
        result = str(row.get("formula_or_result", ""))
        if "评分" in scope or ("本题" in result and "分" in result):
            selected.append(row)
    return selected


def build_questions() -> dict[str, str]:
    sys.path.insert(0, str(ROOT / "07_analysis/scripts"))
    from build_rater_f_clean_package import clean_question_tex, markdown_from_tex  # noqa: PLC0415

    QUESTION_OUTPUT.mkdir(parents=True, exist_ok=True)
    image_output = QUESTION_OUTPUT / "图件"
    shutil.copytree(ATLAS / "markdown/assets", image_output, dirs_exist_ok=True)
    atlas_markdown_output = ATLAS / "markdown"
    atlas_markdown_output.mkdir(parents=True, exist_ok=True)
    generated: dict[str, str] = {}
    for edition, count in QUESTION_COUNTS.items():
        for question in range(1, count + 1):
            qid = f"CPHO{edition}-Q{question:02d}"
            source = ATLAS / "questions" / f"{qid}.tex"
            tex = clean_question_tex(source.read_text(encoding="utf-8"), qid)
            markdown = markdown_from_tex(tex, qid, image_output).replace("(图件/", "(图件/")
            markdown = display_text(markdown) + "\n"
            (QUESTION_OUTPUT / f"{qid}.md").write_text(markdown, encoding="utf-8")
            atlas_markdown = markdown.replace("(图件/", "(assets/")
            atlas_markdown = "\n".join(line.rstrip() for line in atlas_markdown.splitlines()) + "\n"
            (atlas_markdown_output / f"{qid}.md").write_text(atlas_markdown, encoding="utf-8")
            generated[qid] = markdown
    return generated


def build_scores() -> None:
    SCORE_OUTPUT.mkdir(parents=True, exist_ok=True)
    _, rubric_rows = read_csv(ROOT / "03_corpus/cpho35_score_rubric_v1.csv")
    rubric_by_question: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rubric_rows:
        rubric_by_question[f"CPHO35-Q{int(row['question_no']):02d}"].append(row)

    index = ["# 第35至42届逐题评分标准Markdown索引", ""]
    for edition, count in QUESTION_COUNTS.items():
        index.extend([f"## 第{edition}届", ""])
        for question in range(1, count + 1):
            qid = f"CPHO{edition}-Q{question:02d}"
            lines = [f"# 第{edition}届复赛第{question}题评分标准", ""]
            if edition == 35:
                lines.append("对应来源：第35届逐步骤评分标准PDF及结构化评分台账。")
                lines.extend(["", "| 小问 | 大题总分 | 小问分值 | 来源页 |", "|---|---:|---:|---:|"])
                for row in rubric_by_question[qid]:
                    lines.append(
                        f"| {table_cell(row['subquestion_no'])} | {table_cell(row['question_score'])} | "
                        f"{table_cell(row['subquestion_score'])} | {table_cell(row['score_source_pdf_page'])} |"
                    )
            else:
                block = score_block_from_item_text(qid)
                summaries = score_summary_from_formula_check(qid)
                if edition == 37 and summaries:
                    lines.extend(["对应来源：公式核对表中的评分标准登记。", ""])
                    for row in summaries:
                        lines.append(f"- 页码：{display_text(row.get('pdf_pages', ''))}")
                        lines.append(f"- 登记内容：{display_text(row.get('formula_or_result', ''))}")
                elif block:
                    lines.extend(["对应来源：参考解答中的评分标准或评分参考。", "", block])
                elif summaries:
                    lines.extend(["对应来源：公式核对表中的评分标准登记。", ""])
                    for row in summaries:
                        lines.append(f"- 页码：{display_text(row.get('pdf_pages', ''))}")
                        lines.append(f"- 登记内容：{display_text(row.get('formula_or_result', ''))}")
                else:
                    raise RuntimeError(f"未找到评分标准入口：{qid}")
            lines.extend(["", f"对应题干与解答：[`{qid}.md`](../02_试题题干与参考解答/{qid}.md)", ""])
            (SCORE_OUTPUT / f"{qid}_评分标准.md").write_text("\n".join(lines), encoding="utf-8")
            index.append(f"- [{qid}评分标准](./{qid}_评分标准.md)")
        index.append("")
    (SCORE_OUTPUT / "评分标准总索引.md").write_text("\n".join(index), encoding="utf-8")
    if CANONICAL_SCORE_OUTPUT.exists():
        shutil.rmtree(CANONICAL_SCORE_OUTPUT)
    shutil.copytree(SCORE_OUTPUT, CANONICAL_SCORE_OUTPUT)


def build_pdf_companions(questions: dict[str, str]) -> list[tuple[str, str]]:
    PDF_OUTPUT.mkdir(parents=True, exist_ok=True)
    mappings: list[tuple[str, str]] = []
    for source_name, target_name, edition, mode in PDF_COMPANIONS:
        pieces = [
            f"# {Path(target_name).stem}",
            "",
            f"对应原始文件：`{source_name}`",
            "",
            "> 以下文字来自已经校订的逐题LaTeX文本，不使用原PDF的低质量自动文本层。",
            "",
        ]
        for question in range(1, QUESTION_COUNTS[edition] + 1):
            qid = f"CPHO{edition}-Q{question:02d}"
            section = split_question_markdown(questions[qid], mode)
            section = section.replace(
                "(图件/",
                "(../02_试题题干与参考解答/图件/",
            )
            pieces.append(section)
        target = PDF_OUTPUT / target_name
        target.write_text("\n\n".join(pieces), encoding="utf-8")
        mappings.append((source_name, str(target.relative_to(OUTPUT))))
    return mappings


def build_framework_and_coding() -> list[tuple[str, str]]:
    FRAMEWORK_OUTPUT.mkdir(parents=True, exist_ok=True)
    CODING_OUTPUT.mkdir(parents=True, exist_ok=True)
    manual = ROOT / "04_framework/科学思维编码手册_第三版.md"
    manual_target = FRAMEWORK_OUTPUT / manual.name
    shutil.copy2(manual, manual_target)

    matrix = ROOT / "04_framework/科学思维编码决策矩阵_第三版.csv"
    matrix_fields, matrix_rows = read_csv(matrix)
    matrix_target = FRAMEWORK_OUTPUT / "科学思维编码决策矩阵_第三版.md"
    matrix_target.write_text(
        rows_to_markdown("科学思维编码决策矩阵第三版", matrix, matrix_fields, matrix_rows),
        encoding="utf-8",
    )

    item_index = ROOT / "03_corpus/item_index.csv"
    index_fields, index_rows = read_csv(item_index)
    readable_index_fields = [
        "item_id", "competition_no", "year", "question_no", "subquestion_no",
        "analysis_unit", "knowledge_primary", "knowledge_secondary", "representation", "math_tools",
    ]
    item_target = CODING_OUTPUT / "第35至42届221个分析单元索引.md"
    item_target.write_text(
        rows_to_markdown("第35至42届221个分析单元索引", item_index, readable_index_fields, index_rows),
        encoding="utf-8",
    )

    unique = ROOT / "07_analysis/data/作者授权采用分析版/第35至42届科学思维作者授权采用分析表.csv"
    adoption = ROOT / "07_analysis/data/作者授权采用分析版/三方分歧交叉审计后采用记录.csv"
    _, coding_rows = read_csv(unique)
    adoption_fields, adoption_rows = read_csv(adoption)
    adoption_by_id = {row["review_row_id"]: row for row in adoption_rows}
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in coding_rows:
        grouped[row["item_id"]].append(row)
    lines = [
        "# 第35至42届科学思维作者授权采用分析表",
        "",
        f"对应源文件：`{unique.relative_to(ROOT)}`",
        f"分歧采用依据：`{adoption.relative_to(ROOT)}`",
        "",
        "第三版基线保持不变；146条分歧记录的正式理由和证据位置以分歧采用表为准。",
        "",
    ]
    for item_id, rows in grouped.items():
        lines.extend([f"## {item_id}：{display_text(rows[0]['required_output'])}", ""])
        for row in sorted(rows, key=lambda value: DIMENSIONS.index(value["dimension"])):
            adopted = adoption_by_id.get(row["review_row_id"])
            reason = adopted["采用依据"] if adopted else row["author_review_reason"]
            evidence_location = adopted["证据位置"] if adopted else row["post_review_evidence_location"]
            adjacent_review = (
                "见正式采用依据中的存在性门槛与相邻等级说明"
                if adopted
                else row["adjacent_level_review"]
            )
            lines.extend(
                [
                    f"### {row['dimension']}：{row['present_label']} / {row['level']}",
                    "",
                    f"- 题干引文：{display_text(row['question_quote'])}",
                    f"- 题干位置：{display_text(row['question_location'])}",
                    f"- 解答引文：{display_text(row['solution_quote'])}",
                    f"- 解答位置：{display_text(row['solution_location'])}",
                    f"- 必要认知活动：{display_text(row['necessary_cognitive_activity'])}",
                    f"- 判定理由：{display_text(reason)}",
                    f"- 相邻等级核对：{display_text(adjacent_review)}",
                    f"- 证据定位：{display_text(evidence_location)}",
                    "",
                ]
            )
    coding_target = CODING_OUTPUT / "第35至42届科学思维作者授权采用分析表.md"
    coding_target.write_text("\n".join(lines), encoding="utf-8")
    adoption_target = CODING_OUTPUT / "三方分歧交叉审计后采用记录.md"
    adoption_target.write_text(
        rows_to_markdown("三方分歧交叉审计后采用记录", adoption, adoption_fields, adoption_rows),
        encoding="utf-8",
    )
    if len(coding_rows) != 884 or len(grouped) != 221:
        raise RuntimeError(f"正式编码数量异常：{len(grouped)}个单元/{len(coding_rows)}条记录")
    return [
        (str(manual.relative_to(ROOT)), str(manual_target.relative_to(OUTPUT))),
        (str(matrix.relative_to(ROOT)), str(matrix_target.relative_to(OUTPUT))),
        (str(item_index.relative_to(ROOT)), str(item_target.relative_to(OUTPUT))),
        (str(unique.relative_to(ROOT)), str(coding_target.relative_to(OUTPUT))),
        (str(adoption.relative_to(ROOT)), str(adoption_target.relative_to(OUTPUT))),
    ]


def build_results() -> list[tuple[str, str]]:
    RESULT_OUTPUT.mkdir(parents=True, exist_ok=True)
    source_root = ROOT / "07_analysis/results/作者授权采用分析版"
    mappings: list[tuple[str, str]] = []
    for source in sorted(source_root.rglob("*")):
        if not source.is_file():
            continue
        relative = source.relative_to(source_root)
        if source.suffix.lower() == ".csv":
            fields, rows = read_csv(source)
            target = RESULT_OUTPUT / relative.with_suffix(".md")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(rows_to_markdown(source.stem, source, fields, rows), encoding="utf-8")
            mappings.append((str(source.relative_to(ROOT)), str(target.relative_to(OUTPUT))))
        elif source.suffix.lower() == ".md":
            target = RESULT_OUTPUT / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(display_text(source.read_text(encoding="utf-8")) + "\n", encoding="utf-8")
            mappings.append((str(source.relative_to(ROOT)), str(target.relative_to(OUTPUT))))
    return mappings


def build_manuscript_and_presentation() -> list[tuple[str, str]]:
    manuscript_output = OUTPUT / "08_论文"
    presentation_output = OUTPUT / "09_答辩材料"
    manuscript_output.mkdir(parents=True, exist_ok=True)
    presentation_output.mkdir(parents=True, exist_ok=True)

    merged = ROOT / "10_outputs/论文初稿_LaTeX/论文初稿_合并源稿.md"
    thesis_target = manuscript_output / "全国中学生物理竞赛复赛试题的科学思维要求与教学启示.md"
    thesis_target.write_text(display_text(merged.read_text(encoding="utf-8")) + "\n", encoding="utf-8")

    pptx = ROOT / "10_outputs/答辩PPT/全国中学生物理竞赛复赛理论试题的科学思维要求及教学设计启示_答辩PPT.pptx"
    ppt_target = presentation_output / "答辩PPT文字稿.md"
    ppt_target.write_text("# 答辩PPT文字稿\n\n" + extract_pptx_text(pptx) + "\n", encoding="utf-8")
    return [
        ("10_outputs/华东师大2025格式论文/build/全国中学生物理竞赛复赛试题的科学思维要求与教学启示.pdf", str(thesis_target.relative_to(OUTPUT))),
        (str(pptx.relative_to(ROOT)), str(ppt_target.relative_to(OUTPUT))),
        ("10_outputs/全量复赛题干解析与TikZ图册/build/全量题干解析与TikZ图册.pdf", "02_试题题干与参考解答/逐题60份Markdown"),
    ]


def build_school_templates() -> list[tuple[str, str]]:
    SCHOOL_OUTPUT.mkdir(parents=True, exist_ok=True)
    source_root = ROOT / "01_positioning/华东师大官方格式模板"
    mappings: list[tuple[str, str]] = []
    for source in sorted(source_root.iterdir()):
        if source.suffix.lower() == ".pdf":
            result = subprocess.run(["pdftotext", "-layout", str(source), "-"], check=True, capture_output=True, text=True)
            body = result.stdout.strip()
        elif source.suffix.lower() == ".docx":
            body = extract_docx_text(source)
        else:
            continue
        target = SCHOOL_OUTPUT / f"{source.stem}.md"
        target.write_text(f"# {source.stem}\n\n对应源文件：`{source.relative_to(ROOT)}`\n\n{body}\n", encoding="utf-8")
        mappings.append((str(source.relative_to(ROOT)), str(target.relative_to(OUTPUT))))
    return mappings


def write_navigation(mappings: list[tuple[str, str]]) -> None:
    navigation = """# 当前有效材料总入口

> 本目录只收录当前研究和论文交付直接使用的材料。历史草稿、旧编码版本和过程性复核文件不在本目录里混用。

| 项目 | 当前数量或版本 |
|---|---:|
| 复赛届次 | 第35至42届 |
| 大题 | 60道 |
| 原始小问 | 209个 |
| 分析单元 | 221个 |
| 科学思维编码 | 884条 |
| 当前编码版本 | 作者授权采用分析版（第三版基线保留） |

## 直接打开

1. [论文全文Markdown](./08_论文/全国中学生物理竞赛复赛试题的科学思维要求与教学启示.md)
2. [60道试题题干与参考解答](./02_试题题干与参考解答/)
3. [60道逐题评分标准索引](./03_逐题评分标准/评分标准总索引.md)
4. [科学思维编码手册第三版](./05_编码框架/科学思维编码手册_第三版.md)
5. [221个分析单元索引](./06_正式编码/第35至42届221个分析单元索引.md)
6. [884条正式编码](./06_正式编码/第35至42届科学思维作者授权采用分析表.md)
7. [统计结果](./07_统计结果/)
8. [答辩PPT文字稿](./09_答辩材料/答辩PPT文字稿.md)
9. [华东师范大学格式材料](./10_学校格式模板/)
10. [材料包质量检查](./11_质量检查.md)

## 可视化成果

- [当前论文PDF](../华东师大2025格式论文/build/全国中学生物理竞赛复赛试题的科学思维要求与教学启示.pdf)
- [第35至42届全量题干解析与TikZ图册PDF](../全量复赛题干解析与TikZ图册/build/全量题干解析与TikZ图册.pdf)
- [当前答辩PPT](../答辩PPT/全国中学生物理竞赛复赛理论试题的科学思维要求及教学设计启示_答辩PPT.pptx)

## 文字与图件说明

- 60道题干与解答均使用已校订的LaTeX文本生成，不使用原PDF中的低质量自动文本层。
- 题图与解题图已以TikZ或校订图件纳入逐题Markdown，图件链接可直接打开。
- “原始PDF对应文本”用于快速通读同一届试题；正式分析仍以逐题Markdown和题目索引为准。

## 版本说明

正式统计使用“作者授权采用分析版”；“第三版”保留为独立编码比较与分歧复核的冻结基线。源数据中为保持历史主键稳定而保留的旧记录编号，不作为论文结论的数据版本。
"""
    (OUTPUT / "00_开始阅读.md").write_text(navigation, encoding="utf-8")
    lines = [
        "# 非Markdown文件与对应Markdown关系",
        "",
        "本表用于从PDF、CSV、DOCX或PPTX直接进入可阅读的Markdown文本。",
        "",
        "| 原文件 | 对应Markdown |",
        "|---|---|",
    ]
    for source, target in sorted(set(mappings)):
        source_link = f"[`原文件`](../../{source})<br>`{source}`"
        target_path = OUTPUT / target
        if target_path.exists():
            target_link = f"[`打开Markdown`](./{target})<br>`{target}`"
        else:
            target_link = f"`{target}`"
        lines.append(f"| {source_link} | {target_link} |")
    (OUTPUT / "01_材料对应关系.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate() -> None:
    question_files = list(QUESTION_OUTPUT.glob("CPHO??-Q??.md"))
    score_files = list(SCORE_OUTPUT.glob("CPHO??-Q??_评分标准.md"))
    if len(question_files) != 60 or len(score_files) != 60:
        raise RuntimeError(f"逐题Markdown数量异常：题目{len(question_files)}，评分{len(score_files)}")
    markdown_files = list(OUTPUT.rglob("*.md"))
    unreadable: list[Path] = []
    version_tokens: list[Path] = []
    empty_files: list[Path] = []
    broken_links: list[tuple[Path, str]] = []
    link_pattern = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
    for path in markdown_files:
        text = path.read_text(encoding="utf-8")
        if not text.strip():
            empty_files.append(path)
        if "�" in text or re.search(r"[\ue000-\uf8ff]", text):
            unreadable.append(path)
        if re.search(r"(?i)v3", text):
            version_tokens.append(path)
        for raw_target in link_pattern.findall(text):
            target = unquote(raw_target.strip().strip("<>").split("#", 1)[0])
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            resolved_target = (path.parent / target).resolve()
            if resolved_target == (OUTPUT / "11_质量检查.md").resolve():
                continue
            if not resolved_target.exists():
                broken_links.append((path, raw_target))
    if unreadable:
        raise RuntimeError(f"Markdown存在不可识别字符：{unreadable[:3]}")
    if version_tokens:
        raise RuntimeError(f"Markdown仍出现V3写法：{version_tokens[:3]}")
    if empty_files:
        raise RuntimeError(f"Markdown存在空文件：{empty_files[:3]}")
    if broken_links:
        raise RuntimeError(f"Markdown存在断链：{broken_links[:3]}")
    image_files = list((QUESTION_OUTPUT / "图件").glob("*.png"))
    pdf_companions = list(PDF_OUTPUT.glob("*.md"))
    report = [
        "# Markdown材料包质量检查",
        "",
        f"- Markdown文件总数：{len(markdown_files) + 1}",
        f"- 清晰题干与解答：{len(question_files)}/60",
        f"- 逐题评分标准：{len(score_files)}/60",
        f"- 题图与解题图：{len(image_files)}张",
        f"- 原始PDF对应文本：{len(pdf_companions)}/10",
        "- 正式编码：221个分析单元、884条记录",
        "- 不可识别字符：0",
        "- 空Markdown文件：0",
        "- Markdown断链：0",
        "- 旧版英文缩写：0",
        "- 结论：通过",
    ]
    (OUTPUT / "11_质量检查.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def normalize_markdown_files() -> None:
    for path in OUTPUT.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        normalized = "\n".join(line.rstrip() for line in text.splitlines()) + "\n"
        path.write_text(normalized, encoding="utf-8")


def main() -> None:
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    OUTPUT.mkdir(parents=True)
    questions = build_questions()
    build_scores()
    mappings = build_pdf_companions(questions)
    mappings.extend(build_framework_and_coding())
    mappings.extend(build_results())
    mappings.extend(build_manuscript_and_presentation())
    mappings.extend(build_school_templates())
    write_navigation(mappings)
    normalize_markdown_files()
    validate()
    print(f"PASS: Markdown材料包已生成：{OUTPUT}")


if __name__ == "__main__":
    main()
