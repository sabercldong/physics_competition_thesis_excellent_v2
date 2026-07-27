# 第35届复赛第7题：弹簧衍射与DNA X射线衍射类比

## 题干整理

以波长 $633\,\mathrm{nm}$ 的激光照射小弹簧，在 $4.2\,\mathrm m$ 外的光屏得到衍射图样；以波长 $0.15\,\mathrm{nm}$ 的X射线照射DNA样品，在 $9.0\,\mathrm{cm}$ 外底片得到相似图样。根据图中测量信息，估算弹簧钢丝直径、弹簧半径与螺距，以及DNA双螺旋半径与螺距。

## 解析整理

### 1. 衍射周期

远场小角近似：

$$
d\sin\theta_n\simeq d\frac{x_n}{L}=n\lambda,
\qquad
X=x_{n+1}-x_n=\frac{\lambda L}{d}.
$$

图（a）中 $X_1=7.9\,\mathrm{mm}$、$X_2=1.7\,\mathrm{mm}$、$\phi=30^\circ$，因此

$$
d_1=\frac{\lambda L}{X_1}=0.34\,\mathrm{mm},\qquad
d_2=\frac{\lambda L}{X_2}=1.6\,\mathrm{mm}.
$$

### 2. 弹簧参数

$$
p=\frac{d_2}{\cos(\phi/2)}=1.6\,\mathrm{mm},
\qquad
R=\frac{d_2}{2\pi\sin(\phi/2)}=0.96\,\mathrm{mm}.
$$

### 3. DNA参数

图（b）中 $\phi'=84^\circ$、$X'=4.7\,\mathrm{mm}$。

$$
d'=\frac{\lambda'L'}{X'}=2.9\,\mathrm{nm},
$$

$$
p'=\frac{d'}{\cos(\phi'/2)}=3.9\,\mathrm{nm},
\qquad
R'=\frac{d'}{2\pi\sin(\phi'/2)}=0.68\,\mathrm{nm}.
$$

## 图件与依据

TikZ 图保留弹簧、交叉衍射条纹、DNA圆形衍射图样、尺寸基准和第4级亮纹缺失的结构信息，不使用原始照片。题干、公式和图件依据 CPHO35-Q07.md、CPHO35-Q07_formula_check_v1.csv 及图件核对入口；当前 PDF 未明示分值。
