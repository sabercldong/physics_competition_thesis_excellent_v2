# P0第一批真实回填交接材料包索引

任务编号：`G1-07-FOLLOWUP-MANUAL-P0-BATCH1-RETURN-PACKET-INDEX`

## 性质声明

本文件只把P0第一批真实人工回填相关材料收束为一个交接索引。它不代表真实人工校对已经发生，不关闭任何人工校对项，不修改题文，不生成正式编码、正式统计、论文正文或 `final_coding.csv`。

## 材料包结论

当前交接包覆盖6类材料、11个文件：

1. P0第一批小批次入口；
2. 小批次入口QA；
3. 真实人工回填模板；
4. 回填模板QA；
5. 真实校对回填填写说明；
6. 填写说明QA。

上述材料共同说明：P0第一批共有38个题目级小批次，来自76条高风险OCR、公式与特殊符号待核项。当前所有真实回填字段仍为空白或“未回填”，全部保持不放行。

## 推荐交接顺序

1. 先读 `03_corpus/manual_review_p0_batch1_return_instructions.md`，理解字段、允许写法和放行规则；
2. 打开 `03_corpus/manual_review_p0_batch1_return_template_v1.csv`，逐行查看38个待回填小批次；
3. 用 `03_corpus/manual_review_p0_batch1_item_batches_v1.csv` 回查每个小批次的来源问题、题面页、答案页和受影响分析单元；
4. 若怀疑模板或入口字段异常，先看对应QA文件，不要直接改继承字段；
5. 只有完成真实核对后，才可填写校对人、日期、OCR决定、公式决定、证据摘记和放行判断；
6. 回填后仍需进入接收、整合和QA流程，不能直接进入正式编码或论文结果写作。

## 文件清单

| 类别 | 文件 | 作用 | 当前状态 |
|---|---|---|---|
| 小批次入口 | `03_corpus/manual_review_p0_batch1_item_batches.md` | 说明38个题目级小批次的来源、范围和禁写边界 | 可读入口，不放行 |
| 小批次入口 | `03_corpus/manual_review_p0_batch1_item_batches_v1.csv` | 结构化列出38个小批次、76条来源待核项和题面/答案页 | 可作为回查索引，不放行 |
| 入口QA | `03_corpus/manual_review_p0_batch1_item_batches_qa.md` | 记录入口表QA结论和边界 | QA材料，不放行 |
| 入口QA | `03_corpus/manual_review_p0_batch1_item_batches_qa_v1.csv` | 结构化记录29项入口QA检查 | QA材料，不放行 |
| 回填模板 | `03_corpus/manual_review_p0_batch1_return_template.md` | 说明真实回填模板的字段和用途 | 模板说明，不放行 |
| 回填模板 | `03_corpus/manual_review_p0_batch1_return_template_v1.csv` | 38行空白真实回填模板 | 空白模板，不放行 |
| 模板QA | `03_corpus/manual_review_p0_batch1_return_template_qa.md` | 记录回填模板QA结论和边界 | QA材料，不放行 |
| 模板QA | `03_corpus/manual_review_p0_batch1_return_template_qa_v1.csv` | 结构化记录48项模板QA检查 | QA材料，不放行 |
| 填写说明 | `03_corpus/manual_review_p0_batch1_return_instructions.md` | 规定字段填写、OCR/公式判断、放行/阻断逻辑和整合边界 | 操作说明，不放行 |
| 说明QA | `03_corpus/manual_review_p0_batch1_return_instructions_qa.md` | 记录填写说明QA结论和边界 | QA材料，不放行 |
| 说明QA | `03_corpus/manual_review_p0_batch1_return_instructions_qa_v1.csv` | 结构化记录67项说明QA检查 | QA材料，不放行 |

结构化索引见：

- `03_corpus/manual_review_p0_batch1_return_packet_index_v1.csv`

## 交接后的最短流程

真实校对者或后续智能体应按以下流程推进：

`阅读填写说明 -> 打开回填模板 -> 按batch_id核对题面页、答案页、转写稿和公式表 -> 填写真实回填字段 -> 保存回填副本和校验值 -> 进入接收/整合QA -> 决定是否更新人工校对总清单和正式评分者模板`

## 当前仍不能声称

本索引完成后仍不得声称：

- P0第一批真实人工校对已经完成；
- 38个题目级小批次已经销项；
- 第一批76条OCR、公式与特殊符号问题已经关闭；
- 第37、38、40、41、42届题文已经正式无误；
- P0条目可以全部进入正式评分者模板；
- 真实双评分者编码、一致性检验、分歧裁决或 `final_coding.csv` 已经完成；
- 第四章正式统计、典型案例结论或论文结果已经成立。

## 下一最小任务

下一步可执行 `G1-07-FOLLOWUP-MANUAL-P0-BATCH1-RETURN-PACKET-INDEX-QA`：检查交接包索引是否覆盖6类材料、11个文件、路径可定位、CSV编码换行、编号连续和禁写边界。
