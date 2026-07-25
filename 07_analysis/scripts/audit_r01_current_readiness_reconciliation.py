#!/usr/bin/env python3
"""Reconcile the original G1-G10 readiness gates with current R01 artifacts."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUTPUT_CSV = ROOT / "09_quality/r01_current_readiness_reconciliation_20260725.csv"
OUTPUT_MD = ROOT / "09_quality/r01_current_readiness_reconciliation_20260725.md"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def all_pass(path: Path) -> bool:
    return all(row.get("status") == "通过" for row in read_rows(path))


def main() -> None:
    item_rows = read_rows(ROOT / "03_corpus/item_index.csv")
    review_rows = read_rows(ROOT / "03_corpus/manual_review_checklist.csv")
    review_statuses = Counter(row["review_status"] for row in review_rows)
    score_review_rows = [row for row in review_rows if row["issue_type"] == "第35届分值边界复核"]
    score_rubric_rows = read_rows(ROOT / "03_corpus/cpho35_score_rubric_v1.csv")
    score_rubric_qa = ROOT / "09_quality/cpho35_score_rubric_qa_v1.csv"
    score_sensitivity_qa = ROOT / "09_quality/cpho35_score_weighted_sensitivity_qa_v1.csv"
    rater_a = read_rows(ROOT / "07_analysis/data/rater_returns/incoming/R01/formal_coding_rater_A_FILLED_20260722.csv")
    rater_b = read_rows(ROOT / "07_analysis/data/rater_returns/incoming/R01/formal_coding_rater_B_FILLED_20260722.csv")
    final_coding = read_rows(ROOT / "07_analysis/data/final_coding_r01_correction_v1.csv")
    closure_rows = read_rows(ROOT / "09_quality/r01_citation_closure_readiness_20260725.csv")
    candidate_rows = read_rows(ROOT / "09_quality/r01_candidate_bibliographic_readiness_20260725.csv")
    pending_sources = [row for row in closure_rows if row["closure_status"] == "待补全文/不得升级"]
    planning_sources = [row for row in closure_rows if row["closure_status"] == "计划性待补文献（不计正文引文）"]
    candidate_count = len(candidate_rows)
    final_reference_ready = sum(row["final_reference_ready"] == "是" for row in candidate_rows)

    qa_paths = {
        "结果资格": ROOT / "09_quality/r01_results_eligibility_qa_v1.csv",
        "第四章整合": ROOT / "09_quality/r01_results_manuscript_integration_qa_v2.csv",
        "结论对齐": ROOT / "09_quality/r01_conclusion_rq_alignment_qa_v1.csv",
        "章节就绪度": ROOT / "09_quality/manuscript_chapter_readiness_matrix_qa_v1.csv",
    }
    qa_state = "; ".join(f"{name}{'通过' if all_pass(path) else '待复核'}" for name, path in qa_paths.items())

    rows = [
        {
            "gate": "G1 语料与校对",
            "current_status": "部分解除",
            "current_evidence": f"{len(item_rows)}个分析单元；154项校对记录中："
            f"{review_statuses['整合QA通过：正式编码输入候选']}项编码输入候选、"
            f"{review_statuses['整合QA通过：图件候选（非论文定稿）']}项图件候选、"
            f"{review_statuses['整合QA通过：题解图边界候选']}项题解图边界候选、"
            f"{review_statuses['未关闭：待正式评分细则或原卷分值说明']}项原始副本分值边界未关闭。",
            "still_missing": f"校对过程仅按R01回填声明登记；{len(score_review_rows)}项原题面/答案副本分值边界仍未关闭。另有{len(score_rubric_rows)}行E1评分台账（台账QA={'通过' if all_pass(score_rubric_qa) else '待复核'}；敏感性QA={'通过' if all_pass(score_sensitivity_qa) else '待复核'}），其发布/官方版本链未独立核验。",
            "cannot_claim": "不能把过程声明写成项目独立认证；不能把E1评分台账写成独立核验的官方细则，也不能做跨届正式分值比较。",
        },
        {
            "gate": "G2 理论与文献",
            "current_status": "未定稿",
            "current_evidence": f"正文来源41项、出现77次；{candidate_count}项候选著录结构性就绪。",
            "still_missing": f"实际论证引文待补{len(pending_sources)}项；另有{len(planning_sources)}项计划性待补来源（" + "、".join(row["source_id"] for row in planning_sources) + "）可在获得全文后决定是否纳入综述。",
            "cannot_claim": "不能把候选参考文献表、摘要、目录或计划性待补提及写成完整综述或最终参考文献。",
        },
        {
            "gate": "G3 框架开发",
            "current_status": "项目内可用，外部效度未闭合",
            "current_evidence": "编码手册、边界案例、R01编码和裁决链已形成，并用于当前统计。",
            "still_missing": "真实专家审查、导师取舍确认及框架外部效度证据未提供。",
            "cannot_claim": "不能称框架已获专家验证或具有外部效度。",
        },
        {
            "gate": "G4 双评分者编码与裁决",
            "current_status": "项目内可复算，过程不可独立认证",
            "current_evidence": f"RATER-A {len(rater_a)}行、RATER-B {len(rater_b)}行、当前裁决/更正编码 {len(final_coding)}行；{qa_state}。",
            "still_missing": "评分者身份、互盲和独立编码过程仅有声明，项目无法独立验证。",
            "cannot_claim": "不能把回填声明扩展为经项目独立认证的人工过程或框架效度。",
        },
        {
            "gate": "G5 结果可复现",
            "current_status": "项目内达到",
            "current_evidence": "当前编码、证据链、描述统计、图件及第四章结果整合均有脚本与QA。",
            "still_missing": "结果解释仍受语料、编码过程和理论边界限制。",
            "cannot_claim": "不能推出学生能力、因果、显著性、长期趋势或教学效果。",
        },
        {
            "gate": "G6 主张—证据对应",
            "current_status": "部分达到",
            "current_evidence": "来源级关闭清单已定位正文来源和允许用途，候选书目信息审计36/36结构性就绪。",
            "still_missing": f"最终参考文献放行{final_reference_ready}/{candidate_count}；待补来源与逐条学校格式核验仍未关闭。",
            "cannot_claim": "不能称所有文献主张已完成全文、版本、页码和格式终核。",
        },
        {
            "gate": "G7 教学转化/验证",
            "current_status": "仅设计建议可用",
            "current_evidence": "第五章已形成任务、支架、可观察产出与评价入口的设计材料。",
            "still_missing": "未见真实教师访谈、学生作品、课堂实施或经伦理治理的人类参与者数据。",
            "cannot_claim": "不能写教师认可、课堂可行性或教学效果；若采用路线A，应明确收缩为设计建议。",
        },
        {
            "gate": "G8 结论边界",
            "current_status": "内容工作稿达到",
            "current_evidence": "第六章按五个研究问题回应，结论对齐QA通过，并登记了可支持与不可支持范围。",
            "still_missing": "理论全文、教学证据、最终题目与学校要求尚未闭合。",
            "cannot_claim": "不能称论文结论已定稿、已满足优秀论文评定或可提交。",
        },
        {
            "gate": "G9 全文一致与格式",
            "current_status": "工作稿级通过，提交级未开始",
            "current_evidence": "六章工作稿、候选编号引文、V17输入新鲜度和桌面版中文渲染均有项目内QA。",
            "still_missing": "最终GB/T著录、答辩期模板、匿名规则、AI披露、附录与逐页终校未完成。",
            "cannot_claim": "不能称符合学校最终格式、匿名送审或归档要求。",
        },
        {
            "gate": "G10 导师反馈与模拟答辩",
            "current_status": "未提供完成证据",
            "current_evidence": "项目内有审计与修订轨迹，但未见可验证的导师两轮反馈或模拟答辩记录。",
            "still_missing": "需真实反馈记录、修订决定及至少一轮模拟答辩材料。",
            "cannot_claim": "不能称已通过导师反馈、模拟答辩或具有优秀论文资格。",
        },
    ]

    with OUTPUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    lines = [
        "# R01 当前就绪度对账 V2（2026-07-25）",
        "",
        "本表按总方案G1-G10重新读取当前R01文件，不覆盖`g8_09_final_pre_submission_blockers.csv`的准备期历史记录。历史表中“无正式编码/无结果”的项目已被当前回填、裁决、更正与QA文件替代；但回填声明不能被项目自动升级为身份、互盲或独立过程的外部认证。",
        "",
        "| 关卡 | 当前状态 | 最小后续动作 |",
        "|---|---|---|",
    ]
    next_actions = [
        "保留8项原始副本页面边界；若需正式来源链，独立核验E1评分副本的发布/版本链",
        "维持已读来源闭环；获得5项计划性待补全文后再决定是否纳入综述",
        "取得真实专家/导师对框架的反馈，或保持内部框架表述",
        "保留自声明与项目内可复算的区分",
        "维持当前描述性解释边界",
        "完成全文、版本/页码与学校格式终核",
        "确认路线A收缩或采集真实教学证据",
        "待上述证据闭合后再定稿结论",
        "取得学校当期规范并生成终稿材料",
        "取得真实导师反馈与模拟答辩记录",
    ]
    for row, action in zip(rows, next_actions):
        lines.append(f"| {row['gate']} | {row['current_status']} | {action} |")
    lines.extend([
        "",
        "当前可交付物是：可复算、限边界的六章非提交工作稿和研究材料包。它不是最终提交论文，更不能据此宣称已满足学校格式、导师确认、课堂验证或优秀论文评定条件。",
    ])
    OUTPUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"R01当前就绪度对账：{len(rows)}个G1-G10关卡已登记。")


if __name__ == "__main__":
    main()
