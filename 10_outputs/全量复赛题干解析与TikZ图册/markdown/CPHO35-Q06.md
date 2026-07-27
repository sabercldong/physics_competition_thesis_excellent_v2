# 第35届复赛第6题：同心球壳辐射与导热

## 题干整理

同心内球和球壳之间为真空。已知内球半径 $r=0.200\,\mathrm m$、比辐射率 $e=0.800$；球壳内外半径为 $R_1=0.900\,\mathrm m$、$R_2=1.00\,\mathrm m$，导热系数为 $\kappa=1.00\times10^{-2}\,\mathrm{J\,m^{-1}\,s^{-1}\,K^{-1}}$，内表面比辐射率 $E=0.800$，外表面为黑体。热稳定时穿过球壳的热量 $Q=44.0\,\mathrm W$。求 $T_2$、$T_1$ 和 $T_0$。

## 解析整理

### 1. 外表面辐射

$$
Q=4\pi R_2^2\sigma(T_2^4-T^4),
\qquad
T_2=\left(\frac{Q}{4\pi R_2^2\sigma}+T^4\right)^{1/4}
=88.6\,\mathrm K.
$$

### 2. 球壳导热

$$
Q=-4\pi R^2\kappa\frac{\mathrm dT}{\mathrm dR}.
$$

从 $R_1$ 到 $R_2$ 积分，

$$
Q=4\pi\kappa\frac{R_1R_2}{R_2-R_1}(T_1-T_2),
$$

故

$$
T_1=T_2+\frac{(R_2-R_1)Q}{4\pi\kappa R_1R_2}
=128\,\mathrm K.
$$

### 3. 内球与球壳内表面的辐射交换

重复反射中由球壳内表面重新到达内球的几何份额为

$$
k=\left(\frac{r}{R_1}\right)^2.
$$

求和后净辐射功率为

$$
Q''=\frac{4\pi Ee\sigma r^2(T_0^4-T_1^4)}
{1-(1-e)k(1-E)}.
$$

令 $Q''=Q$，得到

$$
T_0=
\left\{
\frac{\left[1-(1-e)(1-E)\dfrac{r^2}{R_1^2}\right]Q}
{4\pi Ee\sigma r^2}
+T_1^4
\right\}^{1/4}
=227\,\mathrm K.
$$

## 图件与依据

题图采用 TikZ 重绘同心内球与球壳及三条半径标注。题干、公式与图件依据 CPHO35-Q06.md、CPHO35-Q06_formula_check_v1.csv 和题图核对入口；当前 PDF 未明示分值。
