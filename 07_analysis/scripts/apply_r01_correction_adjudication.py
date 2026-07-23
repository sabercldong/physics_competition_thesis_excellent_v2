from __future__ import annotations

import argparse
import csv
import hashlib
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BASELINE_ROWS = 876
KEY_FIELDS = ("item_id", "dimension")
FINAL_FIELDS = [
    "item_id", "competition_no", "year", "question_no", "subquestion_no", "dimension",
    "present", "present_label", "level", "evidence", "adjudicator", "adjudication_date",
    "adjudication_reason", "source_adjudication_sha256",
]


def resolve(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def read_rows(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader), reader.fieldnames or []


def write_rows(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description="将已接收的R01更正裁决受控应用到版本化唯一分析表。")
    parser.add_argument("--baseline", default="07_analysis/data/final_coding.csv")
    parser.add_argument("--corrections", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--qa-output", required=True)
    parser.add_argument("--manifest-output", required=True)
    parser.add_argument("--registered-copy", required=True, help="UTF-8 BOM与LF的登记副本路径。")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    baseline_path = resolve(args.baseline)
    correction_path = resolve(args.corrections)
    output_path = resolve(args.output)
    qa_path = resolve(args.qa_output)
    manifest_path = resolve(args.manifest_output)
    registered_path = resolve(args.registered_copy)
    baseline_rows, baseline_fields = read_rows(baseline_path)
    correction_rows, correction_fields = read_rows(correction_path)
    checks: list[tuple[str, str, str]] = []

    baseline_complete = all(field in baseline_fields for field in FINAL_FIELDS)
    baseline_keys = [tuple(row.get(field, "").strip() for field in KEY_FIELDS) for row in baseline_rows]
    checks.append(("基线字段完整", "通过" if baseline_complete else "不通过", "final_coding字段齐全" if baseline_complete else "缺少必要字段"))
    checks.append(("基线记录与键", "通过" if len(baseline_rows) == BASELINE_ROWS and len(set(baseline_keys)) == BASELINE_ROWS else "不通过", f"记录{len(baseline_rows)}；唯一键{len(set(baseline_keys))}"))
    required_correction = {
        "item_id", "dimension", "current_present", "current_level", "final_present", "final_level",
        "adjudicator_id", "adjudication_date", "adjudication_decision", "adjudication_reason",
        "question_trigger_quote", "solution_step_quote",
    }
    correction_complete = required_correction.issubset(correction_fields) and len(correction_rows) == 4
    correction_keys = [tuple(row.get(field, "").strip() for field in KEY_FIELDS) for row in correction_rows]
    checks.append(("更正回填字段与记录数", "通过" if correction_complete else "不通过", f"记录{len(correction_rows)}；必填字段{'齐全' if required_correction.issubset(correction_fields) else '缺失'}"))
    checks.append(("更正键唯一", "通过" if len(correction_keys) == len(set(correction_keys)) else "不通过", f"唯一键{len(set(correction_keys))}"))
    output_allowed = not output_path.exists() or args.force
    checks.append(("输出路径防覆盖", "通过" if output_allowed else "不通过", "输出不存在或已显式--force" if output_allowed else f"已存在：{output_path}"))
    registered_allowed = not registered_path.exists() or args.force
    checks.append(("登记副本路径防覆盖", "通过" if registered_allowed else "不通过", "登记副本不存在或已显式--force" if registered_allowed else f"已存在：{registered_path}"))

    lookup = {key: row for key, row in zip(baseline_keys, baseline_rows)}
    current_match = all(
        key in lookup
        and lookup[key]["present_label"] == row["current_present"].strip()
        and lookup[key]["level"] == row["current_level"].strip()
        for key, row in zip(correction_keys, correction_rows)
    )
    final_logic = all(
        row["final_present"].strip() in {"是", "否"}
        and ((row["final_present"].strip() == "否") == (row["final_level"].strip() == "未出现"))
        and row["adjudication_decision"].strip() in {"采纳建议", "不采纳建议", "另行裁决"}
        for row in correction_rows
    )
    checks.append(("当前值与基线逐键一致", "通过" if current_match else "不通过", "4条当前值均匹配" if current_match else "至少一条当前值不匹配"))
    checks.append(("最终裁决逻辑", "通过" if final_logic else "不通过", "存在性、等级与决定均合法" if final_logic else "存在非法或不一致取值"))

    qa_path.parent.mkdir(parents=True, exist_ok=True)
    write_rows(qa_path, ["check_item", "status", "evidence_or_result"], [
        {"check_item": item, "status": status, "evidence_or_result": detail} for item, status, detail in checks
    ])
    if any(status != "通过" for _, status, _ in checks):
        print("更正应用门禁未通过；未生成版本化分析表。", file=sys.stderr)
        return 1

    correction_sha = hashlib.sha256(correction_path.read_bytes()).hexdigest()
    baseline_sha = hashlib.sha256(baseline_path.read_bytes()).hexdigest()
    correction_lookup = {key: row for key, row in zip(correction_keys, correction_rows)}
    output_rows: list[dict[str, str]] = []
    manifest_rows: list[dict[str, str]] = []
    for row in baseline_rows:
        key = (row["item_id"], row["dimension"])
        amended = dict(row)
        if key in correction_lookup:
            correction = correction_lookup[key]
            amended.update({
                "present": "1" if correction["final_present"].strip() == "是" else "0",
                "present_label": correction["final_present"].strip(),
                "level": correction["final_level"].strip(),
                "evidence": f"题干：{correction['question_trigger_quote'].strip()}；解答：{correction['solution_step_quote'].strip()}",
                "adjudicator": correction["adjudicator_id"].strip(),
                "adjudication_date": correction["adjudication_date"].strip(),
                "adjudication_reason": correction["adjudication_reason"].strip(),
                "source_adjudication_sha256": correction_sha,
            })
            manifest_rows.append({
                "item_id": key[0], "dimension": key[1],
                "baseline_present": row["present_label"], "baseline_level": row["level"],
                "final_present": amended["present_label"], "final_level": amended["level"],
                "adjudication_decision": correction["adjudication_decision"].strip(),
                "adjudicator_id": correction["adjudicator_id"].strip(),
                "adjudication_date": correction["adjudication_date"].strip(),
                "correction_source_sha256": correction_sha,
            })
        output_rows.append(amended)

    coding_changes = {
        (before["item_id"], before["dimension"])
        for before, after in zip(baseline_rows, output_rows)
        if (before["present"], before["present_label"], before["level"])
        != (after["present"], after["present_label"], after["level"])
    }
    expected_changes = set(correction_lookup)
    final_values_match = all(
        (next(row for row in output_rows if (row["item_id"], row["dimension"]) == key)["present_label"],
         next(row for row in output_rows if (row["item_id"], row["dimension"]) == key)["level"])
        == (correction["final_present"].strip(), correction["final_level"].strip())
        for key, correction in correction_lookup.items()
    )
    checks.append(("编码取值仅在裁决键变更", "通过" if coding_changes == expected_changes else "不通过", f"实际{len(coding_changes)}条；预期{len(expected_changes)}条"))
    checks.append(("最终值逐键匹配裁决", "通过" if final_values_match else "不通过", "4条最终值均匹配" if final_values_match else "至少一条最终值不匹配"))
    if any(status != "通过" for _, status, _ in checks):
        write_rows(qa_path, ["check_item", "status", "evidence_or_result"], [
            {"check_item": item, "status": status, "evidence_or_result": detail} for item, status, detail in checks
        ])
        print("更正应用输出复核未通过；未生成版本化分析表。", file=sys.stderr)
        return 1

    write_rows(output_path, FINAL_FIELDS, output_rows)
    write_rows(registered_path, correction_fields, correction_rows)
    output_sha = hashlib.sha256(output_path.read_bytes()).hexdigest()
    for row in manifest_rows:
        row["baseline_final_coding_sha256"] = baseline_sha
        row["corrected_final_coding_sha256"] = output_sha
    write_rows(manifest_path, [
        "item_id", "dimension", "baseline_present", "baseline_level", "final_present", "final_level",
        "adjudication_decision", "adjudicator_id", "adjudication_date", "correction_source_sha256",
        "baseline_final_coding_sha256", "corrected_final_coding_sha256",
    ], manifest_rows)
    write_rows(qa_path, ["check_item", "status", "evidence_or_result"], [
        {"check_item": item, "status": status, "evidence_or_result": detail} for item, status, detail in checks
    ])
    print(f"已生成版本化分析表：{output_path}")
    print(f"已生成更正清单：{manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
