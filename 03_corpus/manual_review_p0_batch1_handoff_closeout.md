# P0第一批真实核对交接链收束

任务编号：`G1-07-FOLLOWUP-MANUAL-P0-BATCH1-HANDOFF-CLOSEOUT`

## 性质声明

本文件是一页式交接说明，用来告诉其他智能体或真实校对者：P0第一批38个题目级小批次应从哪里领取、看哪些材料、把结果写到哪里、完成后如何进入接收与整合。它只收束交接链，不填写真实校对结果。

本任务不填写校对人、校对日期、OCR决定、公式决定、修订位置、证据摘记、专家意见、导师意见、竞赛教师意见或评分者结果；不创建 `03_corpus/manual_review_returns/`；不关闭38个小批次；不生成正式编码、正式统计、论文结果章或 `07_analysis/data/final_coding.csv`；不修改 `00_originals/`、题文原件、论文正文或主张证据矩阵。

## 领取入口

其他智能体或真实校对者只需要从这里开始：

1. 打开 `03_corpus/manual_review_p0_batch1_agent_task_cards_v1.csv`；
2. 领取一个 `task_card_id`，例如 `P0B1CARD-01`；
3. 按同一行的 `batch_id`、`return_id`、`material_id`、题面页、答案页和支持文件逐项核对；
4. 将真实校对结果写入 `03_corpus/manual_review_p0_batch1_return_template_v1.csv` 的对应 `return_id` 行，或写入按接收规则另存的真实回填副本；
5. 如果发现仍需修订或继续待核，必须写明证据摘记、修订位置、剩余疑点和阻断原因。

## 当前覆盖

- 小批次数：38个，`P0B1-01` 至 `P0B1-38`；
- 任务卡数：38张，`P0B1CARD-01` 至 `P0B1CARD-38`；
- 回填模板行：38行，`P0B1RET-01` 至 `P0B1RET-38`；
- 待核问题：76条高风险OCR、公式与特殊符号问题；
- 届次覆盖：第37届8题, 第38届8题, 第40届8题, 第41届7题, 第42届7题；
- 支持文件：题目文本、V1转写稿、公式核对表路径已通过任务卡QA，缺失0项。

## 必读顺序

| 顺序 | 文件 | 用途 |
|---|---|---|
| 1 | `03_corpus/manual_review_p0_batch1_agent_task_cards_v1.csv` | 领取单题任务 |
| 2 | `03_corpus/manual_review_p0_batch1_return_instructions.md` | 明确字段怎么填、哪些不能改 |
| 3 | `03_corpus/manual_review_p0_batch1_return_template_v1.csv` | 写入真实校对结果或作为真实副本模板 |
| 4 | `03_corpus/manual_review_p0_batch1_return_waiting_room_update.md` | 确认真回填前后的冻结边界 |
| 5 | `03_corpus/manual_review_return_integration_protocol.md` | 真实副本收到后的整合规则 |

结构化收束索引见：

- `03_corpus/manual_review_p0_batch1_handoff_closeout_v1.csv`

## 每题最低交付

每个领取者至少交付以下内容：

- 已核对题面页、答案页、题目文本、V1转写稿和公式核对表；
- 已填写真实校对人和校对日期；
- 已填写 `source_pages_checked`、`ocr_decision`、`formula_decision`；
- 已说明是否需要文字或公式修订；
- 已写明修订位置、证据摘记和剩余疑点；
- 已判断是否允许进入正式评分者模板；
- 若不允许，已写明阻断原因和后续需要补的材料。

## 收到真实回填后的最短流程

1. 复制真实回填副本到接收目录，并登记文件名、路径、校验值、大小、接收日期和接收人；
2. 检查38行结构、不可变字段和必填字段；
3. 对“需修订”或“继续待核”的题目建立修订清单；
4. 对“允许进入正式评分者模板”的题目再做整合QA；
5. 只有整合QA通过后，才能讨论是否更新人工校对总清单或正式评分者模板。

## 禁止事项

- 不得把本交接链写成人工校对完成；
- 不得把任务卡、模板、QA或Codex输出写成真实专家、导师、竞赛教师或评分者意见；
- 不得跳过真实回填副本，直接关闭38个小批次；
- 不得把内部编码复制成 `final_coding.csv`；
- 不得生成第四章正式统计、趋势、共现、显著性或教学效果结论；
- 不得修改 `00_originals/` 或覆盖原始题目文件。

## 当前结论

P0第一批真实核对交接链已经可以被其他智能体领取执行，但当前状态仍是“等待真实回填”。它是交接材料包，不是研究结果，也不是正式编码输入。

## 下一最小任务

下一步建议执行 `G1-07-FOLLOWUP-MANUAL-P0-BATCH1-HANDOFF-CLOSEOUT-QA`：检查本收束说明和结构化索引是否覆盖全部交接链文件、编码换行、路径、冻结状态和禁写边界。
