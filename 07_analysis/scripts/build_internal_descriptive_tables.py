from collections import Counter, defaultdict
import csv
from itertools import combinations
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ITEM_INDEX = ROOT / "03_corpus/item_index.csv"
PILOT_CODING = ROOT / "04_framework/pilot_coding.csv"
OUT_DATA = ROOT / "07_analysis/data/internal_coding_v1.csv"
OUT_GENERATED = ROOT / "07_analysis/results/generated"
OUT_REVIEWED = ROOT / "07_analysis/results/reviewed"
SUMMARY = OUT_REVIEWED / "internal_descriptive_summary.md"

DIMENSIONS = ["模型建构", "科学推理", "科学论证", "质疑创新"]
INTERNAL_VERSION = "internal_v1_codex_pilot"
INTERNAL_STATUS = "内部分析用；基于Codex试编码；非正式结果"
INTERNAL_MANUAL = "coding_manual_v2_internal"


def read_csv(path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path, rows, fieldnames):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def pct(numerator, denominator):
    if not denominator:
        return "0.000"
    return f"{numerator / denominator:.3f}"


def md_table(headers, rows):
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(h, "")) for h in headers) + " |")
    return "\n".join(lines)


def build_internal_dataset():
    index_rows = read_csv(ITEM_INDEX)
    coding_rows = read_csv(PILOT_CODING)
    index_by_id = {row["item_id"]: row for row in index_rows}

    if len(index_by_id) != len(index_rows):
        raise ValueError("item_index.csv contains duplicate item_id values.")

    coding_items = {row["item_id"] for row in coding_rows}
    missing = sorted(coding_items - set(index_by_id))
    if missing:
        raise ValueError(f"pilot_coding.csv contains item_id not found in item_index.csv: {missing[:5]}")

    counts = Counter(row["item_id"] for row in coding_rows)
    bad_counts = sorted(item_id for item_id, count in counts.items() if count != len(DIMENSIONS))
    if bad_counts:
        raise ValueError(f"Expected 4 dimension rows per item_id, found mismatch: {bad_counts[:5]}")

    meta_fields = [
        "item_id",
        "competition_no",
        "year",
        "question_no",
        "subquestion_no",
        "analysis_unit",
        "score",
        "page_paper",
        "page_solution",
        "knowledge_primary",
        "knowledge_secondary",
        "context_source",
        "context_authenticity",
        "representation",
        "math_tools",
        "answer_structure",
        "source_verified",
        "notes",
    ]
    out_fields = meta_fields + [
        "dimension",
        "present",
        "present_binary",
        "level",
        "evidence",
        "confidence",
        "coder",
        "source_manual_version",
        "manual_version",
        "pilot_date",
        "analysis_version",
        "analysis_status",
    ]

    out_rows = []
    for row in coding_rows:
        meta = index_by_id[row["item_id"]]
        present = row["present"].strip()
        present_binary = "1" if present == "是" else "0"
        out_row = {field: meta.get(field, "") for field in meta_fields}
        out_row.update(
            {
                "dimension": row["dimension"],
                "present": present,
                "present_binary": present_binary,
                "level": row["level"],
                "evidence": row["evidence"],
                "confidence": row["confidence"],
                "coder": row["coder"],
                "source_manual_version": row["manual_version"],
                "manual_version": INTERNAL_MANUAL,
                "pilot_date": row["date"],
                "analysis_version": INTERNAL_VERSION,
                "analysis_status": INTERNAL_STATUS,
            }
        )
        out_rows.append(out_row)

    write_csv(OUT_DATA, out_rows, out_fields)
    return out_rows


