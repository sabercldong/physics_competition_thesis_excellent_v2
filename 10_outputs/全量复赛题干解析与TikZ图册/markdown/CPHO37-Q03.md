# 第37届复赛第3题：负微分电阻RLC振荡电路

## 题干整理

隧道二极管在特定电压范围内具有负微分电阻 $-R_0$。它与 $R$、$L$、$C$ 组成左侧交流回路，并通过理想扼流圈接入直流源。给定 $i(0)=0$、$\dot i(0)=\beta$，求一般电流、谐振和阻尼条件及最大平均功率。

## 解析整理

### 1. 特征根

$$
L\lambda^2+(R-R_0)\lambda+\frac1C=0,
$$

$$
\lambda_\pm=-\frac{R-R_0}{2L}
\pm\sqrt{\left(\frac{R-R_0}{2L}\right)^2-\frac1{LC}}.
$$

$$
i(t)=\frac{\beta}{2\sqrt{[(R-R_0)/(2L)]^2-1/(LC)}}
\left(e^{\lambda_+t}-e^{\lambda_-t}\right).
$$

### 2. 谐振

$$
R=R_0,
$$

$$
i_H(t)=\beta\sqrt{LC}\sin\frac{t}{\sqrt{LC}},
\qquad f_H=\frac1{2\pi\sqrt{LC}}.
$$

### 3. 阻尼振荡

$$
R_0<R<R_0+2\sqrt{\frac LC},
$$

$$
i_D(t)=\frac{\beta e^{-(R-R_0)t/(2L)}}{\sqrt{1/(LC)-[(R-R_0)/(2L)]^2}}
\sin\left(\sqrt{\frac1{LC}-\left[\frac{R-R_0}{2L}\right]^2}\,t\right),
$$

$$
f_D=\frac1{2\pi}\sqrt{\frac1{LC}-\left[\frac{R-R_0}{2L}\right]^2}.
$$

### 4. 最大平均功率

$$
V_0=\frac{V_{\max}+V_{\min}}2,
\qquad V_{D\max}=\frac{V_{\max}-V_{\min}}2,
$$

$$
\bar P_{\max}=\frac{(V_{\max}-V_{\min})^2}{8R_0}.
$$

## 图件与依据

TikZ 图重绘 RLC 回路、负微分电阻二极管、扼流圈和直流源。题干、公式和图件依据 `CPHO37-Q03.md`、`CPHO37-Q03_formula_check_v1.csv` 和题图核对入口。
