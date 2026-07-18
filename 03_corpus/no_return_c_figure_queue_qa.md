# G1-07-C-NO-RETURN-FIGURE-QUEUE-QA C组候选图件待核清单QA

更新时间：2026-07-19

## 性质声明

本QA只检查 `03_corpus/no_return_c_figure_queue_v1.csv` 和 `03_corpus/no_return_c_figure_queue.md` 是否完整、可复核、未越界。它不填写真实校对人、真实校对日期或最终校对决定，不关闭C组47项，不确认论文最终图，不重绘图，也不改写论文正文或 `09_quality/claim_evidence_matrix.csv`。

## QA结论

- QA检查项：48项。
- 通过项：48项。
- 不通过项：0项。
- C组清单行数：47项。
- `issue_id` 覆盖：与C组回填包47项、C组回填包QA47项完全一致。
- 候选资产复算：64个；候选图路径64条；原裁图路径63条；来源页路径54条。
- 路径直接扫描：缺失0条。
- 优先层级复算：{'P0_SPECIAL_41_FINALCHECK': 2, 'P1_BOUNDARY_OR_REDRAW_HIGH': 10, 'P3_SINGLE_FIGURE_REVIEW': 28, 'P2_MULTI_FIGURE_REVIEW': 5, 'P0_SPECIAL_SOLFIG_BOUNDARY': 1, 'P0_SPECIAL_ANSWER_REFERENCE': 1}。
- 证据链类型复算：{'SPECIAL_41_FINALCHECK_MANIFEST': 2, 'C1_BATCH_LOG_AND_RENDER_INDEX': 43, 'C1_BATCH_PLUS_D1_SOLFIG_BOUNDARY': 1, 'C1_BATCH_PLUS_ANSWER_PAGE_REFERENCE': 1}。
- 重绘需求初分层复算：{'高': 4, '中': 43}。

## 关键通过点

1. `FQ-001` 至 `FQ-047` 连续唯一，未发现漏项或额外项。
2. 第41届第2题和第7题均保留特殊终检、重裁说明和manifest证据链。
3. 第42届第3题已单独标为题面图与D组解答放大图边界关联项。
4. 第35届第7题已单独标为题面页候选图与答案页参考候选边界项。
5. 每项均写明“不得用于论文最终图”与真实终核解锁条件。

## 仍不能说明的内容

- 不能说明C组47项已经完成真实人工校对。
- 不能说明64个候选资产已经成为论文最终插图或附录定稿图。
- 不能说明同题OCR、公式、分值边界或第42届第3题附属图号问题已经销项。
- 不能据此进入正式案例图件结论、正式编码无风险声明、正式统计或论文结果章写作。

## 下一步最小任务

`G1-07-D-NO-RETURN-SCORE-SOLFIG-QUEUE`：按照无真实回填队列 `NQ-04`，整理D组第35届分值边界和第42届第3题解答放大图待核请求清单；不得生成第35届分值统计或附录定稿图结论。

## 输出文件

- QA明细表：`03_corpus/no_return_c_figure_queue_qa_v1.csv`
- 本报告：`03_corpus/no_return_c_figure_queue_qa.md`
