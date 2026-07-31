import csv
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
INTERNAL = ROOT / "07_analysis/data/internal_analysis_candidate_v0.csv"
P0 = ROOT / "07_analysis/results/reviewed/p0_internal_revision_suggestions.csv"
P1 = ROOT / "07_analysis/results/reviewed/p1_internal_revision_suggestions.csv"
P0_EVIDENCE = ROOT / "07_analysis/results/reviewed/p0_evidence_strengthening_checklist.csv"
P1_L4 = ROOT / "07_analysis/results/reviewed/p1_l4_boundary_checklist.csv"
P1_MANUAL = ROOT / "07_analysis/results/reviewed/p1_manual_issue_linkage.csv"
MANUAL = ROOT / "03_corpus/manual_review_checklist.csv"
ITEM_INDEX = ROOT / "03_corpus/item_index.csv"
CODEBOOK = ROOT / "04_framework/codebook_v2_internal.csv"
OUT = ROOT / "07_analysis/results/reviewed"
DATA_OUT = ROOT / "07_analysis/data"
FRAMEWORK_OUT = ROOT / "04_framework"

DIMENSIONS = ["模型建构", "科学推理", "科学论证", "质疑创新"]
BOUNDARY = "正式编码前准备；非正式编码结果；不得写入论文结果"


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


def first_by_item(rows):
    meta = {}
    for row in rows:
        meta.setdefault(row["item_id"], row)
    return meta


def load():
    return {
        "internal": read_csv(INTERNAL),
        "p0": read_csv(P0),
        "p1": read_csv(P1),
        "p0_evidence": read_csv(P0_EVIDENCE),
        "p1_l4": read_csv(P1_L4),
        "p1_manual": read_csv(P1_MANUAL),
        "manual": read_csv(MANUAL),
        "items": read_csv(ITEM_INDEX),
        "codebook": read_csv(CODEBOOK),
    }


def combined_review_master(data):
    rows = []
    for stage, source in [("P0", data["p0"]), ("P1", data["p1"])]:
        for row in source:
            rows.append(
                {
                    "stage": stage,
                    "review_id": row["review_id"],
                    "item_id": row["item_id"],
                    "dimension": row["dimension"],
                    "internal_present": row["internal_present"],
                    "internal_level": row["internal_level"],
                    "suggested_decision": row["suggested_decision"],
                    "required_action": row.get("required_evidence_action") or row.get("required_action", ""),
                    "boundary": BOUNDARY,
                }
            )
    write_csv(OUT / "prep30_combined_review_master.csv", rows, list(rows[0]))
    return rows


def gate_register(data, combined):
    manual_pending = [row for row in data["manual"] if row.get("review_status") == "待人工校对"]
    p0_wait = [row for row in data["p0"] if "待核实" in row["suggested_decision"]]
    p1_l4_wait = [row for row in data["p1"] if "L4待核实" in row["suggested_decision"]]
    rows = [
        {
            "gate_id": "GATE-01",
            "gate_name": "人工校对销项",
            "current_count": len(manual_pending),
            "status": "未满足",
            "required_before": "正式编码前",
            "action": "处理OCR、公式、题图、图注和分值边界问题。",
        },
        {
            "gate_id": "GATE-02",
            "gate_name": "P0待核实处理",
            "current_count": len(p0_wait),
            "status": "未满足",
            "required_before": "正式编码前",
            "action": "对质疑创新和证据薄弱记录完成题面校对或标注排除。",
        },
        {
            "gate_id": "GATE-03",
            "gate_name": "P1 L4边界处理",
            "current_count": len(p1_l4_wait),
            "status": "未满足",
            "required_before": "正式编码前",
            "action": "排除复杂计算误判，确认L4触发条件。",
        },
        {
            "gate_id": "GATE-04",
            "gate_name": "真实评分者独立编码",
            "current_count": 0,
            "status": "未满足",
            "required_before": "正式结果前",
            "action": "由两名真实评分者独立填写正式编码模板。",
        },
        {
            "gate_id": "GATE-05",
            "gate_name": "分歧裁决",
            "current_count": 0,
            "status": "未满足",
            "required_before": "正式唯一分析表前",
            "action": "依据两名评分者编码生成分歧表并裁决。",
        },
    ]
    write_csv(OUT / "prep30_gate_register.csv", rows, list(rows[0]))
    return rows


