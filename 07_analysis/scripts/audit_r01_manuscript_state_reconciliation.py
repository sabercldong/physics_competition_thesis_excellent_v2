#!/usr/bin/env python3
"""Create a bounded rewrite queue for stale manuscript status wording after R01 results."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUTPUT_CSV = ROOT / "09_quality/r01_manuscript_state_reconciliation_v1.csv"
OUTPUT_MD = ROOT / "09_quality/r01_manuscript_state_reconciliation_v1.md"
CHECKS = [
    {
        "audit_id": "STATE-01",
        "file": "08_manuscript/01_introduction.md",
        "needle": "正式统计结果尚未形成",
        "decision": "修订",
        "evidence": "09_quality/r01_results_eligibility_qa_v1.csv（44/44通过）；08_manuscript/04_results.md",
        "direction": "改为已形成R01版本化描述性结果；保留过程自声明、外部效度和教学证据边界。",
    },
    {
        "audit_id": "STATE-02",
        "file": "08_manuscript/01_introduction.md",
        "needle": "第2至第4个问题必须等待真实评分者编码",
        "decision": "修订",
        "evidence": "07_analysis/data/final_coding_r01_correction_v1.csv；09_quality/r01_results_eligibility_qa_v1.csv",
        "direction": "改为第2至第4问可在R01当前编码口径下作描述性回答；不得扩展为外部效度、学生能力或趋势结论。",
    },
    {
        "audit_id": "STATE-03",
        "file": "08_manuscript/01_introduction.md",
        "needle": "在正式阶段组织评分者培训、独立编码、一致性计算和分歧裁决",
        "decision": "修订",
        "evidence": "07_analysis/results/formal_rater_r01/correction_v1/；09_quality/r01_results_eligibility_qa_v1.csv",
        "direction": "改为已归档的RATER-A/B、ADJ-01、ADJ-02和R01流程，并明确独立性仅按自声明登记。",
    },
    {
        "audit_id": "STATE-04",
        "file": "08_manuscript/02_theory.md",
        "needle": "仍需真实评分者一致性和分歧裁决结果支持",
        "decision": "修订",
        "evidence": "09_quality/r01_results_eligibility_qa_v1.csv；07_analysis/data/final_coding_evidence_r01_v1.csv",
        "direction": "改为当前结果支持项目内描述性报告，但不构成框架外部效度或评分过程独立验证。",
    },
    {
        "audit_id": "STATE-05",
        "file": "08_manuscript/02_theory.md",
        "needle": "分歧裁决和正式手册冻结",
        "decision": "修订",
        "evidence": "04_framework/；07_analysis/results/formal_rater_r01/correction_v1/",
        "direction": "表内改为已归档的裁决与版本化编码表，并另列文献理论依据与外部效度仍待补足。",
    },
    {
        "audit_id": "STATE-06",
        "file": "08_manuscript/03_methods.md",
        "needle": "154条正式编码前需人工校对的问题",
        "decision": "修订",
        "evidence": "R01 A/B/C/D组回填、ADJ-01/ADJ-02与09_quality/r01_results_eligibility_qa_v1.csv",
        "direction": "从“正式编码前待处理”改为历史校对队列及其已接收的R01核对/补证状态；第35届分值边界仍单列未闭合。",
    },
    {
        "audit_id": "STATE-07",
        "file": "08_manuscript/03_methods.md",
        "needle": "尚未完成真实双评分者编码和正式分歧裁决",
        "decision": "修订",
        "evidence": "07_analysis/data/final_coding_r01_correction_v1.csv；09_quality/r01_results_eligibility_qa_v1.csv",
        "direction": "改为已形成R01当前版本化编码和描述性结果；身份、独立性与实际过程不可由项目独立验证。",
    },
    {
        "audit_id": "STATE-08",
        "file": "08_manuscript/01_introduction.md",
        "needle": "尚未完成原书全文阅读和关键页码摘录",
        "decision": "保留",
        "evidence": "08_manuscript/reference_readiness_register.csv；02_literature/solo_fulltext_access_audit.md",
        "direction": "保留SOLO全文缺口和“SOLO启发”保守表述。",
    },
    {
        "audit_id": "STATE-09",
        "file": "08_manuscript/01_introduction.md",
        "needle": "没有真实教师或课堂证据",
        "decision": "保留",
        "evidence": "05_fieldwork/；06_teaching_validation/；08_manuscript/05_cases_and_diagnosis.md",
        "direction": "保留教学转化只能回答设计建议、不能回答是否有效的限制。",
    },
    {
        "audit_id": "STATE-10",
        "file": "08_manuscript/06_conclusion.md",
        "needle": "第35届分值边界仍无正式来源",
        "decision": "保留",
        "evidence": "09_quality/r01_results_eligibility_qa_v1.csv（RE-QA-B4）；D组更正说明",
        "direction": "保留不进行第35届分值加权或分值比较的限制。",
    },
]


def main() -> None:
    rows = []
    for check in CHECKS:
        path = ROOT / check["file"]
        matches = [number for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1) if check["needle"] in line]
        rows.append({
            "audit_id": check["audit_id"],
            "file": check["file"],
            "line_numbers": ";".join(map(str, matches)) or "未命中：需人工确认",
            "current_phrase": check["needle"],
            "decision": check["decision"],
            "authoritative_evidence": check["evidence"],
            "rewrite_or_retention_direction": check["direction"],
            "check_status": "通过" if len(matches) == 1 else f"异常：命中{len(matches)}处",
        })
    with OUTPUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    revisions = sum(row["decision"] == "修订" for row in rows)
    retained = sum(row["decision"] == "保留" for row in rows)
    exceptions = [row["audit_id"] for row in rows if row["check_status"] != "通过"]
    OUTPUT_MD.write_text(
        "# G8-04-R01-STATE-RECONCILIATION：六章状态措辞对账（V1）\n\n"
        "## 结论\n\n"
        f"本轮登记 {len(rows)} 条状态性措辞：{revisions} 条应修订，{retained} 条应保留。"
        "R01结果资格 QA 已支持项目内、可追溯的描述性结果报告；它不支持评分过程的独立验证、框架外部效度、学生能力、教学效果或因果结论。\n\n"
        "## 应修订的范围\n\n"
        "第一、二、三章中仍将当前 R01 编码、裁决或描述性结果写成“未开始/未形成/必须等待”的文字，应在后续正文修订时改为实际归档状态，并同步保留自声明与外部效度边界。\n\n"
        "## 必须保留的缺口\n\n"
        "SOLO全文阅读与关键页码、教师/课堂真实证据、第35届正式分值来源仍未闭合，不能因R01描述性结果通过而删除。\n\n"
        "## 下一步\n\n"
        "使用同名 CSV 逐条修订章节，并运行 R01 结果资格 QA、引文追溯和 Word 工作稿生成器。\n",
        encoding="utf-8",
    )
    if exceptions:
        raise SystemExit("状态措辞定位异常：" + ", ".join(exceptions))
    print(f"状态对账通过：{revisions} 条修订，{retained} 条保留。")


if __name__ == "__main__":
    main()
