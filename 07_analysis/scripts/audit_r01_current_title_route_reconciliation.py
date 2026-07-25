#!/usr/bin/env python3
"""Audit the internal work title against current scope and format boundaries."""

from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TITLE = "中学生物理竞赛复赛试题的科学思维要求与教学转化研究"
FILES = {
    "frontmatter": ROOT / "08_manuscript/00_frontmatter.md",
    "abstract": ROOT / "08_manuscript/00_abstract_content_draft.md",
    "introduction": ROOT / "08_manuscript/01_introduction.md",
    "methods": ROOT / "08_manuscript/03_methods.md",
    "cases": ROOT / "08_manuscript/05_cases_and_diagnosis.md",
    "format_audit": ROOT / "09_quality/r01_ecnu_public_baseline_current_draft_audit_20260725.md",
}
OUTPUT_CSV = ROOT / "09_quality/r01_current_title_route_reconciliation_20260725.csv"
OUTPUT_MD = ROOT / "09_quality/r01_current_title_route_reconciliation_20260725.md"


def row(check_id: str, item: str, passed: bool, evidence: str, boundary: str) -> dict[str, str]:
    return {
        "check_id": check_id,
        "item": item,
        "result": "通过" if passed else "不通过",
        "evidence": evidence,
        "boundary_or_action": boundary,
    }


def main() -> None:
    text = {key: path.read_text(encoding="utf-8") for key, path in FILES.items()}
    han_count = len(re.findall(r"[\u4e00-\u9fff]", TITLE))
    checks = [
        row("TITLE-01", "公开基线长度", han_count == 25,
            f"内部候选题目汉字计数={han_count}。",
            "仅满足已登记的公开25字基线，仍需学院当期模板确认。"),
        row("TITLE-02", "当前工作题目登记", TITLE in text["frontmatter"],
            "题名页占位文件登记内部工作题目候选。",
            "必须保留“待导师确认”和非提交工作稿标记。"),
        row("TITLE-03", "研究对象一致性", "第35至42届全国中学生物理竞赛复赛试题" in text["abstract"]
            and "第35至42届全国中学生物理竞赛复赛试题" in text["methods"],
            "摘要和方法章均明确第35至42届全国中学生物理竞赛复赛试题语料。",
            "短题目不逐项列出届次；届次范围应由摘要、方法和封面副题说明。"),
        row("TITLE-04", "路线A边界一致性", "教学转化设计" in text["introduction"]
            and "教学效果" in text["introduction"]
            and "教学效果" in text["abstract"],
            "引言与摘要均把教学转化限定为设计建议，并排除效果结论。",
            "不得将“教学转化”改写为已验证教学策略或课堂效果。"),
        row("TITLE-05", "核心分析范围一致性", "模型建构、科学推理、科学论证和质疑创新" in text["methods"]
            and "任务认知要求" in text["methods"],
            "方法章登记四维任务认知要求分析。",
            "题目不直接承诺框架外部效度或学生能力结论。"),
        row("TITLE-06", "案例章限制一致性", "教学转化设计建议" in text["cases"],
            "第五章标题采用教学转化设计建议表述。",
            "真实教师/课堂证据缺失时，不升级为设计型研究题目。"),
        row("TITLE-07", "格式审计衔接", TITLE in text["format_audit"],
            "ECNU公开基线审计已记录相同的25字候选。",
            "该审计不构成学校、学院或导师批准。"),
    ]
    with OUTPUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(checks[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(checks)
    passed = sum(item["result"] == "通过" for item in checks)
    failures = [item["check_id"] for item in checks if item["result"] != "通过"]
    OUTPUT_MD.write_text(
        "# 当前题目与路线对账（2026-07-25）\n\n"
        "## 内部工作题目\n\n"
        f"**{TITLE}**\n\n"
        "该题目只作为非提交工作稿的内部候选。它对应路线A的稳健收缩版：第35至42届"
        "复赛试题的小问级内容分析、典型机制分析与教学转化设计。届次范围、四维框架、"
        "219个分析单元及876条当前编码记录应由摘要、方法和结果章交代，不以短题目承载。\n\n"
        "## 对账结果\n\n"
        f"{passed}/{len(checks)}项通过。"
        + (" 未通过：" + "、".join(failures) + "。\n" if failures else "\n")
        + "\n## 明确不代表\n\n"
        "本记录不代表导师、学院或学校确认题目；不把路线A升级为课堂设计型研究；"
        "不证明教学效果、学生能力、评分过程独立性或框架外部效度。最终题目仍须在"
        "`01_positioning/title_decision.md` 的确认记录中由作者或导师填写。\n",
        encoding="utf-8",
    )
    print(f"当前题目与路线对账：{passed}/{len(checks)}通过。")
    if failures:
        raise SystemExit("未通过：" + ", ".join(failures))


if __name__ == "__main__":
    main()
