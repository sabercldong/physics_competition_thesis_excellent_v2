> 本文件由项目已校订的LaTeX题干、参考解答和TikZ图件生成。评分时以本文件为主要阅读文本；需核对原始措辞时查看包内对应届次原始PDF。

# 第36届复赛第3题：电磁轨道炮加速模型

## 题干

如图，两根半径为 $b$、长度为 $L$、单位长度电阻为 $\lambda$ 的圆柱形平行导轨，所在对称面与水平面的夹角为 $\theta$。两导轨间的最近距离为 $d$（$d$ 很小）。质量为 $m$、直径为 $d$、电阻为 $R$ 的薄片状金属弹丸与导轨良好接触。导轨下端经同轴硬导线接入电流为 $I$ 的理想恒流源。忽略空气阻力、摩擦阻力和恒流源内部能量损耗，真空磁导率为 $\mu_0$。弹丸从导轨下端由静止开始加速，求：（1）弹丸所受磁场力；（2）出射速度；（3）加速过程中与出射时恒流源两端电压；（4）恒流源所做的功；（5）当 $\theta=0$ 且导轨、弹丸电阻均忽略时，出射动能与电源做功之比。

![CPHO36-Q03-figure1](assets/CPHO36-Q03-figure1.png)

## 参考解答整理

#### （1）安培力。

弹丸直径很小，可将两根载流导轨近似为半无限长直导线。弹丸上一点到一侧导轨轴线的距离为 $r'$ 时，磁感应强度为 $$B=\frac{\mu_0 I}{4\pi r'}+\frac{\mu_0 I}{4\pi(d+2b-r')}.$$ 对弹丸横向积分（$b\le r'\le d+b$），得沿导轨向上的安培力 $$\boxed{F=\frac{\mu_0 I^2}{2\pi}\ln\frac{d+b}{b}.}$$

#### （2）出射速度。

沿导轨列牛顿第二定律： $$F-mg\sin\theta=ma,
\qquad
a=\frac{\mu_0 I^2}{2\pi m}\ln\frac{d+b}{b}-g\sin\theta.$$ 弹丸做匀加速直线运动，因而 $$\boxed{v_{\max}=\sqrt{2L\left(\frac{\mu_0 I^2}{2\pi m}\ln\frac{d+b}{b}-g\sin\theta\right)}.}$$

#### （3）恒流源电压。

设弹丸到导轨下端的距离为 $l$、速度为 $v=\mathrm{d}l/\mathrm{d}t$。回路中的磁通量和感应电动势为 $$\Phi=\frac{\mu_0 I l}{\pi}\ln\frac{d+b}{b},
\qquad
\varepsilon=-\frac{\mu_0 Iv}{\pi}\ln\frac{d+b}{b}.$$ 由全电路欧姆定律 $U+\varepsilon=2\lambda lI+IR$，并代入 $v=at$、$l=at^2/2$，得到任意时刻的电压 $$\boxed{U=\lambda Iat^2+IR+\frac{\mu_0 I}{\pi}\ln\frac{d+b}{b}\,at.}$$ 加速时间 $T=\sqrt{2L/a}$，故出射时 $$\boxed{U_{\rm 出}=2\lambda IL+IR+\frac{\sqrt2\mu_0 I}{\pi}\ln\frac{d+b}{b}\sqrt{a}.}$$

#### （4）电源做功。

由 $W=\int_0^T UI\,\mathrm{d}t$，将三项分别积分，得到 $$W=W_1+W_2+W_3,$$ $$W_1=\frac{2\sqrt2\lambda I^2}{3}L^{3/2}a^{-1/2},\qquad
W_2=I^2R\sqrt{2L}\,a^{-1/2},$$ $$\boxed{W_3=\frac{\mu_0 I^2L}{\pi}\ln\frac{d+b}{b}.}$$ 其中 $a$ 为第（2）问所得的加速度，故上式共同给出整个加速过程的电源做功。

#### （5）无电阻、水平导轨的极限。

当 $\theta=0$ 且电阻可忽略时， $$E_{\max}=\frac{\mu_0 I^2L}{2\pi}\ln\frac{d+b}{b},
\qquad
W=\frac{\mu_0 I^2L}{\pi}\ln\frac{d+b}{b}.$$ 因此 $$\boxed{\eta=\frac{E_{\max}}{W}=50\%.}$$
