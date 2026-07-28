# 第37届复赛第6题：光纤陀螺仪与Sagnac效应

## 题干整理

题目围绕旋转光纤环路中的两束反向传播光展开：先求双层光纤的入射角条件，再求 $N$ 匝环路的传播时间与相位差，最后推导谐振环形腔同一级次两类模式的频率分裂。

## 解析整理

### 1. 光纤输入端

$$
n_0\sin i=n_1\sin i',\qquad i'+i''=\frac\pi2,
$$

$$
\sin i_c=\frac{n_2}{n_1},\qquad i''\geqslant i_c.
$$

因此

$$
i\leqslant\arcsin\frac{\sqrt{n_1^2-n_2^2}}{n_0}.
$$

### 2. Sagnac相位差

![Sagnac效应中的分束器位移与反向传播光](assets/CPHO37-Q06-solution-sagnac.png)

$$
t_{\mathrm{CCW}}=
\frac{N2\pi R(n_1c+\Omega R)}{c^2-(\Omega R)^2},
$$

$$
t_{\mathrm{CW}}=
\frac{N2\pi R(n_1c-\Omega R)}{c^2-(\Omega R)^2}.
$$

$$
\Delta\varphi=
\frac{8\pi^2NR^2\Omega c}{\lambda_0[c^2-(\Omega R)^2]}.
$$

在本题模型中，相位差与介质折射率 $n_1$ 无关。

### 3. 谐振频率差

$$
\Delta f=
\frac{m\Omega}{\pi}
\frac{c^2-(\Omega R)^2}{c^2-(n_1\Omega R)^2}
\approx\frac{m\Omega}{\pi}.
$$

$$
\Omega=\frac\pi m\Delta f
=\frac{\lambda_{m0}}{2R}\Delta f.
$$

## 图件与依据

TikZ 图分别重绘光纤环路的反向光路和双层光纤端口。题干、公式和图形依据本题题面转写稿、答案公式核对表与图件核对入口。
