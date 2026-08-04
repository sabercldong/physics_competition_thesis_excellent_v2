> 本文件由项目已校订的LaTeX题干、参考解答和TikZ图件生成。评分时以本文件为主要阅读文本；需核对原始措辞时查看包内对应届次原始PDF。

# 第38届复赛第5题：原子激光制冷与塞曼减速

## 题干

原子激光制冷利用与原子束反向传播的单频激光，使原子反复吸收光子并各向同性发射，从而减小原子束流速度。塞曼减速装置利用空间变化的磁场补偿原子减速时的多普勒失谐，使原子在减速管中保持共振散射，如图所示。

考虑经准直的 ${}^{40}\mathrm K$ 原子束，其初始运动只有一个自由度，原子气体温度为 $350\,{}^\circ\mathrm C$。共振时散射速率 $\Gamma=5.00\times10^6\,\mathrm{s^{-1}}$，减速激光波长 $\lambda=670\,\mathrm{nm}$。跃迁频率随磁感应强度满足 $$f_0(B)=f_0(B=0)+\beta B,\qquad
\beta=-1.00\times10^{10}\,\mathrm{Hz/T}.$$ 求：（1）原子的方均根速率；（2）共振减速的加速度和减速至静止的距离；（3）无磁场时使相向运动原子共振所需的激光降频量；（4）以准直管出口 $z=0$ 处 $B=0$ 为条件，实现沿程共振的 $B(z)$。

![CPHO38-Q05-figure5a](图件/CPHO38-Q05-figure5a.png)

## 参考解答整理

#### （1）准直原子的初始速率。

准直后只保留一个自由度，能量均分给出 $$\frac12mv_0^2=\frac12k_\mathrm BT.$$ 取 $$m=40\times1.66\times10^{-27}\,\mathrm{kg}=6.64\times10^{-26}\,\mathrm{kg},
\qquad T=(350+273)\,\mathrm K=623\,\mathrm K,$$ 得到 $$\boxed{v_0=360\,\mathrm{m/s}.}$$

#### （2）光子散射产生的减速。

单个光子动量为 $p_{\mathrm{single}}=h/\lambda$。在时间 $\Delta t$ 内，原子共振吸收 $N=\Gamma\Delta t$ 个反向光子，故 $$a=\frac{F}{m}=\frac{\Gamma h}{\lambda m}
=7.45\times10^4\,\mathrm{m/s^2}.$$ 恒减速度减速至静止的距离为 $$\boxed{s=\frac{v_0^2}{2a}=0.87\,\mathrm m.}$$

#### （3）无磁场时的多普勒失谐。

相向运动时，原子参考系中的激光频率为 $$f'=f\sqrt{\frac{1+v/c}{1-v/c}}.$$ 在 $v\ll c$ 下，共振条件 $f'=f_0$ 给出 $$\Delta f\equiv f_0-f=\frac{v}{c}f_0=\frac{v}{\lambda}.$$ 因此，当 $v=v_0$ 时，激光应降低的频率为 $$\boxed{\Delta f=\frac{v_0}{\lambda}=537\,\mathrm{MHz}.}$$

#### （4）塞曼补偿磁场。

沿减速管，原子速度满足 $$v(z)=\sqrt{v_0^2-2az}.$$ 要保持共振，磁场导致的跃迁频率变化必须抵消多普勒失谐的变化。由 $B(0)=0$、$f_0(z)=f_0(0)+\beta B(z)$，得 $$\boxed{
B(z)=-\frac{v_0-\sqrt{v_0^2-2az}}{\beta\lambda}
=-\frac{v_0}{\beta\lambda}
\left[1-\sqrt{1-\frac{2\Gamma h z}{\lambda m v_0^2}}\right].}$$ 代入题给数据， $$\boxed{B(z)=0.0537\left(1-\sqrt{1-1.15z}\right)\,\mathrm T,}$$ 其中 $z$ 以米为单位，$0\le z\le0.869\,\mathrm m$，相应地 $0\le B\le0.0537\,\mathrm T$。
