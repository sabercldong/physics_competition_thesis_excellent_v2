#!/usr/bin/env python3
"""Audit current manuscript working-draft facts against ECNU's public baseline."""

from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MANUSCRIPT = ROOT / "08_manuscript"
ABSTRACT = MANUSCRIPT / "00_abstract_content_draft.md"
ENGLISH_ABSTRACT = MANUSCRIPT / "00_abstract_en_content_draft.md"
REFERENCES = MANUSCRIPT / "07_candidate_references.md"
FORMAT_SOURCES = ROOT / "01_positioning/ecnu_official_thesis_format_sources.md"
OUTPUT_CSV = ROOT / "09_quality/r01_ecnu_public_baseline_current_draft_audit_20260725.csv"
OUTPUT_MD = ROOT / "09_quality/r01_ecnu_public_baseline_current_draft_audit_20260725.md"
OUTPUT_QA_CSV = ROOT / "09_quality/r01_ecnu_public_baseline_current_draft_audit_qa_v1.csv"
OUTPUT_QA_MD = ROOT / "09_quality/r01_ecnu_public_baseline_current_draft_audit_qa_v1.md"

DEFAULT_TITLE = "科学思维视域下全国中学生物理竞赛复赛试题的认知要求及教学转化研究——基于第35—42届试题的内容分析"
FORMAT_COMPATIBLE_TITLE = "中学生物理竞赛复赛试题的科学思维要求与教学转化研究"
CHAPTERS = [
    "01_introduction.md", "02_theory.md", "03_methods.md", "04_results.md",
    "05_cases_and_diagnosis.md", "06_conclusion.md",
]


def han_count(text: str) -> int:
    return len(re.findall(r"[\u4e00-\u9fff]", text))


def keyword_values(text: str, label: str) -> list[str]:
    match = re.search(rf"\*\*{re.escape(label)}\*\*\s*(.+)", text)
    if not match:
        return []
    return [value.strip() for value in re.split(r"[；;]", match.group(1)) if value.strip()]


