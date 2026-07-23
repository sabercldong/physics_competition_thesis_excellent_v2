from __future__ import annotations

import csv
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SELECTED = ["CPHO41-Q06-3", "CPHO41-Q07-4", "CPHO42-Q04-2"]
EXCLUDED = {"CPHO36-Q04-1", "CPHO36-Q05-3", "CPHO37-Q06-3", "CPHO41-Q01-2"}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> int:
    root = ROOT / "07_analysis/results/formal_rater_r01"
    selected = read_rows(root / "r01_case_reselection_v1.csv")
    dossier = read_rows(root / "r01_case_reselection_evidence_dossier_v1.csv")
    chapter = (ROOT / "08_manuscript/05_cases_and_diagnosis.md").read_text(encoding="utf-8")
    checks = []
    checks.append(("筛选案例集合", ";".join(row["item_id"] for row in selected), ";".join(SELECTED), [row["item_id"] for row in selected] == SELECTED))
    checks.append(("筛选门禁", "；".join(row["selection_decision"] for row in selected), "全部可作为任务结构说明案例", all(row["selection_decision"] == "可作为任务结构说明案例" for row in selected)))
    checks.append(("逐维证据记录", str(len(dossier)), "12", len(dossier) == 12 and all(row["evidence_source"] == "R01-EVIDENCE-REPAIR-V2" for row in dossier)))
    checks.append(("旧失败案例排除", "未出现" if not any(case in chapter for case in EXCLUDED) else "出现", "未出现", not any(case in chapter for case in EXCLUDED)))
    checks.append(("案例编号进入正文", "存在" if all(case in chapter for case in SELECTED) else "缺失", "存在", all(case in chapter for case in SELECTED)))
    required_boundaries = ["不诊断学生困难", "不报告教学效果", "项目无法独立验证", "不是课堂有效性的实证结论"]
    checks.append(("正文边界语句", "存在" if all(text in chapter for text in required_boundaries) else "缺失", "存在", all(text in chapter for text in required_boundaries)))
    forbidden = ["教师普遍认为", "教学效果显著", "课堂实践表明"]
    checks.append(("禁止经验性结论", "未出现" if not any(text in chapter for text in forbidden) else "出现", "未出现", not any(text in chapter for text in forbidden)))
    output = ROOT / "09_quality/r01_case_reselection_qa_v1.csv"
    with output.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["check_item", "observed", "expected", "status"], lineterminator="\n")
        writer.writeheader()
        for item, observed, expected, passed in checks:
            writer.writerow({"check_item": item, "observed": observed, "expected": expected, "status": "通过" if passed else "不通过"})
    failures = sum(not check[-1] for check in checks)
    print(f"R01案例重选QA：{len(checks) - failures}/{len(checks)}通过")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
