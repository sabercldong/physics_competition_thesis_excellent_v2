# 第35届复赛第5题：塞曼效应的经典解释

## 题干整理

钠光 D 线在磁场中会分裂为三条。设原子中的价电子质量为 $m$、电荷量为 $-e$（$e>0$），受到等效线性回复力

$$
\boldsymbol F_{\mathrm r}=-m\omega_0^2\boldsymbol r.
$$

电子的固有圆频率为 $\omega_0$。外加磁场沿 $z$ 轴正方向，磁感应强度写为

$$
B=\frac{2m}{e}\omega_L.
$$

要求选择转动参考系导出电子运动，变换回实验室系，并说明弱磁场下谱线的三重分裂及相邻频率间隔。

## 解析整理

### 1. 旋转参考系

实验室系中的动力学方程是

$$
m\boldsymbol a=-m\omega_0^2\boldsymbol r-e\boldsymbol v\times\boldsymbol B.
$$

取绕 $z$ 轴、角速度为 $\boldsymbol\omega=\omega_L\boldsymbol k'$ 的转动系。用

$$
\boldsymbol r=\boldsymbol r',\qquad
\boldsymbol v=\boldsymbol\omega\times\boldsymbol r'+\boldsymbol v'
$$

处理离心力和科里奥利力后，得到

$$
\ddot x'=-(\omega_0^2+\omega_L^2)x',\quad
\ddot y'=-(\omega_0^2+\omega_L^2)y',\quad
\ddot z'=-\omega_0^2z'.
$$

令 $\Omega=\sqrt{\omega_0^2+\omega_L^2}$，则

$$
x'=A_1\cos(\Omega t+\varphi_1),\quad
y'=A_2\sin(\Omega t+\varphi_2),\quad
z'=A_3\cos(\omega_0t+\varphi_3).
$$

### 2. 实验室系

坐标变换为

$$
x=x'\cos\omega_Lt-y'\sin\omega_Lt,\quad
y=x'\sin\omega_Lt+y'\cos\omega_Lt,\quad z=z'.
$$

合并同频项后，

$$
\begin{aligned}
x&=A_+\cos(\omega_+t+\varphi_+)+A_-\cos(\omega_-t+\varphi_-),\\
y&=A_+\sin(\omega_+t+\varphi_+)-A_-\sin(\omega_-t+\varphi_-),\\
z&=A_3\cos(\omega_0t+\varphi_3),
\end{aligned}
$$

其中

$$
\omega_\pm=\sqrt{\omega_0^2+\omega_L^2}\pm\omega_L.
$$

### 3. 塞曼三重分裂

电子运动中出现 $\omega_+$、$\omega_0$、$\omega_-$ 三种圆频率，因此原谱线分裂为三条。弱磁场 $\omega_L\ll\omega_0$ 时，

$$
\omega_\pm\simeq\omega_0\pm\omega_L,
\qquad
\omega_+-\omega_0=\omega_0-\omega_-=\omega_L.
$$

## 图件与依据

原题无题图，不补画非原题图形。题干与公式依据 CPHO35-Q05.md 和 CPHO35-Q05_formula_check_v1.csv；当前 PDF 未明示分值。
