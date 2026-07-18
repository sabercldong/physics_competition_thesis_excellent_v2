# G1-07-MANUSCRIPT-BOUNDARY-P1-QA P1正文门禁句应用范围检查

更新时间：2026-07-19

## 性质声明

本报告只检查 `G1-07-MANUSCRIPT-BOUNDARY-P1-APPLY-SAFE` 中4条P1正文门禁句的落位、范围和证据边界。本轮不继续改写正文，不修改 `09_quality/claim_evidence_matrix.csv`，不填写真实校对人、真实校对日期、评分者、专家意见、统计结果、教师证据、课堂材料或教学效果。

## QA结论

- 4条P1正文门禁句均已落入预期位置：第3章1条，第5章3条。
- `09_quality/claim_evidence_matrix.csv` 未出现 `g1_07_manuscript_boundary_p1_apply`、`P1-APPLY` 或本轮PATCH-003/007/008/009应用标记。
- 最新提交 `5d507db` 的文件列表不包含 `09_quality/claim_evidence_matrix.csv`，说明主张矩阵未被本轮应用任务纳入提交。
- 关键词扫描命中“显著提升”“课堂效果”“教学诊断”“课堂可行性”“专家审查”等高风险词，但均处于“不证明、不能写成、不得声称、准备材料或需真实证据”的限制语境。
- 本轮QA没有发现P1应用任务新增正式结果数字、显著性结论、专家审查完成、教师验证完成或课堂效果成立的越界表述。

## 逐项检查摘要

| 检查项 | 文件 | 位置 | 结论 |
|---|---|---|---|
| QA-001 | `08_manuscript/03_methods.md` | 第61行，3.9本章小结 | 通过：第4章在真实回填、A/B评分者记录和裁决表形成前保持占位版 |
| QA-002 | `08_manuscript/05_cases_and_diagnosis.md` | 第7行，章首说明 | 通过：候选案例需按A/B/C/D人工终核回填包确认 |
| QA-003 | `08_manuscript/05_cases_and_diagnosis.md` | 第21行，5.1候选池前 | 通过：候选小问不得在裁决表形成前进入摘要、结论或教学建议 |
| QA-004 | `08_manuscript/05_cases_and_diagnosis.md` | 第105行，5.8本章小结 | 通过：无真实教师、学生或课堂材料时只能写设计建议 |
| QA-005 | `09_quality/g1_07_manuscript_boundary_p1_apply_log.csv` | 全表 | 通过：5条记录中4条已应用、1条PATCH-010明确未应用 |
| QA-006 | `09_quality/claim_evidence_matrix.csv` | 全表 | 通过：未发现本轮P1应用标记或应用日志来源 |
| QA-007 | 最新提交 `5d507db` | 文件列表 | 通过：提交范围不包含 `claim_evidence_matrix.csv` |
| QA-008 | 第3章/第5章 | 高风险词扫描 | 通过：“显著提升”“课堂效果”等处于禁止或不证明语境 |
| QA-009 | 第3章/第5章 | 专家/正式结果词扫描 | 通过：“专家审查”“正式结果”等处于准备、未完成或不得升级语境 |
| QA-010 | 当前工作区 | 历史改动隔离 | 通过：第3章、第5章和主张矩阵仍有历史未提交改动，未被QA任务改写或暂存 |

## 剩余风险

1. 第3章、第5章和 `09_quality/claim_evidence_matrix.csv` 仍保留历史未提交改动，本轮QA不判定这些历史改动整体可提交。
2. 主张矩阵P1覆盖建议尚未应用；需要单独处理 `09_quality/g1_07_claim_matrix_boundary_overlay.csv` 与 `claim_evidence_matrix.csv` 的关系。
3. 真实人工终核、真实A/B评分者编码、分歧裁决和 `final_coding.csv` 仍不存在，因此第4章仍只能是结果占位，第5章仍只能是候选案例与教学转化证据准备。

## 下一步最小任务

`G1-07-CLAIM-MATRIX-P1-OVERLAY-PLAN`：在不直接改动 `09_quality/claim_evidence_matrix.csv` 的前提下，评估7条主张矩阵覆盖建议应如何安全落地；若矩阵历史改动仍无法隔离，则先生成独立覆盖审计说明，不升级任何主张状态。

## 输出文件

- QA报告：`09_quality/g1_07_manuscript_boundary_p1_qa.md`
- QA表：`09_quality/g1_07_manuscript_boundary_p1_qa.csv`
