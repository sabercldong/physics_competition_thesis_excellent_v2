> 本文件由项目已校订的LaTeX题干、参考解答和TikZ图件生成。评分时以本文件为主要阅读文本；需核对原始措辞时查看包内对应届次原始PDF。

# 第41届复赛第5题：Ioffe磁阱与蒸发冷却

## 题干

四根无限长直导线穿过边长为 $a$、$b$ 的长方形四个顶点，电流大小均为 $I$，方向如图5a。（1）以中心 $O$ 为原点，求 $O$ 点及原点附近 $P(x,y,0)$ 点的磁场，并将可作小量近似的结果保留至领头阶。（2）把原子磁矩视为微小电流圈，证明其在磁场中的势能为 $W_m=-\boldsymbol S\cdot\boldsymbol B$。（3）当磁矩始终与局域磁场反向时，求原子所受磁场力。（4）求均匀原子团的平均势能，并分析半径从 $R_1$ 缩至 $R_1/5$、密度保持不变的蒸发冷却过程。

![CPHO41-Q05-figure5a](图件/CPHO41-Q05-figure5a.png)

## 参考解答整理

#### （1）原点附近的磁场。

无限长直导线在距导线 $r$ 处产生 $B=\mu_0I/(2\pi r)$。由四根导线的对称性，$O$ 点磁场为零。对 $x\ll a$、$y\ll b$，答案给出原点附近的领头阶近似 $$B_x=-\frac{16\mu_0abI}{\pi(a^2+b^2)^2}x,\qquad B_y=\frac{16\mu_0abI}{\pi(a^2+b^2)^2}y,$$ $$B=\frac{16\mu_0abI}{\pi(a^2+b^2)^2}\sqrt{x^2+y^2}.$$

#### （2）磁矩在外磁场中的势能。

电流圈受到的磁力矩为 $\boldsymbol M=\boldsymbol S\times\boldsymbol B$。磁矩从参考方向转至夹角 $\theta$ 时，外力矩所做功的负值给出势能变化： $$W_m(\theta)-W_m(\pi/2)=-\int_{\pi/2}^{\theta}SB\sin\theta'\,\mathrm d\theta'
=-SB\cos\theta.$$ 取参考常量为零，即得 $$\boxed{W_m=-\boldsymbol S\cdot\boldsymbol B}.$$

#### （3）磁矩反向时的约束力。

本题通过实验使磁矩始终与磁场反向，故以 $O$ 为势能零点时 $$W_m=\frac{16\mu_0abIS}{\pi(a^2+b^2)^2}\sqrt{x^2+y^2},$$ 且约束力指向原点： $$F_x=-\frac{16\mu_0abIS}{\pi(a^2+b^2)^2}\frac{x}{\sqrt{x^2+y^2}},\qquad F_y=-\frac{16\mu_0abIS}{\pi(a^2+b^2)^2}\frac{y}{\sqrt{x^2+y^2}}.$$

#### （4）蒸发冷却前后的能量。

半径为 $R_1$ 的均匀原子团有 $N_1=n\pi R_1^2$；其总势能和平均势能分别为 $$E_1=\frac{32\mu_0abISn}{3(a^2+b^2)^2}R_1^3,\qquad \bar E_1=\frac{32\mu_0abIS}{3\pi(a^2+b^2)^2}R_1.$$ 冷却后 $R_2=R_1/5$，故 $N_2=N_1/25$、$E_2=E_1/125$、$\bar E_2=\bar E_1/5$。下图为解析辅助图，不是原题图。

![CPHO41-Q05-evaporation](图件/CPHO41-Q05-evaporation.png)
