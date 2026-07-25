#!/usr/bin/env python3
"""Validate page-level domestic-competition entries in the literature matrix."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MATRIX = ROOT / "02_literature/literature_matrix.csv"
PAGE_MAP = ROOT / "02_literature/physics_competition_page_level_claim_map_v1.csv"
OUTPUT_CSV = ROOT / "09_quality/pcomp_literature_matrix_alignment_qa_v1.csv"
OUTPUT_MD = ROOT / "09_quality/pcomp_literature_matrix_alignment_qa_v1.md"

EXPECTED = {
    "LM-PCOMP-002": "PCOMP-002",
    "LM-PCOMP-003": "PCOMP-003",
    "LM-PCOMP-004": "PCOMP-004",
    "LM-PCOMP-007": "PCOMP-007",
    "LM-PCOMP-008": "PCOMP-008",
}


def main() -> None:
    with MATRIX.open(encoding="utf-8-sig", newline="") as handle:
        matrix = {row["id"]: row for row in csv.DictReader(handle)}
    with PAGE_MAP.open(encoding="utf-8-sig", newline="") as handle:
        page_rows = list(csv.DictReader(handle))
    checks = []
    for matrix_id, source_id in EXPECTED.items():
        row = matrix.get(matrix_id, {})
        status = row.get("verification_status", "")
        notes = row.get("notes", "")
        checks.extend([
            (f"{source_id}-LM-01", f"{source_id}矩阵记录存在", "存在", "存在" if row else "缺失", bool(row)),
            (f"{source_id}-LM-02", f"{source_id}登记E1页码级状态", "E1页码级受限可用", status, "E1页码级受限可用" in status),
            (f"{source_id}-LM-03", f"{source_id}链接页码映射", "映射文件", notes, "physics_competition_page_level_claim_map_v1.csv" in notes),
            (f"{source_id}-LM-04", f"{source_id}页码映射仍存在", "至少一条", str(sum(item["source_id"] == source_id for item in page_rows)), any(item["source_id"] == source_id for item in page_rows)),
        ])
    with OUTPUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["check_id", "check_item", "expected", "actual", "status"])
        for check_id, item, expected, actual, passed in checks:
            writer.writerow([check_id, item, expected, actual, "通过" if passed else "不通过"])
    failures = [check_id for check_id, _, _, _, passed in checks if not passed]
    OUTPUT_MD.write_text(
        "# 国内竞赛研究总文献矩阵页码对齐QA（V1）\n\n"
        f"共{len(checks)}项，{'全部通过' if not failures else '不通过：' + '、'.join(failures)}。"
        "本检查仅验证项目内矩阵与页码映射一致，不核验外部发布链，不将用户提供来源升级为E2。\n",
        encoding="utf-8",
    )
    if failures:
        raise SystemExit("国内竞赛研究总文献矩阵页码对齐QA失败：" + ", ".join(failures))
    print(f"国内竞赛研究总文献矩阵页码对齐QA：{len(checks)}/{len(checks)}通过")


if __name__ == "__main__":
    main()
