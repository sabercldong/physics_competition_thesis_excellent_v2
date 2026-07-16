# 第35届复赛第3题：细杆打击中心与撤轴后运动

## 来源

- 试题文件：`03_corpus/raw_papers/cpho_35_2018_fusai_paper_solution_candidate.pdf`
- 试题页码：1-2
- 解答页码：13-16
- 题图：03_corpus/item_assets/CPHO35-Q03-figure1-page1-raw.png；重裁候选图：03_corpus/item_assets/CPHO35-Q03-figure1-page1-recrop-v1.png
- 抽取状态：PDF文本层抽取，需人工校对公式、图注与特殊符号。

## 题干

```text
三、如图，一质量为 M 、长为 l 的匀质细杆 AB 自由悬挂于通过坐标
原点 O 点的水平光滑转轴上（此时，杆的上端 A 未在图中标出，可视
为与 O 点重合），杆可绕通过 O 点的轴在竖直平面（即 x-y 平面， x 轴

                                                                                         O
                                        第 - 1 - 页 / 共 38 页                                                    x

                                                                                         l       v0   m
                                                                                         M
                                                                                             B
正方向水平向右）内转动； O 点相对于地面足够高，初始时杆自然下垂；一质量为 m 的弹

丸以大小为 v0 的水平速度撞击杆的打击中心（打击过程中轴对杆的水平作用力为零）并很

快嵌入杆中。在杆转半圈至竖直状态时立即撤除转轴。重力加速度大小为 g 。
（1）求杆的打击中心到 O 点的距离；
（2）求撤除转轴前，杆被撞击后转过  （ 0    π ）角时转轴对杆的作用力；
（3）以撤除转轴的瞬间为计时零点，求撤除转轴后直至杆着地前，杆端 B 的位置随时间 t 变

化的表达式 xB ( t ) 和 yB ( t ) ；

（4）求在撤除转轴后，杆再转半圈时 O 、 B 两点的高度差。
```

## G1-07-B1公式核对入口

- 公式核对表：`03_corpus/manual_review_transcripts/CPHO35-Q03_formula_check_v1.csv`
- 题面证据：
  - `03_corpus/manual_review_renders/G1-07-B1/CPHO35-Q03-paper-page-1.png`
  - `03_corpus/manual_review_renders/G1-07-B1/CPHO35-Q03-paper-page-2.png`
- 答案证据：
  - `03_corpus/manual_review_renders/G1-07-B1/CPHO35-Q03-solution-page-13.png`
  - `03_corpus/manual_review_renders/G1-07-B1/CPHO35-Q03-solution-page-14.png`
  - `03_corpus/manual_review_renders/G1-07-B1/CPHO35-Q03-solution-page-15.png`
  - `03_corpus/manual_review_renders/G1-07-B1/CPHO35-Q03-solution-page-16.png`
- 下一题排除边界：
  - `03_corpus/manual_review_renders/G1-07-B1/CPHO35-Q03-solution-boundary-next-page-17.png`

边界说明：第3题题面从试题PDF第1页页底开始，延续至第2页上半部；答案PDF第13页中部开始，第14-15页覆盖核心推导，第16页式⑳后进入第4题，第17页为第4题答案，仅作排除边界。本入口只建立核对路线，不代表公式、特殊符号、题图或分值已经完成正式人工销项。

重点待复核：

1. `l` 与数字 `1` 的视觉混淆，尤其是 `Ml^2`、`(4m+3M)l` 和高度差公式中的 `l`。
2. `L_c`、`x_B`、`y_B`、`omega_0`、`omega'`、`beta'` 等上下标和撇号。
3. 式⑨、式⑮、式⑲、式⑳中的根号、负一次方、分母括号和绝对值范围。
4. 式⑬、式⑭中的轴力分量、三角函数、`cos^2 theta` 和正负号。
5. 同题 `CPHO35-Q03-FIG` 已建立题图核对入口和重裁候选图，但仍未完成真实人工销项；`CPHO35-Q03-SCORE` 分值边界仍为待核实。

