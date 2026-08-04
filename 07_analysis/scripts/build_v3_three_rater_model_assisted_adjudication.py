#!/usr/bin/env python3
"""Build a transparent, non-human candidate adjudication for 146 disagreements."""

from __future__ import annotations

import csv
import hashlib
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PACKET = (
    ROOT
    / "07_analysis/data/v3_independent_validation/adjudication"
    / "第三版RATER-F-G三方分歧裁决材料包_146行"
)
WORKLIST = PACKET / "三方分歧裁决工作表_146行_空白.csv"
MASTER = ROOT / "07_analysis/data/第35至42届科学思维第三版唯一编码表.csv"
OUT = (
    ROOT
    / "07_analysis/data/v3_independent_validation/adjudication"
    / "模型辅助候选裁决_146行_20260803"
)


# One decision per FGADJ row, in the exact order of the locked 146-row worklist.
# "未出现" means present=否; L1-L3 mean present=是.
DECISION_TEXT = """
未出现
L1
L2
L1
未出现
L2
L1
未出现
未出现
未出现
L1
L1
L2
未出现
未出现
L1
未出现
L3
L1
未出现
L2
未出现
未出现
未出现
L2
L1
L1
L1
未出现
L1
未出现
未出现
L1
L2
L1
L2
未出现
L2
未出现
L2
未出现
L2
L1
L1
未出现
未出现
未出现
未出现
未出现
L1
未出现
未出现
未出现
L2
L2
L3
L1
未出现
未出现
L2
L3
L2
L2
L2
L1
L2
L3
L2
L2
L2
L2
L3
L3
L3
L3
L1
L1
L1
L2
L1
L1
L1
L2
L1
L1
L3
L1
L1
L2
L2
L1
L1
L2
L2
L2
L3
L2
L1
L3
L2
L2
L3
L3
L3
L3
L2
L2
L1
L3
L3
L1
L1
L1
L3
L3
L2
L2
L2
L2
L2
L1
L2
L1
L2
L1
L3
L2
L3
L2
L1
L1
L3
L1
L1
L1
L2
L2
L2
L1
L2
L3
L2
L3
L1
L3
L2
"""


SPECIFIC_RULES = {
    "FGADJ-056": (
        "三器件并联拓扑、指定端口接触电阻约束和各支路共享的电流电压未知量必须联立，"
        "任一部分缺失都不能得到误差三次项，因而构成相互约束的统一电路模型，判为模型建构L3。"
    ),
    "FGADJ-132": (
        "先在强约束、低温条件下取得渐近表达式，再对数密度和原子流分别求峰值并保留温度的最低非零修正；"
        "其中包含近似边界和峰值优化，达到科学推理L3。"
    ),
}


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def write_csv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_label(row: dict[str, str], source: str) -> str:
    prefix = "第三版" if source == "第三版" else source
    present = row[f"{prefix}存在性"]
    level = row[f"{prefix}等级"]
    return "未出现" if present == "否" else level


def generic_rule(dimension: str, decision: str) -> str:
    if decision == "未出现":
        return {
            "模型建构": "本小问仅复用前问已建立的模型、进行参数代入或代数处理，没有新增情境到模型的必要映射。",
            "科学推理": "本小问仅含机械代入、同一公式的重排或纯数学处理，没有形成条件到新物理结论的必要推断。",
            "科学论证": "题面任务的结论是计算或推导的直接输出，缺少需要独立支持的主张及其证据—理由关系。",
            "质疑创新": "题面未要求评价局限、比较替代方案、修正模型或在非唯一约束下提出新方案。",
        }[dimension]
    if decision == "L1":
        return {
            "模型建构": "存在一个必要的情境—模型映射，但主要属于单一标准模型或单一关键映射。",
            "科学推理": "主要依据一条物理关系完成直接推断，后续代数或同一方法重复不构成第二条可区分关系。",
            "科学论证": "一条主要证据或理由直接支持一个明确主张，未比较两个以上条件或方案。",
            "质疑创新": "识别并说明一个具体局限，但未比较替代方案或提出受约束方案。",
        }[dimension]
    if decision == "L2":
        return {
            "模型建构": "至少两个可区分模型要素被协调，但尚未形成缺一不可、共享约束的统一耦合模型。",
            "科学推理": "至少两个可区分关系构成局部推理链，但未达到多条件相互约束、临界或优化结构的L3门槛。",
            "科学论证": "比较两个以上条件、情形或方案并说明结论差异，但未系统处理边界、误差、反例或适用性。",
            "质疑创新": "在明确约束下选择或提出可执行方案，但未针对失效条件修正或拓展模型。",
        }[dimension]
    if decision == "L3":
        return {
            "模型建构": "多个对象、阶段、边界或子模型共享变量并相互约束，构成缺一不可的统一模型。",
            "科学推理": "推理包含参数分区、临界判断、优化、多阶段互约束或完整因果结构，达到L3门槛。",
            "科学论证": "论证系统处理边界、误差、反例、关键假设或适用条件，达到L3门槛。",
            "质疑创新": "针对失效条件修正或拓展模型，并说明修正依据，达到L3门槛。",
        }[dimension]
    raise ValueError(f"Unsupported decision: {decision}")


