# 文献理论核验入口

任务编号：`G2-01-LITERATURE-THEORY-VERIFICATION-ENTRY`  
生成日期：2026-07-19

## 性质声明

本文件是文献理论核验的入口文件，只把现有参考文献核验表、P0定稿前复核单、P1全文缺口队列、文献矩阵和主张队列重新整理成下一批可执行核验顺序。它不获取新全文，不改写论文正文，不修改 `09_quality/claim_evidence_matrix.csv`，不新增或修改正式参考文献，不补造页码、图表编号、阅读结论、专家意见、教师意见、问卷结果、课堂材料或学生作品。

结构化入口表见 `02_literature/literature_theory_verification_entry_v1.csv`。

## 输入依据

- `09_quality/safe_prep_next_route_decision.md`；
- `09_quality/no_return_reference_claim_queue.md`；
- `09_quality/no_return_reference_claim_queue_v1.csv`；
- `09_quality/no_return_reference_p0_finalcheck_sheet.md`；
- `09_quality/no_return_reference_p0_finalcheck_sheet_v1.csv`；
- `09_quality/no_return_reference_p1_gap_queue.md`；
- `09_quality/no_return_reference_p1_gap_queue_v1.csv`；
- `02_literature/reference_verification.csv`；
- `02_literature/literature_matrix.csv`；
- `MASTER_PLAN.md`、`PROJECT_STATUS.md` 和 `TASKS.md`。

## 总体判断

当前文献理论路线可以继续推进，但只能推进为“核验入口、阅读任务、页码定位、引用边界和主张支持关系”。它不能替代真实人工校对、正式A/B评分者编码、`final_coding.csv`、正式统计、教师访谈、问卷或课堂证据。

下一批核验入口共12项：

- P0定稿前复核：6项；
- P1全文或主张补证入口：6项；
- 优先执行：4项；
- 第二批执行：5项；
- 第三批执行：2项；
- 暂缓执行：1项。

## 优先执行项

优先执行4项，原因是它们最直接支撑第二章理论框架和第三章方法边界：

1. `G2VE-01` 课程标准概念依据定稿前复核：确认科学思维四维度和课程标准依据；
2. `G2VE-02` 内容分析一致性方法已读来源复核：确认一致性报告和方法边界的可支持语句；
3. `G2VE-03` SOLO理论全文与迁移边界入口：补强“SOLO启发的任务认知结构要求”的理论边界；
4. `G2VE-04` 内容分析与编码一致性方法全文补强入口：补强编码手册、内容分析流程和一致性解释的文献支撑。

这些入口完成后，仍只能支持边界性方法和理论表述，不能声称本项目编码框架已经有效、真实一致性已经通过或正式结果已经成立。

## 第二批执行项

第二批执行5项，主要支撑科学思维测评边界和第五章教学转化参照：

- `G2VE-05` `ST-002`；
- `G2VE-06` `ST-003`；
- `G2VE-07` `ST-001;ST-004`；
- `G2VE-08` `ST-005`；
- `G2VE-09` `ST-006`。

这些材料可以帮助区分“试题任务要求”“学生真实表现”“科学推理测评”和“教学任务评价”，但不能证明本项目存在真实教师意见、问卷结果、课堂效果或学生作品分析。

## 第三批和暂缓项

第三批执行：

- `G2VE-10` 物理竞赛研究全文与研究空白入口；
- `G2VE-11` 工作版参考文献表闭环入口。

暂缓执行：

- `G2VE-12` 主张矩阵侧车合并准备入口。当前 `09_quality/claim_evidence_matrix.csv` 存在历史未提交差异，仍保持侧车引用，不直接合并或升级。

## 禁写边界

本入口之后，仍不得：

- 用题录、摘要、目录、预览或搜索结果替代全文阅读；
- 编造页码、图表编号、版本关系或文献结论；
- 把SOLO理论直接写成学生学习结果测量；
- 把方法文献写成真实一致性已经通过；
- 把科学思维测评文献写成本项目学生能力证据；
- 把教学转化文献写成本项目课堂效果；
- 把物理竞赛文献题名写成研究空白已经证明；
- 直接修改 `02_literature/references.bib` 生成最终参考文献表；
- 直接修改 `09_quality/claim_evidence_matrix.csv` 升级证据等级；
- 改写第四章正式结果、趋势、共现、显著性、p值、效应量或置信区间。

## 下一最小任务

`G2-01-LITERATURE-THEORY-VERIFICATION-ENTRY-QA`：检查本入口表是否覆盖P0/P1来源、编号连续、优先级合理、证据路径可定位、禁写边界完整，并确认未改写正文、未修改主张矩阵、未新增正式参考文献。

## 输出边界

本任务只新增文献理论核验入口说明和入口表，并更新项目台账；不修改 `00_originals/`，不修改 `08_manuscript/`，不修改 `09_quality/claim_evidence_matrix.csv`，不修改 `02_literature/references.bib`，不修改 `07_analysis/scripts/`，不创建真实回填目录，不创建或伪造正式结果文件。
