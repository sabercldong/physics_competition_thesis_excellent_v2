import csv
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
INTERNAL_CODING = ROOT / "07_analysis/data/internal_coding_v1.csv"
QUALITY_ISSUES = ROOT / "07_analysis/results/reviewed/internal_coding_quality_issues.csv"
MANUAL_REVIEW = ROOT / "03_corpus/manual_review_checklist.csv"
OUT_DIR = ROOT / "07_analysis/results/reviewed"

SAMPLE_ITEMS = OUT_DIR / "preformal_review_sample_items.csv"
SAMPLE_CODING = OUT_DIR / "preformal_review_coding_records.csv"
SAMPLE_MANUAL = OUT_DIR / "preformal_review_manual_issues.csv"
PACKET = OUT_DIR / "preformal_review_packet.md"

TARGET_PER_COMPETITION = 8
MIN_SAMPLE_SIZE = 64
DIMENSIONS = ["模型建构", "科学推理", "科学论证", "质疑创新"]
WEIGHTS = {
    "质疑创新保守复核": 100,
    "证据文本薄弱": 70,
    "高等级边界": 45,
    "人工校对未销项": 35,
    "元数据待核风险": 20,
    "编码把握度": 12,
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


def split_items(value):
    return [part.strip() for part in value.split(";") if part.strip()]


def md_table(headers, rows):
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(h, "")) for h in headers) + " |")
    return "\n".join(lines)


def first_meta_by_item(coding_rows):
    meta = {}
    for row in coding_rows:
        meta.setdefault(row["item_id"], row)
    return meta


def issue_maps(issue_rows):
    by_item = defaultdict(list)
    global_issues = []
    for row in issue_rows:
        if row.get("item_id"):
            by_item[row["item_id"]].append(row)
        else:
            global_issues.append(row)
    return by_item, global_issues


def manual_maps(manual_rows):
    by_item = defaultdict(list)
    for row in manual_rows:
        if row.get("review_status") != "待人工校对":
            continue
        for item_id in split_items(row.get("affected_item_ids", "")):
            by_item[item_id].append(row)
    return by_item


def item_scores(meta_by_item, issues_by_item, manual_by_item):
    scores = {}
    categories = {}
    dimensions = {}
    manual_types = {}
    for item_id in meta_by_item:
        category_counter = Counter(row["category"] for row in issues_by_item.get(item_id, []))
        dim_counter = Counter(row["dimension"] for row in issues_by_item.get(item_id, []) if row["dimension"])
        type_counter = Counter(row["issue_type"] for row in manual_by_item.get(item_id, []))
        severity_counter = Counter(row["severity"] for row in manual_by_item.get(item_id, []))
        score = sum(WEIGHTS.get(category, 5) * count for category, count in category_counter.items())
        score += severity_counter.get("高", 0) * 18 + severity_counter.get("中", 0) * 8
        if "题干OCR校对" in type_counter:
            score += 20
        if "公式与特殊符号校对" in type_counter:
            score += 18
        if "题图裁边与图注校对" in type_counter:
            score += 10
        scores[item_id] = score
        categories[item_id] = category_counter
        dimensions[item_id] = dim_counter
        manual_types[item_id] = type_counter
    return scores, categories, dimensions, manual_types


def select_items(meta_by_item, scores, categories):
    selected = set()

    def add_by_category(category):
        item_ids = [
            item_id
            for item_id, counter in categories.items()
            if counter.get(category, 0) > 0
        ]
        for item_id in sorted(item_ids, key=lambda x: (-scores[x], x)):
            selected.add(item_id)

    add_by_category("质疑创新保守复核")
    add_by_category("证据文本薄弱")

    # Ensure every competition has a useful minimum coverage.
    by_competition = defaultdict(list)
    for item_id, meta in meta_by_item.items():
        by_competition[meta["competition_no"]].append(item_id)
    for competition_no, item_ids in by_competition.items():
        ranked = sorted(item_ids, key=lambda x: (-scores[x], x))
        current = [item_id for item_id in selected if meta_by_item[item_id]["competition_no"] == competition_no]
        for item_id in ranked:
            if len(current) >= TARGET_PER_COMPETITION:
                break
            if item_id not in selected:
                selected.add(item_id)
                current.append(item_id)

    if len(selected) < MIN_SAMPLE_SIZE:
        ranked_all = sorted(meta_by_item, key=lambda x: (-scores[x], x))
        for item_id in ranked_all:
            selected.add(item_id)
            if len(selected) >= MIN_SAMPLE_SIZE:
                break

    return sorted(selected, key=lambda x: (int(meta_by_item[x]["competition_no"]), meta_by_item[x]["question_no"], meta_by_item[x]["subquestion_no"], x))


