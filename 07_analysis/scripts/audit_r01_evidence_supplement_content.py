from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MISSING = ("未找到",)
GENERIC = ("题干含", "题面含", "假设识别", "条件", "题干要求", "题面要求")


def resolve(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def normalized(value: str) -> str:
    return re.sub(r"\s+", "", value or "")


def quote_is_locatable(quote: str, text: str, *, field: str) -> bool:
    quote = (quote or "").strip()
    if not quote or quote.startswith(MISSING):
        return False
    if field == "question" and quote.startswith(GENERIC):
        return False
    return len(normalized(quote)) >= 4 and normalized(quote) in normalized(text)


def main() -> None:
    parser = argparse.ArgumentParser(description="审计R01补正回填的逐条证据内容可定位性，不判断复核者身份或过程。")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    with resolve(args.input).open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    question_ok = solution_ok = both_ok = missing_with_sufficient = 0
    question_generic = solution_missing = 0
    for row in rows:
        text_path = resolve(row["item_text_path"])
        text = text_path.read_text(encoding="utf-8") if text_path.exists() else ""
        q = row["question_trigger_quote"]
        s = row["solution_step_quote"]
        q_ok = quote_is_locatable(q, text, field="question")
        s_ok = quote_is_locatable(s, text, field="solution")
        question_ok += q_ok
        solution_ok += s_ok
        both_ok += q_ok and s_ok
        question_generic += (q or "").strip().startswith(GENERIC)
        solution_missing += (s or "").strip().startswith(MISSING)
        missing_with_sufficient += row.get("evidence_sufficiency", "").strip() == "充分" and (not q_ok or not s_ok)
    checks = [
        ("内容记录数", len(rows), "876", len(rows) == 876),
        ("题干引语可在题目整理文本定位", question_ok, "876", question_ok == 876),
        ("解答步骤可在题目整理文本定位", solution_ok, "876", solution_ok == 876),
        ("题干与解答证据均可定位", both_ok, "876", both_ok == 876),
        ("题干引语使用通用标签", question_generic, "0", question_generic == 0),
        ("解答步骤写为未找到对应步骤", solution_missing, "0", solution_missing == 0),
        ("证据充分但至少一侧不可定位", missing_with_sufficient, "0", missing_with_sufficient == 0),
    ]
    output = resolve(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["check_item", "observed", "expected", "status"], lineterminator="\n")
        writer.writeheader()
        for item, observed, expected, passed in checks:
            writer.writerow({"check_item": item, "observed": observed, "expected": expected, "status": "通过" if passed else "不通过"})
    failures = sum(not passed for _, _, _, passed in checks)
    print(f"内容定位检查：{len(checks) - failures}/{len(checks)}通过")


if __name__ == "__main__":
    main()
