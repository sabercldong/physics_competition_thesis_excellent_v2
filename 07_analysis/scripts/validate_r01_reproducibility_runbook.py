#!/usr/bin/env python3
"""Verify that the R01 reproducibility protocol names the current package state."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUNBOOK = ROOT / "07_analysis/reproducibility_protocol.md"
RESULT_QA = ROOT / "09_quality/r01_results_eligibility_qa_v1.csv"
CANDIDATES = ROOT / "09_quality/r01_candidate_references_mapping_v1.csv"
TRACE = ROOT / "09_quality/r01_citation_trace_v1.csv"
OUTPUT_CSV = ROOT / "09_quality/r01_reproducibility_runbook_qa_v1.csv"
OUTPUT_MD = ROOT / "09_quality/r01_reproducibility_runbook_qa_v1.md"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    text = RUNBOOK.read_text(encoding="utf-8")
    result_rows = read_rows(RESULT_QA)
    candidates = read_rows(CANDIDATES)
    trace = read_rows(TRACE)
    result_count = len(result_rows)
    candidate_count = len(candidates)
    trace_total = len(trace)
    trace_placeholders = sum(row["is_citation_placeholder"] == "是" for row in trace)
    checks = [
        ("RUNBOOK-QA-01", "冻结编码文件", "final_coding_r01_correction_v1.csv" in text),
        ("RUNBOOK-QA-02", "证据链文件", "final_coding_evidence_r01_v1.csv" in text),
        ("RUNBOOK-QA-03", "结果资格脚本", "validate_r01_results_eligibility.py" in text),
        ("RUNBOOK-QA-13", "第四章当前结果整合脚本", "validate_r01_results_manuscript_integration_v2.py" in text),
        ("RUNBOOK-QA-14", "内部交接包脚本", "build_r01_internal_material_package.py --validate" in text),
        ("RUNBOOK-QA-15", "全链路健康检查脚本", "validate_r01_full_package_healthcheck.py" in text),
        ("RUNBOOK-QA-04", "案例脚本", "validate_r01_case_reselection.py" in text),
        ("RUNBOOK-QA-05", "引用链脚本", "audit_r01_citation_trace.py" in text),
        ("RUNBOOK-QA-06", "工作稿新鲜度脚本", "validate_working_draft_freshness.py --require-current" in text),
        ("RUNBOOK-QA-07", "材料包审计脚本", "validate_current_material_package_audit.py" in text),
        ("RUNBOOK-QA-08", "手册自身QA", "validate_r01_reproducibility_runbook.py" in text),
        ("RUNBOOK-QA-09", "结果资格计数", f"{result_count}/{result_count}" in text),
        ("RUNBOOK-QA-10", "候选来源计数", f"候选来源{candidate_count}项" in text),
        ("RUNBOOK-QA-11", "引用追溯计数", f"{trace_total}条来源出现、{trace_placeholders}处显式占位" in text),
        ("RUNBOOK-QA-12", "禁止外推边界", all(term in text for term in ["学生能力", "教学效果", "第35届分值"])),
    ]
    with OUTPUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["check_id", "check_item", "status"])
        for check_id, item, passed in checks:
            writer.writerow([check_id, item, "通过" if passed else "不通过"])
    failures = [check_id for check_id, _, passed in checks if not passed]
    OUTPUT_MD.write_text(
        "# R01 复现运行手册 QA\n\n"
        f"共{len(checks)}项检查，{'全部通过' if not failures else '不通过：' + '、'.join(failures)}。"
        "本QA只检查手册入口、当前计数与禁止外推边界的项目内一致性，不执行全部重建命令，也不验证人工过程或外部事实。\n",
        encoding="utf-8",
    )
    if failures:
        raise SystemExit("复现运行手册QA失败：" + ", ".join(failures))
    print(f"R01复现运行手册QA：{len(checks)}/{len(checks)}通过")


if __name__ == "__main__":
    main()
