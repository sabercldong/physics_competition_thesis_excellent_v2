# 第36届复赛第1题：旅行车三脚圆凳与茶水杯稳定性

## 题干整理

半径为 $R$ 的三脚圆凳的三脚端点构成边长为 $a$ 的等边三角形。半径为 $r$、质量为 $m$ 的茶杯位于凳面中心，杯高为 $H$，茶水密度为 $\rho$。求稳定且茶水尽可能多时的最佳高度；并求茶杯滑移到凳面边缘内切后，三只凳脚支持力相对初始状态的改变。

## 解析整理

### 1. 最佳茶水高度

茶杯和茶水整体的质心高度为

$$
y_{\mathrm{CM}}=
\frac{\dfrac{4m}{5}\dfrac H2+\rho\pi r^2h\dfrac h2}
{m+\rho\pi r^2h}.
$$

令 $\lambda=\rho\pi r^2$，令 $\mathrm dy_{\mathrm{CM}}/\mathrm dh=0$，得到

$$
h_{\max}=\frac{m}{\rho\pi r^2}
\left[\sqrt{1+\frac{4\pi\rho r^2H}{5m}}-1\right].
$$

### 2. 支持力改变

令

$$
Q=(m+\lambda h_{\max})g,\qquad P=Mg,\qquad R'=R-r.
$$

滑移后的平衡条件是

$$
N_A+N_B+N_C=Q+P,\qquad N_A=N_C,
$$

$$
Q R'+N_B\frac{a}{\sqrt3}-2N_A\frac{a}{2\sqrt3}=0.
$$

相对于初始的平均支持力 $(P+Q)/3$，

$$
\Delta N_B=-\frac{2\sqrt3}{3}\frac{R-r}{a}
\sqrt{1+\frac{4\pi\rho r^2H}{5m}}\,mg,
$$

$$
\Delta N_A=\Delta N_C=\frac{\sqrt3}{3}\frac{R-r}{a}
\sqrt{1+\frac{4\pi\rho r^2H}{5m}}\,mg.
$$

## 图件与依据

TikZ 图重绘茶杯居中和滑移至边缘内切两种状态下的凳面、支承三角形、凳脚与偏移关系。题干、公式和图件依据 CPHO36-Q01.md、CPHO36-Q01_formula_check_v1.csv 及题图核对入口。
