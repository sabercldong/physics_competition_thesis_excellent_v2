# R01 V2逐条证据补正回填接收检查

接收日期：2026-07-23
任务：`G4-10-R01-EVIDENCE-SUPPLEMENT-V2-INTAKE`

## 接收与声明登记

- 外部副本：`/Users/dongxingxi/Desktop/论文人工复核回填/R01/r01_evidence_supplement_R01_FILLED_20260723_V2.csv`
- 原样归档：`07_analysis/data/rater_returns/incoming/R01/r01_evidence_supplement_R01_FILLED_20260723_V2.csv`
- 原件SHA-256：`f0f473808c6943a1481334948338a086a9984eb2fd9aedeefee0bb25e5cbbdc6`
- LF登记副本：`07_analysis/data/rater_returns/registered/R01/r01_evidence_supplement_R01_FILLED_20260723_V2_registered_lf.csv`
- 登记副本SHA-256：`f0ec21060a59c381764770e84b3628e7795d73ca665b53d94aab1afd6545f06b`

R01自声明于2026-07-23独立核对219个`item_id`和876行记录。本项目只登记该声明，不能独立验证实际复核过程或身份。

## 检查结论

结构检查8/8通过：876行、不可变键与模板同序、工作字段完整、枚举值和存在性—等级逻辑均合格。

内容检查不通过：

| 内容门禁 | 观察值 | 要求 |
|---|---:|---:|
| 题干与解答引文均可在对应`item_text`逐字定位 | 528/876 | 876/876 |
| 至少一侧不可定位但标为“充分” | 348 | 0 |
| 题干引文为禁止占位文本 | 20 | 0 |
| 题干引文不可定位 | 300 | 0 |
| 解答引文不可定位 | 268 | 0 |
| 相邻等级排除理由为通用句式 | 240 | 0 |
| 需返工的唯一记录 | 513 | 0 |

详细机器结果见`r01_evidence_supplement_v2_return_content_qa_v1.csv`和`r01_evidence_supplement_v2_rework_qa_v1.csv`；逐行返工入口见`r01_evidence_supplement_v2_rework_list_v1.csv`。

## 状态与后续动作

本V2副本登记为**已接收、结构通过、内容不放行**。不得解除`final_coding.csv`、第四章或第五章的暂定结果门禁。

返工时只处理清单中的513条；每条必须替换为对应`item_text_path`中可逐字定位的题干和解答原文，并按该题实际任务重写相邻等级排除理由。禁止将“补充引用材料中的相关文本以确保长度满足要求”或任何概括性标签作为引文。提交新版本时不得覆盖本原件。
