import csv
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TRIAGE = ROOT / "07_analysis/results/reviewed/batch10_preformal_review_triage.csv"
REVIEW_LOG = ROOT / "07_analysis/results/reviewed/preformal_review_log.csv"
INTERNAL = ROOT / "07_analysis/data/internal_analysis_candidate_v0.csv"
MANUAL = ROOT / "07_analysis/results/reviewed/preformal_review_manual_issues.csv"
OUT = ROOT / "07_analysis/results/reviewed"

BOUNDARY = "Codex内部P1复核建议；非正式裁决；不得写入论文结果"


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


def split_items(value):
    return [part.strip() for part in value.split(";") if part.strip()]


def suggest(row):
    risk = row["risk_categories"]
    dim = row["dimension"]
    level = row["internal_level"]
    confidence = row["internal_confidence"]
    evidence = row["internal_evidence"]

    if "高等级边界" in risk and level == "L4":
        l4_terms = ["任意", "通项", "递推", "修正", "自生", "一般", "优化", "扰动", "三维", "梯度", "构造", "模型"]
        if any(term in evidence for term in l4_terms):
            return (
                "暂保留L4-待题面校对",
                "L4证据含递推、修正、一般化、扰动、三维建模或构造线索，但仍须对照原题排除复杂计算误判。",
                "补充题干或解答中触发L4的原始证据。",
            )
        return (
            "建议L4待核实",
            "当前证据不足以稳定区分L4与L3，存在复杂计算误判风险。",
            "复核是否只是多步骤计算；证据不足时建议降为L3或待核实。",
        )
    if "人工校对未销项" in risk or "元数据待核风险" in risk:
        return (
            "待文本公式图像校对",
            "记录关联人工校对未销项，正式复核前不能稳定裁决。",
            "先处理OCR、公式、题图或分值边界问题，再复核编码。",
        )
    if confidence == "中":
        return (
            "待评分者复核",
            "内部试编码把握度为中，需真实评分者或后续人工复核确认。",
            "补充相邻等级区别和可定位证据。",
        )
    return (
        "P1低风险暂缓",
        "当前不是P1核心高风险记录。",
        "进入后续批量一致性复核。",
    )


