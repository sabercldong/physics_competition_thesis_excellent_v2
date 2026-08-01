> 本文件由项目已校订的LaTeX题干、参考解答和TikZ图件生成。评分时以本文件为主要阅读文本；需核对原始措辞时查看包内对应届次原始PDF。

# 第35届复赛第8题：穆斯堡尔效应与共振吸收

## 题干

$^{57}\mathrm{Fe}$ 原子核第一激发态与基态的能量差以 $E_0$ 为中心、在宽度 $2\Gamma$ 的范围内取值。给定 $$E_0=2.31\times10^{-15}\,\mathrm J,\qquad
\Gamma=3.2\times10^{-13}E_0,$$ $$m_{\mathrm{Fe}}=9.5\times10^{-26}\,\mathrm{kg},\qquad
h=6.6\times10^{-34}\,\mathrm{J\,s},\qquad
c=3.0\times10^8\,\mathrm{m\,s^{-1}}.$$ 求：（1）忽略能级宽度时，发射光子的反冲能及考虑、不考虑反冲时的频率差；（2）吸收光子的相应结果；（3）考虑能级宽度后，两个静止原子核间能否发生共振吸收；（4）若原子核置于晶体中而不发生核反冲，求发生共振吸收的相对速度范围，并说明如何用速度补偿测量 $10^{-10}$ 的相对频率变化。

## 参考解答整理

#### （1）发射过程。

设发射光子频率为 $\nu_{\mathrm e}$、原子核反冲速度为 $v$。能量和动量守恒给出 $$E_0=h\nu_{\mathrm e}+\frac12m_{\mathrm{Fe}}v^2,\qquad
\frac{h\nu_{\mathrm e}}{c}=m_{\mathrm{Fe}}v.$$ 令 $\nu_0=E_0/h$，在 $E_0\ll m_{\mathrm{Fe}}c^2$ 下， $$\nu_{\mathrm e}\simeq\nu_0-\frac{h\nu_0^2}{2m_{\mathrm{Fe}}c^2},
\qquad
\nu_{\mathrm e}-\nu_0\simeq-\nu_0\frac{E_0}{2m_{\mathrm{Fe}}c^2}
=\boxed{-4.7\times10^{11}\,\mathrm{Hz}}.$$ 反冲能为 $$E_{\mathrm R}=\frac{E_0^2}{2m_{\mathrm{Fe}}c^2}
=\boxed{3.1\times10^{-22}\,\mathrm J}.$$

#### （2）吸收过程。

若吸收光子频率为 $\nu_{\mathrm a}$、核反冲速度为 $v'$，则 $$h\nu_{\mathrm a}=E_0+\frac12m_{\mathrm{Fe}}v'^2,\qquad
\frac{h\nu_{\mathrm a}}{c}=m_{\mathrm{Fe}}v'.$$ 因而 $$\nu_{\mathrm a}-\nu_0\simeq+\nu_0\frac{E_0}{2m_{\mathrm{Fe}}c^2}
=\boxed{4.7\times10^{11}\,\mathrm{Hz}},
\qquad
E'_{\mathrm R}=E_{\mathrm R}=\boxed{3.1\times10^{-22}\,\mathrm J}.$$

#### （3）静止核间不能共振吸收。

发射和吸收频率区间分别为 $$\left[\nu_{\mathrm e}-\frac{\Gamma}{h},\,\nu_{\mathrm e}+\frac{\Gamma}{h}\right],
\qquad
\left[\nu_{\mathrm a}-\frac{\Gamma}{h},\,\nu_{\mathrm a}+\frac{\Gamma}{h}\right].$$ 两区间重叠需要 $\Gamma>E_{\mathrm R}$。然而 $$\frac{E_{\mathrm R}}{\Gamma}=4.2\times10^5,$$ 即 $E_{\mathrm R}\gg\Gamma$，所以静止的自由核之间**不能**发生共振吸收。

#### （4）晶体中的无反冲共振与频率测量。

核嵌入晶体后，晶体整体反冲能可以忽略。能量窗口为 $$[E_0-\Gamma,E_0+\Gamma].$$ 对相对速度 $V$（正负对应相互接近或远离），小速度多普勒近似为 $$\nu'\simeq\left(1+\frac{V}{c}\right)\nu.$$ 两个窗口仍有重叠的速度范围为 $$\boxed{-0.19\,\mathrm{mm\,s^{-1}}\le V\le0.19\,\mathrm{mm\,s^{-1}}.}$$ 若到达吸收晶体的光子频率相对变化为 $\Delta\nu/\nu_0=\pm10^{-10}$，调节吸收晶体速度使多普勒位移抵消它： $$V'=-\frac{\Delta\nu}{\nu}c\simeq-\frac{\Delta\nu}{\nu_0}c.$$ 故所需速度改变量的量级为 $$\boxed{|V'|=10^{-10}c=3\,\mathrm{cm\,s^{-1}}.}$$ 测量达到共振吸收时的速度改变量，即可反推出光子频率的微小变化。
