# G1-07-MANUAL-CLOSURE-ACTION-PLAN 人工终核真实销项动作计划

更新时间：2026-07-19

## 性质声明

本计划把154项正式编码前人工终核问题压缩为可执行顺序、最小校对动作、回填字段和进入正式编码的判定门槛。它只是一份真实销项动作计划，不填写真实校对人、真实校对日期、校对决定、专家意见、问卷结果、课堂结果、分值结论或论文正文结论。

## 当前到达的位置

- 上游待核清单、优先队列、真实销项计划、A/B/C/D回填包、总索引和准备报告已经建立。
- 本轮新增动作计划表：`03_corpus/manual_review_closure_action_plan_v1.csv`。
- 154项均已有可定位入口，但当前真实销项数仍为0。
- 当前可以进入“真实人工终核执行”，不能进入“正式编码、正式统计、正式案例结论、显著性结论、专家审查结论、教师验证或课堂效果结论”。

## 执行阶段

| 阶段 | 名称 | 项数 | 最小动作 |
|---|---|---:|---|
| PHASE-0 | 执行前准备 | 不对应单条问题 | 确认只使用A/B/C/D回填包和页面证据；确定真实校对人编码规则；不得预填日期、决定或结论。 |
| PHASE-1 | A组优先终核 | 76 | 优先关闭直接阻塞正式编码证据的题干OCR、公式和特殊符号问题。 |
| PHASE-2 | B组公式终核 | 22 | 关闭中风险公式与特殊符号问题，保证正式编码证据摘录不被公式错误污染。 |
| PHASE-3 | C组图件终核 | 47 | 判断候选题图是否可用于案例、附录和论文图件；不可用时进入重绘或继续待核。 |
| PHASE-4 | D组分值与附属图终核 | 9 | 确认第35届分值边界来源和第42届第3题题解图边界；来源不足时不得做分值统计或附录定稿。 |
| PHASE-5 | 回填后门禁检查 | 154 | 检查真实回填字段、修订记录和复核后证据位置；全部通过后才进入正式编码准备。 |

## 分组计数

| 组别 | 项数 |
|---|---:|
| A | 76 |
| B | 22 |
| C | 47 |
| D | 9 |

## 销项路线计数

| 销项路线 | 项数 |
|---|---:|
| TEXT_FORMULA_FINAL_REVIEW | 98 |
| FIG_FINAL_REVIEW_OR_REDRAW | 47 |
| SCORE_RUBRIC_REQUIRED | 8 |
| SOLFIG_APPENDIX_BOUNDARY_REQUIRED | 1 |

## 建议批次计数

| 建议批次 | 项数 |
|---|---:|
| BATCH-01 | 76 |
| BATCH-02 | 22 |
| BATCH-03 | 47 |
| BATCH-04 | 9 |

## 问题类型计数

| 问题类型 | 项数 |
|---|---:|
| 题干OCR校对 | 38 |
| 公式与特殊符号校对 | 60 |
| 题图裁边与图注校对 | 47 |
| 第35届分值边界复核 | 8 |
| 解答放大图一致性核对 | 1 |

## 届次覆盖

| 届次 | 项数 |
|---|---:|
| 41 | 19 |
| 40 | 24 |
| 42 | 20 |
| 37 | 22 |
| 38 | 24 |
| 36 | 13 |
| 39 | 11 |
| 35 | 21 |

## 每组最小回填要求

| 组别 | 必填回填字段 | 未满足时禁止进入的环节 |
|---|---|---|
| A | actual_reviewer_or_code; actual_review_date; actual_review_decision; correction_required; correction_summary; post_review_evidence_location; post_review_status | 正式编码证据摘录、正式A/B评分者编码、正式结果统计 |
| B | actual_reviewer_or_code; actual_review_date; actual_review_decision; correction_required; correction_summary; post_review_evidence_location; post_review_status | 正式编码证据摘录、公式支撑性案例、正式结果统计 |
| C | actual_reviewer_or_code; actual_review_date; actual_review_decision; figure_usable_for_manuscript; redraw_required; correction_required; correction_summary; final_figure_file_or_evidence_location; post_review_status | 典型案例图件、附录图件、论文定稿图、图像表征结论 |
| D | actual_reviewer_or_code; actual_review_date; actual_review_decision; official_score_source_or_fig_boundary_confirmed; score_value_or_fig_boundary_statement; correction_required; correction_summary; final_evidence_location; post_review_status | 第35届分值统计、第42届第3题附属图件定稿、案例附属证据结论 |

## 进入正式编码的总门槛

1. 154项 `actual_reviewer_or_code`、`actual_review_date`、`actual_review_decision` 不得为空。
2. 每项必须有复核后证据位置；若需要修订，必须记录修订摘要和修订后的证据位置。
3. A组和B组必须先于正式编码完成；否则题干、公式和特殊符号证据仍不能作为正式编码输入。
4. C组若未完成，相关题图不得用于典型案例、附录或论文定稿图；可暂时只保留文字证据，并在正文中标记图件待核。
5. D组若未完成，第35届分值不得进入正式分值统计；第42届第3题题解放大图不得写成题面图原样放大。
6. 回填完成后仍需另做回收完整性检查、正式评分者独立编码、一致性计算和分歧裁决；本计划本身不替代这些步骤。

## 当前不能继承或声称的内容

- 不能声称第35至42届题干、公式、图件、分值和参考解答已经完成正式人工校对。
- 不能把内部转写、候选图、视觉检查或Codex预演写成真实专家审查、真实评分者编码或导师确认。
- 不能生成正式统计百分比、显著性结果、问卷结果、课堂实验结果或教学效果结论。
- 不能把第35届当前PDF未明示分值的问题补成正式分值，也不能自行补造评分细则。
- 不能把第42届第3题题解图写成题面图原样放大；必须等待附录图号边界确认。

## 下一步最小任务

`G1-07-MANUAL-CLOSURE-ACTION-PLAN-QA`：检查本动作计划是否覆盖154项、A/B/C/D计数是否与总索引一致、CSV是否为UTF-8 BOM和LF换行、真实回填栏是否全部空白，以及本轮是否未混入正文、原始文件或主张矩阵改动。

## 输出文件

- 动作计划表：`03_corpus/manual_review_closure_action_plan_v1.csv`
- 本说明：`03_corpus/manual_review_closure_action_plan.md`
- 上游来源：`03_corpus/manual_review_closure_packet_master_index_v1.csv`、`03_corpus/manual_review_closure_ready_report.md`
