# P0第三批逐项领取任务卡QA

任务编号：`G1-07-FOLLOWUP-MANUAL-P0-BATCH3-TASK-CARDS-QA`

## 性质声明

本文件检查 `03_corpus/manual_review_p0_batch3_task_cards.md` 和 `03_corpus/manual_review_p0_batch3_task_cards_v1.csv` 是否正确把P0第三批48项图件/SOLFIG边界入口拆成逐项任务卡。QA通过只表示任务卡可领取，不表示真实人工校对完成。

## QA结论

通过。任务卡CSV共48张，编号 `P0B3CARD-01` 至 `P0B3CARD-48` 连续唯一，逐卡挂接 `P0B3FIG-01` 至 `P0B3FIG-48`，并与第三批入口的 `source_issue_id` 和 `material_id` 逐行一致。

## 已确认事项

- 任务卡CSV为UTF-8 BOM，LF换行。
- 48张任务卡覆盖C组47项题图裁边与图注问题，以及第42届第3题 `CPHO42-Q03-SOLFIG` 解答放大图边界问题。
- 最低核对输入路径缺失0项。
- 48张任务卡均保持“待领取：未真实回填”和“不放行：P0第三批任务卡，未真实销项”。
- `CPHO42-Q03-SOLFIG` 任务卡明确不替代 `CPHO42-Q03-FIG` 题面图终核。
- `03_corpus/manual_review_returns/` 当前不存在。
- `07_analysis/data/final_coding.csv` 当前不存在。

## 仍不能声称的事项

- 不能声称48张任务卡已经被真实领取或完成。
- 不能声称C组47项图件已经完成真实人工校对。
- 不能声称任何候选图已经成为正式论文插图定稿。
- 不能放行正式评分者模板、正式编码、正式统计、论文结果章、专家意见、教师意见、问卷结果或课堂实验结论。

## 下一步最小任务

若仍未收到真实回填副本，建议转入 `G1-07-FOLLOWUP-MANUAL-P0-BATCH3-HANDOFF-CLOSEOUT`，将第三批入口、入口QA、任务卡和任务卡QA收束为一页式交接链；若收到真实副本，则优先执行对应批次的真实回填接收检查。

## 结构化QA表

见 `03_corpus/manual_review_p0_batch3_task_cards_qa_v1.csv`。
