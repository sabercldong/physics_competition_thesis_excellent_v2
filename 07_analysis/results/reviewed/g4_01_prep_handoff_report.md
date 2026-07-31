# G4-01-PREP 评分者交接检查报告

更新时间：2026-07-14

## 性质声明

本报告用于检查是否具备向真实评分者交接编码材料的最低条件。它不代表真实评分者已经开始编码，也不代表正式编码、裁决或结果分析已经完成。

## 检查结论

可以进入评分者交接准备，但不能进入正式结果分析。

## 交接包清单

| artifact_id | path | exists | type | row_count | handoff_use |
| --- | --- | --- | --- | --- | --- |
| coding_manual_internal | 04_framework/coding_manual_v2_internal.md | 是 | markdown |  | 评分者交接准备 |
| codebook_internal | 04_framework/codebook_v2_internal.csv | 是 | csv | 16 | 评分者交接准备 |
| rater_a_template | 07_analysis/data/formal_coding_rater_A_template.csv | 是 | csv | 876 | 评分者交接准备 |
| rater_b_template | 07_analysis/data/formal_coding_rater_B_template.csv | 是 | csv | 876 | 评分者交接准备 |
| adjudication_template | 07_analysis/data/formal_adjudication_template.csv | 是 | csv | 876 | 评分者交接准备 |
| rater_briefing | 07_analysis/results/reviewed/prep30_rater_briefing.md | 是 | markdown |  | 评分者交接准备 |
| adjudication_protocol | 07_analysis/results/reviewed/prep30_adjudication_protocol.md | 是 | markdown |  | 评分者交接准备 |
| gate_register | 07_analysis/results/reviewed/prep30_gate_register.csv | 是 | csv | 5 | 评分者交接准备 |
| field_validation | 07_analysis/results/reviewed/prep30_formal_coding_field_validation.csv | 是 | csv | 5 | 评分者交接准备 |
| manual_priority | 07_analysis/results/reviewed/prep30_manual_priority_queue.csv | 是 | csv | 154 | 评分者交接准备 |

## 检查结果

| check_id | check_item | status | evidence | action |
| --- | --- | --- | --- | --- |
| HANDOFF-01 | 评分者A空白模板存在且记录数为876 | 通过 | formal_coding_rater_A_template.csv rows=876 | 若未通过，重新生成模板。 |
| HANDOFF-02 | 评分者B空白模板存在且记录数为876 | 通过 | formal_coding_rater_B_template.csv rows=876 | 若未通过，重新生成模板。 |
| HANDOFF-03 | 裁决模板存在且记录数为876 | 通过 | formal_adjudication_template.csv rows=876 | 若未通过，重新生成模板。 |
| HANDOFF-04 | 正式分析门槛仍未满足 | 通过 | 未满足门槛=5 | 允许进入评分者交接准备，但不得生成正式结果。 |
| HANDOFF-05 | 人工校对优先队列存在 | 通过 | prep30_manual_priority_queue.csv rows=154 | 评分者遇到未销项材料时标待核实。 |

## 交接时必须说明

1. 评分者只能依据原始题面、参考解答、题图和正式手册判断；
2. 不得复制 Codex 内部试编码或内部建议；
3. 证据句必须能定位到题干、参考解答或题图；
4. 遇到 OCR、公式、题图或分值边界未销项问题，应标记待核实；
5. 两名评分者必须独立填写，完成后再进行一致性计算和分歧裁决。

## 下一步最小任务

`G4-01`：由两名真实评分者分别填写 `formal_coding_rater_A_template.csv` 和 `formal_coding_rater_B_template.csv`。在此之前，论文正文只能写方法准备和内部预演，不能写正式结果。
