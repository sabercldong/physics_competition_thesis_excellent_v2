> 本文件由项目已校订的LaTeX题干、参考解答和TikZ图件生成。评分时以本文件为主要阅读文本；需核对原始措辞时查看包内对应届次原始PDF。

# 第40届复赛第2题：半圆管中活塞的稳定性与临界温度

## 题干

如图，将一根粗细均匀、两端封闭的细玻璃管弯成半径为 $r$ 的半圆环，竖直固定在水平地面上；玻璃管横截面半径远小于 $r$。管中有质量为 $m$ 的薄金属活塞，活塞与管壁密接而摩擦可忽略。活塞相对竖直方向的角位置记为 $\theta$。活塞两侧各有 $n$ 摩尔理想气体，气体温度始终等于外界绝对温度 $T$，所有状态变化均为准静态过程。已知重力加速度为 $g$、普适气体常量为 $R$。

![CPHO40-Q02-figure1](assets/CPHO40-Q02-figure1.png)

1. 当 $T$ 高于临界温度 $T_c$ 时，玻璃管正中央 $\theta=0$ 是活塞的稳定平衡位置。求 $T_c$，并求此处小振动的圆频率。

2. 当 $T=T_c$ 时，判断 $\theta=0$ 处平衡的稳定性。

3. 当 $T<T_c$ 时，求稳定平衡位置 $\theta_0$ 所满足的方程，并给出 $T$ 略低于 $T_c$ 时 $\theta_0$ 的最低阶近似。

4. 当 $T<T_c$ 时，求稳定平衡位置附近圆频率 $\omega_0(\theta_0)$；再给出 $T$ 略高于和略低于 $T_c$ 时圆频率随温度的关系。

5. 当 $T<T_c$ 时，若活塞初速度近似为零，求其由正中央到达角位置 $\theta$ 时的角速度大小。

## 参考解答整理

#### （1）临界温度与中央位置的小振动。

活塞偏离中央一个小角度时，沿管切线方向的运动方程为 $$mr\ddot\theta=mg\sin\theta-
\frac{nRT}{r(\pi/2-\theta)}+
\frac{nRT}{r(\pi/2+\theta)}.$$ 在线性近似下， $$\ddot\theta=\frac1r\left(g-\frac{8nRT}{\pi^2rm}\right)\theta.$$ 中央位置稳定要求括号内为负，因此 $$T_c=\frac{\pi^2mgr}{8nR}.$$ 当 $T>T_c$ 时，活塞在中央位置作简谐振动，圆频率为 $$\omega=\sqrt{\frac1r\left(\frac{8nRT}{\pi^2rm}-g\right)}
=\sqrt{\frac gr\frac{T-T_c}{T_c}}.$$

#### （2）临界点的稳定性。

令 $T=T_c$，保留最低非零项，得到 $$\ddot\theta=-\frac{(24+\pi^2)g}{6\pi^2r}\theta^3.$$ 加速度方向与 $\theta$ 的符号相反，故中央位置仍为稳定平衡位置；其回复作用为三阶小量，而非线性回复力。

#### （3）低温下的对称破缺平衡位置。

对非零平衡位置 $\theta_0$，合力为零给出 $$mg\sin\theta_0-
\frac{nRT}{r(\pi/2-\theta_0)}+
\frac{nRT}{r(\pi/2+\theta_0)}=0.$$ 利用 $T_c$ 可整理为 $$\frac{T}{T_c}=
\left(1-\frac{4\theta_0^2}{\pi^2}\right)
\frac{\sin\theta_0}{\theta_0}.$$ 当 $T$ 略低于 $T_c$ 时， $$\theta_0=\pm\sqrt{
\frac{6\pi^2}{24+\pi^2}\frac{T_c-T}{T_c}}$$ ，正、负号分别对应竖直线左右两侧的稳定位置。

#### （4）低温平衡位置附近的振动。

在 $\theta_0$ 附近写 $\theta_0+\theta$，其中 $\theta$ 为微小扰动。线性化后得到 $$\omega_0=
\sqrt{\frac{g\cos\theta_0}{r}
\left[
\frac{\tan\theta_0}{\theta_0}
\frac{\pi^2/2+2\theta_0^2}{\pi^2/2-2\theta_0^2}-1
\right]}.$$ 当 $T$ 略低于 $T_c$ 时，$|\theta_0|\ll1$，从而 $$\omega_0\approx\sqrt{\frac{2g}{r}\frac{T_c-T}{T_c}}.$$ 这与 $T$ 略高于 $T_c$ 时的结果共同刻画了临界温度两侧的频率变化。

#### （5）由能量积分求角速度。

将运动方程两边乘以 $d\theta$，并使用初始角速度近似为零的条件，有 $$\frac12mr^2\dot\theta^2
=mg(1-\cos\theta)+\frac{nRT}{r}
\ln\left(1-\frac{4\theta^2}{\pi^2}\right).$$ 故活塞到达可及角位置 $\theta$ 时的角速度大小为 $$|\dot\theta|=
\sqrt{\frac{2g}{r}(1-\cos\theta)+
\frac{2nRT}{mr^2}\ln\left(1-\frac{4\theta^2}{\pi^2}\right)}.$$
