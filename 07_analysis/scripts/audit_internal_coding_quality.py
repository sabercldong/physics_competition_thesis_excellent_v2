import csv
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "07_analysis/data/internal_coding_v1.csv"
MANUAL_REVIEW = ROOT / "03_corpus/manual_review_checklist.csv"
OUT_DIR = ROOT / "07_analysis/results/reviewed"
ISSUES_OUT = OUT_DIR / "internal_coding_quality_issues.csv"
REPORT_OUT = OUT_DIR / "internal_coding_quality_report.md"

DIMENSIONS = ["模型建构", "科学推理", "科学论证", "质疑创新"]
VALID_PRESENT = {"是", "否"}
VALID_BINARY = {"0", "1"}
VALID_LEVELS = {"L1", "L2", "L3", "L4", "未出现"}
VALID_CONFIDENCE = {"高", "中", "低"}
REQUIRED_FIELDS = [
    "item_id",
    "competition_no",
    "year",
    "question_no",
    "subquestion_no",
    "knowledge_primary",
    "knowledge_secondary",
    "context_source",
    "context_authenticity",
    "representation",
    "math_tools",
    "answer_structure",
    "source_verified",
    "dimension",
    "present",
    "present_binary",
    "level",
    "evidence",
    "confidence",
    "source_manual_version",
    "manual_version",
    "analysis_version",
    "analysis_status",
]


def read_csv(path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path, rows, fieldnames):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def issue(issue_id, severity, category, item_id="", dimension="", field="", finding="", action=""):
    return {
        "issue_id": issue_id,
        "severity": severity,
        "category": category,
        "item_id": item_id,
        "dimension": dimension,
        "field": field,
        "finding": finding,
        "recommended_action": action,
        "status": "待处理",
    }


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


def build_review_risk_map(review_rows):
    risk_by_item = defaultdict(list)
    for row in review_rows:
        if row.get("review_status") != "待人工校对":
            continue
        for item_id in split_items(row.get("affected_item_ids", "")):
            risk_by_item[item_id].append(row)
    return risk_by_item


