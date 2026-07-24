#!/usr/bin/env python3
"""Validate the traceability and non-implementation boundaries of R01 design materials."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MATRIX = ROOT / "06_teaching_validation/teaching_design_matrix.md"
CASE_01 = ROOT / "06_teaching_validation/r01_design_case_01_condition_relation_chain.md"
CASE_02 = ROOT / "06_teaching_validation/r01_design_case_02_state_energy_classification.md"
CASE_REGISTER = ROOT / "07_analysis/results/formal_rater_r01/r01_case_reselection_v1.csv"
OUTPUT = ROOT / "09_quality/r01_teaching_design_materials_qa_v1.csv"
REPORT = ROOT / "09_quality/r01_teaching_design_materials_qa_v1.md"


def has_text(path: Path, expected: str) -> bool:
    return path.is_file() and expected in path.read_text(encoding="utf-8-sig")


def main() -> None:
    checks = []

    def check(check_id: str, item: str, passed: bool, source: Path) -> None:
        checks.append(
            {
                "check_id": check_id,
                "check_item": item,
                "status": "通过" if passed else "不通过",
                "source": str(source.relative_to(ROOT)),
            }
        )

    matrix = MATRIX.read_text(encoding="utf-8-sig") if MATRIX.is_file() else ""
    register = CASE_REGISTER.read_text(encoding="utf-8-sig") if CASE_REGISTER.is_file() else ""
    check("TD-QA-01", "矩阵存在并声明未收集学生/教师证据", "未收集学生或教师证据" in matrix, MATRIX)
    check("TD-QA-02", "矩阵覆盖三个R01案例", all(x in matrix for x in ("CPHO41-Q06-3", "CPHO41-Q07-4", "CPHO42-Q04-2")), MATRIX)
    check("TD-QA-03", "矩阵明确不推断教学效果", "不证明学生困难、支架有效、能力提升或课堂可行" in matrix, MATRIX)
    check("TD-QA-04", "矩阵连接R01案例登记表", "r01_case_reselection_v1.csv" in matrix, MATRIX)
    check("TD-QA-05", "案例登记表包含第一个设计案例", "CPHO41-Q06-3" in register, CASE_REGISTER)
    check("TD-QA-06", "案例登记表包含第二个设计案例", "CPHO41-Q07-4" in register, CASE_REGISTER)

    case_specs = (
        ("TD-QA-07", CASE_01, "CPHO41-Q06-3", "条件—关系链"),
        ("TD-QA-08", CASE_02, "CPHO41-Q07-4", "状态分类—平均能量关系"),
    )
    for check_id, path, item_id, task_label in case_specs:
        check(check_id, "设计案例连接正确R01分析单元", has_text(path, item_id), path)
        check(check_id + "A", "设计案例包含任务序列", has_text(path, "## 任务序列"), path)
        check(check_id + "B", "设计案例包含支架撤除规则", has_text(path, "## 支架与撤除"), path)
        check(check_id + "C", "设计案例包含可观察评价记录", has_text(path, "## 评价记录（未验证量规）"), path)
        check(check_id + "D", "设计案例保留未实施边界", has_text(path, "未实施") and has_text(path, "不证明"), path)
        check(check_id + "E", "设计案例任务结构标签正确", has_text(path, task_label), path)

    forbidden = ("显著提升", "教学效果显著", "课堂验证完成")
    for path in (MATRIX, CASE_01, CASE_02):
        text = path.read_text(encoding="utf-8-sig") if path.is_file() else ""
        check(f"TD-QA-{len(checks) + 1:02d}", "未出现未被限定的效果或普遍性结论", not any(term in text for term in forbidden), path)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=("check_id", "check_item", "status", "source"))
        writer.writeheader()
        writer.writerows(checks)

    passed = sum(row["status"] == "通过" for row in checks)
    REPORT.write_text(
        "# R01教学设计材料QA\n\n"
        f"检查结果：{passed}/{len(checks)}通过。\n\n"
        "本检查只验证案例、矩阵、任务、支架、评价记录和未实施边界之间的项目内对应关系；"
        "不验证教师身份、学生参与、课堂实施、作品真实性、量规信效度或教学效果。\n",
        encoding="utf-8",
    )
    if passed != len(checks):
        raise SystemExit("R01教学设计材料QA未通过")
    print(f"R01教学设计材料QA：{passed}/{len(checks)}通过")


if __name__ == "__main__":
    main()
