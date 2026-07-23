from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def resolve(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def normalized(value: str) -> str:
    return re.sub(r"\s+", "", value or "")


def main() -> None:
    parser = argparse.ArgumentParser(description="输出R01补证回填的逐字段引文返工清单。")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    with resolve(args.input).open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    issues: list[dict[str, str]] = []
    for number, row in enumerate(rows, start=2):
        text_path = resolve(row["item_text_path"])
        text = normalized(text_path.read_text(encoding="utf-8")) if text_path.exists() else ""
        for field, label in (("repaired_question_quote", "题干引文"), ("repaired_solution_quote", "解答引文")):
            quote = normalized(row[field])
            if len(quote) < 8:
                issues.append({
                    "csv_line": str(number), "item_id": row["item_id"], "dimension": row["dimension"],
                    "field": field, "issue_type": "少于8个非空字符", "observed": row[field],
                    "required_action": f"从{label}所在原文复制至少8个非空字符的连续原句。",
                })
            elif quote not in text:
                issues.append({
                    "csv_line": str(number), "item_id": row["item_id"], "dimension": row["dimension"],
                    "field": field, "issue_type": "无法在item_text_path逐字定位", "observed": row[field],
                    "required_action": f"仅从该行item_text_path复制{label}原文，不要改写、截断或混用其他小问。",
                })
    output = resolve(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["csv_line", "item_id", "dimension", "field", "issue_type", "observed", "required_action"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(issues)
    print(f"补证引文内容审计：{len(issues)}个字段需返工。")


if __name__ == "__main__":
    main()