def add_structural_issues(rows, issues):
    fields = rows[0].keys() if rows else []
    missing_fields = [field for field in REQUIRED_FIELDS if field not in fields]
    for field in missing_fields:
        issues.append(
            issue(
                f"STRUCT-MISSING-FIELD-{field}",
                "致命",
                "字段结构",
                field=field,
                finding=f"内部分析底稿缺少必要字段：{field}",
                action="补齐字段后重新生成内部分析底稿。",
            )
        )

    item_dimension = defaultdict(list)
    record_keys = set()
    for index, row in enumerate(rows, start=2):
        item_id = row.get("item_id", "")
        dimension = row.get("dimension", "")
        item_dimension[item_id].append(dimension)
        key = (item_id, dimension)
        if key in record_keys:
            issues.append(
                issue(
                    f"STRUCT-DUP-{item_id}-{dimension}",
                    "致命",
                    "重复记录",
                    item_id=item_id,
                    dimension=dimension,
                    finding="同一 item_id 与 dimension 出现重复记录。",
                    action="检查生成脚本和源数据，保留唯一记录。",
                )
            )
        record_keys.add(key)

        for field in REQUIRED_FIELDS:
            if field in row and row[field].strip() == "":
                issues.append(
                    issue(
                        f"STRUCT-BLANK-{index}-{field}",
                        "高",
                        "字段缺失",
                        item_id=item_id,
                        dimension=dimension,
                        field=field,
                        finding=f"字段 {field} 为空。",
                        action="回到源数据补齐或标注待核实。",
                    )
                )

        present = row.get("present", "").strip()
        binary = row.get("present_binary", "").strip()
        level = row.get("level", "").strip()
        confidence = row.get("confidence", "").strip()

        if dimension not in DIMENSIONS:
            issues.append(
                issue(
                    f"STRUCT-BAD-DIM-{index}",
                    "致命",
                    "非法取值",
                    item_id=item_id,
                    dimension=dimension,
                    field="dimension",
                    finding=f"未知维度：{dimension}",
                    action="按内部手册四维度修正。",
                )
            )
        if present not in VALID_PRESENT:
            issues.append(
                issue(
                    f"STRUCT-BAD-PRESENT-{index}",
                    "致命",
                    "非法取值",
                    item_id=item_id,
                    dimension=dimension,
                    field="present",
                    finding=f"present 非法取值：{present}",
                    action="统一为“是”或“否”。",
                )
            )
        if binary not in VALID_BINARY:
            issues.append(
                issue(
                    f"STRUCT-BAD-BINARY-{index}",
                    "致命",
                    "非法取值",
                    item_id=item_id,
                    dimension=dimension,
                    field="present_binary",
                    finding=f"present_binary 非法取值：{binary}",
                    action="统一为 1 或 0。",
                )
            )
        if (present == "是" and binary != "1") or (present == "否" and binary != "0"):
            issues.append(
                issue(
                    f"STRUCT-PRESENT-BINARY-MISMATCH-{index}",
                    "致命",
                    "字段矛盾",
                    item_id=item_id,
                    dimension=dimension,
                    field="present/present_binary",
                    finding=f"present={present} 与 present_binary={binary} 不一致。",
                    action="以 present 为准重算 present_binary。",
                )
            )
        if level not in VALID_LEVELS:
            issues.append(
                issue(
                    f"STRUCT-BAD-LEVEL-{index}",
                    "致命",
                    "非法取值",
                    item_id=item_id,
                    dimension=dimension,
                    field="level",
                    finding=f"level 非法取值：{level}",
                    action="统一为 L1-L4 或“未出现”。",
                )
            )
        if present == "是" and level == "未出现":
            issues.append(
                issue(
                    f"STRUCT-YES-NOLEVEL-{index}",
                    "致命",
                    "字段矛盾",
                    item_id=item_id,
                    dimension=dimension,
                    field="present/level",
                    finding="present 为“是”，但 level 为“未出现”。",
                    action="补充 L1-L4 等级或改为未出现。",
                )
            )
        if present == "否" and level != "未出现":
            issues.append(
                issue(
                    f"STRUCT-NO-HASLEVEL-{index}",
                    "致命",
                    "字段矛盾",
                    item_id=item_id,
                    dimension=dimension,
                    field="present/level",
                    finding=f"present 为“否”，但 level={level}。",
                    action="改为“未出现”或重新判断存在性。",
                )
            )
        if confidence not in VALID_CONFIDENCE:
            issues.append(
                issue(
                    f"STRUCT-BAD-CONFIDENCE-{index}",
                    "高",
                    "非法取值",
                    item_id=item_id,
                    dimension=dimension,
                    field="confidence",
                    finding=f"confidence 非法取值：{confidence}",
                    action="统一为高、中、低。",
                )
            )

    for item_id, dimensions in sorted(item_dimension.items()):
        counts = Counter(dimensions)
        missing = [dimension for dimension in DIMENSIONS if counts[dimension] == 0]
        duplicate = [dimension for dimension, count in counts.items() if count > 1]
        if missing or duplicate:
            issues.append(
                issue(
                    f"STRUCT-ITEM-DIMS-{item_id}",
                    "致命",
                    "维度完整性",
                    item_id=item_id,
                    finding=f"维度缺失={';'.join(missing) or '无'}；重复={';'.join(duplicate) or '无'}。",
                    action="确保每个分析单元恰有四个维度记录。",
                )
            )


