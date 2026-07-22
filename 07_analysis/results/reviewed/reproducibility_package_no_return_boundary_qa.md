# G1-07-NO-RETURN-REPRODUCIBILITY-PACKAGE-BOUNDARY-QA 复现包无真实数据边界QA

更新时间：2026-07-22

## 性质声明

本QA检查复现准备材料、内部候选数据、数据字典、门禁表、输出占位和脚本边界。它不运行内部候选数据生成统计，不生成正式结果，不创建`final_coding.csv`，也不改写论文正文。

## QA结论

- 检查项：35项；通过：28项；不通过：7项。
- 内部候选数据与内部编码数据各876行，均保留“内部/非正式”状态标记；正式A/B/裁决模板各876行，A/B编码字段为空。
- 正式输出占位4项均未放行，5项正式分析门槛均未满足；`final_coding.csv`、真实人工回填目录均不存在。
- `prep30`脚本读取内部候选数据并带有“正式编码前准备；非正式编码结果；不得写入论文结果”边界常量。
- 当前不通过项：RPNR-QA-029, RPNR-QA-030, RPNR-QA-031, RPNR-QA-032, RPNR-QA-033, RPNR-QA-034, RPNR-QA-035。它们均为既有CSV的CRLF换行格式，不是正式数据或结果缺失之外的新研究结论。

## 可用与不可用

| 材料 | 当前可用用途 | 不可作出的主张 |
|---|---|---|
| prep30脚本、数据字典、门禁和占位表 | 正式编码前复现结构准备 | 正式数据分析或论文结果已完成 |
| internal_analysis_candidate_v0.csv | 内部方法演练和字段结构核对 | 正式样本编码、分布、趋势或显著性 |
| A/B与裁决模板 | 真实评分者回收入口 | 已完成独立编码、一致性或裁决 |

## 下一最小任务

`G1-07-NO-RETURN-REPRODUCIBILITY-CSV-FORMAT-FIX`：仅将本QA列出的7份既有复现CSV机械统一为UTF-8 BOM与LF，然后重跑本QA；不得变动任何单元格值、内部状态、脚本或论文内容。

## 输出文件

- QA说明：`07_analysis/results/reviewed/reproducibility_package_no_return_boundary_qa.md`
- QA检查表：`07_analysis/results/reviewed/reproducibility_package_no_return_boundary_qa_v1.csv`
