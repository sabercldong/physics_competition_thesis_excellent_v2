# G1-07-D1：D组附属证据核对摘要

## 任务边界

本文件记录D组“元数据或案例附属证据”入口建设进度，当前包括第35届分值边界复核和第42届第3题解答放大图一致性核对。它只处理分值、放大图页定位和图号边界是否能由当前PDF和现有证据页支持，不改写题干、答案、原始PDF或论文正文，不填写真实校对人和校对日期。

## 已处理条目

| 队列 | issue_id | 材料 | 受影响小问数 | 当前状态 |
|---|---|---|---:|---|
| 146 | CPHO35-Q02-SCORE | 第35届第2题 | 4 | 已建立分值边界核对入口，待最终复核 |
| 147 | CPHO35-Q03-SCORE | 第35届第3题 | 4 | 已建立分值边界核对入口，待最终复核 |
| 148 | CPHO35-Q04-SCORE | 第35届第4题 | 4 | 已建立分值边界核对入口，待最终复核 |
| 149 | CPHO35-Q08-SCORE | 第35届第8题 | 4 | 已建立分值边界核对入口，待最终复核 |
| 150 | CPHO35-Q05-SCORE | 第35届第5题 | 3 | 已建立分值边界核对入口，待最终复核 |
| 151 | CPHO35-Q06-SCORE | 第35届第6题 | 3 | 已建立分值边界核对入口，待最终复核 |
| 152 | CPHO42-Q03-SOLFIG | 第42届第3题 | 3 | 已建立解答放大图一致性核对入口，待最终复核 |
| 153 | CPHO35-Q01-SCORE | 第35届第1题 | 2 | 已建立分值边界核对入口，待最终复核 |
| 154 | CPHO35-Q07-SCORE | 第35届第7题 | 2 | 已建立分值边界核对入口，待最终复核 |

## CPHO35-Q01

- 分值边界核对表：`03_corpus/manual_review_transcripts/CPHO35-Q01_score_boundary_check_v1.csv`
- 题面证据：`03_corpus/manual_review_renders/G1-07-D1/CPHO35-Q01-paper-page-1.png`
- 答案证据：`03_corpus/manual_review_renders/G1-07-D1/CPHO35-Q01-solution-page-06.png` 至 `CPHO35-Q01-solution-page-09.png`
- 下一题排除边界：`03_corpus/manual_review_renders/G1-07-D1/CPHO35-Q01-solution-page-09.png`

核对结论：

1. 第1题题面位于试题PDF第1页上半部，题面可确认两个小问。
2. 当前题面页未见大题分值或小问分值标注。
3. 答案第6页开始重印第1题题面并给出参考解答，第7至8页为第1题推导，第9页上半部为第1题时间积分、最终时间表达式和临界时间结果；当前答案证据页未见评分标准或小问分值拆分。
4. 第9页下半部进入第2题，仅作第1题答案范围排除边界，不提供第1题分值信息。
5. `item_index.csv` 中第35届第1题两个小问的分值字段已由“待人工复核；小问待拆”改为“未见PDF明示，待最终复核”，避免误读为已有具体分值。

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

## CPHO35-Q05

- 分值边界核对表：`03_corpus/manual_review_transcripts/CPHO35-Q05_score_boundary_check_v1.csv`
- 题面证据：`03_corpus/manual_review_renders/G1-07-D1/CPHO35-Q05-paper-page-2.png` 和 `CPHO35-Q05-paper-page-3.png`
- 答案证据：`03_corpus/manual_review_renders/G1-07-D1/CPHO35-Q05-solution-page-19.png` 至 `CPHO35-Q05-solution-page-28.png`
- 下一题排除边界：`03_corpus/manual_review_renders/G1-07-D1/CPHO35-Q05-solution-page-28.png`

核对结论：

1. 第5题题面从试题PDF第2页下部开始，延续至第3页上部，题面可确认三个小问。
2. 当前题面页未见大题分值或小问分值标注。
3. 答案第19页上部为第4题收尾，第5题从题面重印和解法（一）开始；第20至27页为第5题多种解法推导；第28页上部为第5题解法（五）收尾；当前答案证据页未见评分标准或小问分值拆分。
4. 第28页下部进入第6题，仅作第5题答案范围排除边界，不提供第5题分值信息。
5. `item_index.csv` 中第35届第5题三个小问的分值字段已由“待人工复核；小问待拆”改为“未见PDF明示，待最终复核”，避免误读为已有具体分值。

## CPHO35-Q06

- 分值边界核对表：`03_corpus/manual_review_transcripts/CPHO35-Q06_score_boundary_check_v1.csv`
- 题面证据：`03_corpus/manual_review_renders/G1-07-D1/CPHO35-Q06-paper-page-3.png`
- 答案证据：`03_corpus/manual_review_renders/G1-07-D1/CPHO35-Q06-solution-page-28.png` 至 `CPHO35-Q06-solution-page-31.png`
- 下一题排除边界：`03_corpus/manual_review_renders/G1-07-D1/CPHO35-Q06-solution-page-31.png`

核对结论：

