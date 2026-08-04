> 本文件由项目已校订的LaTeX题干、参考解答和TikZ图件生成。评分时以本文件为主要阅读文本；需核对原始措辞时查看包内对应届次原始PDF。

# 第39届复赛第6题：金属温差电效应的经典模型

## 题干

如图，厚度为 $2L$、在 $y,z$ 方向无限延展的金属平板位于 $-L<x<L$；两侧是真空，电场为零。金属中导电电子在均匀正电荷背景上运动。温度 $T(x)=T_0+\delta T(x)$ 会使电子数密度 $n(x)=n_0+\delta n(x)$ 略偏离均匀值，并产生小的 $x$ 向电场 $E_x(x)$；两内表面有面电荷密度 $\sigma_-$、$\sigma_+$。

![CPHO39-Q06-structure](图件/CPHO39-Q06-structure.png)

已知扩散流满足 $j_x=-D\,\mathrm dn/\mathrm dx$，其中 $D=c\sqrt{T/n}$；电阻率 $\rho$ 为常量。求：（1）$E_x(x)$；（2）由高斯定理得到的方程与边界条件；（3）线性化的 $\delta n(x)$；（4）局域力学平衡下的 $\delta T(x)$；（5）Seebeck 系数 $S=[U(L)-U(-L)]/[T(L)-T(-L)]$。

## 参考解答整理

#### （1）零净电流条件。

电子扩散流与漂移电流抵消： $$-e j_x+\frac1\rho E_x=0,
\qquad
\boxed{E_x(x)=-e\rho c\sqrt{\frac{T(x)}{n(x)}}\frac{\mathrm dn}{\mathrm dx}.}$$

#### （2）高斯定理与边界条件。

金属内部净电荷密度为 $-e[n(x)-n_0]$，故 $$\varepsilon_0\frac{\mathrm dE_x}{\mathrm dx}=-e[n(x)-n_0],$$ 从而 $$\varepsilon_0\rho c\frac{\mathrm d}{\mathrm dx}
\left[\sqrt{\frac{T(x)}{n(x)}}\frac{\mathrm dn}{\mathrm dx}\right]=n(x)-n_0.$$ 真空侧电场为零，给出 $\varepsilon_0E_x(-L+0)=\sigma_-$、$\varepsilon_0E_x(L-0)=-\sigma_+$。

#### （3）密度偏离。

保留小量的一阶项，定义 $$\lambda=\sqrt{\frac{\varepsilon_0\rho cT_0}{n_0}},
\qquad
\frac{\mathrm d^2\delta n}{\mathrm dx^2}=\frac{1}{\lambda^2}\delta n.$$ 答案给出的等价形式为 $$\boxed{\delta n(x)=\frac{1}{\lambda e}\left[
\frac{\sigma_++\sigma_-}{2\sinh(L/\lambda)}\cosh\frac{x}{\lambda}
+\frac{\sigma_+-\sigma_-}{2\cosh(L/\lambda)}\sinh\frac{x}{\lambda}\right].}$$

#### （4）局域热平衡。

电子气压强 $p=nk_BT$，薄层力平衡满足 $\mathrm dp/\mathrm dx=-eE_xn$。线性化并代入前述关系后， $$\boxed{\delta T(x)=\frac{T_0}{n_0}\left(\frac{e^2\rho c}{k_BT_0}-1\right)\delta n(x).}$$

![CPHO39-Q06-solution-chain](图件/CPHO39-Q06-solution-chain.png)

#### （5）Seebeck 系数。

由 $E_x=-\mathrm dU/\mathrm dx$，或直接比较两端的电势差和温度差，得到经典玩具模型中的 $$\boxed{S=\left(\frac{e}{k_B}-\frac{T_0}{e\rho c}\right)^{-1}.}$$ 题目附注指出：真实金属温差电效应必须考虑电子量子效应；以上仅为题设的经典简化模型。
