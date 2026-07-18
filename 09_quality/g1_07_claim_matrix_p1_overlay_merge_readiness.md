# G1-07-CLAIM-MATRIX-P1-OVERLAY-MERGE-READINESS 主张矩阵P1覆盖合并准备度判断

## 判断结论

本轮不建议将7条P1侧车覆盖立即合并进 `09_quality/claim_evidence_matrix.csv`。

理由是：侧车文件已经完整记录7条边界，且通过QA；但 `09_quality/claim_evidence_matrix.csv` 当前相对Git基线仍是整块历史差异，表现为从表头扩展到19条主张行。若现在直接合并7条字段级边界，容易把历史矩阵扩展一并纳入本轮提交，超出本任务范围。

因此，本轮结论为：保持侧车引用，暂不合并矩阵本体。

## 依据

已核查文件：

- `09_quality/g1_07_claim_matrix_p1_overlay_application.csv`
- `09_quality/g1_07_claim_matrix_p1_overlay_application.md`
- `09_quality/g1_07_claim_matrix_p1_overlay_sidecar_qa.csv`
- `09_quality/g1_07_claim_matrix_p1_overlay_sidecar_qa.md`
- `09_quality/g1_07_claim_matrix_boundary_overlay.csv`
- `09_quality/claim_evidence_matrix.csv`

关键证据：

- 侧车CSV共7条记录，覆盖 `C3-01`、`C3-02`、`C4-01`、`C4-02`、`C5-01`、`C5-02`、`C2-06`；
- 侧车QA共14项检查，全部通过；
- 7条侧车记录均标明 `status_upgrade_allowed=否`、`evidence_level_upgrade_allowed=否`、`direct_matrix_edit_this_task=否`；
- `claim_evidence_matrix.csv` 当前仍有历史未提交差异，不能在本轮被当作干净合并目标。

## 分项判断

| claim_id | 合并必要性 | 合并风险 | 本轮决定 |
| --- | --- | --- | --- |
| C3-01 | 中 | 中 | 暂缓合并，保持侧车引用 |
| C3-02 | 中 | 中 | 暂缓合并，保持侧车引用 |
| C4-01 | 高 | 高 | 暂缓合并，保持第四章占位和侧车禁写边界 |
| C4-02 | 中 | 高 | 暂缓合并，等待人工终核、真实评分者编码和裁决 |
| C5-01 | 中 | 中 | 暂缓合并，保持候选案例池边界 |
| C5-02 | 高 | 中 | 暂缓合并，保持教学转化禁写边界 |
| C2-06 | 中 | 中 | 暂缓合并，保持文献只能支持设计参照的边界 |

## 可合并条件

只有满足以下条件，才建议另设 `G1-07-CLAIM-MATRIX-P1-OVERLAY-SAFE`：

1. `claim_evidence_matrix.csv` 的历史差异已经被隔离、确认或单独提交；
2. 本轮目标严格限定为7个 `claim_id`；
3. 只更新 `risk` 和 `action` 方向的边界信息；
4. 不改写 `claim`，不升级 `status`，不升级 `evidence_level`；
5. 提交前能证明暂存内容没有混入其他矩阵行、正文文件或原始材料。

## 当前最小推进方向

当前真正阻塞论文材料包进入正式结果和正文落地的，不是侧车是否进矩阵，而是：

- 154项人工终核真实销项数仍为0；
- 正式A/B评分者独立编码未回收；
- 一致性计算和分歧裁决尚未形成；
- `final_coding.csv` 尚未形成；
- 第五章教师、学生或课堂证据仍缺失。

因此，下一步建议从矩阵合并路线转回正式编码前人工终核路线，优先建立可执行的真实销项动作包。

## 下一最小任务

建议执行 `G1-07-MANUAL-CLOSURE-ACTION-PLAN`：把154项人工终核回填包压缩为真实执行顺序、最小校对动作、回填字段和进入正式编码的判定门槛；继续不填写真实校对人、日期或决定。
