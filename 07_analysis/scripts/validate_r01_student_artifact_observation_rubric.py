#!/usr/bin/env python3
"""Validate the traceable, unvalidated R01 student-artifact observation tool."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUBRIC = ROOT / "06_teaching_validation/student_artifact_rubric.md"
TEMPLATE = ROOT / "06_teaching_validation/r01_student_artifact_observation_record_template.csv"
CASE_REGISTER = ROOT / "07_analysis/results/formal_rater_r01/r01_case_reselection_v1.csv"
OUTPUT = ROOT / "09_quality/r01_student_artifact_observation_rubric_qa_v1.csv"
REPORT = ROOT / "09_quality/r01_student_artifact_observation_rubric_qa_v1.md"

EXPECTED = {
    "CPHO41-Q06-3": ("CR-01", "CR-02", "CR-03", "CR-04"),
    "CPHO41-Q07-4": ("SE-01", "SE-02", "SE-03", "SE-04", "SE-05"),
    "CPHO42-Q04-2": ("AM-01", "AM-02", "AM-03", "AM-04"),
}
BLANK_FIELDS = (
    "student_or_artifact_code",
    "work_version",
    "observation_status",
    "evidence_location",
    "observer_id",
    "observation_date",
    "observation_note",
    "implementation_context",
    "consent_or_approval_ref",
    "ai_or_tool_declaration",
)


def main() -> None:
    rubric = RUBRIC.read_text(encoding="utf-8-sig") if RUBRIC.is_file() else ""
    register = CASE_REGISTER.read_text(encoding="utf-8-sig") if CASE_REGISTER.is_file() else ""
    with TEMPLATE.open(encoding="utf-8-sig", newline="") as handle:
        template_rows = list(csv.DictReader(handle))
        fields = tuple(handle.seek(0) or csv.DictReader(handle).fieldnames or ())

    checks: list[tuple[str, str, bool, str]] = []

    def check(check_id: str, item: str, passed: bool, source: str) -> None:
        checks.append((check_id, item, passed, source))

    check("OBS-QA-01", "量规明确为未验证设计工具", "未验证设计工具" in rubric and "不是本项目已经实施、验证或标准化" in rubric, RUBRIC.name)
    check("OBS-QA-02", "量规明确不把记录换算为学生能力或教学效果", "不能把“可见/部分可见/未见”换算为学生科学思维等级" in rubric, RUBRIC.name)
    check("OBS-QA-03", "量规提供四种非推断性观察状态", all(status in rubric for status in ("`可见`", "`部分可见`", "`未见`", "`不适用/材料不足`")), RUBRIC.name)
    check("OBS-QA-04", "量规规定匿名、版本、工具与证据位置记录", all(token in rubric for token in ("作品匿名代码", "任务版本", "AI使用声明", "证据位置")), RUBRIC.name)
    check("OBS-QA-05", "量规设定实施、同意、锚定与分歧处理门槛", all(token in rubric for token in ("伦理/备案", "知情同意", "样例进行锚定", "分歧表")), RUBRIC.name)
    check("OBS-QA-06", "量规连接三个R01案例", all(case_id in rubric and case_id in register for case_id in EXPECTED), RUBRIC.name)
    check("OBS-QA-07", "模板字段完整", set(("record_template_id", "case_id", "indicator_id", "observable_output", "allowed_status", *BLANK_FIELDS, "decision_boundary")).issubset(fields), TEMPLATE.name)
    check("OBS-QA-08", "模板行数与指标数一致", len(template_rows) == sum(len(ids) for ids in EXPECTED.values()), TEMPLATE.name)
    actual = {(row["case_id"], row["indicator_id"]) for row in template_rows}
    expected = {(case_id, indicator_id) for case_id, ids in EXPECTED.items() for indicator_id in ids}
    check("OBS-QA-09", "模板覆盖三个案例的全部观察指标", actual == expected, TEMPLATE.name)
    check("OBS-QA-10", "模板不含伪造的学生、作品或观察数据", all(not row[field].strip() for row in template_rows for field in BLANK_FIELDS), TEMPLATE.name)
    check("OBS-QA-11", "模板状态选项保持可观察边界", all(row["allowed_status"] == "可见|部分可见|未见|不适用/材料不足" for row in template_rows), TEMPLATE.name)
    forbidden = ("显著提升", "教学效果显著", "学生普遍")
    check("OBS-QA-12", "量规未作未限定的效果或普遍性结论", not any(token in rubric for token in forbidden), RUBRIC.name)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(("check_id", "check_item", "status", "source"))
        for check_id, item, passed, source in checks:
            writer.writerow((check_id, item, "通过" if passed else "不通过", source))

    failures = [check_id for check_id, _, passed, _ in checks if not passed]
    REPORT.write_text(
        "# R01学生作品过程性观察记录量规QA\n\n"
        f"检查结果：{len(checks) - len(failures)}/{len(checks)}通过。\n\n"
        "本QA只检查工具的项目内可追溯性、空白模板状态与非推断边界；"
        "不验证学生参与、课堂实施、作品真实性、评分者身份、信度、效度或教学效果。\n",
        encoding="utf-8",
    )
    if failures:
        raise SystemExit("R01学生作品观察量规QA未通过：" + ", ".join(failures))
    print(f"R01学生作品观察量规QA：{len(checks)}/{len(checks)}通过")


if __name__ == "__main__":
    main()