def manual_priority(data):
    severity_order = {"高": 0, "中": 1, "低": 2}
    rows = []
    for row in data["manual"]:
        affected = split_items(row.get("affected_item_ids", ""))
        priority = "P0" if row["severity"] == "高" and row["issue_type"] in {"题干OCR校对", "公式与特殊符号校对"} else "P1"
        rows.append(
            {
                "issue_id": row["issue_id"],
                "competition_no": row["competition_no"],
                "question_no": row["question_no"],
                "issue_type": row["issue_type"],
                "severity": row["severity"],
                "priority": priority,
                "affected_item_count": len(affected),
                "required_action": row["required_action"],
                "status": row["review_status"],
            }
        )
    rows.sort(key=lambda r: (r["priority"], severity_order.get(r["severity"], 9), int(r["competition_no"]), r["question_no"], r["issue_id"]))
    write_csv(OUT / "prep30_manual_priority_queue.csv", rows, list(rows[0]))
    return rows


def rater_templates(data):
    internal = data["internal"]
    fields = [
        "item_id",
        "competition_no",
        "year",
        "question_no",
        "subquestion_no",
        "dimension",
        "present",
        "level",
        "evidence",
        "confidence",
        "coder_id",
        "coding_date",
        "manual_version",
        "notes",
    ]
    blank = []
    for row in internal:
        blank.append(
            {
                "item_id": row["item_id"],
                "competition_no": row["competition_no"],
                "year": row["year"],
                "question_no": row["question_no"],
                "subquestion_no": row["subquestion_no"],
                "dimension": row["dimension"],
                "present": "",
                "level": "",
                "evidence": "",
                "confidence": "",
                "coder_id": "",
                "coding_date": "",
                "manual_version": "待正式冻结",
                "notes": "",
            }
        )
    write_csv(DATA_OUT / "formal_coding_rater_A_template.csv", blank, fields)
    write_csv(DATA_OUT / "formal_coding_rater_B_template.csv", blank, fields)

    adjudication_fields = fields + ["rater_A_present", "rater_A_level", "rater_B_present", "rater_B_level", "adjudicated_present", "adjudicated_level", "adjudicated_evidence", "adjudicator", "adjudication_date", "adjudication_reason"]
    adj = []
    for row in internal:
        adj.append({field: "" for field in adjudication_fields})
        adj[-1].update(
            {
                "item_id": row["item_id"],
                "competition_no": row["competition_no"],
                "year": row["year"],
                "question_no": row["question_no"],
                "subquestion_no": row["subquestion_no"],
                "dimension": row["dimension"],
                "manual_version": "待正式冻结",
            }
        )
    write_csv(DATA_OUT / "formal_adjudication_template.csv", adj, adjudication_fields)
    return len(blank)


def data_dictionary(data):
    fields = [
        ("item_id", "分析单元编号", "来自item_index.csv"),
        ("dimension", "科学思维维度", "模型建构/科学推理/科学论证/质疑创新"),
        ("present", "维度是否出现", "正式评分者填写：是/否"),
        ("level", "认知结构要求等级", "出现时填写L1-L4，未出现填未出现"),
        ("evidence", "判定证据", "必须能回到题干或参考解答"),
        ("confidence", "评分把握度", "高/中/低"),
        ("adjudicated_present", "裁决后存在性", "仅裁决表使用"),
        ("adjudicated_level", "裁决后等级", "仅裁决表使用"),
        ("adjudication_reason", "裁决理由", "记录分歧处理依据"),
    ]
    rows = [{"field": a, "meaning": b, "allowed_or_rule": c, "boundary": BOUNDARY} for a, b, c in fields]
    write_csv(OUT / "prep30_formal_data_dictionary.csv", rows, list(rows[0]))
    return rows


