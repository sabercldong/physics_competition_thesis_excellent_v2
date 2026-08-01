> 本文件由项目已校订的LaTeX题干、参考解答和TikZ图件生成。评分时以本文件为主要阅读文本；需核对原始措辞时查看包内对应届次原始PDF。

# 第36届复赛第7题：闪电、电离层光环与球形闪电模型

## 题干

雷电云中上部带正电、下部带负电，云地闪电把云底负电荷释放到地面，如图。题目依次给定圆柱形雷电云的均匀电场 $E=0.15\,\mathrm{MV/m}$、半径 $r=2.5\,\mathrm{km}$、高度 $d=1.0\,\mathrm{km}$；负电荷层距地 $h=6.0\,\mathrm{km}$；闪电通道总电荷 $2.5\,\mathrm C$ 和空气击穿阈值 $3.0\,\mathrm{MV/m}$；电离层底面高度约 $80\,\mathrm{km}$、光环半径 $100\,\mathrm{km}$；以及在 $12\,\mathrm{km}$ 高空悬浮 $50\,\mathrm{kg}$ 载荷的氦气球参数。求雷电云的电势差、电荷和能量，地表电场，闪电通道直径及电荷密度分布，电离层光环扩展速度和气球体积。

![CPHO36-Q07-figure1](assets/CPHO36-Q07-figure1.png)

## 参考解答整理

#### （1）圆柱雷电云的电学量。

将带电区域近似为平行板电容器，面积 $S=\pi r^2$，有 $$C=\frac{\varepsilon_0S}{d},\qquad U=Ed=150\,\mathrm{MV}.$$ 从而 $$\boxed{Q=CU=26\,\mathrm C,\qquad W=\frac12QU=2.0\times10^9\,\mathrm J.}$$

#### （2）云正下方的地表电场。

把地面看作平面导体，采用镜像法并先以点电荷近似，有 $$E=\frac{Q}{2\pi\varepsilon_0}\left[\frac1{(h+d)^2}-\frac1{h^2}\right]
\approx-3.5\,\mathrm{kV/m}.$$ 负号表示场方向垂直地面向上。将两电荷层按有限带电圆盘积分，可得到更精确的估算 $$\boxed{E_{\rm 地面}\approx-2.8\,\mathrm{kV/m}.}$$

#### （3）闪电通道尺度与径向电荷密度。

通道长度取 $h=6.0\,\mathrm{km}$ 时，线电荷密度 $$\eta=\frac Qh=4.2\times10^{-4}\,\mathrm{C/m}.$$ 通道外电场 $E(r')=\eta/(2\pi\varepsilon_0r')$。令柱面场达到击穿阈值，得通道直径 $$\boxed{D\approx\frac{\eta}{\pi\varepsilon_0E_{\rm 击穿}}=5.0\,\mathrm m.}$$ 对通道内同轴高斯柱面应用高斯定律，并忽略中心放电细路径的尺度， $$r\varepsilon_0E_{\rm 击穿}=\int_0^r r'\rho(r')\,\mathrm dr',$$ 故 $$\boxed{\rho(r)=\frac{\varepsilon_0E_{\rm 击穿}}{r}.}$$

#### （4）电离层底部光环。

无线电波自近地闪电点 $O$ 以球面波传播；波前掠过而不能进入电离层底面，交线形成向外扩展的光环，如图。设 $OA=80\,\mathrm{km}$、$AB=r$，则 $$\cos\theta=\frac{AB}{OB}=\frac{AB}{\sqrt{OA^2+AB^2}},
\qquad
v_{\rm 环}=\frac{c}{\cos\theta}
=c\frac{\sqrt{OA^2+AB^2}}{AB}.$$ 当 $AB=100\,\mathrm{km}$ 时， $$\boxed{v_{\rm 环}=1.28c=3.8\times10^8\,\mathrm{m/s}.}$$ 这是球面波与电离层平面的交线所呈现的几何扩展速度，并非物质或信息以超光速传播。

![CPHO36-Q07-figure2](assets/CPHO36-Q07-figure2.png)

#### （5）$12\,\mathrm{km}$高空气球体积。

悬浮条件为 $$m_{\rm 载荷}g+\rho_{\rm He}Vg=\rho_1Vg,
\qquad V=\frac{m_{\rm 载荷}}{\rho_1-\rho_{\rm He}}.$$ 温度递减关系 $T=T_0-az$（$a=5.0\times10^{-3}\,\mathrm{K/m}$）与静力平衡、理想气体状态方程共同给出 $$p=p_0\left(1-\frac{az}{T_0}\right)^{Mg/(aR)},
\qquad
\rho=\rho_0\left(1-\frac{az}{T_0}\right)^{Mg/(aR)-1}.$$ 在 $z=12\,\mathrm{km}$ 处取 $\rho_1\approx0.31\,\mathrm{kg/m^3}$，代入 $m_{\rm 载荷}=50\,\mathrm{kg}$、$\rho_{\rm He}=0.18\,\mathrm{kg/m^3}$，得到 $$\boxed{V\approx3.8\times10^2\,\mathrm{m^3}.}$$
