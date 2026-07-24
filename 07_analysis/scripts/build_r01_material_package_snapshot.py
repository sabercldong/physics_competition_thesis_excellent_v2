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
    ("PKG-15", "候选引文", "08_manuscript/07_candidate_references.md", "26项限边界候选参考文献", "可随材料包提供；非最终参考文献表"),
    ("PKG-16", "质量保证", "09_quality/r01_results_eligibility_qa_v1.csv", "51项结果资格检查", "可随材料包提供"),
    ("PKG-17", "质量保证", "09_quality/r01_case_reselection_qa_v1.csv", "7项案例检查", "可随材料包提供"),
    ("PKG-18", "质量保证", "09_quality/r01_citation_trace_v1.csv", "正文来源追溯", "可随材料包提供"),
    ("PKG-19", "质量保证", "09_quality/current_material_package_audit_v2.md", "材料包范围与未闭合条件", "可随材料包提供"),
    ("PKG-20", "复现入口", "07_analysis/reproducibility_protocol.md", "推荐复跑顺序", "可随材料包提供"),
    ("PKG-21", "工作稿", "10_outputs/drafts/ECNU_非全日制专硕论文工作稿_R01_v17.docx", "当前Word工作稿", "仅本地工作稿；不得作为最终提交或公开分发件"),
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
        "# R01 当前材料包快照\n\n"
        "本目录是当前非提交材料包的校验清单，不是最终论文提交包。CSV逐项记录文件用途、分发边界与SHA-256。"
        "复跑方法见 `07_analysis/reproducibility_protocol.md`；未闭合条件见 `09_quality/current_material_package_audit_v2.md`。\n\n"
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
