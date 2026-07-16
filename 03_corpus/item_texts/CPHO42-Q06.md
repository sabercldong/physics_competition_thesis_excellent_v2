# 第42届复赛第6题：转速仪刚体动力学模型

## 来源

- 试题文件：`03_corpus/raw_papers/cpho_42_2025_fusai_paper_candidate.pdf`
- 解答文件：`03_corpus/raw_solutions/cpho_42_2025_fusai_solution_candidate.pdf`
- 试题页码：4-5
- 解答页码：16-20
- 题图：03_corpus/item_assets/CPHO42-Q06-figure1-page4-raw.png
- 抽取状态：题干使用扫描页OCR并经视觉定位大题边界；参考解答使用PDF文本层抽取；题图按渲染页原图裁切，未去除来源/权属水印。题干OCR、公式、特殊符号、图注和图件边缘需人工校对。

## G1-07-A1 视觉校对转写入口

- 任务：`G1-07-A1-TRANSCRIBE-42Q06`
- 题面V1转写稿：`03_corpus/manual_review_transcripts/CPHO42-Q06_transcription_v1.md`
- 答案公式核对表：`03_corpus/manual_review_transcripts/CPHO42-Q06_formula_check_v1.csv`
- 页面证据：
  - `03_corpus/manual_review_renders/G1-07-A1/CPHO42-Q06-paper-page-4.png`
  - `03_corpus/manual_review_renders/G1-07-A1/CPHO42-Q06-paper-page-5.png`
  - `03_corpus/manual_review_renders/G1-07-A1/CPHO42-Q06-solution-page-16.png`
  - `03_corpus/manual_review_renders/G1-07-A1/CPHO42-Q06-solution-page-17.png`
  - `03_corpus/manual_review_renders/G1-07-A1/CPHO42-Q06-solution-page-18.png`
  - `03_corpus/manual_review_renders/G1-07-A1/CPHO42-Q06-solution-page-19.png`
  - `03_corpus/manual_review_renders/G1-07-A1/CPHO42-Q06-solution-page-20.png`
- 当前状态：原OCR文本仅保留为错误来源和追溯材料；正式编码前应以V1转写稿、公式核对表和页面证据作为复核入口。`CPHO42-Q06-FIG` 尚未销项；第（1.2）问轴承作用力长分式、第（2.1）问 `Omega_0` 根式、第（2.2）问小振动角频率和第（2.3）问一阶近似需重点最终复核。

## G1-07-C1 题图核对入口

- 任务：`G1-07-C1-FIG-42Q06`
- 题图核对表：`03_corpus/manual_review_transcripts/CPHO42-Q06_figure_check_v1.csv`
- 原始裁图：`03_corpus/item_assets/CPHO42-Q06-figure1-page4-raw.png`
- 重裁候选图：`03_corpus/item_assets/CPHO42-Q06-figure6a-page4-recrop-v1.png`
- 裁框定位图：`03_corpus/manual_review_renders/G1-07-C1/CPHO42-Q06-paper-page-4-figure6a-crop-box.png`
- 新旧对照接触图：`03_corpus/manual_review_renders/G1-07-C1/CPHO42-Q06-figure6a-check-contact-v1.png`
- 当前状态：原始裁图保留图6a主体、`z/x` 轴、轴承 `A/B`、两个 `h` 标注、小球 `a/b`、角度 `theta`、`O` 和图号，但顶部混入上一题参数残字；重裁候选图已去除顶部残字并保留关键图形信息。本入口仍不代表真实人工销项完成，论文或附录使用前需最终复核。

## 题干OCR抽取文本

