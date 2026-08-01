> 本文件由项目已校订的LaTeX题干、参考解答和TikZ图件生成。评分时以本文件为主要阅读文本；需核对原始措辞时查看包内对应届次原始PDF。

# 第35届复赛第4题：Ioffe--Pritchard 磁阱

## 题干

四根通有恒定电流 $I$ 的长直导线垂直于 $x$--$y$ 平面，其与该平面的交点构成边长为 $2a$、中心为原点 $O$ 的正方形顶点。导线 $1,2,3,4$ 的坐标依次为 $(-a,a)$、$(a,a)$、$(a,-a)$、$(-a,-a)$，电流方向如图。装置还置于匀强磁场 $\boldsymbol B_0=B_0\boldsymbol k$ 中，$\boldsymbol k$ 为 $z$ 轴正方向单位矢量，真空磁导率为 $\mu_0$。

求：（1）四根导线在导线外产生的总磁场空间分布；（2）原点附近保留线性项的总磁场；（3）若原子的束缚势能 $V=\mu\lvert\boldsymbol B_{\mathrm{tot}}\rvert$，其中 $\mu>0$，求原点附近的磁场力；（4）原子最易从 $x$--$y$ 平面的何处逸出，并求刚好逸出的动能。

![CPHO35-Q04-figure1](assets/CPHO35-Q04-figure1.png)

## 参考解答整理

#### （1）四导线磁场的叠加。

取 $x$、$y$ 方向单位矢量为 $\boldsymbol i$、$\boldsymbol j$。导线外任一点 $(x,y)$ 处，四根导线分别产生 $$\begin{aligned}
\boldsymbol B_1&=\frac{\mu_0(-I)}{2\pi}\frac{-(y-a)\boldsymbol i+(x+a)\boldsymbol j}{(x+a)^2+(y-a)^2},&
\boldsymbol B_2&=\frac{\mu_0 I}{2\pi}\frac{-(y-a)\boldsymbol i+(x-a)\boldsymbol j}{(x-a)^2+(y-a)^2},\\
\boldsymbol B_3&=\frac{\mu_0(-I)}{2\pi}\frac{-(y+a)\boldsymbol i+(x-a)\boldsymbol j}{(x-a)^2+(y+a)^2},&
\boldsymbol B_4&=\frac{\mu_0 I}{2\pi}\frac{-(y+a)\boldsymbol i+(x+a)\boldsymbol j}{(x+a)^2+(y+a)^2}.
\end{aligned}$$ 因此导线电流产生的总磁场为 $$\boldsymbol B=\boldsymbol B_1+\boldsymbol B_2+\boldsymbol B_3+\boldsymbol B_4.$$

#### （2）原点附近的线性近似。

在 $|x|\ll a$、$|y|\ll a$ 的范围内，将上式保留至 $x/a$、$y/a$ 的一次项，得到 $$\boxed{\boldsymbol B\simeq\frac{\mu_0I}{\pi a^2}\left(x\boldsymbol i-y\boldsymbol j\right).}$$ 加上沿 $z$ 轴的偏置磁场后， $$\boldsymbol B_{\mathrm{tot}}\simeq\frac{\mu_0I}{\pi a^2}\left(x\boldsymbol i-y\boldsymbol j\right)+B_0\boldsymbol k.$$

#### （3）原点附近的束缚力。

磁感应强度大小的二阶展开为 $$\lvert\boldsymbol B_{\mathrm{tot}}\rvert
=\sqrt{B_0^2+\left(\frac{\mu_0I}{\pi a^2}\right)^2(x^2+y^2)}
\simeq B_0+\frac{1}{2B_0}\left(\frac{\mu_0I}{\pi a^2}\right)^2(x^2+y^2).$$ 于是势能及其负梯度为 $$V\simeq\mu B_0+\frac{\mu}{2B_0}\left(\frac{\mu_0I}{\pi a^2}\right)^2(x^2+y^2),
\qquad
\boxed{\boldsymbol F=-\frac{\mu}{B_0}\left(\frac{\mu_0I}{\pi a^2}\right)^2(x\boldsymbol i+y\boldsymbol j).}$$ 该力在 $x$--$y$ 平面内沿径向指向原点。

#### （4）逸出位置与阈值动能。

完整势能可写为 $$V=\mu\sqrt{B_0^2+\lvert\boldsymbol B\rvert^2}.$$ 在 $x$ 轴上取 $y=0$，有 $$V(x,0)=\mu\sqrt{B_0^2+\left(\frac{\mu_0Ia}{\pi}\right)^2
\left[\frac{1}{(x-a)^2+a^2}-\frac{1}{(x+a)^2+a^2}\right]^2}.$$ 由 $\mathrm dV/\mathrm dx=0$ 得 $x(3x^4-4a^4)=0$。原点为势能最小点；势垒顶点位于 $$\boxed{\left(\pm\left(\frac43\right)^{1/4}a,0\right),\qquad
\left(0,\pm\left(\frac43\right)^{1/4}a\right).}$$ 这些点给出原子在平面内最易逸出的四个方向。势垒高度对应的势能为 $$V_{\mathrm b}=\mu\sqrt{B_0^2+\frac{3\sqrt3}{8}\left(\frac{\mu_0I}{\pi a}\right)^2},
\qquad V_O=\mu B_0.$$ 故刚好逸出磁阱所需的最小动能为 $$\boxed{E_k=\mu B_0\left[\sqrt{1+\frac{3\sqrt3}{8}\left(\frac{\mu_0I}{\pi aB_0}\right)^2}-1\right].}$$
