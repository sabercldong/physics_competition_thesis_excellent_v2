# 第41届复赛第3题：油水混合物的表面张力与微观表面层模型

![解析辅助图：表面张力极小值对应的混合终温](assets/CPHO41-Q03-mixing.png)
![解析辅助图：表面层与内部粒子的邻近关系](assets/CPHO41-Q03-surface-layer.png)

题设恒容条件为 $dp=\beta dT$，参考状态还满足 $p=\beta T$。代入后，表面张力成为温度的二次函数：

\[\frac{\sigma}{10^{-3}\,\mathrm{N\,m^{-1}}}=60-110\times10^{-3}\frac{T}{\mathrm K}+167\times10^{-6}\frac{T^2}{\mathrm K^2}.\]

最小值对应 $T_f=329\,\mathrm K$，即 $t_f\approx56^\circ\mathrm C$。等体积油水混合的热量守恒给出注水温度 $t_w\approx35^\circ\mathrm C$。

微观模型以表面层邻近粒子数为内部的 $\zeta$ 倍、特征间距为 $D$ 为起点。由 $L_m=N_A(|\epsilon|/2)n$ 和 $D^3N_A=\mu/\rho$，结果为

\[\sigma=(1-\zeta)\frac{L_m}{N_A}\left(\frac{\rho N_A}{\mu}\right)^{2/3}.\]

原题没有独立题图；本页两图均是用于解释推导关系的 TikZ 解析辅助图。
