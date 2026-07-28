# 第38届复赛第5题：原子激光制冷与塞曼减速

## 题干整理

${}^{40}\mathrm K$ 原子束经准直后只有一个自由度。反向传播的单频减速激光使原子共振散射；随位置变化的磁场通过塞曼效应补偿多普勒失谐。给定

$$
\Gamma=5.00\times10^6\,\mathrm{s^{-1}},\quad
\lambda=670\,\mathrm{nm},\quad
\beta=-1.00\times10^{10}\,\mathrm{Hz/T}.
$$

![塞曼减速装置](assets/CPHO38-Q05-figure5a.png)

## 解析整理

### 1. 初始方均根速率

一维能量均分给出

$$
\frac12mv_0^2=\frac12k_\mathrm BT.
$$

对 $T=623\,\mathrm K$、$m=6.64\times10^{-26}\,\mathrm{kg}$，

$$
\boxed{v_0=360\,\mathrm{m/s}}.
$$

### 2. 共振减速

每个吸收光子提供动量 $h/\lambda$，因此

$$
a=\frac{\Gamma h}{\lambda m}=7.45\times10^4\,\mathrm{m/s^2},
\qquad
\boxed{s=\frac{v_0^2}{2a}=0.87\,\mathrm m}.
$$

### 3. 多普勒补偿量

相向运动、$v\ll c$ 时

$$
\Delta f=f_0-f=\frac{v}{\lambda}.
$$

所以初始速率下激光应降低

$$
\boxed{\Delta f=537\,\mathrm{MHz}}.
$$

### 4. 塞曼磁场函数

恒减速度下

$$
v(z)=\sqrt{v_0^2-2az}.
$$

由 $B(0)=0$ 及 $f_0(B)=f_0(0)+\beta B$，

$$
\boxed{B(z)=0.0537\left(1-\sqrt{1-1.15z}\right)\,\mathrm T}.
$$

其中 $z$ 的单位为米，$0\le z\le0.869\,\mathrm m$，$0\le B\le0.0537\,\mathrm T$。

## 图件与依据

题干依据 `CPHO38-Q05_transcription_v1.md`；公式依据 `CPHO38-Q05_formula_check_v1.csv` 与答案第12至14页。图5a由TikZ重绘。
