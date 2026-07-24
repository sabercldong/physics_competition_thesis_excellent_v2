# R01 G4 生命周期状态对账（2026-07-25）

## 目的

本对账处理 `TASKS.md` 中仍把 G4-01 至 G4-08 标记为未完成、而当前项目已存在 R01 回填、裁决、更正、唯一分析表、描述统计、案例和结果资格 QA 的状态差异。它只核验项目内文件和可复跑输出之间的对应关系；不把任何自声明升级为项目独立验证。

## 对账结论

| 原任务 | 当前项目内状态 | 核验依据 | 仍不证明的事项 |
|---|---|---|---|
| G4-01 双人独立编码 | R01 回填已接收、登记并用于当前分析 | `formal_coding_rater_AB_combined_registered_lf.csv`；`r01_rater_reliability_report.md` | 评分者身份、互盲、独立填写和实际人工过程 |
| G4-02 分歧裁决与日志 | 142 条分歧已形成 ADJ-01 裁决；ADJ-02 采纳4条更正 | `formal_adjudication_R01_prepared_20260723.csv`；`r01_correction_adjudication_change_manifest_v1.csv` | 裁决者身份、裁决过程及框架效度 |
| G4-03 数据清洗与唯一分析表 | 当前唯一版本化分析表为 R01 更正版本，876条唯一键可回溯 | `final_coding_r01_correction_v1.csv`；`r01_results_eligibility_qa_v1.csv` 的 RE-QA-01 至 RE-QA-06 | 对外部数据质量或人工过程的独立验证 |
| G4-04 总体分布 | 四维度出现与等级构成已由冻结表复算 | `correction_v1/final_dimension_presence.csv`；`final_level_distribution.csv`；结果资格 QA | 学生能力、题目总难度或因果关系 |
| G4-05 维度共现 | 共现和 Jaccard 输出已复算 | `correction_v1/final_dimension_cooccurrence.csv`；结果资格 QA RE-QA-C1 | 维度发展关系、因果关系或学生共现表现 |
| G4-06 分届次、模块、情境和数学工具比较 | 分届次、知识模块等样本内部描述表已生成；只作呈现 | `correction_v1/final_year_dimension_presence.csv`；`final_knowledge_dimension_presence.csv`；第四章4.5 | 显著性、长期趋势、组间普遍规律或第35届分值结论 |
| G4-07 典型试题案例 | 三个R01案例已重选并通过案例 QA | `08_manuscript/r01_formal_case_selection.md`；`r01_case_reselection_qa_v1.csv` | 学生困难、教师认可或教学效果 |
| G4-08 稳健性与边界说明 | 结果资格、章节整合、结论对齐与材料包健康检查均已覆盖 | `r01_results_eligibility_qa_v1.csv`；`r01_results_manuscript_integration_qa_v2.csv`；`r01_conclusion_rq_alignment_qa_v1.csv`；`r01_full_package_healthcheck_v1.csv` | 理论外部效度、学校提交资格或论文终稿质量 |

## 当前唯一分析表口径

- 当前用于第四章、结论、摘要和描述统计的是 `07_analysis/data/final_coding_r01_correction_v1.csv`，而非早期 `final_coding.csv` 或内部预演表。
- 该表共有219个分析单元、876条四维记录；其 SHA-256 为 `3da0ec26a25b7b78bd62088dabccbc948dc62c7435fb8672d6daaf97e59af852`。
- 当前证据链为840条 R01 V6、32条 R01 补证 V2 与4条 ADJ-02 更正。其存在只证明项目内可追溯与可复算，不证明声明背后的人工过程。
- 第35届八道题仍无正式逐题/小问分值来源；所有G4输出均禁止分值加权、分值比较、相关、趋势或显著性结论。

## G3 与终稿边界

本对账**不**将 G3-08“冻结正式编码手册V2”标为完成。当前可证明的是 R01 编码使用了登记的 `G4-01-R01-2026-07-22` 版本和后续裁决/更正记录；未取得可独立验证的专家审查、导师确认或框架外部效度材料。

本对账也不关闭SOLO原典全文、国内竞赛研究全文、学校当期格式与AI披露、真实教师/课堂材料及最终参考文献等终稿阻塞项。

## 复跑入口

```bash
python3 07_analysis/scripts/validate_r01_results_eligibility.py
python3 07_analysis/scripts/validate_r01_results_manuscript_integration_v2.py
python3 07_analysis/scripts/validate_r01_conclusion_rq_alignment.py
python3 07_analysis/scripts/validate_r01_full_package_healthcheck.py
```
