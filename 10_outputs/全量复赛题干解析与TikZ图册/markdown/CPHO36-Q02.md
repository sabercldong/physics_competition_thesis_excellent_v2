# 第36届复赛第2题：农用平板车碰撞与摩擦运动

## 题干整理

两车轮半径为 $r$、质量为 $m$；平板长为 $l$、质量为 $2m$；两把手长为 $2l$、质量各为 $m$。先释放被卡住的平板车把手，随后在把手碰地时撤去卡轮装置并研究碰撞、滑动和纯滚动过程中的车轴位移。

## 解析整理

### 1. 落地前角速度

$$
J=\frac43ml^2,\qquad r_C=\frac l4,\qquad h=\frac r6.
$$

由机械能守恒，

$$
\frac12J\omega^2=4mgh,
\qquad
\omega=\sqrt{\frac{gr}{l}}.
$$

### 2. 起动阈值

$$
\sin\theta=\frac{2r}{3l},\qquad
\cos\theta=\frac{\sqrt{9l^2-4r^2}}{3l}.
$$

碰后初速度为

$$
v_0=\frac{\sqrt{gr}}6(\sin\theta-\mu\cos\theta).
$$

若

$$
\mu\ge\frac{2r}{\sqrt{9l^2-4r^2}},
$$

则系统不启动，$s=0$。

### 3. 又滑又滚阶段

$$
a_C=-\mu g,\qquad
\beta=\frac{8\mu g}{3r},
$$

$$
v_1=\frac4{33}\sqrt{gr}(\sin\theta-\mu\cos\theta),
$$

$$
s_1=\frac{57r}{78408\mu l^2}
\left(2r-\mu\sqrt{9l^2-4r^2}\right)^2.
$$

### 4. 纯滚动阶段

$$
a_{C2}=-\frac{\mu g}{11\mu\tan\theta+12},
$$

$$
s_2=\frac{16r}{9801\mu}
\left(2r-\mu\sqrt{9l^2-4r^2}\right)^2
\frac{11\mu r+6\sqrt{9l^2-4r^2}}{9l^2-4r^2}.
$$

当 $\mu<\tan\theta$ 时，车轴总位移为

$$
s=s_1+s_2.
$$

## 图件与依据

TikZ 图重绘车轮、平板、双把手、轴与尺寸标注。题干、公式和图件依据 CPHO36-Q02.md、CPHO36-Q02_formula_check_v1.csv 及题图核对入口。
