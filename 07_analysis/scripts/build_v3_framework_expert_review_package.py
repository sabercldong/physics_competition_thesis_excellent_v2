#!/usr/bin/env python3
"""Build a two-expert content-validity review package for the V3 framework."""

from __future__ import annotations

import csv
import hashlib
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MATRIX = ROOT / "04_framework/科学思维编码决策矩阵_V3.csv"
MANUAL = ROOT / "04_framework/科学思维编码手册_V3.md"
OUT = ROOT / "07_analysis/data/v3_framework_expert_review/handoff_EXPERTS"

REVIEW_FIELDS = (
    "expert_id",
    "review_date",
    "relevance_1_4",
    "clarity_1_4",
    "dimension_level_separation_1_4",
    "operability_1_4",
    "review_decision",
    "suggested_revision",
    "physics_example_or_counterexample",
    "expert_statement",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    with MATRIX.open("r", encoding="utf-8-sig", newline="") as handle:
        source_rows = list(csv.DictReader(handle))
    if len(source_rows) != 20:
        raise SystemExit(f"expected 20 decision rows, found {len(source_rows)}")

    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    shutil.copy2(MANUAL, OUT / MANUAL.name)
    shutil.copy2(MATRIX, OUT / MATRIX.name)

    rows: list[dict[str, str]] = []
    for index, source_row in enumerate(source_rows, start=1):
        row = {"review_item_id": f"CV-{index:02d}", **source_row}
        row.update({field: "" for field in REVIEW_FIELDS})
        rows.append(row)

    form = OUT / "V3框架专家内容效度审查表_20项.csv"
    with form.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    instructions = """# V3框架专家内容效度审查指令

## 一、审查人员

请由两名真实存在的专家分别完成独立副本。专家建议具有物理课程与教学论、物理教育研究、高中物理教学或物理竞赛教学经历。两名专家在提交前不得交换逐项评分和修改意见。

每名专家各自复制 `V3框架专家内容效度审查表_20项.csv`，分别命名为：

- `V3框架专家内容效度审查表_EXPERT-01_已完成.csv`
- `V3框架专家内容效度审查表_EXPERT-02_已完成.csv`

## 二、四项评分

每项均使用1至4分，不设中间值：

- `relevance_1_4`：该规则与相应科学思维维度/等级的相关性；
- `clarity_1_4`：表述是否清楚、不会产生两种明显不同解释；
- `dimension_level_separation_1_4`：是否能区分“维度存在性”和“维度内部等级”；
- `operability_1_4`：能否依据题干和参考解答稳定实施。

分值含义：

- 1：不相关或不可用；
- 2：需重大修改；
- 3：基本适用，需小幅修改；
- 4：清楚且适用。

## 三、必须填写的实质字段

- `review_decision`：只能填 `接受`、`修改后接受`或`删除/重建`；
- `suggested_revision`：接受时也要写明是否需要措辞微调；
- `physics_example_or_counterexample`：至少给出一个能够检验该规则的物理任务例子或反例；
- `expert_statement`：统一填写 `本项为本人独立审查意见，提交前未查看另一专家评分。`

不得只给总评，不得由作者代写示例或修改建议。

## 四、重点审查问题

1. 模型建构是否与“使用已经给定的模型”区分清楚；
2. 科学推理最低门槛是否过宽，能否识别直接读数、定义复述和机械代入等负例；
3. 科学论证是否与一般物理推导区分清楚；
4. 质疑创新是否与题材新颖、复杂计算和模型建构L4区分清楚；
5. L1至L4是否描述维度内部结构，而不是重新决定维度类型；
6. L4的迁移、修正和构造是否造成维度轴与等级轴循环；
7. 当前规则能否用于复赛小问，而不会把分值、公式数量或答案长度当作等级依据。

## 五、完成声明

每名专家另附以下声明：

> 我声明：本文件由本人依据V3编码手册、决策矩阵和本人专业判断独立完成。提交前未查看另一专家的逐项评分，未由作者或自动生成工具代填。
>
> 专家代号：
>
> 专业背景：
>
> 实际审查日期：
>
> 回填文件：

项目回收后先核对40项专家记录的字段与独立声明，再计算条目内容效度指数和全表平均内容效度指数。未真实回收前不得在论文中写入专家人数、评分或效度结论。
"""
    (OUT / "V3框架专家内容效度审查指令.md").write_text(instructions, encoding="utf-8")

    manifest = [
        {
            "file": path.name,
            "sha256": sha256(path),
            "bytes": str(path.stat().st_size),
        }
        for path in sorted(OUT.iterdir())
        if path.is_file()
    ]
    with (OUT / "材料包清单与校验值.csv").open(
        "w", encoding="utf-8-sig", newline=""
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=["file", "sha256", "bytes"])
        writer.writeheader()
        writer.writerows(manifest)

    print(f"review_items={len(rows)}")
    print(f"experts_required=2")
    print(f"handoff={OUT}")


if __name__ == "__main__":
    main()
