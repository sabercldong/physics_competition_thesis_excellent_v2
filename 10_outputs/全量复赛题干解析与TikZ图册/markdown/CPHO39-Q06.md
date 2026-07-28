# 第39届复赛第6题：金属温差电效应的经典模型

## 题目整理

金属平板位于 $-L<x<L$，两侧真空电场为零。温度梯度改变电子密度，扩散流与漂移电流在平衡状态下抵消，进而形成热电势。

![CPHO39-Q06-structure](assets/CPHO39-Q06-structure.png)

## 解答要点

零净电流给出
\[
E_x(x)=-e\rho c\sqrt{\frac{T(x)}{n(x)}}\frac{\mathrm dn}{\mathrm dx}.
\]
高斯定理给出
\[
\varepsilon_0\frac{\mathrm dE_x}{\mathrm dx}=-e[n(x)-n_0].
\]
线性化后
\[
\lambda=\sqrt{\frac{\varepsilon_0\rho cT_0}{n_0}},\qquad
\frac{\mathrm d^2\delta n}{\mathrm dx^2}=\frac{\delta n}{\lambda^2}.
\]
局域力学平衡进一步导出
\[
\delta T(x)=\frac{T_0}{n_0}\left(\frac{e^2\rho c}{k_BT_0}-1\right)\delta n(x).
\]
因此本题经典模型的 Seebeck 系数是
\[
S=\left(\frac{e}{k_B}-\frac{T_0}{e\rho c}\right)^{-1}.
\]

![CPHO39-Q06-solution-chain](assets/CPHO39-Q06-solution-chain.png)

题目已明确说明：真实金属温差电效应需要量子理论，本题只是经典玩具模型。

## 依据

- 题面：`CPHO39-Q06.md` 第3至4页；
- 答案：第23至27页；
- 图6a按原题图重绘；关系图为自绘解析辅助图，答案无独立图件。
