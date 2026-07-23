from __future__ import annotations

import argparse
import csv
import hashlib
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EXPECTED_ROWS = 876
KEY_FIELDS = ["item_id", "competition_no", "year", "question_no", "subquestion_no", "dimension"]
REQUIRED_SOURCE_FIELDS = KEY_FIELDS + [
    "adjudicated_present",
    "adjudicated_level",
    "adjudicated_evidence",
    "adjudicator",
    "adjudication_date",
    "adjudication_reason",
]
OUTPUT_FIELDS = KEY_FIELDS + [
    "present",
    "present_label",
    "level",
    "evidence",
    "adjudicator",
    "adjudication_date",
    "adjudication_reason",
    "source_adjudication_sha256",
]


def _path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def _read_rows(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader), reader.fieldnames or []


def _write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _validate(rows: list[dict[str, str]], fields: list[str]) -> list[tuple[str, str, str]]:
    checks: list[tuple[str, str, str]] = []
    missing = [field for field in REQUIRED_SOURCE_FIELDS if field not in fields]
    checks.append(("字段齐全", "通过" if not missing else "不通过", "缺失：" + ", ".join(missing) if missing else "全部必需字段存在"))
    checks.append(("记录数", "通过" if len(rows) == EXPECTED_ROWS else "不通过", f"实际 {len(rows)}，期望 {EXPECTED_ROWS}"))

    keys = [tuple(row.get(field, "").strip() for field in KEY_FIELDS) for row in rows]
    blank_keys = sum(any(not value for value in key) for key in keys)
    checks.append(("不可变键完整且唯一", "通过" if blank_keys == 0 and len(set(keys)) == len(rows) else "不通过", f"空键 {blank_keys}；唯一键 {len(set(keys))}"))

    adjudication_fields = REQUIRED_SOURCE_FIELDS[len(KEY_FIELDS) :]
    blanks = {field: sum(not row.get(field, "").strip() for row in rows) for field in adjudication_fields}
    blank_total = sum(blanks.values())
    checks.append(("裁决字段完整", "通过" if blank_total == 0 else "不通过", "；".join(f"{field}空值{count}" for field, count in blanks.items() if count) or "全部非空"))

    invalid_present = sum(row.get("adjudicated_present", "").strip() not in {"是", "否"} for row in rows)
    invalid_level = sum(row.get("adjudicated_level", "").strip() not in {"L1", "L2", "L3", "L4", "未出现"} for row in rows)
    inconsistent = sum(
        (row.get("adjudicated_present", "").strip() == "否" and row.get("adjudicated_level", "").strip() != "未出现")
        or (row.get("adjudicated_present", "").strip() == "是" and row.get("adjudicated_level", "").strip() not in {"L1", "L2", "L3", "L4"})
        for row in rows
    )
    checks.append(("裁决取值", "通过" if invalid_present == 0 and invalid_level == 0 else "不通过", f"present非法 {invalid_present}；level非法 {invalid_level}"))
    checks.append(("裁决逻辑", "通过" if inconsistent == 0 else "不通过", f"present/level逻辑不一致 {inconsistent}"))
    return checks


def main() -> int:
    parser = argparse.ArgumentParser(description="仅从完整裁决表生成唯一 final_coding.csv。")
    parser.add_argument("--input", required=True, help="已完成裁决的CSV。")
    parser.add_argument("--output", default="07_analysis/data/final_coding.csv", help="通过门禁后写入的唯一分析表。")
    parser.add_argument("--qa-output", default="07_analysis/results/formal_rater_r01/final_coding_build_qa.csv", help="门禁检查CSV。")
    args = parser.parse_args()

    input_path = _path(args.input)
    output_path = _path(args.output)
    qa_path = _path(args.qa_output)
    if not input_path.exists():
        print(f"输入不存在：{input_path}", file=sys.stderr)
        return 2

    rows, fields = _read_rows(input_path)
    checks = _validate(rows, fields)
    _write_csv(qa_path, ["check_item", "status", "evidence_or_result"], [
        {"check_item": item, "status": status, "evidence_or_result": detail} for item, status, detail in checks
    ])
    failures = [check for check in checks if check[1] != "通过"]
    if failures:
        print(f"裁决门禁未通过：{len(failures)}项。未生成 {output_path}。", file=sys.stderr)
        return 1

    source_sha = hashlib.sha256(input_path.read_bytes()).hexdigest()
    output_rows = []
    for row in rows:
        present_label = row["adjudicated_present"].strip()
        output_rows.append({
            **{field: row[field].strip() for field in KEY_FIELDS},
            "present": "1" if present_label == "是" else "0",
            "present_label": present_label,
            "level": row["adjudicated_level"].strip(),
            "evidence": row["adjudicated_evidence"].strip(),
            "adjudicator": row["adjudicator"].strip(),
            "adjudication_date": row["adjudication_date"].strip(),
            "adjudication_reason": row["adjudication_reason"].strip(),
            "source_adjudication_sha256": source_sha,
        })
    _write_csv(output_path, OUTPUT_FIELDS, output_rows)
    print(f"已生成唯一分析表：{output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
