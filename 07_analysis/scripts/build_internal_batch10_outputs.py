import csv
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "07_analysis/data/internal_coding_v1.csv"
ISSUES = ROOT / "07_analysis/results/reviewed/internal_coding_quality_issues.csv"
SAMPLE_ITEMS = ROOT / "07_analysis/results/reviewed/preformal_review_sample_items.csv"
SAMPLE_CODING = ROOT / "07_analysis/results/reviewed/preformal_review_coding_records.csv"
REVIEW_LOG = ROOT / "07_analysis/results/reviewed/preformal_review_log.csv"
OUT_DATA = ROOT / "07_analysis/data/internal_analysis_candidate_v0.csv"
OUT = ROOT / "07_analysis/results/reviewed"

DIMENSIONS = ["模型建构", "科学推理", "科学论证", "质疑创新"]
LEVEL_ORDER = ["L1", "L2", "L3", "L4"]
INTERNAL_STATUS = "内部预演；非正式结果；不得写入论文结论"


def read_csv(path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path, rows, fieldnames):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def pct(n, d):
    return f"{(n / d):.3f}" if d else "0.000"


def md_table(headers, rows):
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(h, "")) for h in headers) + " |")
    return "\n".join(lines)


def first_by_item(rows):
    meta = {}
    for row in rows:
        meta.setdefault(row["item_id"], row)
    return meta


def issues_by_item(issue_rows):
    by_item = defaultdict(list)
    global_rows = []
    for row in issue_rows:
        if row.get("item_id"):
            by_item[row["item_id"]].append(row)
        else:
            global_rows.append(row)
    return by_item, global_rows


def task1_review_triage(review_rows):
    triage = []
    for row in review_rows:
        risk = row["risk_categories"]
        if "质疑创新保守复核" in risk:
            priority = "P0"
            action = "先核对题干是否明确触发质疑创新，再判断是否保留该维度"
        elif "证据文本薄弱" in risk:
            priority = "P0"
            action = "先补足可回到题干或参考解答的证据句"
        elif "高等级边界" in risk:
            priority = "P1"
            action = "复核L4是否确有迁移、修正、一般化、递推、优化或开放构造"
        elif "题干OCR校对" in risk or "公式与特殊符号校对" in risk:
            priority = "P1"
            action = "先对照原始PDF销项文本、公式或题图问题"
        else:
            priority = "P2"
            action = "按内部手册复核存在性、等级和证据句"
        triage.append(
            {
                "review_id": row["review_id"],
                "item_id": row["item_id"],
                "dimension": row["dimension"],
                "priority": priority,
                "triage_action": action,
                "review_status": row["review_status"],
                "internal_boundary": INTERNAL_STATUS,
            }
        )
    write_csv(OUT / "batch10_preformal_review_triage.csv", triage, list(triage[0]))
    return triage


def task2_formal_readiness(issue_rows, global_issues):
    rows = [
        {
            "formal_task": "G4-01 双人独立编码",
            "current_status": "阻塞",
            "blocking_reason": "尚无两名真实评分者独立填写的正式编码表；当前仅有Codex内部试编码。",
            "prepared_artifact": "preformal_review_log.csv; pilot_coding_round1_template.csv",
            "next_action": "完成样本复核后再决定是否进入真实双评分者编码。",
        },
        {
            "formal_task": "G4-02 分歧裁决与日志",
            "current_status": "阻塞",
            "blocking_reason": "尚无真实双评分者分歧数据，不能裁决。",
            "prepared_artifact": "preformal_review_log.csv",
            "next_action": "真实双评分者完成后再生成分歧日志。",
        },
        {
            "formal_task": "G4-03 数据清洗与唯一分析表",
            "current_status": "内部候选已准备，正式版阻塞",
            "blocking_reason": "正式唯一表必须基于裁决后编码；当前只能生成内部候选表。",
            "prepared_artifact": "internal_analysis_candidate_v0.csv",
            "next_action": "完成正式编码与裁决后替换输入。",
        },
        {
            "formal_task": "G4-04 至 G4-08 分析与结果稳健性",
            "current_status": "内部预演已准备，正式版阻塞",
            "blocking_reason": "正式分析必须等待正式唯一分析表。",
            "prepared_artifact": "batch10_internal_*",
            "next_action": "保留为脚本和表格模板，不写入正式结果。",
        },
    ]
    if global_issues:
        rows.append(
            {
                "formal_task": "全局版本边界",
                "current_status": "高风险",
                "blocking_reason": "内部底稿源试编码来自coding_manual_v1，不能直接视为V2正式编码。",
                "prepared_artifact": "internal_coding_quality_report.md",
                "next_action": "按最终手册重新判读或生成修订日志。",
            }
        )
    write_csv(OUT / "batch10_formal_readiness_map.csv", rows, list(rows[0]))
    return rows


