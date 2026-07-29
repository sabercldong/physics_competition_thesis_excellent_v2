# 第42届复赛第2题：重离子束探针与平行板能量分析器

![原题图2a：重离子束探针测量原理](assets/CPHO42-Q02-figure2a.png)

![原题图2b：普罗卡-格林平行板能量分析器](assets/CPHO42-Q02-figure2b.png)

平行板内的斜抛运动给出接收位置

\[X_D(\theta_I)=\frac{2K_2d\sin(2\theta_I)}{q_2V_A}+(Y_{D1}+Y_{D2})\cot\theta_I.\]

二级聚焦条件为

\[\theta_I=\frac\pi6,\qquad V_A=\frac{K_2d}{2q_2(Y_{D1}+Y_{D2})},\qquad X_D=3\sqrt3(Y_{D1}+Y_{D2}).\]

离轴入射时，接收位置偏移为

\[s=-\frac{\sin(\theta_I+\theta_a)}{\sin(\theta_I+\theta_b)}l.\]

由上、下半平面的接收电流可以反推 $K_2$；再由直接电离过程的能量守恒

\[K_1-q_1\Phi\simeq K_2-q_2\Phi,\]

得到测量位置电势

\[\Phi=\frac{K_2-K_1}{q_2-q_1}=\frac{K_2-K_1}{e}.\]

图2a、图2b均为原题图的 TikZ 重绘。
