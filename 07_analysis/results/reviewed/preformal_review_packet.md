# 正式编码前复核样本包

更新时间：2026-07-14

## 性质声明

本样本包由 `07_analysis/scripts/build_preformal_review_packet.py` 基于内部分析底稿和质量检查问题清单生成。它只用于正式编码前的复核、训练和问题定位，不是正式编码结果，不代表真实专家审查、导师确认或真实双评分者一致性。

## 输入文件

- `07_analysis/data/internal_coding_v1.csv`
- `07_analysis/results/reviewed/internal_coding_quality_issues.csv`
- `03_corpus/manual_review_checklist.csv`
- `04_framework/coding_manual_v2_internal.md`

## 输出文件

- `07_analysis/results/reviewed/preformal_review_sample_items.csv`
- `07_analysis/results/reviewed/preformal_review_coding_records.csv`
- `07_analysis/results/reviewed/preformal_review_manual_issues.csv`
- `07_analysis/results/reviewed/preformal_review_packet.md`

## 样本规模

- 复核样本分析单元：74
- 对应编码记录：296
- 关联人工校对条目：99

## 分届覆盖

| competition_no | sample_items |
| --- | --- |
| 35 | 8 |
| 36 | 8 |
| 37 | 8 |
| 38 | 8 |
| 39 | 8 |
| 40 | 8 |
| 41 | 8 |
| 42 | 18 |

## 风险覆盖

| risk_type | sample_items |
| --- | --- |
| 人工校对未销项 | 74 |
| 元数据待核风险 | 74 |
| 公式与特殊符号校对 | 74 |
| 编码把握度 | 74 |
| 题图裁边与图注校对 | 64 |
| 高等级边界 | 53 |
| 题干OCR校对 | 50 |
| 证据文本薄弱 | 23 |
| 第35届分值边界复核 | 8 |
| 质疑创新保守复核 | 7 |

## 全局问题

- 内部底稿的源试编码版本为：{'coding_manual_v1': 876}。 处理要求：正式编码前按内部V2或后续正式手册重新判读，不能把V1试编码直接视为正式V2结果。

## 复核流程

1. 先对 `preformal_review_manual_issues.csv` 中关联的原始PDF、公式、OCR和题图问题逐条销项；
2. 再用 `preformal_review_coding_records.csv` 对照 `coding_manual_v2_internal.md` 复核维度存在性和等级；
3. 对 L4 记录逐条确认是否存在迁移、修正、一般化、递推、优化或开放构造；
4. 对质疑创新记录逐条确认题干是否明确要求处理假设、替代模型、模型失效或开放方案；
5. 对证据文本薄弱记录补充可回到题干或参考解答的证据句；
6. 复核完成后不得直接覆盖内部底稿，应先形成修订日志，再决定是否进入正式编码表。

## 不得形成的结论

- 不得据此写正式维度比例、届次变化或知识模块差异；
- 不得把样本包写成专家审查或真实评分者结果；
- 不得把 Codex 试编码当成正式双人独立编码；
- 不得在人工校对未销项前使用受影响记录支撑论文结论。

## 下一步最小任务

执行 `G4-00S`：建立复核记录表，逐条记录样本包中的校对状态、复核结论、是否修订编码、修订理由和仍待核实事项。