def source_reason(row: dict[str, str], source: str) -> str:
    if source == "第三版":
        return row["第三版裁决理由"].strip()
    return row[f"{source}相邻等级排除"].strip()


def source_location(row: dict[str, str], source: str) -> str:
    if source == "第三版":
        return row["第三版证据位置"].strip()
    return row[f"{source}证据位置"].strip()


def main() -> None:
    decisions = [line.strip() for line in DECISION_TEXT.splitlines() if line.strip()]
    fields, rows = read_csv(WORKLIST)
    if len(rows) != 146 or len(decisions) != 146:
        raise SystemExit(f"Expected 146 rows/decisions, got {len(rows)}/{len(decisions)}")
    if len({row["裁决序号"] for row in rows}) != 146:
        raise SystemExit("Duplicate adjudication ids in locked worklist")

    candidate_rows: list[dict[str, str]] = []
    compact_rows: list[dict[str, str]] = []
    change_rows: list[dict[str, str]] = []
    source_counter: Counter[str] = Counter()
    for row, decision in zip(rows, decisions):
        matched = [
            source
            for source in ("第三版", "RATER-F", "RATER-G")
            if source_label(row, source) == decision
        ]
        if not matched:
            raise SystemExit(f"{row['裁决序号']} decision {decision} matches no source label")
        matched_reasons = [(source, source_reason(row, source)) for source in matched]
        chosen_source, chosen_reason = max(matched_reasons, key=lambda item: len(item[1]))
        locations = []
        for source in matched:
            location = source_location(row, source)
            if location and location not in locations:
                locations.append(location)
        source_key = "+".join(matched)
        source_counter[source_key] += 1

        present = "否" if decision == "未出现" else "是"
        basis = (
            f"{SPECIFIC_RULES.get(row['裁决序号'], generic_rule(row['维度'], decision))} "
            f"匹配标签来源：{source_key}。其中较完整的既有边界理由为：{chosen_reason}"
        )
        # No row is marked high because this pass reviewed packet excerpts rather
        # than reopening every full source file. Consensus only raises low to medium.
        confidence = "中" if len(matched) >= 2 else "低"
        pending = (
            "无需新增材料；待研究者核对原文并确认"
            if len(matched) >= 2
            else "无需新增材料；该项为少数标签选择，待研究者重点核对原文并确认"
        )
        filled = dict(row)
        filled.update(
            {
                "是否已核对原文": "否（仅核对材料包清晰证据摘录）",
                "裁决后存在性": present,
                "裁决后等级": decision,
                "裁决依据": basis,
                "复核后证据位置": "；".join(locations),
                "裁决置信度": confidence,
                "待补材料": pending,
                "裁决状态": "模型辅助候选，待研究者确认",
            }
        )
        candidate_rows.append(filled)

        compact = {
            "裁决序号": row["裁决序号"],
            "第三版源记录": row["第三版源记录"],
            "blind_row_id": row["blind_row_id"],
            "item_id": row["item_id"],
            "维度": row["维度"],
            "分歧类型": row["分歧类型"],
            "第三版标签": source_label(row, "第三版"),
            "RATER-F标签": source_label(row, "RATER-F"),
            "RATER-G标签": source_label(row, "RATER-G"),
            "候选裁决标签": decision,
            "候选裁决存在性": present,
            "匹配标签来源": source_key,
            "采用的详细理由来源": chosen_source,
            "候选裁决置信度": confidence,
            "研究者确认状态": "待确认",
        }
        compact_rows.append(compact)
        if compact["第三版标签"] != decision:
            change_rows.append(compact)

    OUT.mkdir(parents=True, exist_ok=True)
    candidate_path = OUT / "三方分歧模型辅助候选裁决表_146行_待研究者确认.csv"
    compact_path = OUT / "候选裁决标签清单_146行.csv"
    change_path = OUT / "相对第三版候选变更清单.csv"
    write_csv(candidate_path, fields, candidate_rows)
    compact_fields = list(compact_rows[0])
    write_csv(compact_path, compact_fields, compact_rows)
    write_csv(change_path, compact_fields, change_rows)

    master_fields, master_rows = read_csv(MASTER)
    master_by_id = {row["review_row_id"]: row for row in master_rows}
    if len(master_rows) != 884 or len(master_by_id) != 884:
        raise SystemExit("Master data is not the locked 884-row unique table")
    before = defaultdict(Counter)
    after = defaultdict(Counter)
    for row in master_rows:
        before[row["dimension"]][row["level"]] += 1
        after[row["dimension"]][row["level"]] += 1
    for row in compact_rows:
        source_id = row["第三版源记录"]
        if source_id not in master_by_id:
            raise SystemExit(f"Missing master id: {source_id}")
        master_row = master_by_id[source_id]
        old = master_row["level"]
        new = row["候选裁决标签"]
        if old != row["第三版标签"]:
            raise SystemExit(f"Locked V3 label mismatch: {source_id}")
        if old != new:
            after[master_row["dimension"]][old] -= 1
            after[master_row["dimension"]][new] += 1

    level_order = ["未出现", "L1", "L2", "L3", "L4"]
    sensitivity_rows = []
    for dimension in ("模型建构", "科学推理", "科学论证", "质疑创新"):
        for level in level_order:
            old = before[dimension][level]
            new = after[dimension][level]
            sensitivity_rows.append(
                {
                    "维度": dimension,
                    "等级": level,
                    "第三版正式数量": old,
                    "若采纳全部候选裁决的数量": new,
                    "变化量": new - old,
                    "说明": "仅为敏感性模拟，不改正式数据或论文结果",
                }
            )
    sensitivity_path = OUT / "若采纳全部候选裁决的884行统计敏感性分析.csv"
    write_csv(sensitivity_path, list(sensitivity_rows[0]), sensitivity_rows)

    qa_rows = [
        {"检查项": "锁定工作表行数", "结果": "通过", "实测": len(rows), "期望": 146},
        {"检查项": "候选决策行数", "结果": "通过", "实测": len(decisions), "期望": 146},
        {"检查项": "候选标签均匹配至少一个既有标签", "结果": "通过", "实测": 146, "期望": 146},
        {"检查项": "正式主表只读读取行数", "结果": "通过", "实测": len(master_rows), "期望": 884},
        {"检查项": "相对第三版发生变化的候选数", "结果": "信息", "实测": len(change_rows), "期望": "不预设"},
        {"检查项": "正式主表写入", "结果": "通过", "实测": 0, "期望": 0},
        {"检查项": "候选状态统一为待研究者确认", "结果": "通过", "实测": sum(r["裁决状态"] == "模型辅助候选，待研究者确认" for r in candidate_rows), "期望": 146},
    ]
    qa_path = OUT / "候选裁决程序QA.csv"
    write_csv(qa_path, list(qa_rows[0]), qa_rows)

    summary_path = OUT / "候选裁决汇总.md"
    dimension_decisions = defaultdict(Counter)
    for row in compact_rows:
        dimension_decisions[row["维度"]][row["候选裁决标签"]] += 1
    summary_lines = [
        "# 第三版与RATER-F、RATER-G三方分歧模型辅助候选裁决汇总",
        "",
        "> 本目录不是人工裁决成品。146条结果为模型辅助候选，必须由研究者核对原题、参考解答和编码手册后确认，方可进入正式数据。",
        "",
        f"- 候选裁决：{len(compact_rows)}条。",
        f"- 相对第三版拟变更：{len(change_rows)}条。",
        f"- 相对第三版拟保持：{len(compact_rows) - len(change_rows)}条。",
        f"- 存在性分歧：{sum(r['分歧类型'] == '存在性分歧' for r in compact_rows)}条。",
        f"- 等级分歧：{sum(r['分歧类型'] == '等级分歧' for r in compact_rows)}条。",
        "- 正式884行主表、论文统计和正文：均未修改。",
        "",
        "## 候选标签分布",
        "",
        "| 维度 | 未出现 | L1 | L2 | L3 |",
        "|---|---:|---:|---:|---:|",
    ]
    for dimension in ("模型建构", "科学推理", "科学论证", "质疑创新"):
        counts = dimension_decisions[dimension]
        summary_lines.append(
            f"| {dimension} | {counts['未出现']} | {counts['L1']} | {counts['L2']} | {counts['L3']} |"
        )
    summary_lines.extend(
        [
            "",
            "## 使用顺序",
            "",
            "1. 先看 `相对第三版候选变更清单.csv`，集中核对拟改码记录。",
            "2. 再看146行完整候选裁决表中的清晰题干证据、解答证据和三方理由。",
            "3. 研究者逐条填写确认结果；在确认完成前，不更新884行主表和论文统计。",
            "",
            "## 证据状态",
            "",
            "本轮核对了材料包内的清晰证据摘录和三方边界理由，没有逐一回到43份完整题目文件核对上下文，因此 `是否已核对原文` 统一如实填写为否。少数标签选择尤其需要研究者优先复核。",
            "",
        ]
    )
    summary_path.write_text("\n".join(summary_lines), encoding="utf-8")

    manifest_rows = []
    for path in sorted(OUT.iterdir()):
        if path.is_file() and path.name != "生成文件与校验值.csv":
            manifest_rows.append(
                {
                    "文件名": path.name,
                    "SHA-256": sha256(path),
                    "字节数": path.stat().st_size,
                }
            )
    write_csv(OUT / "生成文件与校验值.csv", list(manifest_rows[0]), manifest_rows)

    print(f"candidate_rows={len(candidate_rows)}")
    print(f"changed_vs_v3={len(change_rows)}")
    print(f"output={OUT}")
    print(f"sources={dict(source_counter)}")


if __name__ == "__main__":
    main()
