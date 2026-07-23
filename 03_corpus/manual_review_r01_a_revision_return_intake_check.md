# G1-07-R01-A-RETURN-REVISION-INTAKE R01 A组重填副本接收检查

接收日期：2026-07-23

## 接收结论

已收到R01自声明于2026-07-23独立人工复核完成的A组重填副本。该副本与2026-07-22已归档原件覆盖相同的76个`issue_id`、38个`material_id`，不可变字段差异为0，且所有必填回填字段、决定选项与项目内证据路径均通过接收检查。

新版的`correction_summary`相对旧版76行均有更新。其中第37、38届的32行是材料特异摘要；第40、41、42届仍有44行使用两种通用句式。故该副本登记为“已接收的部分增强回填”，不应表述为76行均已形成针对性摘要，也不关闭A组的逐项内容充分性门禁。

## 文件登记

| 角色 | 路径 | SHA-256 | 字节数 |
|---|---|---|---:|
| 旧版原始副本 | `03_corpus/manual_review_returns/incoming/REAL-P1/return_20260722_A_R01_filled.csv` | `04d163df839c0fe3c9e9f6a86af44dfad6d2d0c38f10262dede37c70ec66defb` | 114325 |
| 本次原始副本 | `03_corpus/manual_review_returns/incoming/REAL-P1/return_20260723_A_R01_refilled.csv` | `2d5fb6c87b3adbbc12826bd78cfef9007f2ea220c3b35b61d2ae6287c64bcf3b` | 126538 |
| 本次LF登记副本 | `03_corpus/manual_review_returns/registered/REAL-P1/return_20260723_A_R01_refilled_registered_lf.csv` | `0828e27cbb446886a11a09c2d9f7f85d089a6daeed5870066332dc808598388f` | 126461 |

原始副本已按接收协议只读保存，未覆盖2026-07-22原件。登记副本只规范化换行，CSV字段和值与原始副本一致。

## 检查结果

| 项目 | 结果 |
|---|---|
| 行数、问题集合、不可变字段 | 76行；76/76问题集合一致；差异0 |
| 回填字段与决定选项 | 76/76完整；R01与2026-07-23均为76/76；76/76决定属于允许选项 |
| 复核后证据路径 | 452/452项目内路径存在 |
| 相对旧版摘要更新 | 76/76发生变化 |
| 材料特异摘要 | 32/76；第37、38届各16行 |
| 通用摘要待补强 | 44/76；第40届16行、第41届14行、第42届14行 |

详细逐行差异与分类见`03_corpus/manual_review_r01_a_revision_return_diff_v1.csv`，机器检查见`03_corpus/manual_review_r01_a_revision_return_intake_qa_v1.csv`。

## 使用边界

- 本检查只登记R01自声明，不独立认证复核身份或复核过程。
- 该重填副本仅涉及A组题干/OCR和公式复核记录，不能替代`07_analysis`中876行编码证据补正回填。
- 未关闭任何`manual_review_checklist.csv`条目，未放行`final_coding.csv`、第四章或第五章正式结论。
- 若要使A组76行均满足“针对性摘要”要求，须只重填第40—42届44行的`correction_summary`，保留本原件并另交新版本。
