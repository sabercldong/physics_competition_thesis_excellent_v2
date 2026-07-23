# R01 V6逐条证据补正回填接收检查

接收日期：2026-07-23
任务：`G4-14-R01-EVIDENCE-SUPPLEMENT-V6-INTAKE`

## 接收与声明登记

- 外部副本：`/Users/dongxingxi/Desktop/论文人工复核回填/R01/r01_evidence_supplement_R01_FILLED_20260723_V6.csv`
- 原样归档：`07_analysis/data/rater_returns/incoming/R01/r01_evidence_supplement_R01_FILLED_20260723_V6.csv`
- 原件SHA-256：`66dfb7060d9fb0d7686d9f691f8896a59b6b52182afb83c3f6b3fc96adf4404c`
- LF登记副本：`07_analysis/data/rater_returns/registered/R01/r01_evidence_supplement_R01_FILLED_20260723_V6_registered_lf.csv`
- 登记副本SHA-256：`5d1357012b01febbb22359ef1344804345f763b5e19a5e6129885ea5a1f96c0b`

R01自声明于2026-07-23独立核对219个`item_id`和876行记录。本项目只记录该声明，不能独立验证实际复核过程或身份。

## 全量接收门禁

结构检查8/8通过，内容定位检查7/7通过，返工清单为0条：

| 门禁 | 结果 |
|---|---:|
| 题干引语可在对应`item_text`逐字定位 | 876/876 |
| 解答引语可在对应`item_text`逐字定位 | 876/876 |
| 题干与解答均可定位 | 876/876 |
| “充分”但至少一侧不可定位 | 0 |
| 禁止占位文本 | 0 |
| 通用等级边界理由 | 0 |

V5遗留7条解答引文均已替换并通过定位。V6由此通过**结构和逐字定位门禁**。

## 尚未关闭的实质审查

逐字定位不自动证明引用内容足以支持当前维度与等级。补充候选审计发现58条需实质审查：54条解答引文少于8个非空字符，4条题干和解答引文完全相同。短公式可以是有效证据，因此该审计只建立候选清单，不单独判定记录错误。

候选入口：`r01_evidence_supplement_v6_substantive_review_candidates_v1.csv`；统计：`r01_evidence_supplement_v6_substantive_candidate_qa_v1.csv`。

## 状态与后续动作

V6状态为**已接收、结构和定位门禁通过、实质证据审查待完成**。它可作为后续逐条审查的唯一候选输入，但尚不得解除`final_coding.csv`、第四章或第五章的暂定结果门禁。

下一最小任务是审查候选清单的58条，确认每条解答引文能实质支持当前维度、存在性和等级；必要时补充更完整引文或形成“建议更正”裁决输入。随后再进行高风险与抽样记录的编码实质审查。
