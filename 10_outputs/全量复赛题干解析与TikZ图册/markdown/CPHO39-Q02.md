# 第39届复赛第2题：通电螺线管弹簧的平衡与等效劲度

## 题干整理

将原长 $l_0$、劲度系数 $k$ 的长直弹簧视作 $N$ 匝、半径 $r$ 的均匀密绕长直螺线管。比较恒流源保持 $I_0$ 与零电阻闭合回路初始电流为 $I'_0$ 两种条件下的平衡长度与等效劲度。

![两种通电条件](assets/CPHO39-Q02-spring-circuits.png)

原题与参考解答均没有独立图示；此图为依据题设条件绘制的解析辅助示意。

## 解析整理

### 1. 恒流条件

$$
B=\frac{\mu_0NI}{l},\qquad
L=\frac{\mu_0N^2\pi r^2}{l}.
$$

计入恒流源做功后的等效势能为

$$
W=\frac12k(l-l_0)^2-\frac{\mu_0N^2\pi r^2I_0^2}{2l}.
$$

于是

$$
\boxed{k(l_p-l_0)+\frac{\mu_0\pi N^2r^2I_0^2}{2l_p^2}=0},
$$

$$
\boxed{k_{\mathrm{eff}}=k-\frac{\mu_0\pi N^2r^2I_0^2}{l_p^3}},
$$

$$
\boxed{0\le I_0\le\sqrt{\frac{8kl_0^3}{27\mu_0\pi N^2r^2}}}.
$$

### 2. 零电阻闭合回路

磁通守恒：

$$
LI=L_0I'_0=\frac{\mu_0\pi N^2r^2}{l_0}I'_0.
$$

因此

$$
\boxed{l'_p=l_0-\frac{\mu_0\pi N^2r^2I_0'^2}{2kl_0^2},\qquad k'_{\mathrm{eff}}=k}.
$$

## 图件与依据

题干依据 `CPHO39-Q02.md` 第2页；公式依据 `CPHO39-Q02_formula_check_v1.csv` 与答案第6至8页。原题与答案没有独立图示，图件为解析辅助示意。
