# G1-07-MANUAL-CLOSURE-INTEGRATION-DRY-RUN 人工终核回填整合演练模板

更新时间：2026-07-19

## 性质声明

本文件建立真实人工终核回填文件收回前的空白整合演练模板，用来验证回收登记、结构检查、字段检查、冲突登记和账本同步是否能够落表执行。它不填写真实校对人、真实校对日期、校对决定、分值、图号边界、专家意见、评分者记录、问卷结果、课堂结果或论文正文结论，也不关闭154项待核问题。

## 上游依据

- 动作计划：`03_corpus/manual_review_closure_action_plan_v1.csv`
- 总索引：`03_corpus/manual_review_closure_packet_master_index_v1.csv`
- 回填整合协议：`03_corpus/manual_review_return_integration_protocol.md`
- 协议规则表：`03_corpus/manual_review_return_integration_protocol_v1.csv`
- 协议QA：`03_corpus/manual_review_return_integration_protocol_qa.md`

## 本轮输出

| 文件 | 行数 | 用途 |
|---|---:|---|
| `03_corpus/manual_review_return_integration_dry_run_template_v1.csv` | 154 | 逐项登记回填副本、结构检查、不可变字段检查、组别必填字段检查、证据位置检查、冲突登记、关闭候选和同步动作。 |
| `03_corpus/manual_review_return_integration_dry_run_protocol_steps_v1.csv` | 22 | 将 `RIP-01` 至 `RIP-22` 的协议规则转为可逐步勾验的演练步骤。 |

## 逐项模板覆盖

| 组别 | 项数 | 主要用途 |
|---|---:|---|
| A | 76 | 验证高风险题干OCR、公式与特殊符号回填后能否进入正式编码门槛检查。 |
| B | 22 | 验证中风险公式与特殊符号回填后能否作为公式支撑证据。 |
| C | 47 | 验证题图、图注、裁边和论文图件可用性回填后能否进入图件门槛检查。 |
| D | 9 | 验证第35届分值边界和第42届第3题附属图边界回填后能否进入附属证据门槛检查。 |

## 表格执行方式

1. 收到真实回填文件后，先另存副本，并在 `expected_return_copy_path` 与 `expected_return_file_name` 中登记。
2. 逐项填写 `return_copy_preserved_check`、`structure_check_status`、`immutable_fields_check_status` 和 `required_fields_check_status`。
3. 对证据位置、修订摘要和最终状态分别填写 `evidence_location_check_status`、`correction_summary_check_status` 和 `post_review_status_check`。
4. 出现冲突时，填写 `conflict_level`、`conflict_type`、`conflict_description` 和 `conflict_resolution_required`。
5. 只有真实回填和冲突处理全部通过后，后续任务才可把 `closure_candidate_after_dry_run` 从“否”改为关闭候选。
6. 本轮模板中的所有同步动作均保持“不执行：演练模板”，正式同步必须另设整合任务并单独提交。

## 当前仍不能声称

- 不能声称154项人工终核已经完成。
- 不能声称题干、公式、题图、分值或参考解答已经正式校对。
- 不能声称任何条目已经可以进入正式编码、正式统计、正式案例结论或论文定稿图件。
- 不能把本演练模板写成真实专家审查、真实评分者一致性、导师确认或课堂验证。
- 不能据此修改 `08_manuscript/` 正文或 `09_quality/claim_evidence_matrix.csv`。

## 下一步最小任务

`G1-07-MANUAL-CLOSURE-INTEGRATION-DRY-RUN-QA`：检查两张演练模板是否覆盖154项和22条协议规则，字段是否完整，CSV是否为UTF-8 BOM和LF换行，并确认所有真实回填、关闭、正式编码、正文使用和主张矩阵更新栏位仍处于未执行状态。
