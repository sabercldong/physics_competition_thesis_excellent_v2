#!/usr/bin/env python3
"""Run the current R01 material-package validation chain and summarize outcomes."""

from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUTPUT_CSV = ROOT / "09_quality/r01_full_package_healthcheck_v1.csv"
OUTPUT_MD = ROOT / "09_quality/r01_full_package_healthcheck_v1.md"

COMMANDS = [
    ("HP-QA-01", "SOLO应用接入包", ["07_analysis/scripts/validate_solo_application_integration_packet.py"]),
    ("HP-QA-02", "结果资格", ["07_analysis/scripts/validate_r01_results_eligibility.py"]),
    ("HP-QA-03", "第四章当前结果整合", ["07_analysis/scripts/validate_r01_results_manuscript_integration_v2.py"]),
    ("HP-QA-04", "结论章研究问题对齐", ["07_analysis/scripts/validate_r01_conclusion_rq_alignment.py"]),
    ("HP-QA-05", "案例重选", ["07_analysis/scripts/validate_r01_case_reselection.py"]),
    ("HP-QA-06", "候选参考文献", ["07_analysis/scripts/validate_r01_candidate_references.py"]),
    ("HP-QA-07", "正文引用追溯", ["07_analysis/scripts/audit_r01_citation_trace.py"]),
    ("HP-QA-08", "V17输入新鲜度", ["07_analysis/scripts/validate_working_draft_freshness.py", "--require-current"]),
    ("HP-QA-09", "材料包快照", ["07_analysis/scripts/build_r01_material_package_snapshot.py", "--validate"]),
    ("HP-QA-10", "内部交接包", ["07_analysis/scripts/build_r01_internal_material_package.py", "--validate"]),
    ("HP-QA-11", "材料包总审计", ["07_analysis/scripts/validate_current_material_package_audit.py"]),
    ("HP-QA-12", "复现运行手册", ["07_analysis/scripts/validate_r01_reproducibility_runbook.py"]),
    ("HP-QA-13", "中文摘要对齐", ["07_analysis/scripts/validate_r01_abstract_alignment.py"]),
]


def main() -> None:
    rows: list[dict[str, str]] = []
    for check_id, item, args in COMMANDS:
        command = [sys.executable, *args]
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
        output = (result.stdout + result.stderr).strip().replace("\n", " | ")
        rows.append({
            "check_id": check_id,
            "check_item": item,
            "command": " ".join(command),
            "exit_code": str(result.returncode),
            "status": "通过" if result.returncode == 0 else "不通过",
            "summary": output[:1000],
        })
    with OUTPUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    failures = [row["check_id"] for row in rows if row["status"] != "通过"]
    OUTPUT_MD.write_text(
        "# R01 当前材料包全链路健康检查（V1）\n\n"
        f"共执行{len(rows)}项已有门禁，{'全部通过' if not failures else '不通过：' + '、'.join(failures)}。"
        "本检查只串联项目内脚本和当前文件状态；不验证评分者身份、人工过程、外部效度、学生能力、教学效果、学校格式或人类参与者事实。\n",
        encoding="utf-8",
    )
    if failures:
        raise SystemExit("R01全链路健康检查失败：" + ", ".join(failures))
    print(f"R01全链路健康检查：{len(rows)}/{len(rows)}通过")


if __name__ == "__main__":
    main()
