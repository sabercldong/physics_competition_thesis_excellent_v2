from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
KEY = ("item_id", "dimension")
WORK = (
    "repairer_id", "repair_date", "repaired_question_quote", "repaired_question_location",
    "repaired_solution_quote", "repaired_solution_location", "evidence_recheck_decision",
    "rechecked_present", "rechecked_level", "correction_reason", "repairer_statement",
)


def resolve(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def normalized(value: str) -> str:
    return re.sub(r"\s+", "", value or "")


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["check_item", "observed", "expected", "status"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="验证R01需补充引文回填。")
    parser.add_argument("--input", required=True)
    parser.add_argument("--template", default="07_analysis/data/rater_returns/templates/R01/r01_evidence_repair_template_v1.csv")
    parser.add_argument("--qa-output", required=True)
    args = parser.parse_args()
    rows, template = read_rows(resolve(args.input)), read_rows(resolve(args.template))
    keys = [tuple(row[field].strip() for field in KEY) for row in rows]
    template_keys = [tuple(row[field].strip() for field in KEY) for row in template]
    complete = all(all(row[field].strip() for field in WORK) for row in rows)
    decisions = {"充分支持", "仍需补充", "不支持当前编码"}
    enum_ok = all(row["evidence_recheck_decision"].strip() in decisions for row in rows)
    logical = all(
        (row["rechecked_present"].strip() == "否") == (row["rechecked_level"].strip() == "未出现")
        and row["rechecked_present"].strip() in {"是", "否"}
        and row["rechecked_level"].strip() in {"L1", "L2", "L3", "L4", "未出现"}
        for row in rows
    )
    quotes_ok = all(
        len(normalized(row[field])) >= 8
        for row in rows for field in ("repaired_question_quote", "repaired_solution_quote")
    )
    locatable = all(
        (text_path := resolve(row["item_text_path"])).exists()
        and len(normalized(row["repaired_question_quote"])) >= 8
        and len(normalized(row["repaired_solution_quote"])) >= 8
        and normalized(row["repaired_question_quote"]) in normalized(text_path.read_text(encoding="utf-8"))
        and normalized(row["repaired_solution_quote"]) in normalized(text_path.read_text(encoding="utf-8"))
        for row in rows
    )
    distinct = all(
        normalized(row["repaired_question_quote"]) != normalized(row["repaired_solution_quote"])
        for row in rows
    )
    support_match = all(
        row["evidence_recheck_decision"].strip() != "充分支持"
        or (row["rechecked_present"].strip(), row["rechecked_level"].strip()) == (row["current_present"].strip(), row["current_level"].strip())
        for row in rows
    )
    checks = [
        ("记录数", str(len(rows)), "32", len(rows) == 32),
        ("不可变键与模板同序", "一致" if keys == template_keys else "不一致", "一致", keys == template_keys),
        ("工作字段完整", "完整" if complete else "有空值", "完整", complete),
        ("复核决定枚举", "合法" if enum_ok else "非法", "合法", enum_ok),
        ("存在性与等级逻辑", "合法" if logical else "非法", "合法", logical),
        ("补充引文最小长度", "合格" if quotes_ok else "不合格", "合格", quotes_ok),
        ("补充引文可在题目整理文本定位", "合格" if locatable else "不合格", "合格", locatable),
        ("题干与解答补充引文不重复", "合格" if distinct else "不合格", "合格", distinct),
        ("充分支持保持当前值", "一致" if support_match else "不一致", "一致", support_match),
    ]
    write_rows(resolve(args.qa_output), [
        {"check_item": item, "observed": observed, "expected": expected, "status": "通过" if passed else "不通过"}
        for item, observed, expected, passed in checks
    ])
    print(f"需补充引文回填检查：{sum(passed for *_, passed in checks)}/{len(checks)}通过")


if __name__ == "__main__":
    main()
