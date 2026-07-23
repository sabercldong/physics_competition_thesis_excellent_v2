from __future__ import annotations

import argparse
import csv
import hashlib
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
KEY = ("item_id", "dimension")
CURRENT = "07_analysis/data/final_coding_r01_correction_v1.csv"
V6 = "07_analysis/data/rater_returns/registered/R01/r01_evidence_supplement_R01_FILLED_20260723_V6_registered_lf.csv"
CORRECTIONS = "07_analysis/data/rater_returns/incoming/R01/r01_correction_adjudication_R01_FILLED_20260723.csv"
EXPECTED_REPAIR_ITEMS = {"CPHO41-Q05-4", "CPHO41-Q07-4", "CPHO42-Q04-2"}


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


def same_csv_content(path: Path, fields: list[str], rows: list[dict[str, str]]) -> bool:
    if not path.exists():
        return False
    existing_rows, existing_fields = read_rows(path)
    return existing_fields == fields and existing_rows == rows


def normalized(value: str) -> str:
    return re.sub(r"\s+", "", value or "")


def main() -> int:
    parser = argparse.ArgumentParser(description="整合R01 V6、补证V2与更正裁决为当前876条证据链。")
    parser.add_argument("--repair-v1", required=True)
    parser.add_argument("--repair-v2", required=True)
    parser.add_argument("--registered-repair-v2", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--qa-output", required=True)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    paths = {"current": resolve(CURRENT), "v6": resolve(V6), "corrections": resolve(CORRECTIONS), "repair_v1": resolve(args.repair_v1), "repair_v2": resolve(args.repair_v2)}
    current_rows, _ = read_rows(paths["current"])
    v6_rows, _ = read_rows(paths["v6"])
    correction_rows, _ = read_rows(paths["corrections"])
    repair_v1, repair_fields = read_rows(paths["repair_v1"])
    repair_v2, repair_v2_fields = read_rows(paths["repair_v2"])
    output_path, qa_path, registered_path = resolve(args.output), resolve(args.qa_output), resolve(args.registered_repair_v2)

    current_lookup = {tuple(row[field] for field in KEY): row for row in current_rows}
    v6_lookup = {tuple(row[field] for field in KEY): row for row in v6_rows}
    repair_v1_lookup = {tuple(row[field] for field in KEY): row for row in repair_v1}
    repair_v2_lookup = {tuple(row[field] for field in KEY): row for row in repair_v2}
    correction_lookup = {tuple(row[field] for field in KEY): row for row in correction_rows}
    repair_changes = []
    for key, before in repair_v1_lookup.items():
        after = repair_v2_lookup.get(key, {})
        changed_fields = [field for field in repair_fields if before.get(field, "") != after.get(field, "")]
        if changed_fields:
            repair_changes.append((key, changed_fields))
    allowed_changes = all(fields == ["repaired_solution_quote"] for _, fields in repair_changes)
    changed_keys = {key for key, _ in repair_changes}
    expected_keys = {(item, dimension) for item in EXPECTED_REPAIR_ITEMS for dimension in ("模型建构", "科学推理", "科学论证", "质疑创新")}
    repair_support = all(row.get("evidence_recheck_decision") == "充分支持" for row in repair_v2)
    repair_value_match = all(
        key in current_lookup and (row["rechecked_present"], row["rechecked_level"]) == (current_lookup[key]["present_label"], current_lookup[key]["level"])
        for key, row in repair_v2_lookup.items()
    )
    correction_value_match = all(
        key in current_lookup and (row["final_present"], row["final_level"]) == (current_lookup[key]["present_label"], current_lookup[key]["level"])
        for key, row in correction_lookup.items()
    )
    registered_reusable = same_csv_content(registered_path, repair_v2_fields, repair_v2)
    checks = [
        ("当前分析表记录与键", f"{len(current_rows)}/{len(current_lookup)}", "876/876", len(current_rows) == len(current_lookup) == 876),
        ("V6记录与键", f"{len(v6_rows)}/{len(v6_lookup)}", "876/876", len(v6_rows) == len(v6_lookup) == 876),
        ("V6与当前表键集合", "一致" if set(v6_lookup) == set(current_lookup) else "不一致", "一致", set(v6_lookup) == set(current_lookup)),
        ("补证V1/V2键序", "一致" if list(repair_v1_lookup) == list(repair_v2_lookup) and len(repair_v2) == 32 else "不一致", "32条一致", list(repair_v1_lookup) == list(repair_v2_lookup) and len(repair_v2) == 32),
        ("V2仅改解答引文", "是" if allowed_changes else "否", "是", allowed_changes),
        ("V2变更键", str(len(changed_keys)), "12", changed_keys == expected_keys),
        ("V2全部充分支持且匹配当前值", "是" if repair_support and repair_value_match else "否", "是", repair_support and repair_value_match),
        ("4条更正与当前值匹配", "是" if correction_value_match and len(correction_lookup) == 4 else "否", "是", correction_value_match and len(correction_lookup) == 4),
        ("输出路径防覆盖", "通过" if not output_path.exists() or args.force else "不通过", "通过", not output_path.exists() or args.force),
        ("登记副本路径防覆盖", "通过" if not registered_path.exists() or registered_reusable or args.force else "不通过", "通过", not registered_path.exists() or registered_reusable or args.force),
    ]
    if any(not passed for *_, passed in checks):
        write_rows(qa_path, ["check_item", "observed", "expected", "status"], [
            {"check_item": item, "observed": observed, "expected": expected, "status": "通过" if passed else "不通过"}
            for item, observed, expected, passed in checks
        ])
        print("当前证据链前置门禁未通过。", file=sys.stderr)
        return 1

    if not registered_path.exists() or args.force:
        write_rows(registered_path, repair_v2_fields, repair_v2)
    source_shas = {name: hashlib.sha256(path.read_bytes()).hexdigest() for name, path in paths.items()}
    output_rows = []
    for key, current in current_lookup.items():
        source = "R01-V6"
        evidence = v6_lookup[key]
        if key in repair_v2_lookup:
            source, evidence = "R01-EVIDENCE-REPAIR-V2", repair_v2_lookup[key]
            question_quote, question_location = evidence["repaired_question_quote"], evidence["repaired_question_location"]
            solution_quote, solution_location = evidence["repaired_solution_quote"], evidence["repaired_solution_location"]
            source_sha = source_shas["repair_v2"]
        elif key in correction_lookup:
            source, evidence = "ADJ-02-CORRECTION", correction_lookup[key]
            question_quote, question_location = evidence["question_trigger_quote"], evidence["question_location"]
            solution_quote, solution_location = evidence["solution_step_quote"], evidence["solution_location"]
            source_sha = source_shas["corrections"]
        else:
            question_quote, question_location = evidence["question_trigger_quote"], evidence["question_location"]
            solution_quote, solution_location = evidence["solution_step_quote"], evidence["solution_location"]
            source_sha = source_shas["v6"]
        output_rows.append({
            "item_id": key[0], "dimension": key[1], "item_text_path": evidence["item_text_path"],
            "current_present": current["present_label"], "current_level": current["level"],
            "question_quote": question_quote, "question_location": question_location,
            "solution_quote": solution_quote, "solution_location": solution_location,
            "evidence_source": source, "evidence_source_sha256": source_sha,
        })
    locate_ok = all(
        (text_path := resolve(row["item_text_path"])).exists()
        and len(normalized(row["question_quote"])) >= 4 and len(normalized(row["solution_quote"])) >= 4
        and normalized(row["question_quote"]) in normalized(text_path.read_text(encoding="utf-8"))
        and normalized(row["solution_quote"]) in normalized(text_path.read_text(encoding="utf-8"))
        for row in output_rows
    )
    repair_rows = [row for row in output_rows if row["evidence_source"] == "R01-EVIDENCE-REPAIR-V2"]
    repair_strong = all(
        len(normalized(row["question_quote"])) >= 8 and len(normalized(row["solution_quote"])) >= 8
        and normalized(row["question_quote"]) != normalized(row["solution_quote"])
        for row in repair_rows
    )
    checks.append(("876条当前双侧证据可定位", "通过" if locate_ok else "不通过", "通过", locate_ok))
    checks.append(("32条补证记录长度与双侧不重复", "通过" if len(repair_rows) == 32 and repair_strong else "不通过", "通过", len(repair_rows) == 32 and repair_strong))
    source_counts = {source: sum(row["evidence_source"] == source for row in output_rows) for source in {row["evidence_source"] for row in output_rows}}
    expected_sources = {"R01-V6": 840, "R01-EVIDENCE-REPAIR-V2": 32, "ADJ-02-CORRECTION": 4}
    checks.append(("证据来源分布", str(source_counts), str(expected_sources), source_counts == expected_sources))
    if not locate_ok or not repair_strong or len(repair_rows) != 32 or source_counts != expected_sources:
        write_rows(qa_path, ["check_item", "observed", "expected", "status"], [
            {"check_item": item, "observed": observed, "expected": expected, "status": "通过" if passed else "不通过"}
            for item, observed, expected, passed in checks
        ])
        print("当前证据链内容门禁未通过。", file=sys.stderr)
        return 1
    write_rows(output_path, [
        "item_id", "dimension", "item_text_path", "current_present", "current_level", "question_quote", "question_location",
        "solution_quote", "solution_location", "evidence_source", "evidence_source_sha256",
    ], output_rows)
    write_rows(qa_path, ["check_item", "observed", "expected", "status"], [
        {"check_item": item, "observed": observed, "expected": expected, "status": "通过" if passed else "不通过"}
        for item, observed, expected, passed in checks
    ])
    print("已生成876条当前编码—证据链。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
