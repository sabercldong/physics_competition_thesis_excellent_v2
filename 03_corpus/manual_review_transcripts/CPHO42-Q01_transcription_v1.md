# CPHO42-Q01 题面校对转写稿 V1

任务：`G1-07-A1-TRANSCRIBE-42Q01`

更新时间：2026-07-15

## 来源与边界

- 试题PDF：`03_corpus/raw_papers/cpho_42_2025_fusai_paper_candidate.pdf`
- 题面页码：1（经视觉检查，第1题完整位于试题PDF第1页上半部；第1页下半部进入第2题，仅用于边界确认）
- 页面证据：
  - `03_corpus/manual_review_renders/G1-07-A1/CPHO42-Q01-paper-page-1.png`
- 答案PDF：`03_corpus/raw_solutions/cpho_42_2025_fusai_solution_candidate.pdf`
- 答案页码：1-4（经视觉检查，第1题答案从答案PDF第1页开始，延续至第4页中部评分标准结束；第4页下半部进入第2题，仅用于边界确认）
- 答案页面证据：
  - `03_corpus/manual_review_renders/G1-07-A1/CPHO42-Q01-solution-page-01.png`
  - `03_corpus/manual_review_renders/G1-07-A1/CPHO42-Q01-solution-page-02.png`
  - `03_corpus/manual_review_renders/G1-07-A1/CPHO42-Q01-solution-page-03.png`
  - `03_corpus/manual_review_renders/G1-07-A1/CPHO42-Q01-solution-page-04.png`
- 公式核对表：`03_corpus/manual_review_transcripts/CPHO42-Q01_formula_check_v1.csv`

本稿为基于PDF渲染页的题面视觉转写稿，用于替代原OCR乱码作为后续人工校对和正式编码前复核入口。变量、上下标、希腊字母和公式已按可见题面尽量转写；若后续制作论文附录或正式编码证据，仍应按原PDF逐字复核排版。

## 题面转写

一、（45 分）一磁光陷阱中约束的 `N` 个原子构成的原子气处于绝对温度为 `T` 的平衡态。在位置 `r = (x, y, z)`、速度为 `v = (v_x, v_y, v_z)` 的原子数密度 `f(r, v)` 服从玻尔兹曼分布

```text
f(r, v) ∝ exp[-m(omega_x^2 x^2 + omega_y^2 y^2 + omega_z^2 z^2)/(2 k_B T)]
          exp[-m(v_x^2 + v_y^2 + v_z^2)/(2 k_B T)]
```

其中 `omega_i` 为 `i (i = x, y, z)` 方向上陷阱对原子气的约束强度，`m` 为原子质量，`k_B` 为玻尔兹曼常量，`T` 为绝对温度。取竖直向下为 `z` 轴正方向。在陷阱正下方 `z = h (h > 0)` 处有一探测器，可测量 `z = h` 平面附近的原子的纵向数密度（即此平面附近 `z` 方向单位高度内的原子数）和通过该平面的原子流（即单位时间由上至下通过该平面的净原子数）。重力加速度大小为 `g`，忽略原子间的碰撞。在 `t = 0` 时将陷阱撤除。

（1）求陷阱撤除前，平衡态下完整的分布函数 `f(r, v)`；

（2）求某 `t > 0` 时刻，在 `z = h` 平面附近的原子的纵向数密度 `n(t)`，以及通过该平面的原子流 `I(t)`；

（3）在原子气温度极低、约束很强的条件下，可通过测量 `n(t)` 的最大值所对应的时间 `t_n` 或者 `I(t)` 的最大值所对应的时间 `t_I` 求得温度 `T`。在温度极低、约束很强的极限下，求 `t_n` 和 `t_I` 的表达式（准确到温度的非零的最低阶）。

（4）在原子气温度极低、约束很强的极限下，在 `t = t_n` 附近，

```text
n(t) ≈ n_0 exp[-(t - t_n)^2/(2 sigma_t^2)]
```

其中 `n_0` 为与 `t` 无关的量，`sigma_t` 是上述（高斯）分布函数的有效展宽。实验上若测得此有效展宽，可用来估计温度 `T`。求 `sigma_t` 的表达式（准确到温度的非零的最低阶）。

提示：

```text
int_0^infty exp(-x^2) dx = sqrt(pi)/2,
int_0^infty x^2 exp(-x^2) dx = sqrt(pi)/4.
```

## 图件核对提示

- 第42届第1题题面无独立题图。
- 试题PDF第1页下半部包含第2题题面和图2a、图2b，均不得纳入第1题证据。

## 待复核点

1. 原OCR将 `T`、`v_x/v_y/v_z`、`omega_i`、`k_B`、`n(t)`、`I(t)`、`t_n`、`t_I`、`sigma_t` 等关键符号严重误识别，正式编码证据应以本稿和源页图复核。
2. 题面中 `z = h` 平面附近的“纵向数密度”和“原子流”定义是第(2)问建模证据，正式编码时需保留其测量含义。
3. 第(3)问和第(4)问都限定“温度极低、约束很强的极限”，且结果要求准确到温度的非零最低阶；不能把内部OCR中的缺字或错字作为正式条件。
4. 答案第4页中部为第1题评分标准，之后进入第2题答案；第2题内容不得纳入第1题公式核对。
