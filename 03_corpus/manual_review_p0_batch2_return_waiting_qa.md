# P0第二批真实回填等待状态登记QA

任务编号：`G1-07-FOLLOWUP-MANUAL-P0-BATCH2-RETURN-WAITING-QA`

## 性质

本文件检查 `03_corpus/manual_review_p0_batch2_return_waiting.md` 和 `03_corpus/manual_review_p0_batch2_return_waiting_v1.csv` 是否正确记录“真实回填副本未收到”的等待状态、触发条件和冻结边界。QA通过只表示等待登记可靠，不表示人工校对完成。

## QA结论

通过。等待登记CSV共12项，编号 `P0B2WAIT-01` 至 `P0B2WAIT-12` 连续，覆盖真实回填副本、22行回填入口、22张任务卡、接收目录、校验值、不可变字段、必填字段、冲突处理、整合QA、正式评分者模板候选、`final_coding.csv` 和项目状态同步。

## 已确认事项

- 等待登记CSV为UTF-8 BOM，LF换行。
- 12项等待登记均填写当前证据、当前状态、触发条件、触发后动作、禁止事项、放行状态和后续路线。
- 上游回填入口22行、任务卡22张、交接链收束QA 42项均可定位。
- `03_corpus/manual_review_returns/` 当前不存在。
- `07_analysis/data/final_coding.csv` 当前不存在。

## 仍不能声称的事项

- 不能声称P0第二批22项已经完成真实人工校对。
- 不能关闭公式或特殊符号待核问题。
- 不能放行正式评分者模板、正式编码、正式统计或论文结果章。
- 不能把等待登记、任务卡或QA写成真实专家、导师、教师、评分者或人工校对者意见。

## 下一步最小任务

若仍未收到真实回填副本，建议转入 `G1-07-FOLLOWUP-MANUAL-P0-BATCH3-FIGURE-QUEUE`，准备第三批高风险图件与第42届第3题解答放大图边界任务入口；若收到真实副本，则优先执行 `G1-07-FOLLOWUP-MANUAL-P0-BATCH2-RETURN-INTAKE-REAL-CHECK`。

## 结构化QA表

见 `03_corpus/manual_review_p0_batch2_return_waiting_qa_v1.csv`。
