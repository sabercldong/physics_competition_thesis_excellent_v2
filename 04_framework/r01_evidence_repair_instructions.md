# R01 需补充引文回填指令

## 任务目的

本包只处理两份已接收实质审查中被标记为“需补充引文”的32条编码记录：58条实质审查24条、16条高风险审查8条。目标是为每条记录补入能在项目内题目整理文本逐字定位的题干和解答原文，并重新判断这些原文是否足以支持当前编码。

本任务不等同于修改编码、恢复第四章正式结果资格或确认人工过程。不能编造引文、页码、公式、理由或裁决。

## 工作文件

- 模板：`07_analysis/data/rater_returns/templates/R01/r01_evidence_repair_template_v1.csv`
- 每行原文入口：`item_text_path`
- 已有问题说明：`evidence_gap_reason` 与 `existing_support_explanation`
- 当前受控值：`current_present` 与 `current_level`

复制模板后填写，保留32行顺序和所有预填字段。建议回填文件名：

`/Users/dongxingxi/Desktop/论文人工复核回填/R01/r01_evidence_repair_R01_FILLED_20260723.csv`

## 每行填写步骤

1. 打开该行的`item_text_path`，只使用其中可检索到的题干和参考解答文本。
2. 在`repaired_question_quote`填能体现该小问任务要求的连续题干原文；在`repaired_question_location`填题面页与小问号。
3. 在`repaired_solution_quote`填能体现关键解答步骤、公式关系或推导动作的连续原文；在`repaired_solution_location`填答案页与可辨识的小问、式号或步骤。
4. 两侧引文都必须至少含8个非空字符，可在对应`item_text_path`中逐字搜索，并且两侧引文不得相同。
5. 填`evidence_recheck_decision`：
   - `充分支持`：新引文足以支持当前值；`rechecked_present/rechecked_level`必须与当前值完全一致。
   - `仍需补充`：已定位原文，但仍不足以支持当前判断；如实填当前复核值和`correction_reason`，该行不会关闭。
   - `不支持当前编码`：原文不支持当前值；填新的存在性和等级，并在`correction_reason`说明原因。此决定只形成待裁决建议，不会自动改动分析表。
6. 填真实`repairer_id`、`repair_date`、`repairer_statement`。声明只能说明本人实际完成的工作，不能把智能体判断冒充为人工结论。

## 禁止写法

- “见题面”“见答案”“标准推导”“未找到”“同上”等概述或占位语；
- 不能在`item_text_path`中定位的改写、截断公式或凭记忆补写内容；
- 将题干引文复制到解答引文栏；
- 因希望通过门禁而把“仍需补充”写成“充分支持”。

## 接收规则

接收程序将检查32条记录数、键与模板行序、工作字段、决定枚举、存在性—等级逻辑、引文最小长度、题目整理文本定位、题干/解答不重复，以及“充分支持”与当前值的一致性。结构通过不等于项目能够独立验证复核者身份或过程；只有全部实质缺口经真实补证并经后续状态复核，第四章才可能申请升级。
