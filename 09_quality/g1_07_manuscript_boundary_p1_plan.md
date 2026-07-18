# G1-07-MANUSCRIPT-BOUNDARY-P1-PLAN P1正文门禁补丁应用路线评估

更新时间：2026-07-19

## 性质声明

本报告只评估 `G1-07-MANUSCRIPT-BOUNDARY-PATCH-PLAN` 中P1级正文门禁补丁的应用路线，不直接改写第3章、第5章正文，不直接修改 `09_quality/claim_evidence_matrix.csv`。本轮也不填写真实校对人、真实校对日期、评分者、专家意见、统计结果、教师证据、课堂材料或教学效果。

## 评估依据

- `03_corpus/manual_review_closure_ready_report.md`：154项人工校对入口已覆盖，但真实人工销项数为0。
- `09_quality/g1_07_no_true_review_manuscript_boundary_map.md`：第3、4、5章只能保留准备状态、结果占位、候选案例和证据需求。
- `09_quality/g1_07_manuscript_boundary_patch_plan.csv`：P1候选包括 PATCH-003、PATCH-007、PATCH-008、PATCH-009 和 PATCH-010。
- `09_quality/g1_07_manuscript_boundary_patch_qa.md`：P0补丁已通过范围检查，第5章P1句和主张矩阵未被混入。
- 当前工作区状态：`08_manuscript/03_methods.md`、`08_manuscript/05_cases_and_diagnosis.md` 和 `09_quality/claim_evidence_matrix.csv` 仍有历史未提交改动，后续不能使用全量暂存。

## 总体判断

P1补丁的作用不是生成新正文结论，而是给后续正式写作加护栏。当前建议如下：

1. PATCH-003、PATCH-007、PATCH-008、PATCH-009 可进入下一轮安全应用任务；它们只强化“占位、候选、待核实、不能写成正式结论”的边界。
2. PATCH-010 暂不直接应用到 `claim_evidence_matrix.csv`；主张矩阵已有历史未提交改动，且覆盖建议涉及多个claim_id，宜单独开一个矩阵覆盖任务。
3. 下一轮若应用正文P1句，应只处理4条最小句，不新增案例分析、教学诊断、课堂效果、正式编码数字或主张状态升级。
4. 若真实人工终核回填、真实A/B评分者模板或裁决数据先到，则暂停P1正文补丁，优先做真实材料回收完整性检查。

## P1逐项评估

| 补丁 | 文件 | 位置 | 结论 | 理由 |
|---|---|---|---|---|
| PATCH-003 | `08_manuscript/03_methods.md` | 3.9本章小结 | 可应用 | 只强化第4章仍为占位版，和P0门禁一致；风险低。 |
| PATCH-007 | `08_manuscript/05_cases_and_diagnosis.md` | 章首说明 | 可应用 | 将候选案例与A/B/C/D人工终核回填包连接，避免把候选案例误写成正式案例。 |
| PATCH-008 | `08_manuscript/05_cases_and_diagnosis.md` | 5.1候选池表格附近 | 可应用 | 明确候选小问不能进入摘要、结论或教学建议，能保护后续写作边界。 |
| PATCH-009 | `08_manuscript/05_cases_and_diagnosis.md` | 5.8本章小结 | 可应用 | 强化没有真实教师、学生或课堂材料时，只能写设计建议，不能写教学诊断或教学效果。 |
| PATCH-010 | `09_quality/claim_evidence_matrix.csv` | 多个claim_id | 暂缓 | 涉及矩阵历史未提交改动和多条主张状态，需独立任务精确处理。 |

## 后续安全应用建议

建议下一最小任务设为 `G1-07-MANUSCRIPT-BOUNDARY-P1-APPLY-SAFE`。该任务只做以下四件事：

1. 在第3章3.9小结补入“第4章保持占位版”的边界句；
2. 在第5章章首补入“候选案例仍需A/B/C/D人工终核”的边界句；
3. 在第5章5.1补入“候选小问不能进入摘要、结论或教学建议”的边界句；
4. 在第5章5.8补入“无教师、学生或课堂材料时只能写设计建议”的边界句。

该任务不得编辑 `09_quality/claim_evidence_matrix.csv`。主张矩阵建议另设 `G1-07-CLAIM-MATRIX-P1-OVERLAY-SAFE`，只基于 `09_quality/g1_07_claim_matrix_boundary_overlay.csv` 做覆盖或生成不改原表的审计说明。

## 禁止声称

P1补丁应用前后，都仍不得声称：

- 154项人工校对已经真实销项；
- 正式A/B评分者独立编码已经完成；
- 分歧裁决或 `final_coding.csv` 已经形成；
- 第4章已有正式维度分布、等级分布、共现模式、趋势或显著性结论；
- 第5章已有正式代表性案例、质疑创新结论、教学诊断、课堂可行性或教学效果；
- 主张证据矩阵中的C3/C4/C5相关主张已经升级为已核验或已完成。

## 下一步最小任务

`G1-07-MANUSCRIPT-BOUNDARY-P1-APPLY-SAFE`：在完整查看目标正文差异后，只应用PATCH-003、PATCH-007、PATCH-008和PATCH-009四条正文P1门禁句；继续隔离 `09_quality/claim_evidence_matrix.csv`，不补造任何正式结果或教学证据。

## 输出文件

- P1路线评估报告：`09_quality/g1_07_manuscript_boundary_p1_plan.md`
- P1路线评估表：`09_quality/g1_07_manuscript_boundary_p1_plan.csv`
