# 文献理论核验入口QA

任务编号：`G2-01-LITERATURE-THEORY-VERIFICATION-ENTRY-QA`  
生成日期：2026-07-19

## 性质声明

本文件只检查 `02_literature/literature_theory_verification_entry.md` 和 `02_literature/literature_theory_verification_entry_v1.csv` 是否能够作为下一批文献理论核验入口。它不获取新全文，不改写论文正文，不修改 `09_quality/claim_evidence_matrix.csv`，不新增或修改 `02_literature/references.bib`，不补造页码、图表编号、阅读结论、专家意见、教师意见、问卷结果、课堂材料或学生作品。

## QA结论

通过。入口表共12项，编号连续，P0/P1覆盖完整，执行顺序清楚，证据入口路径均可定位，禁写边界覆盖题录/摘要误用、SOLO误用、方法一致性误用、测评与教学误用、竞赛研究空白误用和正式结果误用。

机器可查QA表见 `02_literature/literature_theory_verification_entry_qa_v1.csv`，共34项检查，结果均为“通过”。

## 已确认事项

- 入口CSV为UTF-8 BOM和LF换行；
- `G2VE-01` 至 `G2VE-12` 连续唯一；
- P0六项、P1六项；
- 执行顺序为优先执行4项、第二批执行5项、第三批执行2项、暂缓执行1项；
- P0来源覆盖 `CS-001`、`ST-002`、`ST-003`、`ST-005`、`ST-006` 和 `METH-004`；
- P1来源覆盖SOLO、物理竞赛研究、内容分析/一致性方法、科学推理测评、工作版参考文献表和主张矩阵侧车；
- 所有 `evidence_entry_files` 均可在当前项目中定位；
- 入口报告明确不获取新全文、不改写正文、不修改主张矩阵、不新增正式参考文献。

## 仍不能声称

- 不能声称SOLO原书或1989年论文已经完成全文阅读；
- 不能声称物理竞赛研究空白已经由全文证据证明；
- 不能声称方法文献已经给出本项目一致性通过标准；
- 不能声称科学思维测评文献证明本项目学生能力；
- 不能声称教学转化文献证明本项目课堂效果；
- 不能声称 `references.bib` 已经是最终参考文献表；
- 不能声称主张证据矩阵可以合并或升级；
- 不能声称第四章正式结果、趋势、共现、显著性或效应量已经可写。

## 下一最小任务

`G2VE-01-CS-STANDARD-FINALCHECK`：优先对课程标准概念依据做定稿前复核，确认官方版本、章节或页码表达、学校格式候选写法和可支持语句清单。该任务仍不改写正文、不定稿参考文献表、不升级主张矩阵。

若希望优先补强方法章，也可选择 `G2VE-02-METH004-FINALCHECK`；但默认先处理 `G2VE-01`，因为它支撑科学思维四维度的基础概念边界。

## 输出边界

本QA只新增文献理论入口QA报告和QA表，并更新项目台账；不修改 `00_originals/`，不修改 `08_manuscript/`，不修改 `09_quality/claim_evidence_matrix.csv`，不修改 `02_literature/references.bib`，不修改 `07_analysis/scripts/`，不创建真实回填目录，不创建或伪造正式结果文件。
