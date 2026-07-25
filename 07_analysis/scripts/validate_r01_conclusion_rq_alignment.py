#!/usr/bin/env python3
"""Check that Chapter 6 answers the current research questions within evidence limits."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
INTRODUCTION = ROOT / "08_manuscript/01_introduction.md"
CONCLUSION = ROOT / "08_manuscript/06_conclusion.md"
OUTPUT_CSV = ROOT / "09_quality/r01_conclusion_rq_alignment_qa_v1.csv"
OUTPUT_MD = ROOT / "09_quality/r01_conclusion_rq_alignment_qa_v1.md"


def main() -> None:
    introduction = INTRODUCTION.read_text(encoding="utf-8")
    conclusion = CONCLUSION.read_text(encoding="utf-8")
    questions = [
        "如何构建适用于全国中学生物理竞赛复赛试题的科学思维认知要求分析框架",
        "第35至42届复赛试题在模型建构、科学推理、科学论证和质疑创新四个维度上呈现出怎样的任务要求",
        "这些试题在认知结构要求等级、维度组合和典型题设机制上有哪些特征",
        "不同知识模块、情境类型、表征形式和数学工具下，试题认知要求是否呈现可描述的差异",
        "如何将试题分析结果转化为竞赛教学中的任务、支架和评价设计",
    ]
    response_terms = [
        "第一，针对“如何构建分析框架”",
        "第二，针对“四维度呈现何种任务要求”",
        "第三，针对“等级、组合和典型机制有哪些特征”",
        "第四，针对“不同届次、知识模块、情境、表征和数学工具下是否存在可描述差异”",
        "第五，针对“如何转化为教学设计”",
    ]
    checks: list[tuple[str, str, str, str, bool]] = []
    for index, (question, response) in enumerate(zip(questions, response_terms), start=1):
        checks.append((
            f"CRQA-{index:02d}", f"研究问题{index}与结论回应", "存在", "存在" if question in introduction and response in conclusion else "缺失",
            question in introduction and response in conclusion,
        ))
    for index, value in enumerate(["219个分析单元", "876条R01当前编码记录", "科学推理出现于219个", "模型建构出现于203个", "科学论证出现于106个", "质疑创新出现于84个", "共同出现40次、并集为150个"], start=6):
        checks.append((f"CRQA-{index:02d}", "当前描述性结果", value, "存在" if value in conclusion else "缺失", value in conclusion))
    for index, value in enumerate(["不构成框架已获外部效度", "不进行显著性检验或分值加权", "不把它们写作跨届趋势", "不是学生困难诊断、教师共识、课堂可行性或教学效果证据"], start=13):
        checks.append((f"CRQA-{index:02d}", "结论边界", value, "存在" if value in conclusion else "缺失", value in conclusion))
    for index, value in enumerate([
        "它不意味着不同研究者必然得到完全相同的编码",
        "不是学生真实的思维过程，也不是唯一可能的合理解题路径",
        "并非经过独立验证的量表",
        "论文才可以把相应表述从“设计建议”或“项目内描述性结果”升级为更强的研究结论",
    ], start=17):
        checks.append((f"CRQA-{index:02d}", "新增结论边界与升级路径", value, "存在" if value in conclusion else "缺失", value in conclusion))
    with OUTPUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["check_id", "check_item", "expected", "actual", "status"])
        for check in checks:
            writer.writerow([*check[:4], "通过" if check[4] else "不通过"])
    failures = [check[0] for check in checks if not check[4]]
    OUTPUT_MD.write_text(
        "# R01结论章研究问题对齐QA（V1）\n\n"
        f"共完成{len(checks)}项检查，{'全部通过' if not failures else '不通过：' + '、'.join(failures)}。"
        "本QA只检查第一章当前研究问题与第六章的项目内对应，以及冻结结果和禁止外推边界是否被保留；"
        "不验证框架外部效度、评分过程、学生能力、教学效果、学校格式或人类参与者事实。\n",
        encoding="utf-8",
    )
    if failures:
        raise SystemExit("结论章研究问题对齐QA失败：" + ", ".join(failures))
    print(f"R01结论章研究问题对齐QA：{len(checks)}/{len(checks)}通过")


if __name__ == "__main__":
    main()
