> 本文件由项目已校订的LaTeX题干、参考解答和TikZ图件生成。评分时以本文件为主要阅读文本；需核对原始措辞时查看包内对应届次原始PDF。

# 第37届复赛第2题：台球母球击打后的滑动与滚动

## 题干

质量为 $m$、半径为 $R$ 的均质实心母球静置在水平桌面上，球与桌面的滑动摩擦因数为 $\mu$。球杆保持水平，击打球心上方 $R/2$ 处，作用时间极短，给予大小为 $P$ 的水平冲量。取最大静摩擦力等于滑动摩擦力，重力加速度为 $g$。求：（1）击打后经过多久母球开始纯滚动；（2）以纯滚动开始时为零时刻，设球面上该时刻的接触点为 $B$，求此后 $t'$ 时刻 $B$ 点的位置、速度和加速度。

## 参考解答整理

#### （1）击打后的初始状态。

质心动量定理与相对质心的冲量矩定理给出 $$u_0=\frac Pm,
\qquad
P\frac R2=I\omega_0,
\qquad
I=\frac25mR^2.$$ 故 $$\omega_0=\frac{5P}{4mR}.$$ 击打后瞬间，原接触点 $A$ 的速度为 $$v_A=u_0-R\omega_0=-\frac P{4m}<0,$$ 表明该点向 $x$ 负方向滑动，摩擦力方向为 $x$ 正方向。

#### （2）滑动至纯滚动。

滑动阶段中 $$u(t)=u_0+\mu gt,
\qquad
\omega(t)=\omega_0-\frac{\mu mgR}{I}t.$$ 接触点速度可写为 $$v_A(t)=u(t)-R\omega(t)=\frac72\mu gt-\frac P{4m}.$$ 令 $v_A(t_0)=0$，得到开始纯滚动的时刻 $$\boxed{t_0=\frac{P}{14\mu mg}.}$$ 此时球心速度为 $$\boxed{u_c=u(t_0)=\frac{15P}{14m}.}$$

#### （3）纯滚动后 $B$ 点的运动。

令纯滚动开始后的时间为 $t'$，此时滚动圆心角为 $$\theta=\frac{u_ct'}R=\frac{15Pt'}{14mR}.$$ 以 $B$ 在 $t'=0$ 时的位置为原点，$x$ 轴与冲量 $P$ 同向，$y$ 轴竖直向上，则 $$\boxed{x_B=u_ct'-R\sin\theta
=\frac{15Pt'}{14m}-R\sin\frac{15Pt'}{14mR},}$$ $$\boxed{y_B=R(1-\cos\theta)
=R\left(1-\cos\frac{15Pt'}{14mR}\right).}$$ 速度分量、大小和方向角分别为 $$v_{Bx}=u_c(1-\cos\theta),\qquad v_{By}=u_c\sin\theta,$$ $$\boxed{v_B=2u_c\sin\frac{u_ct'}{2R}
=\frac{15P}{7m}\sin\frac{15Pt'}{28mR},}$$ $$\boxed{\alpha=\frac\pi2-\frac{u_ct'}{2R}
=\frac\pi2-\frac{15Pt'}{28mR}.}$$ 加速度分量为 $$a_{Bx}=\frac{u_c^2}{R}\sin\theta,
\qquad
a_{By}=\frac{u_c^2}{R}\cos\theta,$$ 所以 $$\boxed{a_B=\frac{u_c^2}{R}=\left(\frac{15}{14}\right)^2\frac{P^2}{m^2R},}$$ 方向指向球心 $C$。
