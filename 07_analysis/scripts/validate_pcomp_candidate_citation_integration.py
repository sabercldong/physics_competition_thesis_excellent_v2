#!/usr/bin/env python3
"""Validate the controlled manuscript/candidate-reference integration for PCOMP sources."""

from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
THEORY = ROOT / "08_manuscript/02_theory.md"
MAPPING = ROOT / "09_quality/g8_02_bib_lite_mapping.csv"
CANDIDATES = ROOT / "09_quality/r01_candidate_references_mapping_v1.csv"
BIB = ROOT / "02_literature/references.bib"
OUTPUT_CSV = ROOT / "09_quality/pcomp_candidate_citation_integration_qa_v1.csv"
OUTPUT_MD = ROOT / "09_quality/pcomp_candidate_citation_integration_qa_v1.md"

EXPECTED = {
    "PCOMP-002": "12/15/24",
    "PCOMP-003": "18/63",
    "PCOMP-004": "1/4",
    "PCOMP-007": "5/15/18",
    "PCOMP-008": "20/23/24/32",
}


def main() -> None:
    theory = THEORY.read_text(encoding="utf-8")
    bib = BIB.read_text(encoding="utf-8")
    with MAPPING.open(encoding="utf-8-sig", newline="") as handle:
        mapping = {row["source_id"]: row for row in csv.DictReader(handle)}
    with CANDIDATES.open(encoding="utf-8-sig", newline="") as handle:
        candidates = {row["source_id"]: row for row in csv.DictReader(handle)}
    start = theory.index("国内竞赛试题研究已呈现不同的分析路径")
    end = theory.index("## 2.4", start)
    section = theory[start:end]
    checks = [
        ("PCOMP-CITE-QA-01", "受控段落位于第2.3节末尾", "2.3后、2.4前", "符合", start > theory.index("## 2.3") and end < theory.index("## 2.4") + len("## 2.4")),
        ("PCOMP-CITE-QA-02", "五项来源都在正文占位中", "5项", str(sum(source_id in section for source_id in EXPECTED)), all(source_id in section for source_id in EXPECTED)),
        ("PCOMP-CITE-QA-03", "正文保留题目与学生表现材料分链", "边界句", "符合" if "题目—参考解答编码与任何未来学生表现材料" in section else "缺失", "题目—参考解答编码与任何未来学生表现材料" in section),
        ("PCOMP-CITE-QA-04", "正文不迁移外部统计或结论", "禁止词不存在", "符合" if not any(token in section for token in ["显著", "证明", "学生能力", "研究空白已"] ) else "不符合", not any(token in section for token in ["显著", "证明", "学生能力", "研究空白已"])),
    ]
    for source_id, pages in EXPECTED.items():
        row = mapping.get(source_id, {})
        candidate = candidates.get(source_id, {})
        bib_key = row.get("bib_key", "")
        checks.extend([
            (f"{source_id}-QA-01", f"{source_id}已允许进入工作候选", "yes", row.get("can_enter_formal_candidate_list", ""), row.get("can_enter_formal_candidate_list") == "yes"),
            (f"{source_id}-QA-02", f"{source_id}候选映射含页码", pages, candidate.get("remaining_verification", ""), pages in candidate.get("remaining_verification", "")),
            (f"{source_id}-QA-03", f"{source_id}BibTeX键存在", bib_key, bib_key, bool(bib_key and re.search(r"^@\w+\{" + re.escape(bib_key) + r",", bib, re.MULTILINE))),
            (f"{source_id}-QA-04", f"{source_id}保留不可迁移说明", "不得", candidate.get("blocked_use", ""), "不得" in candidate.get("blocked_use", "")),
        ])
    with OUTPUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["check_id", "check_item", "expected", "actual", "status"])
        for check_id, item, expected, actual, passed in checks:
            writer.writerow([check_id, item, expected, actual, "通过" if passed else "不通过"])
    failures = [check_id for check_id, _, _, _, passed in checks if not passed]
    OUTPUT_MD.write_text(
        "# 国内竞赛研究候选引文受控接入QA（V1）\n\n"
        f"共{len(checks)}项，{'全部通过' if not failures else '不通过：' + '、'.join(failures)}。"
        "本检查不验证外部发布链、学校最终格式、框架效度、学生成绩或教学结论；五篇来源继续按用户提供、页码可定位的E1工作候选使用。\n",
        encoding="utf-8",
    )
    if failures:
        raise SystemExit("国内竞赛研究候选引文受控接入QA失败：" + ", ".join(failures))
    print(f"国内竞赛研究候选引文受控接入QA：{len(checks)}/{len(checks)}通过")


if __name__ == "__main__":
    main()
