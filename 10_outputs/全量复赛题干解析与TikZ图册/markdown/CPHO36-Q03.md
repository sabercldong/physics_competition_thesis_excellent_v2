# 第36届复赛第3题：电磁轨道炮加速模型

## 题干整理

两根半径为 $b$、长度为 $L$、单位长度电阻为 $\lambda$ 的平行圆柱导轨，与水平面夹角为 $\theta$；导轨间最近距离为 $d$。质量为 $m$、直径为 $d$、电阻为 $R$ 的薄片状弹丸在两导轨间良好接触。系统由电流为 $I$ 的理想恒流源供电，忽略摩擦、空气阻力和电源内部损耗。求安培力、出射速度、电源电压、电源做功，以及无电阻水平导轨时的能量比。

## 解析整理

### 1. 安培力

弹丸上距导轨轴线 $r'$ 处的磁感应强度为

$$
B=\frac{\mu_0 I}{4\pi r'}+\frac{\mu_0 I}{4\pi(d+2b-r')}.
$$

积分得到沿导轨向上的安培力

$$
F=\frac{\mu_0 I^2}{2\pi}\ln\frac{d+b}{b}.
$$

### 2. 出射速度

$$
a=\frac{\mu_0 I^2}{2\pi m}\ln\frac{d+b}{b}-g\sin\theta,
$$

$$
v_{\max}=\sqrt{2La}.
$$

### 3. 电源电压

设弹丸沿导轨的位置为 $l$，则

$$
\Phi=\frac{\mu_0 I l}{\pi}\ln\frac{d+b}{b},
\qquad
\varepsilon=-\frac{\mu_0 Iv}{\pi}\ln\frac{d+b}{b}.
$$

利用 $U+\varepsilon=2\lambda lI+IR$、$v=at$、$l=at^2/2$，有

$$
U=\lambda Iat^2+IR+\frac{\mu_0 I}{\pi}\ln\frac{d+b}{b}\,at.
$$

出射时 $T=\sqrt{2L/a}$，

$$
U_{\rm 出}=2\lambda IL+IR+\frac{\sqrt2\mu_0 I}{\pi}\ln\frac{d+b}{b}\sqrt{a}.
$$

### 4. 电源做功

$$
W=W_1+W_2+W_3,
$$

$$
W_1=\frac{2\sqrt2\lambda I^2}{3}L^{3/2}a^{-1/2},
\qquad
W_2=I^2R\sqrt{2L}\,a^{-1/2},
$$

$$
W_3=\frac{\mu_0 I^2L}{\pi}\ln\frac{d+b}{b}.
$$

### 5. 水平、无电阻极限

$$
E_{\max}=\frac{\mu_0 I^2L}{2\pi}\ln\frac{d+b}{b},
\qquad
W=\frac{\mu_0 I^2L}{\pi}\ln\frac{d+b}{b},
$$

$$
\eta=\frac{E_{\max}}W=50\%.
$$

## 图件与依据

TikZ 图重绘平行导轨、弹丸、恒流源、安培力方向、尺寸 $L,d,b$ 与倾角 $\theta$。题干、公式与图件依据 `CPHO36-Q03.md`、`CPHO36-Q03_formula_check_v1.csv` 和题图核对入口。