def task3_candidate_dataset(rows, issue_map):
    out_rows = []
    for row in rows:
        flags = sorted({issue["category"] for issue in issue_map.get(row["item_id"], [])})
        out = dict(row)
        out["formal_readiness"] = "不可作为正式结果"
        out["risk_flags"] = "；".join(flags)
        out["batch_version"] = "batch10_internal_v0"
        out["batch_status"] = INTERNAL_STATUS
        out_rows.append(out)
    write_csv(OUT_DATA, out_rows, list(out_rows[0]))
    return out_rows


def task4_overall(rows):
    total = len({row["item_id"] for row in rows})
    presence = []
    levels = []
    for dim in DIMENSIONS:
        dim_rows = [row for row in rows if row["dimension"] == dim]
        present_rows = [row for row in dim_rows if row["present"] == "是"]
        presence.append(
            {
                "dimension": dim,
                "items_present_internal": len({row["item_id"] for row in present_rows}),
                "total_items": total,
                "proportion_internal": pct(len({row["item_id"] for row in present_rows}), total),
                "status": INTERNAL_STATUS,
            }
        )
        level_counts = Counter(row["level"] for row in present_rows)
        for level in LEVEL_ORDER:
            levels.append(
                {
                    "dimension": dim,
                    "level": level,
                    "count_internal": level_counts[level],
                    "within_dimension_proportion_internal": pct(level_counts[level], sum(level_counts.values())),
                    "status": INTERNAL_STATUS,
                }
            )
    write_csv(OUT / "batch10_internal_overall_presence.csv", presence, list(presence[0]))
    write_csv(OUT / "batch10_internal_level_distribution.csv", levels, list(levels[0]))
    return presence, levels


def task5_cooccurrence(rows):
    present_by_item = defaultdict(set)
    for row in rows:
        if row["present"] == "是":
            present_by_item[row["item_id"]].add(row["dimension"])
    total = len(present_by_item)
    out = []
    for left, right in combinations(DIMENSIONS, 2):
        count = sum(1 for dims in present_by_item.values() if left in dims and right in dims)
        out.append(
            {
                "dimension_pair": f"{left}+{right}",
                "items_present_together_internal": count,
                "total_items": total,
                "proportion_internal": pct(count, total),
                "status": INTERNAL_STATUS,
            }
        )
    write_csv(OUT / "batch10_internal_cooccurrence.csv", out, list(out[0]))
    return out


def grouped_presence(rows, group_field):
    totals = defaultdict(set)
    present = defaultdict(set)
    for row in rows:
        group = row[group_field] or "未标注"
        totals[group].add(row["item_id"])
        if row["present"] == "是":
            present[(group, row["dimension"])].add(row["item_id"])
    out = []
    for group in sorted(totals):
        for dim in DIMENSIONS:
            count = len(present[(group, dim)])
            total = len(totals[group])
            out.append(
                {
                    "group_field": group_field,
                    "group_value": group,
                    "dimension": dim,
                    "items_present_internal": count,
                    "total_items": total,
                    "proportion_internal": pct(count, total),
                    "status": INTERNAL_STATUS,
                }
            )
    return out


def task6_group_comparisons(rows):
    all_rows = []
    for field in ["competition_no", "knowledge_primary", "context_authenticity", "answer_structure"]:
        all_rows.extend(grouped_presence(rows, field))
    write_csv(OUT / "batch10_internal_group_comparisons.csv", all_rows, list(all_rows[0]))
    return all_rows


