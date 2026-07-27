# 第37届复赛第1题：高铁空气弹簧劲度系数模型

## 题干整理

空气弹簧包含主气室、附加气室和阀门。平衡时主气室压强、体积为 $p_{10}$、$V_{10}$，附加气室体积为 $V_2$。有效承载面积为 $A_e$，向下位移为 $y$，并有

$$
\frac{\mathrm dV_1}{\mathrm dy}=-\alpha,
\qquad
\frac{\mathrm dA_e}{\mathrm dy}=\beta.
$$

求阀门关闭、打开时，在等温和绝热条件下的劲度系数。

## 解析整理

### 1. 统一关系

$$
F=(p_1-p_0)A_e,
\qquad p_1V_1^n=\text{常量},
$$

$$
K=\frac{\alpha n p_{10}V_{10}^n}{V_1^{n+1}}A_e
+\beta\left[p_{10}\left(\frac{V_{10}}{V_1}\right)^n-p_0\right].
$$

### 2. 阀门关闭

等温过程：

$$
K=\frac{\alpha p_{10}V_{10}}{V_1^2}A_e
+\beta\left(\frac{p_{10}V_{10}}{V_1}-p_0\right).
$$

绝热过程，$\gamma=7/5$：

$$
K=\frac{7\alpha p_{10}V_{10}^{7/5}}{5V_1^{12/5}}A_e
+\beta\left[p_{10}\left(\frac{V_{10}}{V_1}\right)^{7/5}-p_0\right].
$$

### 3. 阀门打开

低频时两气室整体等温：

$$
K=\frac{\alpha p_{10}(V_{10}+V_2)}{(V_1+V_2)^2}A_e
+\beta\left[\frac{p_{10}(V_{10}+V_2)}{V_1+V_2}-p_0\right].
$$

高频时附加气室来不及参与，结果仍为主气室绝热表达式。

## 图件与依据

TikZ 图重绘簧上负载、主气室、附加气室、阀门和位移方向。题干、公式和图件依据 `CPHO37-Q01.md`、`CPHO37-Q01_formula_check_v1.csv` 和题图核对入口。
