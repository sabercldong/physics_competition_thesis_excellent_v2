#!/usr/bin/env python3
"""Validate that domestic-competition literature claims retain their page-level limits."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MATRIX = ROOT / "09_quality/claim_evidence_matrix.csv"
PAGE_MAP = ROOT / "02_literature/physics_competition_page_level_claim_map_v1.csv"
OUTPUT_CSV = ROOT / "09_quality/pcomp_claim_matrix_alignment_qa_v1.csv"
OUTPUT_MD = ROOT / "09_quality/pcomp_claim_matrix_alignment_qa_v1.md"


def main() -> None:
    with MATRIX.open(encoding="utf-8-sig", newline="") as handle:
        claims = {row["claim_id"]: row for row in csv.DictReader(handle)}
    with PAGE_MAP.open(encoding="utf-8-sig", newline="") as handle:
        page_rows = list(csv.DictReader(handle))

    c2 = claims.get("C2-05", {})
    c1 = claims.get("C1-05", {})
    checks = [
        ("PCOMP-CM-QA-01", "C2-05存在", "存在", "存在" if c2 else "缺失", bool(c2)),
        ("PCOMP-CM-QA-02", "C2-05使用E1", "E1", c2.get("evidence_level", ""), c2.get("evidence_level") == "E1"),
        ("PCOMP-CM-QA-03", "C2-05连接页码映射", "映射路径", c2.get("evidence_file", ""), "physics_competition_page_level_claim_map_v1.csv" in c2.get("evidence_file", "")),
        ("PCOMP-CM-QA-04", "C2-05保留非空白证明边界", "不得宣称证明空白", c2.get("risk", ""), "不能据此宣称已证明研究空白" in c2.get("risk", "")),
        ("PCOMP-CM-QA-05", "C1-05反映已读五篇与未读两篇", "002/003/004/007/008已读；001/005未读", c1.get("evidence_location", ""), all(token in c1.get("evidence_location", "") for token in ["002/003/004/007/008", "001/005未读"])),
        ("PCOMP-CM-QA-06", "C1-05仍为研究空白候选", "研究空白候选", c1.get("claim_type", ""), c1.get("claim_type") == "研究空白候选" and c1.get("evidence_level") == "E1"),
        ("PCOMP-CM-QA-07", "页码映射覆盖五份来源", "5个来源、至少14条", f"{len({row['source_id'] for row in page_rows})}个来源、{len(page_rows)}条", len({row["source_id"] for row in page_rows}) == 5 and len(page_rows) >= 14),
    ]
    with OUTPUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["check_id", "check_item", "expected", "actual", "status"])
        for check_id, item, expected, actual, passed in checks:
            writer.writerow([check_id, item, expected, actual, "通过" if passed else "不通过"])
    failures = [check_id for check_id, _, _, _, passed in checks if not passed]
    OUTPUT_MD.write_text(
        "# 国内竞赛研究主张矩阵对齐QA（V1）\n\n"
        f"共{len(checks)}项，{'全部通过' if not failures else '不通过：' + '、'.join(failures)}。"
        "本检查只验证页码映射、研究空白候选状态和不可外推边界的一致性；不验证出版链、框架效度、学生成绩或教学结论。\n",
        encoding="utf-8",
    )
    if failures:
        raise SystemExit("主张矩阵对齐QA失败：" + ", ".join(failures))
    print(f"国内竞赛研究主张矩阵对齐QA：{len(checks)}/{len(checks)}通过")


if __name__ == "__main__":
    main()
