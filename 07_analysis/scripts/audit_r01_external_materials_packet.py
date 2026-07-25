#!/usr/bin/env python3
"""Build a current external-material gap packet without upgrading project-internal evidence."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUTPUT_CSV = ROOT / "09_quality/r01_external_materials_packet_20260725.csv"
OUTPUT_MD = ROOT / "09_quality/r01_external_materials_packet_20260725.md"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def all_pass(path: Path) -> bool:
    return all(row.get("status") == "通过" for row in read_rows(path))


def main() -> None:
    final_coding = read_rows(ROOT / "07_analysis/data/final_coding.csv")
    citation_rows = read_rows(ROOT / "09_quality/r01_citation_closure_readiness_20260725.csv")
    candidate_rows = read_rows(ROOT / "09_quality/r01_candidate_bibliographic_readiness_20260725.csv")
    score_rows = read_rows(ROOT / "03_corpus/cpho35_score_rubric_v1.csv")
    fieldwork_rows = read_rows(ROOT / "05_fieldwork/data_collection_log.csv")
    classroom_rows = read_rows(ROOT / "06_teaching_validation/classroom_data_manifest.csv")

    qa_paths = {
        "结果资格": ROOT / "09_quality/r01_results_eligibility_qa_v1.csv",
        "第四章整合": ROOT / "09_quality/r01_results_manuscript_integration_qa_v2.csv",
        "结论对齐": ROOT / "09_quality/r01_conclusion_rq_alignment_qa_v1.csv",
        "章节就绪度": ROOT / "09_quality/manuscript_chapter_readiness_matrix_qa_v1.csv",
    }
    qa_summary = "；".join(f"{name}={'通过' if all_pass(path) else '待复核'}" for name, path in qa_paths.items())
    citation_pending_ids = [row["source_id"] for row in citation_rows if row["closure_status"] == "待补全文/不得升级"]
    planning_ids = [row["source_id"] for row in citation_rows if row["closure_status"] == "计划性待补文献（不计正文引文）"]
    final_reference_ready = sum(row["final_reference_ready"] == "是" for row in candidate_rows)

    rows = [
        {
            "packet_id": "EXT-01",
            "workstream": "项目内编码与结果",
            "current_status": "已有项目内可复算版本；不需重新收集",
            "current_evidence": f"final_coding.csv={len(final_coding)}行；{qa_summary}",
            "external_material_needed": "无新增材料；仅在正式对外使用时保留评分者身份、互盲和独立过程不可独立认证的边界。",
            "acceptance_condition": "不得把已有回填声明升级为外部认证；无需重复编码以替代当前版本。",
            "cannot_claim": "不能称评分过程已获项目外独立认证或框架外部效度已闭合。",
        },
        {
            "packet_id": "EXT-02",
            "workstream": "核心理论与方法全文",
            "current_status": f"实际待补引文{len(citation_pending_ids)}项；计划性待补{len(planning_ids)}项",
            "current_evidence": "计划性待补来源：" + "、".join(planning_ids),
            "external_material_needed": "若拟扩展第二章综述，通过学校数据库、馆际互借、出版社授权或合法馆藏获取5项全文/关键章节；逐项登记获取渠道、阅读页码、支持主张和不可迁移边界。",
            "acceptance_condition": "全文或关键章节实际可读，且页码记录与论文具体主张对应；题录、摘要和搜索片段不接受。",
            "cannot_claim": "不能把候选题录或摘要写成已读综述或最终引文。",
        },
        {
            "packet_id": "EXT-03",
            "workstream": "参考文献终核",
            "current_status": f"候选{len(candidate_rows)}项；最终放行{final_reference_ready}/{len(candidate_rows)}",
            "current_evidence": "候选著录结构审计通过，但每项保留全文、版本/页码或学校格式事项。",
            "external_material_needed": "补每项实际使用版本、可访问来源/馆藏信息、引用页码，并取得学校当前参考文献格式要求。",
            "acceptance_condition": "每条正文引文均有已读来源和页码，且按学校要求生成终表。",
            "cannot_claim": "不能把候选编号引文或BibTeX工作表写成最终参考文献。",
        },
        {
            "packet_id": "EXT-04",
            "workstream": "第35届评分细则发布链",
            "current_status": f"已有{len(score_rows)}条E1评分台账；发布链未独立核验",
            "current_evidence": "双来源对账7/7通过；8项原题面/答案副本页面边界仍未关闭。",
            "external_material_needed": "可独立核验的官方附件、命题组/竞委会来源或合法馆藏版本，并与现有28页副本逐页对照。",
            "acceptance_condition": "记录稳定来源、版本信息、获取日期和逐页一致/差异结论；不得覆盖E1历史登记。",
            "cannot_claim": "不能把用户提供副本写成已独立核验的官方评分细则。",
        },
        {
            "packet_id": "EXT-05",
            "workstream": "框架外部反馈与题目路线",
            "current_status": "未见真实导师/专家反馈记录或最终题目确认",
            "current_evidence": "当前框架为项目内可用；路线A为内部稳健收缩建议。",
            "external_material_needed": "导师或真实相关领域专家的书面反馈；至少涵盖研究题目、SOLO边界、四维度规则、结果解释和第五章路线。",
            "acceptance_condition": "保留日期、反馈者角色/专业关系、具体意见、原始载体位置及逐条处理决定。",
            "cannot_claim": "不能称框架已获专家验证、导师已确认题目或路线已正式批准。",
        },
        {
            "packet_id": "EXT-06",
            "workstream": "教学转化路径",
            "current_status": f"教师/课堂登记均为空（fieldwork={len(fieldwork_rows)}行；classroom={len(classroom_rows)}行）",
            "current_evidence": "现有第五章只能作为教学转化设计与证据需求，不含真实人类参与者材料。",
            "external_material_needed": "二选一：A. 形成收缩决定，仅保留设计建议；B. 先完成伦理/同意、再采集真实教师反馈或课堂实施、学生作品和匿名化记录。",
            "acceptance_condition": "路线决定有作者/导师记录；若采证，原始材料、同意、匿名化、实施偏离和分析规则完整。",
            "cannot_claim": "不能写教师认可、课堂可行性、学生困难诊断或教学效果。",
        },
        {
            "packet_id": "EXT-07",
            "workstream": "学校提交规范",
            "current_status": "公开基线已登记；当期学院/专业学位执行规则未闭合",
            "current_evidence": "V17为非提交工作稿，学校格式、匿名、AI披露与归档规则均未终核。",
            "external_material_needed": "学院当期专业学位模板、提交通知、匿名评审规则、AI使用披露与伦理/数据管理要求。",
            "acceptance_condition": "将正式文件版本、发布日期和适用范围登记到格式台账，并完成Word/PDF逐页核验。",
            "cannot_claim": "不能称当前工作稿符合当期提交、匿名送审或归档要求。",
        },
    ]

    with OUTPUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    lines = [
        "# R01当前外部材料与人工回填包（2026-07-25）",
        "",
        "## 使用前提",
        "",
        "本包以当前R01版本为准，专门纠正旧准备期材料中“正式编码、裁决、结果表尚未生成”的过时表述。当前已有876行唯一分析表与项目内结果QA；本包不把这些QA升级为评分者身份、互盲、独立编码过程或框架外部效度的认证。",
        "",
        "## 当前需要外部材料的事项",
        "",
        "| 编号 | 事项 | 当前状态 | 交付物 |",
        "|---|---|---|---|",
    ]
    for row in rows:
        lines.append(f"| {row['packet_id']} | {row['workstream']} | {row['current_status']} | {row['external_material_needed']} |")
    lines.extend([
        "",
        "## 通用回填格式",
        "",
        "每项外部材料请另存原始载体，并建立一份回填说明，至少填写：材料编号、提供者角色（不必公开姓名）、取得日期、来源/文件位置、适用范围、可支持的具体论文主张、不能支持的结论、与现有文本的处理决定。不得用智能体生成的意见、搜索摘要或模板文本替代真实材料。",
        "",
        "## 最小顺序",
        "",
        "1. 先完成EXT-05中的路线与框架反馈，决定第五章是收缩为设计建议，还是依法采集真实教学证据。",
        "2. 并行完成EXT-02和EXT-03，优先补5项待全文来源及其页码。",
        "3. 若论文需要正式引用第35届分值，再执行EXT-04；否则维持现有受限敏感性分析。",
        "4. 在提交前取得EXT-07，再进行终稿Word/PDF、匿名版和AI披露处理。",
        "",
        "本包不要求重新处理219个分析单元、876行裁决编码或现有第四章项目内结果；它只列出当前无法由项目内部文件自行补齐的证据。",
    ])
    OUTPUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"R01外部材料包：{len(rows)}项已登记；当前唯一分析表={len(final_coding)}行。")


if __name__ == "__main__":
    main()