def reason_text(category_counter, manual_counter):
    parts = []
    for category in ["质疑创新保守复核", "证据文本薄弱", "高等级边界", "人工校对未销项", "元数据待核风险", "编码把握度"]:
        if category_counter.get(category, 0):
            parts.append(f"{category}x{category_counter[category]}")
    for issue_type in ["题干OCR校对", "公式与特殊符号校对", "题图裁边与图注校对", "第35届分值边界复核", "解答放大图一致性核对"]:
        if manual_counter.get(issue_type, 0):
            parts.append(f"{issue_type}x{manual_counter[issue_type]}")
    return "；".join(parts)


def review_focus(category_counter):
    focus = []
    if category_counter.get("质疑创新保守复核", 0):
        focus.append("核对质疑创新是否由题干明确触发，避免把陌生背景误判为创新要求")
    if category_counter.get("证据文本薄弱", 0):
        focus.append("补足可回到题干或参考解答的判定证据")
    if category_counter.get("高等级边界", 0):
        focus.append("复核L4是否确有迁移、修正、一般化、递推、优化或开放构造")
    if category_counter.get("编码把握度", 0):
        focus.append("复核中等把握度记录的维度存在性与等级")
    if not focus:
        focus.append("对照原始PDF与内部手册复核编码稳定性")
    return "；".join(focus)


def build_outputs():
    coding_rows = read_csv(INTERNAL_CODING)
    issue_rows = read_csv(QUALITY_ISSUES)
    manual_rows = read_csv(MANUAL_REVIEW)

    meta_by_item = first_meta_by_item(coding_rows)
    issues_by_item, global_issues = issue_maps(issue_rows)
    manual_by_item = manual_maps(manual_rows)
    scores, categories, dimensions, manual_types = item_scores(meta_by_item, issues_by_item, manual_by_item)
    selected = select_items(meta_by_item, scores, categories)

    item_rows = []
    for order, item_id in enumerate(selected, start=1):
        meta = meta_by_item[item_id]
        category_counter = categories[item_id]
        manual_counter = manual_types[item_id]
        item_rows.append(
            {
                "sample_order": order,
                "item_id": item_id,
                "competition_no": meta["competition_no"],
                "year": meta["year"],
                "question_no": meta["question_no"],
                "subquestion_no": meta["subquestion_no"],
                "knowledge_primary": meta["knowledge_primary"],
                "knowledge_secondary": meta["knowledge_secondary"],
                "score": scores[item_id],
                "risk_categories": reason_text(category_counter, manual_counter),
                "affected_dimensions": "；".join(sorted(dimensions[item_id])),
                "review_focus": review_focus(category_counter),
                "source_status": "内部复核样本；非正式编码结果",
            }
        )

    selected_set = set(selected)
    coding_out = []
    for row in coding_rows:
        if row["item_id"] in selected_set:
            coding_out.append(row)

    manual_out = []
    for row in manual_rows:
        affected = [item_id for item_id in split_items(row.get("affected_item_ids", "")) if item_id in selected_set]
        if affected:
            out = dict(row)
            out["selected_affected_item_ids"] = ";".join(affected)
            manual_out.append(out)

    write_csv(SAMPLE_ITEMS, item_rows, list(item_rows[0]))
    write_csv(SAMPLE_CODING, coding_out, list(coding_out[0]))
    write_csv(SAMPLE_MANUAL, manual_out, list(manual_out[0]))
    write_packet(item_rows, coding_out, manual_out, global_issues)
    return item_rows, coding_out, manual_out


