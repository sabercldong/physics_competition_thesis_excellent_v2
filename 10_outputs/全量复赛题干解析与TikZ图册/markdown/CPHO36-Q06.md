# 第36届复赛第6题：π介子衰变与μ子相对论寿命

## 题干整理

高速 π 介子发生

$$
\pi\rightarrow\mu+\bar\nu_\mu.
$$

给定 $m_\pi=139.57061\,\mathrm{MeV}/c^2$、$m_\mu=105.65837\,\mathrm{MeV}/c^2$、母粒子实验室系速度 $v=0.965c$。求衰变后 μ 子的速度范围，并求其自 $10000\,\mathrm{m}$ 高空飞向地面时的最大存活概率。

## 解析整理

### 1. 母粒子静止系中的速度

动量和能量守恒给出

$$
\boldsymbol p'_\mu+\boldsymbol p'_{\bar\nu}=0,
\qquad
E'_\mu+E'_{\bar\nu}=m_\pi c^2.
$$

反中微子质量忽略时

$$
u'_\mu=\frac{m_\pi^2-m_\mu^2}{m_\pi^2+m_\mu^2}c=0.2714c.
$$

### 2. 实验室系速度范围

$$
u_{\mu,\max}=\frac{u'_\mu+v}{1+u'_\mu v/c^2}=0.980c
=2.94\times10^8\,\mathrm{m/s},
$$

$$
u_{\mu,\min}=\frac{-u'_\mu+v}{1-u'_\mu v/c^2}=0.940c
=2.82\times10^8\,\mathrm{m/s}.
$$

### 3. 最大存活概率

最大速度给出最短飞行时间：

$$
(\Delta t)_{\min}=\frac{10000}{0.980\times3.00\times10^8}
=3.40\times10^{-5}\,\mathrm{s}.
$$

地面系半衰期为

$$
T_{1/2}=\frac{T_{1/2}^{(0)}}{\sqrt{1-u_{\mu,\max}^2/c^2}}
=0.765\times10^{-5}\,\mathrm{s}.
$$

所以

$$
P_{\max}=2^{-(\Delta t)_{\min}/T_{1/2}}
=0.0459\approx4.59\%.
$$

使用平均寿命 $\tau_0=T_{1/2}^{(0)}/\ln2$ 的指数衰变形式，可得到 $4.55\%$ 至 $4.59\%$ 的等价结果。

## 图件与依据

原题无题图，不补画非原题图形。题干与公式依据 `CPHO36-Q06.md` 和 `CPHO36-Q06_formula_check_v1.csv`。
