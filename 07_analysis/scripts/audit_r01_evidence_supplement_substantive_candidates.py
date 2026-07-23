from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def resolve(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def compact(value: str) -> str:
    return re.sub(r"\s+", "", value or "")


def main() -> None:
    parser = argparse.ArgumentParser(description="标记逐字可定位但仍需实质审查的R01补正证据候选。")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--qa-output", required=True)
    args = parser.parse_args()
    with resolve(args.input).open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))

    candidates: list[dict[str, str]] = []
    short_solution = same_quote = 0
    for row in rows:
        reasons: list[str] = []
        if len(compact(row["solution_step_quote"])) < 8:
            reasons.append("解答引文少于8个非空字符，需确认是否为足以支撑判断的完整公式或步骤")
            short_solution += 1
        if compact(row["question_trigger_quote"]) == compact(row["solution_step_quote"]):
            reasons.append("题干引文与解答引文完全相同，需确认答案并非误填题干")
            same_quote += 1
        if reasons:
            candidates.append({
                "item_id": row["item_id"], "dimension": row["dimension"], "item_text_path": row["item_text_path"],
                "question_trigger_quote": row["question_trigger_quote"], "question_location": row["question_location"],
                "solution_step_quote": row["solution_step_quote"], "solution_location": row["solution_location"],
                "current_present": row["rechecked_present"], "current_level": row["rechecked_level"],
                "adjacent_level_exclusion": row["adjacent_level_exclusion"], "review_reason": "；".join(reasons),
                "required_review": "回到同一item_text的参考解答，确认引文能够实质支撑该维度与等级；若不能，替换为更完整的连续原文或如实建议更正。",
            })

    output = resolve(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    fields = ["item_id", "dimension", "item_text_path", "question_trigger_quote", "question_location", "solution_step_quote", "solution_location", "current_present", "current_level", "adjacent_level_exclusion", "review_reason", "required_review"]
    with output.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(candidates)

    qa_output = resolve(args.qa_output)
    with qa_output.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["check_item", "observed", "interpretation"], lineterminator="\n")
        writer.writeheader()
        writer.writerow({"check_item": "解答引文少于8个非空字符", "observed": short_solution, "interpretation": "候选审查数，不以长度单独否定公式类证据"})
        writer.writerow({"check_item": "题干与解答引文完全相同", "observed": same_quote, "interpretation": "候选审查数，需确认解答栏并非误填题干"})
        writer.writerow({"check_item": "需实质审查的唯一记录", "observed": len(candidates), "interpretation": "定位通过不等于编码证据实质充分"})
    print(f"实质审查候选：{len(candidates)}条；短解答{short_solution}条；题干解答相同{same_quote}条")


if __name__ == "__main__":
    main()
