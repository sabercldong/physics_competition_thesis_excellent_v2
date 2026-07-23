from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
KEY = ("item_id", "dimension")
PACKETS = (
    ("58条实质审查", "07_analysis/data/rater_returns/registered/R01/r01_substantive_evidence_review_R01_FILLED_20260723_registered_lf.csv"),
    ("16条高风险审查", "07_analysis/data/rater_returns/registered/R01/r01_high_risk_case_review_R01_FILLED_20260723_registered_lf.csv"),
)
TEMPLATE_FIELDS = [
    "packet_version", "source_review_packets", "item_id", "dimension", "item_text_path",
    "current_present", "current_level", "reviewed_present", "reviewed_level",
    "original_question_trigger_quote", "original_question_location", "original_solution_step_quote", "original_solution_location",
    "evidence_gap_reason", "existing_support_explanation", "repairer_id", "repair_date",
    "repaired_question_quote", "repaired_question_location", "repaired_solution_quote", "repaired_solution_location",
    "evidence_recheck_decision", "rechecked_present", "rechecked_level", "correction_reason", "repairer_statement",
]


def resolve(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_rows(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="汇总R01实质审查中需补充引文的记录，生成受控回填模板。")
    parser.add_argument("--final-coding", default="07_analysis/data/final_coding_r01_correction_v1.csv")
    parser.add_argument("--template-output", required=True)
    parser.add_argument("--manifest-output", required=True)
    parser.add_argument("--item-worklist-output", required=True)
    parser.add_argument("--qa-output", required=True)
    args = parser.parse_args()

    final_path = resolve(args.final_coding)
    final_rows = read_rows(final_path)
    final_lookup = {(row["item_id"], row["dimension"]): row for row in final_rows}
    if len(final_rows) != 876 or len(final_lookup) != 876:
        raise ValueError("版本化分析表必须为876条唯一item_id/dimension记录")

    merged: dict[tuple[str, str], dict[str, object]] = {}
    source_counts: dict[str, int] = {}
    for packet_name, relative in PACKETS:
        rows = read_rows(ROOT / relative)
        candidates = [row for row in rows if row.get("evidence_support_decision", "").strip() == "需补充引文"]
        source_counts[packet_name] = len(candidates)
        for row in candidates:
            key = tuple(row[field].strip() for field in KEY)
            if key not in final_lookup:
                raise ValueError(f"审查记录无法映射当前分析表：{key}")
            if key not in merged:
                merged[key] = {"row": row, "sources": [packet_name]}
            else:
                existing = merged[key]
                existing["sources"].append(packet_name)  # type: ignore[index]
                original = existing["row"]  # type: ignore[assignment]
                if (original["current_present"], original["current_level"]) != (row["current_present"], row["current_level"]):
                    raise ValueError(f"同一键在两份审查中的当前值冲突：{key}")

    template_rows: list[dict[str, str]] = []
    manifest_rows: list[dict[str, str]] = []
    for key in sorted(merged):
        entry = merged[key]
        row = entry["row"]  # type: ignore[assignment]
        current = final_lookup[key]
        sources = "；".join(entry["sources"])  # type: ignore[arg-type]
        template_rows.append({
            "packet_version": "G4-20-R01-2026-07-23",
            "source_review_packets": sources,
            "item_id": key[0], "dimension": key[1], "item_text_path": row["item_text_path"],
            "current_present": current["present_label"], "current_level": current["level"],
            "reviewed_present": row["current_present"], "reviewed_level": row["current_level"],
            "original_question_trigger_quote": row["question_trigger_quote"], "original_question_location": row["question_location"],
            "original_solution_step_quote": row["solution_step_quote"], "original_solution_location": row["solution_location"],
            "evidence_gap_reason": row["support_explanation"], "existing_support_explanation": row["adjacent_level_exclusion"],
            "repairer_id": "", "repair_date": "", "repaired_question_quote": "", "repaired_question_location": "",
            "repaired_solution_quote": "", "repaired_solution_location": "", "evidence_recheck_decision": "",
            "rechecked_present": "", "rechecked_level": "", "correction_reason": "", "repairer_statement": "",
        })
        manifest_rows.append({
            "item_id": key[0], "dimension": key[1], "source_review_packets": sources,
            "current_present": current["present_label"], "current_level": current["level"],
            "source_final_coding_sha256": hashlib.sha256(final_path.read_bytes()).hexdigest(),
        })

    write_rows(resolve(args.template_output), TEMPLATE_FIELDS, template_rows)
    write_rows(resolve(args.manifest_output), ["item_id", "dimension", "source_review_packets", "current_present", "current_level", "source_final_coding_sha256"], manifest_rows)
    by_item: dict[str, list[dict[str, str]]] = {}
    for order, row in enumerate(template_rows, start=1):
        by_item.setdefault(row["item_id"], []).append({**row, "return_row_order": str(order)})
    item_rows = []
    for item_id, rows in sorted(by_item.items()):
        item_rows.append({
            "item_id": item_id,
            "item_text_path": rows[0]["item_text_path"],
            "pending_dimensions": "；".join(row["dimension"] for row in rows),
            "pending_record_count": str(len(rows)),
            "source_review_packets": "；".join(sorted({row["source_review_packets"] for row in rows})),
            "current_values": "；".join(f"{row['dimension']}={row['current_present']}/{row['current_level']}" for row in rows),
            "return_row_order": "；".join(row["return_row_order"] for row in rows),
        })
    write_rows(resolve(args.item_worklist_output), [
        "item_id", "item_text_path", "pending_dimensions", "pending_record_count", "source_review_packets", "current_values", "return_row_order",
    ], item_rows)
    checks = [
        ("58条审查需补引文数", str(source_counts["58条实质审查"]), "24", source_counts["58条实质审查"] == 24),
        ("16条审查需补引文数", str(source_counts["16条高风险审查"]), "8", source_counts["16条高风险审查"] == 8),
        ("合并后唯一键数", str(len(template_rows)), "32", len(template_rows) == 32),
        ("按题目工作单数", str(len(item_rows)), "8", len(item_rows) == 8),
        ("模板与当前分析表映射", "32/32", "32/32", len(template_rows) == 32),
        ("工作字段为空", "是" if all(not row["repairer_id"] for row in template_rows) else "否", "是", all(not row["repairer_id"] for row in template_rows)),
    ]
    write_rows(resolve(args.qa_output), ["check_item", "observed", "expected", "status"], [
        {"check_item": item, "observed": observed, "expected": expected, "status": "通过" if passed else "不通过"}
        for item, observed, expected, passed in checks
    ])
    print(f"已生成{len(template_rows)}条需补充引文回填模板。")


if __name__ == "__main__":
    main()