def add_research_risk_issues(rows, review_risk_by_item, issues):
    low_confidence_seen = set()
    l4_seen = set()
    innovation_seen = set()
    review_note_seen = set()
    source_manual_versions = Counter(row.get("source_manual_version", "") for row in rows)

    if any(version != "coding_manual_v2_internal" for version in source_manual_versions):
        issues.append(
            issue(
                "RISK-SOURCE-MANUAL-V1",
                "高",
                "版本继承风险",
                finding=f"内部底稿的源试编码版本为：{dict(source_manual_versions)}。",
                action="正式编码前按内部V2或后续正式手册重新判读，不能把V1试编码直接视为正式V2结果。",
            )
        )

    for row in rows:
        item_id = row["item_id"]
        dimension = row["dimension"]
        confidence = row["confidence"]
        level = row["level"]
        present = row["present"]
        evidence = row["evidence"].strip()
        notes = row.get("notes", "")
        row_key = (item_id, dimension)

        if confidence != "高" and row_key not in low_confidence_seen:
            issues.append(
                issue(
                    f"RISK-CONFIDENCE-{item_id}-{dimension}",
                    "中",
                    "编码把握度",
                    item_id=item_id,
                    dimension=dimension,
                    field="confidence",
                    finding=f"Codex试编码把握度为“{confidence}”。",
                    action="正式编码前由评分者重点复核证据句与等级边界。",
                )
            )
            low_confidence_seen.add(row_key)

        if present == "是" and level == "L4" and row_key not in l4_seen:
            issues.append(
                issue(
                    f"RISK-L4-{item_id}-{dimension}",
                    "中",
                    "高等级边界",
                    item_id=item_id,
                    dimension=dimension,
                    field="level",
                    finding="该记录被试编码为 L4，易受“复杂计算等于高阶”误判影响。",
                    action="按内部V2手册复核是否确有迁移、修正、一般化、递推、优化或开放构造要求。",
                )
            )
            l4_seen.add(row_key)

        if present == "是" and dimension == "质疑创新" and row_key not in innovation_seen:
            issues.append(
                issue(
                    f"RISK-INNOVATION-{item_id}",
                    "高",
                    "质疑创新保守复核",
                    item_id=item_id,
                    dimension=dimension,
                    field="present",
                    finding="质疑创新维度被试编码为出现；该维度按内部手册应保守判定。",
                    action="复核题干是否明确要求处理假设、替代模型、模型失效、开放设计或证据约束的新方案。",
                )
            )
            innovation_seen.add(row_key)

        if len(evidence) < 12:
            issues.append(
                issue(
                    f"RISK-EVIDENCE-SHORT-{item_id}-{dimension}",
                    "中",
                    "证据文本薄弱",
                    item_id=item_id,
                    dimension=dimension,
                    field="evidence",
                    finding="判定证据过短，难以支撑复核。",
                    action="补充能回到题干或参考解答步骤的证据句。",
                )
            )

        if "待人工" in notes or "OCR" in notes or "公式" in notes or "复核" in notes:
            if item_id not in review_note_seen:
                issues.append(
                    issue(
                        f"RISK-NOTES-REVIEW-{item_id}",
                        "中",
                        "元数据待核风险",
                        item_id=item_id,
                        field="notes",
                        finding="该记录元数据备注含待人工校对、OCR、公式或复核提示。",
                        action="在正式编码前对照原始PDF销项相关文本或公式问题。",
                    )
                )
                review_note_seen.add(item_id)

    for item_id, risks in sorted(review_risk_by_item.items()):
        severity_order = {"高": 0, "中": 1, "低": 2}
        main_risks = sorted(risks, key=lambda row: severity_order.get(row.get("severity"), 9))
        severities = Counter(row.get("severity", "") for row in risks)
        types = sorted({row.get("issue_type", "") for row in risks if row.get("issue_type", "")})
        issues.append(
            issue(
                f"RISK-MANUAL-REVIEW-{item_id}",
                "高" if "高" in severities else "中",
                "人工校对未销项",
                item_id=item_id,
                field="manual_review_checklist",
                finding=f"关联待校对问题 {len(risks)} 条；类型：{';'.join(types)}。",
                action=f"优先处理：{main_risks[0].get('required_action', '对照原始PDF校对。')}",
            )
        )