```text
六、（45 分） 一转速仪的简化模型如图 6a 所示。竖直转轴底部由光滑地面支振，

并由固定的光滑轴承 A、B 约束。两灿承的厚度均可忽略，它们相虐 2 ，其中点       rs
为0。质量分别为上和ms 的小球 a 和 b(均可视为质点) 国定在质量为M、长 Gy |
为2/ 的匀质细杆的两端; 一光滑水平轴固定在竖直转轴的 O 点，细杆中心的小加      Sa
孔套在此水平负上，细杆可在它和转轴所在的平面内绕此水平轴转动。以 O 为原             ey
点、坚直向上为z轴正方向建立固定于地面的直角坐标系O30z，y》 轴重直于纸面     0 iI
向里《图中未画出)，x、)，z 方向的单位矢量分别记为e . @,. e, 。记 Oa 相对 ANYD
于z轴正方向的夹角为 。转轴上 O 处装有一轻质鼻先，可对细杆施加一大小为      eiffen
ko 的回复力矩，其中 为盘答的所转系数。重力加速度大小为&               |

《1 转速仪以某一角速度绕坚直转灿做匀束转动， 为某一固定值& (0<4<r SA

第4页，共5页

Aa, aa
2
(1.1)求转速仪做匀速转动的角速度 ©, » 并分别在 m, > m, Am, < m, 的情况下讨论实际存在此 ou It 6, AT
满足的条件，
〈1.2) 某时刻，细杆运动至如图 6a 所示的xz平面内，求此时转速仪相对 O 点的角动量工 以及轴承 A、
B 对转轴的作用力惟、互.

(2) Rim, = ma =z，初始时系统处于第〈1) 问中的稳定运动状态，某时刻〈记为! = 0 ) NER a 受到在细
杆和竖直转轴所在平面内、且垂直于细杆的冲击〈使8 增大)，此冲击作用时间极短。已知在此后的运动过
程中6 的最大值为 (& < <r)。

(21) 求小球 a 在受到冲击后的瞬间，8 的时间变化率 包 ;

(2.2) 当冲击足够小时，细杆可在鳃附近做小幅简谐振动，求振动的角频率 os +

(2.3) 15, =Oy-O (5 <<gb )，求!时刻转速仪绕竖直转轴转动的角速度 o(f) ，结果保留至名的一阶
项。
```

## 参考解答抽取文本

