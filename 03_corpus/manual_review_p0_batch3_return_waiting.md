# P0第三批真实回填等待状态登记

任务编号：`G1-07-FOLLOWUP-MANUAL-P0-BATCH3-RETURN-WAITING`

## 性质声明

本文件用于登记P0第三批48项图件与 `CPHO42-Q03-SOLFIG` 边界任务在“交接链已收束、真实回填副本未收到”时的等待状态、触发条件和触发后最短动作。它是等待状态登记，不是人工校对结果。

本任务不填写真实校对人、校对日期、图件决定、是否可用于论文、是否需重绘、修订说明、最终证据位置、专家意见、导师意见、竞赛教师意见或评分者结果；不创建 `03_corpus/manual_review_returns/`；不关闭C组47项图件问题或D组 `CPHO42-Q03-SOLFIG` 边界问题；不生成正式论文插图定稿、正式编码、正式统计、论文结果章或 `07_analysis/data/final_coding.csv`；不修改 `00_originals/`、题文原件、论文正文或主张证据矩阵。

## 当前结论

P0第三批图件与SOLFIG边界真实核对交接入口已经可以领取，但当前仍处于“等待真实回填副本”状态。

已经具备的材料包括：

- 48项图件与SOLFIG边界任务入口；
- 入口QA；
- 48张逐项领取任务卡；
- 任务卡QA；
- 交接链收束说明与QA；
- C组47项图件回填包；
- D组9项分值与附属图回填包，其中包含第42届第3题SOLFIG边界；
- 通用真实回填接收规则与整合协议。

尚未出现的材料是：由真实执行者填写后的回填副本，或按任务卡逐项完成并可追溯的真实图件/附属图边界核对记录。

## 可领取入口

其他智能体或真实校对者应从以下文件领取和执行：

| 用途 | 文件 |
|---|---|
| 领取逐项任务 | `03_corpus/manual_review_p0_batch3_task_cards_v1.csv` |
| 阅读交接说明 | `03_corpus/manual_review_p0_batch3_handoff_closeout.md` |
| 查看入口QA | `03_corpus/manual_review_p0_batch3_figure_queue_qa.md` |
| 查看任务卡QA | `03_corpus/manual_review_p0_batch3_task_cards_qa.md` |
| 查看收束QA | `03_corpus/manual_review_p0_batch3_handoff_closeout_qa.md` |
| C组图件写回位置 | `03_corpus/manual_review_c_closure_packet_v1.csv` 的对应 `issue_id` 行，或按接收协议另存真实副本 |
| D组SOLFIG写回位置 | `03_corpus/manual_review_d_closure_packet_v1.csv` 的 `CPHO42-Q03-SOLFIG` 对应行，或按接收协议另存真实副本 |

结构化等待登记表见：

- `03_corpus/manual_review_p0_batch3_return_waiting_v1.csv`

## 收到真实回填后的触发流程

只有在真实回填副本出现后，才能进入以下最短流程：

1. 按接收规则登记真实副本文件名、路径、大小、校验值、接收日期和接收人；
2. 检查48项任务卡映射、`source_issue_id`、`material_id`、不可变继承字段和必填回填字段；
3. 将“需重绘”“继续待核”或“题面/题解图边界冲突”的条目列入隔离修订清单；
4. 对“允许用于论文图件或进入正式评分者模板”的条目执行整合QA；
5. 整合QA通过后，再讨论是否更新人工校对总清单、正式论文图件候选清单、正式评分者模板候选或后续正式编码入口。

## 当前禁止事项

- 不得把任务卡、入口、交接链或等待登记写成人工校对完成；
- 不得把Codex内部图件判断写成真实专家、导师、竞赛教师、评分者或人工校对者意见；
- 不得跳过真实回填副本，直接关闭C组47项图件问题或 `CPHO42-Q03-SOLFIG` 边界问题；
- 不得声称 `CPHO42-Q03-SOLFIG` 已替代 `CPHO42-Q03-FIG` 题面图终核；
- 不得把候选图、重裁图或接触图直接升格为正式论文插图定稿；
- 不得把内部编码复制成 `final_coding.csv`；
- 不得生成第四章正式统计、趋势、共现、显著性或教学效果结论；
- 不得修改 `00_originals/` 或覆盖原始题目文件。

## 下一最小任务

若真实回填副本仍未收到，下一步建议执行 `G1-07-FOLLOWUP-MANUAL-P0-BATCH3-RETURN-WAITING-QA`：检查本等待登记和结构化触发表是否正确记录未收到状态、触发条件、冻结边界、CSV格式和禁止推进项。

若真实回填副本已经收到，则跳过等待QA，优先执行 `G1-07-FOLLOWUP-MANUAL-P0-BATCH3-RETURN-INTAKE-REAL-CHECK`：只做接收登记、结构检查、不可变字段检查和整合前QA，不直接进入正式编码、正式论文图件定稿或论文结果写作。
