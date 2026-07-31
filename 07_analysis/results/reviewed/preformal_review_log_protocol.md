# 正式编码前复核记录表使用说明

更新时间：2026-07-14

## 性质声明

`preformal_review_log.csv` 是复核记录空表，服务于正式编码前的内部质量控制。当前所有记录均为“待复核”，不得视为已经完成校对、编码修订或分歧裁决。

## 使用顺序

1. 先处理同一样本在 `preformal_review_manual_issues.csv` 中关联的题干、公式、OCR、题图或分值边界问题；
2. 在 `text_formula_figure_checked` 中记录是否已经对照原始PDF完成校对；
3. 对照 `coding_manual_v2_internal.md` 复核维度存在性与等级，在 `v2_boundary_checked` 中记录是否完成；
4. 若保留内部试编码，填写 `revision_decision=保留` 并说明理由；
5. 若修订，填写 `proposed_present`、`proposed_level`、`proposed_evidence` 和 `revision_reason`；
6. 证据不足时填写 `unresolved_issue`，不要自行补齐；
7. 只有在全部样本完成复核并形成修订日志后，才可考虑生成下一版内部编码表。

## 允许的修订决定

- `保留`
- `修订存在性`
- `修订等级`
- `修订证据`
- `待核实`

## 禁止事项

- 不得把本表空白记录当作复核完成；
- 不得把 Codex 内部复核写成真实专家或真实评分者意见；
- 不得在题干、公式或图像问题未销项前形成正式编码结论；
- 不得直接覆盖 `internal_coding_v1.csv`。
