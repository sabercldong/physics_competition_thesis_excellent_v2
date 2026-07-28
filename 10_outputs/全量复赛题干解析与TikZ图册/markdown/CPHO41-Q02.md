# 第41届复赛第2题：台球弹性碰撞、滑动摩擦与30度经验规则

![原题图2a：碰撞后的飞行方向](assets/CPHO41-Q02-figure2a.png)
![原题图2b：达到纯滚后的最终方向](assets/CPHO41-Q02-figure2b.png)
![原题图2c：球杆冲量与开球自旋](assets/CPHO41-Q02-figure2c.png)
![答案图2b：碰撞速度的质心系几何关系](assets/CPHO41-Q02-solution-geometry.png)

两球完全弹性碰撞且球间无摩擦时，$\theta+\varphi=90^\circ$，碰撞不改变 $Q$ 球自旋；其碰撞后速度分量为

\[v_{Qx}=v_0\sin\varphi\cos\varphi,\qquad v_{Qy}=v_0\sin^2\varphi.\]

接触点初速度为

\[\boldsymbol v_{C0}=(v_0\sin\varphi\cos\varphi-R\omega_{0y})\boldsymbol i+(v_0\sin^2\varphi+R\omega_{0x})\boldsymbol j,\]

纯滚前的持续时间是 $\Delta t=2|\boldsymbol v_{C0}|/(7\mu g)$。在 $h=7R/5$ 的开球条件下，$Q$ 球立即纯滚；其最终偏角满足

\[\tan\theta_f=\frac{\sin\varphi\cos\varphi}{\sin^2\varphi+2/5}=\frac{5\sin2\varphi}{9-5\cos2\varphi}.\]

当 $\varphi_m=28.1^\circ$ 时，$\theta_f$ 最大，为 $33.7^\circ$。题面三幅图和答案速度几何图均为 TikZ 重绘，不含原始截图。