1. 第6题题面位于试题PDF第3页下半部，题面可确认三个小问。
2. 当前题面页未见大题分值或小问分值标注。
3. 答案第28页上半部为第5题收尾，下半部开始第6题题面重印；第29至30页为第6题参考解答；第31页上半部为第6题解答收尾，当前答案证据页未见评分标准或小问分值拆分。
4. 第31页下半部进入第7题，仅作第6题答案范围排除边界，不提供第6题分值信息。
5. `item_index.csv` 中第35届第6题三个小问的分值字段已由“待人工复核；小问待拆”改为“未见PDF明示，待最终复核”，避免误读为已有具体分值。

## CPHO35-Q07

- 分值边界核对表：`03_corpus/manual_review_transcripts/CPHO35-Q07_score_boundary_check_v1.csv`
- 题面证据：`03_corpus/manual_review_renders/G1-07-D1/CPHO35-Q07-paper-page-4.png`
- 答案证据：`03_corpus/manual_review_renders/G1-07-D1/CPHO35-Q07-solution-page-31.png` 至 `CPHO35-Q07-solution-page-35.png`
- 下一题排除边界：`03_corpus/manual_review_renders/G1-07-D1/CPHO35-Q07-solution-boundary-next-page-36.png`

核对结论：

1. 第7题题面完整位于试题PDF第4页，题面可确认两个小问。
2. 当前题面页未见大题分值或小问分值标注。
3. 答案第31页上半部为第6题收尾，下半部开始第7题题面重印；第32页为图a，第33页为图b和参考解答起点，第34页为核心推导，第35页上半部为第7题最终结果；当前答案证据页未见评分标准或小问分值拆分。
4. 第35页下半部进入第8题；第36页已为第8题解答，仅作第7题答案范围排除边界，不提供第7题分值信息。
5. `item_index.csv` 中第35届第7题两个小问的分值字段已由“待人工复核；小问待拆”改为“未见PDF明示，待最终复核”，避免误读为已有具体分值。

## CPHO42-Q03-SOLFIG

- 解答放大图核对表：`03_corpus/manual_review_transcripts/CPHO42-Q03_solution_figure_large_check_v1.csv`
- 题面证据：`03_corpus/manual_review_renders/G1-07-D1/CPHO42-Q03-paper-page-2.png` 和 `CPHO42-Q03-paper-page-3.png`
- 解答证据：`03_corpus/manual_review_renders/G1-07-D1/CPHO42-Q03-solution-page-07.png` 至 `CPHO42-Q03-solution-page-10.png`
- 放大图证据：`03_corpus/manual_review_renders/G1-07-D1/CPHO42-Q03-solution-figlarge-page-26.png` 和 `CPHO42-Q03-solution-figlarge-page-27.png`

核对结论：

1. 解答第7页明示“本题解图中的字号较小，放大图见P26和P27”。
2. 第26页呈现题解图3a和题解图3b；当前视觉核对显示其保留解答页小图中的端口、测压端、电流方向、开关导线和连接关系。
3. 第27页呈现题解图3c；当前视觉核对显示其保留解答页小图中的器件(a)/(b)、顶端/中央电流、U3/U7测压端和三重并联连接关系。
4. 题解图3a-3c是参考解答推导用等效电路图，不是题面图3a-3d的一一原样放大。论文或附录引用时必须区分“题面图”和“题解图”。
5. 本项只建立D组核对入口，不关闭 `CPHO42-Q03-FIG`，也不代表附录用图正式定稿。

## 不可声称

- 不能声称第35届第2题大题分值已经由当前PDF确认。
- 不能声称第35届第2题四个小问存在已核定配分。
- 不能声称第35届第1题大题分值已经由当前PDF确认。
- 不能声称第35届第1题两个小问存在已核定配分。
- 不能声称第35届第3题大题分值已经由当前PDF确认。
- 不能声称第35届第3题四个小问存在已核定配分。
- 不能声称第35届第4题大题分值已经由当前PDF确认。
- 不能声称第35届第4题四个小问存在已核定配分。
- 不能声称第35届第8题大题分值已经由当前PDF确认。
- 不能声称第35届第8题四个小问存在已核定配分。
- 不能声称第35届第5题大题分值已经由当前PDF确认。
- 不能声称第35届第5题三个小问存在已核定配分。
- 不能声称第35届第6题大题分值已经由当前PDF确认。
- 不能声称第35届第6题三个小问存在已核定配分。
- 不能声称第35届第7题大题分值已经由当前PDF确认。
- 不能声称第35届第7题两个小问存在已核定配分。
- 不能声称第42届第3题题解放大图已经完成正式人工校对。
- 不能把第42届第3题题解图3a-3c误作题面图3a-3d的一一原样放大。
- 不能声称第42届第3题题面图、题解图或论文附录用图已经正式定稿。
- 不能据此生成正式分值统计、评分结论或论文附录分值。

## 下一步

D组9项附属证据入口均已建立。下一步最小任务建议转入 `G1-07-FOLLOWUP-COVERAGE-AUDIT`：汇总154项人工校对入口覆盖情况、仍未真实销项的缺口和正式编码前门禁；若后续获得第35届正式评分细则或更清晰原卷，再回填第1题至第8题最终复核记录；若正式论文附录需要使用第42届第3题题解放大图，需在附录排版前完成真实人工终核和图号命名边界确认。
