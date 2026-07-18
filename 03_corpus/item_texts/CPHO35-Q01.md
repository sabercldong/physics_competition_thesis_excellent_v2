# 第35届复赛第1题：地球引力场中的发射运动

## 来源

- 试题文件：`03_corpus/raw_papers/cpho_35_2018_fusai_paper_solution_candidate.pdf`
- 试题页码：1
- 解答页码：6-9
- 题图：无
- 抽取状态：PDF文本层抽取，需人工校对公式与特殊符号。

## G1-07-B1 公式核对入口

- 公式核对表：`03_corpus/manual_review_transcripts/CPHO35-Q01_formula_check_v1.csv`
- 页面证据：
  - `03_corpus/manual_review_renders/G1-07-B1/CPHO35-Q01-paper-page-1.png`
  - `03_corpus/manual_review_renders/G1-07-B1/CPHO35-Q01-solution-page-06.png`
  - `03_corpus/manual_review_renders/G1-07-B1/CPHO35-Q01-solution-page-07.png`
  - `03_corpus/manual_review_renders/G1-07-B1/CPHO35-Q01-solution-page-08.png`
  - `03_corpus/manual_review_renders/G1-07-B1/CPHO35-Q01-solution-page-09.png`
- 边界说明：经视觉检查，第35届第1题答案从PDF第6页开始，第9页上半部仍为第1题时间积分、参数 `a/b/c`、`Delta`、最终时间表达式和临界时间结果；第9页下半部进入第2题。本轮将原答案页范围 `6-8` 纠偏为 `6-9`。
- 待终核重点：`v0min`、周期运动上下界、落地速度根号、`alpha` 展开式、极坐标能量式、径向速度式、式⑭时间积分、`a/b/c` 与 `Delta` 定义、式⑮最终时间表达式和临界时间。
- 状态：答案公式核对入口完成，待最终复核；第35届分值边界 `CPHO35-Q01-SCORE` 已建立核对入口，待最终复核。

## G1-07-D1 分值边界核对入口

- 分值边界核对表：`03_corpus/manual_review_transcripts/CPHO35-Q01_score_boundary_check_v1.csv`
- 页面证据：
  - `03_corpus/manual_review_renders/G1-07-D1/CPHO35-Q01-paper-page-1.png`
  - `03_corpus/manual_review_renders/G1-07-D1/CPHO35-Q01-solution-page-06.png`
  - `03_corpus/manual_review_renders/G1-07-D1/CPHO35-Q01-solution-page-07.png`
  - `03_corpus/manual_review_renders/G1-07-D1/CPHO35-Q01-solution-page-08.png`
  - `03_corpus/manual_review_renders/G1-07-D1/CPHO35-Q01-solution-page-09.png`
- 核对结论：第1题题面位于试题PDF第1页上半部，可确认两个小问；答案第6页开始第1题参考解答，第7至8页继续推导，第9页上半部为第1题时间积分、最终时间表达式和临界时间结果，第9页下半部进入第2题。
- 当前分值边界：题面页、答案页和PDF文本层辅助检索均未见第1题大题分值、小问分值拆分或评分标准；`item_index.csv` 中第1题两个小问分值字段已标为“未见PDF明示，待最终复核”。
- 不可声称：不得据此生成第35届第1题正式分值统计、评分结论或论文附录分值；若后续取得正式评分细则、原卷说明或真实最终复核记录，再回填具体分值。

## 题干

```text
一、假设地球是一个质量分布各向同性的球体。从地球上空离地面高度为 h 的空间站发射一

个小物体，该物体相对于地球以某一初速度运动，初速度方向与其到地心的连线垂直。已知

地球半径为 R ，质量为 M ，引力常量为 G 。地球自转及地球大气的影响可忽略。

  （1）若该物体能绕地球做周期运动，其初速度的大小应满足什么条件？
  （2）若该物体的初速度大小为 v0 ，且能落到地面，求其落地时速度的大小和方向（即

速度与其水平分量之间的夹角）、以及它从开始发射直至落地所需的时间。

  已知：对于 c  0 ，  = b 2 − 4ac  0 ，有

            xdx               a + bx + cx 2        b              2cx + b
       a + bx + cx   2
                          =
                                   c
                                            −
                                              2 ( −c )
                                                      3/ 2
                                                           arcsin
                                                                     
                                                                          +C


式中 C 为积分常数。
```

## 参考解答抽取文本

