> 本文件由项目已校订的LaTeX题干、参考解答和TikZ图件生成。评分时以本文件为主要阅读文本；需核对原始措辞时查看包内对应届次原始PDF。

# 第38届复赛第8题：电动汽车电机与加速效率

## 题干

如图，简化电动汽车的前、后轮各合并视为半径 $r$、质量 $m$ 的均质圆柱刚体，刚体车身质量为 $M$，质心位于两轮轴中点。忽略空气阻力和车轴摩擦。永磁直流电机的动子线圈在匀强磁场 $B$ 中转动；线圈导线总长度为 $l$，转动轨迹半径为 $r_{\mathrm c}$，线圈电阻为 $R_{\text{线圈}}$，电池开路电压和内阻分别为 $V$、$R_{\text{内}}$。

求：（1）电机输出力矩 $\tau$ 与转速 $\omega$ 的关系、$\tau_{\max}$、$\omega_{\max}$ 及 $P_{\max}$；（2）变速比为 $r_i$、无滑动且变速器效率为 $100\%$ 时，车速 $v(t)$ 与时间的关系；（3）取 A 型车 $M=1.8\times10^3\,\mathrm{kg}$、$r=0.40\,\mathrm m$、$\tau_{\max}=4.0\times10^2\,\mathrm{N\,m}$、$r_i=10$、$P_{\max}=2.0\times10^2\,\mathrm{kW}$，求从静止加速至 $100\,\mathrm{km/h}$ 的时间、电池能量消耗及电能转化为机械能的效率。车轮质量相对车身质量可忽略，任一车轮组转动惯量 $J=mr^2/2$。

![CPHO38-Q08-figure8a](图件/CPHO38-Q08-figure8a.png)

## 参考解答整理

#### （1）永磁直流电机的力矩--转速关系。

令总电阻为 $R_{\text{总}}=R_{\text{内}}+R_{\text{线圈}}$。线圈受磁场力矩、反电动势和电流分别为 $$\tau=BIlr_{\mathrm c},\qquad
\varepsilon=B\omega r_{\mathrm c}l,\qquad
I=\frac{V-\varepsilon}{R_{\text{总}}}.$$ 因此 $$\tau(\omega)=\frac{Br_{\mathrm c}l\left(V-Br_{\mathrm c}l\omega\right)}{R_{\text{总}}}.$$ 输出功率 $P=\tau\omega$ 在 $Br_{\mathrm c}l\omega=V/2$ 时最大，从而 $$\boxed{P_{\max}=\frac{V^2}{4R_{\text{总}}},\qquad
\omega_{\max}=\frac{V}{Br_{\mathrm c}l},\qquad
\tau_{\max}=\frac{4P_{\max}}{\omega_{\max}}.}$$ 写成后续计算方便的形式， $$\boxed{\tau(\omega)=\tau_{\max}\left(1-\frac{\omega}{\omega_{\max}}\right).}$$

#### （2）车速随时间的演化。

无滑动时 $\omega_{\text{轮}}=v/r$，电机转速为 $$\omega=\omega_{\text{轮}}r_i=\frac vr r_i.$$ 变速器无功率损失，传给后轮的力矩为 $$\tau_{\text{轮}}=\tau r_i
=\tau_{\max}\left(1-\frac{r_iv}{r\omega_{\max}}\right)r_i.$$ 结合题给加速度关系 $a=(\tau_{\text{轮}}/r)/(M+3m)$，得到一阶微分方程，其解可写为 $$\boxed{v(t)=v_{\max}\left(1-\exp\left(-\frac{a_{\max}t}{v_{\max}}\right)\right),}$$ 其中 $$\boxed{v_{\max}=\frac{r\omega_{\max}}{r_i},\qquad
a_{\max}=\frac{\tau_{\max}r_i}{(M+3m)r}.}$$

#### （3）A 型车的时间、能耗和效率。

忽略车轮质量后， $$\omega_{\max}=\frac{4P_{\max}}{\tau_{\max}}
=2.0\times10^3\,\mathrm{rad/s},$$ $$v_{\max}=80\,\mathrm{m/s},\qquad
a_{\max}=5.6\,\mathrm{m/s^2}.$$ 目标速度 $v_f=100/3.6\,\mathrm{m/s}$ 对应的加速时间为 $$\boxed{t_f=-\frac{v_{\max}}{a_{\max}}
\ln\left(1-\frac{v_f}{v_{\max}}\right)=6.1\,\mathrm s.}$$ 电池瞬时功率为 $P_{\text{电池}}=4P_{\max}(1-v/v_{\max})$，积分得 $$\Delta E_{\text{电池}}
=\frac{4P_{\max}v_f}{a_{\max}}
\approx4.0\times10^6\,\mathrm J
\approx1.1\,\mathrm{kWh}.$$ 增加的机械能为 $\Delta E_{\text{机械能}}=\frac12(M+3m)v_f^2$，所以 $$\boxed{\eta=\frac{\Delta E_{\text{机械能}}}{\Delta E_{\text{电池}}}
=\frac{(M+3m)a_{\max}v_f}{8P_{\max}}
\approx18\%.}$$
