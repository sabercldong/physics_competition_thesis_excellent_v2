#!/usr/bin/env python3
"""Screen the corrected coding table for high-risk boundary conflicts.

The output is a review queue, not an automatic recoding result. Lexical and
metadata cues only identify records that must be checked against the full item
and solution.
"""

from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CODING = ROOT / "07_analysis/data/final_coding_r01_correction_v1.csv"
EVIDENCE = ROOT / "07_analysis/data/final_coding_evidence_r01_v1.csv"
INDEX = ROOT / "03_corpus/item_index.csv"
OUTPUT = ROOT / "09_quality/正式编码边界冲突程序筛查_G8-63.csv"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def has_any(text: str, patterns: list[str]) -> bool:
    return any(re.search(pattern, text) for pattern in patterns)


def main() -> None:
    coding = read_rows(CODING)
    evidence = {
        (row["item_id"], row["dimension"]): row
        for row in read_rows(EVIDENCE)
    }
    index = {row["item_id"]: row for row in read_rows(INDEX)}

    innovation_positive_cues = [
        r"设计", r"提出", r"构造", r"改进", r"修正", r"替代",
        r"质疑", r"失效", r"推广", r"一般化", r"开放", r"另一种方案",
        r"改变.{0,8}条件", r"评价.{0,8}假设",
    ]
    model_organization_cues = [
        r"建模", r"模型", r"建立.{0,8}方程", r"写出.{0,8}方程",
        r"受力图", r"参考系", r"状态分类", r"递推", r"分阶段",
        r"平衡条件", r"稳定性", r"参数区间", r"临界条件",
    ]
    reasoning_integration_cues = [
        r"多步", r"递推", r"分阶段", r"临界", r"方程组", r"微分",
        r"积分", r"优化", r"极值", r"分情形", r"状态分类", r"稳定性",
        r"多对象", r"约束联立",
    ]
    argument_positive_cues = [
        r"说明.{0,10}理由", r"证明", r"检验", r"比较", r"讨论",
        r"稳定性", r"误差", r"边界", r"适用", r"能否", r"为什么",
    ]

    flagged: list[dict[str, str]] = []
    for row in coding:
        item_id = row["item_id"]
        dimension = row["dimension"]
        item = index[item_id]
        ev = evidence.get((item_id, dimension), {})
        question = ev.get("question_quote", "")
        solution = ev.get("solution_quote", "")
        metadata = "；".join(
            [
                item.get("knowledge_secondary", ""),
                item.get("representation", ""),
                item.get("math_tools", ""),
                item.get("answer_structure", ""),
            ]
        )
        combined = "；".join([question, solution, metadata])

        reasons: list[str] = []
        priority = ""

        if dimension == "质疑创新" and row["present_label"] == "是":
            if row["level"] == "L4":
                reasons.append("质疑创新L4须逐条核对开放构造、模型修正或一般化证据")
                priority = "P0"
            if not has_any(question, innovation_positive_cues):
                reasons.append("题干摘记未检出质疑创新的强触发活动")
                priority = priority or "P1"

        if dimension == "模型建构" and row["present_label"] == "否":
            if has_any(combined, model_organization_cues):
                reasons.append("当前判为未出现，但题干/元数据含模型组织线索")
                priority = "P0"

        if dimension == "科学推理" and row["level"] == "L1":
            if has_any(metadata, reasoning_integration_cues):
                reasons.append("当前为L1，但答案结构元数据含多关系整合线索")
                priority = priority or "P1"

        if dimension == "科学论证" and row["present_label"] == "是":
            if not has_any(question, argument_positive_cues):
                reasons.append("题干摘记未检出理由、比较、检验或边界活动")
                priority = priority or "P2"

        if reasons:
            flagged.append(
                {
                    "priority": priority,
                    "item_id": item_id,
                    "dimension": dimension,
                    "current_present": row["present_label"],
                    "current_level": row["level"],
                    "question_quote": question,
                    "answer_structure": item.get("answer_structure", ""),
                    "flag_reason": "；".join(reasons),
                    "review_boundary": "程序筛查仅生成复审队列，不自动更改编码",
                }
            )

    priority_order = {"P0": 0, "P1": 1, "P2": 2}
    flagged.sort(
        key=lambda row: (
            priority_order[row["priority"]],
            row["item_id"],
            row["dimension"],
        )
    )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "priority",
        "item_id",
        "dimension",
        "current_present",
        "current_level",
        "question_quote",
        "answer_structure",
        "flag_reason",
        "review_boundary",
    ]
    with OUTPUT.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(flagged)

    counts = {priority: 0 for priority in priority_order}
    for row in flagged:
        counts[row["priority"]] += 1
    print(f"flagged={len(flagged)}")
    print(" ".join(f"{key}={counts[key]}" for key in ("P0", "P1", "P2")))
    print(OUTPUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