```text
第 35 届全国中学生物理竞赛复赛理论考试试题解答


一、假设地球是一个质量分布各向同性的球体。从地球上空离地面高度为 h 的空间站发射一

个小物体，该物体相对于地球以某一初速度运动，初速度方向与其到地心的连线垂直。已知

地球半径为 R ，质量为 M ，引力常量为 G 。地球自转及地球大气的影响可忽略。

 （1）若该物体能绕地球做周期运动，其初速度的大小应满足什么条件？
 （2）若该物体的初速度大小为 v0 ，且能落到地面，求其落地时速度的大小和方向（即

速度与其水平分量之间的夹角）、以及它从开始发射直至落地所需的时间。

  已知：对于 c  0 ，  = b 2 − 4ac  0 ，有

                xdx           a + bx + cx 2        b              2cx + b
       a + bx + cx   2
                          =
                                   c
                                            −
                                              2 ( −c )
                                                      3/ 2
                                                           arcsin
                                                                     
                                                                          +C


式中 C 为积分常数。



参考解答：

（1）解法（一）

  假设小物体初始速度大小为 v0 ，在地球引力场中其能量为

              1 2        Mm
      E=        m v0 − G
              2          R+h
式中 m 是小物体的质量。小物体相对于地球中心的角动量为

      L = mv0 ( R + h )

  该物体能绕地球做周期运动，其能量应

      E0

由此条件以及 E 的表达式，得
              2GM                2GM
      v02        ，即 v0                                                       ①
              R+h                R+h
  物体能绕地球做持续的周期运动，不能坠落到地球表面。当物体初始速度 v 0 降低到某

个值 v0 min 时，物体运动的椭圆轨道将与地球表面相切，设这种情况下物体在与地球表面相

切时的运动速度为 v ，由角动量守恒定律
                                                R+h
      mv0min ( R + h ) = mvR ，即 v = v0min                                      ②
                                                 R
  由能量守恒定律有

                                        第 - 6 - 页 / 共 38 页
        1 2          Mm 1 2      Mm
          mv0min − G    = mv − G                                 ③
        2            R+h 2        R
将②式代入③式得

                        2GMR
        v0min =                                                  ④
                   ( R + h )( 2 R + h )

     当物体初速度 v 0 低于 v0 min 时，其轨道都将与地球表面相交，因此会坠落到地面上。所

以物体绕地球作椭圆或圆形轨道运动，但不会坠落到地球表面的条件是

               2GMR                  2GM
                               v0                              ⑤
          ( R + h )( 2R + h )        R+h

  解法（二）
   该物体能绕地球做周期运动，其运动轨迹应为椭圆（圆被视为椭圆的特殊情形），设其

近或远地点之一与地心的距离和速度大小分别为 r1 和 v1 ，另一近或远地点与地心的距离和速

度大小分别为 r2 和 v 2 。由角动量守恒和能量守恒有
        r1v1 = r2 v2                                             ①
        1 2       Mm 1 2        Mm
          mv1 − G     = mv2 − G                                  ②
        2          r1  2         r2

式中 m 是小物体的质量。消去 v2 得

         1 2GM 1         1         2GM 
            − 2 2     − 2 2  v12 −     =0
        r22
              r1 v1 r2 r1 v1        r1 

                                1                                   1
将 r1 和 v1 视为已知，上式是                 满足的一个一元二次方程。 r2 = r1 显然满足方程①②，因而
                                r2                                  r1

是一元二次方程的解。利用韦达定理，另一解是

        1 1  2GM        
          =          − 1                                       ③
        r2 r1  r1 v1
                    2
                         

     显然， r2  R ，且有限，故有
             1 1
        0                                                      ④
             r2 R

由③④式得，当 r1 给定时， v1 必须满足

            2GMR               2GM
                         v1      .
          r1 ( r1 + R )         r1

由题意知
         r1 = R + h ， v1 = v0

故有



                                          第 - 7 - 页 / 共 38 页
                 2GMR                      2GM
                                   v0                           ⑤
            ( R + h )( 2R + h )            R+h

（2）如果

                      2GMR
        v0                                                       ⑥
                 ( R + h )( 2R + h )
则物体会落到地球上。根据能量守恒，它落到地面时的速度大小 v 满足方程
        1 2      Mm 1 2       Mm
          mv − G    = mv0 − G                                     ⑦
        2         R  2        R+h
由⑦式得

                        2GM 2GM           2GMh
        v = v02 +          −     = v02 +                          ⑧
                         R   R+h         R ( R + h)

设物体落地点相对于地心的矢径与物体初始位置相对于地心的矢径之间的夹角为  。根据角

动量守恒，物体落到地面时的水平速度 v 满足方程

        Rv = ( R + h ) v0

上式即
                R+h
        v =        v0                                            ⑨
                 R
物体的速度方向与水平面的夹角是

                        v                  ( R + h ) v0
         = arccos  = arccos
                        v                          2GMRh          ⑩
                                       R 2 v02 +
                                                    R+h

     将物体的运动用极坐标  ( t ) 、 r ( t ) 描写，角动量守恒和能量守恒可分别表为

             d
        r2      = ( R + h ) v0                                    ⑪
             dt
和

        1  dr  1 2  d 
                    2                  2
                               Mm 1 2       Mm
         m   + mr       −G    = mv0 − G                       ⑫
        2  dt  2    dt      r  2        R+h

     d
消去      得
     dt

                ( R + h ) v0 2GM 2 2GM
                              2    2
        dr
           =− −             +    + v0 −                           ⑬
        dt           r2        r        R+h

物体从开始发射直至落地需要的时间为




                                             第 - 8 - 页 / 共 38 页
               R+h                          dr
         t=
                           ( R + h ) v02 + 2GM + v2 − 2GM
               R                    2

                       −
                                                             R+h
                                                         0
                               r2             r
                                                                                            ⑭
               R+h                           rdr
          =
               R
                        2 2GM  2
                        v0 −     r + 2GMr − ( R + h ) v0
                                                       2 2

                             R+h

                                                             2GM
取参量 a = − ( R + h ) v02 ， b = 2GM ， c = v0 −                      0 ，有
                       2                                 2

                                                             R+h

           = b2 − 4ac
                                                  2GM 
              = (2GM ) 2 + 4 ( R + h ) v02  v02 −
                                      2
                                                       
                                                  R+h
                                                 2
                           2       2GM 
              = 4 ( R + h )  v02 −      0
                                   R+h

利用题给积分公式，完成积分得

                  R+h            2GMRh
         t=                            − v02 ( 2 R + h ) h
              2GM − v0 ( R + h )
                     2
                                  R+h
                                                     3                                          ⑮
                     R+h            2  π          v02 R ( R + h ) − GM ( R − h ) 
           + GM                          + arcsin                             2 
                 2GM − v0 ( R + h )   2          GM ( R + h ) − v02 ( R + h ) 
                         2



                                                 2GMR
当初始速度大小为临界值 v0 =                                                时，下落时间为
                                            ( R + h )( 2R + h )
                                        3
                 2R + h  2
                   π
          t=            
             GM  2 
```
