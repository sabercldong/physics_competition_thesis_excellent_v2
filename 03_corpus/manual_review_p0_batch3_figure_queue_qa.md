# P0第三批图件任务入口QA

任务编号：`G1-07-FOLLOWUP-MANUAL-P0-BATCH3-FIGURE-QUEUE-QA`

## 性质声明

本文件检查 `03_corpus/manual_review_p0_batch3_figure_queue.md` 和 `03_corpus/manual_review_p0_batch3_figure_queue_v1.csv` 是否正确建立P0第三批图件类领取入口。QA通过只表示入口结构可靠，不表示真实人工校对完成。

## QA结论

通过。第三批入口CSV共48项，编号 `P0B3FIG-01` 至 `P0B3FIG-48` 连续唯一，覆盖C组47项题图裁边与图注问题，以及第42届第3题 `CPHO42-Q03-SOLFIG` 解答放大图边界问题。

## 已确认事项

- 第三批入口CSV为UTF-8 BOM，LF换行。
- 48项均保持“待领取：未真实回填”和“不放行”。
- 引用路径缺失0项。
- C组47项与 `manual_review_c_closure_packet_v1.csv` 的 `issue_id` 集合一致。
- `CPHO42-Q03-SOLFIG` 只作为解答放大图和题面/题解图命名边界任务，不替代 `CPHO42-Q03-FIG` 的题面图终核。
- `03_corpus/manual_review_returns/` 当前不存在。
- `07_analysis/data/final_coding.csv` 当前不存在。

## 仍不能声称的事项

- 不能声称C组47项图件已经完成真实人工校对。
- 不能声称任何候选图已经是正式论文插图定稿。
- 不能声称第42届第3题题解图3a-3c是题面图3a-3d的一一原样放大。
- 不能放行正式评分者模板、正式编码、正式统计、论文结果章、专家意见、教师意见、问卷结果或课堂实验结论。

## 下一步最小任务

若仍未收到真实回填副本，建议转入 `G1-07-FOLLOWUP-MANUAL-P0-BATCH3-TASK-CARDS`，将48项图件入口拆为逐项领取任务卡；若收到真实副本，则优先执行对应批次的真实回填接收检查。

## 结构化QA表

见 `03_corpus/manual_review_p0_batch3_figure_queue_qa_v1.csv`。
