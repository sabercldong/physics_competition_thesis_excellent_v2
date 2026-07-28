# 第38届复赛第6题：同轴带电圆筒与电磁角动量

## 题干整理

两个无限长同轴薄壁圆筒的半径为 $r_1,r_2$，单位长度质量均为 $m$，单位长度电荷分别为 $q$、$-q$。两筒都能绕轴自由旋转。

![同轴带电圆筒与粒子运动](assets/CPHO38-Q06-figure6a.png)

## 解析整理

### 1. 电场和磁场

$$
E(r)=
\begin{cases}
\dfrac{q}{2\pi\varepsilon_0r},&r_1<r<r_2,\\
0,&\text{其他区域},
\end{cases}
$$

两筒以相同角速度 $\omega$ 同向旋转时，

$$
B(r)=
\begin{cases}
-\dfrac{\mu_0q\omega}{2\pi},&r_1<r<r_2,\\
0,&\text{其他区域}.
\end{cases}
$$

### 2. 点电荷到达外筒的条件

点电荷角动量和电场做功分别为

$$
\ell=\frac12QB(r^2-r_1^2),
\qquad
E_k=\frac{qQ}{2\pi\varepsilon_0}\ln\frac r{r_1}.
$$

要求 $r=r_2$ 处径向动能非负，得到

$$
\boxed{
\omega^2\le
\frac{16\pi\mu r_2^2}
{\varepsilon_0\mu_0^2qQ(r_2^2-r_1^2)^2}
\ln\frac{r_2}{r_1}}.
$$

### 3. 外筒驱动与角动量

定义

$$
\alpha=\frac{\mu_0q^2}{4\pi m+\mu_0q^2},
$$

则内筒角速度为

$$
\boxed{\omega=\alpha\Omega}.
$$

外力矩总冲量矩和两筒总机械角动量分别为

$$
\boxed{J=\left[mr_2^2-\frac{\mu_0q^2}{4\pi}
(\alpha r_1^2-r_2^2)\right]\Omega},
$$

$$
\boxed{L=m\Omega(\alpha r_1^2+r_2^2)}.
$$

## 图件与依据

题干依据 `CPHO38-Q06_transcription_v1.md`；公式依据 `CPHO38-Q06_formula_check_v1.csv` 与答案第14至16页。左图重绘原题图6a，右图为场区和粒子运动辅助示意。
