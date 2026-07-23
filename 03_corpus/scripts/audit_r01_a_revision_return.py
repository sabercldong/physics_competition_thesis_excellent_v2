from __future__ import annotations

import argparse
import csv
import hashlib
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
GENERIC_SUMMARIES = {
    "与V1转写稿一致；OCR杂字不影响编码未发现影响正式编码的题面误转",
    "答案公式核对表与原始解答一致；关键公式和变量定义正确",
}


def project_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    parser = argparse.ArgumentParser(description="检查R01 A组重填副本的结构、旧版差异与摘要特异性。")
    parser.add_argument("--old", required=True)
    parser.add_argument("--new", required=True)
    parser.add_argument("--registered", required=True)
    parser.add_argument("--qa-output", required=True)
    parser.add_argument("--diff-output", required=True)
    args = parser.parse_args()

    old_path = project_path(args.old)
    new_path = project_path(args.new)
    registered_path = project_path(args.registered)
    old_rows, new_rows = load_csv(old_path), load_csv(new_path)
    old_by_issue = {row["issue_id"]: row for row in old_rows}
    new_by_issue = {row["issue_id"]: row for row in new_rows}
    required = (
        "actual_reviewer_or_code", "actual_review_date", "actual_review_decision",
        "correction_required", "correction_summary", "post_review_evidence_location", "post_review_status",
    )
    immutable = (
        "issue_id", "material_id", "competition_no", "year", "question_no", "issue_type",
        "source_path", "source_page_range", "source_text_or_formula_anchor", "risk_description",
        "review_task", "suggested_decision_options", "rendered_evidence_paths", "manual_review_entry_path",
        "formula_check_entry_path", "figure_asset_path", "boundary_note",
    )
    expected_issues = set(old_by_issue)
    new_issues = set(new_by_issue)
    immutable_diffs = [
        (issue, field) for issue in expected_issues & new_issues
        for field in immutable if old_by_issue[issue].get(field) != new_by_issue[issue].get(field)
    ]
    required_filled = sum(all(row.get(field, "").strip() for field in required) for row in new_rows)
    valid_dates = sum(row.get("actual_review_date") == "2026-07-23" for row in new_rows)
    valid_reviewer = sum(row.get("actual_reviewer_or_code") == "R01" for row in new_rows)
    valid_decisions = sum(
        row.get("actual_review_decision", "") in row.get("suggested_decision_options", "").split(";")
        for row in new_rows
    )
    evidence_paths = [
        value.strip() for row in new_rows for value in row.get("post_review_evidence_location", "").split(";") if value.strip()
    ]
    evidence_exists = sum((ROOT / value).exists() for value in evidence_paths)
    generic_rows = [row for row in new_rows if row.get("correction_summary") in GENERIC_SUMMARIES]
    targeted_rows = [row for row in new_rows if row.get("correction_summary") not in GENERIC_SUMMARIES]
    changed_summaries = sum(
        issue in old_by_issue and old_by_issue[issue].get("correction_summary") != row.get("correction_summary")
        for issue, row in new_by_issue.items()
    )
    qa_rows = [
        ("A2INT-01", "行数", "76", str(len(new_rows)), len(new_rows) == 76),
        ("A2INT-02", "问题集合", "与旧版76个issue_id一致", f"{len(expected_issues & new_issues)}/76", expected_issues == new_issues),
        ("A2INT-03", "不可变字段", "逐行无差异", f"差异{len(immutable_diffs)}", not immutable_diffs),
        ("A2INT-04", "必填回填字段", "76/76完整", f"{required_filled}/76", required_filled == 76),
        ("A2INT-05", "复核者与日期", "R01；2026-07-23", f"R01 {valid_reviewer}/76；日期 {valid_dates}/76", valid_reviewer == valid_dates == 76),
        ("A2INT-06", "决定选项", "76/76属于允许选项", f"{valid_decisions}/76", valid_decisions == 76),
        ("A2INT-07", "复核后证据路径", "全部项目内路径存在", f"{evidence_exists}/{len(evidence_paths)}", evidence_exists == len(evidence_paths)),
        ("A2INT-08", "相对旧版的摘要更新", "76行均改变", f"{changed_summaries}/76", changed_summaries == 76),
        ("A2INT-09", "摘要材料特异性", "76行均非通用句式", f"特异 {len(targeted_rows)}/76；通用 {len(generic_rows)}/76", not generic_rows),
        ("A2INT-10", "原件与登记副本", "字段和值一致，仅换行规范化", f"原件 {digest(new_path)}；登记 {digest(registered_path)}", load_csv(new_path) == load_csv(registered_path)),
    ]
    qa_path = project_path(args.qa_output)
    qa_path.parent.mkdir(parents=True, exist_ok=True)
    with qa_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["check_id", "check_scope", "expected", "observed", "result"], lineterminator="\n")
        writer.writeheader()
        for check_id, scope, expected, observed, passed in qa_rows:
            writer.writerow({"check_id": check_id, "check_scope": scope, "expected": expected, "observed": observed, "result": "PASS" if passed else "FAIL"})
    diff_path = project_path(args.diff_output)
    with diff_path.open("w", encoding="utf-8-sig", newline="") as handle:
        fields = ["issue_id", "material_id", "competition_no", "issue_type", "old_correction_summary", "new_correction_summary", "summary_class"]
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for issue in sorted(expected_issues):
            old, new = old_by_issue[issue], new_by_issue[issue]
            writer.writerow({
                "issue_id": issue, "material_id": new["material_id"], "competition_no": new["competition_no"], "issue_type": new["issue_type"],
                "old_correction_summary": old["correction_summary"], "new_correction_summary": new["correction_summary"],
                "summary_class": "通用句式，待补强" if new["correction_summary"] in GENERIC_SUMMARIES else "材料特异摘要",
            })
    print(f"A组重填接收检查：{sum(passed for *_, passed in qa_rows)}/{len(qa_rows)}通过；材料特异摘要{len(targeted_rows)}/76")


if __name__ == "__main__":
    main()
