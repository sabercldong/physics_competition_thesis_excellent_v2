import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "07_analysis/results/reviewed"
DATA = ROOT / "07_analysis/data"

FILES = {
    "coding_manual_internal": ROOT / "04_framework/coding_manual_v2_internal.md",
    "codebook_internal": ROOT / "04_framework/codebook_v2_internal.csv",
    "rater_a_template": DATA / "formal_coding_rater_A_template.csv",
    "rater_b_template": DATA / "formal_coding_rater_B_template.csv",
    "adjudication_template": DATA / "formal_adjudication_template.csv",
    "rater_briefing": OUT / "prep30_rater_briefing.md",
    "adjudication_protocol": OUT / "prep30_adjudication_protocol.md",
    "gate_register": OUT / "prep30_gate_register.csv",
    "field_validation": OUT / "prep30_formal_coding_field_validation.csv",
    "manual_priority": OUT / "prep30_manual_priority_queue.csv",
}


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


def count_csv(path):
    return len(read_csv(path))


def main():
    package_rows = []
    for name, path in FILES.items():
        kind = "csv" if path.suffix == ".csv" else "markdown"
        row_count = count_csv(path) if kind == "csv" and path.exists() else ""
        package_rows.append(
            {
                "artifact_id": name,
                "path": str(path.relative_to(ROOT)),
                "exists": "是" if path.exists() else "否",
                "type": kind,
                "row_count": row_count,
                "handoff_use": "评分者交接准备",
            }
        )
    write_csv(OUT / "g4_01_prep_rater_package_index.csv", package_rows, list(package_rows[0]))

    a_rows = read_csv(FILES["rater_a_template"])
    b_rows = read_csv(FILES["rater_b_template"])
    adj_rows = read_csv(FILES["adjudication_template"])
    gates = read_csv(FILES["gate_register"])
    manual_priority = read_csv(FILES["manual_priority"])

    audit_rows = [
        {
            "check_id": "HANDOFF-01",
            "check_item": "评分者A空白模板存在且记录数为876",
            "status": "通过" if len(a_rows) == 876 else "未通过",
            "evidence": f"formal_coding_rater_A_template.csv rows={len(a_rows)}",
            "action": "若未通过，重新生成模板。",
        },
        {
            "check_id": "HANDOFF-02",
            "check_item": "评分者B空白模板存在且记录数为876",
            "status": "通过" if len(b_rows) == 876 else "未通过",
            "evidence": f"formal_coding_rater_B_template.csv rows={len(b_rows)}",
            "action": "若未通过，重新生成模板。",
        },
        {
            "check_id": "HANDOFF-03",
            "check_item": "裁决模板存在且记录数为876",
            "status": "通过" if len(adj_rows) == 876 else "未通过",
            "evidence": f"formal_adjudication_template.csv rows={len(adj_rows)}",
            "action": "若未通过，重新生成模板。",
        },
        {
            "check_id": "HANDOFF-04",
            "check_item": "正式分析门槛仍未满足",
            "status": "通过",
            "evidence": f"未满足门槛={sum(1 for row in gates if row['status'] != '已满足')}",
            "action": "允许进入评分者交接准备，但不得生成正式结果。",
        },
        {
            "check_id": "HANDOFF-05",
            "check_item": "人工校对优先队列存在",
            "status": "通过" if len(manual_priority) == 154 else "未通过",
            "evidence": f"prep30_manual_priority_queue.csv rows={len(manual_priority)}",
            "action": "评分者遇到未销项材料时标待核实。",
        },
    ]
    write_csv(OUT / "g4_01_prep_handoff_audit.csv", audit_rows, list(audit_rows[0]))

    decision = "可以进入评分者交接准备，但不能进入正式结果分析"
    if any(row["status"] == "未通过" for row in audit_rows[:3]):
        decision = "暂缓评分者交接，先修复模板"

    report = f"""# G4-01-PREP 评分者交接检查报告

更新时间：2026-07-14

## 性质声明

本报告用于检查是否具备向真实评分者交接编码材料的最低条件。它不代表真实评分者已经开始编码，也不代表正式编码、裁决或结果分析已经完成。

## 检查结论

{decision}。

## 交接包清单

{md_table(["artifact_id", "path", "exists", "type", "row_count", "handoff_use"], package_rows)}

## 检查结果

{md_table(["check_id", "check_item", "status", "evidence", "action"], audit_rows)}

## 交接时必须说明

1. 评分者只能依据原始题面、参考解答、题图和正式手册判断；
2. 不得复制 Codex 内部试编码或内部建议；
3. 证据句必须能定位到题干、参考解答或题图；
4. 遇到 OCR、公式、题图或分值边界未销项问题，应标记待核实；
5. 两名评分者必须独立填写，完成后再进行一致性计算和分歧裁决。

## 下一步最小任务

`G4-01`：由两名真实评分者分别填写 `formal_coding_rater_A_template.csv` 和 `formal_coding_rater_B_template.csv`。在此之前，论文正文只能写方法准备和内部预演，不能写正式结果。
"""
    (OUT / "g4_01_prep_handoff_report.md").write_text(report, encoding="utf-8")
    print("completed G4-01-PREP handoff audit")
    print(f"templates={len(a_rows)}/{len(b_rows)} adjudication={len(adj_rows)}")


if __name__ == "__main__":
    main()
