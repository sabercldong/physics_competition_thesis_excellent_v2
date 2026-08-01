> 本文件由项目已校订的LaTeX题干、参考解答和TikZ图件生成。评分时以本文件为主要阅读文本；需核对原始措辞时查看包内对应届次原始PDF。

# 第36届复赛第5题：阶跃型光纤耦合与全反射

## 题干

阶跃型光纤内芯直径为 $50\,\mu\mathrm{m}$、折射率 $n_1=1.46$；玻璃外包层外径为 $125\,\mu\mathrm{m}$、折射率 $n_2=1.45$。现用直径 $D=3.00\,\mathrm{mm}$、折射率 $n=1.50$ 的微球透镜将氦氖激光器输出的圆柱形平行光束耦合入光纤，空气折射率 $n_0=1.00$，激光束轴、透镜球心和光纤轴重合，如图。求：（1）光纤端面的最大入射角；（2）平行光刚好会聚在光纤端面时，微球后表面顶点 $O$ 与端面的距离；（3）满足长距离传输条件的平行入射光束最大直径。

![CPHO36-Q05-figure1](assets/CPHO36-Q05-figure1.png)

## 参考解答整理

#### （1）端面最大入射角。

设端面最大入射角为 $\theta$，进入纤芯后的折射角为 $\alpha$。由端面折射和芯--包层界面的全反射临界条件， $$n_0\sin\theta=n_1\sin\alpha,
\qquad
n_1\cos\alpha=n_2.$$ 相应的端面折射与芯--包层全反射临界光线见图左图。 消去 $\alpha$，得 $$\sin\theta=\sqrt{\left(\frac{n_1}{n_0}\right)^2-\left(\frac{n_2}{n_0}\right)^2}
=\sqrt{1.46^2-1.45^2}\approx0.17.$$ 因此 $$\boxed{\theta_{\max}=\arcsin(0.17)\approx9.8^\circ.}$$

#### （2）微球后顶点到端面的距离。

对微球前表面，平行光经球面折射后的一次像距为 $$\frac{n_0}{o_1}+\frac{n}{i_1}=\frac{n-n_0}{r},
\qquad o_1=\infty,\quad r=\frac D2,$$ 故 $$i_1=\frac{nD}{2(n-n_0)}=4.5\,\mathrm{mm}.$$ 相对于后表面顶点 $O$，该像为虚物， $$o_2=i_1-D=\frac{(n-2n_0)D}{2(n-n_0)}=-1.50\,\mathrm{mm},
\qquad r_2=-\frac D2.$$ 再对后表面应用球面折射公式，得到二次像距 $$\boxed{i_2=\frac{(2n_0-n)D}{4(n-n_0)}=0.75\,\mathrm{mm}.}$$ 因此 $O$ 到光纤端面的距离为 $0.75\,\mathrm{mm}$。几何近轴解法同样给出 $OF=D/4=0.75\,\mathrm{mm}$。

![CPHO36-Q05-solution-figures](assets/CPHO36-Q05-solution-figures.png)

#### （3）可耦合的最大光束直径。

微球的等效焦距为 $$f_e=\frac{nD}{4(n-n_0)}=2.25\,\mathrm{mm}.$$ 当边缘光线在光纤端面的入射角恰为 $\theta_{\max}$ 时，利用近轴几何关系（忽略 $O[(d/D)^3]$ 项）有 $$d_{\max}=\frac{nD\sin\theta_{\max}}{2(n-n_0)}.$$ 代入参数， $$\boxed{d_{\max}=0.76\,\mathrm{mm}.}$$ 故平行入射激光束的直径不能超过 $0.76\,\mathrm{mm}$。
