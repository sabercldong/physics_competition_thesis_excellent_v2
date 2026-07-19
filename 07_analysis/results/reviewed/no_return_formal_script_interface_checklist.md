# 无真实回填条件下的正式脚本接口检查清单

## 性质声明

本文件是 `G1-07-NO-RETURN-FORMAL-SCRIPT-INTERFACE-CHECKLIST` 的接口准备报告，用于说明未来正式统计脚本接入 `07_analysis/data/final_coding.csv` 前必须检查的字段、输入路径、输出路径、运行日志和QA门槛。本任务不运行正式统计，不修改任何脚本，不生成 `final_coding.csv`，不生成正式表图，不改写论文正文。

## 当前判断

项目已有正式描述统计脚本 `07_analysis/scripts/build_descriptive_tables.py` 和一致性计算脚本 `07_analysis/scripts/compute_reliability.py`，但正式输入尚不存在。当前能做的是把未来接口要求固定下来，避免真实A/B评分者编码和分歧裁决回来后出现字段口径、输出路径或分母解释混乱。

## 检查清单概况

接口清单共22项，覆盖：

- 前置门禁3项：人工校对、P0/P1复核、正式唯一分析表；
- 字段接口6项：`item_id`、`dimension`、`present`、`level`、`evidence` 和分组元数据；
- 脚本接口5项：描述统计输入、输出目录、共现/分组比较、一致性输入和一致性输出；
- 正式输出4项：维度总体分布、等级分布、共现和分组比较；
- 运行与QA4项：运行日志、正式输出QA、正文门禁和版本归档。

## 已识别的接口风险

1. `present` 字段口径需要统一：准备版数据字典写作“是/否”，但 `build_descriptive_tables.py` 当前按 `present==1` 筛选。
2. 输出路径需要统一：`build_descriptive_tables.py` 当前输出到 `07_analysis/results/generated/`，而占位表登记的正式结果路径在 `07_analysis/results/reviewed/final_*.csv`。
3. 当前描述统计脚本只生成维度总体分布和等级分布，不生成正式共现表或分组比较表。
4. 分组比较需要届次、知识模块、情境、表征和数学工具等元数据；这些元数据必须由 `item_id` 可追溯联结，不能临时手工拼接。
5. 一致性计算脚本可支持真实A/B编码，但在没有真实输入前不能产生正式一致性结论。

## 当前可做

- 保留本清单作为后续脚本修改或脚本QA的需求来源；
- 等 `final_coding.csv` 生成后，用本清单逐项检查字段、取值、输出路径和日志；
- 若后续修改脚本，应单独开任务并先写脚本接口QA；
- 在方法章中只可说明“预设复现接口和门禁”，不得写统计结果。

## 当前不可做

- 不得运行内部数据并命名为正式输出；
- 不得把 `internal_coding_v1.csv` 改名或复制为 `final_coding.csv`；
- 不得直接把 `generated/` 下的内部或临时输出用于论文正文；
- 不得在 `present` 口径未统一时计算正式比例；
- 不得写第四章正式百分比、趋势、显著性、p值或效应量。

## 下一最小任务

`G1-07-NO-RETURN-FORMAL-SCRIPT-INTERFACE-CHECKLIST-QA`：检查接口清单是否覆盖前置门禁、字段、脚本输入输出、运行日志、QA和正文门禁，确认没有运行正式统计或生成正式结果文件。

## 输出边界

本任务只新增正式脚本接口检查清单报告和CSV，并更新项目台账；不修改 `00_originals/`，不修改 `08_manuscript/`，不修改 `09_quality/claim_evidence_matrix.csv`，不修改 `02_literature/references.bib`，不创建或伪造正式结果文件。
