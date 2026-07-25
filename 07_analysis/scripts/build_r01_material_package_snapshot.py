#!/usr/bin/env python3
"""Build and validate a checksum manifest for the current non-submission R01 package."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = ROOT / "10_outputs/material_package"
MANIFEST = OUTPUT_DIR / "R01_current_material_package_manifest_v1.csv"
README = OUTPUT_DIR / "README.md"

ARTIFACTS = [
    ("PKG-01", "语料索引", "03_corpus/item_index.csv", "冻结语料范围与分析单位", "可随材料包提供"),
    ("PKG-02", "当前编码", "07_analysis/data/final_coding_r01_correction_v1.csv", "876条当前版本化编码", "可随材料包提供"),
    ("PKG-03", "编码证据链", "07_analysis/data/final_coding_evidence_r01_v1.csv", "876条题干—解答定位证据", "可随材料包提供"),
    ("PKG-04", "描述统计", "07_analysis/results/formal_rater_r01/correction_v1/final_dimension_presence.csv", "维度出现分布", "可随材料包提供"),
    ("PKG-05", "描述统计", "07_analysis/results/formal_rater_r01/correction_v1/final_level_distribution.csv", "等级分布", "可随材料包提供"),
    ("PKG-06", "描述统计", "07_analysis/results/formal_rater_r01/correction_v1/final_dimension_cooccurrence.csv", "维度共现", "可随材料包提供"),
    ("PKG-07", "结果图件", "08_manuscript/figures/figure_4_1_dimension_presence_r01_v1.png", "维度出现图", "可随材料包提供"),
    ("PKG-08", "结果图件", "08_manuscript/figures/figure_4_2_level_distribution_r01_v1.png", "等级分布图", "可随材料包提供"),
    ("PKG-09", "正文", "08_manuscript/01_introduction.md", "第一章工作稿", "可随材料包提供；非最终稿"),
    ("PKG-10", "正文", "08_manuscript/02_theory.md", "第二章工作稿", "可随材料包提供；非最终稿"),
    ("PKG-11", "正文", "08_manuscript/03_methods.md", "第三章工作稿", "可随材料包提供；非最终稿"),
    ("PKG-12", "正文", "08_manuscript/04_results.md", "第四章工作稿", "可随材料包提供；非最终稿"),
    ("PKG-13", "正文", "08_manuscript/05_cases_and_diagnosis.md", "第五章工作稿", "可随材料包提供；非最终稿"),
    ("PKG-14", "正文", "08_manuscript/06_conclusion.md", "第六章工作稿", "可随材料包提供；非最终稿"),
    ("PKG-15", "候选引文", "08_manuscript/07_candidate_references.md", "36项限边界候选参考文献", "可随材料包提供；非最终参考文献表"),
    ("PKG-16", "质量保证", "09_quality/r01_results_eligibility_qa_v1.csv", "51项结果资格检查", "可随材料包提供"),
    ("PKG-17", "质量保证", "09_quality/r01_case_reselection_qa_v1.csv", "7项案例检查", "可随材料包提供"),
    ("PKG-18", "质量保证", "09_quality/r01_citation_trace_v1.csv", "正文来源追溯", "可随材料包提供"),
    ("PKG-19", "质量保证", "09_quality/current_material_package_audit_v2.md", "材料包范围与未闭合条件", "可随材料包提供"),
    ("PKG-20", "复现入口", "07_analysis/reproducibility_protocol.md", "推荐复跑顺序", "可随材料包提供"),
    ("PKG-21", "工作稿", "10_outputs/drafts/ECNU_非全日制专硕论文工作稿_R01_v17.docx", "当前Word工作稿", "仅本地工作稿；不得作为最终提交或公开分发件"),
    ("PKG-22", "质量保证", "09_quality/r01_results_manuscript_integration_qa_v2.csv", "第四章当前结果与图件整合QA", "可随材料包提供；V1仅为更正前历史基线"),
    ("PKG-23", "正文", "08_manuscript/00_abstract_content_draft.md", "中文摘要内容工作底稿", "可随材料包提供；非最终学校格式摘要"),
    ("PKG-24", "质量保证", "09_quality/r01_abstract_alignment_qa_v1.csv", "中文摘要与冻结结果对齐QA", "可随材料包提供；不验证英文摘要或学校格式"),
    ("PKG-25", "正文", "08_manuscript/00_abstract_en_content_draft.md", "英文摘要内容工作底稿", "可随材料包提供；非最终学校格式或官方术语版本"),
    ("PKG-26", "质量保证", "09_quality/r01_abstract_alignment_qa_v1.md", "中英文摘要与冻结结果对齐QA说明", "可随材料包提供；不验证学校格式或官方英文赛事名"),
    ("PKG-27", "定位与格式", "01_positioning/competition_english_terminology_verification.md", "赛事英文术语核验记录", "可随材料包提供；描述性工作译法不等于官方赛事名称"),
    ("PKG-28", "定位与格式", "09_quality/ecnu_professional_format_reconciliation_20260725.md", "非全日制专业学位公开格式基线对账", "可随材料包提供；不构成当期学院提交确认"),
    ("PKG-29", "质量保证", "09_quality/r01_current_chapter_evidence_audit_v1.csv", "当前章节证据审计记录", "可随材料包提供；不验证人工过程或外部事实"),
    ("PKG-30", "质量保证", "09_quality/r01_current_chapter_evidence_audit_v1.md", "当前章节证据审计说明", "可随材料包提供；第二章文献与旧主张矩阵仍待处理"),
    ("PKG-31", "教学设计", "06_teaching_validation/teaching_design_matrix.md", "R01结果到待实施教学设计的转化矩阵", "可随材料包提供；未收集学生或教师问题证据"),
    ("PKG-32", "教学设计", "06_teaching_validation/r01_design_case_01_condition_relation_chain.md", "条件—关系链教学设计案例", "可随材料包提供；未实施，不证明教学效果"),
    ("PKG-33", "教学设计", "06_teaching_validation/r01_design_case_02_state_energy_classification.md", "状态分类—平均能量关系教学设计案例", "可随材料包提供；未实施，不证明教学效果"),
    ("PKG-34", "质量保证", "09_quality/r01_teaching_design_materials_qa_v1.csv", "教学设计材料QA", "可随材料包提供；只验证项目内可追溯性与边界"),
    ("PKG-35", "教学设计", "06_teaching_validation/student_artifact_rubric.md", "R01学生作品过程性观察记录量规", "可随材料包提供；未验证设计工具，不含学生数据"),
    ("PKG-36", "教学设计", "06_teaching_validation/r01_student_artifact_observation_record_template.csv", "学生作品观察记录空白模板", "可随材料包提供；空白模板，不含个人或课堂数据"),
    ("PKG-37", "质量保证", "09_quality/r01_student_artifact_observation_rubric_qa_v1.csv", "学生作品观察记录量规QA", "可随材料包提供；只验证工具边界与模板为空"),
    ("PKG-38", "文献核验", "02_literature/reference_verification.csv", "来源可读状态、限定用途和待核边界", "可随材料包提供；工作核验台账，不是最终参考文献表"),
    ("PKG-39", "文献核验", "02_literature/physics_competition_page_level_claim_map_v1.csv", "五篇国内竞赛研究的14条页码级主张映射", "可随材料包提供；用户提供来源的E1页码映射，不验证外部发布链"),
    ("PKG-40", "质量保证", "09_quality/pcomp_candidate_citation_integration_qa_v1.csv", "国内竞赛研究第二章与候选引文受控接入QA", "可随材料包提供；只验证项目内接入与边界"),
    ("PKG-41", "文献核验", "09_quality/core_literature_status_reconciliation_20260725.md", "SOLO与国内竞赛核心来源当前可读状态对账", "可随材料包提供；不验证副本授权、外部发布链或理论效度"),
    ("PKG-42", "文献核验", "02_literature/core_source_public_metadata_recheck_20260725.md", "SOLO与两篇竞赛文献公开元数据复核", "可随材料包提供；不以题录或摘要替代全文阅读"),
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows() -> list[dict[str, str]]:
    result = []
    for artifact_id, group, relative_path, purpose, boundary in ARTIFACTS:
        path = ROOT / relative_path
        result.append({
            "artifact_id": artifact_id,
            "group": group,
            "relative_path": relative_path,
            "purpose": purpose,
            "distribution_boundary": boundary,
            "exists": "是" if path.is_file() else "否",
            "sha256": sha256(path) if path.is_file() else "",
        })
    return result


def build() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest_rows = rows()
    with MANIFEST.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(manifest_rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(manifest_rows)
    README.write_text(
        "# R01 当前材料包快照与内部交接入口\n\n"
        "`R01_current_material_package_manifest_v1.csv` 是当前非提交材料包的校验清单，不是最终论文提交包。"
        "CSV逐项记录文件用途、分发边界与SHA-256。复跑方法见 `07_analysis/reproducibility_protocol.md`；"
        "未闭合条件见 `09_quality/current_material_package_audit_v2.md`。\n\n"
        "运行 `07_analysis/scripts/build_r01_internal_material_package.py --force` 可生成 `R01_internal_handoff_v1/`："
        f"默认复制{len([row for row in manifest_rows if row['distribution_boundary'].startswith('可随材料包提供')])}项允许内部交接的材料，并保留来源路径和SHA-256；不含原始试卷/解答、受限文献全文、私人数据或V17。"
        "该目录只用于项目内部交接和复现，不是公开发布包、匿名送审包、答辩包或正式提交包。\n\n"
        "原始试卷与解答的权利状态、学校格式、真实参与者材料和V17工作稿的提交资格均不因本清单而改变。\n",
        encoding="utf-8",
    )
    print(f"已生成材料包快照：{len(manifest_rows)}项。")


def validate() -> None:
    with MANIFEST.open(encoding="utf-8-sig", newline="") as handle:
        manifest_rows = list(csv.DictReader(handle))
    failures = []
    for row in manifest_rows:
        path = ROOT / row["relative_path"]
        if not path.is_file() or row["exists"] != "是" or sha256(path) != row["sha256"]:
            failures.append(row["artifact_id"])
    if failures:
        raise SystemExit("材料包快照校验失败：" + ", ".join(failures))
    print(f"材料包快照校验：{len(manifest_rows)}/{len(manifest_rows)}通过")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--validate", action="store_true")
    args = parser.parse_args()
    validate() if args.validate else build()