def task7_case_candidates(rows, issue_map):
    by_item = defaultdict(list)
    meta = first_by_item(rows)
    for row in rows:
        by_item[row["item_id"]].append(row)
    candidates = []
    for item_id, item_rows in by_item.items():
        issue_categories = Counter(issue["category"] for issue in issue_map.get(item_id, []))
        present_dims = [row["dimension"] for row in item_rows if row["present"] == "是"]
        l4_dims = [row["dimension"] for row in item_rows if row["level"] == "L4"]
        score = len(present_dims) * 5 + len(l4_dims) * 20
        score += issue_categories.get("质疑创新保守复核", 0) * 80
        score += issue_categories.get("证据文本薄弱", 0) * 25
        score += issue_categories.get("高等级边界", 0) * 15
        candidates.append(
            {
                "item_id": item_id,
                "competition_no": meta[item_id]["competition_no"],
                "year": meta[item_id]["year"],
                "question_no": meta[item_id]["question_no"],
                "subquestion_no": meta[item_id]["subquestion_no"],
                "knowledge_primary": meta[item_id]["knowledge_primary"],
                "present_dimensions_internal": "；".join(present_dims),
                "l4_dimensions_internal": "；".join(l4_dims),
                "case_candidate_score": score,
                "candidate_use": "典型案例候选；须先人工校对与复核",
                "status": INTERNAL_STATUS,
            }
        )
    top = sorted(candidates, key=lambda r: (-int(r["case_candidate_score"]), int(r["competition_no"]), r["item_id"]))[:30]
    write_csv(OUT / "batch10_typical_case_candidates.csv", top, list(top[0]))
    return top


def task8_boundary_memo(overall, cooccurrence, issue_rows, sample_rows):
    issue_counts = Counter(row["category"] for row in issue_rows)
    content = f"""# 内部结果稳健性与边界说明

更新时间：2026-07-14

## 性质声明

本文件只基于 Codex 内部试编码和内部质量检查生成，用于判断后续正式编码前的风险。它不是正式结果稳健性检验，不提供论文结论。

## 当前内部预演最主要的边界

- 源编码版本：内部分析表整理自 `coding_manual_v1` 试编码，虽已标注 `coding_manual_v2_internal`，但尚未按V2逐条重新判读；
- 人工校对：质量清单显示所有219个分析单元都有关联的文本、公式、OCR、题图或元数据待核风险；
- 样本复核：复核样本包覆盖74个分析单元，但 `preformal_review_log.csv` 仍全部为待复核；
- 正式评分：没有两名真实评分者的独立正式编码，也没有真实分歧裁决；
- 推断边界：八届样本可做描述性比较预演，不适合夸大为长期规律或因果结论。

## 内部风险计数

{md_table(["category", "count"], [{"category": k, "count": v} for k, v in sorted(issue_counts.items(), key=lambda x: (-x[1], x[0]))])}

## 后续进入正式结果前的最低条件

1. 样本包复核记录不再为空；
2. 高风险人工校对项至少有处理说明；
3. L4和质疑创新记录完成保守复核；
4. 形成裁决后的唯一分析表；
5. 所有正式表格由脚本从唯一分析表重现。
"""
    (OUT / "batch10_internal_boundary_memo.md").write_text(content, encoding="utf-8")


def task9_teaching_seed(rows, cases):
    dimension_guides = {
        "模型建构": ("模型边界与假设显化", "让学生先写研究对象、边界条件、可忽略因素和模型适用条件"),
        "科学推理": ("多规律约束链", "要求学生用箭头链或方程组说明条件如何推出结论"),
        "科学论证": ("比较与检验", "加入临界情形、量纲、极限、反例或误差阶检查"),
        "质疑创新": ("假设修正与替代方案", "只在题目确有开放或假设处理要求时设计替代模型讨论"),
    }
    rows_out = []
    for dim, (focus, seed) in dimension_guides.items():
        example_items = [case["item_id"] for case in cases if dim in case["present_dimensions_internal"]][:5]
        rows_out.append(
            {
                "dimension": dim,
                "teaching_focus_seed": focus,
                "task_design_seed": seed,
                "candidate_items": "；".join(example_items),
                "evidence_boundary": "内部预演；需正式编码和真实教学材料支持后才能写入论文",
            }
        )
    write_csv(OUT / "batch10_teaching_transfer_seed_matrix.csv", rows_out, list(rows_out[0]))
    return rows_out


