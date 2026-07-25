#!/usr/bin/env python3
"""Validate page-level evidence transfer into the domestic-competition reference register."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REGISTER = ROOT / "02_literature/reference_verification.csv"
PAGE_MAP = ROOT / "02_literature/physics_competition_page_level_claim_map_v1.csv"
OUTPUT_CSV = ROOT / "09_quality/pcomp_reference_verification_alignment_qa_v1.csv"
OUTPUT_MD = ROOT / "09_quality/pcomp_reference_verification_alignment_qa_v1.md"
EXPECTED = {
    "PCOMP-002": ("12/15/24", "26-35届分布"),
    "PCOMP-003": ("18/63", "不能继承成绩"),
    "PCOMP-004": ("1/4", "不能迁移两题判定"),
    "PCOMP-007": ("5/15/18", "不采用预赛统计"),
    "PCOMP-008": ("20/23/24/32", "不采用八因素"),
}


def main() -> None:
    with REGISTER.open(encoding="utf-8-sig", newline="") as handle:
        register = {row["id"]: row for row in csv.DictReader(handle)}
    with PAGE_MAP.open(encoding="utf-8-sig", newline="") as handle:
        page_map = list(csv.DictReader(handle))
    checks = []
    for source_id, (pages, prohibited) in EXPECTED.items():
        row = register.get(source_id, {})
        notes = row.get("notes", "")
        checks.extend([
            (f"{source_id}-QA-01", f"{source_id}已登记为用户提供且相关段已读", "full_text_available/相关段=是", f"{row.get('full_text_available', '')}/{row.get('relevant_passage_checked', '')}", "用户提供PDF" in row.get("full_text_available", "") and row.get("relevant_passage_checked") == "是"),
            (f"{source_id}-QA-02", f"{source_id}含页码锚点", pages, notes, pages in notes),
            (f"{source_id}-QA-03", f"{source_id}保留不可迁移边界", prohibited, notes, prohibited in notes),
            (f"{source_id}-QA-04", f"{source_id}回到页码映射", "至少一条映射", str(sum(item["source_id"] == source_id for item in page_map)), any(item["source_id"] == source_id for item in page_map)),
        ])
    with OUTPUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["check_id", "check_item", "expected", "actual", "status"])
        for check_id, item, expected, actual, passed in checks:
            writer.writerow([check_id, item, expected, actual, "通过" if passed else "不通过"])
    failures = [check_id for check_id, _, _, _, passed in checks if not passed]
    OUTPUT_MD.write_text(
        "# 国内竞赛研究文献核验台账对齐QA（V1）\n\n"
        f"共{len(checks)}项，{'全部通过' if not failures else '不通过：' + '、'.join(failures)}。"
        "本检查不验证外部出版链或将用户提供来源升级为E2，只验证项目内页码、阅读状态和不可迁移边界的一致性。\n",
        encoding="utf-8",
    )
    if failures:
        raise SystemExit("文献核验台账对齐QA失败：" + ", ".join(failures))
    print(f"国内竞赛研究文献核验台账对齐QA：{len(checks)}/{len(checks)}通过")


if __name__ == "__main__":
    main()
