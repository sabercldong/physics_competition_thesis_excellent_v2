# 内部描述统计准备说明

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

- 分析单元数：219
- 编码记录数：876
- 每个分析单元维度数：4
- 手册版本：`coding_manual_v2_internal`
- 数据版本：`internal_v1_codex_pilot`

## 字段检查

- `item_index.csv` 与 `pilot_coding.csv` 的 `item_id` 已完成内部匹配；
- 每个 `item_id` 均有四个维度记录；
- 输出数据表为 `07_analysis/data/internal_coding_v1.csv`；
- 生成表保存于 `07_analysis/results/generated/`，该目录为可复现输出，不纳入提交对象。

## 维度出现预演表

| dimension | items_present | total_items | proportion |
| --- | --- | --- | --- |
| 模型建构 | 219 | 219 | 1.000 |
| 科学推理 | 219 | 219 | 1.000 |
| 科学论证 | 147 | 219 | 0.671 |
| 质疑创新 | 7 | 219 | 0.032 |

## 维度共现预演表

| dimension_pair | items_present_together | total_items | proportion |
| --- | --- | --- | --- |
| 模型建构+科学推理 | 219 | 219 | 1.000 |
| 模型建构+科学论证 | 147 | 219 | 0.671 |
| 模型建构+质疑创新 | 7 | 219 | 0.032 |
| 科学推理+科学论证 | 147 | 219 | 0.671 |
| 科学推理+质疑创新 | 7 | 219 | 0.032 |
| 科学论证+质疑创新 | 7 | 219 | 0.032 |

## 当前致命边界

- `03_corpus/manual_review_checklist.csv` 中仍有待核项，OCR、公式、图注和题图边界尚未全部人工销项；
- 尚未完成真实专家审查或导师确认；
- 尚未完成两名真实评分者独立编码；
- 尚未完成真实分歧裁决；
- 当前输出不能作为正式结果章、摘要或结论依据。

## 下一步最小任务

在不写论文正文的前提下，建议先执行 `G4-00R`：检查 `internal_coding_v1.csv` 的字段完整性、异常值、维度分布极端项和证据文本缺口，形成正式编码前的数据质量问题清单。
