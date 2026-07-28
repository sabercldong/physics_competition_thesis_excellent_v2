# 第38届复赛第8题：电动汽车电机与加速效率

## 题干整理

简化电动汽车在水平路面上加速，前、后轮各为半径 $r$、质量 $m$ 的均质圆柱，车身质量为 $M$。永磁直流电机的线圈在匀强磁场 $B$ 中转动，线圈轨迹半径为 $r_{\mathrm c}$、总电阻为 $R_{\text{总}}$；电机经变速比 $r_i$ 的变速器驱动后轮。

![电动汽车模型与电机特性](assets/CPHO38-Q08-figure8a.png)

## 解析整理

### 1. 力矩--转速关系

线圈受力矩、反电动势和电流为

$$
\tau=BIlr_{\mathrm c},\qquad
\varepsilon=B\omega r_{\mathrm c}l,\qquad
I=\frac{V-\varepsilon}{R_{\text{总}}}.
$$

因此输出力矩随转速线性降低：

$$
\boxed{\tau(\omega)=\tau_{\max}\left(1-\frac{\omega}{\omega_{\max}}\right)}.
$$

其中

$$
\boxed{P_{\max}=\frac{V^2}{4R_{\text{总}}},\quad
\omega_{\max}=\frac{V}{Br_{\mathrm c}l},\quad
\tau_{\max}=\frac{4P_{\max}}{\omega_{\max}}}.
$$

### 2. 车速随时间的关系

无滑动时

$$
\omega=\frac vr r_i,qquad
\tau_{\text{轮}}=\tau_{\max}\left(1-\frac{r_iv}{r\omega_{\max}}\right)r_i.
$$

由题给加速度关系可得

$$
\boxed{v(t)=v_{\max}\left(1-e^{-a_{\max}t/v_{\max}}\right)},
$$

$$
v_{\max}=\frac{r\omega_{\max}}{r_i},qquad
a_{\max}=\frac{\tau_{\max}r_i}{(M+3m)r}.
$$

### 3. A 型车的数值结果

题解给出

$$
\omega_{\max}=2.0\times10^3\,\mathrm{rad/s},\quad
v_{\max}=80\,\mathrm{m/s},\quad
a_{\max}=5.6\,\mathrm{m/s^2}.
$$

从静止加速至 $100\,\mathrm{km/h}$：

$$
\boxed{t_f=6.1\,\mathrm s},
$$

$$
\boxed{\Delta E_{\text{电池}}\approx4.0\times10^6\,\mathrm J
\approx1.1\,\mathrm{kWh},\qquad \eta\approx18\%}.
$$

## 图件与依据

题干依据 `CPHO38-Q08_transcription_v1.md`；公式依据 `CPHO38-Q08_formula_check_v1.csv` 与答案第18至20页。左图重绘原题图8a，右图是力矩--转速关系的辅助图。
