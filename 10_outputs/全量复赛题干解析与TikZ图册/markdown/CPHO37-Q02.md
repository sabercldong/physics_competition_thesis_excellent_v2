# 第37届复赛第2题：台球母球击打后的滑动与滚动

## 题干整理

均质实心母球质量为 $m$、半径为 $R$，球杆在球心上方 $R/2$ 处施加水平冲量 $P$。球与桌面滑动摩擦因数为 $\mu$。求母球开始纯滚动的时间，以及纯滚动后初始接触点 $B$ 的位置、速度和加速度。

## 解析整理

### 1. 击打后初始状态

$$
u_0=\frac Pm,
\qquad
I=\frac25mR^2,
\qquad
\omega_0=\frac{5P}{4mR}.
$$

初始接触点速度为

$$
v_A=u_0-R\omega_0=-\frac P{4m}<0.
$$

因此摩擦力沿冲量方向。

### 2. 纯滚动开始时刻

$$
u(t)=u_0+\mu gt,
\qquad
\omega(t)=\omega_0-\frac{\mu mgR}{I}t,
$$

$$
v_A(t)=\frac72\mu gt-\frac P{4m}.
$$

令 $v_A=0$，

$$
t_0=\frac{P}{14\mu mg},
\qquad
u_c=\frac{15P}{14m}.
$$

### 3. 纯滚动后接触点 B 的运动

令

$$
\theta=\frac{u_ct'}R=\frac{15Pt'}{14mR}.
$$

$$
x_B=u_ct'-R\sin\theta,
\qquad
y_B=R(1-\cos\theta).
$$

$$
v_{Bx}=u_c(1-\cos\theta),
\qquad v_{By}=u_c\sin\theta,
$$

$$
v_B=\frac{15P}{7m}\sin\frac{15Pt'}{28mR}.
$$

$$
a_B=\frac{u_c^2}{R}=\left(\frac{15}{14}\right)^2\frac{P^2}{m^2R},
$$

方向指向球心。

## 图件与依据

原题无题图，不补画非原题图形。题干与公式依据 `CPHO37-Q02.md` 和 `CPHO37-Q02_formula_check_v1.csv`。