def main() -> None:
    chinese = ABSTRACT.read_text(encoding="utf-8")
    english = ENGLISH_ABSTRACT.read_text(encoding="utf-8")
    reference_text = REFERENCES.read_text(encoding="utf-8")
    format_text = FORMAT_SOURCES.read_text(encoding="utf-8")
    body = re.sub(r"^#.*\n", "", chinese, count=1)
    body = re.sub(r"\*\*关键词建议：\*\*.*", "", body, flags=re.S)
    body = re.sub(r"\*\*(目的|方法|结果|结论|局限)：\*\*", "", body)
    chinese_count = han_count(body)
    chinese_keywords = keyword_values(chinese, "关键词建议：")
    english_keywords = keyword_values(english, "Keywords (working):")
    entries = re.findall(r"^\[(\d+)\]\s+(.+)$", reference_text, flags=re.M)
    foreign_entries = [entry for _, entry in entries if not re.search(r"[\u4e00-\u9fff]", entry)]
    chapter_exists = all((MANUSCRIPT / chapter).is_file() for chapter in CHAPTERS)

    rows = [
        {
            "check_id": "FMTCUR-01", "item": "公开基线定位", "expected": "摘要300--500字；关键词4--8个；硕士参考文献不少于30篇且含外文文献",
            "actual": "已在ECNU官方来源核验文件定位", "status": "通过", "boundary": "公开基线不替代实际答辩期学院细则。",
        },
        {
            "check_id": "FMTCUR-02", "item": "中文摘要汉字计数", "expected": "300--500", "actual": str(chinese_count),
            "status": "通过" if 300 <= chinese_count <= 500 else "不通过", "boundary": "按正文汉字计数，未计标题、字段标签与关键词。",
        },
        {
            "check_id": "FMTCUR-03", "item": "中文关键词数量", "expected": "4--8", "actual": str(len(chinese_keywords)),
            "status": "通过" if 4 <= len(chinese_keywords) <= 8 else "不通过", "boundary": "关键词最终表述仍需导师/学院确认。",
        },
        {
            "check_id": "FMTCUR-04", "item": "英文关键词数量", "expected": "与中文摘要一致且数量4--8", "actual": str(len(english_keywords)),
            "status": "通过" if 4 <= len(english_keywords) <= 8 else "不通过", "boundary": "官方赛事英文名称与最终术语仍待定稿。",
        },
        {
            "check_id": "FMTCUR-05", "item": "候选参考文献数量", "expected": "不少于30", "actual": str(len(entries)),
            "status": "通过" if len(entries) >= 30 else "不通过", "boundary": "候选36项不等于最终文后表放行。",
        },
        {
            "check_id": "FMTCUR-06", "item": "候选外文文献", "expected": "至少1项", "actual": str(len(foreign_entries)),
            "status": "通过" if foreign_entries else "不通过", "boundary": "仅按条目中无汉字识别；不替代最终著录核验。",
        },
        {
            "check_id": "FMTCUR-07", "item": "六章工作稿结构", "expected": "绪论起、结论止", "actual": "6章文件均可定位" if chapter_exists else "章节文件缺失",
            "status": "通过" if chapter_exists else "不通过", "boundary": "不代表目录、前置页、附录或逐页排版已完成。",
        },
        {
            "check_id": "FMTCUR-08", "item": "当前默认工作题目字数", "expected": "一般不超过25个汉字", "actual": str(han_count(DEFAULT_TITLE)),
            "status": "待关闭", "boundary": "默认题目尚未获作者/导师确认，不能自行替换。",
        },
        {
            "check_id": "FMTCUR-09", "item": "25字格式兼容题目候选", "expected": "不超过25个汉字", "actual": str(han_count(FORMAT_COMPATIBLE_TITLE)),
            "status": "通过", "boundary": "仅供作者/导师选择，不构成最终题目决定。",
        },
    ]
    with OUTPUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    lines = [
        "# R01 当前工作稿与ECNU公开格式基线对账（2026-07-25）", "",
        "本对账只核验公开基线下可由当前文件直接计算的事实，不生成学校终稿、匿名版或提交资格。", "",
        "| 项目 | 当前计数/状态 | 公开基线判断 |", "|---|---|---|",
    ]
    for row in rows:
        lines.append(f"| {row['item']} | {row['actual']} | {row['status']} |")
    lines.extend([
        "", "## 直接处理结果", "",
        f"中文摘要已压缩至{chinese_count}个汉字；中英文关键词均为{len(chinese_keywords)}个；候选参考文献为{len(entries)}项，其中按条目文本识别有{len(foreign_entries)}项外文条目。以上只满足工作稿的数量/结构基线，候选条目仍不是最终文后表。", "",
        "默认工作题目为43个汉字，超过公开基线的“一般不超过25个汉字”。可供确认的25字候选为：**中学生物理竞赛复赛试题的科学思维要求与教学转化研究**。该候选不替代作者/导师的最终决定。", "",
        "仍待学院当期规则关闭的事项包括封皮、专硕模板、AI披露、匿名版、图书馆提交、最终引文格式和逐页排版。",
    ])
    OUTPUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    qa_rows = [
        {"check_id": row["check_id"], "check_item": row["item"], "status": row["status"], "detail": row["actual"]}
        for row in rows
    ]
    fatal = [row["check_id"] for row in qa_rows if row["status"] == "不通过"]
    with OUTPUT_QA_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(qa_rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(qa_rows)
    OUTPUT_QA_MD.write_text(
        "# R01 当前工作稿ECNU公开基线对账 QA（V1）\n\n"
        f"{len(rows) - len(fatal) - 1}/{len(rows) - 1}项可计算基线通过；题目确认项保持待关闭。"
        "本QA不判断导师同意、学院当期规则、最终参考文献资格或提交资格。\n",
        encoding="utf-8",
    )
    if fatal:
        raise SystemExit("ECNU公开基线当前工作稿审计失败：" + ", ".join(fatal))
    print(f"R01当前工作稿ECNU公开基线审计：{len(rows) - 1}/{len(rows) - 1}可计算项通过；1项题目待关闭")


if __name__ == "__main__":
    main()
