# P0第一批真实回填等待室QA

任务编号：`G1-07-FOLLOWUP-MANUAL-P0-BATCH1-RETURN-WAITING-ROOM-UPDATE-QA`

## 性质声明

本文件只检查 `03_corpus/manual_review_p0_batch1_return_waiting_room_update.md` 与 `03_corpus/manual_review_p0_batch1_return_waiting_room_update_v1.csv` 的结构、路径、状态和边界。QA通过不代表已经收到真实回填，不代表38个题目级小批次已人工销项，不代表正式评分者模板、正式编码、正式统计、论文结果章或 `final_coding.csv` 已放行。

本任务不创建 `03_corpus/manual_review_returns/`，不填写校对人、日期、OCR决定、公式决定、证据摘记、专家意见、导师意见、竞赛教师意见或评分者结果，不修改题文、正文、主张证据矩阵或 `00_originals/`。

## QA结论

等待室更新通过40项边界检查。

已确认：

- 等待室说明文件和路线表均存在；
- 路线表为UTF-8 BOM与LF换行；
- 路线表字段完整，共12条，编号为 `P0B1WR-01` 至 `P0B1WR-12`；
- 三类边界计数正确：5项必须等待真实回填、4项可继续准备、3项禁止推进；
- 12条路线的证据路径均可定位；
- 放行状态仅包含“冻结”和“不放行正式结果”；
- 未创建真实回填目录；
- 当前未生成 `07_analysis/data/final_coding.csv`；
- 等待室说明没有把内部QA、模板或准备状态写成真实回填、人工校对完成、正式评分者意见或论文正式结果。

结构化QA表见：

- `03_corpus/manual_review_p0_batch1_return_waiting_room_update_qa_v1.csv`

## 仍不能声称

即使本QA通过，仍不能声称：

- P0第一批38个题目级小批次已经人工校对完成；
- 第一批76条OCR、公式与特殊符号问题已经销项；
- 校对人、校对日期、OCR决定、公式决定或证据摘记已经真实填写；
- 正式评分者模板可以使用P0第一批全部条目；
- `final_coding.csv` 已生成或可以由内部编码替代；
- 第四章结果、趋势、共现、比例、显著性或典型案例结论可以写入正文；
- Codex、模板、QA或内部预演可以被写成真实专家、导师、竞赛教师或评分者意见。

## 下一最小任务

下一步建议执行 `G1-07-FOLLOWUP-MANUAL-P0-BATCH1-AGENT-TASK-CARDS`：把P0第一批38个题目级小批次整理成其他智能体可直接执行的逐题核对任务卡。该任务仍只准备核对入口，不代填真实校对结果，不关闭小批次，不放行正式编码。