```text
六.（45 分）
（1）
   （1.1）在绕 z 轴以角速度 ω 0 匀速转动的参考系中，细杆在 θ0 位置处于平衡状态，有力矩平衡方程（以
θ 增大方向为正）

                                                                                        16
                                           − kθ 0 + m1 gl sin θ 0 − m 2 gl sin θ 0 + M 离 = 0                                   ①
其中惯性离心力的力矩
                                                                                  dr M 2
                                                                                  l
                            M 离 = (m1 + m2 )ω02 l sin θ0 ⋅ l cos θ 0 − 2              ω0 r sin θ 0 ⋅ r cos θ 0
                                                                                 0 l 2
                                                                                                                               ②
                                                     M 22
                                     = (m1 + m2 +      )ω0 l sin θ 0 cos θ0
                                                     3
由①②得
                                                            kθ0 − (m1 − m2 ) gl sin θ0
                                                 ω0 =                                                                          ③
                                                                    M
                                                          (m1 + m2 + )l 2 sin θ0 cosθ0
                                                                     3
（i）当 m1 > m 2 时：
             π                                                        M
    若 0 < θ0 < ，由①②式可得 kθ 0 − ( m1 − m2 ) gl sin θ 0 = ( m1 + m2 + )ω 02 l 2 sin θ 0 cos θ 0 > 0 ，即 θ0 应满足
             2                                                        3
                                        π
                             0 < θ 0 < 且 kθ 0 > ( m1 − m2 ) gl sin θ 0                                    ④
                                        2
 π                                                             M
若 < θ 0 < π ，由①②式可得 kθ 0 − ( m1 − m2 ) gl sin θ 0 = ( m1 + m2 + )ω 02 l 2 sin θ 0 cos θ 0 < 0 ，即 θ0 应满足
 2                                                              3
                             π
                                < θ 0 < π 且 kθ 0 < ( m1 − m2 ) gl sin θ 0                                 ⑤
                             2
（ii）当 m1 ≤ m2 时：
                                                                       M 2 2
    由①②式可得 kθ 0 + ( m2 − m1 ) gl sin θ 0 = ( m1 + m2 +                    )ω 0 l sin θ 0 cos θ 0 > 0 ，即 θ0 应满足
                                                                       3
                                                                           π
                                                                 0 < θ0 <                                                      ⑥
                                                                           2
    （1.2）在地面系中，以 O 为参考点， m1 和 m 2 的角动量分别为
                                         L1 = r1 × m1v1 = m1l 2 sin θ 0ω 0 (cos θ 0 e x + sin θ 0 e z )                        ⑦
                                        L2 = r2 × m2 v 2 = m2 l sin θ 0ω 0 (cos θ 0 e x + sin θ 0 e z )
                                                                  2
                                                                                                                               ⑧
细杆 M 的角动量
                            l   dr M 2                                           M 2
                 LM = 2             r sin θ 0ω 0 (cos θ 0 e x + sin θ 0 e z ) =   l sin θ 0ω 0 (cos θ 0 e x + sin θ 0 e z )   ⑨
                        0        l 2                                             3
所以系统的角动量
                                                   M 2
                     L = L1 + L2 + LM = ( m1 + m2 +  )l sin θ 0ω0 (cos θ 0 e x + sin θ 0 e z )
                                                   3
                                                                                                                               ⑩
                                    M            kθ − ( m1 − m2 ) gl sin θ 0
                       = ( m1 + m2 + )l 2 sin θ 0 0                          (cos θ 0 e x + sin θ 0 e z )
                                    3                     cos θ 0
    在地面系中，系统质心 C 在细杆所在直线上，到 O 的距离为
                       m l + m2 (−l ) + M ⋅ 0     m1 − m2
                   rC = 1                     =             l                                                                  ⑪
                           m1 + m2 + M          m1 + m2 + M
质心 C 绕 z 轴做角速度为 ω 0 、半径为 rC sin θ0 的匀速圆周运动，质心加速度为
                                                            a C = ω 02 rC sin θ 0 e x                                          ⑫
系统在轴承 A、B 处的作用力 FA = FAx ex + FAy ey 、 FB = FBx ex + FBy ey 作用下（系统重力与地面对转轴的支持
力抵消），由质心运动定理得
                                                     FA + FB = ( m1 + m2 + M )aC                                               ⑬
x、y 方向分量式分别为
                                       FAx + FBx = ( m1 + m2 + M ) aC = ( m1 − m 2 )ω 02 l sin θ 0                             ⑭
                                                                                                                               17
                                                   FAy + FBy = 0                                                ⑮
  以 O 为参考点，系统重力的力矩记为 M G ，轴承 A、B 处作用力的力矩分别记为 M A 、 M B 。
  角动量 L 随系统同步绕转轴（z 轴）以角速度 ω0 e z 旋转，是常模旋转矢量，其变化率
                               dL
                                  = ω0 e z × L = ω0 e z × ( Lx e x + Lz e z ) = ω0 Lx e y
                               dt
                                                                                                                ⑯
                                                 M
                                  = (m1 + m2 + )ω02 l 2 sin θ 0 cos θ 0 e y
                                                  3
由质点系角动量定理得
                                                                      dL
                                              MG + MA + MB =                                                    ⑰
                                                                      dt
x、y 方向分量式分别为
                                                −hFAy + hFBy = 0                                                ⑱
                                                                              M 2 2
                    − ( m1 − m2 ) gl sin θ 0 + hFAx − hFBx = ( m1 + m2 +        )ω 0 l cos θ sin θ              ⑲
                                                                              3
由⑮⑱两式得
                                                   FAy = FBy = 0                                                ⑳
由⑭⑲两式得
             1                             1                            1           M
        FAx =  ( m1 − m2 )ω02 l sin θ 0 +     ( m1 − m2 ) gl sin θ 0 +    (m1 + m2 + )ω02 l 2 sin θ 0 cos θ 0
             2                            2h                           2h           3
             1            kθ − ( m1 − m2 ) gl sin θ 0 kθ 0                                                      ㉑
            = ( m1 − m2 ) 0                               +
             2                             M
                           ( m1 + m2 + )l cos θ 0            2h
                                            3
             1                            1                            1            M
        FBx = ( m1 − m2 )ω02 l sin θ 0 −      ( m1 − m2 ) gl sin θ 0 −    (m1 + m2 + )ω02 l 2 sin θ 0 cos θ 0
             2                            2h                           2h           3
             1            kθ 0 − ( m1 − m2 ) gl sin θ 0 kθ 0                                                    ㉒
            = ( m1 − m2 )                                 −
             2                             M
                           ( m1 + m2 + )l cos θ 0            2h
                                           3
[解法二
   以 O 为参考点，转轴在轴承 A、B 处约束力的力矩 M A 、 M B 和盘簧对其施加的力矩 − Mk 作用下力矩
平衡，即
                                               MA + MB − Mk = 0                                                 ⑯′
其中
                                                    Mk = kθ0ey                                                  ⑰′
x、y 方向分量式分别为
                                                −hFAy + hFBy = 0                                                ⑱′
                                              hFAx − hFBx − kθ0 = 0                                             ⑲′
由⑮⑱′两式得
                                                   FAy = FBy = 0                                                ⑳′
由⑭⑲′两式得
                                      1           kθ − (m1 − m2 ) gl sin θ 0 kθ 0
                              FAx =     (m1 − m2 ) 0                        +                                   ㉑′
                                      2                       M
                                                   ( m1 + m2 + )l cos θ 0     2h
                                                              3



                                                                                                                18
                                     1          kθ − (m1 − m2 ) gl sin θ0 kθ0
                                FBx = (m1 − m2 ) 0                       −                              ㉒′
                                     2                     M
                                                 (m1 + m2 + )l cos θ0      2h
                                                            3
]
（2）
  （2.1）取 m1 = m2 = m ，转速仪可绕转轴自由转动时，受冲击后，系统绕转轴（z 轴）的角动量（系统角
动量 L 的 z 方向分量）守恒，因此，在⑩式的第二个等式中， θ 和 ω 加下标“0”和不加下标“0”对应的式子
相等，即
                                                   M 2                   M
                                Lz = (2 m +          )l sin 2 θω = (2 m + )l 2 sin 2 θ 0ω 0             ㉓
                                                   3                     3
解得
                                                              sin 2 θ0
                                                         ω=            ω0                               ㉔
                                                              sin 2 θ
系统的动能为
                   1 2 1                     l dr M
                     Iθ + 2m(ωl sin θ )2 + 2
                              Ek =                   (ωr sin θ ) 2
                   2     2                   0 l   2
                                                                                                        ㉕
                   1     M          1       M
                  = (2m + )l 2θ 2 + (2m + )l 2 sin 2 θω 2
                   2      3         2        3
其中 I 为系统在细杆-转轴平面绕 O 的转动惯量
                                                             1                    M 2
                                    I = ( m1 + m 2 )l 2 +      M (2l ) 2 = (2 m +   )l                  ㉖
                                                            12                    3
系统的机械能为
                                         1        M 2 2 1        M 2              1
                       E = Ek + Ep =       (2 m +   )l θ + (2 m +   )l sin 2 θω 2 + kθ 2                ㉗
                                         2        3       2       3                2
系统受冲击后的瞬间有 θ = θ0 、θ = Ω0 、ω = ω0 ，细杆与转轴的夹角到达最大时，θ = θ M 、θ = 0 、ω = ωM ，
由机械能守恒得
            1        M 2 2 1          M 2                 1       1       M 2                  1
              (2 m +   )l Ω0 + (2 m +   )l sin 2 θ 0ω 02 + kθ 02 = (2 m +   )l sin 2 θ M ω M2 + kθ M2   ㉘
            2        3        2       3                   2       2       3                    2
将③㉔式代入后解得

                                               k                      sin 2 θ 0    
                             Ω0 =                         θ 0 tan θ 0           − 1 + θ M2 − θ 02     ㉙
                                                                      sin θ M
                                                                          2
                                           M                                        
                                      (2m + )l 2
                                           3
    （2.2）
由㉔㉗式得
                               1     M         1     M        sin 4 θ0 1 2
                            E = (2m + )l 2θ2 + (2m + )l 2ω02         + kθ                              ㉚
                               2     3         2     3        sin 2 θ 2
将 θ = θ 0 + δ （ δ << θ 0 ）代入后展开至 δ 的二阶项，并将③式代入得
                         1      M          1      M                              
                    E=     (2m + )l 2δ 2 +  (2m + )l 2ω02 (2 cos 2 θ 0 + 1) + k  δ 2 + 常量
                         2      3          2      3                              
                                                                                                        ㉛
                        1     M          1           2 cos 2 θ 0 + 1  2
                       = (2m + )l 2δ 2 + k  1 + θ 0                  δ + 常量
                        2     3          2           sin θ 0 cos θ 0 

                         π          2 cos θ 0 + 1
                                           2
由⑥式知，此时 0 < θ 0 <          ， 1 + θ0               > 0 ，细杆在 θ0 附近做简谐运动，角频率
                         2          sin θ0 cos θ0


                                                                                                        19
                                                         k            2 cos 2 θ 0 + 1 
                                         ωθ =                  1 + θ0                                       ㉜
                                                        M
                                                   (2m + )l 2         sin θ 0 cos θ 0 
                                                        3
[解法二
在绕 z 轴以角速度 ω 随系统同步转动的参考系中，细杆受冲击后绕 O 轴（垂直于转轴和细杆）做定轴转动，
考虑到惯性离心力的力矩（见②式），由转动定理得
                                                             M 2 2
                                          − kθ + (2 m +        )ω l sin θ cos θ = I θ
                                                             3
将㉔㉖式代入上式得
                                                   M                     cos θ            M 2 
                                − kθ + (2 m +        ) sin 4 θ 0ω 02 l 2         = (2 m +   )l θ              ㉚′
                                                   3                     sin 3 θ          3
将 θ = θ 0 + δ （ δ << θ 0 ）代入后展开至 δ 的一阶项，再将③式代入得
                          M 2 2                                     2 cos 2 θ 0 + 1           M 2
              −  k + (2m + )l ω0 (2 cos θ 0 + 1)  δ =  − k  1 + θ 0                  δ = (2m + )l δ   ㉛′
                                         2

                          3                                         sin θ 0 cos θ 0           3

                 π         2 cos θ 0 + 1       2
由⑥式知，此时 0 < θ 0 < ， 1 + θ0               > 0 ，细杆在 θ0 附近做简谐运动，角频率
                 2         sin θ0 cos θ0

                                                         k            2 cos 2 θ 0 + 1 
                                         ωθ =                  1 + θ0                                       ㉜′
                                                        M
                                                   (2m + )l 2         sin θ 0 cos θ 0 
                                                        3
]
    （2.3）受冲击之后
                                           θ (t ) = θ 0 + δ 0 sin ωθ t （ δ 0 << θ 0 ）                         ㉝
将上式代入㉔式并展开至 δ0 的一阶项得
                                               sin 2 θ0
                            ω (t ) =                              ω0 ≈ (1 − 2cot θ0 ⋅ δ 0 sin ωθ t )ω0        ㉞
                                       sin 2 (θ0 + δ 0 sin ωθ t )

               k           2 cos 2 θ 0 + 1                          kθ0
其中 ωθ =             1 + θ0                  、 ω0 =                                  。
               M 2
          (2m + )l          sin θ 0 cos θ 0                        M 2
                                                               (2m + )l sin θ0 cos θ0
               3                                                    3

评分标准：本题 45 分
第（1）问 24 分，
  （1.1）问 7 分，①式 2 分，②③④⑤⑥式各 1 分；
  （1.2）问 17 分，⑦⑧⑨⑩式各 1 分（若只给出角动量的某个分量，⑦⑧⑨⑩式不得分），⑭式 2
分，⑮式 1 分，⑯式 2 分，⑱式 1 分，⑲式 2 分，⑳式 1 分，㉑㉒式各 2 分；
   [解法二：带撇的式子与不带撇的相同序数的式子赋分相同]
第（2）问 21 分，
    （2.1）问 9 分，㉓式 2 分，㉔式 1 分，㉕式 2 分，㉖式 1 分，㉘式 2 分，㉙式 1 分；
    （2.2）问 8 分，㉚㉛式各 3 分，㉜式 2 分；
    [解法二：带撇的式子与不带撇的相同序数的式子赋分相同]
    （2.3）问 4 分，㉝㉞式各 2 分。
```
