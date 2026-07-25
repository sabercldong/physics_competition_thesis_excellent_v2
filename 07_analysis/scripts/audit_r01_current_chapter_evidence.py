#!/usr/bin/env python3
"""Audit current manuscript chapters against frozen R01 evidence and QA artifacts."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MANUSCRIPT = ROOT / "08_manuscript"
QUALITY = ROOT / "09_quality"
CODING = ROOT / "07_analysis/data/final_coding_r01_correction_v1.csv"
OUTPUT_CSV = QUALITY / "r01_current_chapter_evidence_audit_v1.csv"
OUTPUT_MD = QUALITY / "r01_current_chapter_evidence_audit_v1.md"


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def all_pass(path: Path, expected_count: int) -> bool:
    records = csv_rows(path)
    return len(records) == expected_count and all(row.get("status") == "通过" for row in records)


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> None:
    chapter_paths = [MANUSCRIPT / f"0{index}_{name}.md" for index, name in [
        (1, "introduction"),
        (2, "theory"),
        (3, "methods"),
        (4, "results"),
        (5, "cases_and_diagnosis"),
        (6, "conclusion"),
    ]]
    chapters = {path.name: text(path) for path in chapter_paths}
    coding_rows = csv_rows(CODING)
    results_qa = QUALITY / "r01_results_manuscript_integration_qa_v2.csv"
    cases_qa = QUALITY / "r01_case_reselection_qa_v1.csv"
    conclusion_qa = QUALITY / "r01_conclusion_rq_alignment_qa_v1.csv"
    abstract_qa = QUALITY / "r01_abstract_alignment_qa_v1.csv"
    claim_matrix = text(QUALITY / "claim_evidence_matrix.csv")
    format_audit = QUALITY / "ecnu_professional_format_reconciliation_20260725.md"

    records: list[dict[str, str]] = []

    def add(check_id: str, item: str, actual: str, expected: str, passed: bool, boundary: str) -> None:
        records.append({
            "check_id": check_id,
            "check_item": item,
            "actual": actual,
            "expected": expected,
            "status": "通过" if passed else "需处理",
            "boundary_or_action": boundary,
        })

    add("CE-AUD-01", "六章Markdown存在", f"{sum(path.is_file() for path in chapter_paths)}/6", "6/6", all(path.is_file() for path in chapter_paths), "文件存在不等于终稿。")
    add("CE-AUD-02", "冻结分析单位与编码记录", f"{len(coding_rows) // 4}/{len(coding_rows)}", "219/876", len(coding_rows) == 876 and len({row['item_id'] for row in coding_rows}) == 219, "只核对当前冻结表，不验证评分过程身份或独立性。")
    add("CE-AUD-03", "第四章当前结果整合QA", "44/44" if all_pass(results_qa, 44) else "不完整", "44/44通过", all_pass(results_qa, 44), "第四章可报告描述性结果，不能外推学生能力、教学效果或因果。")
    add("CE-AUD-04", "第五章案例重选QA", "7/7" if all_pass(cases_qa, 7) else "不完整", "7/7通过", all_pass(cases_qa, 7), "案例可追溯不等于课堂有效或教师认可。")
    add("CE-AUD-05", "第六章研究问题回应QA", "16/16" if all_pass(conclusion_qa, 16) else "不完整", "16/16通过", all_pass(conclusion_qa, 16), "结论仅限当前语料和编码口径。")
    add("CE-AUD-06", "中英文摘要对齐QA", "28/28" if all_pass(abstract_qa, 28) else "不完整", "28/28通过", all_pass(abstract_qa, 28), "摘要仍是非学校格式内容底稿。")
    add("CE-AUD-07", "第四章关键当前结果", "存在" if all(token in chapters["04_results.md"] for token in ["203", "219", "106", "84", "150"]) else "缺失", "存在", all(token in chapters["04_results.md"] for token in ["203", "219", "106", "84", "150"]), "数值必须随冻结编码变动而重建。")
    add("CE-AUD-08", "第五章三个可追溯案例", "存在" if all(case_id in chapters["05_cases_and_diagnosis.md"] for case_id in ["CPHO41-Q06-3", "CPHO41-Q07-4", "CPHO42-Q04-2"]) else "缺失", "存在", all(case_id in chapters["05_cases_and_diagnosis.md"] for case_id in ["CPHO41-Q06-3", "CPHO41-Q07-4", "CPHO42-Q04-2"]), "仅为任务结构与教学设计材料。")
    add("CE-AUD-09", "结果和案例禁止外推边界", "存在" if all(token in chapters["04_results.md"] + chapters["05_cases_and_diagnosis.md"] for token in ["学生", "教学效果", "项目无法独立验证"]) else "缺失", "存在", all(token in chapters["04_results.md"] + chapters["05_cases_and_diagnosis.md"] for token in ["学生", "教学效果", "项目无法独立验证"]), "须继续保留自声明和无课堂数据限制。")
    add("CE-AUD-10", "第二章文献闭合状态", "未闭合" if "[待补核验文献]" in chapters["02_theory.md"] else "未标记", "明确未闭合", "[待补核验文献]" in chapters["02_theory.md"], "不得把SOLO、竞赛研究或待读方法文献写成正式综述结论。")
    add("CE-AUD-11", "旧主张矩阵与当前结果版本", "发现旧内部预演表述" if "内部预演结果" in claim_matrix else "未发现", "发现并隔离", "内部预演结果" in claim_matrix, "矩阵有并行改动；以本审计侧车列出差异，待人工确认后再合并。")
    add("CE-AUD-12", "非全日制专硕格式对账入口", "存在" if format_audit.is_file() else "缺失", "存在", format_audit.is_file(), "公开格式基线不等于当期学院提交确认。")

    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(records[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(records)

    unresolved = [record for record in records if record["check_id"] in {"CE-AUD-10", "CE-AUD-11"}]
    lines = [
        "# R01当前章节证据审计",
        "",
        "本审计核对当前六章稿与冻结R01编码、结果QA、案例QA、结论QA、摘要QA及格式对账入口。"
        "它不修改并行编辑的正文或主张矩阵，也不验证评分者身份、过程独立性、文献全文、学校格式或课堂事实。",
        "",
        "## 当前可进入非提交工作稿的部分",
        "",
        "- 第四章的当前描述性结果已由44项整合QA核对；",
        "- 第五章的三个案例由7项案例重选QA限定为可追溯任务结构材料；",
        "- 第六章对五个研究问题的回应已由16项QA核对；",
        "- 中英文摘要内容底稿已由28项QA核对。",
        "",
        "## 仍需处理的侧车事项",
        "",
    ]
    lines.extend(f"- `{record['check_id']}`：{record['boundary_or_action']}" for record in unresolved)
    lines.extend([
        "",
        "## 审计结果",
        "",
        "| 编号 | 项目 | 状态 |",
        "|---|---|---|",
    ])
    lines.extend(f"| {record['check_id']} | {record['check_item']} | {record['status']} |" for record in records)
    OUTPUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"R01当前章节证据审计：{sum(record['status'] == '通过' for record in records)}/{len(records)}通过；2项侧车事项已登记")


if __name__ == "__main__":
    main()
