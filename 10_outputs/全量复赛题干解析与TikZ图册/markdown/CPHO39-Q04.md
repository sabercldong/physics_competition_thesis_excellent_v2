# 第39届复赛第4题：旋转圆环上铰接细杆的平衡与稳定性

## 题目整理

长度为 $2a$、质量为 $m$ 的匀质细杆在端点 $P$ 铰接于半径为 $R$ 的水平圆环。圆环以角速度 $\omega$ 绕竖直中心轴转动；细杆始终位于 $OP$ 的竖直平面，与竖直方向夹角为 $\theta$。求两参考系机械能、平衡方程、各象限平衡位形数、受力检验与稳定性。

![CPHO39-Q04-structure](assets/CPHO39-Q04-structure.png)

## 解答要点

实验室系与随动系机械能分别为

\[
E_L=mga\cos\theta+\frac23ma^2\dot\theta^2+\frac12m\left[(R+a\sin\theta)^2+\frac13a^2\sin^2\theta\right]\omega^2,
\]
\[
E_S=\frac23ma^2\dot\theta^2+mga\cos\theta-\frac12m\left[(R+a\sin\theta)^2+\frac13a^2\sin^2\theta\right]\omega^2.
\]

平衡条件为
\[
\tan\theta+\frac{4a\omega^2}{3g}\sin\theta+\frac{R\omega^2}{g}=0.
\]
令 $A=4a\omega^2/(3g)$、$B=R\omega^2/g$，可画成 $-\tan\theta=A\sin\theta+B$。

![CPHO39-Q04-solution-tan](assets/CPHO39-Q04-solution-tan.png)

等价地也可画为 $-\cot\theta=A'\cos\theta+B'$，其中 $A'=4a/(3R)$、$B'=g/(R\omega^2)$。

![CPHO39-Q04-solution-cot](assets/CPHO39-Q04-solution-cot.png)

- 第I象限无平衡位形；第II、IV象限各一个。
- 第III象限的临界条件是
  \[
  \left(\frac{4a}{3}\right)^{2/3}-R^{2/3}=\left(\frac{g}{\omega^2}\right)^{2/3}.
  \]
  左端较小时无位形，较大时有两个，等号时有一个临界位形。
- 第II象限稳定，第IV象限不稳定；第III象限双根中较大根稳定、较小根不稳定，临界相切位形不稳定。

## 分象限受力图

![CPHO39-Q04-solution-forces-upper](assets/CPHO39-Q04-solution-forces-upper.png)

![CPHO39-Q04-solution-forces-iii](assets/CPHO39-Q04-solution-forces-iii.png)

![CPHO39-Q04-solution-forces-iv](assets/CPHO39-Q04-solution-forces-iv.png)

图中 $F_c$ 是离心分布力对 $P$ 点力矩的等效合力，$mg$ 作用于细杆中点。

## 依据

- 题面：`CPHO39-Q04.md` 第2至3页；
- 答案：第12至19页；
- 图件：原题图4a，答案解题图4a、4a$'$、4b；均以TikZ重绘，不使用页面截图。
