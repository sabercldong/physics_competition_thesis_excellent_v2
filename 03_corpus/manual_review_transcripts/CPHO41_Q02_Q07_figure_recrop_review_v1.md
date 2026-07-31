# CPHO41-Q02/Q07 题图重裁候选记录 V1

任务：`G1-07-A1-FIG-REDRAW-41Q02-Q07`

## 处理边界

- 本轮只从已渲染的原始题面页面重新裁切图件，不重绘、不补字、不修图、不改动 `00_originals/` 或原始PDF；
- 新图件是来源明确的候选图，可用于后续人工复核、附录准备或正式图件重绘参考；
- 因未填写真实校对人和校对日期，本轮不关闭 `CPHO41-Q02-FIG` 或 `CPHO41-Q07-FIG`；
- 若正式论文需要高清出版图，仍建议在人工确认后依据这些候选图重绘矢量版或重新导出高分辨率图。

## 输出清单

| 图件 | 输出文件 | 来源页 | 裁切框 | 复核要点 |
|---|---|---|---|---|
| CPHO41-Q02-FIG2A-RECROP-V1 | `03_corpus/item_assets/CPHO41-Q02-figure2a-page1-recrop-v1.png` | `03_corpus/manual_review_renders/G1-07-A1/CPHO41-Q02-paper-page-1.png` | `3080,4380,3835,5150` | 保留图2a、Q/T球、x/y轴、phi/theta/v_T/v_Q标记和图号。 |
| CPHO41-Q02-FIG2B-RECROP-V1 | `03_corpus/item_assets/CPHO41-Q02-figure2b-page2-recrop-v1.png` | `03_corpus/manual_review_renders/G1-07-A1/CPHO41-Q02-paper-page-2.png` | `2960,640,3840,1535` | 保留图2b、Q/T球、x/y轴、v_T、v_Q0、theta_f、phi等标记。 |
| CPHO41-Q02-FIG2C-RECROP-V1 | `03_corpus/item_assets/CPHO41-Q02-figure2c-page2-recrop-v1.png` | `03_corpus/manual_review_renders/G1-07-A1/CPHO41-Q02-paper-page-2.png` | `3130,1660,3850,2185` | 保留图2c、球杆/球/桌面、M、omega_0、v_0、h和图号。 |
| CPHO41-Q02-TABLE-RECROP-V1 | `03_corpus/item_assets/CPHO41-Q02-table-page2-recrop-v1.png` | `03_corpus/manual_review_renders/G1-07-A1/CPHO41-Q02-paper-page-2.png` | `520,3020,3300,3350` | 保留phi、theta_f两行表头及六个取值栏，左右边框完整。 |
| CPHO41-Q07-FIG7A-RECROP-V1 | `03_corpus/item_assets/CPHO41-Q07-figure7a-page4-recrop-v1.png` | `03_corpus/manual_review_renders/G1-07-A1/CPHO41-Q07-paper-page-4.png` | `3150,3510,3900,3995` | 保留圆环、电子符号和图7a图号。 |
| CPHO41-Q07-FIG7B-RECROP-V1 | `03_corpus/item_assets/CPHO41-Q07-figure7b-page4-recrop-v1.png` | `03_corpus/manual_review_renders/G1-07-A1/CPHO41-Q07-paper-page-4.png` | `3210,4265,3900,5015` | 保留圆环、电子符号、磁通箭头、Phi标记和图7b图号。 |

## 当前判断

1. 第41届第2题图2a、图2b、图2c和第(4.3)问空表已形成重裁候选版，旧裁切中的邻近题干或公式残边风险有所降低。
2. 第41届第7题图7a和图7b已形成统一重裁候选版，其中图7b旧裁切左侧邻近题干残边已通过重裁处理。
3. 所有候选图均来自 `03_corpus/manual_review_renders/G1-07-A1/` 的页面证据图，生成信息登记在 `03_corpus/item_assets/CPHO41_Q02_Q07_recrop_manifest.csv`。
4. 本记录不等同于真实人工校对完成，不生成正式编码证据摘录，也不替代后续论文用图的最终审定。

## 后续最小动作

- 若继续处理图件：人工打开六张候选图与原PDF页对照，确认图号、变量、箭头、电子符号和表格边框是否完整，再决定是否关闭FIG项；
- 若转向扩大语料校对：继续 `G1-07-A1-TRANSCRIBE-40Q03`，处理A组后续高风险OCR/公式问题。
