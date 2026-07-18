# G1-07-CLOSURE-PACKET-MASTER-INDEX 人工终核回填包总索引

更新时间：2026-07-19

## 性质声明

本报告汇总A、B、C、D四组人工终核回填包及QA结果，只用于定位真实人工终核入口和正式编码前门禁。它不关闭任何人工校对项，不填写真实校对人、日期、最终决定、分值、配分、图号边界、专家意见或论文正文结论。

## 核心结论

- 总索引覆盖154项人工校对问题，与优先队列和真实销项计划一致。
- A/B/C/D四组数量分别为：A组76项、B组22项、C组47项、D组9项。
- 154项均可定位到对应组回填包；154项均可定位到QA结果或A组题目级校对单。
- 154项均有对应核对入口文件或入口路径可定位。
- 154项真实回填栏均保持空白；当前真实人工销项数仍为0。
- 真实销项状态统计：{'未真实销项': 154}。

## 分组索引

| 组别 | 项数 | 回填包 | QA/视图 | 当前边界 |
|---|---:|---|---|---|
| A组高风险OCR/公式 | 76 | `03_corpus/manual_review_a_closure_packet_v1.csv` | `03_corpus/manual_review_a_material_closure_sheet_v1.csv` | 题目级校对单已建，仍未真实销项 |
| B组中风险公式 | 22 | `03_corpus/manual_review_b_closure_packet_v1.csv` | `03_corpus/manual_review_b_closure_packet_qa_v1.csv` | 公式回填包QA通过，仍未真实销项 |
| C组题图图注 | 47 | `03_corpus/manual_review_c_closure_packet_v1.csv` | `03_corpus/manual_review_c_closure_packet_qa_v1.csv` | 图件回填包QA通过，仍未真实销项 |
| D组分值/附属证据 | 9 | `03_corpus/manual_review_d_closure_packet_v1.csv` | `03_corpus/manual_review_d_closure_packet_qa_v1.csv` | 分值/附属证据回填包QA通过，仍未真实销项 |

## 正式使用门禁

- A组76项：题干OCR、答案公式和特殊符号必须由真实校对人填写回填栏后，才能进入正式编码证据摘录。
- B组22项：中风险公式入口已齐，但仍需真实终核，不能直接写成公式校对完成。
- C组47项：题图候选图和对照图已齐，但不能写成论文定稿图或正式案例图件证据。
- D组9项：第35届8题不能生成正式分值统计；第42届第3题题解图不能误作题面图原样放大。
- 四组共同门禁：真实校对人、真实校对日期、真实决定和复核后证据位置未填写前，154项均不得视为人工销项。

## 下一步最小任务

`G1-07-MANUAL-CLOSURE-READY-REPORT`：基于总索引生成正式编码前人工终核准备报告，压缩说明当前可交给真实校对人的材料包、仍不能进入正式结果分析的原因，以及若无真实校对回填时论文只能采用的证据边界。

## 输出文件

- 总索引表：`03_corpus/manual_review_closure_packet_master_index_v1.csv`
- 本报告：`03_corpus/manual_review_closure_packet_master_index.md`
