# G1-07-RETURN-INTAKE-FOLDER-PREP-QA 真实回填接收目录准备QA报告

更新时间：2026-07-19

## 性质声明

本QA只检查 `03_corpus/return_intake_folder_protocol.md`、`03_corpus/manual_review_return_intake_register_template_v1.csv` 和 `03_corpus/manual_review_return_intake_folder_rules_v1.csv` 是否与 `NQ-01`、接收检查、正式阻断表和回填整合协议一致。它不填写真实校对人、真实校对日期、校对决定、分值、图号边界、专家意见、评分者记录、问卷结果、课堂结果或论文正文结论，也不关闭154项待核问题。

## QA结论

- QA检查项：75项。
- 通过项：75项。
- 不通过项：0项。
- 接收登记模板为UTF-8 BOM和LF换行，共5行，覆盖A/B/C/D/MIXED五类模板。
- 5行登记模板中的真实文件名、副本路径、校验值、文件大小、接收日期、接收人、校对人编码和校对日期均为空。
- 5行登记模板的状态均为“模板：未收到”，决定字段和冲突字段均为“未检查：未收到真实回填”。
- 目录规则表为UTF-8 BOM和LF换行，共12行，`RIF-01` 至 `RIF-12` 连续唯一，释放状态全部为“不放行”。
- 接收目录规范包含性质声明、推荐目录结构、文件命名规则、回收登记字段、接收流程、冻结边界和下一任务。
- `03_corpus/manual_review_returns`、`03_corpus/returns`、`03_corpus/returned` 和 `03_corpus/manual_review_return_copies` 均未创建。
- 上游接收状态仍显示未收到真实回填；正式阻断表6项均保持“阻断”。

## 关键检查结果

| 检查 | 结果 | 证据 |
|---|---|---|
| 登记模板编码与换行 | 通过 | UTF-8 BOM；LF换行；无CRLF/CR |
| 登记模板行数与组别 | 通过 | 5行；A/B/C/D/MIXED |
| 登记模板真实字段 | 通过 | 文件名、路径、校验值、接收日期、校对人和日期均为空 |
| 登记模板状态 | 通过 | 5行均为“模板：未收到” |
| 登记模板RIP引用 | 通过 | 所有关联 `RIP-01` 至 `RIP-09` 均可在整合协议中定位 |
| 目录规则表编码与换行 | 通过 | UTF-8 BOM；LF换行；无CRLF/CR |
| 目录规则ID | 通过 | `RIF-01` 至 `RIF-12` 连续唯一 |
| 目录规则释放状态 | 通过 | 12条规则均为“不放行” |
| 接收目录 | 通过 | 四个候选真实回填目录均不存在 |
| 上游队列 | 通过 | `NQ-01` 指向接收目录规范和回收登记模板，状态为“不放行” |
| 接收状态 | 通过 | 8项接收状态均为未收到、阻断、未通过或不得使用语境 |
| 正式阻断 | 通过 | 6项正式产出均为“阻断” |
| 正文与主张矩阵隔离 | 通过 | 规范明确隔离 `08_manuscript/` 和 `09_quality/claim_evidence_matrix.csv` |
| 越界表述扫描 | 通过 | 未发现“正式放行”“真实人工终核已完成”等正向完成表述 |

## 仍然不能说明的内容

- 不能说明已经收到真实人工终核回填副本。
- 不能说明154项人工终核已经完成或可关闭。
- 不能说明任何题干、公式、题图、分值或参考解答已经正式校对。
- 不能说明可以进入正式A/B评分者编码、正式统计、正式案例结论、教师验证或课堂效果结论。
- 不能把接收规范、登记模板、目录规则或本QA写成真实专家审查、真实评分者一致性、导师确认或正式结果分析。
- 不能据此修改 `08_manuscript/` 正文或 `09_quality/claim_evidence_matrix.csv`。

## 下一步最小任务

`G1-07-NO-RETURN-CORPUS-PATH-QA`：按照无真实回填队列 `NQ-02`，检查转写稿、公式核对表、页面证据图、候选图和索引路径是否可定位，整理断链和边界疑点；该任务仍不得写成正式人工终核。

## 输出文件

- QA报告：`03_corpus/return_intake_folder_prep_qa.md`
- QA记录表：`03_corpus/return_intake_folder_prep_qa_v1.csv`
- 被检查文件：`03_corpus/return_intake_folder_protocol.md`、`03_corpus/manual_review_return_intake_register_template_v1.csv`、`03_corpus/manual_review_return_intake_folder_rules_v1.csv`
