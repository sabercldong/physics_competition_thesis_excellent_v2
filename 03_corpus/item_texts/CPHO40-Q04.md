# 第40届复赛第4题：编木拱桥杆系静力平衡

## 来源

- 试题文件：`03_corpus/raw_papers/cpho_40_2023_fusai_paper_solution_candidate.pdf`
- 试题页码：2-3
- 解答页码：12-13
- 题图：03_corpus/item_assets/CPHO40-Q04-figure1-page2-raw.png;03_corpus/item_assets/CPHO40-Q04-figure2-page2-raw.png;03_corpus/item_assets/CPHO40-Q04-figure3-page3-raw.png;03_corpus/item_assets/CPHO40-Q04-figure4-page3-raw.png
- 抽取状态：题干使用页面OCR并经视觉定位大题边界；参考解答使用PDF文本层抽取；题图按渲染页原图裁切，未去除来源/权属水印。公式、特殊符号、图注和OCR错字需人工校对。

## 题干OCR抽取文本

```text
四、(40 分) 北宋著名画家张择端所绘的《清明上河图》中有一座用木材制作的"编木拱桥”〈图 4a)，形成一首
飞虹架设在河上。四百多年后达-芬奇也曾留下类似的设计手稿，至今为世人称奇。图 4b 是五个单元组成的编林
拱桥实物模型，每个单元包含一对与纸面平行的长杆和一根牌直于纸面的短杆，它没有钉也没有卯，整个结构的
所有组件在重力作用下互相挤压而结合在一起，靠支持力和摩擦力互相支撑，互相制约。真实桥梁需要在木村上
开槽，以提升桥的安全性。

a aa              i
ee Lg | itll,
aera” a                      Fab
图4a
考虑一个简化的编森拱桥模型，即仅有三个单元的左右对称的拱桥，图 4c 是其侧视图。在简化模型下，只
考虑拱桥在竖直平面纸面) 内的平衡，将与纸面平行的每一对长杆等效为一根质量为 M 的杆，则此编木拱桥

可进一步简化为六根杆;三根短杆A、A'、B 和三根长杆 C、D、D'。所有的杆都是半径为 R 的匀质圆柱体，没

有开杜。短杆的质量均为 m，长杆的长度均为上，长杆之间互不接触。短杆 B 表面是光滑的，其余杆之间的藤麻
2

控因数均为w，杆与地面间的静摩擦因数为心。长杆 D、D与水平地面的夹角均为 b。 重力加速度大小为8。
P30
5 A. 7 |
CA                        \@)
a        b
D&Ka                           AZD'
图 4c ”三单元编木拱桥侧视图〈简化为六根杆)
f
Si
|

图 4d.A 杆的受力图      图 4e. B 杆的受力图

(1) 已知图 4c 中 D 杆下端到与 A 杆的接触点之间的长度为 ，求 D 杆下端到与 B 杆的接触点之间的长度上的
表达式。

(2) 系统平衡时，考虑到杆 A 与 A'对称，杆 D 与 D'对称，分析图 4e 中 A、B、C、D 四根杆的受力情况。图
4d、4e 分别给出了 A、B 两根杆的受力，请画出图 4c 中 C、D 两根杆的受力图，为简明起见，每一对作用力和
反作用力请用同一符号表示。对A、B、C、D 四根杆分别列出相应的力平衡方程〈必要时包括力矩平衡方程)。

(3) &M=6m, 0=45°, L=30cem, a=16cm, R=2%AV2-lNeom, RRB RRA pM WET RAR
件时，图 4c 所示的结构能保持平衡(数值结果保留三位有效数字) ?
```

## 参考解答抽取文本

