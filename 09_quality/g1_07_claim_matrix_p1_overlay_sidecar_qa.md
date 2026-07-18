# G1-07-CLAIM-MATRIX-P1-OVERLAY-SIDECAR-QA 主张矩阵P1覆盖侧车检查

## 检查结论

`09_quality/g1_07_claim_matrix_p1_overlay_application.csv` 通过本轮QA。该文件可以作为后续主张矩阵安全合并的依据，但不等同于 `09_quality/claim_evidence_matrix.csv` 已经合并或更新。

本轮继续不直接修改 `09_quality/claim_evidence_matrix.csv`，不升级任何主张状态或证据等级。

## 检查范围

本轮检查以下文件：

- `09_quality/g1_07_claim_matrix_p1_overlay_application.csv`
- `09_quality/g1_07_claim_matrix_p1_overlay_application.md`
- `09_quality/g1_07_claim_matrix_boundary_overlay.csv`
- `09_quality/claim_evidence_matrix.csv`

检查对象为7个 `claim_id`：`C3-01`、`C3-02`、`C4-01`、`C4-02`、`C5-01`、`C5-02`、`C2-06`。

## 通过项

| 检查项 | 结论 |
| --- | --- |
| CSV编码 | UTF-8 BOM，LF换行 |
| 行数 | 7条覆盖记录 |
| `claim_id` 覆盖 | 7条目标主张完整，无新增无遗漏 |
| 来源覆盖表匹配 | 7条均可匹配 `g1_07_claim_matrix_boundary_overlay.csv` |
| 主张矩阵行匹配 | 7条均可匹配当前工作区 `claim_evidence_matrix.csv` 行 |
| 当前状态一致性 | `current_status` 与矩阵 `status` 一致 |
| 当前证据等级一致性 | `current_evidence_level` 与矩阵 `evidence_level` 一致 |
| 边界覆盖语句一致性 | `boundary_overlay` 与来源覆盖表一致 |
| 后续动作建议一致性 | `proposed_action_overlay` 与来源覆盖表一致 |
| 状态升级门禁 | 7条 `status_upgrade_allowed` 均为“否” |
| 证据等级升级门禁 | 7条 `evidence_level_upgrade_allowed` 均为“否” |
| 直接改矩阵门禁 | 7条 `direct_matrix_edit_this_task` 均为“否” |

## 保留风险

`09_quality/claim_evidence_matrix.csv` 当前仍存在历史未提交差异。本轮QA确认侧车文件可用，但不能把侧车文件理解为矩阵本体已经安全更新。

后续若要合并矩阵，必须另设任务，并满足：

1. 矩阵历史差异已被隔离、确认或单独处理；
2. 只处理7个目标 `claim_id`；
3. 只补充风险边界和后续动作；
4. 不改写主张本身，不升级 `status`，不升级 `evidence_level`；
5. 提交前能证明暂存范围没有混入其他矩阵行、正文文件或原始材料。

## 禁止声称

通过本轮QA后，仍不能声称：

- 正式编码已经完成；
- 正式统计结果已经成立；
- 专家审查、双评分者一致性或分歧裁决已经完成；
- 第四章内部预演数字可以进入摘要、结论或正式结果章；
- 第五章候选案例已经成为正式代表性案例；
- 教师困难、学生困难、课堂可行性或教学效果已经得到验证。

## 下一最小任务

建议执行 `G1-07-CLAIM-MATRIX-P1-OVERLAY-MERGE-READINESS`：在不直接改矩阵的前提下，判断是否有必要进入字段级安全合并；若矩阵历史差异仍不可隔离，则保持侧车引用，转回人工终核销项或正式编码输入准备。
