# G1-07-REAL-RETURN-PACKET-HANDOFF-REGISTER 首批真实回填接收登记

更新时间：2026-07-19

## 性质声明

本任务为首批A组真实人工终核回填建立接收登记和交接规则。它只规定未来真实回填副本如何保存、命名、校验、登记和触发整合QA；当前不创建真实回填目录，不登记真实回填副本，不填写真实校对人、日期、决定、修订说明、专家意见、评分者意见、问卷结果、课堂结果或论文正文结论，也不关闭任何人工校对项。

## 上游依据

- 首批优先包：`03_corpus/manual_review_real_return_priority_packet.md`
- 首批优先包表：`03_corpus/manual_review_real_return_priority_packet_v1.csv`
- 首批优先包QA：`03_corpus/manual_review_real_return_priority_packet_qa.md`
- 通用接收目录规范：`03_corpus/return_intake_folder_protocol.md`
- 通用接收登记模板：`03_corpus/manual_review_return_intake_register_template_v1.csv`
- 回填整合协议：`03_corpus/manual_review_return_integration_protocol.md`

## 登记范围

| 指标 | 数量 |
|---|---:|
| 首批接收登记行 | 38 |
| 对应题目级材料包 | 38 |
| 覆盖A组人工终核问题 | 76 |
| 覆盖组别 | A组 |
| 本轮收到真实回填副本 | 0 |
| 本轮真实销项数 | 0 |
| 本轮正式编码放行数 | 0 |

## 届次覆盖

| 届次 | 登记行数 |
|---|---:|
| 第37届 | 8 |
| 第38届 | 8 |
| 第40届 | 8 |
| 第41届 | 7 |
| 第42届 | 7 |

## 推荐接收目录

当前不创建真实回填目录。收到真实副本后，按以下结构创建并登记：

| 目录 | 用途 | 创建条件 |
|---|---|---|
| `03_corpus/manual_review_returns/incoming/REAL-P1/` | 原样保存刚收到的首批回填文件 | 收到至少一份REAL-P1真实回填副本 |
| `03_corpus/manual_review_returns/registered/REAL-P1/` | 保存已登记且通过基本结构检查的副本 | 完成文件名、校验值、行数和字段检查 |
| `03_corpus/manual_review_returns/quarantine/REAL-P1/` | 隔离来源不清、结构异常或字段冲突的文件 | 文件未通过基本接收检查 |
| `03_corpus/manual_review_returns/integration_logs/REAL-P1/` | 保存后续整合QA、冲突处理和同步日志 | 触发REAL-P1整合QA |

## 文件命名规则

首批真实回填副本建议命名为：

`return_{YYYYMMDD}_A_real-p1_{material_id}_{reviewer_code}_{seq}.{ext}`

示例格式仅用于说明，不代表已经收到真实文件：

`return_YYYYMMDD_A_real-p1_CPHO41-Q02_RXX_001.csv`

命名要求：

- `YYYYMMDD` 只能使用实际接收登记日期；
- `reviewer_code` 只能使用可追溯的匿名编码，不写真实姓名；
- `material_id` 必须与首批包中的38个材料ID之一一致；
- 同一材料多次回填时用 `seq` 保留顺序，不覆盖旧副本；
- 转换件必须另存，不覆盖收到时的原始副本。

## 接收登记字段

`03_corpus/manual_review_real_return_handoff_register_v1.csv` 已为38个首批材料逐行预置登记字段，包括：

- 来源定位：`priority_packet_id`、`material_id`、`covered_issue_ids`；
- 接收目录：`expected_incoming_directory`、`expected_registered_directory`、`expected_quarantine_directory`、`expected_integration_log_directory`；
- 命名规则：`expected_filename_pattern`、`allowed_extensions`；
- 校验字段：`sha256`、`file_size_bytes`；
- 接收字段：`received_original_filename`、`stored_incoming_copy_path`、`intake_date`、`received_by`；
- 回填观察字段：校对人、校对日期、材料决定、OCR决定、公式决定、修订说明和复核后证据位置；
- 门禁字段：结构检查、字段完整性、冲突状态、整合QA触发记录、正式编码放行和正文使用放行。

以上真实接收和回填观察字段本轮全部保持空白或“未检查：未收到真实回填”。

## 触发整合QA的条件

任一首批材料进入整合QA前，至少满足：

1. 真实副本已另存到 `incoming/REAL-P1/`，且未覆盖空白优先包；
2. `received_original_filename`、`stored_incoming_copy_path`、`sha256`、`file_size_bytes`、`intake_date` 和 `received_by` 已登记；
3. 文件中的 `material_id`、`covered_issue_ids`、届次、年份和题号与首批优先包一致；
4. 真实校对人或编码、校对日期、材料决定、OCR决定、公式决定、是否需修订、修订说明和复核后证据位置可被检查；
5. 若存在缺行、多行、字段错位、固定字段不一致或来源不明，必须进入 `quarantine/REAL-P1/`，不得同步账本；
6. 通过接收检查后，另设 `G1-07-REAL-RETURN-PACKET-INTEGRATION-QA` 执行整合QA；接收登记本身不关闭条目。

## 当前不能声称的内容

- 不能声称首批38个材料包已经收到真实回填。
- 不能声称A组76项已经完成正式人工校对或真实销项。
- 不能声称B组22项、C组47项和D组9项已处理。
- 不能进入正式A/B评分者编码、正式统计、正式结果分析、显著性结论或正文结果章写作。
- 不能修改 `08_manuscript/`、`09_quality/claim_evidence_matrix.csv` 或 `02_literature/references.bib` 来升级主张。

## 下一步最小任务

`G1-07-REAL-RETURN-PACKET-HANDOFF-REGISTER-QA`：检查首批接收登记是否严格覆盖38个首批材料包、CSV是否为UTF-8 BOM和LF换行、真实文件名/路径/校验值/接收日期/校对人/决定是否全部空白、触发整合QA条件是否与回填整合协议一致，并确认本轮未创建真实回填目录、未关闭条目、未放行正式编码。

## 输出文件

- 首批接收登记说明：`03_corpus/manual_review_real_return_handoff_register.md`
- 首批接收登记表：`03_corpus/manual_review_real_return_handoff_register_v1.csv`
- 首批接收规则表：`03_corpus/manual_review_real_return_handoff_rules_v1.csv`
