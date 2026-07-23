from __future__ import annotations

import argparse
import csv
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PLACEHOLDERS = ("补充引用材料中的相关文本以确保长度满足要求",)
GENERIC_EXCLUSIONS = (
    "维度不存在，无需排除相邻等级",
    "维度「质疑创新」经判定不存在于本题，无需考虑相邻等级排除",
    "单一关系直接推断，无需多步推理",
    "L2为多关系并列推理，L3为复杂推理链，两者在推理步骤数量和关系嵌套上有明确界限",
)


def resolve(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def compact(value: str) -> str:
    return re.sub(r"\s+", "", value or "")


def locatable(quote: str, text: str) -> bool:
    quote = (quote or "").strip()
    return bool(quote) and quote not in PLACEHOLDERS and len(compact(quote)) >= 4 and compact(quote) in compact(text)


def main() -> None:
    parser = argparse.ArgumentParser(description="为R01 V2补正回填生成逐条内容返工清单。")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--qa-output", required=True)
    args = parser.parse_args()
    with resolve(args.input).open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))

    worklist: list[dict[str, str]] = []
    flags = Counter()
    for row in rows:
        item_path = resolve(row["item_text_path"])
        text = item_path.read_text(encoding="utf-8") if item_path.exists() else ""
        reasons: list[str] = []
        if row["question_trigger_quote"] in PLACEHOLDERS:
            reasons.append("题干引文为禁止占位文本")
        if not locatable(row["question_trigger_quote"], text):
            reasons.append("题干引文无法在对应item_text定位")
        if not locatable(row["solution_step_quote"], text):
            reasons.append("解答引文无法在对应item_text定位")
        if row["adjacent_level_exclusion"] in GENERIC_EXCLUSIONS:
            reasons.append("相邻等级排除理由为通用句式")
        for reason in reasons:
            flags[reason] += 1
        if reasons:
            worklist.append({
                "item_id": row["item_id"], "dimension": row["dimension"], "item_text_path": row["item_text_path"],
                "question_location": row["question_location"], "solution_location": row["solution_location"],
                "question_trigger_quote": row["question_trigger_quote"], "solution_step_quote": row["solution_step_quote"],
                "adjacent_level_exclusion": row["adjacent_level_exclusion"], "rework_reason": "；".join(reasons),
                "required_action": "从对应item_text原文重新摘录可逐字定位的题干/解答引文；按该题任务重写相邻等级排除理由；复核后再判定是否仍为充分。",
            })
    output = resolve(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    fields = ["item_id", "dimension", "item_text_path", "question_location", "solution_location", "question_trigger_quote", "solution_step_quote", "adjacent_level_exclusion", "rework_reason", "required_action"]
    with output.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(worklist)
    qa_output = resolve(args.qa_output)
    with qa_output.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["check_item", "observed", "expected", "status"], lineterminator="\n")
        writer.writeheader()
        writer.writerow({"check_item": "需返工的唯一记录", "observed": len(worklist), "expected": "0", "status": "通过" if not worklist else "不通过"})
        for reason in ("题干引文为禁止占位文本", "题干引文无法在对应item_text定位", "解答引文无法在对应item_text定位", "相邻等级排除理由为通用句式"):
            writer.writerow({"check_item": reason, "observed": flags[reason], "expected": "0", "status": "通过" if flags[reason] == 0 else "不通过"})
    print(f"V2返工清单：{len(worklist)}条；" + "；".join(f"{k}{v}" for k, v in flags.items()))


if __name__ == "__main__":
    main()
