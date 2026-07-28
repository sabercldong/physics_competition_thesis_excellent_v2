# 第38届复赛第7题：汽车斜坡加速与车轮附着条件

## 题干整理

汽车在倾角为 $\theta$ 的斜坡上加速。前、后轮各合并为质量 $m$、半径 $r$ 的均质圆柱，轮轴间距为 $L$；车身质量为 $M$，质心在两轴中点正上方，高度为 $h$。车轮转动惯量为

$$
J=\frac12mr^2.
$$

发动机向后轮施加顺时针力矩 $\tau_{\text{轮}}$。给定 A 型电动汽车的 $M,h,r,L,\tau,r_i$ 等参数，求正压力、安全加速度、车身加速度以及无滑动所需的摩擦系数。

![汽车斜坡模型与受力](assets/CPHO38-Q07-figure7a.png)

## 解析整理

### 1. 正压力和前轮离地边界

取沿坡面向上为 $x$ 正方向。由车身受力和相对质心的力矩平衡，

$$
N_{\text{前}}=mg\cos\theta+\frac12Mg\cos\theta
-\frac hL M(a+g\sin\theta),
$$

$$
N_{\text{后}}=mg\cos\theta+\frac12Mg\cos\theta
+\frac hL M(a+g\sin\theta).
$$

令 $N_{\text{前}}=0$，得到前轮不离地的安全上限：

$$
\boxed{a_{\text{安全}}=
\frac{(2m+M)L}{2Mh}g\cos\theta-g\sin\theta}.
$$

### 2. 后轮驱动时的加速度

无滑动约束与前轮转动方程给出

$$
\alpha_{\text{前}}=\alpha_{\text{后}}=-\frac ar,
\qquad F_{x,\text{前}}=-\frac m2a.
$$

再联立整车的沿坡面运动方程和后轮转动方程，

$$
\boxed{a=\frac{\tau_{\text{轮}}/r-(M+2m)g\sin\theta}{M+3m}}.
$$

### 3. A 型车数值与附着条件

变速器效率为 $100\%$，因此

$$
\tau_{\text{轮}}=\tau r_i.
$$

忽略车轮质量后，题解给出

$$
\boxed{a(0^\circ)=5.6\,\mathrm{m/s^2},\qquad
a(30^\circ)=0.66\,\mathrm{m/s^2}}.
$$

无滑动需要 $|F_{x,\text{前}}|\le\mu N_{\text{前}}$、$|F_{x,\text{后}}|\le\mu N_{\text{后}}$。两种路况对应

$$
\boxed{\mu_{\min}(0^\circ)=1.09,\qquad
\mu_{\min}(30^\circ)=1.25}.
$$

## 图件与依据

题干依据 `CPHO38-Q07_transcription_v1.md`；公式依据 `CPHO38-Q07_formula_check_v1.csv` 与答案第16至18页。左图重绘原题图7a，右图为沿坡面动力学辅助示意。
