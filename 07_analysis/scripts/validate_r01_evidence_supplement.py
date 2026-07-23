from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
KEYS = ["item_id", "competition_no", "year", "question_no", "subquestion_no", "dimension"]
WORK_FIELDS = [
    "reviewer_id", "review_date", "source_checked", "question_trigger_quote", "question_location",
    "solution_step_quote", "solution_location", "evidence_sufficiency", "rechecked_present",
    "rechecked_level", "adjacent_level_exclusion", "recheck_decision", "reviewer_statement",
]


def resolve(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def read(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader), reader.fieldnames or []


def write(path: Path, checks: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["check_item", "status", "observed"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(checks)


def main() -> int:
    parser = argparse.ArgumentParser(description="验证R01逐条证据补正回填的结构和逻辑，不判定来源事实。")
    parser.add_argument("--input", required=True)
    parser.add_argument("--template", default="07_analysis/data/rater_returns/templates/R01/r01_evidence_supplement_template.csv")
    parser.add_argument("--qa-output", required=True)
    args = parser.parse_args()
    input_rows, fields = read(resolve(args.input))
    template_rows, _ = read(resolve(args.template))
    input_keys = [tuple(row.get(key, "").strip() for key in KEYS) for row in input_rows]
    template_keys = [tuple(row.get(key, "").strip() for key in KEYS) for row in template_rows]
    blank_work = {field: sum(not row.get(field, "").strip() for row in input_rows) for field in WORK_FIELDS}
    invalid_present = sum(row.get("rechecked_present", "").strip() not in {"是", "否"} for row in input_rows)
    invalid_level = sum(row.get("rechecked_level", "").strip() not in {"L1", "L2", "L3", "L4", "未出现"} for row in input_rows)
    invalid_source = sum(row.get("source_checked", "").strip() != "是" for row in input_rows)
    invalid_sufficiency = sum(row.get("evidence_sufficiency", "").strip() not in {"充分", "不足"} for row in input_rows)
    bad_logic = sum(
        (row.get("rechecked_present", "").strip() == "是" and row.get("rechecked_level", "").strip() == "未出现")
        or (row.get("rechecked_present", "").strip() == "否" and row.get("rechecked_level", "").strip() != "未出现")
        for row in input_rows
    )
    bad_decision = sum(
        row.get("recheck_decision", "").strip() not in {"保持当前裁决", "建议更正"}
        or (
            row.get("recheck_decision", "").strip() == "保持当前裁决"
            and (row.get("rechecked_present", "").strip() != row.get("current_present", "").strip() or row.get("rechecked_level", "").strip() != row.get("current_level", "").strip())
        )
        or (
            row.get("recheck_decision", "").strip() == "建议更正"
            and row.get("rechecked_present", "").strip() == row.get("current_present", "").strip()
            and row.get("rechecked_level", "").strip() == row.get("current_level", "").strip()
        )
        for row in input_rows
    )
    checks = [
        {"check_item": "字段齐全", "status": "通过" if all(field in fields for field in WORK_FIELDS) else "不通过", "observed": "工作字段缺失" if not all(field in fields for field in WORK_FIELDS) else "工作字段完整"},
        {"check_item": "记录数", "status": "通过" if len(input_rows) == 876 else "不通过", "observed": str(len(input_rows))},
        {"check_item": "不可变键与模板同序", "status": "通过" if input_keys == template_keys else "不通过", "observed": f"输入{len(input_keys)}；模板{len(template_keys)}"},
        {"check_item": "工作字段非空", "status": "通过" if not any(blank_work.values()) else "不通过", "observed": "；".join(f"{key}:{value}" for key, value in blank_work.items() if value) or "全部非空"},
        {"check_item": "存在性和等级枚举", "status": "通过" if invalid_present == invalid_level == 0 else "不通过", "observed": f"present:{invalid_present}；level:{invalid_level}"},
        {"check_item": "来源核对和充分性枚举", "status": "通过" if invalid_source == invalid_sufficiency == 0 else "不通过", "observed": f"source_checked:{invalid_source}；evidence_sufficiency:{invalid_sufficiency}"},
        {"check_item": "存在性和等级逻辑", "status": "通过" if bad_logic == 0 else "不通过", "observed": str(bad_logic)},
        {"check_item": "保持或更正决定逻辑", "status": "通过" if bad_decision == 0 else "不通过", "observed": str(bad_decision)},
    ]
    write(resolve(args.qa_output), checks)
    failures = [check for check in checks if check["status"] != "通过"]
    print(f"补正回填检查：{len(checks) - len(failures)}/{len(checks)}通过")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