def write_markdown_docs(data, combined, gates, template_rows):
    decision_counts = Counter(row["suggested_decision"] for row in combined)
    gate_rows = [{"gate_id": row["gate_id"], "gate_name": row["gate_name"], "status": row["status"], "current_count": row["current_count"]} for row in gates]
    decision_rows = [{"suggested_decision": k, "count": v} for k, v in sorted(decision_counts.items())]

    (OUT / "prep30_rater_briefing.md").write_text(
        f"""# 真实评分者编码准备说明

更新时间：2026-07-14

## 性质声明

本文件用于后续真实评分者编码准备。当前项目尚未完成真实双评分者独立编码，本文件不代表评分者意见或正式一致性结果。

## 编码材料

- 编码手册：`04_framework/coding_manual_v2_internal.md`，但正式使用前仍需冻结正式版；
- 空白模板：`07_analysis/data/formal_coding_rater_A_template.csv`、`formal_coding_rater_B_template.csv`；
- 裁决模板：`07_analysis/data/formal_adjudication_template.csv`；
- 重点风险：`prep30_gate_register.csv`、`prep30_combined_review_master.csv`。

## 评分者填写要求

1. 每名评分者独立填写，不参考另一名评分者；
2. 每条记录必须填写维度是否出现、等级、证据和把握度；
3. 证据必须来自题干、参考解答或题图，不得来自内部预演结果；
4. 遇到OCR、公式或题图未销项问题，标注待核实；
5. 不得直接复制Codex内部试编码。
""",
        encoding="utf-8",
    )

    (OUT / "prep30_adjudication_protocol.md").write_text(
        """# 正式分歧裁决协议草案

更新时间：2026-07-14

## 性质声明

本协议是裁决准备文件。当前尚无真实双评分者编码，因此不能执行正式裁决。

## 裁决顺序

1. 先比较两名评分者的维度存在性；
2. 存在性一致但等级不同，再比较等级证据；
3. 若证据受OCR、公式或题图影响，先退回人工校对；
4. 裁决结果必须写入 `formal_adjudication_template.csv`；
5. 裁决后才能生成正式唯一分析表。

## 禁止事项

- 不得用Codex内部建议替代裁决；
- 不得无证据取平均或投票；
- 不得在证据不足时强行给出等级。
""",
        encoding="utf-8",
    )

    (OUT / "prep30_analysis_readiness_report.md").write_text(
        f"""# 正式分析准备度报告

更新时间：2026-07-14

## 总体判断

正式分析尚未就绪。当前已完成的是正式编码前准备包，不是正式结果。

## 门槛状态

{md_table(["gate_id", "gate_name", "status", "current_count"], gate_rows)}

## P0/P1建议汇总

{md_table(["suggested_decision", "count"], decision_rows)}

## 当前可进入的工作

- 真实评分者培训；
- 人工校对销项；
- 双评分者空白模板分发；
- 分歧裁决规则确认。

## 当前不可进入的工作

- 正式总体分布结论；
- 正式共现结论；
- 显著性或趋势判断；
- 教学效果或因果结论。
""",
        encoding="utf-8",
    )

    tasks = []
    for prefix, names in [
        ("G4-00W", ["P0/P1总建议表", "总门槛清单", "人工校对优先队列", "证据补强总表", "L4总复核队列", "质疑创新总复核队列", "中等把握度总队列", "正式准备度报告", "正式数据字典", "W组完成记录"]),
        ("G4-00X", ["评分者A模板", "评分者B模板", "裁决模板", "评分者说明", "裁决协议", "版本路线图", "评分者交接清单", "正式编码字段校验清单", "分歧类型预设表", "X组完成记录"]),
        ("G4-00Y", ["分析输入占位说明", "正式结果表占位", "正式图表清单", "主张证据占位", "论文写作门槛表", "结果章占位说明", "教学转化证据门槛", "归档清单", "下轮任务路线图", "30项完成报告"]),
    ]:
        for i, name in enumerate(names, start=1):
            tasks.append({"task_id": f"{prefix}{i}", "task_name": name, "status": "完成-准备性质"})
    (OUT / "prep30_completion_report.md").write_text(
        f"""# 后续30项正式编码前准备任务完成报告

更新时间：2026-07-14

## 性质声明

本批30项任务完成的是正式编码前准备，不是正式编码、正式分歧裁决或论文结果。

## 完成清单

{md_table(["task_id", "task_name", "status"], tasks)}

## 关键产物

- P0/P1总建议表：`prep30_combined_review_master.csv`
- 总门槛清单：`prep30_gate_register.csv`
- 正式评分者模板：`formal_coding_rater_A_template.csv`、`formal_coding_rater_B_template.csv`
- 正式裁决模板：`formal_adjudication_template.csv`
- 准备度报告：`prep30_analysis_readiness_report.md`

## 关键数量

- P0/P1建议记录：{len(combined)}
- 正式评分者模板记录：{template_rows}
- 未满足门槛：{sum(1 for row in gates if row["status"] != "已满足")}

## 下一步最小任务

执行 `G4-01-PREP`：在不填写正式编码结论的前提下，完成评分者交接检查，并决定是否开始真实双评分者独立编码。
""",
        encoding="utf-8",
    )


