# 第35届复赛第8题：穆斯堡尔效应与共振吸收

## 题干整理

$^{57}\mathrm{Fe}$ 第一激发态与基态的能量差为 $E_0=2.31\times10^{-15}\,\mathrm J$，能级宽度参数为 $\Gamma=3.2\times10^{-13}E_0$。要求分析自由原子核发射、吸收时的反冲能与频移，判断静止原子核的共振吸收，并说明晶体中的无反冲共振如何测量 $10^{-10}$ 相对频率变化。

## 解析整理

### 1. 发射反冲

$$
E_0=h\nu_{\mathrm e}+\frac12m_{\mathrm{Fe}}v^2,\qquad
\frac{h\nu_{\mathrm e}}{c}=m_{\mathrm{Fe}}v.
$$

令 $\nu_0=E_0/h$，则

$$
\nu_{\mathrm e}-\nu_0\simeq-\nu_0\frac{E_0}{2m_{\mathrm{Fe}}c^2}
=-4.7\times10^{11}\,\mathrm{Hz},
$$

$$
E_{\mathrm R}=\frac{E_0^2}{2m_{\mathrm{Fe}}c^2}
=3.1\times10^{-22}\,\mathrm J.
$$

### 2. 吸收反冲

$$
h\nu_{\mathrm a}=E_0+\frac12m_{\mathrm{Fe}}v'^2,\qquad
\frac{h\nu_{\mathrm a}}{c}=m_{\mathrm{Fe}}v'.
$$

所以

$$
\nu_{\mathrm a}-\nu_0=4.7\times10^{11}\,\mathrm{Hz},
\qquad E'_{\mathrm R}=E_{\mathrm R}.
$$

### 3. 自由核不发生共振吸收

发射与吸收频率窗口重叠的必要条件为

$$
\Gamma>E_{\mathrm R}.
$$

但

$$
\frac{E_{\mathrm R}}{\Gamma}=4.2\times10^5,
$$

因此反冲能远大于能级宽度，两个静止自由核之间不能共振吸收。

### 4. 晶体中的速度补偿

晶体整体反冲可忽略，能量窗口为 $[E_0-\Gamma,E_0+\Gamma]$。小速度多普勒近似为

$$
\nu'\simeq\left(1+\frac{V}{c}\right)\nu.
$$

可发生共振吸收的范围是

$$
-0.19\,\mathrm{mm\,s^{-1}}\le V\le0.19\,\mathrm{mm\,s^{-1}}.
$$

若 $\Delta\nu/\nu_0=\pm10^{-10}$，以速度补偿频移：

$$
V'\simeq-\frac{\Delta\nu}{\nu_0}c,
\qquad
|V'|=3\,\mathrm{cm\,s^{-1}}.
$$

测得达到共振时的速度改变量，便可得到频率的微小变化。

## 图件与依据

原题无题图，不补画非原题图形。题干和公式依据 CPHO35-Q08.md 与 CPHO35-Q08_formula_check_v1.csv；当前 PDF 未明示分值。
