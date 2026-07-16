# G1-07-C1：题图裁边与图注核对摘要

## 任务边界

本文件记录C组“题图裁边与图注校对”入口建设进度。它只处理题图来源、裁边、图号、图注和相邻内容边界，不改写题干、答案、原始PDF或论文正文，不填写真实校对人和校对日期。

## 已处理条目

| 队列 | issue_id | 材料 | 受影响小问数 | 当前状态 |
|---|---|---|---:|---|
| 101 | CPHO40-Q03-FIG | 第40届第3题 | 6 | 已建立题图核对入口和图3a重裁候选图，待最终复核 |
| 102 | CPHO42-Q02-FIG | 第42届第2题 | 6 | 已建立题图核对入口和图2a/图2b修剪候选图，待最终复核 |
| 103 | CPHO42-Q05-FIG | 第42届第5题 | 6 | 已建立题图核对入口和图5b重裁候选图，待最终复核 |

## CPHO40-Q03

- 题图核对表：`03_corpus/manual_review_transcripts/CPHO40-Q03_figure_check_v1.csv`
- 原始裁图：`03_corpus/item_assets/CPHO40-Q03-figure1-page2-raw.png`
- 重裁候选图：`03_corpus/item_assets/CPHO40-Q03-figure3a-page2-recrop-v1.png`
- 裁框定位图：`03_corpus/manual_review_renders/G1-07-C1/CPHO40-Q03-paper-page-2-figure3a-crop-box.png`
- 新旧对照接触图：`03_corpus/manual_review_renders/G1-07-C1/CPHO40-Q03-figure3a-check-contact-v1.png`

视觉检查结论：

1. 图3a位于第40届第3题题面右侧，属于第3题；同页下半部第4题的图4a和图4b不得纳入本题证据。
2. 原始裁图保留球、楔块、水平地面线、角度 `theta` 和“图3a”，但左侧有邻近题干残字，边界偏紧。
3. 重裁候选图去除左侧残字，保留球体、斜面、竖直边、水平地面线、角度 `theta` 和图号。
4. 本轮只建立题图核对入口和候选图，不代表真实人工销项完成；若作为论文或附录图使用，仍需最终版式复核。

## CPHO42-Q02

- 题图核对表：`03_corpus/manual_review_transcripts/CPHO42-Q02_figure_check_v1.csv`
- 原始裁图：`03_corpus/item_assets/CPHO42-Q02-figure1-page1-raw.png`; `03_corpus/item_assets/CPHO42-Q02-figure2-page1-raw.png`
- 修剪候选图：`03_corpus/item_assets/CPHO42-Q02-figure2a-page1-recrop-v1.png`; `03_corpus/item_assets/CPHO42-Q02-figure2b-page1-recrop-v1.png`
- 裁框定位图：`03_corpus/manual_review_renders/G1-07-C1/CPHO42-Q02-paper-page-1-figure2a2b-crop-box.png`
- 新旧对照接触图：`03_corpus/manual_review_renders/G1-07-C1/CPHO42-Q02-figure2a2b-check-contact-v1.png`

视觉检查结论：

1. 图2a位于第42届第2题题面右侧，图2b位于同页下部，均属于第2题重离子束探针与能量分析器题面证据。
2. 图2a原始裁图保留一次离子束、二次离子束、测量位置、等离子体、磁场方向、接收狭缝和图号，但底部混入图2b横线；修剪候选图已去除该残边。
3. 图2b原始裁图保留平行板结构、无场区域、狭缝、`YD1`、`YD2`、`theta_I`、`theta_a`、`theta_b`、`XD`、`l=0`、`s=0` 和图号，但底部混入页码残字；修剪候选图已去除页码残字。
4. 图2b顶部 `VA` 标注边界仍偏紧；若作为论文或附录图使用，仍需最终版式复核，必要时基于源页重绘。
5. 本轮只建立题图核对入口和候选图，不填写真实校对人和校对日期，不代表正式人工销项完成。

## CPHO42-Q05

- 题图核对表：`03_corpus/manual_review_transcripts/CPHO42-Q05_figure_check_v1.csv`
- 原始裁图：`03_corpus/item_assets/CPHO42-Q05-figure1-page3-raw.png`; `03_corpus/item_assets/CPHO42-Q05-figure2-page4-raw.png`
- 重裁候选图：`03_corpus/item_assets/CPHO42-Q05-figure5b-page4-recrop-v1.png`
- 裁框定位图：`03_corpus/manual_review_renders/G1-07-C1/CPHO42-Q05-paper-pages-3-4-figure5a5b-crop-box.png`
- 新旧对照接触图：`03_corpus/manual_review_renders/G1-07-C1/CPHO42-Q05-figure5a5b-check-contact-v1.png`

视觉检查结论：

1. 图5a位于第42届第5题题面第3页右下方，图5b位于第4页第(3)问右侧，均属于第5题约瑟夫森结题面证据。
2. 图5a原始裁图保留超导体1、薄绝缘层、超导体2、电流方向、坐标轴、`lambda` 标注、中心 `O` 和图号，未见明显邻近正文残边。
3. 图5b原始裁图保留 `R`、`I`、`J`、`C`、并联结构和图号，但左侧夹带邻近正文残字；重裁候选图已去除左侧正文残字和底部正文。
4. 第4页下方进入第6题并出现图6a；图6a不得纳入第5题题图证据。
5. 本轮只建立题图核对入口和候选图，不填写真实校对人和校对日期，不代表正式人工销项完成。

## 下一最小任务

`G1-07-C1-FIG-36Q03`：继续处理C组队列第104项 `CPHO36-Q03-FIG`。队列第099项 `CPHO41-Q02-FIG`、第100项 `CPHO41-Q07-FIG`、第101项 `CPHO40-Q03-FIG`、第102项 `CPHO42-Q02-FIG` 和第103项 `CPHO42-Q05-FIG` 均仍需真实确认记录才能正式销项。
