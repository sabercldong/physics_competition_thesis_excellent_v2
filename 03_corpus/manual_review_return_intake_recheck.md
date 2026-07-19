# 真实人工终核回填接收入口复查

## 性质声明

本文件是 `G1-07-MANUAL-RETURN-INTAKE-RECHECK` 的复查报告，用于重新检查当前项目中是否出现可接收的真实人工终核回填文件。本任务只复查接收入口、登记字段和阻断状态；不填写真实校对人、真实校对日期、校对决定、分值、图号边界、专家意见、评分者记录、问卷结果、课堂结果或论文正文结论，也不关闭154项人工校对问题。

## 复查结论

当前仍未发现可接收的真实人工终核回填文件。`03_corpus/returns`、`03_corpus/manual_review_returns`、`03_corpus/returned` 和 `03_corpus/manual_review_return_copies` 四个候选回填目录均不存在；首批A组接收登记和剩余B/C/D接收登记中的真实文件名、保存路径、校验值、接收日期和接收人均未填写；A/B/C/D四组回填包中的真实校对人、校对日期和校对决定仍为0项填写。

因此，正式编码、正式统计、第四章正式结果、案例图件定稿、第35届分值统计、第42届第3题附属图边界、主张证据矩阵升级和论文结果章写作继续冻结。

## 复查范围

- `03_corpus/manual_review_real_return_handoff_register_v1.csv`
- `03_corpus/manual_review_remaining_return_handoff_register_v1.csv`
- `03_corpus/manual_review_a_closure_packet_v1.csv`
- `03_corpus/manual_review_b_closure_packet_v1.csv`
- `03_corpus/manual_review_c_closure_packet_v1.csv`
- `03_corpus/manual_review_d_closure_packet_v1.csv`
- `03_corpus/manual_review_closure_action_plan_v1.csv`
- `03_corpus/manual_review_return_integration_dry_run_template_v1.csv`
- 候选回填目录：`03_corpus/returns`、`03_corpus/manual_review_returns`、`03_corpus/returned`、`03_corpus/manual_review_return_copies`

## 关键证据

| 对象 | 当前状态 | 结论 |
|---|---|---|
| 候选回填目录 | 四个候选目录均不存在 | 未收到可登记的真实回填副本 |
| 首批A组接收登记 | 38行；接收文件名、保存路径、校验值、接收日期和接收人均0项填写 | REAL-P1未接收 |
| 剩余B/C/D接收登记 | 78行；接收文件名、保存路径、校验值、接收日期和接收人均0项填写 | REMAINING-B/C/D未接收 |
| A组回填包 | 76项；真实校对人、日期、决定均0项填写 | A组不能销项 |
| B组回填包 | 22项；真实校对人、日期、决定均0项填写 | B组不能销项 |
| C组回填包 | 47项；真实校对人、日期、决定和图件可用性均0项填写 | C组候选图不能定稿 |
| D组回填包 | 9项；真实校对人、日期、决定均0项填写 | 分值与附属图边界不能确认 |
| 动作计划 | 154项；真实回填字段和正式编码放行字段均0项有效填写 | 不能解锁正式编码 |
| 整合演练模板 | 154项；回填文件路径、文件名和冲突字段为空 | 不能同步账本或主张矩阵 |

## 当前阻断

1. 154项人工校对问题仍未真实销项；
2. 不能生成正式A/B评分者编码任务的放行输入；
3. 不能计算真实评分者一致性；
4. 不能进行分歧裁决或生成 `07_analysis/data/final_coding.csv`；
5. 不能生成正式统计表、图或运行日志；
6. 不能把候选图写成论文定稿图；
7. 不能写第35至42届试题正式百分比、趋势、共现、显著性、p值、效应量或教学效果结论；
8. 不能升级 `09_quality/claim_evidence_matrix.csv` 中相关主张证据等级。

## 收到真实回填后的最小动作

1. 原样保存真实回填副本，不覆盖空白回填包；
2. 登记来源文件名、保存路径、SHA-256、文件大小、接收日期和接收人；
3. 按组别进入 `incoming/REAL-P1/` 或 `incoming/REMAINING-B/C/D/`；
4. 执行结构检查、固定字段检查、必填回填字段检查和冲突分级；
5. 另开整合QA任务，通过后再同步人工校对清单、优先队列、动作计划和总索引；
6. 正文和主张矩阵必须另设任务处理，不能混入接收提交。

## 下一最小任务

`G1-07-MANUAL-RETURN-INTAKE-RECHECK-QA`：检查本复查报告和复查CSV是否与当前项目文件一致，确认真实回填仍未收到、正式结果仍冻结，且未创建回填目录或正式结果文件。

## 输出边界

本任务只新增真实回填入口复查报告和CSV，并更新项目台账；不修改 `00_originals/`，不修改 `08_manuscript/`，不修改 `09_quality/claim_evidence_matrix.csv`，不修改 `02_literature/references.bib`，不修改 `07_analysis/scripts/`，不创建真实回填目录，不创建或伪造正式结果文件。
