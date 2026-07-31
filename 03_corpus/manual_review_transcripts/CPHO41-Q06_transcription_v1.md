# CPHO41-Q06 题面校对转写稿 V1

任务：`G1-07-A1-TRANSCRIBE-41Q06`

更新时间：2026-07-15

## 来源与边界

- 试题PDF：`03_corpus/raw_papers/cpho_41_2024_fusai_paper_candidate.pdf`
- 答案PDF：`03_corpus/raw_solutions/cpho_41_2024_fusai_solution_candidate.pdf`
- 题面页码：3-4（经视觉检查，第6题从试题PDF第3页底部“六、（45分）”开始，延续至第4页中部“已知太阳的质量...”结束；第3页上部为第5题，第4页下半部进入第7题）
- 页面证据：
  - `03_corpus/manual_review_renders/G1-07-A1/CPHO41-Q06-paper-page-3.png`
  - `03_corpus/manual_review_renders/G1-07-A1/CPHO41-Q06-paper-page-4.png`
- 答案页码：13-16（经视觉检查，第6题答案从答案PDF第13页下部“六、（45分）”开始，至第16页评分标准结束；第16页下部进入第7题）
- 答案页面证据：
  - `03_corpus/manual_review_renders/G1-07-A1/CPHO41-Q06-solution-page-13.png`
  - `03_corpus/manual_review_renders/G1-07-A1/CPHO41-Q06-solution-page-14.png`
  - `03_corpus/manual_review_renders/G1-07-A1/CPHO41-Q06-solution-page-15.png`
  - `03_corpus/manual_review_renders/G1-07-A1/CPHO41-Q06-solution-page-16.png`
  - `03_corpus/manual_review_renders/G1-07-A1/CPHO41-Q06-solution-page-17.png`（第7题边界页，不纳入第6题答案）
- 公式核对表：`03_corpus/manual_review_transcripts/CPHO41-Q06_formula_check_v1.csv`

本稿为基于PDF渲染页的题面视觉转写稿，用于替代原OCR乱码作为后续人工校对和正式编码前复核入口。变量、上下标、希腊字母和图注已按可见题面尽量转写；若后续制作论文附录或正式编码证据，仍应按原PDF逐字复核排版。

## 题面转写

六、（45分）爱因斯坦的广义相对论预言星光会在太阳附近发生偏折。1919年，英国天文学家埃丁顿率领一支队伍，藉发生日全食的机会对这个现象进行了观测，验证了上述预言。下面对此进行分析。

（1）先在牛顿的动力学和万有引力理论的框架下考虑。若质量为 `m` 的质点在位于坐标原点 `O` 的质量 `M`（`M >> m`）的引力场中运动，其轨道是圆锥曲线。在平面极坐标系 `(r,theta)` 中，轨道方程为

```text
r(theta) = p/(1 + e cos theta)
```

其中 `-pi < theta <= pi`，`p (p > 0)` 称为半通径，`e (e >= 0)` 称为偏心率。若 `e > 1`，则存在 `theta_max`，使 `-theta_max < theta < theta_max`，试确定 `theta_max` 及其取值范围。

（2）第（1）问中的质点的轨道的参数 `p` 和 `e` 由质点的能量 `E`（含动能和相互作用势能）和相对于 `O` 点的轨道角动量的大小 `L` 决定。试导出 `p = p(E,L)` 和 `e = e(E,L)` 的函数关系。

（3）设一物体以速度 `v_0` 从外太空飞入太阳系，朝向太阳的瞄准距离是 `b`（即初速度 `v_0` 所在直线到太阳中心的距离），如图6a所示。设

```text
v_0^2 b/(G M_sun) >> 1
```

其中 `M_sun` 是太阳质量。当它飞离太阳系时，对下述两种情况，求其飞出方向相对于原飞入方向的偏转角 `Delta phi`：

（i）该入射物是一块陨石；

（ii）该入射物是一束星光，且该光束恰好掠过太阳表面而射入到我们的观测站，此时可近似认为瞄准距离 `b` 等于太阳半径 `R_sun`。

（4）广义相对论断言星光在引力场中会弯曲，在弱场近似下，这等效于存在引力场的空间有不恒为1的相对折射率

```text
n_eff(r) = 1 - 2 phi(r)/c^2
```

其中 `phi(r)` 是空间中的质量分布在 `r` 处的牛顿引力势。光线的轨迹可由费马原理

```text
delta ∫_A^B n_eff(r) dl = 0
```

决定，其中 `∫_A^B n_eff(r) dl` 是 `A` 到 `B` 的光程，变分符号 `delta` 表示总光程取极小值。设 `n_eff` 与 `theta` 无关，即 `n_eff = n_eff(r)`，若光线的轨迹方程为 `theta = theta(r)`，上述变分就导致方程

```text
d/dr [ r^2 theta' n_eff(r) / sqrt(1 + r^2 theta'^2) ] = 0
```

这里

```text
theta' = d theta/dr
```

利用此方程，试重新计算掠过太阳表面的星光的偏折角。

已知太阳的质量为 `M_sun`，太阳半径为 `R_sun`。引力常量为 `G`，真空中的光速为 `c`。

## 图件核对提示

- 图6a：星光或入射物从左侧以速度 `v_0` 入射，瞄准距离标为 `b`，轨迹在太阳附近弯曲，右侧标出偏转角 `Delta phi`。
- 现有题图文件：`03_corpus/item_assets/CPHO41-Q06-figure1-page4-raw.png`。
- 本轮只确认题面页中图6a的基本元素可见；`CPHO41-Q06-FIG` 仍为独立图件校对项，尚未销项。

## 待复核点

1. 原OCR将“爱因斯坦”“广义相对论”“埃丁顿”“日全食”“圆锥曲线”“半通径”“偏心率”“费马原理”“相对折射率”等关键文字严重误识别，正式编码证据不得继续使用原OCR文本。
2. 第(1)问轨道方程 `r(theta) = p/(1 + e cos theta)`、定义域 `-pi < theta <= pi`、`p > 0`、`e >= 0` 和 `e > 1` 条件需逐字核对。
3. 第(3)问条件 `v_0^2 b/(G M_sun) >> 1`、`b = R_sun` 的近似，以及偏折角 `Delta phi` 是第(3)问和第(4)问答案比较的关键。
4. 第(4)问中的 `n_eff(r) = 1 - 2 phi(r)/c^2`、费马原理积分和欧拉方程是公式OCR高风险区，需逐式排版复核。
5. 第6题题面从试题PDF第3页底部开始，延续至第4页中部；第4页下半部进入第7题，不得纳入第6题题面证据。
6. 第6题答案从答案PDF第13页下部开始，至第16页评分标准结束；第16页下部和第17页进入第7题，不得纳入第6题答案公式证据。
7. 本题答案中的 `theta_max`、`p/e` 与 `E/L` 关系、牛顿偏折角 `2GM_sun/(v_0^2 b)`、牛顿光线偏折角 `2GM_sun/(c^2 R_sun)` 和广义相对论弱场偏折角 `4GM_sun/(c^2 R_sun)`，均需逐式复核上下标、平方项、根号和近似符号。
