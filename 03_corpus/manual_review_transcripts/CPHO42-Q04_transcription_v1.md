# CPHO42-Q04 题面校对转写稿 V1

任务：`G1-07-A1-TRANSCRIBE-42Q04`

更新时间：2026-07-15

## 来源与边界

- 试题PDF：`03_corpus/raw_papers/cpho_42_2025_fusai_paper_candidate.pdf`
- 题面页码：3（经视觉检查，第4题从试题PDF第3页中部“四、（50分）”开始，第3页下半部结束；第3页上半部为第3题尾部，第3页底部进入第5题，仅用于边界确认）
- 页面证据：
  - `03_corpus/manual_review_renders/G1-07-A1/CPHO42-Q04-paper-page-3.png`
- 答案PDF：`03_corpus/raw_solutions/cpho_42_2025_fusai_solution_candidate.pdf`
- 答案页码：10-14（经视觉检查，第4题答案从答案PDF第10页中部“四、（50分）”开始，延续至第14页上半部评分标准结束；第10页上半部为第3题尾部和评分标准，第14页中下部进入第5题答案，仅用于边界确认）
- 答案页面证据：
  - `03_corpus/manual_review_renders/G1-07-A1/CPHO42-Q04-solution-page-10.png`
  - `03_corpus/manual_review_renders/G1-07-A1/CPHO42-Q04-solution-page-11.png`
  - `03_corpus/manual_review_renders/G1-07-A1/CPHO42-Q04-solution-page-12.png`
  - `03_corpus/manual_review_renders/G1-07-A1/CPHO42-Q04-solution-page-13.png`
  - `03_corpus/manual_review_renders/G1-07-A1/CPHO42-Q04-solution-page-14.png`
- 公式核对表：`03_corpus/manual_review_transcripts/CPHO42-Q04_formula_check_v1.csv`

本稿为基于PDF渲染页的题面视觉转写稿，用于替代原OCR乱码作为后续人工校对和正式编码前复核入口。变量、上下标、希腊字母和公式已按可见题面尽量转写；若后续制作论文附录或正式编码证据，仍应按原PDF逐字复核排版。

## 题面转写

四、（50 分）真空激光加速机制即是利用强激光脉冲加速电子使其获得能量增益。实际激光束的电磁场十分复杂，现采用单色平面电磁波与电子相互作用的简化模型。入射强激光可视为沿 `z` 轴传播的线偏振单色平面电磁波，入射波的电场和磁场可表示为

```text
E = E_0 cos(kz - omega t) e_x,
B = (E_0/c) cos(kz - omega t) e_y,
```

其中 `E_0` 为电场强度的振幅，`c` 为真空中的光速，`k` 为波矢的大小，`omega` 为圆频率，`e_x` 和 `e_y` 表示 `x` 轴和 `y` 轴的基矢。不计重力，应用相对论动力学讨论以下问题：

（1）假设 `t = 0` 时电子静止且位于坐标原点处，忽略辐射阻尼，求

（1.1）`t` 时刻电子的动量 `p` 和能量 `epsilon`（表达式中可含有 `t` 时刻的 `z` 坐标）；

（1.2）电子的位置坐标 `x, y, z` 与时间 `t` 的代数关系，可用隐函数形式表达。

（2）假设 `t = 0` 时刻将能量为 `epsilon_0` 的电子从坐标原点沿 `x-z` 平面注入，且其初速度方向与 `x` 轴正方向的夹角不大于 `pi/2`，忽略辐射阻尼，求电子加速达到的最大能量 `epsilon_max` 及相应的入射角 `theta_0`，这里 `theta_0` 是电子入射方向与 `z` 轴的夹角。

（3）当激光脉冲强度很大时，辐射阻尼将无法忽略。辐射阻尼导致的能量损失满足

```text
d epsilon / dt = - e^4 mu_0 E_0^2 epsilon^2 / (4 pi m_e^4 c^5)
```

其中 `mu_0` 为真空磁导率。已知激光脉冲强度 `I = 1.0 x 10^22 W/cm^2`，激光波长 `lambda = 800 nm`，初始时刻电子能量

```text
epsilon_0 = 1000 m_e c^2
```

求经过一个周期 `T` 由辐射阻尼引起的相对能量损失 `Delta epsilon / epsilon_0`。已知 `m_e = 9.101 x 10^-31 kg`，`e = 1.602 x 10^-19 C`，`c = 2.998 x 10^8 m/s`，`mu_0 = 4 pi x 10^-7 N/A^2`，激光强度 `I` 是能流密度

```text
S = (1/mu_0) E x B
```

大小的时间平均值。

## 图件核对提示

- 第42届第4题题面无独立题图。
- 试题PDF第3页上半部包含第3题图3c、图3d和第3题末尾小问，不得纳入第4题证据。
- 试题PDF第3页底部进入第5题并出现图5a，不得纳入第4题证据。

## 待复核点

1. 原OCR将 `E_0`、`omega`、`e_x/e_y`、`epsilon_0`、`epsilon_max`、`theta_0`、`Delta epsilon / epsilon_0`、`mu_0`、`lambda`、能流密度 `S` 等关键符号严重误识别，正式编码证据应以本稿和源页图复核。
2. 第（1）问中的相对论动量、能量、位置隐函数和 `z` 坐标依赖，是后续案例编码的重要证据，需对照答案页逐式核对。
3. 第（2）问长分式和根号表达式集中在答案第12-13页，正式引用前必须逐项复核括号层级、上下标和最大值条件。
4. 第（3）问中的辐射阻尼损失率、激光强度单位、周期代入和最终 `-40%` 结果应作为重点公式复核项；不能直接继承原OCR中的数量级和单位误识别。
