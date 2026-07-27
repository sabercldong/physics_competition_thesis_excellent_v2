# 第36届复赛第7题：闪电、电离层光环与球形闪电模型

## 题干整理

雷电云上部带正电、下部带负电。题目依次讨论：圆柱雷电云的电势差、电荷和能量；云下方地表电场；云地闪电通道的直径与电荷密度；电离层底部光环的扩展速度；以及 $12\,\mathrm{km}$ 高空气球的悬浮体积。

## 解析整理

### 1. 雷电云的电学量

$$
C=\frac{\varepsilon_0\pi r^2}{d},
\qquad U=Ed=150\,\mathrm{MV},
$$

$$
Q=CU=26\,\mathrm C,
\qquad W=\frac12QU=2.0\times10^9\,\mathrm J.
$$

### 2. 地表电场

镜像点电荷近似下

$$
E=\frac{Q}{2\pi\varepsilon_0}\left[\frac1{(h+d)^2}-\frac1{h^2}\right]
\approx-3.5\,\mathrm{kV/m}.
$$

有限圆盘积分给出的更精确结果为

$$
E_{\rm 地面}\approx-2.8\,\mathrm{kV/m}.
$$

### 3. 闪电通道

$$
\eta=\frac Qh=4.2\times10^{-4}\,\mathrm{C/m},
$$

$$
D\approx\frac{\eta}{\pi\varepsilon_0E_{\rm 击穿}}=5.0\,\mathrm m,
$$

$$
\rho(r)=\frac{\varepsilon_0E_{\rm 击穿}}{r}.
$$

### 4. 电离层光环

$$
v_{\rm 环}=c\frac{\sqrt{OA^2+AB^2}}{AB}.
$$

当 $OA=80\,\mathrm{km}$、$AB=100\,\mathrm{km}$ 时，

$$
v_{\rm 环}=1.28c=3.8\times10^8\,\mathrm{m/s}.
$$

这是波前与电离层平面交线的几何扩展速度。

### 5. 高空气球

$$
V=\frac{m_{\rm 载荷}}{\rho_1-\rho_{\rm He}},
$$

$$
p=p_0\left(1-\frac{az}{T_0}\right)^{Mg/(aR)},
\qquad
\rho=\rho_0\left(1-\frac{az}{T_0}\right)^{Mg/(aR)-1}.
$$

在 $12\,\mathrm{km}$ 处，$\rho_1\approx0.31\,\mathrm{kg/m^3}$，所以

$$
V\approx3.8\times10^2\,\mathrm{m^3}.
$$

## 图件与依据

TikZ 图重绘雷电云电荷分布，并按第（4）问要求绘制电离层底部光环产生与扩展过程。题干、公式和图件依据 `CPHO36-Q07.md`、`CPHO36-Q07_formula_check_v1.csv`、题图核对入口及解题图页面。
