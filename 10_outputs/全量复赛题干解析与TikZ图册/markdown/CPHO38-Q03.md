# 第38届复赛第3题：超球与平行硬板的连续弹性碰撞

## 题干整理

半径为 $r$、质量为 $m$ 的均质超球在上下两个固定硬板之间连续碰撞3次。初始水平速度为 $v_{0x}$、绕 $z$ 轴角速度为 $\omega_{0z}$，且

$$
J_z=\frac25mr^2,\qquad \omega_{0z}<\frac{v_{0x}}r.
$$

![超球与平行硬板的连续碰撞](assets/CPHO38-Q03-figure3a.png)

## 解析整理

### 1. 第1次碰撞

接触点无滑动使接触点水平速度反向：

$$
v_{1x}-r\omega_{1z}=-(v_{0x}-r\omega_{0z}).
$$

由水平动量、角动量和 $J_z=2mr^2/5$，

$$
v_{1x}=\frac37v_{0x}+\frac47r\omega_{0z},
\qquad
\omega_{1z}=\frac{10}{7}\frac{v_{0x}}r-\frac37\omega_{0z}.
$$

### 2. 第2次碰撞

上板碰撞时摩擦力矩反号：

$$
v_{2x}=-\frac{31}{49}v_{0x}+\frac{24}{49}r\omega_{0z},
\qquad
\omega_{2z}=-\frac{60}{49}\frac{v_{0x}}r-\frac{31}{49}\omega_{0z}.
$$

### 3. 第3次碰撞

回到下板碰撞后，

$$
v_{3x}=-\frac{333}{343}v_{0x}-\frac{52}{343}r\omega_{0z},
\qquad
\omega_{3z}=-\frac{130}{343}\frac{v_{0x}}r+\frac{333}{343}\omega_{0z}.
$$

## 图件与依据

题干依据 CPHO38-Q03_transcription_v1.md；公式依据 CPHO38-Q03_formula_check_v1.csv 与答案第8至10页。题图为根据图3a自绘的TikZ图。
