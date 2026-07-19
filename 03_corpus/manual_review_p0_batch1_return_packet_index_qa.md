# P0第一批真实回填交接包索引QA

任务编号：`G1-07-FOLLOWUP-MANUAL-P0-BATCH1-RETURN-PACKET-INDEX-QA`

## 性质声明

本文件只检查 `03_corpus/manual_review_p0_batch1_return_packet_index.md` 与 `03_corpus/manual_review_p0_batch1_return_packet_index_v1.csv` 的结构完整性、路径可定位性和禁写边界。它不代表真实人工校对已经发生，不关闭任何人工校对项，不修改题文，不生成正式编码、正式统计、论文正文或 `final_coding.csv`。

## QA结论

本轮完成35项QA检查，结论为通过。

已确认：

- Markdown索引和CSV索引均存在；
- CSV索引为UTF-8 BOM和LF换行；
- `P0B1PKT-01` 至 `P0B1PKT-11` 连续唯一；
- 交接包覆盖6类材料、11个文件；
- 11个引用文件均可定位；
- 11项 `release_status` 均为 `不放行：交接索引，未真实回填`；
- 索引说明包含交接顺序、后续最短流程和禁写边界；
- 索引未把真实人工校对、正式编码、正式统计或论文结果写成已完成。

结构化QA表见：

- `03_corpus/manual_review_p0_batch1_return_packet_index_qa_v1.csv`

## 仍不能声称

QA通过后仍不得声称：

- P0第一批真实人工校对已经完成；
- 38个题目级小批次已经销项；
- 第一批76条OCR、公式与特殊符号问题已经关闭；
- 第37、38、40、41、42届题文已经正式无误；
- P0条目可以全部进入正式评分者模板；
- 真实双评分者编码、一致性检验、分歧裁决或 `final_coding.csv` 已经完成；
- 第四章正式统计、典型案例结论或论文结果已经成立。

## 下一最小任务

下一步可执行 `G1-07-FOLLOWUP-MANUAL-P0-BATCH1-RETURN-INTAKE-READY-CHECK`：在不填写真实回填的前提下，检查P0第一批回填材料是否已经具备接收真实回填副本的最小条件，包括接收目录规则、回填副本命名、校验值记录和整合前冻结边界。
