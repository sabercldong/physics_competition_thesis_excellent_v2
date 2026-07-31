# CPHO42-Q05 题面校对转写稿 V1

任务：`G1-07-A1-TRANSCRIBE-42Q05`

更新时间：2026-07-15

## 来源与边界

- 试题PDF：`03_corpus/raw_papers/cpho_42_2025_fusai_paper_candidate.pdf`
- 题面页码：3-4（经视觉检查，第5题从试题PDF第3页底部开始，延续至第4页中下部；第4页下部已进入第6题，仅用于边界确认）
- 页面证据：
  - `03_corpus/manual_review_renders/G1-07-A1/CPHO42-Q05-paper-page-3.png`
  - `03_corpus/manual_review_renders/G1-07-A1/CPHO42-Q05-paper-page-4.png`
- 答案PDF：`03_corpus/raw_solutions/cpho_42_2025_fusai_solution_candidate.pdf`
- 答案页码：14-16（经视觉检查，第5题答案从答案PDF第14页中部开始，至第16页评分标准结束；第16页下方已进入第6题，仅用于边界确认）
- 答案页面证据：
  - `03_corpus/manual_review_renders/G1-07-A1/CPHO42-Q05-solution-page-14.png`
  - `03_corpus/manual_review_renders/G1-07-A1/CPHO42-Q05-solution-page-15.png`
  - `03_corpus/manual_review_renders/G1-07-A1/CPHO42-Q05-solution-page-16.png`
- 公式核对表：`03_corpus/manual_review_transcripts/CPHO42-Q05_formula_check_v1.csv`

本稿为基于PDF渲染页的题面视觉转写稿，用于替代原OCR乱码作为后续人工校对和正式编码前复核入口。变量、上下标、希腊字母和图号已按可见题面尽量转写；若后续制作论文附录或正式编码证据，仍应按原PDF逐字复核排版。

## 题面转写

五、（45 分）低温下的约瑟夫森结可作为超导量子计算电路的基本单元。如图 5a，理想的约瑟夫森结可视为“超导体-薄绝缘层（灰色区域）-超导体”组成的三明治结构，直角坐标系原点 O 位于其中心（z 轴正方向垂直于纸面向外，未画出），其在 y-z 平面内矩形截面的边长分别为 Y 和 Z，绝缘层厚度为 d（d << Y、Z）。超导体 1、2 中电子的状态可以分别用波函数 psi_1 ∝ e^(i phi_1)、psi_2 ∝ e^(i phi_2) 来描述，它们的相位差 delta = phi_2 - phi_1。由于绝缘层很薄，超导电子可以隧穿形成沿 x 方向的约瑟夫森电流，电流密度记为 j，结两端的电压记为 U，相位差 delta 满足约瑟夫森方程：

```text
j = j0 sin delta,
partial delta / partial t = (2e / hbar) U
```

其中 j0 > 0 为常量，hbar 是约化普朗克常量，e（e > 0）是元电荷的电荷量，partial delta / partial t 为在 delta 依赖的所有自变量中，除 t 之外的其他自变量均不变时对 t 求导。以上两式表明，即使约瑟夫森结两端电压 U = 0，也可以存在直流约瑟夫森电流。以上两式在外磁场为零和不为零两种情况下都成立，当外磁场为零时，相位差 delta 与空间坐标无关。

（1）当约瑟夫森结两端的电压 U 为直流恒定电压 U0 时，试求此时电流密度 j(t) 的表达式（t = 0 时的相位差记为 delta(0)），以及该电流变化的周期 T。

（2）当约瑟夫森结两端电压 U = 0 时，沿 z 方向施加一恒定均匀外磁场。由于超导体对外磁场的屏蔽作用，总磁场只能存在于绝缘层及两侧等效厚度为 lambda 的超导体内，即图 5a 中两虚线之间的区域。已知绝缘层内总磁感应强度 B 只有 z 分量且只与 y 坐标有关，即 B = B_z(y)e_z，其中 e_z 是 z 方向的单位矢量。相位差 delta 在外磁场不为零时随 y 坐标的变化满足

```text
partial delta / partial y = [2e(d + 2lambda) / hbar] B_z(y)
```

