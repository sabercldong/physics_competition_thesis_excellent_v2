import csv
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REVIEW_LOG = ROOT / "07_analysis/results/reviewed/preformal_review_log.csv"
TRIAGE = ROOT / "07_analysis/results/reviewed/batch10_preformal_review_triage.csv"
INTERNAL = ROOT / "07_analysis/data/internal_analysis_candidate_v0.csv"
OUT = ROOT / "07_analysis/results/reviewed"

BOUNDARY = "Codex内部复核建议；非正式裁决；不得写入论文结果"
P0_REVIEW = OUT / "p0_internal_review_log.csv"
P0_REVISION = OUT / "p0_internal_revision_suggestions.csv"
P0_OVERLAY = OUT / "p0_internal_candidate_overlay.csv"
P0_REPORT = OUT / "p0_internal_review_report.md"


def read_csv(path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path, rows, fieldnames):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def md_table(headers, rows):
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(h, "")) for h in headers) + " |")
    return "\n".join(lines)


def contains_any(text, terms):
    return any(term in text for term in terms)


def recommendation(row):
    risk = row["risk_categories"]
    dimension = row["dimension"]
    present = row["internal_present"]
    level = row["internal_level"]
    evidence = row["internal_evidence"]

    if "质疑创新保守复核" in risk and dimension == "质疑创新" and present == "是":
        strong_terms = ["设想", "如何测量", "模型构造", "解释性模型", "同时达到", "真实现象", "模型边界", "方案"]
        weak_terms = ["新观测", "反直觉", "构造定性", "现象解释迁移", "联系起来"]
        if contains_any(evidence, strong_terms):
            return (
                "暂保留-待题面校对",
                present,
                level,
                "证据句含开放方案、模型构造、模型边界或显性条件讨论线索；但仍须对照原题确认是否由题干明确要求。",
                "补充题干原句或参考解答步骤，证明不是研究者外加的替代解法。",
            )
        if contains_any(evidence, weak_terms):
            return (
                "建议降级为待核实",
                present,
                level,
                "证据更接近陌生现象解释或类比迁移，尚不足以稳定触发质疑创新。",
                "对照题干是否要求处理假设、替代模型、模型失效或开放方案；若没有，建议改为未出现。",
            )
        return (
            "建议待核实",
            present,
            level,
            "当前证据不足以区分质疑创新与常规模型建构/科学推理。",
            "补充题干明确要求，证据不足时改为未出现。",
        )

    if "证据文本薄弱" in risk:
        if len(evidence) < 18:
            return (
                "建议修订证据",
                present,
                level,
                "证据句过短，难以支持复核。",
                "补充题干条件、关键公式、参考解答步骤或相邻等级区别。",
            )
        if present == "否" and contains_any(evidence, ["未要求", "只要求", "主要是", "属于既定"]):
            return (
                "暂保留-补强证据",
                present,
                level,
                "否定性证据方向清楚，但需要补足排除依据。",
                "补充不触发该维度的题干或解答依据。",
            )
        return (
            "建议修订证据",
            present,
            level,
            "当前证据能表达大意，但不足以作为正式编码证据。",
            "补充可定位到题干或参考解答的证据句。",
        )

    if "高等级边界" in risk:
        if level == "L4":
            return (
                "暂保留-待L4复核",
                present,
                level,
                "L4记录需要确认是否符合迁移、修正、一般化、递推、优化或开放构造。",
                "对照内部V2手册排除复杂计算误判。",
            )

    return (
        "待后续P1复核",
        present,
        level,
        "该记录不是P0核心问题。",
        "进入P1复核队列。",
    )


