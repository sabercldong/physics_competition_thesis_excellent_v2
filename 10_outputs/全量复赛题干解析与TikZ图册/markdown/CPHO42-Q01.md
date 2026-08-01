> 本文件由项目已校订的LaTeX题干、参考解答和TikZ图件生成。评分时以本文件为主要阅读文本；需核对原始措辞时查看包内对应届次原始PDF。

# 第42届复赛第1题：磁光阱原子气的自由下落测温

## 题干

磁光阱中 $N$ 个原子组成温度为 $T$ 的平衡原子气。撤去陷阱后，位于正下方 $z=h$ 的探测器测量纵向数密度和向下通过该平面的净原子流。（1）求撤除前完整的玻尔兹曼分布；（2）求撤除后纵向数密度 $n(t)$ 和原子流 $I(t)$；（3）在低温、强约束极限下求两个观测量峰值对应的时间 $t_n$、$t_I$；（4）求 $n(t)$ 在峰值附近高斯分布的有效展宽 $\sigma_t$。题面没有独立题图；下图为解析辅助图。

![CPHO42-Q01-solution-release](assets/CPHO42-Q01-solution-release.png)

## 参考解答整理

#### （1）撤除前的完整分布。

撤除前的归一化分布函数为 $$\begin{aligned}
f(\boldsymbol r,\boldsymbol v)={}&N\left(\frac{m}{2\pi k_BT}\right)^3\omega_x\omega_y\omega_z
\exp\left[-\frac{m(\omega_x^2x^2+\omega_y^2y^2+\omega_z^2z^2)}{2k_BT}\right]\\
&\times\exp\left[-\frac{m(v_x^2+v_y^2+v_z^2)}{2k_BT}\right].
\end{aligned}$$

#### （2）撤除后的数密度与原子流。

撤除后，对在 $z=h$ 平面被测到的原子反推其初始位置和初始速度，再完成横向变量积分，得到纵向数密度 $$n(t)=N\left[\frac{m\omega_z^2}{2\pi k_BT(1+\omega_z^2t^2)}\right]^{1/2}
\exp\left[-\frac{m\omega_z^2(h-gt^2/2)^2}{2k_BT(1+\omega_z^2t^2)}\right],$$ 以及由上至下的原子流 $$I(t)=n(t)\left[gt+\frac{\omega_z^2t(h-gt^2/2)}{1+\omega_z^2t^2}\right].$$

#### （3）低温、强约束极限下的峰值时间。

在强约束极限，$\omega_i\to\infty$，数密度化为 $$n(t)\simeq N\left(\frac{m}{2\pi k_BT}\right)^{1/2}\frac1t
\exp\left[-\frac{m(h-gt^2/2)^2}{2k_BTt^2}\right].$$ 数密度和原子流的峰值时间在温度的非零最低阶相同： $$t_n=t_I=\left(1-\frac{k_BT}{2mgh}\right)\sqrt{\frac{2h}{g}}.$$

#### （4）峰值附近的有效时间展宽。

在 $t=t_n$ 附近，$n(t)$ 的对数二阶导数满足 $$\left.\frac{d^2\ln n}{dt^2}\right|_{t_n}\simeq-\frac{mg^2}{k_BT},$$ 与高斯峰形比较可得有效展宽 $$\boxed{\sigma_t=\sqrt{\frac{k_BT}{mg^2}}}.$$
