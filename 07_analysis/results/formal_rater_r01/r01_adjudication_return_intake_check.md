# R01 裁决回填接收检查

接收日期：2026-07-23
任务：`G4-05-R01-ADJUDICATION-RETURN-INTAKE`

## 接收文件

- 主裁决表：876 条，SHA-256 `f88d66593a8a62bf5847d9f6755854f59b56e43d43bad6c606a615ca00df48c2`；
- 分歧工作清单：142 条，SHA-256 `c5036a72bb792c6233444e07dd5227f39dbc92204e2f01789ed774a2b74ca013`。

原件保存在 `07_analysis/data/rater_returns/incoming/R01/`，并以只读及 Git `-text` 规则保存；登记副本只统一为 UTF-8 BOM 与 LF。

## 字段与交叉检查

主表与冻结模板的 24 列、876 个不可变键及行序完全一致；工作清单与预填清单的 26 列、142 个键及行序完全一致。两表的裁决字段均无空值，取值、存在性—等级逻辑、代号与日期均通过。142 条工作清单与主表裁决字段逐条一致，A/B 原始判断与已登记回填逐条一致。

`build_final_coding.py` 的 8 项硬门禁均通过，已生成 `07_analysis/data/final_coding.csv`。详细检查见 `r01_adjudication_return_intake_check_v1.csv` 与 `final_coding_build_qa.csv`。

## 边界

已收到 ADJ-01 的独立裁决自声明；项目可以登记该声明，但不能独立验证实际裁决过程。字段 QA 检查裁决证据非空和可按 `item_id` 追溯语料，不替代对每条证据的外部学术质量认证。

用户消息中的最终分布摘要与从回填主表重新计算的分布不一致；本项目只采用已归档主表和脚本输出中的可复算结果。
