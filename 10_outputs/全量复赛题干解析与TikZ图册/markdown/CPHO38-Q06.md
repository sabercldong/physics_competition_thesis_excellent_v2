> 本文件由项目已校订的LaTeX题干、参考解答和TikZ图件生成。评分时以本文件为主要阅读文本；需核对原始措辞时查看包内对应届次原始PDF。

# 第38届复赛第6题：同轴带电圆筒与电磁角动量

## 题干

真空中有两个同轴、无限长、均匀带电的薄壁圆筒，半径分别为 $r_1$、$r_2$。沿轴向单位长度内，两圆筒的质量均为 $m$，内、外圆筒的电荷分别为 $q$ 和 $-q$（$q>0$），两筒均可绕轴自由旋转，如图。真空介电常量和磁导率分别为 $\varepsilon_0$、$\mu_0$。

求：（1）距轴 $r$ 处的电场；（2）两筒以相同角速度 $\omega$ 同向旋转时的磁场；（3）质量为 $\mu$、电荷量为 $Q$ 且 $Q$ 与 $q$ 同号的点电荷从 $r=r_1$ 处静止释放，能够到达 $r=r_2$ 的 $\omega$ 条件；（4）两筒初始静止，对外筒施加外力矩，待外筒角速度达到 $\Omega$ 时，求内筒角速度、外力矩总冲量矩和两筒总机械角动量。

![CPHO38-Q06-figure6a](assets/CPHO38-Q06-figure6a.png)

## 参考解答整理

#### （1）电场分布。

由圆柱对称性和高斯定理，电场沿径向， $$\boxed{
E(r)=
\begin{cases}
\dfrac{q}{2\pi\varepsilon_0r},&r_1<r<r_2,\\[4pt]
0,&\text{其他区域}.
\end{cases}}$$

#### （2）磁场分布。

内筒旋转形成的轴向单位长度等效电流为 $I=q\omega/(2\pi)$。内、外筒等效电流大小相同、方向相反。以题解规定的轴向为正， $$\boxed{
B(r)=
\begin{cases}
-\dfrac{\mu_0q\omega}{2\pi},&r_1<r<r_2,\\[4pt]
0,&\text{其他区域}.
\end{cases}}$$

#### （3）点电荷到达外筒的条件。

设点电荷的径向速度为 $v_r=\dot r$，绕轴机械角动量为 $\ell$。磁场力矩满足 $$\frac{\mathrm d\ell}{\mathrm dt}=QB r\dot r,
\qquad
\ell=\frac12QB(r^2-r_1^2),$$ 其中使用了 $\ell(r_1)=0$。电场做功给出 $$E_k=\frac{qQ}{2\pi\varepsilon_0}\ln\frac r{r_1}
=\frac12\left(\mu v_r^2+\frac{\ell^2}{\mu r^2}\right).$$ 在 $r=r_2$ 处要求径向动能非负，代入 $|B|=\mu_0q|\omega|/(2\pi)$，得到 $$\boxed{
\omega^2\le
\frac{16\pi\mu r_2^2}
{\varepsilon_0\mu_0^2qQ(r_2^2-r_1^2)^2}
\ln\frac{r_2}{r_1}.}$$

#### （4）外筒驱动时的角动量传递。

记内、外筒在自身内部产生的磁场为 $$B_1=\frac{\mu_0q\omega}{2\pi},
\qquad
B_2=-\frac{\mu_0q\Omega}{2\pi}.$$ 变化磁场在 $r=r_1$ 处产生切向感应电场。由法拉第定律和内筒转动方程， $$E_1=-\frac{\mu_0qr_1}{4\pi}\frac{\mathrm d}{\mathrm dt}(\omega-\Omega),
\qquad
mr_1^2\frac{\mathrm d\omega}{\mathrm dt}=qE_1r_1.$$ 初态两筒均静止，积分得 $$\boxed{\omega=\alpha\Omega,\qquad
\alpha\equiv\frac{\mu_0q^2}{4\pi m+\mu_0q^2}.}$$

在 $r=r_2$ 处，感应电场对外筒的力矩为 $$M_2=\frac{\mu_0q^2}{4\pi}
\left(r_1^2\frac{\mathrm d\omega}{\mathrm dt}
-r_2^2\frac{\mathrm d\Omega}{\mathrm dt}\right).$$ 因此感应力矩的冲量矩为 $$J_{\text{电场}}=\frac{\mu_0q^2}{4\pi}(\alpha r_1^2-r_2^2)\Omega.$$ 外筒的机械角动量为 $L_2=mr_2^2\Omega$，由 $J+J_{\text{电场}}=L_2$ 得外力矩总冲量矩 $$\boxed{J=\left[mr_2^2-\frac{\mu_0q^2}{4\pi}
(\alpha r_1^2-r_2^2)\right]\Omega.}$$ 两筒总机械角动量为 $$\boxed{L=m(r_1^2\omega+r_2^2\Omega)
=m\Omega(\alpha r_1^2+r_2^2).}$$
