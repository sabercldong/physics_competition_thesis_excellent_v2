# 第39届复赛第3题：斜面上实心球的反复弹性碰撞

## 题干整理

半径 $R$、质量 $m$ 的匀质实心球以垂直斜面的初速度 $V$ 发射。取 $x$ 轴沿坡向下、$y$ 轴垂直斜面向上；碰撞弹性且接触点不滑动，转动惯量 $I=2mR^2/5$。

![斜面坐标与碰撞辅助图](assets/CPHO39-Q03-figures.png)

求首次碰撞前后状态、第 $n$ 次碰撞后的平动和转动，以及前 $n$ 次碰撞的总冲量。

## 解析整理

飞行时间 $T=2V/(g\cos\theta)$，故每段飞行增加的沿坡速度为

$$
w=2V\tan\theta.
$$

碰撞映射为

$$
v_f=\frac37v_i+\frac47R\omega_i,\qquad
R\omega_f=\frac{10}{7}v_i-\frac37R\omega_i.
$$

首次碰撞后：

$$
v_1=\frac67V\tan\theta,\qquad
\omega_1=\frac{20}{7R}V\tan\theta.
$$

第 $n$ 次碰撞后：

$$
\begin{aligned}
n\text{ 为偶数}:&\quad v_n=\frac{10}{7}nV\tan\theta,\quad \omega_n=\frac{10}{7R}nV\tan\theta;\\
n\text{ 为奇数}:&\quad v_n=\frac27(5n-2)V\tan\theta,\quad \omega_n=\frac{10}{7R}(n+1)V\tan\theta.
\end{aligned}
$$

总冲量为

$$
\mathbf J=m(v_n-nw)\hat{x}+2nmV\hat{y}.
$$

## 图件与依据

题干依据 `CPHO39-Q03.md` 第2页；公式依据 `CPHO39-Q03_formula_check_v1.csv` 与答案第9至12页。左图重绘原题图3a；答案没有独立图示，右图为解析辅助图。