def make_tables(rows):
    item_ids = sorted({row["item_id"] for row in rows})
    total_items = len(item_ids)

    presence = []
    for dimension in DIMENSIONS:
        dimension_rows = [row for row in rows if row["dimension"] == dimension]
        present_items = {row["item_id"] for row in dimension_rows if row["present_binary"] == "1"}
        presence.append(
            {
                "dimension": dimension,
                "items_present": len(present_items),
                "total_items": total_items,
                "proportion": pct(len(present_items), total_items),
            }
        )

    levels = []
    for dimension in DIMENSIONS:
        level_counts = Counter(
            row["level"]
            for row in rows
            if row["dimension"] == dimension and row["present_binary"] == "1"
        )
        for level in sorted(level_counts):
            levels.append(
                {
                    "dimension": dimension,
                    "level": level,
                    "count": level_counts[level],
                    "within_dimension_proportion": pct(level_counts[level], sum(level_counts.values())),
                }
            )

    competition_totals = defaultdict(set)
    competition_present = defaultdict(set)
    for row in rows:
        competition_totals[row["competition_no"]].add(row["item_id"])
        if row["present_binary"] == "1":
            competition_present[(row["competition_no"], row["dimension"])].add(row["item_id"])

    by_competition = []
    for competition_no in sorted(competition_totals, key=lambda x: int(x)):
        total = len(competition_totals[competition_no])
        for dimension in DIMENSIONS:
            present_count = len(competition_present[(competition_no, dimension)])
            by_competition.append(
                {
                    "competition_no": competition_no,
                    "dimension": dimension,
                    "items_present": present_count,
                    "total_items": total,
                    "proportion": pct(present_count, total),
                }
            )

    knowledge_totals = defaultdict(set)
    knowledge_present = defaultdict(set)
    for row in rows:
        knowledge = row["knowledge_primary"]
        knowledge_totals[knowledge].add(row["item_id"])
        if row["present_binary"] == "1":
            knowledge_present[(knowledge, row["dimension"])].add(row["item_id"])

    by_knowledge = []
    for knowledge in sorted(knowledge_totals):
        total = len(knowledge_totals[knowledge])
        for dimension in DIMENSIONS:
            present_count = len(knowledge_present[(knowledge, dimension)])
            by_knowledge.append(
                {
                    "knowledge_primary": knowledge,
                    "dimension": dimension,
                    "items_present": present_count,
                    "total_items": total,
                    "proportion": pct(present_count, total),
                }
            )

    present_by_item = defaultdict(set)
    for row in rows:
        if row["present_binary"] == "1":
            present_by_item[row["item_id"]].add(row["dimension"])
    cooccurrence = []
    for left, right in combinations(DIMENSIONS, 2):
        count = sum(1 for dims in present_by_item.values() if left in dims and right in dims)
        cooccurrence.append(
            {
                "dimension_pair": f"{left}+{right}",
                "items_present_together": count,
                "total_items": total_items,
                "proportion": pct(count, total_items),
            }
        )

    write_csv(OUT_GENERATED / "internal_dimension_presence.csv", presence, list(presence[0]))
    write_csv(OUT_GENERATED / "internal_dimension_levels.csv", levels, list(levels[0]))
    write_csv(OUT_GENERATED / "internal_dimension_by_competition.csv", by_competition, list(by_competition[0]))
    write_csv(OUT_GENERATED / "internal_dimension_by_knowledge.csv", by_knowledge, list(by_knowledge[0]))
    write_csv(OUT_GENERATED / "internal_dimension_cooccurrence.csv", cooccurrence, list(cooccurrence[0]))

    return {
        "total_items": total_items,
        "total_rows": len(rows),
        "presence": presence,
        "levels": levels,
        "by_competition": by_competition,
        "by_knowledge": by_knowledge,
        "cooccurrence": cooccurrence,
    }


def write_summary(stats):
    top_by_knowledge = [
        row for row in stats["by_knowledge"] if row["total_items"] and int(row["total_items"]) >= 5
    ]
    content = f"""# 内部描述统计准备说明

更新时间：2026-07-14

## 性质声明

本文件由 `07_analysis/scripts/build_internal_descriptive_tables.py` 基于 `03_corpus/item_index.csv` 和 `04_framework/pilot_coding.csv` 生成。当前数据为 Codex 试编码整理后的内部分析底稿，只用于检查字段、脚本和表格结构，不是正式论文结果。

不得据此写入：

- 正式维度比例；
- 届次变化结论；
- 知识模块差异结论；
- 显著性、因果或教学效果表述；
- 专家审查、导师确认或真实评分者一致性已经完成的表述。

## 数据范围

- 分析单元数：{stats["total_items"]}
- 编码记录数：{stats["total_rows"]}
- 每个分析单元维度数：4
- 手册版本：`coding_manual_v2_internal`
- 数据版本：`internal_v1_codex_pilot`

## 字段检查

- `item_index.csv` 与 `pilot_coding.csv` 的 `item_id` 已完成内部匹配；
- 每个 `item_id` 均有四个维度记录；
- 输出数据表为 `07_analysis/data/internal_coding_v1.csv`；
- 生成表保存于 `07_analysis/results/generated/`，该目录为可复现输出，不纳入提交对象。

## 维度出现预演表

{md_table(["dimension", "items_present", "total_items", "proportion"], stats["presence"])}

## 维度共现预演表

{md_table(["dimension_pair", "items_present_together", "total_items", "proportion"], stats["cooccurrence"])}

## 当前致命边界

- `03_corpus/manual_review_checklist.csv` 中仍有待核项，OCR、公式、图注和题图边界尚未全部人工销项；
- 尚未完成真实专家审查或导师确认；
- 尚未完成两名真实评分者独立编码；
- 尚未完成真实分歧裁决；
- 当前输出不能作为正式结果章、摘要或结论依据。

## 下一步最小任务

在不写论文正文的前提下，建议先执行 `G4-00R`：检查 `internal_coding_v1.csv` 的字段完整性、异常值、维度分布极端项和证据文本缺口，形成正式编码前的数据质量问题清单。
"""
    OUT_REVIEWED.mkdir(parents=True, exist_ok=True)
    SUMMARY.write_text(content, encoding="utf-8")


def main():
    rows = build_internal_dataset()
    stats = make_tables(rows)
    write_summary(stats)
    print(f"wrote {OUT_DATA} rows={stats['total_rows']} items={stats['total_items']}")
    print(f"wrote {SUMMARY}")


if __name__ == "__main__":
    main()