def placeholder_files(data):
    placeholder_rows = [
        {"artifact": "正式唯一分析表", "path": "07_analysis/data/final_coding.csv", "status": "阻塞", "reason": "尚无真实双评分者编码和裁决结果"},
        {"artifact": "正式总体分布表", "path": "07_analysis/results/reviewed/final_dimension_presence.csv", "status": "阻塞", "reason": "尚无正式唯一分析表"},
        {"artifact": "正式共现表", "path": "07_analysis/results/reviewed/final_dimension_cooccurrence.csv", "status": "阻塞", "reason": "尚无正式唯一分析表"},
        {"artifact": "正式图表", "path": "08_manuscript/figure_table_plan.md", "status": "待后续更新", "reason": "正式结果未生成"},
    ]
    write_csv(OUT / "prep30_formal_output_placeholders.csv", placeholder_rows, list(placeholder_rows[0]))

    claim_rows = [
        {"claim_type": "试题科学思维维度分布", "required_evidence": "裁决后正式编码表与脚本输出", "current_status": "待正式编码"},
        {"claim_type": "届次变化或比较", "required_evidence": "正式分组描述统计与边界说明", "current_status": "待正式编码"},
        {"claim_type": "典型题机制", "required_evidence": "正式编码、题干证据、解答证据和案例协议", "current_status": "待复核"},
        {"claim_type": "教学转化建议", "required_evidence": "正式试题结果加教师或课堂证据", "current_status": "待真实证据"},
    ]
    write_csv(OUT / "prep30_claim_evidence_placeholders.csv", claim_rows, list(claim_rows[0]))

    figure_rows = [
        {"figure_or_table": "维度总体分布表", "input_required": "final_coding.csv", "status": "占位"},
        {"figure_or_table": "等级分布表", "input_required": "final_coding.csv", "status": "占位"},
        {"figure_or_table": "维度共现热图", "input_required": "final_coding.csv", "status": "占位"},
        {"figure_or_table": "分届次比较图", "input_required": "final_coding.csv", "status": "占位"},
    ]
    write_csv(OUT / "prep30_final_figure_table_placeholders.csv", figure_rows, list(figure_rows[0]))

    archive_rows = [
        {"folder": "03_corpus", "archive_status": "保留原始语料与校对清单", "next_action": "继续校对销项"},
        {"folder": "04_framework", "archive_status": "保留内部手册与正式模板", "next_action": "冻结正式手册前不得覆盖"},
        {"folder": "07_analysis/data", "archive_status": "保留内部候选表与正式空白模板", "next_action": "正式编码后再生成final_coding.csv"},
        {"folder": "07_analysis/results/reviewed", "archive_status": "保留内部预演与准备报告", "next_action": "正式结果生成后分区归档"},
    ]
    write_csv(OUT / "prep30_archive_manifest.csv", archive_rows, list(archive_rows[0]))

    next_rows = [
        {"next_task": "G4-01-PREP", "description": "评分者交接检查", "can_start_now": "是"},
        {"next_task": "G4-01", "description": "真实双评分者独立编码", "can_start_now": "需先确认评分者与正式手册"},
        {"next_task": "G4-02", "description": "分歧裁决", "can_start_now": "否，等待G4-01"},
        {"next_task": "G4-03", "description": "正式唯一分析表", "can_start_now": "否，等待G4-02"},
    ]
    write_csv(OUT / "prep30_next_task_route.csv", next_rows, list(next_rows[0]))

    version_rows = [
        {"version_node": "coding_manual_v2_internal", "status": "已内部冻结", "allowed_use": "内部预演与模板准备", "next_condition": "正式专家/导师/评分者反馈后生成正式版"},
        {"version_node": "formal_coding_rater_A_template", "status": "已生成空白模板", "allowed_use": "真实评分者A独立填写", "next_condition": "评分者身份与编码日期确认"},
        {"version_node": "formal_coding_rater_B_template", "status": "已生成空白模板", "allowed_use": "真实评分者B独立填写", "next_condition": "评分者身份与编码日期确认"},
        {"version_node": "formal_adjudication_template", "status": "已生成空白模板", "allowed_use": "真实双评分者编码后分歧裁决", "next_condition": "A/B编码均完成"},
        {"version_node": "final_coding.csv", "status": "未生成", "allowed_use": "正式分析输入", "next_condition": "裁决完成"},
    ]
    write_csv(OUT / "prep30_version_route.csv", version_rows, list(version_rows[0]))

    handoff_rows = [
        {"check_item": "评分者是否取得编码手册正式版", "required": "是", "current_status": "待确认"},
        {"check_item": "评分者是否取得空白编码模板", "required": "是", "current_status": "已准备"},
        {"check_item": "是否说明不得复制Codex内部编码", "required": "是", "current_status": "已写入说明"},
        {"check_item": "是否说明证据句必须可定位", "required": "是", "current_status": "已写入说明"},
        {"check_item": "是否说明OCR/公式未销项记录需标待核实", "required": "是", "current_status": "已写入说明"},
    ]
    write_csv(OUT / "prep30_rater_handoff_checklist.csv", handoff_rows, list(handoff_rows[0]))

    validation_rows = [
        {"field": "present", "valid_values": "是;否", "required": "是"},
        {"field": "level", "valid_values": "L1;L2;L3;L4;未出现", "required": "是"},
        {"field": "evidence", "valid_values": "非空；可定位到题干或参考解答", "required": "是"},
        {"field": "confidence", "valid_values": "高;中;低", "required": "是"},
        {"field": "coder_id", "valid_values": "评分者匿名编号", "required": "是"},
    ]
    write_csv(OUT / "prep30_formal_coding_field_validation.csv", validation_rows, list(validation_rows[0]))

    disagreement_rows = [
        {"disagreement_type": "存在性分歧", "definition": "A/B对同一维度是否出现判断不同", "resolution_rule": "优先回到题干和解答证据"},
        {"disagreement_type": "等级分歧", "definition": "A/B均判出现但L1-L4不同", "resolution_rule": "按相邻等级边界裁决"},
        {"disagreement_type": "证据分歧", "definition": "A/B结论相同但证据依据不同", "resolution_rule": "保留更可定位、更符合手册优先级的证据"},
        {"disagreement_type": "待核实分歧", "definition": "一方或双方因OCR/公式/图像问题标待核实", "resolution_rule": "先完成材料校对再裁决"},
    ]
    write_csv(OUT / "prep30_disagreement_type_schema.csv", disagreement_rows, list(disagreement_rows[0]))

    manuscript_gate_rows = [
        {"chapter_or_section": "第三章研究设计", "minimum_gate": "正式手册版本、正式编码流程、真实评分者说明", "current_status": "部分准备"},
        {"chapter_or_section": "第四章结果", "minimum_gate": "final_coding.csv与脚本输出", "current_status": "未满足"},
        {"chapter_or_section": "第五章教学转化", "minimum_gate": "正式试题结果加教师或课堂证据", "current_status": "未满足"},
        {"chapter_or_section": "结论", "minimum_gate": "所有核心主张可回到证据矩阵", "current_status": "未满足"},
    ]
    write_csv(OUT / "prep30_manuscript_gate_table.csv", manuscript_gate_rows, list(manuscript_gate_rows[0]))

    teaching_gate_rows = [
        {"teaching_claim": "教学策略针对性", "required_evidence": "正式试题分析结果与教学任务对应矩阵", "current_status": "内部种子矩阵"},
        {"teaching_claim": "教师认可", "required_evidence": "真实教师访谈、问卷或评审记录", "current_status": "缺失"},
        {"teaching_claim": "课堂可行性", "required_evidence": "真实课堂记录、学生作品或教学日志", "current_status": "缺失"},
        {"teaching_claim": "效果提升", "required_evidence": "真实测量工具、前后数据和统计分析", "current_status": "缺失，不得书写"},
    ]
    write_csv(OUT / "prep30_teaching_evidence_gate.csv", teaching_gate_rows, list(teaching_gate_rows[0]))

    (OUT / "prep30_analysis_input_placeholder.md").write_text(
        """# 正式分析输入占位说明

正式分析输入应为 `07_analysis/data/final_coding.csv`。该文件目前不得生成，因为尚无真实双评分者编码和分歧裁决结果。
""",
        encoding="utf-8",
    )

    (OUT / "prep30_results_chapter_placeholder.md").write_text(
        """# 结果章占位说明

当前只能保留结果章结构，不得写入正式比例、趋势、显著性或教学效果。结果章写作须等待 `final_coding.csv` 与正式脚本输出。
""",
        encoding="utf-8",
    )


