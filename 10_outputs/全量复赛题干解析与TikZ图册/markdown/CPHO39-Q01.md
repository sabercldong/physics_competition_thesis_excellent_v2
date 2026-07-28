# 第39届复赛第1题：迈克尔逊干涉仪的相位突变与折射率测量

## 题干整理

迈克尔逊干涉仪以单色激光照明，反射臂与透射臂相互垂直。开始时中心为亮斑、最外侧为亮圆环，共有20个亮条纹。移动一个反射镜后，中心与最外侧的明暗变化周期数分别为23和20。半反半透镜的两束反射光因反射界面不同有相位突变差 $\Delta\varphi$。

![迈克尔逊干涉仪与石英槽](assets/CPHO39-Q01-figures.png)

求相位突变差、移动后的亮条纹数，以及用 $\lambda=633\,\mathrm{nm}$、$t=2.00\,\mathrm{mm}$、$\theta=5.00^\circ$ 和 $\Delta N=17-10$ 测得的待测液体折射率。

## 解析整理

### 1. 条纹数与相位突变

$$
\cos\gamma_M=\frac{20}{23},\qquad
\Delta d=\frac{23}{2}\lambda,
$$

$$
2d=145\frac23\lambda,\qquad
\boxed{\Delta\varphi=\frac{2\pi}{3}\pmod{2\pi}}.
$$

### 2. 移动后的亮条纹数

$$
\frac{2\pi}{\lambda}2(d-\Delta d)(1-\cos\gamma_M)=(m-1)2\pi,
\qquad \boxed{m=17}.
$$

### 3. 石英槽倾斜测折射率

![折射路径](assets/CPHO39-Q01-solution-refraction.png)

折射定律为 $\sin\theta=n\sin i$。答案给出的有液体与空槽的光程差为

$$
\Delta L(\theta)=2nt\sqrt{1-\frac{\sin^2\theta}{n^2}}-2t\cos\theta.
$$

取 $\Delta N=7$ 并作小角度展开：

$$
\boxed{n=\frac{t\sin^2\theta}{2t(1-\cos\theta)-\lambda\Delta N}=1.41}.
$$

## 图件与依据

题干依据 `CPHO39-Q01.md` 第1页；公式依据 `CPHO39-Q01_formula_check_v1.csv` 与答案第5至6页。第一幅图重绘原题图1a和1b，第二幅图重绘答案解题图1a。
