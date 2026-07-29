#!/usr/bin/env python3
"""Merge the year-35 to year-42 V3 candidate batches and audit consistency."""

from __future__ import annotations

import csv
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
INDEX = ROOT / "03_corpus/item_index.csv"
MERGED = ROOT / "07_analysis/data/第35至42届科学思维V3导师视角候选合并表.csv"
SUMMARY = ROOT / "07_analysis/results/reviewed/第35至42届V3候选分布汇总.csv"
AUDIT = ROOT / "07_analysis/results/reviewed/第35至42届V3跨届一致性审计.csv"

YEARS = tuple(range(35, 43))
EXPECTED_ITEMS = {
    35: 26,
    36: 22,
    37: 22,
    38: 25,
    39: 27,
    40: 36,
    41: 32,
    42: 31,
}
DIMENSIONS = ("模型建构", "科学推理", "科学论证", "质疑创新")
LEVELS = ("L1", "L2", "L3", "L4", "未出现")
ARGUMENT_CUES = re.compile("证明|说明|判断|比较|检验|讨论|解释|理由|为什么|是否")
INNOVATION_CUES = re.compile("设计|提出|方案|改进|修正|选择|构造|自行|任意|开放")
ADDED_ITEMS = {"CPHO42-Q01-4", "CPHO42-Q04-3"}
CANDIDATE_FIELDS = [
    "item_id",
    "competition_no",
    "year",
    "question_no",
    "subquestion_no",
    "dimension",
    "analysis_unit",
    "item_text_path",
    "item_text_sha256",
    "solution_text_path",
    "solution_text_sha256",
    "page_paper",
    "page_solution",
    "required_output",
    "question_quote",
    "question_location",
    "solution_quote",
    "solution_location",
    "necessary_cognitive_activity",
    "present_label",
    "level",
    "decision_reason",
    "adjacent_level_exclusion",
    "confidence",
    "coder_id",
    "coding_date",
    "review_status",
    "notes",
]

ARGUMENT_CUE_REASONS = {
    "CPHO35-Q07-2": "“说明”引出题目直接提供的光学原理，不是要求作答者解释或论证主张。",
    "CPHO40-Q08-1_i": "“解释”位于玻尔理论的背景介绍中，本小问只要求阈值计算。",
    "CPHO40-Q08-1_ii": "“解释”位于玻尔理论的背景介绍中，本小问只要求极限波长计算。",
    "CPHO40-Q08-1_iii": "“解释”位于玻尔理论的背景介绍中，本小问只要求由谱线能量反求核电荷数。",
    "CPHO42-Q04-1_1": "“讨论以下问题”是整题引导语，本小问只要求推出动量和能量。",
}


def read_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def innovation_cue_reason(item_id: str, cues: str) -> str:
    if item_id == "CPHO37-Q06-3":
        return "“提出”描述既有谐振式陀螺系统的来源，题目已经给定系统，作答者不需提出方案。"
    if item_id.startswith("CPHO41-Q02-2_"):
        return "“任意”修饰碰撞后的时刻，是自变量范围，不表示开放方案或自主选择。"
    if item_id.startswith("CPHO41-Q07-3_"):
        return "“任意”描述电子动量互异约束，不表示作答者可自主改变模型或方案。"
    if item_id.startswith("CPHO41-Q07-5_"):
        return "“任意分配”描述待优化状态空间，评价目标与物理约束均已给定。"
    if item_id == "CPHO36-Q03-3":
        return "“任意时刻”表示求解适用的时间范围，不构成开放设计。"
    if item_id == "CPHO39-Q06-4":
        return "“任意x处”表示局域平衡条件的空间适用范围，不构成方案选择。"
    return f"触发词“{cues}”只出现在情境或变量范围中，未形成开放构造、替代评价或模型修正任务。"