## G1-07-C1题图核对入口

- 题图核对表：`03_corpus/manual_review_transcripts/CPHO35-Q03_figure_check_v1.csv`
- 原始裁图：`03_corpus/item_assets/CPHO35-Q03-figure1-page1-raw.png`
- 重裁候选图：`03_corpus/item_assets/CPHO35-Q03-figure1-page1-recrop-v1.png`
- 裁框定位图：`03_corpus/manual_review_renders/G1-07-C1/CPHO35-Q03-paper-page-1-figure1-crop-box.png`
- 新旧对照接触图：`03_corpus/manual_review_renders/G1-07-C1/CPHO35-Q03-figure1-check-contact-v1.png`

边界说明：第3题题图位于试题PDF第1页页底右侧。原始裁图保留 `y`、`O`、`x`、竖直细杆、`l/M`、`B`、弹丸 `m` 和 `v0` 箭头，但左侧混入邻近题干残字且 `B` 端贴近底部。重裁候选图去除左侧残字并保留关键坐标和杆图；因图位于页底，`B` 端下方留白有限，论文或附录使用前仍需最终版式复核。本入口不填写真实校对人和日期，不代表题图正式销项。

## 参考解答抽取文本

```text
三、如图，一质量为 M 、长为 l 的匀质细杆 AB 自由悬挂于通过坐标                                                      y

原点 O 点的水平光滑转轴上（此时，杆的上端 A 未在图中标出，可视
为与 O 点重合），杆可绕通过 O 点的轴在竖直平面（即 x-y 平面， x 轴
正方向水平向右）内转动； O 点相对于地面足够高，初始时杆自然下
                                                                                      O
                                                                                                           x
垂；一质量为 m 的弹丸以大小为 v0 的水平速度撞击杆的打击中心（打
                                                                                      l           v0   m
击过程中轴对杆的水平作用力为零）并很快嵌入杆中。在杆转半圈至                                                        M
竖直状态时立即撤除转轴。重力加速度大小为 g 。                                                                      B
（1）求杆的打击中心到 O 点的距离；
（2）求撤除转轴前，杆被撞击后转过  （ 0    π ）角时转轴对杆的作用力；
（3）以撤除转轴的瞬间为计时零点，求撤除转轴后直至杆着地前，杆端 B 的位置随时间 t 变

化的表达式 xB ( t ) 和 yB ( t ) ；

（4）求在撤除转轴后，杆再转半圈时 O 、 B 两点的高度差。



参考解答：
（1）设打击中心位置距转轴距离为 L ，水平外力 F 作用于打击中心后杆的角加速度为  。

由刚体定轴转动的动力学方程有
             1
         FL = Ml 2                                                                                    ①
             3


                                            第 - 13 - 页 / 共 38 页
  1 2
式中 Ml 是杆绕过其端点 A （即 O 点）的水平轴转动的转动惯量。由①式得
  3
          3FL
     =
          Ml 2
在弹丸撞击杆后的瞬间，杆的质心加速度的水平分量为
            l    3FL
     ax =     =                                         ②
            2    2 Ml

设轴对杆的作用力的水平分量为 Fx ，由质心运动定理有

     F − Fx = Max                                        ③

将②式代入③式，水平外力打击到杆的打击中心处，轴对杆的作用力的水平分量应为零

           3L 
     Fx =  1 −  F = 0
              2l 

由此得，杆的打击中心到 O 点的距离为
            2
     L=       l                                          ④
            3
（2）弹丸与杆的碰撞过程满足动量守恒
     mv0 = (M + m)v

解得
           m v0
     v=                                                  ⑤
          M +m

设碰撞后带弹丸的杆的质心位置与 O 点的距离为 Lc ，则
                      1
      ( M + m) Lc =     Ml + mL
                      2
即
            4m + 3M
     Lc =             l                                  ⑥
            6( M + m)

在碰撞后的瞬间，杆转动的角速度为
             v     6mv0
     0 =      =                                         ⑦
             Lc (4m + 3M )l

带弹丸的杆的转动惯量为
                          2
        1         2  1
     I = Ml 2 + m  l  = ( 3M + 4m ) l 2
        3         3  9
在杆从垂直位置转过  （ 0    π ）角的过程中，系统的机械能守恒，有
     1 2 1 2
       I 0 = I  + ( M + m ) gLc (1 − cos  )           ⑧
     2       2
解得


                                   第 - 14 - 页 / 共 38 页
                    2( M + m) gLc (1 − cos  )
       2 = 02 −
                               I
将⑤⑥⑦式以及转动惯量 I 的表达式代入上式得

                 36m 2 v02       3g
      =                       −    (1 − cos  )                                              ⑨
              (4m + 3M ) 2 l 2    l

   另一方面，杆由初始位置转过  角时，由刚体定轴转动的动力学方程有

      ( M + m ) gLc sin  = I  

式中   是重力矩产生的角加速度。由此得
             ( M + m) gLc sin  3g
       =                     =    sin                                                      ⑩
                    I            2l

此时质心加速度的 x 分量 acx 和 y 分量 acy 分别为

      acx = Lc   cos + Lc 2 sin 

      acy = Lc 2 cos  − Lc   sin 

其中角速度  由⑨式给出。设撤除转轴前，杆被撞击后转过  角时转轴对杆的作用力的 x 分

量和 y 分量分别为 N x 和 N y ，由质心运动定理有

      N x = ( M + m)acx = ( M + m) Lc (   cos  +  2 sin  )                               ⑪

      N y = ( M + m )( g + acy ) = ( M + m )[ g + Lc ( 2 cos  −   sin  )]                ⑫

将⑥⑨⑩式代入⑪⑫式得

             (4m + 3M ) g                             6m2 v02
      Nx =                (3sin  cos − 2sin  ) +             sin                          ⑬
                  4                                 (4m + 3M )l

                              6m2 v02          (4m + 3M ) g
      N y = (M + m) g +
                            (4m + 3M )l
                                        cos +
                                                    4
                                                            (3cos2  − 2cos − 1)             ⑭

（3）当杆转到竖直位置即  = π 时，由⑨式得，角速度   为

                36m 2 v02       6g
       =                    −                                                               ⑮
              (4m + 3M ) l2 2
                                 l

撤除转轴后，带弹丸的杆的质心做平抛运动，同时杆绕其质心以角速度  在竖直平面内做
顺时针转动。以撤除转轴的瞬间为计时零点，在 t 时刻的质心坐标为

      xc = vct = ( Lc ) t

                    1 2
      yc = Lc −       gt
                    2
建立如图所示的质心坐标系，由于杆同时绕质心以角速度  在竖直
                                                                                 y'
平面内顺时针转动，在 t 时刻杆的 B 端相对于其质心的坐标为
                                                                                      ’t B
                                                                                 c                x'

                                         第 - 15 - 页 / 共 38 页
       xB = (l − Lc ) sin  t     yB = (l − Lc ) cos t
在地面参考系中， t 时刻杆的 B 端的坐标为

       xB (t ) = xc + xB = ( Lc) t + (l − Lc )sin t       ⑯

                                    1 2
       yB (t ) = yc + y B = Lc −     gt + (l − Lc ) cos t   ⑰
                                    2
（4）撤除转轴后，经过时间 t1，杆再转了半圈，即

        t1 = π
设此时 O 、 B 两点的高度差为 h ，即此时杆 B 端的 y 坐标的绝对值。由⑰式得
                                               2
                                    1 π
       h = yB (t1 ) = 2 Lc − l −     g                                       ⑱
                                    2   

将⑥⑮式代入⑱式得
                                          −1
          π 2 g  36m2 v02      6g     ml
       h=                     −  −                                           ⑲
           2  (4m + 3M ) l2 2
                                 l  3(M + m)

或

                 π 2 g (4m + 3M )2 l 2           ml
       h=                                  −                                   ⑳
               
            12 6m v0 − g (4m + 3M ) l 
                   2 2                 2
                                            3( M + m)
```
