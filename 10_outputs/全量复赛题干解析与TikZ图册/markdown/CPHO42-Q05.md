# 第42届复赛第5题：约瑟夫森结的相位动力学

![原题图5a：约瑟夫森结横截面](assets/CPHO42-Q05-figure5a.png)

![原题图5b：J、R、C 并联等效电路](assets/CPHO42-Q05-figure5b.png)

\[j=j_0\sin\delta,\qquad \frac{\partial\delta}{\partial t}=\frac{2e}{\hbar}U.\]

恒定电压下：

\[j(t)=j_0\sin\!\left(\frac{2eU_0}{\hbar}t+\delta(0)\right),\qquad T=\frac{\pi\hbar}{eU_0}.\]

自生磁场给出 sine-Gordon 型相位方程与穿透深度：

\[\frac{\mathrm d^2\delta}{\mathrm dy^2}=\frac{1}{\lambda_J^2}\sin\delta,\qquad
\lambda_J=\sqrt{\frac{\hbar}{2e\mu_0j_0(d+2\lambda)}}.\]

RCSJ 方程为

\[C\frac{\hbar}{2e}\frac{\mathrm d^2\delta}{\mathrm dt^2}+\frac{\hbar}{2eR}\frac{\mathrm d\delta}{\mathrm dt}+I_0\sin\delta=I.\]

最终速率比：

\[\frac{\bar c}{c}=\sqrt{\frac{d}{\epsilon_r(d+2\lambda)}}=0.055.\]

图5a、图5b均为原题图的TikZ重绘。
