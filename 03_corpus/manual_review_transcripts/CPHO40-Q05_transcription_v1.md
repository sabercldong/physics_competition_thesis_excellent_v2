# CPHO40-Q05 题面校对转写稿 V1

任务：`G1-07-A1-TRANSCRIBE-40Q05`

更新时间：2026-07-15

## 来源与边界

- 试题/答案合并PDF：`03_corpus/raw_papers/cpho_40_2023_fusai_paper_solution_candidate.pdf`
- 题面页码：3-4（经视觉检查，第5题从试题PDF第3页下部开始，延续至第4页顶部；第3页上部为第4题尾部，第4页中部已进入第6题，均仅用于边界确认）
- 页面证据：
  - `03_corpus/manual_review_renders/G1-07-A1/CPHO40-Q05-paper-page-3.png`
  - `03_corpus/manual_review_renders/G1-07-A1/CPHO40-Q05-paper-page-4.png`
- 答案页码：13-16（经视觉检查，第5题答案从PDF第13页下部开始，至第16页评分标准结束；第13页上部为第4题答案尾部，第16页下部已进入第6题，仅用于边界确认）
- 答案页面证据：
  - `03_corpus/manual_review_renders/G1-07-A1/CPHO40-Q05-solution-page-13.png`
  - `03_corpus/manual_review_renders/G1-07-A1/CPHO40-Q05-solution-page-14.png`
  - `03_corpus/manual_review_renders/G1-07-A1/CPHO40-Q05-solution-page-15.png`
  - `03_corpus/manual_review_renders/G1-07-A1/CPHO40-Q05-solution-page-16.png`
- 公式核对表：`03_corpus/manual_review_transcripts/CPHO40-Q05_formula_check_v1.csv`

本稿为基于PDF渲染页的题面视觉转写稿，用于替代原OCR乱码作为后续人工校对和正式编码前复核入口。变量、上下标、矢量和希腊字母已按可见题面尽量转写；若后续制作论文附录或正式编码证据，仍应按原PDF逐字复核排版。

## 题面转写

五、（40 分）如图 5a，一个质量为 m、带电量为 e 的正点电荷在固定于原点 O 处的电偶极子作用下运动，电偶极子的电偶极矩 p 指向 z 轴正方向。设 r(t) 是点电荷在 t 时刻的位置矢量，其大小为 r(t)，与 p 的夹角为 theta(t)。已知 r(t = 0) = r_0 > 0，theta(t = 0) = theta_0，真空介电常量为 epsilon_0，电偶极子的电场和电势分别为

```text
E = [3(p . r_hat) r_hat - p] / (4 pi epsilon_0 r^3),
phi = (p . r) / (4 pi epsilon_0 r^3)
```

其中 r_hat 为 r 的单位方向矢量。

（1）假定点电荷在垂直于 z 轴的平面内绕着 z 轴作匀速圆周运动。据此确定 theta_0 以及点电荷作圆周运动的速度大小 v_0。

（2）假定 t = 0 时刻点电荷是静止的，

（i）求出在此后的运动过程中，点电荷相对原点 O 的角动量大小 L 对 theta 的依赖关系 L(theta)；

（ii）求出在此后的运动过程中，点电荷径向速率 v_r 对 r 的依赖关系 v_r(r)；

（iii）theta_0 满足什么条件时，点电荷的运动范围在空间上是有界的？不考虑点电荷与偶极子碰撞的情形，如果 theta_0 的数值正好取有界运动的边界值时，确定点电荷在竖直平面内的运动轨道；

（iv）如果 theta_0 的数值可使点电荷的运动是无界的，求点电荷的径向距离随时间的变化关系 r(t)。

## 图件核对提示

- 图 5a：z 轴、电偶极矩 p、原点 O、位置矢量 r、夹角 theta、点电荷标记 e,m。
- 现有题图文件：`03_corpus/item_assets/CPHO40-Q05-figure1-page3-raw.png`。
- 本轮只确认题面页中图 5a 的基本元素可见；`CPHO40-Q05-FIG` 仍为独立图件校对项，尚未销项。

## 待复核点

1. 本稿使用 `theta`、`theta_0`、`epsilon_0`、`r_hat`、`v_0`、`v_r` 等ASCII近似记录；正式附录或论文正文需统一转为项目采用的公式排版格式。
2. 题面中的电场、电势、初始条件、静止条件和“垂直于 z 轴的平面”会直接影响建模和编码证据，最终排版需逐字复核。
3. 第3页上部仍是第4题内容，第4页中部已进入第6题，本轮保留其渲染图作为边界确认，不得把第4题或第6题内容混入第5题题面证据。
4. 答案PDF第13页上部为第4题答案尾部，第16页下部已进入第6题，本轮保留这些页面作为第5题答案边界确认，不得把相邻题目内容纳入第5题公式证据。
5. 本稿未关闭 `CPHO40-Q05-FIG`，题图裁边、图注与论文用重裁或重绘仍需单独销项。
