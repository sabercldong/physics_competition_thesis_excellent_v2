#!/usr/bin/env python3
"""Build a label-blind, stratified V3 independent-coding package."""

from __future__ import annotations

import csv
import hashlib
import shutil
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "07_analysis/data/第35至42届科学思维V3唯一编码表.csv"
OUT = ROOT / "07_analysis/data/v3_independent_validation"
HANDOFF = OUT / "handoff_RATER-C"
AUTHOR_ONLY = OUT / "author_only"
SEED = "G8-82-V3-INDEPENDENT-BLIND-20260730"

DIMENSIONS = ("模型建构", "科学推理", "科学论证", "质疑创新")
REVIEW_FIELDS = (
    "independent_reviewer_id",
    "review_date",
    "review_present",
    "review_level",
    "question_evidence_quote",
    "solution_evidence_quote",
    "evidence_location",
    "adjacent_level_exclusion",
    "confidence",
    "reviewer_statement",
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def stable_rank(item_id: str) -> str:
    return hashlib.sha256(f"{SEED}|{item_id}".encode()).hexdigest()


def main() -> None:
    rows = read_csv(SOURCE)
    if len(rows) != 884:
        raise SystemExit(f"expected 884 source rows, found {len(rows)}")

    by_item: dict[str, dict[str, dict[str, str]]] = defaultdict(dict)
    for row in rows:
        by_item[row["item_id"]][row["dimension"]] = row
    if len(by_item) != 221:
        raise SystemExit(f"expected 221 analysis units, found {len(by_item)}")
    if any(set(dim_rows) != set(DIMENSIONS) for dim_rows in by_item.values()):
        raise SystemExit("one or more analysis units do not contain all four dimensions")

    argument_present = {
        item_id
        for item_id, dim_rows in by_item.items()
        if dim_rows["科学论证"]["present_label"] == "是"
    }
    innovation_present = {
        item_id
        for item_id, dim_rows in by_item.items()
        if dim_rows["质疑创新"]["present_label"] == "是"
    }
    model_absent = {
        item_id
        for item_id, dim_rows in by_item.items()
        if dim_rows["模型建构"]["present_label"] == "否"
    }
    reasoning_l1 = {
        item_id
        for item_id, dim_rows in by_item.items()
        if dim_rows["科学推理"]["level"] == "L1"
    }
    core = argument_present | innovation_present | model_absent | reasoning_l1
    if len(core) != 59:
        raise SystemExit(f"expected 59 boundary-focused units, found {len(core)}")

    regular: set[str] = set()
    for competition_no in [str(value) for value in range(35, 43)]:
        eligible = [
            item_id
            for item_id, dim_rows in by_item.items()
            if dim_rows["模型建构"]["competition_no"] == competition_no
            and item_id not in core
        ]
        eligible.sort(key=stable_rank)
        if len(eligible) < 2:
            raise SystemExit(f"edition {competition_no} has fewer than two eligible units")
        regular.update(eligible[:2])

    selected = core | regular
    if len(selected) != 75:
        raise SystemExit(f"expected 75 selected units, found {len(selected)}")

    if HANDOFF.exists():
        shutil.rmtree(HANDOFF)
    if AUTHOR_ONLY.exists():
        shutil.rmtree(AUTHOR_ONLY)
    (HANDOFF / "原题与参考解答").mkdir(parents=True)
    (HANDOFF / "编码规则").mkdir(parents=True)
    AUTHOR_ONLY.mkdir(parents=True)

    blind_rows: list[dict[str, str]] = []
    selection_rows: list[dict[str, str]] = []
    item_index_rows: list[dict[str, str]] = []

    for item_position, item_id in enumerate(sorted(selected), start=1):
        dim_rows = by_item[item_id]
        anchor = dim_rows["模型建构"]
        copied_source_names: list[str] = []
        for source_field in ("item_text_path", "solution_text_path"):
            rel_path = anchor[source_field]
            source_path = ROOT / rel_path
            if not source_path.is_file():
                raise SystemExit(f"missing source file: {rel_path}")
            target = HANDOFF / "原题与参考解答" / source_path.name
            if not target.exists():
                shutil.copy2(source_path, target)
            copied_source_names.append(target.name)

        item_index_rows.append(
            {
                "blind_unit_no": f"BU-{item_position:03d}",
                "item_id": item_id,
                "competition_no": anchor["competition_no"],
                "year": anchor["year"],
                "question_no": anchor["question_no"],
                "subquestion_no": anchor["subquestion_no"],
                "source_text_file": copied_source_names[0],
                "solution_text_file": copied_source_names[1],
            }
        )

        strata = []
        if item_id in argument_present:
            strata.append("科学论证正例")
        if item_id in innovation_present:
            strata.append("质疑创新正例")
        if item_id in model_absent:
            strata.append("模型建构未出现")
        if item_id in reasoning_l1:
            strata.append("科学推理L1")
        if item_id in regular:
            strata.append("各届常规补充")

        for dimension_position, dimension in enumerate(DIMENSIONS, start=1):
            source_row = dim_rows[dimension]
            blind_row = {
                "blind_row_id": f"BR-{item_position:03d}-{dimension_position}",
                "blind_unit_no": f"BU-{item_position:03d}",
                "item_id": item_id,
                "competition_no": source_row["competition_no"],
                "year": source_row["year"],
                "question_no": source_row["question_no"],
                "subquestion_no": source_row["subquestion_no"],
                "dimension": dimension,
                "source_text_file": copied_source_names[0],
                "solution_text_file": copied_source_names[1],
            }
            blind_row.update({field: "" for field in REVIEW_FIELDS})
            blind_rows.append(blind_row)

            selection_rows.append(
                {
                    "blind_row_id": blind_row["blind_row_id"],
                    "item_id": item_id,
                    "dimension": dimension,
                    "selection_stratum": "；".join(strata),
                    "v3_present_label": source_row["present_label"],
                    "v3_level": source_row["level"],
                    "source_review_row_id": source_row["review_row_id"],
                }
            )

    blind_fields = list(blind_rows[0])
    write_csv(HANDOFF / "第35至42届V3独立盲评编码表_75单元300行.csv", blind_rows, blind_fields)
    write_csv(HANDOFF / "独立盲评材料索引_75单元.csv", item_index_rows, list(item_index_rows[0]))
    write_csv(AUTHOR_ONLY / "独立盲评抽样与V3对照密钥_不得交评分者.csv", selection_rows, list(selection_rows[0]))

    for rel_path in (
        "04_framework/科学思维编码手册_V3.md",
        "04_framework/科学思维编码决策矩阵_V3.csv",
    ):
        source_path = ROOT / rel_path
        shutil.copy2(source_path, HANDOFF / "编码规则" / source_path.name)

    instructions = f"""# 第35至42届V3独立盲评操作指令

## 一、评分者资格

本包只能交给一名真实存在、此前未参与本项目候选编码、作者复核或裁决的人。建议其具备高中物理教学、物理竞赛教学或物理教育研究经历。作者本人、此前评分者、项目自动化工具和其他代理均不能充当本次独立评分者。

## 二、盲评要求

1. 评分者只能接收整个 `handoff_RATER-C` 文件夹，不得接收 `author_only` 文件夹。
2. 编码前不得查看项目中的V3候选表、唯一编码表、统计结果、既有复核表或案例标签。
3. 评分者须逐题阅读 `原题与参考解答` 中的材料，并依据 `编码规则` 独立填写空白表。
4. 不得使用自动生成工具代替个人判断，不得与作者讨论具体题目的现有标签。
5. 如证据不足，仍须填写所依据的原文位置，并在相邻等级排除栏写明不确定点；不得猜测题面、答案或评分标准。

## 三、抽样范围

空白表共75个分析单元、300行四维记录，占全样本221个分析单元的33.94%。抽样由程序完成，覆盖科学论证、质疑创新、模型建构未出现、科学推理L1等边界记录，并按第35至42届各补入常规单元。评分者不会看到任何抽样分层或V3标签。

## 四、逐行填写规则

- `independent_reviewer_id`：统一填写匿名代号，如 `RATER-C`；
- `review_date`：实际编码日期，格式 `YYYY-MM-DD`；
- `review_present`：只能填 `是` 或 `否`；
- `review_level`：出现时填 `L1`、`L2`、`L3`或`L4`，未出现时填 `未出现`；
- `question_evidence_quote`：填写能够支持判断的题干原文；
- `solution_evidence_quote`：填写参考解答中的关键原文；若题面已经足够，仍须说明解答核对结果；
- `evidence_location`：写明文件名、小问及可定位位置；
- `adjacent_level_exclusion`：出现时说明为何不取相邻等级，未出现时说明为何不进入该维度；
- `confidence`：只能填 `高`、`中`或`低`；
- `reviewer_statement`：每行填写同一声明：`本行为本人在未查看V3候选与最终标签的条件下独立判断。`

## 五、完成声明

评分者完成后须另附以下声明，不得由作者代写：

> 我声明：本文件由本人在未查看V3候选编码、作者复核结果和最终统计的条件下独立完成。本人逐题阅读了交接包中的题干、参考解答和编码规则，所有判断均为本人意见，未由自动生成工具或他人代填。
>
> 匿名评分者代号：
>
> 实际编码日期：
>
> 回填文件：

## 六、交回文件

只交回填写完成的 `第35至42届V3独立盲评编码表_75单元300行.csv` 和独立声明。不得改动前10个固定字段，不得增删行。项目接收后先做字段与证据QA，再与V3标签比较；比较结果不会反向覆盖原始回填文件。

抽样种子：`{SEED}`
"""
    instruction_path = HANDOFF / "独立盲评操作指令.md"
    instruction_path.write_text(instructions, encoding="utf-8")

    manifest_rows: list[dict[str, str]] = []
    for path in sorted(HANDOFF.rglob("*")):
        if path.is_file():
            manifest_rows.append(
                {
                    "relative_path": path.relative_to(HANDOFF).as_posix(),
                    "sha256": sha256(path),
                    "bytes": str(path.stat().st_size),
                }
            )
    write_csv(HANDOFF / "材料包清单与校验值.csv", manifest_rows, list(manifest_rows[0]))

    print(f"selected_units={len(selected)}")
    print(f"blind_rows={len(blind_rows)}")
    print(f"boundary_units={len(core)}")
    print(f"regular_supplement_units={len(regular)}")
    print(f"handoff={HANDOFF}")


if __name__ == "__main__":
    main()
