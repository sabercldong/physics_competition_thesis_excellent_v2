import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SAMPLE_ITEMS = ROOT / "07_analysis/results/reviewed/preformal_review_sample_items.csv"
SAMPLE_CODING = ROOT / "07_analysis/results/reviewed/preformal_review_coding_records.csv"
OUT_LOG = ROOT / "07_analysis/results/reviewed/preformal_review_log.csv"
OUT_PROTOCOL = ROOT / "07_analysis/results/reviewed/preformal_review_log_protocol.md"


def read_csv(path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path, rows, fieldnames):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main():
    sample_items = {row["item_id"]: row for row in read_csv(SAMPLE_ITEMS)}
    coding_rows = read_csv(SAMPLE_CODING)
    fieldnames = [
        "review_id",
        "sample_order",
        "item_id",
        "competition_no",
        "year",
        "question_no",
        "subquestion_no",
        "dimension",
        "internal_present",
        "internal_level",
        "internal_confidence",
        "internal_evidence",
        "risk_categories",
        "review_focus",
        "text_formula_figure_checked",
        "v2_boundary_checked",
        "proposed_present",
        "proposed_level",
        "proposed_evidence",
        "revision_decision",
        "revision_reason",
        "unresolved_issue",
        "reviewer",
        "review_date",
        "review_status",
    ]

    rows = []
    for index, row in enumerate(coding_rows, start=1):
        sample = sample_items[row["item_id"]]
        rows.append(
            {
                "review_id": f"PR-{index:03d}",
                "sample_order": sample["sample_order"],
                "item_id": row["item_id"],
                "competition_no": row["competition_no"],
                "year": row["year"],
                "question_no": row["question_no"],
                "subquestion_no": row["subquestion_no"],
                "dimension": row["dimension"],
                "internal_present": row["present"],
                "internal_level": row["level"],
                "internal_confidence": row["confidence"],
                "internal_evidence": row["evidence"],
                "risk_categories": sample["risk_categories"],
                "review_focus": sample["review_focus"],
                "text_formula_figure_checked": "待复核",
                "v2_boundary_checked": "待复核",
                "proposed_present": "",
                "proposed_level": "",
                "proposed_evidence": "",
                "revision_decision": "待复核",
                "revision_reason": "",
                "unresolved_issue": "",
                "reviewer": "",
                "review_date": "",
                "review_status": "待复核",
            }
        )

    write_csv(OUT_LOG, rows, fieldnames)
    OUT_PROTOCOL.write_text(
        """# 正式编码前复核记录表使用说明

更新时间：2026-07-14

## 性质声明

`preformal_review_log.csv` 是复核记录空表，服务于正式编码前的内部质量控制。当前所有记录均为“待复核”，不得视为已经完成校对、编码修订或分歧裁决。

## 使用顺序

1. 先处理同一样本在 `preformal_review_manual_issues.csv` 中关联的题干、公式、OCR、题图或分值边界问题；
2. 在 `text_formula_figure_checked` 中记录是否已经对照原始PDF完成校对；
3. 对照 `coding_manual_v2_internal.md` 复核维度存在性与等级，在 `v2_boundary_checked` 中记录是否完成；
4. 若保留内部试编码，填写 `revision_decision=保留` 并说明理由；
5. 若修订，填写 `proposed_present`、`proposed_level`、`proposed_evidence` 和 `revision_reason`；
6. 证据不足时填写 `unresolved_issue`，不要自行补齐；
7. 只有在全部样本完成复核并形成修订日志后，才可考虑生成下一版内部编码表。

## 允许的修订决定

- `保留`
- `修订存在性`
- `修订等级`
- `修订证据`
- `待核实`

## 禁止事项

- 不得把本表空白记录当作复核完成；
- 不得把 Codex 内部复核写成真实专家或真实评分者意见；
- 不得在题干、公式或图像问题未销项前形成正式编码结论；
- 不得直接覆盖 `internal_coding_v1.csv`。
""",
        encoding="utf-8",
    )
    print(f"review_log_rows={len(rows)}")
    print(f"wrote {OUT_LOG}")
    print(f"wrote {OUT_PROTOCOL}")


if __name__ == "__main__":
    main()
