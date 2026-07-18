# 剩余B/C/D真实回填接收登记

## 性质声明

本文件是 `G1-07-REMAINING-RETURN-PACKET-HANDOFF-REGISTER` 的接收登记说明。它只建立剩余B/C/D材料的真实回填接收入口，不代表已经收到真实回填，不代表人工校对已经销项，也不放行正式编码、正式统计或论文正文结果写作。

## 上游依据

- `03_corpus/manual_review_b_closure_packet_v1.csv`
- `03_corpus/manual_review_c_closure_packet_v1.csv`
- `03_corpus/manual_review_d_closure_packet_v1.csv`
- `03_corpus/manual_review_closure_action_plan_v1.csv`
- `03_corpus/manual_review_closure_packet_master_index_v1.csv`
- `03_corpus/manual_review_return_integration_protocol_v1.csv`
- `03_corpus/manual_review_real_return_handoff_register_v1.csv`

## 登记范围

本轮登记剩余 78 项待真实回填问题：B组 22 项、C组 47 项、D组 9 项。登记表见 `03_corpus/manual_review_remaining_return_handoff_register_v1.csv`。

| 组别 | 数量 | 主要用途 | 对应RIP规则 | 当前状态 |
|---|---:|---|---|---|
| B组 | 22 | 公式与特殊符号终核 | RIP-05, RIP-11 | 未收到真实回填，不放行 |
| C组 | 47 | 题图裁边、图注、可用性或重绘终核 | RIP-06, RIP-12 | 未收到真实回填，不放行 |
| D组 | 9 | 第35届分值来源或第42届第3题附属图边界 | RIP-07, RIP-13 | 未收到真实回填，不放行 |

## 推荐接收目录

登记表为每行预置以下推荐目录，但本任务不创建真实回填目录：

- `03_corpus/manual_review_returns/incoming/REMAINING-B/`
- `03_corpus/manual_review_returns/incoming/REMAINING-C/`
- `03_corpus/manual_review_returns/incoming/REMAINING-D/`
- `03_corpus/manual_review_returns/registered/REMAINING-B/`
- `03_corpus/manual_review_returns/registered/REMAINING-C/`
- `03_corpus/manual_review_returns/registered/REMAINING-D/`
- `03_corpus/manual_review_returns/quarantine/REMAINING-B/`
- `03_corpus/manual_review_returns/quarantine/REMAINING-C/`
- `03_corpus/manual_review_returns/quarantine/REMAINING-D/`
- `03_corpus/manual_review_returns/integration_logs/REMAINING-B/`
- `03_corpus/manual_review_returns/integration_logs/REMAINING-C/`
- `03_corpus/manual_review_returns/integration_logs/REMAINING-D/`

推荐文件名格式为 `return_YYYYMMDD_组别_remaining_issue_id_reviewerCode_seq.ext`，允许扩展名为 `csv;xlsx;pdf;zip`。收到真实副本后，必须登记来源文件名、另存路径、校验值、文件大小、接收日期、接收人、回填人代码和回填日期。

## 必填回填字段

- B组：`actual_reviewer_or_code`、`actual_review_date`、`actual_review_decision`、`correction_required`、`correction_summary`、`post_review_evidence_location`、`post_review_status`。
- C组：`actual_reviewer_or_code`、`actual_review_date`、`actual_review_decision`、`figure_usable_for_manuscript`、`redraw_required`、`correction_required`、`correction_summary`、`final_figure_file_or_evidence_location`、`post_review_status`。
- D组：`actual_reviewer_or_code`、`actual_review_date`、`actual_review_decision`、`official_score_source_or_fig_boundary_confirmed`、`score_value_or_fig_boundary_statement`、`correction_required`、`correction_summary`、`final_evidence_location`、`post_review_status`。

## 当前不能声称的内容

- 不能声称B组公式终核已经完成；
- 不能声称C组候选图已经成为论文定稿图；
- 不能声称D组第35届分值或第42届第3题附属图边界已经确认；
- 不能声称剩余78项已经真实销项；
- 不能基于本登记进入正式编码、正式统计、显著性结论、问卷结果、教学实验结果或正文结果章写作；
- 不能把本项目内部流程写成真实专家审查、导师确认或竞赛教师审查。

## 下一最小任务

`G1-07-REMAINING-RETURN-PACKET-HANDOFF-REGISTER-QA`：检查剩余78项接收登记的行数、组别计数、编号连续性、上游集合一致性、空白保护、放行门禁、目录未创建状态和提交边界。

## 输出边界

本任务新增接收登记与规则，不修改 `00_originals/`，不修改 `08_manuscript/`，不修改 `09_quality/claim_evidence_matrix.csv`，不修改 `02_literature/references.bib`，不创建 `03_corpus/manual_review_returns/` 真实回填目录。
