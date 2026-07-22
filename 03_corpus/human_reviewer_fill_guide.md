# 人工复核者填写指南

更新时间：2026-07-22

## 先选你要做的事

本指南只适用于你本人或其他真实人员已经逐页看过原始题面、答案或图件之后的回填。若由智能体完成，只能写为“智能体内部复核”，不得使用本指南的人工回填声明。

| 你核对的内容 | 复制并填写的源文件 | 只填这些字段 |
|---|---|---|
| A组：题干OCR、公式 | `03_corpus/manual_review_a_closure_packet_v1.csv` | `actual_reviewer_or_code`、`actual_review_date`、`actual_review_decision`、`correction_required`、`correction_summary`、`post_review_evidence_location`、`post_review_status` |
| B组：公式、特殊符号 | `03_corpus/manual_review_b_closure_packet_v1.csv` | `actual_reviewer_or_code`、`actual_review_date`、`actual_review_decision`、`correction_required`、`correction_summary`、`post_review_evidence_location`、`post_review_status` |
| C组：图号、图注、裁边、重绘 | `03_corpus/manual_review_c_closure_packet_v1.csv` | `actual_reviewer_or_code`、`actual_review_date`、`actual_review_decision`、`figure_usable_for_manuscript`、`redraw_required`、`correction_required`、`correction_summary`、`final_figure_file_or_evidence_location`、`post_review_status` |
| D组：分值、附属图边界 | `03_corpus/manual_review_d_closure_packet_v1.csv` | `actual_reviewer_or_code`、`actual_review_date`、`actual_review_decision`、`official_score_source_or_fig_boundary_confirmed`、`score_value_or_fig_boundary_statement`、`correction_required`、`correction_summary`、`final_evidence_location`、`post_review_status` |

最推荐先做A组。不要直接修改原包；先复制一份再填写。首批38个题目级材料包、原PDF页和任务范围见 `03_corpus/manual_review_real_return_priority_packet.md`。

## 每一行怎样填

| 字段 | 填写要求 | 示例 |
|---|---|---|
| `actual_reviewer_or_code` | 你的匿名代号；同一人始终一致，不写真实姓名 | `R01` |
| `actual_review_date` | 你实际核对该行的日期，格式为`YYYY-MM-DD` | `2026-07-22` |
| `actual_review_decision` | 只从该行` suggested_decision_options`给出的选项中选择 | `与原PDF一致` |
| `correction_required` | 仅填“是”或“否” | `是` |
| `correction_summary` | 只写你实际观察到的差异；没有差异可写“未发现需修正处” | `答案第12页分母指数应为2，当前转写为3` |
| 证据位置字段 | 写原始文件名和PDF页码，必要时补截图路径 | `cpho_41_2024_fusai_paper_solution_candidate.pdf，第2页；答案第9页` |
| `post_review_status` | 只写实际状态，如“已人工复核，待接收QA”；不要写“正式放行” | `已人工复核，待接收QA` |

C组额外规则：`figure_usable_for_manuscript`和`redraw_required`只填“是”或“否”。D组额外规则：必须注明你实际看到的评分标准来源页或图件边界来源；没有来源不要猜测分值。

## 人工回填声明

在提交副本时附上一段单独文字：

```text
我声明：此副本由我本人独立人工核对完成。
匿名复核代号：R01
实际复核日期：YYYY-MM-DD
核对材料：填写实际看过的原始题面、答案或图件文件。
未将其他评分者或智能体的判断冒充为本人复核结论。
```

该声明用于记录来源，不要求公开真实姓名。它不自动关闭任何问题，后续仍要经过接收、结构检查和整合QA。

## 保存与交付

1. 保留原始空白包不动；把填写后的副本命名为：`return_YYYYMMDD_{A|B|C|D}_{Rxx}_filled.csv`。
2. 实际填写完成后，告诉我副本路径和匿名代号；我会创建接收目录、计算SHA-256、填写接收登记，并做结构检查。
3. 不要自己填写以下接收或放行字段：`sha256`、`file_size_bytes`、`intake_date`、`received_by`、`structure_check_status`、`field_completeness_status`、`conflict_status`、`release_status`、`formal_coding_release`、`formal_statistics_release`、`manuscript_use_release`、`claim_matrix_update_release`。
4. 只填写你亲自看过的行。未看的行保持空白；不确定时写入修订说明并标记“待核实”。

## 正式双评分者编码是另一件事

人工终核完成并冻结输入后，才分别由两位真实评分者独立填写：

- A评分者：`07_analysis/data/formal_coding_rater_A_template.csv`
- B评分者：`07_analysis/data/formal_coding_rater_B_template.csv`

每位评分者只填自己的模板中的`present`、`level`、`evidence`、`confidence`、`coder_id`、`coding_date`、`manual_version`和`notes`。填写规则见 `04_framework/rater_independent_coding_instructions_v1.md`。两人提交前不得互看，不能由同一人同时充当A和B。

