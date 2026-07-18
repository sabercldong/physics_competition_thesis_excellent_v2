# G1-07-REAL-RETURN-PACKET-HANDOFF-REGISTER-QA 首批真实回填接收登记QA

更新时间：2026-07-19

## 性质声明

本QA只检查首批真实回填接收登记和交接规则是否可作为未来真实回填接收入口。它不填写真实文件名、真实路径、校验值、接收日期、接收人、校对人、校对日期、校对决定、修订说明、专家意见、评分者意见、问卷结果、课堂结果或论文正文结论，也不关闭任何人工校对项。

## 检查结论

- QA检查项：89项。
- 通过：89项。
- 未通过：0项。
- 接收登记表：38行，对应首批38个题目级材料包。
- 接收规则表：12条规则。
- 覆盖问题：A组76项高风险OCR/公式问题。
- 真实回填副本：0份。
- 真实销项数：0项。
- 正式编码放行：0项。
- 正文使用放行：0项。

## 检查分布

| 类别 | 检查项数 |
|---|---:|
| CSV格式 | 4 |
| 上游QA | 1 |
| 协议一致性 | 2 |
| 字段结构 | 2 |
| 报告文本 | 7 |
| 提交边界 | 5 |
| 数量核验 | 2 |
| 未收到状态 | 3 |
| 未放行门禁 | 4 |
| 目录规范 | 6 |
| 空白保护 | 17 |
| 组别核验 | 1 |
| 编号核验 | 2 |
| 覆盖核验 | 1 |
| 规则覆盖 | 12 |
| 触发条件 | 6 |
| 输入存在性 | 6 |
| 首批继承 | 8 |

## 已确认一致性

1. `03_corpus/manual_review_real_return_handoff_register_v1.csv` 和 `03_corpus/manual_review_real_return_handoff_rules_v1.csv` 均为UTF-8 BOM和LF换行。
2. 登记表38行，`RPH-001` 至 `RPH-038` 连续唯一。
3. 规则表12行，`RPHR-01` 至 `RPHR-12` 连续唯一。
4. 登记表的 `priority_packet_id`、`material_id`、届次、年份、题号、`covered_issue_ids` 和 `covered_issue_count` 与首批优先包逐行一致。
5. 登记表全部指向A组和 `03_corpus/manual_review_real_return_priority_packet_v1.csv`。
6. 推荐目录均指向 `03_corpus/manual_review_returns/` 下的 `incoming/REAL-P1/`、`registered/REAL-P1/`、`quarantine/REAL-P1/` 和 `integration_logs/REAL-P1/`，但当前目录未创建。
7. 真实文件名、另存路径、校验值、文件大小、接收日期、接收人、校对人、校对日期、材料决定、OCR决定、公式决定、修订说明和复核后证据位置均为空。
8. 结构检查、字段完整性和冲突状态均为“未检查：未收到真实回填”。
9. 登记表和规则表均保持“不放行”；正式编码和正文使用均为“否”。
10. 每行关联的 `RIP` 规则均可在回填整合协议中定位，且包含首批A组接收、结构检查、字段完整性、冲突处理、关闭判定、账本同步和隔离边界所需规则。

## 仍不能声称的内容

- 不能声称首批38个材料包已经收到真实回填。
- 不能声称A组76项已经完成正式人工校对或真实销项。
- 不能声称B组22项、C组47项和D组9项已处理。
- 不能进入正式A/B评分者编码、正式统计、正式结果分析、显著性结论或正文结果章写作。
- 不能把接收登记、接收规则或本QA写成真实专家审查、真实评分者编码或导师确认。
- 不能修改 `08_manuscript/`、`09_quality/claim_evidence_matrix.csv` 或 `02_literature/references.bib` 来升级主张。

## 保留风险

- 本QA只证明接收登记结构可用，不证明已经收到或整合真实回填。
- 首批接收登记只覆盖A组76项，B/C/D剩余78项仍需后续登记或真实回填。
- 未来收到真实回填后，必须先另存副本、计算校验值、做结构检查和冲突分级，再另设整合QA任务。
- 即使首批A组完成回填，仍需真实评分者独立编码、一致性计算和分歧裁决后，才可能进入正式结果分析。

## 下一步最小任务

`G1-07-REMAINING-RETURN-PACKET-HANDOFF-REGISTER`：为B组22项、C组47项和D组9项建立剩余78项真实回填接收登记，衔接既有B/C/D回填包、通用接收目录规范和回填整合协议。该任务仍不得代填真实回填，不得创建真实回填目录，不得关闭条目或放行正式编码。

## 输出文件

- QA报告：`03_corpus/manual_review_real_return_handoff_register_qa.md`
- QA表：`03_corpus/manual_review_real_return_handoff_register_qa_v1.csv`
- 被检查对象：`03_corpus/manual_review_real_return_handoff_register.md`、`03_corpus/manual_review_real_return_handoff_register_v1.csv`、`03_corpus/manual_review_real_return_handoff_rules_v1.csv`
