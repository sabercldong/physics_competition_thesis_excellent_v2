# P0第一批真实人工回填模板说明

任务编号：`G1-07-FOLLOWUP-MANUAL-P0-BATCH1-RETURN-TEMPLATE`

## 性质声明

本文件说明 `03_corpus/manual_review_p0_batch1_return_template_v1.csv` 的用途和填写边界。该模板只为后续真实人工校对预留回填字段，不代表已经发生人工校对，不关闭任何待核项，不填写校对人、日期或校对结论，不修改题文，不生成正式编码、正式统计或论文正文。

## 模板范围

模板覆盖P0第一批38个题目级小批次，对应第一批76条高风险OCR、公式与特殊符号待核项。每行继承：

- 小批次编号；
- 题目材料编号；
- 届次、年份、题号；
- 原始队列ID；
- 原始问题ID；
- 受影响分析单元；
- 来源文件、题面页和答案页；
- 最低核对输入。

## 预留回填字段

模板预留以下真实回填字段：

| 字段 | 用途 |
|---|---|
| `reviewer_name` | 真实校对人姓名或匿名编号 |
| `review_date` | 真实校对日期 |
| `source_pages_checked` | 实际核对的题面页、答案页或页面证据 |
| `ocr_decision` | OCR决定：确认无误、需修订、继续待核 |
| `formula_decision` | 公式决定：确认无误、需修订、继续待核 |
| `text_revision_needed` | 是否需要修订题文 |
| `formula_revision_needed` | 是否需要修订公式或特殊符号 |
| `revision_locations` | 需修订位置 |
| `evidence_note` | 支撑判断的证据摘记 |
| `remaining_uncertainty` | 未解决疑点 |
| `allow_formal_rater_template` | 是否允许进入正式评分者模板 |
| `blocking_reason_if_not_allowed` | 若不允许，说明阻断原因 |
| `files_to_update_after_return` | 回填后需更新的项目文件 |
| `return_file_path` | 真实回填副本路径 |
| `return_checksum` | 回填副本校验值 |
| `integration_status` | 整合状态 |

## 当前填写状态

当前所有真实回填字段均保持空白或“未回填”。38行 `release_status` 均为：

`不放行：空白回填模板`

因此，本模板不能作为人工校对完成证明，也不能作为正式编码、正式统计或论文结果的依据。

## 后续使用规则

真实回填时应复制或更新模板，并逐行填写校对人、日期、决定、证据和放行判断。若某题仍存在疑点，应在 `remaining_uncertainty` 和 `blocking_reason_if_not_allowed` 中写明，不得强行放行。

若回填结果需要修改题文、索引、公式核对表或正式评分者模板，应先记录 `files_to_update_after_return`，再按单题或小批次单独提交，避免混入历史脏文件。

## 禁写边界

本任务完成后仍不得声称：

- P0第一批已经真实人工校对完成；
- 38个题目级小批次已经销项；
- 第37、38、40、41、42届题文已经正式无误；
- 所有P0条目可以进入正式评分者模板；
- 已生成正式 `final_coding.csv`；
- 第四章正式统计或论文结果已经成立。

## 下一最小任务

下一步可执行 `G1-07-FOLLOWUP-MANUAL-P0-BATCH1-RETURN-TEMPLATE-QA`：检查回填模板的CSV编码、编号连续性、38个小批次覆盖、真实回填字段空白状态、来源映射和禁写边界。
