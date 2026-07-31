# 第38届复赛第2题：玻璃管水银封闭气体加热过程

## 来源

- 试题文件：`03_corpus/raw_papers/cpho_38_2021_fusai_paper_solution_candidate.pdf`
- 试题页码：1
- 解答页码：7
- 题图：03_corpus/item_assets/CPHO38-Q02-figure1-page1-raw.png
- 抽取状态：题干使用页面OCR并经视觉定位大题边界；参考解答使用PDF文本层抽取。公式、特殊符号、图注和OCR错字需人工校对。

## G1-07-A1人工校对入口

- 任务：`G1-07-A1-TRANSCRIBE-38Q02`
- 题面V1视觉转写：`03_corpus/manual_review_transcripts/CPHO38-Q02_transcription_v1.md`
- 答案公式核对表：`03_corpus/manual_review_transcripts/CPHO38-Q02_formula_check_v1.csv`
- 页面证据：
  - `03_corpus/manual_review_renders/G1-07-A1/CPHO38-Q02-paper-page-1.png`
  - `03_corpus/manual_review_renders/G1-07-A1/CPHO38-Q02-solution-page-07.png`
  - `03_corpus/manual_review_renders/G1-07-A1/CPHO38-Q02-solution-page-08.png`
- 题图证据：`03_corpus/item_assets/CPHO38-Q02-figure1-page1-raw.png`
- 边界说明：第2题题面位于试题PDF第1页中下部；第1页上部为第1题，第1页下部进入第3题，仅作边界确认。答案从PDF第7页中部“二、”开始，延续至PDF第8页评分标准结束；原清单中的解答页码 `7` 已按视觉检查纠偏为 `7-8`。
- 状态说明：`CPHO38-Q02-OCR` 已建立V1视觉转写入口；`CPHO38-Q02-FORMULA` 已建立答案公式核对入口；`CPHO38-Q02-FIG` 本轮未销项，图2a裁图仍需后续人工确认或重裁/重绘判断。
- 使用限制：原OCR文本仅作错误来源对照，不得作为正式编码证据；当前未填写真实校对人和校对日期，不得声称人工校对完成。

## 题干OCR抽取文本

```text
二、如图 2a, 一端开口的游壁玻璃管烃直放置, FOWL, 玻璃答总长1= 75.0 cm, aki S=10.0 cm’,
玻璃管内用水银封闭一段理想气体，水银和理想气体之间有一薄而轻的绝热光浴活塞，气柱高度与水银柱
高度均为=25.0cm 。已知该理想气体初始温度五=400K , EMR RMAC, =iR, HH
R=8.31 J/mol'K) 为普适气体常量;水银密度 =13.6x10° kg/m? ，大气压强 p, =75.0 cmHg ，重力加速
BEX g = 9.80 mis’.
(1) 过程 A; 对封闭的气体级介加热，使水银上液而恰好到达玻璃答开口处，求过程 A 中封闭气体
对外所做的功;
(2) 过程 B: 继续对封闭气体绥慢加热，直至水银恰好全部流出为止〈洲活塞恰好与玻璃答开口平
齐)，通过计算说明过程 B 能否绥慢稳定地发生? 计竺过程 B 中封闭气体所吸收的热量。                     图2a
忽略玻璃答和水银的热脱胀效应。计每结果保留三位有效数字。
```

## 参考解答抽取文本

```text
HF    r + HO
         k=       = 0                                                         ⑩
              H'F' r  + H'O'
其中
                                                 (1 − n)r0
         HO = rmax cos  max − r0 ， rmax =
                                              1 − n cos  max
                                                  (1 − n)r0
                                       =
                  cos  max − r0 ， rmax
         H'O' = rmax                                                          ⑪
                                               1 − n cos  max
所以
             (1 − n )(1 − n cos  max ) r0
        k=                                                                    ⑫
             (1 − n)(1 − n cos  max ) r0
]


评分参考：本题 40 分。
第（1）问 20 分，①②③④⑤式各 4 分；
第（2）问 20 分，⑥⑦⑧式各 4 分，⑨⑩⑪⑫式各 2 分。


二、
（1）过程 A 中封闭气体初态体积为
                          V1 = Sh                                                       ①
温度为
                           T1 = T0                                                  ②
初始压强为
                           p1 = p0 +  gh = 4  gh                                  ③
末态压强为
                           p2 = p1                                                  ④
末态体积为
                          V2 = 2 Sh                                                 ⑤
根据理想气体物态方程得
                           p1V1 p2V2
                               =                                                    ⑥
                            T1   T2
由以上各式得
                           T2 = 2T0                                                     ⑦
     过程 A 是等压过程，此过程中封闭气体对外所做的功为
                          W1 = p1 (V2 − V1 ) = 4  ghSh = 33.3 J                        ⑧
[
或利用理想气体所做的功等于水银重力势能的增加和克服大气压对外做的功，即
                          W1 =  Shgh + p0 (V2 − V1 ) =  Shgh + 3 Shgh = 33.3 J       ⑧
由于缓慢加热，水银的动能可以忽略。
]
（2）设过程 B 中水银柱的高度为 x ，若该过程可以缓慢稳定地发生，则要求水银柱高度在不断减小的过程中，满
足气体状态方程的 x 始终有解。设对应于 x 的封闭气体压强为 p ，体积为 V ，温度为 T ，则
                           p = p0 +  gx = 3 gh +  gx                             ⑨
                                                     第 3 页 , 共 16 页
```
