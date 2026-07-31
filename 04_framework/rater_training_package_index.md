# G3-04-QA 评分者培训包索引

更新时间：2026-07-14

> 状态：培训包 QA 索引。本文用于检查评分者培训材料是否齐备、是否与正式编码模板字段对齐。当前尚未完成真实评分者独立编码、分歧裁决或一致性检验。

## 一、包内文件

| 顺序 | 文件 | 用途 | QA状态 | 使用边界 |
|---:|---|---|---|---|
| 1 | `04_framework/analysis_unit_and_coding_definitions_formal_draft.md` | 分析单位、纳入排除、四维度定义和 L1-L4 等级草案 | 已纳入培训包 | 正式草案，不是冻结版手册 |
| 2 | `04_framework/codebook_v2_formal_draft.csv` | 16个维度-等级指标定义 | 已纳入培训包 | 待真实评分者试用和导师确认 |
| 3 | `04_framework/rater_training_manual_formal_draft.md` | 评分者阅读顺序、字段填写、停止条件和分歧处理提醒 | 已纳入培训包 | 培训候选稿，不代表评分者意见 |
| 4 | `04_framework/boundary_case_bank_formal_draft.csv` | 16个边界训练案例 | 已纳入培训包 | 训练风险清单，不是标准答案库 |
| 5 | `04_framework/evidence_note_and_disagreement_protocol_formal_draft.md` | 证据摘记、把握度、分歧类型和正式统计入口规则 | 已纳入培训包 | 协议草案，不代表已裁决 |
| 6 | `07_analysis/data/formal_coding_rater_A_template.csv` | 评分者A正式空白编码模板 | 已对齐字段 | 空白模板，尚未填写 |
| 7 | `07_analysis/data/formal_coding_rater_B_template.csv` | 评分者B正式空白编码模板 | 已对齐字段 | 空白模板，尚未填写 |
| 8 | `07_analysis/data/formal_adjudication_template.csv` | 分歧裁决模板 | 已对齐字段 | 空白模板，需A/B编码后使用 |
| 9 | `04_framework/rater_training_return_checklist.csv` | 回收培训和编码材料时逐项核对 | 新增 | 只作回收检查，不产生研究结果 |
| 10 | `04_framework/rater_training_field_alignment_audit.csv` | 字段对齐审计 | 新增 | 只作QA记录 |

## 二、交接前最低条件

评分者培训包可以交接，但必须同时说明以下边界：

- 该包不是正式编码结果；
- A/B 评分者模板仍为空白；
- 裁决模板仍为空白；
- `03_corpus/manual_review_checklist.csv` 中仍有待销项问题；
- 内部预演、Codex模拟编码和边界案例不能复制为评分者结果；
- 正式论文结果必须等待真实评分者独立编码、分歧裁决和唯一分析表。

## 三、回收时最低检查

回收评分者材料时必须检查：

1. 评分者A/B模板记录数是否仍为876条；
2. `present` 是否只含“是/否”；
3. `level` 是否只含 L1-L4 或“未出现”；
4. `evidence` 是否非空且可定位；
5. `confidence` 是否只含“高/中/低”；
6. `coder_id`、`coding_date`、`manual_version` 是否填写；
7. `notes` 是否标出待核实材料问题；
8. 是否存在复制内部预演或训练案例结论的迹象。

不满足以上条件时，不进入一致性计算。