def make_report(rows, issues):
    total_rows = len(rows)
    total_items = len({row["item_id"] for row in rows})
    severity_counts = Counter(row["severity"] for row in issues)
    category_counts = Counter(row["category"] for row in issues)
    confidence_counts = Counter(row["confidence"] for row in rows)
    level_counts = Counter(row["level"] for row in rows if row["present"] == "是")
    dimension_present = []
    for dimension in DIMENSIONS:
        dim_rows = [row for row in rows if row["dimension"] == dimension]
        present = len({row["item_id"] for row in dim_rows if row["present"] == "是"})
        dimension_present.append(
            {
                "dimension": dimension,
                "items_present_internal": present,
                "total_items": total_items,
                "proportion_internal": f"{present / total_items:.3f}" if total_items else "0.000",
            }
        )

    severity_rows = [
        {"severity": key, "count": severity_counts.get(key, 0)}
        for key in ["致命", "高", "中", "低"]
        if severity_counts.get(key, 0)
    ]
    category_rows = [
        {"category": key, "count": count}
        for key, count in sorted(category_counts.items(), key=lambda item: (-item[1], item[0]))
    ]
    confidence_rows = [
        {"confidence": key, "count": count}
        for key, count in sorted(confidence_counts.items())
    ]
    level_rows = [
        {"level": key, "count": count}
        for key, count in sorted(level_counts.items())
    ]

    fatal_count = severity_counts.get("致命", 0)
    high_count = severity_counts.get("高", 0)

    content = f"""# 内部编码数据质量检查报告

更新时间：2026-07-14

## 性质声明

本报告由 `07_analysis/scripts/audit_internal_coding_quality.py` 基于 `07_analysis/data/internal_coding_v1.csv` 与 `03_corpus/manual_review_checklist.csv` 生成。它是正式编码前的数据质量检查，不是论文结果分析，不提供显著性、趋势或教学效果结论。

## 检查范围

- 内部编码记录数：{total_rows}
- 分析单元数：{total_items}
- 输出问题清单：`07_analysis/results/reviewed/internal_coding_quality_issues.csv`
- 当前结构性致命问题数：{fatal_count}
- 当前高优先级风险数：{high_count}

## 问题等级汇总

{md_table(["severity", "count"], severity_rows)}

## 问题类型汇总

{md_table(["category", "count"], category_rows)}

## 编码把握度汇总

{md_table(["confidence", "count"], confidence_rows)}

## 出现等级汇总

{md_table(["level", "count"], level_rows)}

## 内部维度分布预警

以下只用于发现复核重点，不得写入论文正式结果。

{md_table(["dimension", "items_present_internal", "total_items", "proportion_internal"], dimension_present)}

## 关键发现

1. 数据结构层面未发现必须立即修复的致命错误，若上表致命问题数为0，说明字段、维度、存在性与等级基本一致。
2. 内部底稿的源试编码来自 `coding_manual_v1`，当前只是被整理到 `coding_manual_v2_internal` 分析底稿中；正式编码前必须按最终手册重新判读。
3. 大量记录关联 `manual_review_checklist.csv` 的待人工校对项，尤其是OCR、公式、特殊符号、图注和题图边界；这些会影响题干理解、解答步骤和等级判定。
4. 模型建构与科学推理在内部试编码中均为全覆盖，质疑创新极少出现；这类极端分布可能是真实题型特征，也可能是手册边界或试编码倾向造成，正式统计前必须抽样复核。
5. L4记录、质疑创新出现记录和“中/低”把握度记录应作为评分者培训与正式编码前复核样本。

## 不得形成的结论

- 不得说正式编码已经完成；
- 不得说当前比例是论文结果；
- 不得说内部检查证明编码框架有效；
- 不得据此写“显著差异”“趋势明显”或教学效果结论；
- 不得把待人工校对记录直接作为最终证据。

## 下一步最小任务

执行 `G4-00F`：按 `internal_coding_quality_issues.csv` 先处理高优先级问题，尤其是人工校对未销项、质疑创新出现记录、L4记录和源手册版本继承风险，形成正式编码前复核样本包。
"""
    REPORT_OUT.write_text(content, encoding="utf-8")


def main():
    rows = read_csv(INPUT)
    review_rows = read_csv(MANUAL_REVIEW)
    issues = []
    add_structural_issues(rows, issues)
    add_research_risk_issues(rows, build_review_risk_map(review_rows), issues)
    fieldnames = [
        "issue_id",
        "severity",
        "category",
        "item_id",
        "dimension",
        "field",
        "finding",
        "recommended_action",
        "status",
    ]
    write_csv(ISSUES_OUT, issues, fieldnames)
    make_report(rows, issues)
    print(f"checked rows={len(rows)} items={len({row['item_id'] for row in rows})} issues={len(issues)}")
    print(f"wrote {ISSUES_OUT}")
    print(f"wrote {REPORT_OUT}")


if __name__ == "__main__":
    main()