def build_p0_review():
    triage_rows = read_csv(TRIAGE)
    log_rows = {row["review_id"]: row for row in read_csv(REVIEW_LOG)}
    p0_ids = [row["review_id"] for row in triage_rows if row["priority"] == "P0"]

    out_rows = []
    revisions = []
    for review_id in p0_ids:
        row = log_rows[review_id]
        decision, proposed_present, proposed_level, reason, action = recommendation(row)
        out = dict(row)
        out.update(
            {
                "text_formula_figure_checked": "未完成-内部建议阶段",
                "v2_boundary_checked": "已按内部V2作初步建议",
                "proposed_present": proposed_present,
                "proposed_level": proposed_level,
                "proposed_evidence": "",
                "revision_decision": decision,
                "revision_reason": reason,
                "unresolved_issue": action,
                "reviewer": "Codex-internal",
                "review_date": "2026-07-14",
                "review_status": "内部建议完成-待正式复核",
                "review_boundary": BOUNDARY,
            }
        )
        out_rows.append(out)
        revisions.append(
            {
                "review_id": review_id,
                "item_id": row["item_id"],
                "dimension": row["dimension"],
                "internal_present": row["internal_present"],
                "internal_level": row["internal_level"],
                "suggested_decision": decision,
                "suggested_present": proposed_present,
                "suggested_level": proposed_level,
                "reason": reason,
                "required_evidence_action": action,
                "boundary": BOUNDARY,
            }
        )

    write_csv(P0_REVIEW, out_rows, list(out_rows[0]))
    write_csv(P0_REVISION, revisions, list(revisions[0]))
    return out_rows, revisions


def build_overlay(revisions):
    data_rows = read_csv(INTERNAL)
    revision_map = {(row["item_id"], row["dimension"]): row for row in revisions}
    overlay = []
    for row in data_rows:
        out = dict(row)
        revision = revision_map.get((row["item_id"], row["dimension"]))
        if revision:
            out["p0_review_status"] = "P0内部建议完成"
            out["p0_suggested_decision"] = revision["suggested_decision"]
            out["p0_suggested_present"] = revision["suggested_present"]
            out["p0_suggested_level"] = revision["suggested_level"]
            out["p0_required_action"] = revision["required_evidence_action"]
        else:
            out["p0_review_status"] = "非P0或待后续复核"
            out["p0_suggested_decision"] = ""
            out["p0_suggested_present"] = ""
            out["p0_suggested_level"] = ""
            out["p0_required_action"] = ""
        out["p0_boundary"] = BOUNDARY
        overlay.append(out)
    write_csv(P0_OVERLAY, overlay, list(overlay[0]))
    return overlay


