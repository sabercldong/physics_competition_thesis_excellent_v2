#!/usr/bin/env python3
"""Validate that the R01 package snapshot retains domestic-competition evidence entries."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "10_outputs/material_package/R01_current_material_package_manifest_v1.csv"
OUTPUT_CSV = ROOT / "09_quality/pcomp_package_snapshot_refresh_qa_v1.csv"
OUTPUT_MD = ROOT / "09_quality/pcomp_package_snapshot_refresh_qa_v1.md"

EXPECTED = {
    "PKG-15": "36项限边界候选参考文献",
    "PKG-38": "02_literature/reference_verification.csv",
    "PKG-39": "02_literature/physics_competition_page_level_claim_map_v1.csv",
    "PKG-40": "09_quality/pcomp_candidate_citation_integration_qa_v1.csv",
}


def main() -> None:
    with MANIFEST.open(encoding="utf-8-sig", newline="") as handle:
        rows = {row["artifact_id"]: row for row in csv.DictReader(handle)}
    checks = [
        ("PCOMP-PKG-QA-01", "快照项目数", "40", str(len(rows)), len(rows) == 40),
    ]
    for artifact_id, expected in EXPECTED.items():
        row = rows.get(artifact_id, {})
        actual = row.get("purpose", "") if artifact_id == "PKG-15" else row.get("relative_path", "")
        checks.append((f"{artifact_id}-QA", f"{artifact_id}已纳入快照", expected, actual, actual == expected and row.get("exists") == "是" and bool(row.get("sha256"))))
    checks.append(("PCOMP-PKG-QA-06", "新增页码映射保留E1边界", "E1页码映射", rows.get("PKG-39", {}).get("distribution_boundary", ""), "E1页码映射" in rows.get("PKG-39", {}).get("distribution_boundary", "")))
    with OUTPUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["check_id", "check_item", "expected", "actual", "status"])
        for check_id, item, expected, actual, passed in checks:
            writer.writerow([check_id, item, expected, actual, "通过" if passed else "不通过"])
    failures = [check_id for check_id, _, _, _, passed in checks if not passed]
    OUTPUT_MD.write_text(
        "# 国内竞赛研究材料包快照刷新QA（V1）\n\n"
        f"共{len(checks)}项，{'全部通过' if not failures else '不通过：' + '、'.join(failures)}。"
        "本检查只验证快照入口与哈希字段，不验证外部发布链、学校最终格式或论文结论。\n",
        encoding="utf-8",
    )
    if failures:
        raise SystemExit("国内竞赛研究材料包快照刷新QA失败：" + ", ".join(failures))
    print(f"国内竞赛研究材料包快照刷新QA：{len(checks)}/{len(checks)}通过")


if __name__ == "__main__":
    main()
