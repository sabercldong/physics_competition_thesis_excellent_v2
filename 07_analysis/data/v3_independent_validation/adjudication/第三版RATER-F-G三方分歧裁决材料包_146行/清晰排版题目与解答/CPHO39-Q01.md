> 本文件由项目已校订的LaTeX题干、参考解答和TikZ图件生成。评分时以本文件为主要阅读文本；需核对原始措辞时查看包内对应届次原始PDF。

# 第39届复赛第1题：迈克尔逊干涉仪的相位突变与折射率测量

## 题干

迈克尔逊干涉仪的光路如图（a）所示。单色激光经半反半透镜分为相互垂直的反射臂与透射臂，两臂端各有可沿臂移动的反射镜。两束返回光在空间重叠；对发散光源，观察到同心圆环条纹。开始时，中心为亮斑，最外侧为亮圆环，共有 $20$ 个亮条纹（计及中心亮斑）。缓慢移动一个反射镜后，圆环变稀疏；中心明暗变化 $23$ 个周期，最外侧明暗变化 $20$ 个周期。

半反半透镜由石英基板和金属膜构成；两束反射光因反射界面不同有相位突变差 $\Delta\varphi$。求：（1）$\Delta\varphi$；（2）移动后亮条纹数；（3）将内壁间距 $t=2.00\,\mathrm{mm}$ 的扁平石英槽置入一个臂，先使槽面相对臂转过 $\theta=5.00^\circ$，空槽时中心变化 $10$ 个周期；注入待测液体后再将石英槽复位，中心变化 $17$ 个周期。已知 $\lambda=633\,\mathrm{nm}$、空气折射率为 $1.00$，求液体折射率。

![CPHO39-Q01-figures](图件/CPHO39-Q01-figures.png)

## 参考解答整理

#### （1）由条纹周期确定相位突变。

设初始两臂光学长度差为 $d$，最大倾角为 $\gamma_M$。中心和最外侧均为亮纹，分别有 $$\frac{2\pi}{\lambda}2d+\Delta\varphi=2k\pi,\qquad
\frac{2\pi}{\lambda}2d\cos\gamma_M+\Delta\varphi=2(k-19)\pi.$$ 反射镜移动 $\Delta d$ 后，中心与最外侧的条纹变化给出 $$\frac{2\pi}{\lambda}2\Delta d=23\times2\pi,\qquad
\frac{2\pi}{\lambda}2\Delta d\cos\gamma_M=20\times2\pi.$$ 因而 $\cos\gamma_M=20/23$、$\Delta d=23\lambda/2$，并由初始条纹数得到 $$2d=\frac{23\times19}{3}\lambda=145\frac23\lambda.$$ 代回中心亮纹条件，得到 $$\boxed{\Delta\varphi=\frac{2\pi}{3}\pmod{2\pi}.}$$

#### （2）移动后的亮条纹数。

仍以中心和最外侧为亮纹，设亮条纹总数为 $m$，则 $$\frac{2\pi}{\lambda}2(d-\Delta d)(1-\cos\gamma_M)=(m-1)2\pi,$$ 故 $\boxed{m=17}$。

#### （3）由倾斜石英槽的光程差求折射率。

图画出答案使用的折射路径。设液体折射率为 $n$、折射角为 $i$，折射定律为 $$\sin\theta=n\sin i.$$ 与空槽相比，光线在倾角 $\theta$ 下往返通过石英槽的光程差为 $$\Delta L(\theta)=2nt\sqrt{1-\frac{\sin^2\theta}{n^2}}-2t\cos\theta.$$ 将其同 $\theta=0$ 的结果比较，并用 $\Delta N=N_2-N_1=17-10=7$，有 $$2nt\left(1-\sqrt{1-\frac{\sin^2\theta}{n^2}}\right)-2t(1-\cos\theta)=-\lambda\Delta N.$$ 题解按小角度展开，得到 $$\boxed{n=\frac{t\sin^2\theta}{2t(1-\cos\theta)-\lambda\Delta N}=1.41.}$$

![CPHO39-Q01-solution-refraction](图件/CPHO39-Q01-solution-refraction.png)
