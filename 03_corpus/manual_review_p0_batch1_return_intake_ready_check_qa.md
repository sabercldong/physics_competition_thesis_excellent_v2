# P0第一批真实回填接收准备表QA

任务编号：`G1-07-FOLLOWUP-MANUAL-P0-BATCH1-RETURN-INTAKE-READY-CHECK-QA`

## 性质声明

本文件只检查 `03_corpus/manual_review_p0_batch1_return_intake_ready_check.md` 与 `03_corpus/manual_review_p0_batch1_return_intake_ready_check_v1.csv` 的结构完整性、引用路径、接收规则覆盖和冻结边界。它不代表真实回填已经收到，不创建真实回填目录，不填写校对人、日期或校对结论，不关闭任何人工校对项，不修改题文，不生成正式编码、正式统计、论文正文或 `final_coding.csv`。

## QA结论

本轮完成42项QA检查，结论为通过。

已确认：

- 接收准备说明和结构表均存在；
- CSV为UTF-8 BOM和LF换行；
- `P0B1INTAKE-01` 至 `P0B1INTAKE-18` 连续唯一；
- 18项检查均保持 `不放行：接收准备，未真实回填`；
- 上游模板、填写说明、交接包索引、索引QA、通用接收协议、登记模板和目录规则均可定位；
- 接收准备表覆盖命名规则、SHA-256、文件大小、结构检查、不可变字段、必填字段、隔离处理、整合门槛、正式编码边界和正文边界；
- 当前未创建 `03_corpus/manual_review_returns/`；
- QA未把真实回填、人工销项、正式编码、正式统计或论文结果写成已完成。

结构化QA表见：

- `03_corpus/manual_review_p0_batch1_return_intake_ready_check_qa_v1.csv`

## 仍不能声称

QA通过后仍不得声称：

- P0第一批真实回填副本已经收到；
- P0第一批真实人工校对已经完成；
- 38个题目级小批次已经销项；
- 第一批76条OCR、公式与特殊符号问题已经关闭；
- 第37、38、40、41、42届题文已经正式无误；
- 正式评分者模板已经放行；
- 真实双评分者编码、一致性检验、分歧裁决或 `final_coding.csv` 已经完成；
- 第四章正式统计、典型案例结论或论文结果已经成立。

## 下一最小任务

下一步可执行 `G1-07-FOLLOWUP-MANUAL-P0-BATCH1-RETURN-WAITING-ROOM-UPDATE`：把P0第一批回填链条更新到等待室，明确哪些动作必须等待真实回填、哪些准备可以继续推进、哪些正式产出继续冻结。