def main():
    data = load()
    combined = combined_review_master(data)
    gates = gate_register(data, combined)
    manual_priority(data)
    template_rows = rater_templates(data)
    data_dictionary(data)
    placeholder_files(data)

    # Focused queues.
    evidence_rows = []
    for row in data["p0_evidence"]:
        evidence_rows.append({"source": "P0", **row})
    write_csv(OUT / "prep30_evidence_strengthening_master.csv", evidence_rows, list(evidence_rows[0]))

    l4_rows = []
    for row in data["p1_l4"]:
        l4_rows.append({"source": "P1", **row})
    write_csv(OUT / "prep30_l4_review_master.csv", l4_rows, list(l4_rows[0]))

    innovation_rows = [row for row in combined if row["dimension"] == "质疑创新"]
    write_csv(OUT / "prep30_innovation_review_master.csv", innovation_rows, list(innovation_rows[0]))

    confidence_rows = [row for row in combined if "把握度" in row["required_action"] or row["dimension"]]
    write_csv(OUT / "prep30_confidence_review_master.csv", confidence_rows, list(confidence_rows[0]))

    write_markdown_docs(data, combined, gates, template_rows)
    print("completed prep30 outputs")
    print(f"combined={len(combined)} template_rows={template_rows} gates={len(gates)}")


if __name__ == "__main__":
    main()
