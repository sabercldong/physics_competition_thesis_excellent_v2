#!/usr/bin/env python3
"""Reconcile current R01 submission and quality blockers without reopening legacy gates."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUTPUT_CSV = ROOT / "09_quality/r01_current_finalization_blockers_20260725.csv"
OUTPUT_MD = ROOT / "09_quality/r01_current_finalization_blockers_20260725.md"
OUTPUT_QA_CSV = ROOT / "09_quality/r01_current_finalization_blockers_qa_v1.csv"
OUTPUT_QA_MD = ROOT / "09_quality/r01_current_finalization_blockers_qa_v1.md"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    fieldnames: list[str] = []
    for row in rows:
        for fieldname in row:
            if fieldname not in fieldnames:
                fieldnames.append(fieldname)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    closure_rows = read_rows(ROOT / "09_quality/r01_citation_closure_readiness_20260725.csv")
    bibliography_rows = read_rows(ROOT / "09_quality/r01_candidate_bibliographic_readiness_20260725.csv")
    pending_citations = [row for row in closure_rows if row["closure_status"] == "待补全文/不得升级"]
    planning_sources = [row for row in closure_rows if row["closure_status"] == "计划性待补文献（不计正文引文）"]
    final_reference_ready = sum(row["final_reference_ready"] == "是" for row in bibliography_rows)

    bases = [
        {
            "record_id": "BASE-01",
            "type": "当前研究基础",
            "current_status": "项目内已形成",
            "item": "唯一分析表与描述性结果",
            "evidence": "07_analysis/data/final_coding.csv；09_quality/r01_results_eligibility_qa_v1.csv；09_quality/r01_results_manuscript_integration_qa_v2.csv",
            "boundary": "可支持当前语料和编码口径下的项目内描述性结果；不认证评分者身份、过程独立性或框架外部效度。",
            "next_action": "保持版本化输入、脚本和结果解释边界。",
        },
        {
            "record_id": "BASE-02",
            "type": "当前研究基础",
            "current_status": "项目内已形成",
            "item": "六章内容工作稿与结论边界",
            "evidence": "08_manuscript/01_introduction.md 至 06_conclusion.md；09_quality/manuscript_chapter_readiness_matrix_20260725.md；09_quality/r01_conclusion_rq_alignment_qa_v1.csv",
            "boundary": "工作稿可用不等于学校终稿、盲审稿、答辩稿或优秀论文资格。",
            "next_action": "只在外部条件关闭后做终稿级改写与格式转换。",
        },
        {
            "record_id": "BASE-03",
            "type": "当前研究基础",
            "current_status": "项目内已形成",
            "item": "可读的非提交Word工作稿",
            "evidence": "10_outputs/drafts/ECNU_非全日制专硕论文工作稿_R01_v17.docx；09_quality/r01_v17_desktop_render_qa_20260725.md",
            "boundary": "桌面抽检不等于逐页终校或学院模板验收。",
            "next_action": "待取得当期规则后，用专硕模板重新排版。",
        },
        {
            "record_id": "BASE-04",
            "type": "当前研究基础",
            "current_status": "正文实际引文已关闭",
            "item": "现有正文的来源级候选引文",
            "evidence": "09_quality/r01_citation_closure_readiness_20260725.csv；09_quality/r01_candidate_bibliographic_readiness_20260725.csv",
            "boundary": f"实际待补正文引文{len(pending_citations)}项；{len(planning_sources)}项仅为后续综述扩展计划；候选条目不等于最终参考文献。",
            "next_action": "按正式文后表标准逐条核验全文、版本、页码与学院格式。",
        },
    ]

    blockers = [
        {
            "record_id": "RFIN-01", "priority": "P0-学术质量", "current_status": "待真实确认",
            "item": "题目与研究路线的作者/导师确认", "why_it_matters": "题目决定第五章采用路线A的收缩表述，还是补充真实教师/课堂证据后升级。",
            "evidence": "01_positioning/route_convergence_memo.md；01_positioning/title_decision.md",
            "minimum_close": "保留真实确认记录，写明最终题目、研究范围、第五章路线和确认日期。",
            "cannot_claim": "不能称导师已确认题目、路线或优秀论文目标。",
        },
        {
            "record_id": "RFIN-02", "priority": "P0-学术质量", "current_status": "外部过程未认证",
            "item": "框架审查与双评分过程的外部确认", "why_it_matters": "当前编码、裁决和结果可复算，但评分者身份、互盲、独立过程及框架外部效度不能由项目内部文件认证。",
            "evidence": "09_quality/r01_current_readiness_reconciliation_20260725.md；04_framework/；07_analysis/results/formal_rater_r01/",
            "minimum_close": "取得真实专家/导师的可追溯反馈；或在终稿继续明确只报告项目内可复算过程。",
            "cannot_claim": "不能称专家验证、独立双评分过程或框架外部效度已经完成。",
        },
        {
            "record_id": "RFIN-03", "priority": "P0-论文范围", "current_status": "待路线决定或真实材料",
            "item": "第五章教学转化的证据路线", "why_it_matters": "没有教师、学生或课堂材料时，第五章只能是基于试题结构的设计建议，不能成为教学验证章。",
            "evidence": "08_manuscript/05_cases_and_diagnosis.md；05_fieldwork/；06_teaching_validation/",
            "minimum_close": "明确采用路线A并收缩为设计建议，或取得合规的真实教师/课堂材料并完成对应分析。",
            "cannot_claim": "不能写教师认可、学生困难诊断、课堂可行性或教学效果。",
        },
        {
            "record_id": "RFIN-04", "priority": "P1-理论定稿", "current_status": "可选扩展材料待阅读",
            "item": "五项计划性待补全文与页码", "why_it_matters": "它们可以扩展第二章的SOLO课程评价、竞赛预赛和方法论比较，但不支撑当前正文论断。",
            "evidence": "09_quality/r01_citation_closure_readiness_20260725.csv；02_literature/literature_matrix.csv",
            "minimum_close": "合法取得并阅读全文，登记页码、允许用途和局限后，再决定是否纳入正文。",
            "cannot_claim": "不能把题录、摘要或计划性待补提及写成已读理论证据。",
        },
        {
            "record_id": "RFIN-05", "priority": "P1-来源链", "current_status": "E1边界保留",
            "item": "第35届评分标准副本的官方版本链", "why_it_matters": "当前评分台账只限本届敏感性分析；官网索引可定位但附件当前不可访问，无法逐文件比对。",
            "evidence": "09_quality/cpho35_score_dual_source_reconciliation_20260725.md；09_quality/cpho35_score_official_origin_audit_20260725.md",
            "minimum_close": "取得可访问的官方附件或其他可核验发布链，并与用户副本比对版本。",
            "cannot_claim": "不能把E1副本称为已逐文件核验的官方评分细则，或做跨届分值结论。",
        },
        {
            "record_id": "RFIN-06", "priority": "P1-参考文献", "current_status": f"最终放行{final_reference_ready}/{len(bibliography_rows)}",
            "item": "最终参考文献、版本与页码终核", "why_it_matters": "候选条目的结构字段完整，不等于正式引用许可、版本一致、页码可复核或学院格式正确。",
            "evidence": "09_quality/r01_candidate_bibliographic_readiness_20260725.md；08_manuscript/reference_readiness_register.csv",
            "minimum_close": "逐条完成全文/版本/页码和正文双向核对，依当期学校格式生成文后表。",
            "cannot_claim": "不能把36项候选清单或V17编号文献当成最终参考文献表。",
        },
        {
            "record_id": "RFIN-07", "priority": "P1-学校规则", "current_status": "公开基线已核，个人当期规则待确认",
            "item": "物理学院实际答辩期的专硕提交规则", "why_it_matters": "封皮、匿名送审、AI披露、提交时间、收件方式与个人信息处理不能由公开基线推定。",
            "evidence": "09_quality/ecnu_professional_format_reconciliation_20260725.md；01_positioning/school_requirements_register.csv",
            "minimum_close": "取得物理学院研究生秘书或官方当期通知，登记模板、流程、匿名和AI披露要求。",
            "cannot_claim": "不能称已符合学校当期格式、匿名要求、AI披露或答辩资格。",
        },
        {
            "record_id": "RFIN-08", "priority": "P1-终稿生产", "current_status": "未开始",
            "item": "基于正式模板的Word/PDF、摘要、附录与逐页终校", "why_it_matters": "V17只验证内部工作稿可读性；正式封面、签名页、摘要字数、前后置材料和逐页版式仍需真实信息与学校模板。",
            "evidence": "10_outputs/drafts/build_r01_working_draft.py；09_quality/ecnu_professional_format_reconciliation_20260725.md",
            "minimum_close": "在RFIN-06/07关闭后，生成正式版和匿名副本，逐页检查并保存排版QA。",
            "cannot_claim": "不能把V17称为最终Word/PDF、匿名版或归档版。",
        },
        {
            "record_id": "RFIN-09", "priority": "P1-导师与答辩", "current_status": "未提供真实记录",
            "item": "导师反馈、修订决定与模拟答辩", "why_it_matters": "优秀论文目标需要经得起外部追问，项目内部审计不能替代真实指导和答辩训练。",
            "evidence": "09_quality/r01_current_readiness_reconciliation_20260725.md",
            "minimum_close": "保存至少两轮真实反馈和修订记录，并完成至少一轮模拟答辩的提问—回应材料。",
            "cannot_claim": "不能称已获导师认可、通过模拟答辩或具备优秀论文资格。",
        },
        {
            "record_id": "RFIN-10", "priority": "P2-提交审计", "current_status": "后置待执行",
            "item": "终稿跨章、图表、参考文献、附录和匿名性审计", "why_it_matters": "终稿产生后仍可能引入编号、版本、个人信息或主张边界不一致。",
            "evidence": "09_quality/r01_current_chapter_evidence_audit_v1.md；09_quality/r01_citation_closure_readiness_20260725.md",
            "minimum_close": "在正式Word/PDF生成后运行终稿主张—证据、引文—文后表、图表—数据和匿名性四类审计。",
            "cannot_claim": "不能称终稿已完成一致性检查或可提交。",
        },
    ]

    rows = bases + blockers
    write_csv(OUTPUT_CSV, rows)

    lines = [
        "# R01 当前最终化阻塞总表（2026-07-25）", "",
        "本表以当前R01材料为准，替代早期准备期文件中“尚无正式编码、结果或第四章”的过时叙述，但不删除历史档案。它将项目内已形成的基础与真正需要外部材料、真实流程或终稿生产才能关闭的条件分开登记。", "",
        "## 已形成的项目内基础", "",
        "| 编号 | 项目 | 状态 | 边界 |", "|---|---|---|---|",
    ]
    for row in bases:
        lines.append(f"| {row['record_id']} | {row['item']} | {row['current_status']} | {row['boundary']} |")
    lines.extend(["", "## 当前阻塞项", "", "| 编号 | 优先级 | 项目 | 当前状态 | 最小关闭条件 |", "|---|---|---|---|---|"])
    for row in blockers:
        lines.append(f"| {row['record_id']} | {row['priority']} | {row['item']} | {row['current_status']} | {row['minimum_close']} |")
    lines.extend([
        "", "## 建议顺序", "",
        "1. 先完成RFIN-01与RFIN-03：确认题目/路线，并明确第五章收缩还是补采真实材料。",
        "2. 处理RFIN-02与RFIN-06：获得真实方法反馈，完成参考文献的全文、版本与页码终核。",
        "3. 处理RFIN-07、RFIN-08、RFIN-09与RFIN-10：按实际答辩期规则生产终稿、匿名版和提交审计。",
        "4. RFIN-04与RFIN-05用于理论和第35届敏感性分析的进一步升级；不应被误报为现有结果或正文实际引文的阻断。",
        "", "因此，当前可交付物仍是限边界的研究材料包与非提交工作稿，不能据此断言学校提交资格、导师确认、教学验证或优秀论文评定已经完成。",
    ])
    OUTPUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    required = [
        ROOT / "07_analysis/data/final_coding.csv",
        ROOT / "09_quality/r01_results_eligibility_qa_v1.csv",
        ROOT / "09_quality/r01_results_manuscript_integration_qa_v2.csv",
        ROOT / "09_quality/manuscript_chapter_readiness_matrix_20260725.md",
        ROOT / "09_quality/r01_citation_closure_readiness_20260725.csv",
        ROOT / "09_quality/r01_candidate_bibliographic_readiness_20260725.csv",
        ROOT / "09_quality/ecnu_professional_format_reconciliation_20260725.md",
    ]
    qa_rows = [{"check_id": f"RFIN-QA-{index:02d}", "check_item": str(path.relative_to(ROOT)), "status": "通过" if path.is_file() else "不通过", "detail": "当前证据文件存在" if path.is_file() else "当前证据文件缺失"} for index, path in enumerate(required, 1)]
    qa_rows.extend([
        {"check_id": "RFIN-QA-08", "check_item": "当前基础记录数", "status": "通过" if len(bases) == 4 else "不通过", "detail": f"{len(bases)}/4"},
        {"check_id": "RFIN-QA-09", "check_item": "当前阻塞记录数", "status": "通过" if len(blockers) == 10 else "不通过", "detail": f"{len(blockers)}/10"},
        {"check_id": "RFIN-QA-10", "check_item": "实际待补正文引文", "status": "通过" if not pending_citations else "不通过", "detail": f"{len(pending_citations)}项（计划性待补{len(planning_sources)}项不计入）"},
        {"check_id": "RFIN-QA-11", "check_item": "历史未编码叙述未写入当前基础", "status": "通过" if all("尚无正式编码" not in row["boundary"] for row in bases) else "不通过", "detail": "基础记录不把当前编码或结果误写为缺失"},
        {"check_id": "RFIN-QA-12", "check_item": "禁写边界完整", "status": "通过" if all(row["cannot_claim"] for row in blockers) else "不通过", "detail": "每项阻塞均含不可声称边界"},
    ])
    write_csv(OUTPUT_QA_CSV, qa_rows)
    failures = [row for row in qa_rows if row["status"] != "通过"]
    OUTPUT_QA_MD.write_text(
        "# R01 当前最终化阻塞总表 QA（V1）\n\n"
        f"{len(qa_rows) - len(failures)}/{len(qa_rows)}通过。"
        "本QA只检查当前证据入口、计数和边界声明；不认证人类过程、外部来源版本、学校资格或优秀论文评定。\n",
        encoding="utf-8",
    )
    if failures:
        raise SystemExit("当前最终化阻塞总表QA失败：" + ", ".join(row["check_id"] for row in failures))
    print(f"R01当前最终化阻塞总表QA：{len(qa_rows)}/{len(qa_rows)}通过；{len(blockers)}项当前阻塞已登记。")


if __name__ == "__main__":
    main()
