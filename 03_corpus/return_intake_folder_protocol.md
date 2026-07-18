# G1-07-RETURN-INTAKE-FOLDER-PREP 真实回填接收目录规范

更新时间：2026-07-19

## 性质声明

本文件按照无真实回填队列 `NQ-01` 建立真实人工终核回填副本的接收目录规范、文件命名规则、回收登记字段和后续整合触发条件。当前项目仍未发现真实人工终核回填副本，本任务不创建真实回填目录，不登记虚构回填，不填写真实校对人、日期或决定，不关闭154项人工校对问题，也不释放正式编码、正式统计、正文结果写作或主张矩阵升级。

## 上游依据

- 无回填材料队列：`03_corpus/no_return_material_queue.md`
- 无回填材料队列表：`03_corpus/no_return_material_queue_v1.csv`
- 无回填材料队列QA：`03_corpus/no_return_material_queue_qa.md`
- 真实回填接收检查：`03_corpus/manual_review_return_intake_check.md`
- 真实回填接收状态表：`03_corpus/manual_review_return_intake_status_v1.csv`
- 正式编码阻断表：`03_corpus/manual_review_formal_coding_blocker_v1.csv`
- 回填整合协议：`03_corpus/manual_review_return_integration_protocol.md`
- 回填整合规则表：`03_corpus/manual_review_return_integration_protocol_v1.csv`

## 推荐目录结构

当前不创建下列目录。只有在真实回填副本实际收到时，才按接收批次创建，并同步登记。

| 目录 | 用途 | 创建条件 | 禁止事项 |
|---|---|---|---|
| `03_corpus/manual_review_returns/` | 真实回填材料接收根目录 | 收到至少一份真实回填副本 | 不得放入空白模板冒充回填 |
| `03_corpus/manual_review_returns/incoming/` | 原样保存刚收到的文件 | 收到文件后先复制到此处 | 不得改名覆盖原文件含义 |
| `03_corpus/manual_review_returns/registered/` | 已登记且完成基本校验的副本 | 完成回收登记、校验值和结构检查 | 不得直接用于关闭条目 |
| `03_corpus/manual_review_returns/quarantine/` | 结构异常、字段冲突或来源不明文件 | 出现缺行、多行、字段错位、来源不清等问题 | 不得进入账本同步 |
| `03_corpus/manual_review_returns/integration_logs/` | 接收、结构检查、冲突处理和整合日志 | 任一真实回填副本进入检查 | 不得省略失败记录 |
| `03_corpus/manual_review_returns/superseded/` | 被后续更正版本替代的回填副本 | 收到明确更正版本并保留替代说明 | 不得删除旧副本 |

## 文件命名规则

真实回填副本另存时，推荐使用：

`return_{YYYYMMDD}_{group}_{packet}_{reviewer_code}_{seq}.{ext}`

字段含义：

| 字段 | 示例 | 说明 |
|---|---|---|
| `YYYYMMDD` | `20260719` | 接收登记日期，不得用推测日期 |
| `group` | `A`、`B`、`C`、`D`、`MIXED` | 对应A/B/C/D回填包；混合文件先标为 `MIXED` |
| `packet` | `closure_packet` | 对应回填包或来源材料类型 |
| `reviewer_code` | `R01` | 仅使用可复核的匿名编码；不得写真实姓名到公开复现包 |
| `seq` | `001` | 同日同组同来源的流水号 |
| `ext` | `csv`、`xlsx`、`pdf`、`zip` | 保留原始格式；转换件必须另存 |

示例仅用于命名说明，不代表本项目已收到该文件：

`return_YYYYMMDD_A_closure_packet_RXX_001.csv`

## 回收登记字段

真实回填接收登记至少包含：

| 字段 | 含义 | 当前任务状态 |
|---|---|---|
| `receipt_id` | 接收流水号 | 仅提供模板 |
| `intake_date` | 接收日期 | 不填写真实日期 |
| `received_by` | 接收人或经手人编码 | 不填写真实人员 |
| `source_group` | A/B/C/D/MIXED | 模板行可标明待真实回填 |
| `source_packet` | 对应空白回填包或材料包 | 模板行可列目标包 |
| `source_filename` | 收到时的原始文件名 | 当前为空 |
| `stored_copy_path` | 另存副本位置 | 当前为空 |
| `sha256` | 另存副本校验值 | 当前为空 |
| `file_size_bytes` | 文件大小 | 当前为空 |
| `reviewer_code_claimed` | 文件内声明的评分者/校对者编码 | 当前为空 |
| `review_date_claimed` | 文件内声明的校对日期 | 当前为空 |
| `decision_fields_present` | 必填决定字段是否存在 | 当前为未检查 |
| `conflict_status` | 无冲突/一般/重大/致命/未检查 | 当前为未检查 |
| `intake_status` | 模板、已登记、隔离、退回补正、进入结构检查 | 当前为模板 |
| `linked_protocol_rule` | 对应 `RIP-01` 至 `RIP-22` | 当前主要指向 `RIP-01` 至 `RIP-03` |
| `next_action` | 下一步处理 | 等待真实回填 |
| `notes` | 备注 | 必须声明模板不代表已收到 |

## 接收流程

1. 收到真实回填副本后，先复制到 `incoming/`，不得覆盖A/B/C/D空白回填包。
2. 计算另存副本的SHA-256和文件大小，写入接收登记表。
3. 核对文件名、组别、来源包、行数、表头和 `issue_id` 集合。
4. 结构通过后移入或复制到 `registered/`，结构异常或来源不明的文件进入 `quarantine/`。
5. 按 `manual_review_return_integration_protocol_v1.csv` 的 `RIP-01` 至 `RIP-22` 执行结构检查、不可变字段检查、字段完整性检查、冲突分级和关闭候选判定。
6. 只有通过整合QA的条目，才可另设任务同步 `manual_review_checklist.csv`、优先队列、销项计划、动作计划、总索引、`PROJECT_STATUS.md`、`TASKS.md` 和 `CHANGELOG.md`。
7. 正式编码、正式统计、论文正文结果和主张矩阵更新必须另设任务，不得混入回填接收提交。
8. `08_manuscript/` 正文文件和 `09_quality/claim_evidence_matrix.csv` 必须继续隔离；接收登记或接收QA不能直接修改正文主张、证据等级或结论状态。

## 当前冻结边界

- 154项人工校对问题仍未真实销项。
- A/B组未完成真实回填前，不进入正式A/B评分者独立编码。
- C组未完成真实图件回填前，不定稿论文案例图、附录图或图件结论。
- D组未完成真实分值/附属图边界回填前，不生成第35届分值统计或第42届第3题附属图定稿。
- 当前接收规范只支持未来接收、校验和整合流程，不支持任何正式结论。

## 下一步最小任务

`G1-07-RETURN-INTAKE-FOLDER-PREP-QA`：检查本接收目录规范、登记模板和规则表是否与 `NQ-01`、接收检查、正式阻断表和回填整合协议一致，确认没有登记真实回填、没有创建真实回填目录、没有关闭154项、没有释放正式编码。

## 输出文件

- 接收目录规范：`03_corpus/return_intake_folder_protocol.md`
- 接收登记模板：`03_corpus/manual_review_return_intake_register_template_v1.csv`
- 目录与接收规则表：`03_corpus/manual_review_return_intake_folder_rules_v1.csv`
