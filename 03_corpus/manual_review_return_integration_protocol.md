# G1-07-MANUAL-CLOSURE-RETURN-INTEGRATION-PROTOCOL 人工终核回填整合协议

更新时间：2026-07-19

## 性质声明

本协议规定真实人工终核回填文件收回之后，如何检查、判定、处理冲突、关闭条目和同步项目账本。它不填写真实校对人、真实校对日期、校对决定、分值、图号边界、专家意见、评分者记录、问卷结果、课堂结果或论文正文结论，也不关闭154项待核问题。

## 上游依据

- 动作计划：`03_corpus/manual_review_closure_action_plan_v1.csv`
- 动作计划QA：`03_corpus/manual_review_closure_action_plan_qa_v1.csv`
- 总索引：`03_corpus/manual_review_closure_packet_master_index_v1.csv`
- A/B/C/D回填包：`manual_review_a_closure_packet_v1.csv`、`manual_review_b_closure_packet_v1.csv`、`manual_review_c_closure_packet_v1.csv`、`manual_review_d_closure_packet_v1.csv`

## 整合流程

1. 回收登记：先保存真实回填副本，记录来源、回收人、组别和文件名，不覆盖原始空白包。
2. 结构检查：检查CSV编码、换行、表头、行数、`issue_id`集合和重复项。
3. 不可变字段检查：比对题号、届次、页码、材料ID、受影响小问和来源文件；无证据改动不得接受。
4. 字段完整性检查：按A/B/C/D各组必填字段逐项检查。
5. 证据位置检查：所有关闭候选必须有复核后证据位置；有修订时必须有修订摘要。
6. 冲突分级：按致命、重大、一般冲突登记，冲突未解决不得关闭。
7. 关闭候选判定：只有通过组别关闭条件的条目才能进入真实销项候选。
8. 整合QA：对关闭候选再次做集合、字段、证据和禁止声称边界检查。
9. 账本同步：按回填副本/整合日志、`manual_review_checklist.csv`、优先队列、销项计划、动作计划、总索引、项目状态和任务清单的顺序分批同步。
10. Git提交：一批一提交，只暂存本批整合文件和账本文件。

## A/B/C/D关闭门槛

| 组别 | 必填字段 | 关闭前必须证明 | 未满足时状态 |
|---|---|---|---|
| A | `actual_reviewer_or_code`、`actual_review_date`、`actual_review_decision`、`correction_required`、`correction_summary`、`post_review_evidence_location`、`post_review_status` | 题干OCR、答案公式、特殊符号、小问边界和证据摘录均通过或修订后通过 | 保持待核实，不能进入正式编码 |
| B | `actual_reviewer_or_code`、`actual_review_date`、`actual_review_decision`、`correction_required`、`correction_summary`、`post_review_evidence_location`、`post_review_status` | 关键公式、特殊符号、变量含义和答案边界均通过或修订后通过 | 保持待核实，不能作为公式支撑证据 |
| C | `actual_reviewer_or_code`、`actual_review_date`、`actual_review_decision`、`figure_usable_for_manuscript`、`redraw_required`、`correction_required`、`correction_summary`、`final_figure_file_or_evidence_location`、`post_review_status` | 图号、图注、关键标注、裁边、论文可用性或重绘决定均明确 | 不能进入案例图件、附录或论文定稿图 |
| D | `actual_reviewer_or_code`、`actual_review_date`、`actual_review_decision`、`official_score_source_or_fig_boundary_confirmed`、`score_value_or_fig_boundary_statement`、`correction_required`、`correction_summary`、`final_evidence_location`、`post_review_status` | 第35届分值来源或第42届第3题附属图边界有正式证据 | 不能进入分值统计或附属图件定稿 |

## 冲突处理

| 等级 | 典型情形 | 处理规则 |
|---|---|---|
| 致命 | `issue_id`错位、题号或年份无证据变化、证据文件缺失、真实校对人或日期缺失、第35届分值无来源、第42届第3题图件边界不清 | 不得关闭，退回补证或单独裁决 |
| 重大 | 修订摘要过粗、图件可用性和重绘决定矛盾、证据位置不够具体、关联问题未同步 | 暂缓关闭，补充说明后复查 |
| 一般 | 日期格式、校对人编码格式、路径书写或轻微格式问题但证据可定位 | 修正后复查，保留修正日志 |

## 同步更新顺序

1. 保留真实回填原始副本和整合日志。
2. 生成回填完整性检查表和冲突清单。
3. 对通过整合QA的条目，更新 `03_corpus/manual_review_checklist.csv`。
4. 同步更新 `manual_review_priority_followup.csv`、`manual_review_closure_plan_v1.csv`、`manual_review_closure_action_plan_v1.csv` 和总索引中的状态字段。
5. 只有A/B组相关条目达到正式编码门槛后，才允许另设任务准备正式评分者独立编码。
6. C/D未完成时，相关图件、附录和分值统计继续冻结。
7. `09_quality/claim_evidence_matrix.csv` 仍需单独任务处理，不能混入回填整合提交。
8. 正文修改必须另设任务，且只能使用已经关闭并可追溯的证据。

## 当前仍不能声称

- 不能声称154项人工终核已经完成。
- 不能声称题干、公式、题图、分值或参考解答已经正式校对。
- 不能进入正式编码、正式统计、正式案例结论或教学效果结论。
- 不能把内部转写、候选图、Codex视觉检查或本协议写成真实专家审查、真实评分者一致性或导师确认。

## 下一步最小任务

`G1-07-MANUAL-CLOSURE-RETURN-INTEGRATION-PROTOCOL-QA`：检查本协议是否覆盖回收登记、结构检查、A/B/C/D字段完整性、冲突分级、关闭条件、账本同步顺序、正文和主张矩阵隔离，以及CSV是否符合UTF-8 BOM和LF换行。

## 输出文件

- 协议说明：`03_corpus/manual_review_return_integration_protocol.md`
- 协议规则表：`03_corpus/manual_review_return_integration_protocol_v1.csv`
