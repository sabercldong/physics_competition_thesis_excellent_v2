# G1-07-D1：第35届分值边界核对摘要

## 任务边界

本文件记录D组“第35届分值边界复核”入口建设进度。它只处理分值信息是否能由当前PDF和现有证据页支持，不改写题干、答案、原始PDF或论文正文，不填写真实校对人和校对日期。

## 已处理条目

| 队列 | issue_id | 材料 | 受影响小问数 | 当前状态 |
|---|---|---|---:|---|
| 146 | CPHO35-Q02-SCORE | 第35届第2题 | 4 | 已建立分值边界核对入口，待最终复核 |
| 147 | CPHO35-Q03-SCORE | 第35届第3题 | 4 | 已建立分值边界核对入口，待最终复核 |
| 148 | CPHO35-Q04-SCORE | 第35届第4题 | 4 | 已建立分值边界核对入口，待最终复核 |
| 149 | CPHO35-Q08-SCORE | 第35届第8题 | 4 | 已建立分值边界核对入口，待最终复核 |

## CPHO35-Q02

- 分值边界核对表：`03_corpus/manual_review_transcripts/CPHO35-Q02_score_boundary_check_v1.csv`
- 题面证据：`03_corpus/manual_review_renders/G1-07-D1/CPHO35-Q02-paper-page-1.png`
- 答案证据：`03_corpus/manual_review_renders/G1-07-D1/CPHO35-Q02-solution-page-09.png` 至 `CPHO35-Q02-solution-page-13.png`
- 下一题排除边界：`03_corpus/manual_review_renders/G1-07-D1/CPHO35-Q02-solution-boundary-next-page-14.png`

核对结论：

1. 第2题题面位于试题PDF第1页中部，题面可确认四个小问。
2. 当前题面页未见大题分值或小问分值标注。
3. 答案第9页下半部重印第2题题面，第10至13页为参考解答；当前答案证据页未见评分标准或小问分值拆分。
4. 第14页进入第3题答案，仅作第2题答案范围排除边界，不提供第2题分值信息。
5. `item_index.csv` 中第35届第2题四个小问的分值字段已由“待人工复核；小问待拆”改为“未见PDF明示，待最终复核”，避免误读为已有具体分值。

## CPHO35-Q03

- 分值边界核对表：`03_corpus/manual_review_transcripts/CPHO35-Q03_score_boundary_check_v1.csv`
- 题面证据：`03_corpus/manual_review_renders/G1-07-D1/CPHO35-Q03-paper-page-1.png` 和 `CPHO35-Q03-paper-page-2.png`
- 答案证据：`03_corpus/manual_review_renders/G1-07-D1/CPHO35-Q03-solution-page-13.png` 至 `CPHO35-Q03-solution-page-16.png`
- 下一题排除边界：`03_corpus/manual_review_renders/G1-07-D1/CPHO35-Q03-solution-boundary-next-page-17.png`

核对结论：

1. 第3题题面从试题PDF第1页页底开始，延续至第2页上半部，题面可确认四个小问。
2. 当前题面页未见大题分值或小问分值标注。
3. 答案第13页中部开始重印第3题题面并给出参考解答，第14至15页覆盖核心推导，第16页式⑳后进入第4题；当前答案证据页未见评分标准或小问分值拆分。
4. 第17页进入第4题答案，仅作第3题答案范围排除边界，不提供第3题分值信息。
5. `item_index.csv` 中第35届第3题四个小问的分值字段已由“待人工复核；小问待拆”改为“未见PDF明示，待最终复核”，避免误读为已有具体分值。

## CPHO35-Q04

- 分值边界核对表：`03_corpus/manual_review_transcripts/CPHO35-Q04_score_boundary_check_v1.csv`
- 题面证据：`03_corpus/manual_review_renders/G1-07-D1/CPHO35-Q04-paper-page-2.png`
- 答案证据：`03_corpus/manual_review_renders/G1-07-D1/CPHO35-Q04-solution-page-16.png` 至 `CPHO35-Q04-solution-page-19.png`
- 下一题排除边界：`03_corpus/manual_review_renders/G1-07-D1/CPHO35-Q04-solution-boundary-next-page-20.png`

核对结论：

1. 第4题题面位于试题PDF第2页中部，题面可确认四个小问。
2. 当前题面页未见大题分值或小问分值标注。
3. 答案第16页为第3题尾部、第4题题面重印和参考解答起点，第17至18页为核心推导，第19页上半部为第4题式⑳和答案结束；当前答案证据页未见评分标准或小问分值拆分。
4. 第20页进入第5题答案，仅作第4题答案范围排除边界，不提供第4题分值信息。
5. `item_index.csv` 中第35届第4题四个小问的分值字段已由“待人工复核；小问待拆”改为“未见PDF明示，待最终复核”，避免误读为已有具体分值。

## CPHO35-Q08

- 分值边界核对表：`03_corpus/manual_review_transcripts/CPHO35-Q08_score_boundary_check_v1.csv`
- 题面证据：`03_corpus/manual_review_renders/G1-07-D1/CPHO35-Q08-paper-page-5.png`
- 答案证据：`03_corpus/manual_review_renders/G1-07-D1/CPHO35-Q08-solution-page-35.png` 至 `CPHO35-Q08-solution-page-38.png`
- 末页边界：`03_corpus/manual_review_renders/G1-07-D1/CPHO35-Q08-solution-page-38.png`

核对结论：

1. 第8题题面完整位于试题PDF第5页，题面可确认四个小问。
2. 当前题面页未见大题分值或小问分值标注。
3. 答案第35页上部为第7题尾部，第8题从题面重印和“参考解答”开始；第36至38页覆盖第8题推导至式⑳和结尾；当前答案证据页未见评分标准或小问分值拆分。
4. 第38页为第8题答案收尾且为PDF末页，无下一题边界页，不提供第8题分值信息。
5. `item_index.csv` 中第35届第8题四个小问的分值字段已由“待人工复核；小问待拆”改为“未见PDF明示，待最终复核”，避免误读为已有具体分值。

## 不可声称

- 不能声称第35届第2题大题分值已经由当前PDF确认。
- 不能声称第35届第2题四个小问存在已核定配分。
- 不能声称第35届第3题大题分值已经由当前PDF确认。
- 不能声称第35届第3题四个小问存在已核定配分。
- 不能声称第35届第4题大题分值已经由当前PDF确认。
- 不能声称第35届第4题四个小问存在已核定配分。
- 不能声称第35届第8题大题分值已经由当前PDF确认。
- 不能声称第35届第8题四个小问存在已核定配分。
- 不能据此生成正式分值统计、评分结论或论文附录分值。

## 下一步

`G1-07-D1-SCORE-35Q05`：继续人工校对优先队列，处理队列第150项 `CPHO35-Q05-SCORE`，核对第35届第5题分值边界；若后续获得第35届正式评分细则或更清晰原卷，再回填第2题、第3题、第4题和第8题最终复核记录。