def main():
    triage = read_csv(TRIAGE)
    log = {row["review_id"]: row for row in read_csv(REVIEW_LOG)}
    p1_ids = [row["review_id"] for row in triage if row["priority"] == "P1"]
    manual_rows = read_csv(MANUAL)
    manual_by_item = defaultdict(list)
    for row in manual_rows:
        for item_id in split_items(row.get("selected_affected_item_ids", "")):
            manual_by_item[item_id].append(row)

    review_rows = []
    suggestions = []
    l4_rows = []
    manual_link_rows = []
    confidence_rows = []
    for review_id in p1_ids:
        row = log[review_id]
        decision, reason, action = suggest(row)
        out = dict(row)
        out.update(
            {
                "text_formula_figure_checked": "未完成-内部P1建议阶段",
                "v2_boundary_checked": "已按内部V2作P1初步建议",
                "proposed_present": row["internal_present"],
                "proposed_level": row["internal_level"],
                "proposed_evidence": "",
                "revision_decision": decision,
                "revision_reason": reason,
                "unresolved_issue": action,
                "reviewer": "Codex-internal",
                "review_date": "2026-07-14",
                "review_status": "P1内部建议完成-待正式复核",
                "review_boundary": BOUNDARY,
            }
        )
        review_rows.append(out)
        suggestion = {
            "review_id": review_id,
            "item_id": row["item_id"],
            "dimension": row["dimension"],
            "internal_present": row["internal_present"],
            "internal_level": row["internal_level"],
            "internal_confidence": row["internal_confidence"],
            "suggested_decision": decision,
            "reason": reason,
            "required_action": action,
            "boundary": BOUNDARY,
        }
        suggestions.append(suggestion)
        if "L4" == row["internal_level"] or "高等级边界" in row["risk_categories"]:
            l4_rows.append(suggestion)
        if row["internal_confidence"] == "中":
            confidence_rows.append(suggestion)
        for manual_issue in manual_by_item.get(row["item_id"], []):
            manual_link_rows.append(
                {
                    "review_id": review_id,
                    "item_id": row["item_id"],
                    "dimension": row["dimension"],
                    "issue_id": manual_issue["issue_id"],
                    "issue_type": manual_issue["issue_type"],
                    "severity": manual_issue["severity"],
                    "required_action": manual_issue["required_action"],
                    "boundary": BOUNDARY,
                }
            )

    write_csv(OUT / "p1_internal_review_log.csv", review_rows, list(review_rows[0]))
    write_csv(OUT / "p1_internal_revision_suggestions.csv", suggestions, list(suggestions[0]))
    write_csv(OUT / "p1_l4_boundary_checklist.csv", l4_rows, list(l4_rows[0]))
    write_csv(OUT / "p1_confidence_review_queue.csv", confidence_rows, list(confidence_rows[0]))
    write_csv(OUT / "p1_manual_issue_linkage.csv", manual_link_rows, list(manual_link_rows[0]))

    internal = read_csv(INTERNAL)
    suggestion_map = {(row["item_id"], row["dimension"]): row for row in suggestions}
    overlay = []
    for row in internal:
        out = dict(row)
        s = suggestion_map.get((row["item_id"], row["dimension"]))
        if s:
            out["p1_review_status"] = "P1内部建议完成"
            out["p1_suggested_decision"] = s["suggested_decision"]
            out["p1_required_action"] = s["required_action"]
        else:
            out["p1_review_status"] = "非P1或待后续复核"
            out["p1_suggested_decision"] = ""
            out["p1_required_action"] = ""
        out["p1_boundary"] = BOUNDARY
        overlay.append(out)
    write_csv(OUT / "p1_internal_candidate_overlay.csv", overlay, list(overlay[0]))

    decision_counts = Counter(row["suggested_decision"] for row in suggestions)
    dimension_counts = Counter(row["dimension"] for row in suggestions)
    item_counts = Counter(row["item_id"] for row in suggestions)
    impact = [
        {
            "dimension": dim,
            "p1_records": dimension_counts[dim],
            "l4_records": sum(1 for row in suggestions if row["dimension"] == dim and row["internal_level"] == "L4"),
            "manual_linked_records": sum(1 for row in suggestions if row["dimension"] == dim and row["item_id"] in manual_by_item),
            "boundary": "P1内部影响预演，不改变正式结果",
        }
        for dim in sorted(dimension_counts)
    ]
    write_csv(OUT / "p1_internal_impact_preview.csv", impact, list(impact[0]))

    item_summary = [
        {
            "item_id": item_id,
            "p1_records": count,
            "dimensions": "；".join(sorted({row["dimension"] for row in suggestions if row["item_id"] == item_id})),
            "decisions": "；".join(sorted({row["suggested_decision"] for row in suggestions if row["item_id"] == item_id})),
            "boundary": BOUNDARY,
        }
        for item_id, count in sorted(item_counts.items())
    ]
    write_csv(OUT / "p1_item_review_summary.csv", item_summary, list(item_summary[0]))

    gate = [
        {
            "gate": "进入正式编码前",
            "condition": "P0与P1建议均已人工确认或标记待核实",
            "current_status": "未满足",
            "next_action": "继续处理P2或直接开始真实评分者独立编码准备。",
        },
        {
            "gate": "进入正式结果表前",
            "condition": "有裁决后的唯一分析表",
            "current_status": "未满足",
            "next_action": "不能用内部overlay表替代正式结果。",
        },
    ]
    write_csv(OUT / "p1_next_gate_plan.csv", gate, list(gate[0]))

    task_rows = [
        ("G4-00V1", "抽取P1复核子集", "p1_internal_review_log.csv"),
        ("G4-00V2", "L4边界复核建议", "p1_l4_boundary_checklist.csv"),
        ("G4-00V3", "人工校对联动表", "p1_manual_issue_linkage.csv"),
        ("G4-00V4", "中等把握度复核队列", "p1_confidence_review_queue.csv"),
        ("G4-00V5", "P1建议版复核日志", "p1_internal_review_log.csv"),
        ("G4-00V6", "P1修订建议表", "p1_internal_revision_suggestions.csv"),
        ("G4-00V7", "P1覆盖候选表", "p1_internal_candidate_overlay.csv"),
        ("G4-00V8", "P1影响预演", "p1_internal_impact_preview.csv"),
        ("G4-00V9", "P1题目汇总与后续门槛", "p1_item_review_summary.csv; p1_next_gate_plan.csv"),
        ("G4-00V10", "P1内部复核完成报告", "p1_internal_review_report.md"),
    ]
    task_table = [{"task_id": a, "task_name": b, "output": c, "status": "完成-内部建议"} for a, b, c in task_rows]
    decision_table = [{"suggested_decision": k, "count": v} for k, v in sorted(decision_counts.items())]
    dimension_table = [{"dimension": k, "p1_records": v} for k, v in sorted(dimension_counts.items())]
    report = f"""# P1内部复核与修订建议报告

更新时间：2026-07-14

## 性质声明

本报告处理 `batch10_preformal_review_triage.csv` 中的P1记录，属于Codex内部复核建议。它不是正式校对、正式评分者复核、分歧裁决或论文结果。

## 完成的后续10项任务

{md_table(["task_id", "task_name", "output", "status"], task_table)}

## P1范围

- P1复核记录：{len(suggestions)}
- 涉及分析单元：{len(item_counts)}
- L4/高等级边界记录：{len(l4_rows)}
- 中等把握度记录：{len(confidence_rows)}
- 人工校对联动记录：{len(manual_link_rows)}

## 建议类型汇总

{md_table(["suggested_decision", "count"], decision_table)}

## 维度汇总

{md_table(["dimension", "p1_records"], dimension_table)}

## 不能形成的结论

- 不得把P1建议写成正式裁决；
- 不得覆盖正式编码表；
- 不得把L4比例、分组比较或案例候选写成论文结果；
- 所有关联人工校对项在销项前只能作为待核实风险。

## 下一步最小任务

执行 `G4-00W`：汇总P0/P1建议，生成正式编码前总门槛清单和真实评分者编码准备包。
"""
    (OUT / "p1_internal_review_report.md").write_text(report, encoding="utf-8")
    print(f"p1_records={len(suggestions)} p1_items={len(item_counts)} l4_rows={len(l4_rows)} manual_links={len(manual_link_rows)}")
    print("wrote p1_internal_review_report.md")


if __name__ == "__main__":
    main()
