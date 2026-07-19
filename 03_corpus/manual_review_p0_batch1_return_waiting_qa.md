# P0第一批真实回填等待状态登记QA

任务编号：`G1-07-FOLLOWUP-MANUAL-P0-BATCH1-RETURN-WAITING-QA`

## 性质声明

本文件检查 `G1-07-FOLLOWUP-MANUAL-P0-BATCH1-RETURN-WAITING` 形成的等待状态登记是否可用、是否越界、是否仍保持真实回填未收到的冻结边界。它只做QA，不接收真实回填副本，不填写校对结果。

本任务不填写真实校对人、校对日期、OCR决定、公式决定、修订位置、证据摘记、专家意见、导师意见、竞赛教师意见或评分者结果；不创建 `03_corpus/manual_review_returns/`；不关闭38个小批次；不生成正式评分者完成数据、正式统计、论文结果章或 `07_analysis/data/final_coding.csv`；不修改 `00_originals/`、题文原件、论文正文或主张证据矩阵。

## QA结论

等待状态登记QA通过。

已确认：

- `03_corpus/manual_review_p0_batch1_return_waiting.md` 存在，并明确等待登记不是人工校对结果；
- `03_corpus/manual_review_p0_batch1_return_waiting_v1.csv` 为UTF-8 BOM与LF换行；
- 等待登记表共12项，`P0B1WAIT-01` 至 `P0B1WAIT-12` 连续唯一；
- 12项均包含当前证据、当前状态、触发条件、触发后动作、禁止事项、放行状态和后续路线；
- 当前未创建 `03_corpus/manual_review_returns/`；
- 当前未生成 `07_analysis/data/final_coding.csv`；
- 等待登记未放行正式评分者模板、正式编码、正式统计或论文结果章。

结构化QA表见：

- `03_corpus/manual_review_p0_batch1_return_waiting_qa_v1.csv`

## 仍不能声称

- 不能声称P0第一批38个小批次已经人工校对完成；
- 不能声称真实回填副本已经收到；
- 不能声称任何OCR、公式、特殊符号或小问边界已经真实销项；
- 不能声称可以进入正式评分者模板、正式A/B编码、一致性计算或分歧裁决；
- 不能声称 `final_coding.csv` 已生成或第四章正式结果已经成立；
- 不能把Codex准备材料写成真实专家、导师、竞赛教师、评分者或人工校对者意见。

## 下一最小任务

若真实回填副本仍未收到，建议转入 `G1-07-FOLLOWUP-MANUAL-P0-BATCH2-RETURN-PREP`：按同样规则为P0第二批中风险公式与特殊符号项准备回填入口，继续推进可交接材料包。

若真实回填副本已经收到，则优先执行 `G1-07-FOLLOWUP-MANUAL-P0-BATCH1-RETURN-INTAKE-REAL-CHECK`：只做接收登记、结构检查、不可变字段检查、必填字段检查和整合前QA，不直接进入正式编码或论文结果写作。