def write_packet(item_rows, coding_rows, manual_rows, global_issues):
    by_comp = Counter(row["competition_no"] for row in item_rows)
    category_counter = Counter()
    for row in item_rows:
        for part in row["risk_categories"].split("；"):
            if "x" in part:
                category_counter[part.split("x", 1)[0]] += 1
    comp_rows = [{"competition_no": key, "sample_items": by_comp[key]} for key in sorted(by_comp, key=lambda x: int(x))]
    category_rows = [{"risk_type": key, "sample_items": count} for key, count in sorted(category_counter.items(), key=lambda x: (-x[1], x[0]))]

    global_text = "\n".join(
        f"- {row['finding']} 处理要求：{row['recommended_action']}"
        for row in global_issues
    ) or "- 无全局问题。"

    content = f"""# 正式编码前复核样本包

更新时间：2026-07-14

## 性质声明

本样本包由 `07_analysis/scripts/build_preformal_review_packet.py` 基于内部分析底稿和质量检查问题清单生成。它只用于正式编码前的复核、训练和问题定位，不是正式编码结果，不代表真实专家审查、导师确认或真实双评分者一致性。

## 输入文件

- `07_analysis/data/internal_coding_v1.csv`
- `07_analysis/results/reviewed/internal_coding_quality_issues.csv`
- `03_corpus/manual_review_checklist.csv`
- `04_framework/coding_manual_v2_internal.md`

## 输出文件

- `07_analysis/results/reviewed/preformal_review_sample_items.csv`
- `07_analysis/results/reviewed/preformal_review_coding_records.csv`
- `07_analysis/results/reviewed/preformal_review_manual_issues.csv`
- `07_analysis/results/reviewed/preformal_review_packet.md`

## 样本规模

- 复核样本分析单元：{len(item_rows)}
- 对应编码记录：{len(coding_rows)}
- 关联人工校对条目：{len(manual_rows)}

## 分届覆盖

{md_table(["competition_no", "sample_items"], comp_rows)}

## 风险覆盖

{md_table(["risk_type", "sample_items"], category_rows)}

## 全局问题

{global_text}

## 复核流程

1. 先对 `preformal_review_manual_issues.csv` 中关联的原始PDF、公式、OCR和题图问题逐条销项；
2. 再用 `preformal_review_coding_records.csv` 对照 `coding_manual_v2_internal.md` 复核维度存在性和等级；
3. 对 L4 记录逐条确认是否存在迁移、修正、一般化、递推、优化或开放构造；
4. 对质疑创新记录逐条确认题干是否明确要求处理假设、替代模型、模型失效或开放方案；
5. 对证据文本薄弱记录补充可回到题干或参考解答的证据句；
6. 复核完成后不得直接覆盖内部底稿，应先形成修订日志，再决定是否进入正式编码表。

## 不得形成的结论

- 不得据此写正式维度比例、届次变化或知识模块差异；
- 不得把样本包写成专家审查或真实评分者结果；
- 不得把 Codex 试编码当成正式双人独立编码；
- 不得在人工校对未销项前使用受影响记录支撑论文结论。

## 下一步最小任务

执行 `G4-00S`：建立复核记录表，逐条记录样本包中的校对状态、复核结论、是否修订编码、修订理由和仍待核实事项。
"""
    PACKET.write_text(content, encoding="utf-8")


def main():
    item_rows, coding_rows, manual_rows = build_outputs()
    print(f"sample_items={len(item_rows)} coding_records={len(coding_rows)} manual_issues={len(manual_rows)}")
    print(f"wrote {SAMPLE_ITEMS}")
    print(f"wrote {SAMPLE_CODING}")
    print(f"wrote {SAMPLE_MANUAL}")
    print(f"wrote {PACKET}")


if __name__ == "__main__":
    main()
