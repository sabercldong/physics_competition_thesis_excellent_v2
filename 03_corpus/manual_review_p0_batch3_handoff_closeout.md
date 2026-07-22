# P0第三批图件交接链收束

任务编号：`G1-07-FOLLOWUP-MANUAL-P0-BATCH3-HANDOFF-CLOSEOUT`

## 性质声明

本文件将P0第三批图件/SOLFIG边界入口、入口QA、逐项任务卡和任务卡QA收束为一页式交接链。它用于后续其他智能体或真实人工校对者领取任务、写回结果和触发回填整合。

本任务不填写真实校对人、日期、决定或最终证据位置，不关闭C组47项图件问题或 `CPHO42-Q03-SOLFIG`，不创建真实回填副本，不生成正式论文插图、正式编码、正式统计或论文结果章。

## 已收束材料

- 第三批入口：`03_corpus/manual_review_p0_batch3_figure_queue_v1.csv`，48项。
- 入口QA：`03_corpus/manual_review_p0_batch3_figure_queue_qa_v1.csv`，36项QA通过。
- 逐项任务卡：`03_corpus/manual_review_p0_batch3_task_cards_v1.csv`，48张。
- 任务卡QA：`03_corpus/manual_review_p0_batch3_task_cards_qa_v1.csv`，37项QA通过。
- 写回目标：C组47项写回 `03_corpus/manual_review_c_closure_packet_v1.csv` 或未来真实回填副本；`CPHO42-Q03-SOLFIG` 写回 `03_corpus/manual_review_d_closure_packet_v1.csv` 对应行或未来真实回填副本。
- 整合协议：`03_corpus/manual_review_return_integration_protocol_v1.csv`，22条规则。

## 领取顺序

1. 领取者先读本文件和结构化收束索引；
2. 按 `P0B3CARD-01` 至 `P0B3CARD-48` 逐项领取；
3. 每张卡只处理一个 `source_issue_id`；
4. 打开 `minimum_inputs_to_check` 的全部证据；
5. 将真实核对发现写回任务卡指定的 `handoff_target`；
6. 收到真实回填副本后，先走回收登记、结构检查、不可变字段检查、必填字段检查和整合QA；
7. 只有整合QA通过后，后续任务才可考虑更新人工校对主清单和正式编码输入。

## 当前仍不能声称

- 不能声称48张任务卡已经被真实领取或完成；
- 不能声称C组47项图件已经完成真实人工校对；
- 不能声称任何候选图已经成为正式论文插图定稿；
- 不能声称 `CPHO42-Q03-SOLFIG` 已替代 `CPHO42-Q03-FIG` 题面图终核；
- 不能创建或更新 `07_analysis/data/final_coding.csv`；
- 不能写论文结果章、图件定稿结论、专家意见、教师意见、问卷结果或课堂实验结论。

## 下一步最小任务

`G1-07-FOLLOWUP-MANUAL-P0-BATCH3-HANDOFF-CLOSEOUT-QA`：检查第三批交接链收束索引的输入存在性、行数编号、链条覆盖、路径可定位、状态边界和不放行边界。

## 输出文件

- 交接链说明：`03_corpus/manual_review_p0_batch3_handoff_closeout.md`
- 结构化收束索引：`03_corpus/manual_review_p0_batch3_handoff_closeout_v1.csv`
