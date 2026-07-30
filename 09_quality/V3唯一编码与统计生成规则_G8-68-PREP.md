# V3唯一编码与统计生成规则

任务编号：`G8-68-PREP`

版本日期：2026-07-30

## 一、生成前门禁

V3唯一编码表只能由以下两份文件共同生成：

1. 通过全量 `filled` 校验的884行作者实质复核文件；
2. G8-80人工QA完成后填写的一行验收决定。

验收决定必须满足：

- `accepted_review_sha256`与884行复核文件完全一致；
- `qa_decision=接受进入唯一编码表`；
- 不可变字段确认、高风险标记处置、未闭合记录处置和证据抽查四项均为“是”；
- QA报告路径可定位；
- 验收代号、日期和声明完整。

作者复核中只要仍有一条“待核实”“待补证”或“待裁决”，唯一表生成器就必须拒绝。

## 二、验收决定填写

复制：

`10_outputs/material_package/V3作者实质复核分批包_G8-80-PREP/V3作者实质复核G8-80验收决定模板.csv`

填写一行，不得修改表头。`qa_decision`只在全部门禁满足时填写`接受进入唯一编码表`；否则应继续使用接收报告和质量标记处理问题，不运行G8-68。

## 三、生成唯一编码表

```bash
python3 07_analysis/scripts/build_v3_final_coding.py \
  --review "<884行作者复核完成副本>" \
  --acceptance "<G8-80验收决定文件>" \
  --output "07_analysis/data/第35至42届科学思维V3唯一编码表.csv" \
  --qa-output "09_quality/第35至42届科学思维V3唯一编码表生成QA.csv"
```

唯一表包含884行、221个分析单元和四个维度，并同时保存：

- 原题、解答路径与哈希；
- 题干和解答引文；
- 候选存在性、候选等级；
- 作者复核后的存在性、等级、理由和证据位置；
- G8-80验收代号与日期；
- 作者复核文件和验收决定文件SHA-256。

该文件使用新的中文名称，不覆盖V2的876行 `final_coding.csv` 或 `final_coding_r01_correction_v1.csv`。

## 四、生成中文统计表

```bash
python3 07_analysis/scripts/build_v3_descriptive_outputs.py \
  --input "07_analysis/data/第35至42届科学思维V3唯一编码表.csv" \
  --item-index "03_corpus/item_index.csv" \
  --output-dir "07_analysis/results/v3_final"
```

输出包括：

- `总体维度出现分布.csv`
- `各维度等级分布.csv`
- `维度共现分布.csv`
- `分届次维度出现分布.csv`
- `分届次维度等级分布.csv`
- `维度组合分布.csv`
- `结果数据来源登记.csv`
- `描述统计生成说明.md`

所有结果表绑定唯一编码表SHA-256。比例保留六位小数，分母同时保存在表中，不使用分值加权。

## 五、生成正式图件

```bash
python3 07_analysis/scripts/build_v3_formal_figures.py \
  --input "07_analysis/data/第35至42届科学思维V3唯一编码表.csv" \
  --output-dir "08_manuscript/figures/v3_final"
```

输出四幅中文PNG/PDF图件和一份图件来源登记：

- `图4-1_四维度出现比例_V3`
- `图4-2_四维度等级构成_V3`
- `图4-3_各届次维度出现比例_V3`
- `图4-4_维度组合分布_V3`
- `V3结果图件来源登记.csv`

每幅图同时登记唯一编码表SHA-256、PNG/PDF路径及文件SHA-256。图内不写推断性标题，论文中的图题和解释必须继续遵守结果边界。

## 六、独立复算

```bash
python3 07_analysis/scripts/validate_v3_final_outputs.py \
  --coding "07_analysis/data/第35至42届科学思维V3唯一编码表.csv" \
  --results-dir "07_analysis/results/v3_final" \
  --figures-dir "08_manuscript/figures/v3_final" \
  --qa-output "09_quality/第35至42届科学思维V3正式结果复算QA_G8-68.csv"
```

独立复算覆盖唯一键、四维覆盖、存在性与等级逻辑、人工更正、总体分布、等级分布、分届次分布、组合、共现、来源哈希和图件非空检查。任何一项失败均不得进入G8-69。

## 七、解释边界

这些统计描述第35至42届复赛理论试题的任务要求，不是学生实际作答结果。不得据此声称学生能力、教学效果、因果关系、统计显著性或命题质量优劣。跨届分布可作描述性比较，不自动构成时间趋势。

G8-68生成完成后，还需独立复算行数、比例、四维覆盖和源哈希，才能进入G8-69正文重写。
