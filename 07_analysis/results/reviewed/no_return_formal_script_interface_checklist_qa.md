# 无真实回填条件下的正式脚本接口检查清单QA

## 性质声明

本文件是 `G1-07-NO-RETURN-FORMAL-SCRIPT-INTERFACE-CHECKLIST-QA` 的检查报告，只验证正式脚本接口检查清单是否完整、可追溯且未误放行正式统计。本QA不修改脚本，不运行统计，不创建 `07_analysis/data/final_coding.csv`，不生成正式表图，不改写论文正文或主张证据矩阵。

## 检查结论

QA通过。`07_analysis/results/reviewed/no_return_formal_script_interface_checklist.md` 与 `07_analysis/results/reviewed/no_return_formal_script_interface_checklist_v1.csv` 可以作为后续正式脚本接口修订和脚本QA的需求入口，但不能替代真实人工终核、真实A/B评分者编码、分歧裁决或正式统计输出。

## 已确认事项

- QA表共82项检查，全部通过；
- 接口清单CSV为UTF-8 BOM和LF换行；
- 接口清单包含22项，`FSI-01` 至 `FSI-22` 连续唯一；
- 字段覆盖检查编号、接口区域、检查事项、来源或目标路径、接口要求、当前状态、放行状态和禁止事项；
- 接口区域覆盖前置门禁、输入文件、必需字段、输入字段补充、脚本接口、一致性输入、一致性输出、输出表、运行日志、QA门槛、正文门禁和版本归档；
- 清单已标出 `present` 字段口径风险、`generated/` 与 `reviewed/final_*.csv` 输出路径风险、共现和分组比较脚本接口缺口；
- `final_coding.csv` 和正式结果输出表仍未生成；
- 本任务没有修改 `build_descriptive_tables.py`、`compute_reliability.py`、第四章正文或主张证据矩阵。

## 仍不能声称

- 不能声称正式统计脚本已经修订完成；
- 不能声称 `present` 字段口径已经统一；
- 不能声称正式共现表或分组比较表已有脚本输出；
- 不能声称正式结果路径已经定稿；
- 不能声称第四章正式结果可以写入论文。

## 保留风险

接口清单已经把主要风险暴露出来，但真正解决风险需要后续单独任务修改或补充脚本，并在真实 `final_coding.csv` 到位后运行正式脚本QA。当前最重要的阻塞仍是154项人工校对真实销项、真实A/B评分者编码和分歧裁决。

## 下一最小任务

`G1-07-NO-RETURN-FORMAL-SCRIPT-INTERFACE-CLOSEOUT`：收束无真实回填条件下的复现包与正式脚本接口准备链，明确哪些内容已经可作为未来复现需求，哪些必须等待真实材料。

## 输出边界

本任务只新增正式脚本接口检查清单QA报告和CSV，并更新项目台账；不修改 `00_originals/`，不修改 `08_manuscript/`，不修改 `09_quality/claim_evidence_matrix.csv`，不修改 `02_literature/references.bib`，不创建或伪造正式结果文件。
