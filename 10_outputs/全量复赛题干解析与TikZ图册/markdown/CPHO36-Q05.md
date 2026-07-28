# 第36届复赛第5题：阶跃型光纤耦合与全反射

## 题干整理

内芯折射率 $n_1=1.46$、包层折射率 $n_2=1.45$ 的阶跃型光纤，采用直径 $D=3.00\,\mathrm{mm}$、折射率 $n=1.50$ 的微球透镜耦合空气中的平行激光束。空气折射率 $n_0=1.00$。求端面最大入射角、微球后顶点到光纤端面的距离，以及可耦合光束的最大直径。

## 解析整理

### 1. 最大入射角

![端面临界光线与微球两次折射几何](assets/CPHO36-Q05-solution-figures.png)

$$
n_0\sin\theta=n_1\sin\alpha,
\qquad
n_1\cos\alpha=n_2.
$$

$$
\sin\theta_{\max}=\sqrt{\left(\frac{n_1}{n_0}\right)^2-\left(\frac{n_2}{n_0}\right)^2}
=0.17,
$$

$$
\theta_{\max}\approx9.8^\circ.
$$

### 2. 焦点位置

前表面折射给出

$$
i_1=\frac{nD}{2(n-n_0)}=4.5\,\mathrm{mm}.
$$

后表面的虚物距与曲率半径为

$$
o_2=\frac{(n-2n_0)D}{2(n-n_0)}=-1.50\,\mathrm{mm},
\qquad r_2=-\frac D2.
$$

因此

$$
OF=i_2=\frac{(2n_0-n)D}{4(n-n_0)}=0.75\,\mathrm{mm}.
$$

### 3. 最大光束直径

$$
f_e=\frac{nD}{4(n-n_0)}=2.25\,\mathrm{mm}.
$$

近轴近似下

$$
d_{\max}=\frac{nD\sin\theta_{\max}}{2(n-n_0)}=0.76\,\mathrm{mm}.
$$

## 图件与依据

TikZ 图重绘平行激光束、微球透镜、焦点、芯层/包层与尺寸标注。题干、公式与图件依据 `CPHO36-Q05.md`、`CPHO36-Q05_formula_check_v1.csv` 和题图核对入口。