def build_secondary_outputs(review_rows, revisions, overlay):
    decision_counts = Counter(row["suggested_decision"] for row in revisions)
    dimension_counts = Counter(row["dimension"] for row in revisions)
    item_counts = Counter(row["item_id"] for row in revisions)
    p0_items = sorted(item_counts)

    evidence_actions = []
    for row in revisions:
        if "证据" in row["suggested_decision"] or "补充" in row["required_evidence_action"]:
            evidence_actions.append(
                {
                    "review_id": row["review_id"],
                    "item_id": row["item_id"],
                    "dimension": row["dimension"],
                    "evidence_action": row["required_evidence_action"],
                    "boundary": BOUNDARY,
                }
            )
    write_csv(OUT / "p0_evidence_strengthening_checklist.csv", evidence_actions, list(evidence_actions[0]))

    impact_rows = []
    for dim in sorted(dimension_counts):
        internal_yes = sum(1 for row in revisions if row["dimension"] == dim and row["internal_present"] == "是")
        wait_or_downgrade = sum(
            1
            for row in revisions
            if row["dimension"] == dim and row["suggested_decision"] in {"建议待核实", "建议降级为待核实"}
        )
        impact_rows.append(
            {
                "dimension": dim,
                "p0_records": dimension_counts[dim],
                "internal_present_yes": internal_yes,
                "wait_or_downgrade_suggestions": wait_or_downgrade,
                "impact_boundary": "仅为P0内部建议影响预演，不改变正式结果",
            }
        )
    write_csv(OUT / "p0_internal_impact_preview.csv", impact_rows, list(impact_rows[0]))

    item_summary = []
    for item_id in p0_items:
        item_rows = [row for row in revisions if row["item_id"] == item_id]
        item_summary.append(
            {
                "item_id": item_id,
                "p0_records": len(item_rows),
                "dimensions": "；".join(sorted({row["dimension"] for row in item_rows})),
                "suggested_decisions": "；".join(sorted({row["suggested_decision"] for row in item_rows})),
                "boundary": BOUNDARY,
            }
        )
    write_csv(OUT / "p0_item_review_summary.csv", item_summary, list(item_summary[0]))

    p1_plan = [
        {
            "next_task": "P1-L4复核",
            "scope": "非P0中的L4和高等级边界记录",
            "priority": "P1",
            "action": "排除复杂计算误判，确认L4触发条件。",
        },
        {
            "next_task": "P1-人工校对联动",
            "scope": "P0/P1样本关联的OCR、公式、题图问题",
            "priority": "P1",
            "action": "对照原始PDF销项，不直接改正式编码。",
        },
        {
            "next_task": "P1-证据句补强",
            "scope": "非P0但中等把握度记录",
            "priority": "P1",
            "action": "补充题干或参考解答证据。",
        },
    ]
    write_csv(OUT / "p0_next_p1_review_plan.csv", p1_plan, list(p1_plan[0]))

    task_rows = [
        ("G4-00U1", "抽取P0复核子集", "p0_internal_review_log.csv"),
        ("G4-00U2", "质疑创新内部建议", "p0_internal_revision_suggestions.csv"),
        ("G4-00U3", "证据薄弱内部建议", "p0_evidence_strengthening_checklist.csv"),
        ("G4-00U4", "P0建议版复核日志", "p0_internal_review_log.csv"),
        ("G4-00U5", "P0修订建议表", "p0_internal_revision_suggestions.csv"),
        ("G4-00U6", "P0覆盖候选表", "p0_internal_candidate_overlay.csv"),
        ("G4-00U7", "P0影响预演", "p0_internal_impact_preview.csv"),
        ("G4-00U8", "P0题目汇总", "p0_item_review_summary.csv"),
        ("G4-00U9", "下一轮P1计划", "p0_next_p1_review_plan.csv"),
        ("G4-00U10", "P0内部复核完成报告", "p0_internal_review_report.md"),
    ]
    task_table = [{"task_id": a, "task_name": b, "output": c, "status": "完成-内部建议"} for a, b, c in task_rows]
    decision_table = [{"suggested_decision": k, "count": v} for k, v in sorted(decision_counts.items())]
    dimension_table = [{"dimension": k, "p0_records": v} for k, v in sorted(dimension_counts.items())]
    content = f"""# P0内部复核与修订建议报告

更新时间：2026-07-14

## 性质声明

本报告只处理 `batch10_preformal_review_triage.csv` 中的 P0 记录，属于 Codex 内部复核建议。它不是正式校对、正式评分者复核、分歧裁决或论文结果。

## 完成的后续10项任务

{md_table(["task_id", "task_name", "output", "status"], task_table)}

## P0范围

- P0复核记录：{len(revisions)}
- 涉及分析单元：{len(p0_items)}
- P0覆盖维度数：{len(dimension_counts)}

## 建议类型汇总

{md_table(["suggested_decision", "count"], decision_table)}

## 维度汇总

{md_table(["dimension", "p0_records"], dimension_table)}

## 不能形成的结论

- 不得把 `p0_internal_review_log.csv` 当作正式复核完成；
- 不得把 `suggested_decision` 当作最终编码裁决；
- 不得覆盖 `internal_coding_v1.csv` 或正式编码表；
- 不得把质疑创新或L4比例写入论文结果。

## 下一步最小任务

执行 `G4-00V`：处理P1复核，优先覆盖非P0的L4边界记录和仍未补强的中等把握度记录。
"""
    P0_REPORT.write_text(content, encoding="utf-8")


def main():
    review_rows, revisions = build_p0_review()
    overlay = build_overlay(revisions)
    build_secondary_outputs(review_rows, revisions, overlay)
    print(f"p0_records={len(revisions)} p0_items={len(set(row['item_id'] for row in revisions))}")
    print(f"wrote {P0_REPORT}")


if __name__ == "__main__":
    main()
