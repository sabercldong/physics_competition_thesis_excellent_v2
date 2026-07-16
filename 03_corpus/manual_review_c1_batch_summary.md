# G1-07-C1：题图裁边与图注核对摘要

## 任务边界

本文件记录C组“题图裁边与图注校对”入口建设进度。它只处理题图来源、裁边、图号、图注和相邻内容边界，不改写题干、答案、原始PDF或论文正文，不填写真实校对人和校对日期。

## 已处理条目

| 队列 | issue_id | 材料 | 受影响小问数 | 当前状态 |
|---|---|---|---:|---|
| 101 | CPHO40-Q03-FIG | 第40届第3题 | 6 | 已建立题图核对入口和图3a重裁候选图，待最终复核 |

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

## 下一最小任务

`G1-07-C1-FIG-42Q02`：继续处理C组队列第102项 `CPHO42-Q02-FIG`。队列第099项 `CPHO41-Q02-FIG` 和第100项 `CPHO41-Q07-FIG` 已为“内部视觉终检完成，待人工确认”，若要正式销项仍需真实确认记录。
