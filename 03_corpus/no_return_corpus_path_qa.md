# G1-07-NO-RETURN-CORPUS-PATH-QA 无真实回填语料证据路径QA报告

更新时间：2026-07-19

## 性质声明

本QA按照无真实回填队列 `NQ-02`，检查转写稿、公式核对表、页面证据图、候选图、图件索引和A/B/C/D回填包中的本地路径是否可定位。它只证明路径入口当前可达，不填写真实校对人、真实校对日期、校对决定、分值、图号边界、专家意见、评分者记录、问卷结果、课堂结果或论文正文结论，也不关闭154项待核问题。

## QA结论

- QA检查项：82项。
- 通过项：77项。
- 不通过项：5项。
- 路径明细：4375条引用，覆盖898个唯一文件路径。
- 断链数量：0条。
- 主要路径角色：rendered_page_files=1182；source_pdf=676；render_file=341；file_path=335；packet_file=308；qa_file=308；source_file=306；markdown_path_ref=301；contact_sheet_file=92；review_entry_path=76；candidate_figure_files=64；original_figure_files=63。
- A组回填包76项、B组回填包22项、C组回填包47项、D组回填包9项均可定位到对应入口路径。
- 渲染索引当前覆盖A1 188行、B1 153行、C1 264行、D1 71行。
- C组47项中，45项由C1批次日志覆盖，`CPHO41-Q02-FIG` 和 `CPHO41-Q07-FIG` 由第41届特殊图件终检、重裁说明和manifest覆盖；这属于路径组织边界，不是断链。
- 5项不通过均为CSV编码或换行格式问题，不是路径断链。
- 动作计划154项真实校对人、日期、决定和复核后证据位置仍为空，正式阻断表6项仍为“阻断”。

## 主要来源表路径引用量

- `03_corpus/manual_review_a_closure_packet_v1.csv`：528条路径引用
- `03_corpus/manual_review_c1_render_index.csv`：528条路径引用
- `03_corpus/manual_review_a1_batch_log.csv`：452条路径引用
- `03_corpus/manual_review_a1_render_index.csv`：376条路径引用
- `03_corpus/manual_review_c_closure_packet_v1.csv`：326条路径引用
- `03_corpus/manual_review_closure_action_plan_v1.csv`：308条路径引用
- `03_corpus/manual_review_closure_packet_master_index_v1.csv`：308条路径引用
- `03_corpus/manual_review_b1_render_index.csv`：306条路径引用
- `03_corpus/manual_review_c1_batch_log.csv`：256条路径引用
- `03_corpus/manual_review_b_closure_packet_v1.csv`：197条路径引用

## 边界疑点与处理

| 疑点 | 当前判断 | 处理边界 |
|---|---|---|
| C组47项与C1批次45行不相等 | 不是断链；第41届第2题和第7题图件走特殊终检与重裁manifest路径 | 后续C组真实回填时仍需逐项填写真实图件可用性、重绘决定和最终图件位置 |
| 5个CSV存在编码或换行格式问题 | `manual_review_a1_batch_log.csv`、`manual_review_b1_batch_log.csv`、`manual_review_a1_render_index.csv`、`manual_review_b1_render_index.csv` 缺少UTF-8 BOM；`CPHO41_Q02_Q07_recrop_manifest.csv` 使用CRLF换行 | 后续格式修复任务中统一转为UTF-8 BOM与LF后复查；本任务先如实登记，不把格式问题写成路径断链 |
| 路径可达不等于校对完成 | 本QA只确认文件能找到 | 不得写成题干、公式、图件、分值或参考解答已正式人工校对 |
| 候选图存在不等于论文定稿图 | 候选图、原裁图、对照图当前均为内部复核材料 | 不得把候选图写成案例定稿图或附录定稿图 |
| 渲染页可达不等于页码边界最终确认 | 页面证据可定位，但真实终核字段仍为空 | 正式编码前仍需真实人工终核和回填整合QA |

## 仍然不能说明的内容

- 不能说明154项人工终核已经完成。
- 不能说明任何题干、公式、题图、分值或参考解答已经正式校对。
- 不能说明可以进入正式A/B评分者编码、正式统计、正式案例结论、教师验证或课堂效果结论。
- 不能把路径QA、内部转写、公式核对入口、候选图或页面渲染图写成真实专家审查、真实评分者一致性、导师确认或正式结果分析。
- 不能据此修改 `08_manuscript/` 正文或 `09_quality/claim_evidence_matrix.csv`。

## 下一步最小任务

`G1-07-C-NO-RETURN-FIGURE-QUEUE`：按照无真实回填队列 `NQ-03`，汇总C组候选图、原裁图、对照图、重绘需求和图号图注疑点，形成C组候选图件待核分层清单；该任务仍不得把候选图写成论文最终图。

## 输出文件

- QA报告：`03_corpus/no_return_corpus_path_qa.md`
- QA记录表：`03_corpus/no_return_corpus_path_qa_v1.csv`
- 路径明细表：`03_corpus/no_return_corpus_path_audit_v1.csv`
