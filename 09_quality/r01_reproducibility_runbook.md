# R01 核心材料包复现运行手册

在项目根目录运行。下列命令只验证或重建项目内的版本化结果，不验证回填者身份、独立性或实际人工过程。

## 1. 当前编码—证据链

```bash
python3 07_analysis/scripts/build_r01_current_evidence_chain.py \
  --repair-v1 07_analysis/data/rater_returns/incoming/R01/r01_evidence_repair_R01_FILLED_20260723.csv \
  --repair-v2 07_analysis/data/rater_returns/incoming/R01/r01_evidence_repair_R01_FILLED_20260723_V2.csv \
  --registered-repair-v2 07_analysis/data/rater_returns/registered/R01/r01_evidence_repair_R01_FILLED_20260723_V2_registered_lf.csv \
  --output 07_analysis/data/final_coding_evidence_r01_v1.csv \
  --qa-output 07_analysis/results/formal_rater_r01/r01_current_evidence_chain_qa_v1.csv \
  --force
```

预期：876条记录、840条V6来源、32条V2补证来源、4条ADJ-02来源，且所有检查通过。

## 2. 结果资格与正文

```bash
python3 07_analysis/scripts/validate_r01_results_eligibility.py
```

预期：`44/44通过`。输出为`09_quality/r01_results_eligibility_qa_v1.csv`。

## 3. 第五章案例材料

```bash
python3 07_analysis/scripts/build_r01_case_reselection.py
python3 07_analysis/scripts/validate_r01_case_reselection.py
```

预期：3个任务结构案例、12条逐维证据记录，案例QA `7/7通过`。

## 4. 可解释边界

所有复现输出仅描述第35至42届复赛试题及参考解答的任务认知要求。不得据此推断学生能力、教学效果、因果关系、长期趋势或第35届分值差异；学校格式、关键文献全文和真实教学证据仍需另行补齐。
