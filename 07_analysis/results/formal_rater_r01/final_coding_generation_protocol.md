# 唯一分析表生成门禁

脚本：`07_analysis/scripts/build_final_coding.py`

## 输入与输出

输入必须是已完成裁决的 876 行表，且包含不可变键与六个裁决字段：`adjudicated_present`、`adjudicated_level`、`adjudicated_evidence`、`adjudicator`、`adjudication_date`、`adjudication_reason`。脚本通过门禁后才会生成 `07_analysis/data/final_coding.csv`。

输出把裁决存在性同时保留为 `present_label`（是/否）和 `present`（1/0），从而和 `build_descriptive_tables.py` 的数值口径一致。每行保留裁决源文件的 SHA-256，便于回溯。

## 硬门禁

1. 输入表必须恰为 876 行，且不可变键完整、唯一，并与冻结裁决模板的键集合及行序完全一致；
2. 所有六个裁决字段必须非空；
3. `adjudicated_present` 只能是“是”或“否”；
4. `adjudicated_level` 只能是 `L1` 至 `L4` 或“未出现”；
5. “否”必须配“未出现”，“是”必须配 `L1` 至 `L4`。

6. 输出路径已有 `final_coding.csv` 时，必须显式传入 `--force`，否则拒绝覆盖。

任一门禁失败时，脚本只生成 QA CSV 并以非零状态退出，绝不生成或覆盖 `final_coding.csv`。当前 R01 预填裁决表的裁决字段为空，预期无法通过该门禁。

## 推荐运行

```bash
python3 07_analysis/scripts/build_final_coding.py \
  --input 07_analysis/data/formal_adjudication_R01_FILLED_YYYYMMDD.csv
```

生成唯一分析表后，再运行 `build_descriptive_tables.py`；第35届 8 项分值缺口仍不能进入分值统计或相关结论。
