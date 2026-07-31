# CPHO42-Q07 题面校对转写稿 V1

任务：`G1-07-A1-TRANSCRIBE-42Q07`

更新时间：2026-07-15

## 来源与边界

- 试题PDF：`03_corpus/raw_papers/cpho_42_2025_fusai_paper_candidate.pdf`
- 题面页码：5（经视觉检查，第7题从试题PDF第5页中部“七、（45分）”开始，至第5页页末结束；第5页上半部为第6题尾部，仅用于边界确认）
- 页面证据：
  - `03_corpus/manual_review_renders/G1-07-A1/CPHO42-Q07-paper-page-5.png`
- 答案PDF：`03_corpus/raw_solutions/cpho_42_2025_fusai_solution_candidate.pdf`
- 答案页码：20-25（经视觉检查，第7题答案从答案PDF第20页下部“七、（45分）”开始，延续至第25页评分标准结束；第20页上半部为第6题解法二和评分标准）
- 答案页面证据：
  - `03_corpus/manual_review_renders/G1-07-A1/CPHO42-Q07-solution-page-20.png`
  - `03_corpus/manual_review_renders/G1-07-A1/CPHO42-Q07-solution-page-21.png`
  - `03_corpus/manual_review_renders/G1-07-A1/CPHO42-Q07-solution-page-22.png`
  - `03_corpus/manual_review_renders/G1-07-A1/CPHO42-Q07-solution-page-23.png`
  - `03_corpus/manual_review_renders/G1-07-A1/CPHO42-Q07-solution-page-24.png`
  - `03_corpus/manual_review_renders/G1-07-A1/CPHO42-Q07-solution-page-25.png`
- 公式核对表：`03_corpus/manual_review_transcripts/CPHO42-Q07_formula_check_v1.csv`

本稿为基于PDF渲染页的题面视觉转写稿，用于替代原OCR乱码作为后续人工校对和正式编码前复核入口。变量、上下标、希腊字母和公式已按可见题面尽量转写；若后续制作论文附录或正式编码证据，仍应按原PDF逐字复核排版。

## 题面转写

七、（45 分）在光纤中传播的光信号到达光纤的外表面时，会发生折射和反射。折射光导致能量损耗，降低光信号的信噪比。通过掺杂工艺可以改变光纤的折射率，使光线在光纤中螺旋前进，不到达光纤的外表面，避免折射造成的能量损失。现考虑一种由所谓自聚焦光纤构成的圆柱体，其对称轴为 `z` 轴，它的一段如图7a所示。在光纤中建立柱坐标系，光纤中质元的位置坐标为 `(rho, theta, z)`。光纤中任意一点的折射率 `n` 随该点到 `z` 轴的距离 `rho` 的增加而递减，即

```text
n = n_0 sqrt(1 - alpha^2 rho^2)
```

这里，`alpha` 和 `n_0` 均为大于零的常量，且 `alpha rho` 足够小。光纤内的光线是三维空间曲线，记曲线的参数方程为

```text
rho = rho(z),    theta = theta(z)
```

已知光纤的横截面半径足够大，光线轨迹始终不能到达光纤柱体的侧面。

（1）导出 `rho(z)` 和 `theta(z)` 满足的微分方程。

（2）如果在光纤内部 `z = 0` 处，光线满足边界条件

```text
rho(0) = rho_0,    rho'(0) = k_1 > 0;
theta(0) = 0,      theta'(0) = k_2 > 0
```

其中字母右上角的撇号表示对 `z` 求导。求光线在此后的传播中，离轴线的最远距离 `rho_max`。

（3）在第（2）问的边界条件下，求解光线在直角坐标系中的轨迹 `x(z), y(z)`。

## 图件核对提示

- 题图为图7a，位于试题PDF第5页第7题题干右侧，显示圆柱形自聚焦光纤、螺旋光线路径和 `z` 轴方向。
- 本任务只处理 `CPHO42-Q07-OCR` 与 `CPHO42-Q07-FORMULA`；`CPHO42-Q07-FIG` 仍保留为后续图件裁边与图注校对项，不在本轮关闭。
- 原题面图件可作为表征形式和案例证据候选，但正式论文用图前仍需重新核对图号、箭头、轴标和裁边。

## 待复核点

1. 原OCR将“掺杂工艺”误识别为“失杂工艺”，将对称轴 `z`、柱坐标 `rho, theta, z` 和参数方程严重误识别。
2. 原OCR漏掉折射率公式中的根号结构，并误读 `alpha^2 rho^2`；正式编码证据必须按题面公式 `n = n_0 sqrt(1 - alpha^2 rho^2)` 复核。
3. 原OCR将边界条件中的 `rho_0`、`k_1`、`k_2`、撇号和 `rho_max` 误识别，后续案例分析不得直接引用原OCR。
4. 答案PDF第21-25页公式密集，尤其式⑬、⑯、㉑、㉒、㉗、㊲、㊳、㊴和㊵涉及根号、平方、分母和正负号，正式引用前必须逐式排版复核。
5. 答案第24-25页包含解法二（费马原理、莫培督原理）和评分标准；解法二可作为替代推导证据，不应与主解法混写成新的题面条件。
