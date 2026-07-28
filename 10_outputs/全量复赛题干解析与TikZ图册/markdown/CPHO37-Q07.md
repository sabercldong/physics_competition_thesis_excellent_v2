# 第37届复赛第7题：LIGO双黑洞引力波辐射估算

## 题干整理
将质量为 $M$、$m$ 的双黑洞视为绕共同质心旋近的质点系统。题目要求用量纲分析建立功率模型，并根据能量损失求一圈时间和间距减半时的转角。

## 解析整理
$$P=\alpha GI^\lambda\omega^\xi c^\sigma,$$
$$P=\frac{\alpha GI^2\omega^6}{c^5}.$$
$$\omega^2=\frac{G(M+m)}{L^3},\qquad I=\frac{Mm}{M+m}L^2.$$
$$\omega^{-11/3}\frac{\mathrm d\omega}{\mathrm dt}=\frac{3\alpha G^{5/3}Mm}{c^5(M+m)^{1/3}}.$$

一圈时间为
$$
t_{360^\circ}=\frac{c^5L_0^4}{8\alpha G^3Mm(M+m)}
\left\{1-\left[1-\frac{10\pi\alpha G^{5/2}Mm\sqrt{M+m}}{c^5L_0^{5/2}}\right]^{8/5}\right\}.
$$

间距减半时的转角为
$$
\Delta\theta=\frac{(1-\sqrt2/8)c^5L_0^{5/2}}{5\alpha G^{5/2}Mm\sqrt{M+m}}\frac{180^\circ}{\pi}.
$$

## 图件与依据
TikZ 图重绘双黑洞、质心、间距与旋近方向。功率表达式仅用于题设的近似模型，不视为完整广义相对论结论。
