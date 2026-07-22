# G1-07-NO-RETURN-REAL-RETURN-TRIGGER-MAP 真实回填触发路线图

更新时间：2026-07-22

## 性质声明

本路线图把既有接收协议、评分者交接规则、正式分析门槛和结果出口串为单向触发链。当前所有节点仍停在 `TRM-01`：项目未收到真实回填，`03_corpus/manual_review_returns/` 和 `07_analysis/data/final_coding.csv` 均不存在。路线图不构成真实回填、真实编码、一致性、裁决或论文结果。

## 使用规则

1. 事件必须以可保存、可校验的真实副本或真实填写记录为触发证据。
2. 每一节点只允许产生本节点列出的产物；只能在前一节点验证通过后进入下一节点。
3. A/B/C/D人工校对回填与A/B评分者编码是不同流程：前者解决语料可用性，后者产生正式编码；两者不能互相替代。
4. `final_coding.csv` 是裁决后唯一正式分析表，而非接收登记、内部预演或空白模板的别名。

## 当前状态

- 当前节点：`TRM-01`。
- 当前允许：维护接收规则、未来触发条件、空白模板、语料路径和冻结边界。
- 当前禁止：关闭154项、创建虚构回填、正式A/B评分、一致性计算、裁决、统计、结果章或教学效果结论。

## 路线表

见 `03_corpus/no_return_real_return_trigger_map_v1.csv`。

## 上游依据

- `03_corpus/return_intake_folder_protocol.md`
- `03_corpus/manual_review_real_return_handoff_register.md`
- `04_framework/rater_handoff_lock_v1.md`
- `04_framework/rater_handoff_file_rules.csv`
- `07_analysis/results/reviewed/prep30_gate_register.csv`
- `07_analysis/results/reviewed/prep30_formal_output_placeholders.csv`

## 下一最小任务

`G1-07-NO-RETURN-REAL-RETURN-TRIGGER-MAP-QA`：核对11个触发节点的顺序、证据、产物、禁止事项和上游路径；不得因路线图存在而创建真实回填或放行正式结果。
