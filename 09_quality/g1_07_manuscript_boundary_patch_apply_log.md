# G1-07-MANUSCRIPT-BOUNDARY-PATCH-APPLY-SAFE 应用记录

更新时间：2026-07-19

## 性质声明

本记录说明 `G1-07-MANUSCRIPT-BOUNDARY-PATCH-PLAN` 中P0门禁句的安全应用情况。本轮只应用第三章和第四章的P0句，不应用第五章P1候选句，不直接修改 `09_quality/claim_evidence_matrix.csv`，不填写真实校对人、真实校对日期、评分者、专家意见、统计结果或教学证据。

## 已应用内容

| 应用项 | 来源补丁 | 文件 | 位置 | 应用边界 |
|---|---|---|---|---|
| APPLY-001 | PATCH-001 | `08_manuscript/03_methods.md` | 3.2 | 154项有入口但真实人工销项数为0 |
| APPLY-002 | PATCH-002 | `08_manuscript/03_methods.md` | 3.6 | A/B/C/D回填包可交付但正式人工终核和评分者流程未发生 |
| APPLY-003 | PATCH-004 | `08_manuscript/04_results.md` | 章首说明 | 第四章边界来源化，继续不报告正式结果 |
| APPLY-004 | PATCH-005 | `08_manuscript/04_results.md` | 4.1 | 219个分析单元只作为语料规模说明 |
| APPLY-005 | PATCH-006 | `08_manuscript/04_results.md` | 4.6 | 人工校对门槛细化为A/B/C/D四组均未真实销项 |

## 未应用内容

- PATCH-003、PATCH-007、PATCH-008、PATCH-009 属于P1，等待P0补丁稳定后再处理；
- PATCH-010 涉及 `09_quality/claim_evidence_matrix.csv`，该矩阵已有历史未提交改动，本轮不直接编辑；
- PATCH-011 是跨文件提交隔离约束，不对应正文新增句。

## 禁止声称

本轮应用后，仍不得声称人工校对完成、正式评分者编码完成、分歧裁决完成、正式统计完成、显著性结论成立、专家审查完成、教师验证完成或课堂效果成立。

## 下一步最小任务

`G1-07-MANUSCRIPT-BOUNDARY-PATCH-QA`：检查本轮P0门禁句是否均已落入正确章节，并确认没有混入P1案例句、主张矩阵改动、正式结果数字或教学验证表述。若QA通过，再决定是否应用P1句或回到真实人工回填完整性检查。