（2.1）忽略约瑟夫森电流产生的磁场，B_z(y) 为常量 B0，试求 delta(y)（y = 0 处的相位差记为 delta_0，delta_0 != k pi，k 为整数），以及总的约瑟夫森电流 I_J 与外磁场 B0 的关系；试问当 B0 为何值时，总电流 I_J = 0？

（2.2）考虑约瑟夫森电流产生的磁场，试证明此时 delta(y) 满足形如

```text
d^2 delta / dy^2 = (1 / lambda_J^2) sin delta
```

的方程，并确定 lambda_J 的表达式（lambda_J 称为约瑟夫森穿透深度）。已知绝缘层材料的磁导率为 mu_0。

（3）在外磁场为零（相位差 delta 与空间坐标无关）的情况下，采用宏观电路模型研究外加一定直流偏置电流 I 的约瑟夫森结相位差 delta 随时间 t 的变化。约瑟夫森结具有等效电容 C（即三明治结构形成的平行板电容器的电容）。在一般工作状态下，约瑟夫森结还有与约瑟夫森电流并存的直流电流，需要考虑约瑟夫森结存在的直流电阻 R。因此，实际的约瑟夫森结可以等效为满足约瑟夫森方程的理想结 J 与电阻 R、电容 C 的并联，如图 5b 所示。为简化起见，记 I0 = j0YZ。

（3.1）求以上三个支路电流的表达式（用相位差 delta(t) 及其时间导数表示），并导出 delta(t) 所满足的微分方程。

以下讨论中直流电阻 R 足够大，可忽略电阻支路中的电流。

（3.2）第（3.1）问中的微分方程描述的运动可视为“位移”为 delta、单位“质量”的等效“粒子”在势 V(delta) 中的运动。求势 V(delta) 的表达式；当电流 I 处于什么范围时，势 V(delta) 存在势阱？求势阱底部对应的 delta 值，并求“粒子”在势阱底部做小幅振动的角频率 omega。

（3.3）改变偏置电流 I，第（3.2）问中的角频率 omega 将随之改变，角频率的最大值称为约瑟夫森等离子体角频率 omega_J。已知电磁波在结区中传播的波速 c_bar = omega_J lambda_J，绝缘层材料的相对介电常量 epsilon_r = 9.0，d = 3.0 nm，lambda = 53 nm，求 c_bar 与真空中光速 c 的比值（结果保留两位有效数字）。

## 图件核对提示

- 图 5a：约瑟夫森结结构示意图，标出超导体1、薄绝缘层、超导体2、电流方向、x/y轴、lambda、O 点和虚线边界。
- 图 5b：约瑟夫森结宏观等效电路，标出理想结 J、电阻 R、电容 C 和外加电流 I。
- 现有题图文件：`03_corpus/item_assets/CPHO42-Q05-figure1-page3-raw.png`; `03_corpus/item_assets/CPHO42-Q05-figure2-page4-raw.png`。
- 本轮只确认题面页中图 5a 和图 5b 的基本元素可见；`CPHO42-Q05-FIG` 仍为独立图件校对项，尚未销项。

## 待复核点

1. 本稿使用 `psi`、`phi`、`delta`、`lambda`、`hbar`、`mu_0`、`epsilon_r`、`omega`、`omega_J` 和 `c_bar` 等ASCII近似记录；正式附录或论文正文需统一转为项目采用的公式排版格式。
2. `partial delta / partial t`、`partial delta / partial y`、`B_z(y)`、`I_J`、`I0 = j0YZ`、`lambda_J` 和 `c_bar = omega_J lambda_J` 等关键式需在最终排版时逐项核对上下标、偏导符号和根号。
3. 第4页下部已进入第6题，本轮保留其渲染图作为边界确认，不得把第6题内容混入第5题题面或公式证据。
4. 答案PDF第16页下方已进入第6题，本轮保留该页作为第5题评分标准和边界确认，不得把第6题内容纳入第5题公式证据。
5. 本稿未关闭 `CPHO42-Q05-FIG`，题图裁边、图注与论文用重裁或重绘仍需单独销项。
