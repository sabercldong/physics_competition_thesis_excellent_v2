# 第38届复赛第4题：两枚小永磁针的相互作用与平衡

## 题干整理

两枚小永磁针均可看作磁矩大小为 $\mu=IS$ 的小电流环，$S=\pi R^2$。磁针 $A$ 固定在原点，其磁矩沿 $+x$ 方向；磁针 $B$ 位于正下方 $(0,0,z)$，$z\gg R$，其磁矩与 $x$ 轴成 $\theta$ 角。竖直向下取为 $+z$ 方向。

![电流环磁矩与两磁偶极子相对位置](assets/CPHO38-Q04-figure4a.png)

## 解析整理

### 1. 相互作用势能

$A$ 在 $B$ 所在位置产生的远场为

$$
\mathbf B_A=-\frac{\mu_0\mu}{4\pi z^3}\mathbf e_x.
$$

因此

$$
\boxed{E_p=\frac{\mu_0\mu^2\cos\theta}{4\pi z^3}}.
$$

### 2. 稳定磁矩方向

固定 $z$ 时，

$$
V(\theta)=\frac{\mu_0\mu^2\cos\theta}{4\pi z^3}-mgz,
\qquad
M=-\frac{\mathrm dV}{\mathrm d\theta}
=\frac{\mu_0\mu^2\sin\theta}{4\pi z^3}.
$$

平衡候选为 $\theta=0$ 和 $\theta=\pi$。由于 $\theta=\pi$ 对应势能极小，

$$
\boxed{\theta_{\text{稳}}=\pi}.
$$

### 3. 竖直平衡位置

代入 $\theta=\pi$ 后，竖直方向合力为

$$
F=-\frac{3\mu_0\mu^2}{4\pi z^4}+mg.
$$

所以

$$
\boxed{z_0=\left(\frac{3\mu_0\mu^2}{4\pi mg}\right)^{1/4}}.
$$

在此处

$$
\frac{\mathrm d^2V}{\mathrm dz^2}=-\frac{3\mu_0\mu^2}{\pi z_0^5}<0,
$$

故竖直方向平衡不稳定。

## 图件与依据

题干依据 `CPHO38-Q04_transcription_v1.md`；公式依据 `CPHO38-Q04_formula_check_v1.csv` 与答案第10至12页。左侧电流环为原题图4a的TikZ重绘；右侧仅为题设相对位置的辅助示意。
