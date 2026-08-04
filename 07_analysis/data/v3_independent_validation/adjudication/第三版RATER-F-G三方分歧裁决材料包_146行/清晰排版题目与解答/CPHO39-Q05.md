> 本文件由项目已校订的LaTeX题干、参考解答和TikZ图件生成。评分时以本文件为主要阅读文本；需核对原始措辞时查看包内对应届次原始PDF。

# 第39届复赛第5题：快慢拉动双弹簧断裂模型

## 题干

两根相同的理想轻弹簧，劲度系数均为 $k$、自然长度均为零；中间以质量为 $m$ 的小球相连。弹簧1上端固定在天花板，系统自然下垂且初始静止。任一弹簧拉伸到临界长度（大于 $mg/k$）即断裂。对弹簧2下端施加随时间变化的外力 $F(t)$。

设 $F(t)=0$（$t<0$），$F(t)=\alpha t$（$t\ge0$），其中 $\alpha>0$ 表示加载快慢。求：（1）弹簧1长度的运动方程；（2）$x_1(t),x_2(t)$；（3）两根弹簧先断的条件及其与 $\alpha$ 的关系；（4）临界长度为 $L$ 时确保弹簧2先断的 $\alpha$ 条件，以及同时断裂的条件。

![CPHO39-Q05-model](图件/CPHO39-Q05-model.png)

## 参考解答整理

#### （1）运动方程。

以弹簧1的长度 $x_1(t)$ 描述小球的竖直位置。牛顿第二定律与胡克定律给出 $$\boxed{m\ddot{x}_1=-kx_1+mg+F(t).}$$

#### （2）线性加载下的长度。

令 $\omega^2=k/m$，以 $mg/k$ 平移坐标并代入 $F(t)=\alpha t$。由初始条件 $x_1(0)=mg/k$、$\dot{x}_1(0)=0$，得到 $$\boxed{x_1(t)=\frac{mg}{k}+\frac{\alpha}{k}t-\frac{\alpha}{\omega k}\sin\omega t,}
\qquad
\boxed{x_2(t)=\frac{\alpha}{k}t.}$$ 后式直接由 $F(t)=kx_2(t)$ 得到。

#### （3）先断条件与快慢加载。

两弹簧长度差为 $$\Delta x=x_1-x_2=\frac{mg}{k}-\frac{\alpha}{\omega k}\sin\omega t.$$ 因此当 $\alpha<mg\omega=g\sqrt{km}$ 时，任何时刻均有 $\Delta x>0$，弹簧1必先断。若 $\alpha\ge mg\omega$，弹簧1先断需满足 $$\sin(\omega t_0)<\frac{mg\omega}{\alpha};$$ 弹簧2先断则需满足相反的不等式，且必须有 $\alpha>mg\omega$。图将该长度差的相位判定画出：加载越快，满足弹簧2先断的相位区间越宽，这解释了快速拉动下弹簧2更可能断裂的现象。

![CPHO39-Q05-phase](图件/CPHO39-Q05-phase.png)

#### （4）给定临界长度 $L$。

弹簧2达到临界长度的时刻为 $t_0=kL/\alpha$。要确保其先断，应满足 $$\boxed{\sin\left(\frac{kL}{\alpha}\sqrt{\frac{k}{m}}\right)
>\frac{mg}{\alpha}\sqrt{\frac{k}{m}}.}$$ 存在同时断裂的情形，其临界条件只需将上式的不等号改为等号。
