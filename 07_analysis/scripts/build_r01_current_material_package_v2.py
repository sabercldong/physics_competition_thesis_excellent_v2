#!/usr/bin/env python3
"""Create a hash-only V2 snapshot for the current non-submission R01 package."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = ROOT / "10_outputs/material_package"
MANIFEST = OUTPUT_DIR / "R01_current_material_package_manifest_v2.csv"
README = OUTPUT_DIR / "README_v2.md"

ARTIFACTS = [
    ("V2-01", "语料索引", "03_corpus/item_index.csv", "219个分析单元的索引", "可随内部材料包提供；非官方原卷"),
    ("V2-02", "当前编码", "07_analysis/data/final_coding_r01_correction_v1.csv", "876条当前编码", "可随内部材料包提供；过程仅按自声明登记"),
    ("V2-03", "编码证据", "07_analysis/data/final_coding_evidence_r01_v1.csv", "876条题干—解答定位证据", "可随内部材料包提供；不含原始试卷"),
    ("V2-04", "结果", "07_analysis/results/formal_rater_r01/correction_v1/final_dimension_presence.csv", "维度出现统计", "可随内部材料包提供；仅描述性结果"),
    ("V2-05", "结果", "07_analysis/results/formal_rater_r01/correction_v1/final_level_distribution.csv", "等级分布统计", "可随内部材料包提供；仅描述性结果"),
    ("V2-06", "结果", "07_analysis/results/formal_rater_r01/correction_v1/final_dimension_cooccurrence.csv", "维度共现统计", "可随内部材料包提供；仅描述性结果"),
    ("V2-07", "图件", "08_manuscript/figures/figure_4_1_dimension_presence_r01_v1.png", "维度出现图", "可随内部材料包提供；非终稿图件"),
    ("V2-08", "图件", "08_manuscript/figures/figure_4_2_level_distribution_r01_v1.png", "等级分布图", "可随内部材料包提供；非终稿图件"),
    ("V2-09", "前置内容", "08_manuscript/00_frontmatter.md", "题名与摘要占位", "可随内部材料包提供；题目待确认"),
    ("V2-10", "前置内容", "08_manuscript/00_abstract_content_draft.md", "中文摘要底稿", "可随内部材料包提供；非学校格式终稿"),
    ("V2-11", "前置内容", "08_manuscript/00_abstract_en_content_draft.md", "英文摘要底稿", "可随内部材料包提供；非学校格式终稿"),
    *[(f"V2-{12 + i:02d}", "正文", f"08_manuscript/{name}", purpose, "可随内部材料包提供；非提交工作稿") for i, (name, purpose) in enumerate([
        ("01_introduction.md", "第一章"), ("02_theory.md", "第二章"), ("03_methods.md", "第三章"),
        ("04_results.md", "第四章"), ("05_cases_and_diagnosis.md", "第五章"), ("06_conclusion.md", "第六章"),
    ])],
    ("V2-18", "候选文献", "08_manuscript/07_candidate_references.md", "39项候选文后表", "可随内部材料包提供；不是最终参考文献"),
    ("V2-19", "工作稿", "10_outputs/drafts/ECNU_非全日制专硕论文工作稿_R01_v18.docx", "V18可读工作稿", "仅本地工作稿；不得提交或公开分发"),
    ("V2-20", "工作稿", "10_outputs/drafts/ECNU_非全日制专硕论文工作稿_R01_v18_inputs.json", "V18输入哈希", "可随内部材料包提供；只说明快照一致性"),
    ("V2-21", "QA", "09_quality/r01_results_eligibility_qa_v1.csv", "结果资格QA", "可随内部材料包提供；不认证过程独立性"),
    ("V2-22", "QA", "09_quality/r01_results_manuscript_integration_qa_v2.csv", "第四章整合QA", "可随内部材料包提供；不判定学校格式"),
    ("V2-23", "QA", "09_quality/r01_conclusion_rq_alignment_qa_v1.csv", "结论研究问题对齐QA", "可随内部材料包提供；不替代终稿审计"),
    ("V2-24", "QA", "09_quality/r01_v18_working_draft_qa_20260725.csv", "V18工作稿QA", "可随内部材料包提供；非中文逐页终校"),
    ("V2-25", "最终化", "09_quality/r01_current_finalization_blockers_20260725_v2.csv", "最终化阻塞总表", "可随内部材料包提供；不构成提交资格"),
    ("V2-26", "最终化", "09_quality/r01_final_reference_action_queue_20260725.csv", "最终参考文献行动队列", "可随内部材料包提供；均未最终放行"),
    ("V2-27", "最终化", "09_quality/r01_final_reference_backfill_template_20260725.csv", "最终参考文献真实核对模板", "可随内部材料包提供；真实字段为空"),
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build() -> None:
    rows = []
    for artifact_id, group, relative_path, purpose, boundary in ARTIFACTS:
        path = ROOT / relative_path
        rows.append({"artifact_id": artifact_id, "group": group, "relative_path": relative_path, "purpose": purpose, "distribution_boundary": boundary, "exists": "是" if path.is_file() else "否", "sha256": digest(path) if path.is_file() else ""})
    if not all(row["exists"] == "是" for row in rows):
        raise SystemExit("V2材料包缺失：" + "、".join(row["artifact_id"] for row in rows if row["exists"] == "否"))
    with MANIFEST.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)
    README.write_text(
        "# R01 当前材料包 V2\n\n"
        f"本清单记录{len(rows)}项当前非提交材料的路径、用途、分发边界与SHA-256，不复制任何文件。"
        "它替代已过期的V1快照作为当前核对入口，但不是公开发布包、匿名送审包或学校提交包。"
        "原始试卷、答案、受限全文、个人信息和回填原件均不纳入。\n",
        encoding="utf-8",
    )
    print(f"V2材料包快照：{len(rows)}项。")


def validate() -> None:
    with MANIFEST.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    failed = [row["artifact_id"] for row in rows if not (ROOT / row["relative_path"]).is_file() or digest(ROOT / row["relative_path"]) != row["sha256"]]
    if len(rows) != len(ARTIFACTS) or failed:
        raise SystemExit("V2材料包校验失败：" + "、".join(failed or ["条目数不一致"]))
    print(f"V2材料包校验：{len(rows)}/{len(rows)}通过。")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--validate", action="store_true")
    args = parser.parse_args()
    validate() if args.validate else build()
