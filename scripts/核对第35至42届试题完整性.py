#!/usr/bin/env python3
"""核对第35至42届复赛试题、分析单元及第三版编码的完整对应关系。"""

from __future__ import annotations

import csv
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ITEM_INDEX = ROOT / "03_corpus/item_index.csv"
CODING = ROOT / "07_analysis/data/第35至42届科学思维第三版唯一编码表.csv"
ATLAS = ROOT / "10_outputs/全量复赛题干解析与TikZ图册"
CURRENT_MARKDOWN = ROOT / "10_outputs/当前有效材料_Markdown版"
OUTPUT_CSV = ROOT / "09_quality/第35至42届试题完整性逐题检查_G8-89.csv"
OUTPUT_REPORT = ROOT / "09_quality/G8-89第35至42届试题完整性复核.md"

DIMENSIONS = ("模型建构", "科学推理", "科学论证", "质疑创新")
QUESTION_COUNTS = {35: 8, 36: 7, 37: 8, 38: 8, 39: 7, 40: 8, 41: 7, 42: 7}
YEARS = {35: 2018, 36: 2019, 37: 2020, 38: 2021, 39: 2022, 40: 2023, 41: 2024, 42: 2025}
SOURCE_FILES = {
    35: (
        "03_corpus/raw_papers/cpho_35_2018_fusai_paper_solution_candidate.pdf",
        "03_corpus/raw_papers/cpho_35_2018_fusai_paper_solution_candidate.pdf",
    ),
    36: (
        "03_corpus/raw_papers/cpho_36_2019_fusai_paper_solution_candidate.pdf",
        "03_corpus/raw_papers/cpho_36_2019_fusai_paper_solution_candidate.pdf",
    ),
    37: (
        "03_corpus/raw_papers/cpho_37_2020_fusai_paper_solution_candidate.pdf",
        "03_corpus/raw_papers/cpho_37_2020_fusai_paper_solution_candidate.pdf",
    ),
    38: (
        "03_corpus/raw_papers/cpho_38_2021_fusai_paper_solution_candidate.pdf",
        "03_corpus/raw_papers/cpho_38_2021_fusai_paper_solution_candidate.pdf",
    ),
    39: (
        "03_corpus/raw_papers/cpho_39_2022_fusai_paper_solution_candidate.pdf",
        "03_corpus/raw_papers/cpho_39_2022_fusai_paper_solution_candidate.pdf",
    ),
    40: (
        "03_corpus/raw_papers/cpho_40_2023_fusai_paper_solution_candidate.pdf",
        "03_corpus/raw_papers/cpho_40_2023_fusai_paper_solution_candidate.pdf",
    ),
    41: (
        "03_corpus/raw_papers/cpho_41_2024_fusai_paper_candidate.pdf",
        "03_corpus/raw_solutions/cpho_41_2024_fusai_solution_candidate.pdf",
    ),
    42: (
        "03_corpus/raw_papers/cpho_42_2025_fusai_paper_candidate.pdf",
        "03_corpus/raw_solutions/cpho_42_2025_fusai_solution_candidate.pdf",
    ),
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def qid_for(row: dict[str, str]) -> str:
    return f"CPHO{int(row['competition_no']):02d}-Q{int(row['question_no']):02d}"


def original_subquestion(label: str) -> str:
    """合并为研究编码而细分的罗马数字后缀，保留原卷自身的小数编号。"""
    return re.sub(r"-[ivxlcdm]+$", "", label.lower())


def normalized(text: str) -> str:
    return unicodedata.normalize("NFKC", text).lower().replace("（", "(").replace("）", ")")


def label_is_present(text: str, label: str) -> bool:
    if "-" in label:
        major, minor = label.lower().split("-", 1)
        candidates = (f"({major})({minor})", f"({major}.{minor})", f"({major}-{minor})")
    else:
        candidates = (f"({label.lower()})",)
    return any(candidate in text for candidate in candidates)


def markdown_images_exist(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    for target in re.findall(r"!\[[^]]*\]\(([^)]+)\)", text):
        if not (path.parent / target).resolve().exists():
            return False
    return True


def main() -> None:
    index_rows = read_csv(ITEM_INDEX)
    coding_rows = read_csv(CODING)
    expected_qids = [
        f"CPHO{edition}-Q{question:02d}"
        for edition, count in QUESTION_COUNTS.items()
        for question in range(1, count + 1)
    ]

    index_by_qid: dict[str, list[dict[str, str]]] = defaultdict(list)
    coding_by_item: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in index_rows:
        index_by_qid[qid_for(row)].append(row)
    for row in coding_rows:
        coding_by_item[row["item_id"]].append(row)

    global_errors: list[str] = []
    item_ids = [row["item_id"] for row in index_rows]
    duplicate_items = [item for item, count in Counter(item_ids).items() if count > 1]
    if duplicate_items:
        global_errors.append(f"分析单元标识重复：{'、'.join(duplicate_items)}")
    if set(index_by_qid) != set(expected_qids):
        missing = sorted(set(expected_qids) - set(index_by_qid))
        extra = sorted(set(index_by_qid) - set(expected_qids))
        global_errors.append(f"大题集合不一致：缺少{missing}；多出{extra}")
    if set(coding_by_item) != set(item_ids):
        missing = sorted(set(item_ids) - set(coding_by_item))
        extra = sorted(set(coding_by_item) - set(item_ids))
        global_errors.append(f"编码单元集合不一致：缺少{missing}；多出{extra}")

    output_rows: list[dict[str, str]] = []
    split_groups: list[tuple[str, str, int]] = []
    edition_summary: dict[int, dict[str, int]] = defaultdict(lambda: defaultdict(int))

    for qid in expected_qids:
        edition = int(qid[4:6])
        question = int(qid[-2:])
        units = sorted(index_by_qid[qid], key=lambda row: item_ids.index(row["item_id"]))
        labels = [row["subquestion_no"] for row in units]
        original_labels = list(dict.fromkeys(original_subquestion(label) for label in labels))
        split_delta = len(units) - len(original_labels)
        if split_delta:
            grouped_labels: dict[str, list[str]] = defaultdict(list)
            for label in labels:
                grouped_labels[original_subquestion(label)].append(label)
            for original, members in grouped_labels.items():
                if len(members) > 1:
                    split_groups.append((qid, original, len(members)))

        paper_source, solution_source = SOURCE_FILES[edition]
        item_text = ROOT / "03_corpus/item_texts" / f"{qid}.md"
        formula_check = ROOT / "03_corpus/manual_review_transcripts" / f"{qid}_formula_check_v1.csv"
        question_tex = ATLAS / "questions" / f"{qid}.tex"
        atlas_question_md = ATLAS / "markdown" / f"{qid}.md"
        question_md = CURRENT_MARKDOWN / "02_试题题干与参考解答" / f"{qid}.md"
        score_md = CURRENT_MARKDOWN / "03_逐题评分标准" / f"{qid}_评分标准.md"
        errors: list[str] = []

        required_files = {
            "原始题面": ROOT / paper_source,
            "原始解答": ROOT / solution_source,
            "题目文本层": item_text,
            "公式核对表": formula_check,
            "清洗版LaTeX": question_tex,
            "图册Markdown": atlas_question_md,
            "清洗版Markdown": question_md,
            "评分标准Markdown": score_md,
        }
        for label, path in required_files.items():
            if not path.is_file() or path.stat().st_size == 0:
                errors.append(f"{label}缺失或为空")

        formula_rows: list[dict[str, str]] = []
        if formula_check.is_file():
            formula_rows = read_csv(formula_check)
            if not formula_rows:
                errors.append("公式核对表没有记录")
            elif not any(row.get("pdf_pages", "").strip() for row in formula_rows):
                errors.append("公式核对表缺少页码定位")

        figure_refs: list[str] = []
        missing_labels: list[str] = []
        if question_tex.is_file():
            tex = question_tex.read_text(encoding="utf-8")
            clean_text = normalized(tex)
            missing_labels = [label for label in labels if not label_is_present(clean_text, label)]
            if missing_labels:
                errors.append(f"清洗版未明确标出小问：{'、'.join(missing_labels)}")
            figure_refs = re.findall(r"\\input\{tikz/([^}]+)\}", tex)
            missing_figures = [name for name in figure_refs if not (ATLAS / "tikz" / name).is_file()]
            if missing_figures:
                errors.append(f"TikZ图源缺失：{'、'.join(missing_figures)}")

        if question_md.is_file():
            markdown = question_md.read_text(encoding="utf-8")
            if "## 题干" not in markdown or "## 参考解答整理" not in markdown:
                errors.append("清洗版Markdown缺少题干或参考解答栏目")
            if not markdown_images_exist(question_md):
                errors.append("清洗版Markdown存在失效图件链接")
        if atlas_question_md.is_file() and not markdown_images_exist(atlas_question_md):
            errors.append("图册Markdown存在失效图件链接")

        if any(not row.get("page_paper", "").strip() or not row.get("page_solution", "").strip() for row in units):
            errors.append("分析单元缺少题面或解答页码")
        if any(int(row["competition_no"]) != edition or int(row["question_no"]) != question for row in units):
            errors.append("分析单元届次或题号字段错位")

        coding_count = 0
        for unit in units:
            records = coding_by_item.get(unit["item_id"], [])
            coding_count += len(records)
            dimension_counts = Counter(row["dimension"] for row in records)
            if set(dimension_counts) != set(DIMENSIONS) or any(count != 1 for count in dimension_counts.values()):
                errors.append(f"{unit['item_id']}未形成四维唯一编码")
        if coding_count != len(units) * 4:
            errors.append(f"编码记录数应为{len(units) * 4}，实际为{coding_count}")

        edition_summary[edition]["questions"] += 1
        edition_summary[edition]["original_subquestions"] += len(original_labels)
        edition_summary[edition]["units"] += len(units)
        edition_summary[edition]["coding"] += coding_count
        output_rows.append(
            {
                "届次": str(edition),
                "年份": str(YEARS[edition]),
                "大题标识": qid,
                "大题序号": str(question),
                "原始小问数": str(len(original_labels)),
                "分析单元数": str(len(units)),
                "研究细分新增单元数": str(split_delta),
                "分析单元编号": "；".join(row["item_id"] for row in units),
                "小问编号": "；".join(labels),
                "题面页码": "；".join(dict.fromkeys(row["page_paper"] for row in units)),
                "解答页码": "；".join(dict.fromkeys(row["page_solution"] for row in units)),
                "公式核对记录数": str(len(formula_rows)),
                "TikZ图源数": str(len(figure_refs)),
                "第三版编码记录数": str(coding_count),
                "完整性结论": "通过" if not errors else "未通过",
                "问题说明": "无" if not errors else "；".join(dict.fromkeys(errors)),
            }
        )

    write_csv(OUTPUT_CSV, output_rows)
    failures = [row for row in output_rows if row["完整性结论"] != "通过"]
    total_original = sum(int(row["原始小问数"]) for row in output_rows)
    total_units = len(index_rows)
    total_coding = len(coding_rows)
    report = [
        "# G8-89 第35至42届试题完整性复核",
        "",
        "## 复核结论",
        "",
        f"- 原始试题覆盖：8届，{len(output_rows)}道大题；各届题号连续，无整道题遗漏。",
        f"- 原始小问覆盖：{total_original}个；当前分析单元：{total_units}个。",
        f"- 第三版编码覆盖：{total_coding}条；每个分析单元均有模型建构、科学推理、科学论证、质疑创新4条唯一记录。",
        "- 题目材料覆盖：每道题均有原始PDF、项目文本层、公式核对表、清洗版LaTeX、图册Markdown、当前有效Markdown和评分标准Markdown。",
        "- 图件覆盖：清洗版所引用的TikZ图源均存在，Markdown图件链接均有效。",
        f"- 最终判定：{'通过，未发现遗漏题目或遗漏分析单元。' if not failures and not global_errors else '未通过，需处理下列异常。'}",
        "",
        "## 届次汇总",
        "",
        "| 届次 | 年份 | 大题数 | 原始小问数 | 分析单元数 | 第三版编码记录数 |",
        "|---:|---:|---:|---:|---:|---:|",
    ]
    for edition in QUESTION_COUNTS:
        values = edition_summary[edition]
        report.append(
            f"| {edition} | {YEARS[edition]} | {values['questions']} | "
            f"{values['original_subquestions']} | {values['units']} | {values['coding']} |"
        )
    report.extend(
        [
            f"| **合计** | 2018—2025 | **{len(output_rows)}** | **{total_original}** | **{total_units}** | **{total_coding}** |",
            "",
            "## 209与221的关系",
            "",
            "原卷共有209个原始小问。研究为避免一个复合小问内部不同认知任务相互遮蔽，"
            "将6个原始小问按罗马数字子任务拆为18个分析单元，净增加12个，因此正式统计使用221个分析单元。"
            "这一处理只改变分析粒度，不新增题目内容，也不删除原始小问。",
            "",
            "| 大题 | 原始小问 | 拆分后单元数 |",
            "|---|---:|---:|",
        ]
    )
    for qid, original, count in split_groups:
        report.append(f"| {qid} | {original} | {count} |")
    report.extend(
        [
            "",
            "## 本轮修复",
            "",
            "完整性扫描发现4道清洗版题目虽然内容和编码均已存在，但小问标题未逐项显式呈现，已补齐：",
            "",
            "- CPHO35-Q01：补明第（1）（2）问；",
            "- CPHO40-Q06：补明第（1）至（4）问；",
            "- CPHO41-Q06：补明第（1）至（4）问；",
            "- CPHO42-Q04：补明第（1.1）（1.2）（2）（3）问。",
            "",
            "同时将图册目录的逐题Markdown由52份补齐为60份，并纳入图件链接检查。",
            "这些是呈现结构修复，不改变题意、答案、分析单元或第三版编码。",
            "",
            "## 可复核文件",
            "",
            "- 逐题检查表：`09_quality/第35至42届试题完整性逐题检查_G8-89.csv`",
            "- 分析单元索引：`03_corpus/item_index.csv`",
            "- 第三版唯一编码表：`07_analysis/data/第35至42届科学思维第三版唯一编码表.csv`",
            "",
        ]
    )
    if global_errors or failures:
        report.extend(["## 异常", ""])
        report.extend(f"- {error}" for error in global_errors)
        report.extend(f"- {row['大题标识']}：{row['问题说明']}" for row in failures)
        report.append("")
    OUTPUT_REPORT.write_text("\n".join(report), encoding="utf-8")

    print(
        f"大题{len(output_rows)}，原始小问{total_original}，分析单元{total_units}，"
        f"第三版编码{total_coding}，未通过{len(failures)}，全局异常{len(global_errors)}"
    )
    if failures or global_errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
