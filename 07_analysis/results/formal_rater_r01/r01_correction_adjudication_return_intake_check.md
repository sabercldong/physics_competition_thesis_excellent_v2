# R01 更正裁决回填接收检查

## 接收范围

- 原始回填：`07_analysis/data/rater_returns/incoming/R01/r01_correction_adjudication_R01_FILLED_20260723.csv`
- 原件 SHA-256：`c091bdbf4320cb928451c824357897e97e2b3efbaba75e6804ef7e012fae55d9`
- UTF-8 BOM/LF 登记副本：`07_analysis/data/rater_returns/registered/R01/r01_correction_adjudication_R01_FILLED_20260723_registered_lf.csv`
- 登记副本 SHA-256：`2cf043003bb07dc5829cd55ea9ac82ad43ce81a0f0fe9728c5f73682b645710e`
- 裁决者：`ADJ-02`；日期：`2026-07-23`；独立性仅按其自声明登记，项目无法独立验证过程。

## 接收结果

- 回填门禁 6/6 通过：记录数、不可变键与模板行序、工作字段、决定枚举、存在性—等级逻辑、采纳建议关系均合法。
- 应用门禁 9/9 通过：876行基线字段和键完整，4条当前值逐键匹配，输出仅在4个裁决键改变，且4条最终值逐键匹配裁决。
- 基线表保留为 `07_analysis/data/final_coding.csv`（SHA-256：`23f76e0c63fad60fa02e54a4b51aeef3e83752da7fb20b46346027aa5a11e045`）。
- 新版本化表为 `07_analysis/data/final_coding_r01_correction_v1.csv`（SHA-256：`3da0ec26a25b7b78bd62088dabccbc948dc62c7435fb8672d6daaf97e59af852`）。

## 已采纳的四处变更

1. `CPHO36-Q04-1` 模型建构：`是/L3` 改为 `是/L1`。
2. `CPHO36-Q04-1` 质疑创新：`是/L4` 改为 `否/未出现`。
3. `CPHO36-Q04-2` 质疑创新：`是/L4` 改为 `否/未出现`。
4. `CPHO36-Q06-2` 质疑创新：`是/L1` 改为 `否/未出现`。

完整逐键清单见 `r01_correction_adjudication_change_manifest_v1.csv`；版本化描述统计见 `correction_v1/`。

## 结果边界

新表仅替换旧版的暂定复算对照：质疑创新出现数由87降为84，模型建构L1由108增至109、L3由73降至72。58条实质审查中仍有24条、16条高风险审查中仍有8条标为“需补充引文”；在这些实质证据缺口关闭前，第四章仍不得升级为正式研究发现，且不得用于摘要、结论、第五章机制解释、学生能力或教学效果判断。