```text
四、
           （1）由几何关系得
                                                                                                                         N4
                                                             
                                       b  a  4 R cot                           ①
                                                             2
           （2）C、D 两根杆的受力图分别如题解图 4a 和题解图 4b 所示。


                                                                                                        N5               Mg

                                                                                                                   N2
                                                                                                                        f5
                                                                                                   f2
                                                             题解图 4a                                            题解图 4b

                   对 A 杆而言，力平衡方程为
                                N1  mg  N 2 cos   f 2 sin                                                ②
                                                                 f1  f 2 cos   N 2 sin                    ③
           对圆柱轴线的力矩平衡方程为
                                                                        f1 R  f 2 R                          ④
                 对 B 杆而言，力平衡方程为
                                                                 N 3  2 N 4 cos   mg                       ⑤
                 对 C 杆而言，力平衡方程为
                                                                    2N1  N 3  Mg                            ⑥

                 对 D 杆而言，力平衡方程为
                     N 5  N 4 cos   N 2 cos   f 2 sin   Mg                                             ⑦
                                   f 5  N 2 sin   N 4 sin   f 2 cos                                     ⑧
           对 D 杆与地面接触点的力矩平衡方程为
                           L                
                N 2 a  Mg  cos   R sin    N 4 b  f 2 2 R                                              ⑨
                           2                
           【或对 D 杆质心的力矩平衡方程为
                    L                      L                       L                       L
                N 5  cos   R sin    f5  sin   R cos    N 2   a   f 2 R  N 4  b           ⑨′】
                     2                      2                       2                      2
           （3）此条件下
                                                                                 
                                                              b  a  4 R cot         24 cm                  ⑩
                                                                                 2
           由②③④式可得
                                                                                sin 
                                                                 f1  f 2              N2                    ⑪
                                                                              1  cos 
                                                                     N 1  mg  N 2                           ⑫
           由⑤⑥式可得
                                                                                 1
                                                             N 1  N 4 cos       (M  m) g                  ⑬
                                                                                 2
           将⑪⑫⑬式代入⑨式可得
                               L                        1            b       sin 
             ( N1  mg )a  Mg  cos   R sin     N1  ( M  m) g                 ( N1  mg )2 R ⑭
                               2                        2            cos  1  cos 
           解得


                                                                                               7




{#{QQABYQCQggggQAIAAQhCUQGgCgOQkBAACAoGRBAAoAABARFABAA=}#}
                                           L                1             b     sin 
                                 mga  Mg  cos   R sin    (M  m) g               mg 2 R
                                           2                2           cos  1  cos
                            N1 
                                                       b       sin                                              ⑮
                                                                    2R  a
                                                    cos 1  cos
                                10.427 mg
           由⑪⑫式可得
                                                                     L                 1               b
                                                                  Mg  cos   R sin    ( M  3m) g
                                  sin                    sin       2                 2             cos
                     f1  f 2            ( N1  mg ) 
                                1  cos                1  cos            b        sin                        ⑯
                                                                                          2R  a
                                                                          cos  1  cos 
                         4.733mg
           系统保持平衡要求
                                                               f1   N 1 ， f 2   N 2                          ⑰
           （因为 f1  f 2 、 N 2  N1  mg  N1 ，μ 的范围由上式中第一式决定）
           解得
                                                          L                 1               b
                                                       Mg  cos   R sin    (M  3m) g
                      f   sin                             2                 2            cos 
                    1 
                     N1 1  cos                     L                 1              b       sin             ⑱
                                            mga  Mg  cos   R sin    ( M  m) g                  mg 2 R
                                                      2                  2          cos    1  cos 
               0.454
           由②⑤⑥⑦式可得
                                                                    3             21
                                                             N5      (M  m) g     mg                          ⑲
                                                                    2             2
           由⑧⑩⑪⑫式可得
                                                         sin   1                            sin 
                                     f 5  N1  tan               ( M  m ) g tan   mg
                                                       1  cos   2                        1  cos            ⑳
                                          2.194mg
           系统保持平衡要求
                                                                      f5   N 5                                ㉑
           解得
                               f5      2 N1                sin   1               2m       sin 
                                             tan               tan                         0.209     ㉒
                               N 5 3( M  m ) g          1  cos   3         3( M  m ) 1  cos 


           评分参考：本题 40 分。
           第（1）问 2 分，①式 2 分；
           第（2）问 20 分，C 杆和 D 杆的受力图各 2 分，②③④⑤⑥⑦⑧⑨（或⑨′）式各 2 分；
           第（3）问 18 分，⑮⑯⑰式各 2 分，⑱式 3 分，⑲⑳㉑式各 2 分，㉒式 3 分。
```
