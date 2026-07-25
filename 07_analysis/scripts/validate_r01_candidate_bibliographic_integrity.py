#!/usr/bin/env python3
"""Validate the structural coverage of the candidate bibliographic-integrity audit."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
AUDIT = ROOT / "09_quality/r01_candidate_bibliographic_integrity_20260725.csv"
MAPPING = ROOT / "09_quality/r01_candidate_references_mapping_v1.csv"
OUTPUT = ROOT / "09_quality/r01_candidate_bibliographic_integrity_qa_20260725.csv"


def load(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    audit = load(AUDIT)
    mapping = load(MAPPING)
    detail = [row for row in audit if row["reference_number"].isdigit()]
    summaries = [row for row in audit if row["reference_number"].startswith("SUMMARY-")]
    audit_sources = {row["source_id"] for row in detail}
    mapping_sources = {row["source_id"] for row in mapping}
    checks = [
        ("REFI-QA-01", "候选覆盖", len(detail) == len(mapping) == 39 and audit_sources == mapping_sources, f"审计{len(detail)}；映射{len(mapping)}"),
        ("REFI-QA-02", "汇总检查存在", len(summaries) == 3, f"{len(summaries)}/3"),
        ("REFI-QA-03", "身份状态取值", all(row["internal_identity_status"] in {"通过", "待核实"} for row in detail), "状态仅为通过或待核实"),
        ("REFI-QA-04", "边界声明完整", all(row["boundary_note"] for row in detail), "39条均不声称外部认证或最终放行"),
    ]
    with OUTPUT.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["check_id", "check_item", "status", "detail"])
        for check_id, item, passed, detail_text in checks:
            writer.writerow([check_id, item, "通过" if passed else "不通过", detail_text])
    failures = [check_id for check_id, _, passed, _ in checks if not passed]
    if failures:
        raise SystemExit("候选书目身份审计QA失败：" + ", ".join(failures))
    print(f"候选书目身份审计QA：{len(checks)}/{len(checks)}通过。")


if __name__ == "__main__":
    main()
