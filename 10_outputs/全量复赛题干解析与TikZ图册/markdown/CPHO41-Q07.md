# 第41届复赛第7题：超导环磁通量子化与无相互作用电子

![原题图7a：一维圆环上的电子](assets/CPHO41-Q07-figure7a.png)

![原题图7b：穿过圆环的磁通](assets/CPHO41-Q07-figure7b.png)

圆环闭合要求波函数满足 $\psi(x+2\pi R)=\psi(x)$，所以电子动量为

\[p_n=\frac{n\hbar}{R},\qquad n\in\mathbb Z.\]

通入磁通 $\Phi$ 后，$p'_n=p_n+eA$、$\Phi=2\pi RA$，单电子能量成为

\[E_n(\Phi)=\frac{\hbar^2}{2mR^2}\left(n+\frac{e\Phi}{h}\right)^2.\]

无相互作用多电子系统取不同的动量量子数，并选择使总能量最小的占据方式。以 $n\mapsto n+1$ 重新编号可得

\[E_{\mathrm{tot}}\left(\Phi+\frac{h}{e}\right)=E_{\mathrm{tot}}(\Phi).\]

对奇数电子数 $N=2M+1$，在 $-h/(2e)\leq\Phi<h/(2e)$ 内，

\[\bar E(\Phi)=\frac{e^2\Phi^2}{4\pi^2}\frac{1}{2mR^2}+\frac{\hbar^2}{2mR^2}\frac{M(M+1)}{3}.\]

因此奇数电子数时，$\Phi=0$ 的平均能量较低；偶数电子数时，$|\Phi|=h/(2e)$ 附近较低。加入 $p'$ 与 $-p'$ 成对出现的约束后，题设的两种双环构型具有

\[C_1=\frac{M(M+1)}{3},\qquad C_2=\frac{M(M+1)}{3}+\frac14,\qquad \lim_{M\to\infty}\frac{C_1}{C_2}=1.\]

图7a、图7b均为原题图的 TikZ 重绘。
