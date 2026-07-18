# G1-07-MANUSCRIPT-BOUNDARY-P1-APPLY-SAFE 应用记录

更新时间：2026-07-19

## 性质声明

本记录说明 `G1-07-MANUSCRIPT-BOUNDARY-P1-PLAN` 中4条正文P1门禁句的安全应用情况。本轮只应用PATCH-003、PATCH-007、PATCH-008和PATCH-009，不直接修改 `09_quality/claim_evidence_matrix.csv`，不填写真实校对人、真实校对日期、评分者、专家意见、统计结果、教师证据、课堂材料或教学效果。

## 已应用内容

| 应用项 | 来源补丁 | 文件 | 位置 | 应用边界 |
|---|---|---|---|---|
| P1-APPLY-001 | PATCH-003 | `08_manuscript/03_methods.md` | 3.9本章小结 | 第4章在正式回填、评分者记录和裁决表形成前保持占位版 |
| P1-APPLY-002 | PATCH-007 | `08_manuscript/05_cases_and_diagnosis.md` | 章首说明 | 候选案例需按A/B/C/D人工终核回填包确认后才能升级 |
| P1-APPLY-003 | PATCH-008 | `08_manuscript/05_cases_and_diagnosis.md` | 5.1候选池说明 | 候选小问只能用于证据表准备，不能进入摘要、结论或教学建议 |
| P1-APPLY-004 | PATCH-009 | `08_manuscript/05_cases_and_diagnosis.md` | 5.8本章小结 | 无真实教师、学生或课堂材料时只能写设计建议，不能写教学诊断或教学效果评价 |

## 未应用内容

- PATCH-010涉及 `09_quality/claim_evidence_matrix.csv`，该矩阵仍存在历史未提交改动，本轮继续隔离；
- 本轮不新增案例分析、候选案例、正式编码数字、正式统计表、专家审查结论、教师验证结论或课堂效果表述；
- 本轮不处理第4章结果占位，也不改变P0门禁句。

## 禁止声称

本轮应用后，仍不得声称人工校对完成、正式评分者编码完成、分歧裁决完成、`final_coding.csv` 已形成、正式统计完成、显著性结论成立、专家审查完成、教师验证完成或课堂效果成立。

## 下一步最小任务

`G1-07-MANUSCRIPT-BOUNDARY-P1-QA`：检查4条P1门禁句是否均已落入正确章节，确认 `09_quality/claim_evidence_matrix.csv` 未被本轮修改，且“教学效果”“课堂可行性”“显著提升”等高风险词均处于禁止语境。

## 输出文件

- 应用记录报告：`09_quality/g1_07_manuscript_boundary_p1_apply_log.md`
- 应用记录表：`09_quality/g1_07_manuscript_boundary_p1_apply_log.csv`
