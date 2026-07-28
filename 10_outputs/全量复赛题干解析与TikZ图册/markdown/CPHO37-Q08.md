# 第37届复赛第8题：电光调制器与调制效率

电光晶体产生的相位差为
$$\Delta\varphi=\frac{2\pi}{\lambda_0}n_0^3\gamma V,$$
故半波电压
$$V_\pi=\frac{\lambda_0}{2n_0^3\gamma}.$$

未加 $\lambda/4$ 波片时，$T\approx[\pi V/(2V_\pi)]^2$，为非线性；加入后
$$T\approx\frac12\left(1+\frac{\pi V_m}{V_\pi}\sin\omega_mt\right),$$
从而在小信号区线性化。高频时 $|V_c|\ll|V|$；并联谐振 $\omega_m=1/\sqrt{LC}$ 且 $R_L\gg R_m$ 时，$|V_c|\approx|V|$。

TikZ图重绘题面光路及等效电路。
