#!/usr/bin/env python3
"""Validate the manuscript after applying the R01 state-reconciliation queue."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUTPUT_CSV = ROOT / "09_quality/r01_manuscript_state_reconciliation_qa_v1.csv"
OUTPUT_MD = ROOT / "09_quality/r01_manuscript_state_reconciliation_qa_v1.md"
CHECKS = [
    ("STATE-QA-01", "08_manuscript/01_introduction.md", "正式统计结果尚未形成", "absent", "旧的结果未形成表述已移除"),
    ("STATE-QA-02", "08_manuscript/01_introduction.md", "第2至第4个问题必须等待真实评分者编码", "absent", "研究问题已允许R01描述性回答"),
    ("STATE-QA-03", "08_manuscript/01_introduction.md", "876条当前编码—证据链", "present", "当前R01结果范围已明确"),
    ("STATE-QA-04", "08_manuscript/02_theory.md", "仍需真实评分者一致性和分歧裁决结果支持", "absent", "旧的编码未完成表述已移除"),
    ("STATE-QA-05", "08_manuscript/02_theory.md", "当前R01版本化编码、裁决与证据链已支持项目内描述性报告", "present", "理论章已保留项目内结果边界"),
    ("STATE-QA-06", "08_manuscript/03_methods.md", "154条正式编码前需人工校对的问题", "absent", "历史队列不再误写为编码前阻塞"),
    ("STATE-QA-07", "08_manuscript/03_methods.md", "尚未完成真实双评分者编码和正式分歧裁决", "absent", "方法章已更新为R01归档状态"),
    ("STATE-QA-08", "08_manuscript/03_methods.md", "第35届八道题的分值边界仍无正式来源", "present", "分值限制仍保留"),
    ("STATE-QA-09", "08_manuscript/01_introduction.md", "尚未完成原书全文阅读和关键页码摘录", "present", "SOLO全文缺口仍保留"),
    ("STATE-QA-10", "08_manuscript/01_introduction.md", "没有真实教师或课堂证据", "present", "教学效果限制仍保留"),
]


def main() -> None:
    rows = []
    for check_id, relative_path, phrase, expectation, note in CHECKS:
        text = (ROOT / relative_path).read_text(encoding="utf-8")
        count = text.count(phrase)
        passed = (count == 0) if expectation == "absent" else (count > 0)
        rows.append({
            "check_id": check_id,
            "file": relative_path,
            "expectation": "不得出现" if expectation == "absent" else "必须保留",
            "phrase": phrase,
            "match_count": count,
            "status": "通过" if passed else "不通过",
            "note": note,
        })
    with OUTPUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    failures = [row for row in rows if row["status"] != "通过"]
    OUTPUT_MD.write_text(
        "# G8-04-R01-STATE-RECONCILIATION：修订后 QA（V1）\n\n"
        f"本检查共 {len(rows)} 项，{'全部通过' if not failures else f'{len(failures)} 项不通过'}。"
        "它仅验证状态措辞与既有R01结果资格边界的一致性，不替代R01结果资格QA、文献全文核验或学校格式检查。\n\n"
        "## 保留边界\n\n"
        "SOLO全文、教师或课堂真实证据、第35届正式分值来源仍未闭合。R01结果仍限定为项目内、可追溯、可复算的描述性编码结果。\n",
        encoding="utf-8",
    )
    if failures:
        raise SystemExit("状态对账QA失败：" + ", ".join(row["check_id"] for row in failures))
    print(f"状态对账QA：{len(rows)}/{len(rows)}通过。")


if __name__ == "__main__":
    main()
