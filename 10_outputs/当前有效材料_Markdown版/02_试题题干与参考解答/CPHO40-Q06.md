> 本文件由项目已校订的LaTeX题干、参考解答和TikZ图件生成。评分时以本文件为主要阅读文本；需核对原始措辞时查看包内对应届次原始PDF。

# 第40届复赛第6题：交变磁场中导体球涡电流悬浮与热效应

## 题干

半径 $b$ 的圆线圈置于水平面，电流 $I(t)=I_0\cos\omega t$。重量 $G$、半径 $a$、电导率 $\sigma$ 的导体球球心在线圈轴线上方 $h$ 处，且 $\delta\ll a\ll b$。求理想导体球磁矩和面电流、球心磁场、悬浮所需 $I_0$ 与平均焦耳热功率。

![CPHO40-Q06-structure](图件/CPHO40-Q06-structure.png)

## 参考解答整理

#### （1）理想导体球的磁矩与面电流。

理想导体球内总磁场为零，故 $$\boxed{\boldsymbol m=-\frac{2\pi a^3}{\mu_0}\boldsymbol B_e,\qquad \boldsymbol i=-\frac{3B_e}{2\mu_0}\sin\theta\,\hat{\boldsymbol\phi}.}$$

#### （2）线圈在球心处产生的磁场。

线圈轴线上球心处 $$B_0=\frac{\mu_0I_0b^2}{2(b^2+h^2)^{3/2}}.$$

#### （3）导体球悬浮所需的电流振幅。

周期平均安培力平衡给出 $$\boxed{I_0=\sqrt{\frac{4G(b^2+h^2)^4}{3\pi a^3b^4\mu_0h}}}.$$

#### （4）涡电流的周期平均热功率。

用趋肤层均匀体电流近似并消去 $\delta$，平均热功率为 $$\boxed{\overline P=\frac{3\pi a^2b^4I_0^2}{8(b^2+h^2)^3}\sqrt{\frac{2\omega\mu_0}{\sigma}}}.$$