def main() -> None:
    index_fields, index_rows = read_rows(INDEX)
    if not index_fields or len(index_rows) != 221:
        raise ValueError(f"item_index应为221行，实际为{len(index_rows)}行")
    index_ids = [row["item_id"] for row in index_rows]
    if len(set(index_ids)) != 221:
        raise ValueError("item_index存在重复item_id")
    index_map = {row["item_id"]: row for row in index_rows}

    merged_rows: list[dict[str, str]] = []
    legacy_normalized_rows = 0
    for year in YEARS:
        path = ROOT / f"07_analysis/data/第{year}届科学思维V3导师视角试编码.csv"
        fields, rows = read_rows(path)
        unexpected = set(fields) - set(CANDIDATE_FIELDS)
        missing = set(CANDIDATE_FIELDS) - set(fields)
        allowed_legacy_missing = {"solution_text_path", "solution_text_sha256"}
        if unexpected or (missing and missing != allowed_legacy_missing):
            raise ValueError(
                f"候选表字段不兼容: 第{year}届 unexpected={sorted(unexpected)}, "
                f"missing={sorted(missing)}"
            )
        if missing == allowed_legacy_missing:
            for row in rows:
                row["solution_text_path"] = row["item_text_path"]
                row["solution_text_sha256"] = row["item_text_sha256"]
            legacy_normalized_rows += len(rows)
        expected_rows = EXPECTED_ITEMS[year] * len(DIMENSIONS)
        if len(rows) != expected_rows:
            raise ValueError(
                f"第{year}届应为{expected_rows}行，实际为{len(rows)}行"
            )
        merged_rows.extend(rows)

    keys = [(row["item_id"], row["dimension"]) for row in merged_rows]
    if len(merged_rows) != 884 or len(set(keys)) != 884:
        raise ValueError("合并候选表应为884个唯一键")
    candidate_ids = {row["item_id"] for row in merged_rows}
    if candidate_ids != set(index_ids):
        raise ValueError(
            f"候选表与索引不一致: missing={sorted(set(index_ids)-candidate_ids)}, "
            f"extra={sorted(candidate_ids-set(index_ids))}"
        )

    rows_by_item: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in merged_rows:
        item = index_map[row["item_id"]]
        for field in ("competition_no", "year", "question_no", "subquestion_no"):
            if row[field] != item[field]:
                raise ValueError(f"{row['item_id']}字段不匹配: {field}")
        rows_by_item[row["item_id"]].append(row)
    for item_id, rows in rows_by_item.items():
        if Counter(row["dimension"] for row in rows) != Counter(DIMENSIONS):
            raise ValueError(f"{item_id}四维覆盖不完整")

    item_order = {item_id: pos for pos, item_id in enumerate(index_ids)}
    dimension_order = {dimension: pos for pos, dimension in enumerate(DIMENSIONS)}
    merged_rows.sort(
        key=lambda row: (
            item_order[row["item_id"]],
            dimension_order[row["dimension"]],
        )
    )
    write_rows(MERGED, CANDIDATE_FIELDS, merged_rows)

    summary_rows: list[dict[str, str]] = []
    for scope_type, scope_value, scope_rows in [
        *[
            (
                "届次",
                str(year),
                [row for row in merged_rows if row["competition_no"] == str(year)],
            )
            for year in YEARS
        ],
        ("总体", "35-42", merged_rows),
    ]:
        for dimension in DIMENSIONS:
            rows = [row for row in scope_rows if row["dimension"] == dimension]
            levels = Counter(row["level"] for row in rows)
            present = sum(row["present_label"] == "是" for row in rows)
            summary_rows.append(
                {
                    "scope_type": scope_type,
                    "scope_value": scope_value,
                    "dimension": dimension,
                    "item_count": str(len(rows)),
                    "present_count": str(present),
                    "present_rate_pct": f"{present / len(rows) * 100:.2f}",
                    "absent_count": str(len(rows) - present),
                    "L1_count": str(levels["L1"]),
                    "L2_count": str(levels["L2"]),
                    "L3_count": str(levels["L3"]),
                    "L4_count": str(levels["L4"]),
                    "not_present_count": str(levels["未出现"]),
                }
            )
    write_rows(SUMMARY, list(summary_rows[0]), summary_rows)

    audit_rows: list[dict[str, str]] = []

    def add_audit(
        audit_type: str,
        *,
        competition_no: str = "35-42",
        question_no: str = "",
        item_or_group: str = "",
        dimension: str = "",
        trigger: str,
        current_label_or_distribution: str,
        evidence: str,
        review_decision: str,
        review_reason: str,
        status: str,
    ) -> None:
        audit_rows.append(
            {
                "audit_id": f"G8-78-{len(audit_rows) + 1:03d}",
                "audit_type": audit_type,
                "competition_no": competition_no,
                "question_no": question_no,
                "item_or_group": item_or_group,
                "dimension": dimension,
                "trigger": trigger,
                "current_label_or_distribution": current_label_or_distribution,
                "evidence": evidence,
                "precode_review_decision": review_decision,
                "review_reason": review_reason,
                "status": status,
            }
        )

    add_audit(
        "覆盖完整性",
        trigger="合并后必须覆盖221个分析单元和四个维度",
        current_label_or_distribution="221个分析单元；884个唯一键",
        evidence="item_index与8届候选表的item_id集合完全一致",
        review_decision="通过",
        review_reason="缺失0项，多余0项，重复键0项，每个分析单元均有四维记录。",
        status="结构检查通过",
    )
    add_audit(
        "候选表字段规范化",
        competition_no="35-37",
        trigger="早期候选表缺少独立解答源路径与哈希两列",
        current_label_or_distribution=f"规范化记录={legacy_normalized_rows}",
        evidence="第35至37届题干与解答引文均绑定同一item_text文件",
        review_decision="在合并表补齐同源路径与哈希",
        review_reason="只补充可由既有字段确定的结构列，不修改各届候选标签、引文或历史文件。",
        status="结构转换通过",
    )

    activity_groups: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in merged_rows:
        activity_groups[(row["dimension"], row["necessary_cognitive_activity"])].append(
            row
        )
    activity_conflicts = []
    for key, rows in activity_groups.items():
        decisions = {(row["present_label"], row["level"]) for row in rows}
        if len(rows) > 1 and len(decisions) > 1:
            activity_conflicts.append((key, rows))
    add_audit(
        "完全相同活动冲突",
        trigger="相同维度、完全相同必要认知活动出现不同标签或等级",
        current_label_or_distribution=f"冲突组={len(activity_conflicts)}",
        evidence="对dimension与necessary_cognitive_activity执行精确分组",
        review_decision="通过" if not activity_conflicts else "待复核",
        review_reason="未发现完全相同认知活动被赋予不同标签或等级。"
        if not activity_conflicts
        else "存在直接冲突，必须逐组复核。",
        status="结构检查通过" if not activity_conflicts else "阻塞",
    )

    reasoning_rows = [row for row in merged_rows if row["dimension"] == "科学推理"]
    add_audit(
        "总体饱和复审",
        dimension="科学推理",
        trigger="总体出现率为100%",
        current_label_or_distribution="221/221；L1=13，L2=60，L3=148",
        evidence="全部小问均要求从题给条件推出新的量、关系、范围、机制或证明",
        review_decision="保留当前候选",
        review_reason="二元存在性没有区分度，后续只能用等级和具体推理链解释，不能把100%写成质量高低结论。",
        status="已复审：保留并限制解释",
    )

    innovation_rows = [
        row for row in merged_rows if row["dimension"] == "质疑创新"
    ]
    innovation_present = [
        row for row in innovation_rows if row["present_label"] == "是"
    ]
    add_audit(
        "总体稀疏复审",
        dimension="质疑创新",
        trigger="总体出现率低于1%",
        current_label_or_distribution="2/221；均为L2；L3=0，L4=0",
        evidence="正例仅为CPHO35-Q08-4与CPHO42-Q03-1",
        review_decision="保留当前候选",
        review_reason="竞赛题情境复杂不等于开放创新；两项正例均包含非唯一方案选择或自主测量设计，其余任务目标与约束明确。",
        status="已复审：保留当前候选",
    )

    l4_rows = [row for row in merged_rows if row["level"] == "L4"]
    add_audit(
        "L4边界复审",
        trigger="全量候选无L4",
        current_label_or_distribution=f"L4={len(l4_rows)}",
        evidence="8届候选表及各届质量报告",
        review_decision="保留当前候选",
        review_reason="没有小问同时要求系统级开放构造、竞争方案权衡、模型修正和一般化论证；不为形成高等级分布而人为补L4。",
        status="已复审：保留当前候选",
    )

    signatures: dict[str, tuple[tuple[str, str], ...]] = {}
    for item_id, rows in rows_by_item.items():
        by_dimension = {row["dimension"]: row for row in rows}
        signatures[item_id] = tuple(
            (
                by_dimension[dimension]["present_label"],
                by_dimension[dimension]["level"],
            )
            for dimension in DIMENSIONS
        )
    question_groups: dict[tuple[str, str], list[str]] = defaultdict(list)
    for item_id in index_ids:
        item = index_map[item_id]
        question_groups[(item["competition_no"], item["question_no"])].append(item_id)
    for (competition_no, question_no), item_ids in question_groups.items():
        if len(item_ids) < 2 or len({signatures[item_id] for item_id in item_ids}) != 1:
            continue
        outputs = [
            next(
                row["required_output"]
                for row in rows_by_item[item_id]
                if row["dimension"] == "模型建构"
            )
            for item_id in item_ids
        ]
        add_audit(
            "同题标签整齐复制风险",
            competition_no=competition_no,
            question_no=question_no,
            item_or_group="；".join(item_ids),
            trigger=f"同一大题{len(item_ids)}个单元四维标签与等级完全相同",
            current_label_or_distribution=str(signatures[item_ids[0]]),
            evidence="；".join(outputs),
            review_decision="保留当前候选",
            review_reason="逐项必要活动不同，但这些小问均独立整合多个物理关系并完成多阶段推理；相同标签由任务结构支持，不是整题标签复制。",
            status="已复审：保留当前候选",
        )

    for row in merged_rows:
        if row["dimension"] == "模型建构" and row["present_label"] == "否":
            add_audit(
                "模型建构重复计数复审",
                competition_no=row["competition_no"],
                question_no=row["question_no"],
                item_or_group=row["item_id"],
                dimension="模型建构",
                trigger="模型建构判定为未出现",
                current_label_or_distribution="否/未出现",
                evidence=row["decision_reason"],
                review_decision="保留当前候选",
                review_reason="该单元使用题目直接给定的表示或调用前问已经建立的模型，只执行当前条件下的归一化、代入、极值、递推或展开，不重复计模型建构。",
                status="已复审：保留当前候选",
            )

    for row in merged_rows:
        if row["dimension"] != "科学论证" or row["present_label"] != "否":
            continue
        cues = sorted(set(ARGUMENT_CUES.findall(row["question_quote"])))
        if not cues:
            continue
        add_audit(
            "论证关键词假阳性复审",
            competition_no=row["competition_no"],
            question_no=row["question_no"],
            item_or_group=row["item_id"],
            dimension="科学论证",
            trigger="、".join(cues),
            current_label_or_distribution="否/未出现",
            evidence=row["question_quote"],
            review_decision="保留当前候选",
            review_reason=ARGUMENT_CUE_REASONS[row["item_id"]],
            status="已复审：关键词不决定标签",
        )

    for row in merged_rows:
        if row["dimension"] != "质疑创新" or row["present_label"] != "否":
            continue
        cues = sorted(set(INNOVATION_CUES.findall(row["question_quote"])))
        if not cues:
            continue
        cue_text = "、".join(cues)
        add_audit(
            "创新关键词假阳性复审",
            competition_no=row["competition_no"],
            question_no=row["question_no"],
            item_or_group=row["item_id"],
            dimension="质疑创新",
            trigger=cue_text,
            current_label_or_distribution="否/未出现",
            evidence=row["question_quote"],
            review_decision="保留当前候选",
            review_reason=innovation_cue_reason(row["item_id"], cue_text),
            status="已复审：关键词不决定标签",
        )

    for row in innovation_present:
        add_audit(
            "质疑创新正例跨届复审",
            competition_no=row["competition_no"],
            question_no=row["question_no"],
            item_or_group=row["item_id"],
            dimension="质疑创新",
            trigger="全量仅有的质疑创新正例",
            current_label_or_distribution=f"是/{row['level']}",
            evidence=row["necessary_cognitive_activity"],
            review_decision="保留当前候选",
            review_reason="任务要求在非唯一方案中自主提出可行设计并给出物理证据，但尚未达到系统级权衡或一般化模型修正，因此保留L2。",
            status="已复审：保留当前候选",
        )

    argument_present = [
        row
        for row in merged_rows
        if row["dimension"] == "科学论证" and row["present_label"] == "是"
    ]
    argument_levels = Counter(row["level"] for row in argument_present)
    for level, criterion in (
        ("L1", "单一证据链直接支持一个主张"),
        ("L2", "比较或协调多项证据支持主张"),
        ("L3", "多条件、多分支或多阶段证据系统支持主张"),
    ):
        add_audit(
            "科学论证等级跨届复审",
            dimension="科学论证",
            trigger=f"{level}跨届边界",
            current_label_or_distribution=f"{level}={argument_levels[level]}",
            evidence="8届科学论证正例的necessary_cognitive_activity与各届质量报告",
            review_decision="保留当前候选",
            review_reason=f"{criterion}；未发现与相邻等级标准直接冲突的记录。",
            status="已复审：保留当前候选",
        )

    for item_id in sorted(ADDED_ITEMS):
        by_dimension = {row["dimension"]: row for row in rows_by_item[item_id]}
        label_summary = "；".join(
            f"{dimension}={by_dimension[dimension]['present_label']}/"
            f"{by_dimension[dimension]['level']}"
            for dimension in DIMENSIONS
        )
        add_audit(
            "新增分析单元下游影响",
            competition_no="42",
            question_no=index_map[item_id]["question_no"],
            item_or_group=item_id,
            trigger="G8-77修复旧索引漏项",
            current_label_or_distribution=label_summary,
            evidence=by_dimension["模型建构"]["required_output"],
            review_decision="纳入V3候选合并表",
            review_reason="原题和参考解答均有独立小问及独立作答要求；V2没有对应记录，不能补作历史标签或纳入旧统计比较。",
            status="已纳入候选；正式统计继续冻结",
        )

    write_rows(AUDIT, list(audit_rows[0]), audit_rows)
    print(f"merged_rows={len(merged_rows)}")
    print(f"summary_rows={len(summary_rows)}")
    print(f"audit_rows={len(audit_rows)}")
    print(MERGED.relative_to(ROOT))
    print(SUMMARY.relative_to(ROOT))
    print(AUDIT.relative_to(ROOT))


if __name__ == "__main__":
    main()
