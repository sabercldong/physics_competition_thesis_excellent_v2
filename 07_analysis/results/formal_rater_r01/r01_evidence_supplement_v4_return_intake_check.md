# R01 V4逐条证据补正回填接收检查

接收日期：2026-07-23
任务：`G4-12-R01-EVIDENCE-SUPPLEMENT-V4-INTAKE`

## 接收与声明登记

- 外部副本：`/Users/dongxingxi/Desktop/论文人工复核回填/R01/r01_evidence_supplement_R01_FILLED_20260723_V4.csv`
- 原样归档：`07_analysis/data/rater_returns/incoming/R01/r01_evidence_supplement_R01_FILLED_20260723_V4.csv`
- 原件SHA-256：`f63300ee644931dc2164cd98596d40ebd1c4bf5bd1a1569d08ab5a53086d02fb`
- LF登记副本：`07_analysis/data/rater_returns/registered/R01/r01_evidence_supplement_R01_FILLED_20260723_V4_registered_lf.csv`
- 登记副本SHA-256：`971395fee15d34f096d349e213a9601e624ebe1b532fbe4a8e38b2323ed8c95d`

R01自声明于2026-07-23独立核对219个`item_id`和876行记录。本项目只登记该声明，不能独立验证实际复核过程或身份。

## 检查结论

结构检查8/8通过。内容门禁已显著改善，但仍差12条解答引文：

| 内容门禁 | V4观察值 | 要求 |
|---|---:|---:|
| 题干引语可在对应`item_text`逐字定位 | 876/876 | 876/876 |
| 解答引语可在对应`item_text`逐字定位 | 864/876 | 876/876 |
| 题干与解答均可定位 | 864/876 | 876/876 |
| “充分”但至少一侧不可定位 | 12 | 0 |
| 禁止占位文本 | 0 | 0 |
| 通用等级边界理由 | 0 | 0 |
| 需返工的唯一记录 | 12 | 0 |

V3至V4共替换348条题干引文和348条解答引文，双侧可定位数从528条提升至864条。剩余12条均只缺解答引文，集中在三个小问的四个维度：`CPHO39-Q06-3`、`CPHO40-Q07-3`、`CPHO40-Q08-2`。

## 状态与后续动作

本V4副本登记为**已接收、结构通过、内容暂不放行**。不得解除`final_coding.csv`、第四章或第五章的暂定结果门禁。

下一步只需修复`r01_evidence_supplement_v4_rework_list_v1.csv`中的12条`solution_step_quote`：从对应的同一`item_text_path`中复制实际参考解答连续原文，并确认每段可逐字搜索命中。题干、定位和等级边界理由均无需重做；不得覆盖V4原件。
