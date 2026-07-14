# 评分者一致性计划

## 两类一致性

1. 维度是否出现：二分类一致性；
2. 认知结构等级：有序分类一致性。

## 推荐报告

- 原始一致率；
- Cohen's kappa或其他适当系数；
- 有序等级使用加权kappa；
- 类别极不平衡时增加更稳健的系数或敏感性说明；
- 每个维度分别报告，不只给一个总体数值。

## 流程

1. 随机抽取覆盖不同届次和模块的试编码样本；
2. 培训但不共同讨论具体答案；
3. 独立编码；
4. 计算一致性；
5. 分析系统性分歧；
6. 修订手册；
7. 进行第二轮试编码；
8. 冻结手册后再正式编码。

## 解释原则

一致性阈值应在分析前设定并结合类别分布解释。未达到目标时，不能只通过讨论把结果“做高”，应报告原因和框架局限。

## 可复现脚本

使用 `07_analysis/scripts/compute_reliability.py` 计算两名评分者一致性。脚本支持两类输入：

- 正式/试编码表字段：`item_id,coder,dimension,present,level,evidence`
- 评分者模板字段：`item_id,rater_id,dimension,present_yes_no,level_if_present,evidence`

真实评分者完成第一轮试编码后，可运行：

```bash
/Users/dongxingxi/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 07_analysis/scripts/compute_reliability.py \
  --input 04_framework/pilot_coding_round1_filled.csv \
  --output 07_analysis/results/generated/round1_reliability_by_dimension.csv \
  --disagreements 07_analysis/results/generated/round1_reliability_disagreements.csv
```

Codex模拟评分者数据只能用于压力测试，运行时必须显式加入 `--allow-simulated`，且不得作为正式一致性结果。
