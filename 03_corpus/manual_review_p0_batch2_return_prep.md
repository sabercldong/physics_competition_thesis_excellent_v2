# P0第二批公式与特殊符号回填入口

任务编号：`G1-07-FOLLOWUP-MANUAL-P0-BATCH2-RETURN-PREP`

## 性质声明

本文件为P0第二批中风险公式与特殊符号待核项建立真实回填入口。它只整理领取与回填位置，不执行真实校对，不填写真实校对结果。

本任务不填写真实校对人、校对日期、公式决定、修订位置、证据摘记、专家意见、导师意见、竞赛教师意见或评分者结果；不创建真实回填目录；不关闭任何人工校对项；不生成正式编码、正式统计、论文结果章或 `07_analysis/data/final_coding.csv`；不修改 `00_originals/`、题文原件、论文正文或主张证据矩阵。

## 当前覆盖

- 来源：`03_corpus/manual_review_priority_queue_v1.csv` 中 `recommended_batch=第二批` 的22条记录；

- 类型：公式与特殊符号校对；

- 优先级：均为P0，直接影响正式编码；

- 届次覆盖：第35届8题，第36届7题，第39届7题；

- 回填入口：`03_corpus/manual_review_p0_batch2_return_prep_v1.csv`。

## 使用方法

1. 从结构化表中领取一个 `return_id`；

2. 核对同一行的题目文本、题面页、答案页和公式核对表；

3. 只在真实核对后填写校对人、日期、已核页码、公式决定、修订位置、证据摘记和剩余疑点；

4. 若公式或特殊符号仍需修订或继续待核，必须写明阻断原因，不能允许进入正式评分者模板；

5. 收到真实回填副本后，仍需按既有接收协议做接收登记、结构检查、不可变字段检查和整合QA。

## 回填字段

结构化表预留真实回填字段：`reviewer_name`、`review_date`、`source_pages_checked`、`formula_decision`、`formula_revision_needed`、`revision_locations`、`evidence_note`、`remaining_uncertainty`、`allow_formal_rater_template`、`blocking_reason_if_not_allowed`、`files_to_update_after_return`、`return_file_path`、`return_checksum` 和 `integration_status`。当前这些字段均为空白或“未回填”。

## 禁止事项

- 不得把本入口写成P0第二批人工校对完成；

- 不得把公式核对入口写成真实人工结论；

- 不得跳过真实回填副本和整合QA，直接关闭待核项；

- 不得把内部编码复制成 `final_coding.csv`；

- 不得生成第四章正式统计、趋势、共现、显著性或教学效果结论。

## 下一最小任务

下一步建议执行 `G1-07-FOLLOWUP-MANUAL-P0-BATCH2-RETURN-PREP-QA`：检查P0第二批回填入口的来源筛选、字段结构、路径、空白回填字段、冻结状态和CSV格式。
