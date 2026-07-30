#!/usr/bin/env python3
"""Build the V3 unique coding table after an explicit G8-80 acceptance gate."""

from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
from pathlib import Path

from build_v3_author_review_package import ROOT
from build_v3_cross_year_audit import read_rows, write_rows


EXPECTED_ROWS = 884
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ACCEPTANCE_FIELDS = [
    "intake_id",
    "accepted_review_sha256",
    "qa_reviewer_or_code",
    "qa_date",
    "qa_decision",
    "immutable_fields_confirmed",
    "high_risk_flags_resolved",
    "pending_records_resolved",
    "evidence_spotcheck_completed",
    "qa_report_path",
    "qa_statement",
]
YES_FIELDS = [
    "immutable_fields_confirmed",
    "high_risk_flags_resolved",
    "pending_records_resolved",
    "evidence_spotcheck_completed",
]
OUTPUT_FIELDS = [
    "review_row_id",
    "item_id",
    "competition_no",
    "year",
    "question_no",
    "subquestion_no",
    "dimension",
    "analysis_unit",
    "item_text_path",
    "item_text_sha256",
    "solution_text_path",
    "solution_text_sha256",
    "required_output",
    "question_quote",
    "question_location",
    "solution_quote",
    "solution_location",
    "necessary_cognitive_activity",
    "present",
    "present_label",
    "level",
    "candidate_present_label",
    "candidate_level",
    "author_review_decision",
    "author_review_reason",
    "adjacent_level_review",
    "post_review_evidence_location",
    "author_reviewer_or_code",
    "author_review_date",
    "g8_80_qa_reviewer_or_code",
    "g8_80_qa_date",
    "source_author_review_sha256",
    "source_g8_80_acceptance_sha256",
]
QA_FIELDS = ["check_id", "check_item", "status", "detail"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--review", type=Path, required=True)
    parser.add_argument("--acceptance", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--qa-output", type=Path, required=True)
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def add_check(
    checks: list[dict[str, str]],
    item: str,
    passed: bool,
    detail: str,
) -> None:
    checks.append(
        {
            "check_id": f"V3FINAL-QA-{len(checks) + 1:02d}",
            "check_item": item,
            "status": "通过" if passed else "不通过",
            "detail": detail,
        }
    )


def main() -> None:
    args = parse_args()
    review_path = resolve(args.review)
    acceptance_path = resolve(args.acceptance)
    output_path = resolve(args.output)
    qa_path = resolve(args.qa_output)
    checks: list[dict[str, str]] = []

    if not review_path.is_file():
        raise SystemExit(f"作者复核文件不存在: {review_path}")
    if not acceptance_path.is_file():
        raise SystemExit(f"G8-80验收决定不存在: {acceptance_path}")

    validator = ROOT / "07_analysis/scripts/validate_v3_author_review.py"
    validation = subprocess.run(
        [sys.executable, str(validator), str(review_path), "--mode", "filled"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    add_check(
        checks,
        "作者复核全量成品校验",
        validation.returncode == 0,
        (validation.stdout + validation.stderr).strip(),
    )

    _, review_rows = read_rows(review_path)
    acceptance_fields, acceptance_rows = read_rows(acceptance_path)
    add_check(
        checks,
        "作者复核记录数",
        len(review_rows) == EXPECTED_ROWS,
        f"实际{len(review_rows)}行，要求{EXPECTED_ROWS}行",
    )
    add_check(
        checks,
        "G8-80验收表头",
        acceptance_fields == ACCEPTANCE_FIELDS,
        f"实际{len(acceptance_fields)}字段，要求{len(ACCEPTANCE_FIELDS)}字段",
    )
    add_check(
        checks,
        "G8-80验收记录数",
        len(acceptance_rows) == 1,
        f"实际{len(acceptance_rows)}行，要求1行",
    )

    review_hash = sha256(review_path)
    acceptance_hash = sha256(acceptance_path)
    acceptance = acceptance_rows[0] if len(acceptance_rows) == 1 else {}
    missing_acceptance = [
        field for field in ACCEPTANCE_FIELDS if not acceptance.get(field, "").strip()
    ]
    add_check(
        checks,
        "G8-80验收字段完整",
        not missing_acceptance,
        "全部非空" if not missing_acceptance else "缺失：" + "、".join(missing_acceptance),
    )
    add_check(
        checks,
        "复核文件哈希与验收登记一致",
        acceptance.get("accepted_review_sha256", "").strip() == review_hash,
        f"实际复核文件SHA-256={review_hash}",
    )
    add_check(
        checks,
        "G8-80明确接受",
        acceptance.get("qa_decision", "").strip() == "接受进入唯一编码表",
        f"qa_decision={acceptance.get('qa_decision', '')}",
    )
    yes_failures = [
        field for field in YES_FIELDS if acceptance.get(field, "").strip() != "是"
    ]
    add_check(
        checks,
        "G8-80四项放行确认",
        not yes_failures,
        "全部为是" if not yes_failures else "未确认：" + "、".join(yes_failures),
    )
    qa_date = acceptance.get("qa_date", "").strip()
    add_check(
        checks,
        "G8-80验收日期格式",
        bool(DATE_PATTERN.fullmatch(qa_date)),
        f"qa_date={qa_date}",
    )
    qa_report_value = acceptance.get("qa_report_path", "").strip()
    qa_report_path = resolve(Path(qa_report_value)) if qa_report_value else None
    add_check(
        checks,
        "G8-80人工QA报告可定位",
        bool(qa_report_path and qa_report_path.is_file()),
        str(qa_report_path) if qa_report_path else "未填写",
    )
    statement = acceptance.get("qa_statement", "").strip()
    add_check(
        checks,
        "G8-80验收声明",
        len(statement) >= 12,
        f"声明长度={len(statement)}",
    )

    pending_rows = [
        row
        for row in review_rows
        if row.get("candidate_review_decision") == "待核实"
        or row.get("rechecked_present_label") == "待核实"
        or row.get("rechecked_level") == "待核实"
        or row.get("author_review_status") in {"待补证", "待裁决"}
    ]
    add_check(
        checks,
        "作者复核无未闭合记录",
        not pending_rows,
        f"待核实、待补证或待裁决记录={len(pending_rows)}",
    )

    pair_keys = [
        (row.get("item_id", ""), row.get("dimension", "")) for row in review_rows
    ]
    add_check(
        checks,
        "分析单元×维度键唯一",
        len(pair_keys) == EXPECTED_ROWS and len(set(pair_keys)) == EXPECTED_ROWS,
        f"记录={len(pair_keys)}，唯一键={len(set(pair_keys))}",
    )
    item_dimensions: dict[str, set[str]] = {}
    for item_id, dimension in pair_keys:
        item_dimensions.setdefault(item_id, set()).add(dimension)
    expected_dimensions = {"模型建构", "科学推理", "科学论证", "质疑创新"}
    complete_items = sum(
        dimensions == expected_dimensions for dimensions in item_dimensions.values()
    )
    add_check(
        checks,
        "221个分析单元四维覆盖",
        len(item_dimensions) == 221 and complete_items == 221,
        f"分析单元={len(item_dimensions)}，四维完整={complete_items}",
    )
    add_check(
        checks,
        "输出路径防覆盖",
        not output_path.exists() or args.force,
        (
            "输出不存在或已显式使用--force"
            if not output_path.exists() or args.force
            else f"输出已存在：{output_path}"
        ),
    )

    write_rows(qa_path, QA_FIELDS, checks)
    failures = [check for check in checks if check["status"] != "通过"]
    if failures:
        raise SystemExit(
            f"G8-68唯一表门禁未通过：{len(failures)}项；未生成{output_path}"
        )

    output_rows = []
    for row in review_rows:
        present_label = row["rechecked_present_label"].strip()
        output_rows.append(
            {
                "review_row_id": row["review_row_id"],
                "item_id": row["item_id"],
                "competition_no": row["competition_no"],
                "year": row["year"],
                "question_no": row["question_no"],
                "subquestion_no": row["subquestion_no"],
                "dimension": row["dimension"],
                "analysis_unit": row["analysis_unit"],
                "item_text_path": row["item_text_path"],
                "item_text_sha256": row["item_text_sha256"],
                "solution_text_path": row["solution_text_path"],
                "solution_text_sha256": row["solution_text_sha256"],
                "required_output": row["required_output"],
                "question_quote": row["question_quote"],
                "question_location": row["question_location"],
                "solution_quote": row["solution_quote"],
                "solution_location": row["solution_location"],
                "necessary_cognitive_activity": row["necessary_cognitive_activity"],
                "present": "1" if present_label == "是" else "0",
                "present_label": present_label,
                "level": row["rechecked_level"].strip(),
                "candidate_present_label": row["present_label"],
                "candidate_level": row["level"],
                "author_review_decision": row["candidate_review_decision"],
                "author_review_reason": row["correction_reason"],
                "adjacent_level_review": row["adjacent_level_review"],
                "post_review_evidence_location": row[
                    "post_review_evidence_location"
                ],
                "author_reviewer_or_code": row[
                    "actual_author_reviewer_or_code"
                ],
                "author_review_date": row["actual_review_date"],
                "g8_80_qa_reviewer_or_code": acceptance[
                    "qa_reviewer_or_code"
                ].strip(),
                "g8_80_qa_date": acceptance["qa_date"].strip(),
                "source_author_review_sha256": review_hash,
                "source_g8_80_acceptance_sha256": acceptance_hash,
            }
        )
    write_rows(output_path, OUTPUT_FIELDS, output_rows)
    print(f"final_rows={len(output_rows)}")
    print(f"review_sha256={review_hash}")
    print(f"acceptance_sha256={acceptance_hash}")
    print(f"output={output_path}")
    print(f"qa={qa_path}")


if __name__ == "__main__":
    main()
