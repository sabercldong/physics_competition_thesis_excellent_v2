# 第37届复赛第4题：回旋加速器与反质子产生阈能

## 题干整理

Tevatron 的最大回旋轨道周长为 $L_{\max}=6436\,\mathrm m$，质子最大总能量为 $E_{p,\max}=1.00\times10^6\,\mathrm{MeV}$。求将质子加速到该能量所需的最小磁场；再求固定靶反应

$$
p+p\longrightarrow p+p+p+\bar p
$$

产生反质子所需的最小入射动能。

## 解析整理

### 1. 最小磁场

相对论动量与轨道半径满足

$$
B=\frac{p}{eR},\qquad R\leqslant\frac{L_{\max}}{2\pi},
$$

并且

$$
E_p^2=p^2c^2+m_p^2c^4.
$$

所以

$$
B_{\min}=\frac{2\pi}{eL_{\max}c}
\sqrt{E_{p,\max}^2-m_p^2c^4}=3.26\,\mathrm T.
$$

### 2. 反质子产生阈能

反应前系统的不变质量为

$$
M^2=\left(\frac{E_1+m_pc^2}{c^2}\right)^2-\left(\frac{p_1}{c}\right)^2
=\frac{2m_pE_1}{c^2}+2m_p^2.
$$

阈值处四个末态粒子在质心系中没有相对动能，因此

$$
M^2=(4m_p)^2.
$$

于是

$$
E_{1,\min}=7m_pc^2=6568.1\,\mathrm{MeV},
$$

$$
K_{1,\min}=E_{1,\min}-m_pc^2
=6m_pc^2=5629.8\,\mathrm{MeV}.
$$

Tevatron 的最大总能量远高于阈值，因而能够产生反质子。

## 图件与依据

原题无题图，不补画非原题图形。题干与公式依据 `CPHO37-Q04_transcription_v1.md` 和 `CPHO37-Q04_formula_check_v1.csv`。
