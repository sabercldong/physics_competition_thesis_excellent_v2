# R01 G3 分析框架生命周期状态对账（2026-07-25）

## 目的与核验范围

本对账处理 `TASKS.md` 中 G3 分析框架任务仍以“草案/待完成”描述、而后续 R01 已使用相关规则完成回填、登记、一致性计算、裁决和更正的状态差异。它仅核验项目内文件、行数、字段结构和可复跑输出的相互对应；不会把任何人工自声明升级为身份、互盲、独立过程或外部效度的独立证明。

## 对账结果

| 原任务 | 当前项目内状态 | 可复核依据 | 未闭合边界 |
|---|---|---|---|
| G3-01 分析单位与排除规则 | 已形成并用于当前 219 个分析单元的项目内操作规则 | `04_framework/analysis_unit_and_coding_definitions_formal_draft.md`；`03_corpus/item_index.csv` | 文本/公式人工终核与外部方法审查不由此证明 |
| G3-02 四维操作定义 | 草案与内部 V2 规则均已进入 R01 编码输入 | `04_framework/codebook_v2_formal_draft.csv`；`coding_manual_v2_internal.md`；R01 回填登记 | 不证明四维度的构念效度或专家共识 |
| G3-03 SOLO 启发等级 | L1--L4 已按“任务认知结构要求”用于编码，且未等同学生学习结果 | `analysis_unit_and_coding_definitions_formal_draft.md`；`02_literature/solo_original_fulltext_reading_notes_20260725.md` | 原典仅限关键章节阅读；1989 论文、理论取舍与外部效度未闭合 |
| G3-04 手册、正反例与分歧规则 | 培训候选稿、边界案例、证据/分歧协议和内部 V2 均存在，并与字段回收检查对应 | `04_framework/rater_training_manual_formal_draft.md`；`boundary_case_bank_formal_draft.csv`；`evidence_note_and_disagreement_protocol_formal_draft.md` | 仍不是经专家审查和导师确认的正式手册 |
| G3-05 专家审查 | 仅完成材料包与内部预审准备，未收到真实专家审查记录 | `04_framework/expert_review_packet.md`；`expert_panel_template.csv`；`codex_internal_pre_review_report.md` | 不得把 Codex 内部预审、统计或人工声明写成专家意见 |
| G3-06 双评分者编码 | 两份各 876 条的 RATER-A/B 回填已接收、登记且字段检查通过 | `07_analysis/data/rater_returns/incoming/R01/`；`r01_rater_return_intake_check.md` | 项目不能独立验证评分者身份、互盲、独立填写或实际人工过程 |
| G3-07 一致性与裁决 | 对登记的 876 对记录已复算一致性；142 条分歧已进入 ADJ-01 裁决，后有 ADJ-02 四条更正 | `r01_rater_reliability_report.md`；`r01_adjudication_return_intake_check.md`；`final_coding_r01_correction_v1.csv` | 数值不构成框架效度、专家认可或独立过程验证 |
| G3-08 正式手册冻结 | 未完成；当前仅有内部 V2 与 R01 输入版本冻结 | `04_framework/coding_manual_v2_internal.md`；`04_framework/r01_formal_coding_input_freeze.md` | 仍需真实可核验的专家/导师审查、理论取舍和正式版本确认 |

## 当前允许的项目内表述

1. 可以说：项目已归档两份 R01 编码回填、其字段检查、一致性计算、裁决和更正后的唯一分析表；对应记录可在项目内复算。
2. 可以说：当前四维与 L1--L4 是用于本语料任务要求分析的操作规则；SOLO只作受限启发，不等同学生真实学习结果。
3. 不可以说：编码手册已获专家或导师确认、评分者身份与独立性已由项目验证、统计量证明框架有效，或这些编码结论可外推为学生能力、教学效果、因果或显著性结论。

## 对任务状态的处理

本文件不追溯性地将 G3-01 至 G3-04 改写成“正式完成”，也不关闭 G3-05 或 G3-08。`TASKS.md` 的更新只补充后续 R01 实际使用和项目内可复算的状态；正式方法确认仍需外部、可归档的审查材料。

## 最小后续动作

若研究需要将编码框架提升为正式方法结论，应先取得真实专家或导师审查的匿名化反馈、日期、版本、采纳/未采纳理由和手册修订记录；同时明确 SOLO 原典理论取舍。若无法取得这些材料，应保持当前为“R01 项目内可复算操作规则”，并在论文方法与局限中如实限定。

## 复跑入口

```bash
python3 07_analysis/scripts/validate_r01_g3_framework_lifecycle_reconciliation.py
python3 07_analysis/scripts/compute_reliability.py
python3 07_analysis/scripts/validate_r01_results_eligibility.py
```
