#!/usr/bin/env python3
"""Audit current manuscript facts and citation mappings without editing chapters."""

from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CHAPTERS = {
    "introduction": ROOT / "08_manuscript/01_introduction.md",
    "theory": ROOT / "08_manuscript/02_theory.md",
    "methods": ROOT / "08_manuscript/03_methods.md",
    "results": ROOT / "08_manuscript/04_results.md",
    "conclusion": ROOT / "08_manuscript/06_conclusion.md",
}
MAPPING = ROOT / "09_quality/r01_candidate_references_mapping_v1.csv"
OUTPUT_CSV = ROOT / "09_quality/r01_current_worktree_manuscript_reconciliation_20260725.csv"
OUTPUT_MD = ROOT / "09_quality/r01_current_worktree_manuscript_reconciliation_20260725.md"


def placeholders(text: str) -> set[str]:
    values: set[str] = set()
    for contents in re.findall(r"\[引文占位：([^\]]+)\]", text):
        values.update(re.findall(r"[A-Z]+(?:-[A-Z]+)?-\d{3}[A-Z]?", contents))
    return values


def check(check_id: str, subject: str, passed: bool, evidence: str, boundary: str) -> dict[str, str]:
    return {
        "check_id": check_id,
        "subject": subject,
        "result": "通过" if passed else "不通过",
        "evidence": evidence,
        "boundary_or_action": boundary,
    }


def main() -> None:
    text = {name: path.read_text(encoding="utf-8") for name, path in CHAPTERS.items()}
    with MAPPING.open(encoding="utf-8-sig", newline="") as handle:
        mapped_sources = {row["source_id"] for row in csv.DictReader(handle)}

    all_placeholders = set().union(*(placeholders(value) for value in text.values()))
    missing = sorted(all_placeholders - mapped_sources)
    rows = [
        check("CW-01", "正文引文占位映射", not missing,
              f"五章共识别{len(all_placeholders)}个来源ID；未映射={','.join(missing) if missing else '无'}。",
              "只检查候选映射，不把候选参考文献升级为最终文后表。"),
        check("CW-02", "R01分析单位与编码记录", all(token in text["introduction"] for token in ("219个分析单元", "876条当前编码"))
              and all(token in text["methods"] for token in ("219个分析单元", "876条当前编码"))
              and all(token in text["results"] for token in ("219个分析单元", "876条当前R01编码记录")),
              "引言、方法和结果章均以219个分析单元、876条当前记录表述。",
              "该一致性不认证评分者身份、独立性或框架外部效度。"),
        check("CW-03", "裁决版本链", all(token in text["methods"] for token in ("142条分歧", "4条更正", "final_coding_r01_correction_v1.csv"))
              and "ADJ-02四条更正裁决后" in text["results"],
              "方法章与结果章均指向ADJ-02后唯一分析表。",
              "更正前基线和历史输出只能用于版本复现。"),
        check("CW-04", "SOLO-002受控用途", "SOLO-002" in placeholders(text["theory"])
              and "任务要求”和“学生表现”分开" in text["theory"]
              and "不直接给出当前四维编码或L1至L4的效度依据" in text["theory"],
              "第二章45行将SOLO-002限于课程/评价语境中的任务—学生表现边界。",
              "不得据此证明L1至L4、学生水平、教学结论或框架效度。"),
        check("CW-05", "Cohen与Landis受控用途", all(source in placeholders(text["methods"]) for source in ("METH-002", "METH-003"))
              and "不把任何历史区间设为通过线" in text["methods"],
              "第三章60行保留名义分类前提、历史区间的语境限制和不设阈值。",
              "不得用一致性系数证明真实独立过程或框架效度。"),
        check("CW-06", "国内竞赛研究受控用途", all(source in placeholders(text["theory"]) for source in ("PCOMP-002", "PCOMP-003", "PCOMP-004", "PCOMP-007", "PCOMP-008"))
              and "不能直接给出本项目的四维编码" in text["theory"],
              "第二章66至74行将五篇相邻研究限于研究对象、分析路径和透明报告边界。",
              "不得迁移其分布、分值、成绩、难度或教学结论。"),
        check("CW-07", "过程与教学限制", "项目无法独立验证" in text["results"]
              and "不代表学生实际能力，也不代表教学效果" in text["results"]
              and "教学转化仍是设计建议而非效果结论" in text["introduction"],
              "引言和结果章均保留评分过程自声明、学生能力和教学效果限制。",
              "这些限制不得因工作稿可读性提升而删除。"),
        check("CW-08", "理论框架图资源", (ROOT / "08_manuscript/figures/figure_2_1_r01_theoretical_framework_v1.png").is_file()
              and "figure_2_1_r01_theoretical_framework_v1.png" in text["theory"],
              "第二章引用的理论框架PNG在工作区可定位。",
              "只验证文件存在，不评价视觉质量或学校图表格式。"),
    ]

    with OUTPUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    passed = sum(row["result"] == "通过" for row in rows)
    failures = [row["check_id"] for row in rows if row["result"] != "通过"]
    OUTPUT_MD.write_text(
        "# 当前工作区正文对账（2026-07-25）\n\n"
        "## 范围\n\n"
        "本审计仅检查当前第一至四章和第六章的引文占位映射、冻结结果数字、"
        "受控文献用途、限制性表述与理论框架图资源。它不修改正文，不判断外部来源授权，"
        "不认证人工评分过程，也不放行最终参考文献或学位论文格式。\n\n"
        "## 结果\n\n"
        f"{passed}/{len(rows)}项通过。"
        + (" 未通过：" + "、".join(failures) + "。\n" if failures else " 未发现本轮范围内的不同步项。\n")
        + "\n## 保留的定稿门禁\n\n"
        "候选参考文献仍需逐条终核和学院当期格式确认；评分者身份、独立性与实际过程"
        "只能按声明登记；框架外部效度、教师/课堂证据以及教学效果结论均未闭合。\n",
        encoding="utf-8",
    )
    print(f"当前工作区正文对账：{passed}/{len(rows)}通过。")
    if failures:
        raise SystemExit("未通过：" + ", ".join(failures))


if __name__ == "__main__":
    main()