def task10_report(outputs):
    tasks = [
        ("G4-00T1", "复核分流清单", "batch10_preformal_review_triage.csv"),
        ("G4-00T2", "正式任务阻塞与准备图", "batch10_formal_readiness_map.csv"),
        ("G4-00T3", "内部分析候选表", "internal_analysis_candidate_v0.csv"),
        ("G4-00T4", "总体分布预演", "batch10_internal_overall_presence.csv; batch10_internal_level_distribution.csv"),
        ("G4-00T5", "维度共现预演", "batch10_internal_cooccurrence.csv"),
        ("G4-00T6", "分组比较预演", "batch10_internal_group_comparisons.csv"),
        ("G4-00T7", "典型案例候选", "batch10_typical_case_candidates.csv"),
        ("G4-00T8", "边界与稳健性说明", "batch10_internal_boundary_memo.md"),
        ("G4-00T9", "教学转化种子矩阵", "batch10_teaching_transfer_seed_matrix.csv"),
        ("G4-00T10", "10项完成报告", "batch10_completion_report.md"),
    ]
    task_rows = [{"task_id": t, "task_name": n, "output": o, "status": "完成-内部预演"} for t, n, o in tasks]
    content = f"""# 后续10项内部任务完成报告

更新时间：2026-07-14

## 性质声明

本批处理完成的是内部预演、复核准备和可复现分析模板，不是正式双人编码、正式分歧裁决、正式论文结果、真实教师证据或课堂验证。

## 完成清单

{md_table(["task_id", "task_name", "output", "status"], task_rows)}

## 关键数量

- 内部分析候选记录：{outputs["candidate_rows"]}
- 复核分流记录：{outputs["triage_rows"]}
- 典型案例候选：{outputs["case_rows"]}
- 教学转化种子：{outputs["teaching_rows"]}

## 正式任务仍未完成

- `G4-01` 双人独立编码：尚未完成真实双评分者独立编码；
- `G4-02` 分歧裁决与日志：尚无真实分歧可裁决；
- `G4-03` 正式唯一分析表：必须等待裁决后数据；
- `G5` 教师与课堂证据：尚无真实问卷、访谈、课堂记录或学生作品。

## 下一步最小任务

执行 `G4-00T-REVIEW`：逐条填写 `preformal_review_log.csv`，至少先处理 P0 样本，即质疑创新保守复核和证据文本薄弱记录。
"""
    (OUT / "batch10_completion_report.md").write_text(content, encoding="utf-8")


def main():
    rows = read_csv(DATA)
    issue_rows = read_csv(ISSUES)
    sample_rows = read_csv(SAMPLE_ITEMS)
    review_rows = read_csv(REVIEW_LOG)
    issue_map, global_issues = issues_by_item(issue_rows)

    triage = task1_review_triage(review_rows)
    task2_formal_readiness(issue_rows, global_issues)
    candidate = task3_candidate_dataset(rows, issue_map)
    overall, _levels = task4_overall(rows)
    cooccur = task5_cooccurrence(rows)
    task6_group_comparisons(rows)
    cases = task7_case_candidates(rows, issue_map)
    task8_boundary_memo(overall, cooccur, issue_rows, sample_rows)
    teaching = task9_teaching_seed(rows, cases)
    task10_report(
        {
            "candidate_rows": len(candidate),
            "triage_rows": len(triage),
            "case_rows": len(cases),
            "teaching_rows": len(teaching),
        }
    )
    print("completed internal batch10 outputs")
    print(f"candidate_rows={len(candidate)} triage_rows={len(triage)} case_rows={len(cases)} teaching_rows={len(teaching)}")


if __name__ == "__main__":
    main()
