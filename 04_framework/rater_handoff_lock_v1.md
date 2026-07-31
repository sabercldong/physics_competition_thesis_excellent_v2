# G4-01-PREP-LOCK 评分者交接包冻结说明

更新时间：2026-07-14

## 性质声明

本文件只冻结“评分者交接包”的文件清单、阅读顺序、回收命名规则和未销项风险提示。它不代表正式编码手册V2已经完成真实专家审查，不代表两名评分者已经独立编码，也不代表已经完成一致性检验、分歧裁决或正式结果分析。

## 冻结版本

- 冻结编号：`G4-01-PREP-LOCK-2026-07-14`
- 冻结对象：评分者交接包清单与回收流程
- 允许用途：向评分者A/B交接空白模板、说明评分边界、回收材料前后核对
- 禁止用途：生成正式统计结果、写作第四章正式结果、替代专家审查、替代导师确认、替代真实评分者独立判断

## 交接包阅读顺序

1. `04_framework/analysis_unit_and_coding_definitions_formal_draft.md`
2. `04_framework/codebook_v2_formal_draft.csv`
3. `04_framework/rater_training_manual_formal_draft.md`
4. `04_framework/evidence_note_and_disagreement_protocol_formal_draft.md`
5. `04_framework/boundary_case_bank_formal_draft.csv`
6. `07_analysis/data/formal_coding_rater_A_template.csv` 或 `07_analysis/data/formal_coding_rater_B_template.csv`
7. `04_framework/rater_independent_coding_instructions_v1.md`
8. `04_framework/rater_handoff_file_rules.csv`
9. `04_framework/rater_handoff_unresolved_risks.csv`
10. `04_framework/rater_training_return_checklist.csv`

## 交接边界

- 评分者只能依据原始题面、参考解答、题图和交接包中的操作性定义编码；
- 评分者不得复制 `internal_*`、`batch10_*`、`p0_*`、`p1_*` 或 `prep30_*` 内部预演结论；
- 边界案例库只用于理解风险类型，不是标准答案库；
- 遇到OCR、公式、图注、题图裁边、分值边界或小问拆分疑问时，必须在 `notes` 标记“待核实”，不得强行补齐；
- A/B模板回收前，不得计算一致性；
- 一致性计算后，仍需裁决模板形成唯一分析表，才能进入正式结果表和论文正文结果。

## 发放前最低检查

| 检查项 | 最低要求 | 当前状态 | 处理 |
|---|---|---|---|
| A模板记录数 | 876条 | 已满足 | 可交给评分者A |
| B模板记录数 | 876条 | 已满足 | 可交给评分者B |
| 裁决模板记录数 | 876条 | 已满足 | 仅在A/B回收后使用 |
| 人工校对风险 | 已列出154条 | 未销项 | 评分者遇到相关材料时标“待核实” |
| 正式手册版本 | 草案/内部版并存 | 未完成正式专家审查 | 本轮只冻结交接流程，不冻结正式手册结论 |
| 真实评分者记录 | 尚无 | 未满足 | 不得宣称已完成双评分者编码 |

## 回收后入口规则

评分者A/B模板全部回收后，必须先完成以下检查，再进入一致性脚本：

1. 两个模板均保持876条记录；
2. `present` 只包含“是/否”；
3. `level` 只包含 `L1`、`L2`、`L3`、`L4` 或“未出现”；
4. `evidence` 非空，且能回到题干、参考解答或题图；
5. `confidence` 只包含“高/中/低”；
6. `coder_id`、`coding_date`、`manual_version` 已填写；
7. `notes` 对所有材料疑问标出“待核实”；
8. 未出现复制内部预演或边界案例结论的迹象。

任一项不满足时，不进入一致性计算。

## 后续出口

本冻结包的下一步不是正式结果分析，而是：

1. 回收评分者A/B独立填写模板；
2. 运行字段完整性和取值检查；
3. 计算维度存在性与等级一致性；
4. 生成分歧清单；
5. 依据裁决协议填写 `formal_adjudication_template.csv`；
6. 生成唯一正式分析表；
7. 再由脚本生成正式结果表。

在第6步以前，论文正文只能写“方法准备”“正式编码流程拟定”和“内部预演边界”，不能写正式分布、正式趋势或正式显著性结论。
