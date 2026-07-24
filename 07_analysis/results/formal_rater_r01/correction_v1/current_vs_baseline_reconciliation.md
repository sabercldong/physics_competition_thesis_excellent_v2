# G7-04-R01-CORRECTION-OUTPUT-RECONCILIATION 当前结果与基线输出对账

更新时间：2026-07-25

## 结论

`07_analysis/results/reviewed/`中的`final_*`文件是ADJ-02更正前的历史基线输出，输入为`07_analysis/data/final_coding.csv`，SHA-256为`23f76e0c63fad60fa02e54a4b51aeef3e83752da7fb20b46346027aa5a11e045`。它们应保留以复现更正前版本，但不得用于当前第四章、图4-1、图4-2、摘要、结论或候选参考工作稿。

当前唯一可用于R01描述性结果的输入为`07_analysis/data/final_coding_r01_correction_v1.csv`，SHA-256为`3da0ec26a25b7b78bd62088dabccbc948dc62c7435fb8672d6daaf97e59af852`；其统计输出只位于`07_analysis/results/formal_rater_r01/correction_v1/`。`08_manuscript/04_results.md`已使用当前版本。

## 版本差异

| 项目 | 历史基线 | 当前更正版本 | 使用规则 |
|---|---:|---:|---|
| 输入记录数 | 876 | 876 | 两版本均为219个分析单位×4维度；不能仅凭记录数判断版本正确 |
| ADJ-02受控变更键 | 0 | 4 | 当前版本只允许这4个键相对基线变更 |
| 质疑创新出现数 | 87 | 84 | 当前正文只能使用84/219（38.36%） |
| 模型建构L3数 | 73 | 72 | 当前正文只能使用72/203（35.47%） |
| 质疑创新L4数 | 10 | 8 | 当前正文只能使用8/84（9.52%） |

四个经ADJ-02采纳的变更为：`CPHO36-Q04-1`模型建构L3改为L1；同一单元的质疑创新L4改为未出现；`CPHO36-Q04-2`质疑创新L4改为未出现；`CPHO36-Q06-2`质疑创新L1改为未出现。变更依据和逐键应用检查见`../r01_correction_adjudication_change_manifest_v1.csv`与`../r01_correction_adjudication_application_qa_v1.csv`。

## 当前结果的保留边界

当前结果仅描述第35至42届219个独立小问在当前编码手册、回填与裁决链下的任务要求。它不验证评分者身份、独立性或实际人工过程，不表示学生能力、教学效果、因果、显著性、长期趋势，也不允许进行第35届分值加权或分值比较。

## 复跑顺序

```sh
BUNDLED_PY=/Users/dongxingxi/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
"$BUNDLED_PY" 07_analysis/scripts/build_formal_descriptive_outputs.py \
  --input 07_analysis/data/final_coding_r01_correction_v1.csv \
  --output-dir 07_analysis/results/formal_rater_r01/correction_v1
"$BUNDLED_PY" 07_analysis/scripts/validate_r01_results_eligibility.py
```

只有在第二条命令报告`44/44通过`后，才可使用当前目录的统计表与第四章数字。
