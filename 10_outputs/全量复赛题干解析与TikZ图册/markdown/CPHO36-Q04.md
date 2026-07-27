# 第36届复赛第4题：微孔竹板亥姆霍兹共振吸声

## 题干整理

微孔竹板的周期性长方形微孔与后方空气腔构成亥姆霍兹共振器。设微孔深度为 $l$、面积为 $S$、后腔体积为 $V_0$。声波绝热传播，满足 $v_s=\sqrt{\kappa/\rho}$、$\kappa=-V\Delta p/\Delta V$。给定标准状态空气参数，求空气密度和声速、共振吸收频率，以及吸收 $120\,\mathrm{Hz}$ 和 $200\,\mathrm{Hz}$ 时的孔面积比。

## 解析整理

### 1. 空气密度与声速

$$
pV=\frac{M}{M_{\rm mol}}RT,
\qquad
\rho=\frac{M_{\rm mol}p}{RT}.
$$

标准状态下

$$
\rho_0=1.29\,\mathrm{kg/m^3}.
$$

绝热过程给出

$$
\kappa=\gamma p,
\qquad
v_s=\sqrt{\frac{\gamma p}{\rho}},
$$

因此

$$
v_{s0}=331\,\mathrm{m/s}.
$$

### 2. 共振频率

微孔空气柱质量为 $m=\rho Sl$。取其向外位移为 $x$，

$$
\Delta V=Sx,
\qquad
F=-\frac{\gamma pS^2}{V}x.
$$

所以

$$
\omega=\sqrt{\frac{\gamma pS}{\rho lV}},
\qquad
f_0=\frac{v_s}{2\pi}\sqrt{\frac{S}{lV_0}}.
$$

### 3. 孔面积比

$$
\frac{S_1}{S_2}=\left(\frac{f_{01}}{f_{02}}\right)^2
=\left(\frac{120}{200}\right)^2=0.36.
$$

## 图件与依据

TikZ 图以规则孔阵列表现照片型原图的微孔结构，并重绘板--空气层截面、孔面积 $S$、孔深 $l$ 和后腔 $V_0$。题干、公式与图件依据 `CPHO36-Q04.md`、`CPHO36-Q04_formula_check_v1.csv` 和题图核对入口。
