# R01 双评分者回填接收检查

接收日期：2026-07-23
任务：`G4-02-R01-RATER-RETURN-INTAKE`

## 接收范围

- `RATER-A`：876 条，原件 SHA-256 为 `26fae1007658a7de04c9034076ad45e9fea45c67bda5e49722c762cf281daaca`；
- `RATER-B`：876 条，原件 SHA-256 为 `da36966b7d5a62f38de806da19719c8e34862f2a452ea44831ee553e8c7cd3e1`；
- 原件保存在 `07_analysis/data/rater_returns/incoming/R01/`，以 Git `-text` 规则保留字节；登记副本和合并计算输入位于 `07_analysis/data/rater_returns/registered/R01/`。

## 结构检查结果

两份文件均为 876 行、14 个字段，分别与对应空白模板的不可变字段及行序完全一致。A/B 之间的 876 个不可变键集合和行序也完全一致。

`present`、`level`、`evidence`、`confidence`、`coder_id`、`coding_date`、`manual_version` 均无空值；枚举取值和“`present=否` 时 `level=未出现`”的逻辑均无异常。两份文件的 `notes` 均为空：此项允许为空，但不提供不确定性补充说明。

字段级检查见 `r01_rater_return_intake_check_v1.csv`，回收登记见 `04_framework/rater_r01_return_register.csv`。

## 自声明与不可验证边界

项目收到 RATER-A 与 RATER-B 分别作出的独立编码自声明，均声明未查看对方编码、未以智能体或内部预演作为本人判断。该声明已登记；本项目只能核验文件结构与内容，不具备独立验证提交前互盲或实际编码过程的条件。

本轮仅核验 `evidence` 字段非空，尚未逐条判定证据摘记的实质充分性；该检查应在分歧裁决与最终数据 QA 中完成。

## 放行结论

两份回填可进入一致性计算，已生成分歧清单；不得直接视为 `final_coding.csv`、正式统计或论文结果。下一步必须以 `r01_reliability_disagreements.csv` 的 142 条记录为入口，完成有证据的分歧裁决，再生成唯一分析表。
