# G2-01 文献检索策略

## 任务边界

本文件完成的是“数据库与检索式制定”，不是正式检索结果报告。`search_log.csv` 中本轮新增记录均为计划检索式，结果数、筛选数和纳入数均标为待检索或0；后续实际进入数据库检索时，必须另起日志行记录真实日期、结果数量、筛选数量和纳入数量。

本阶段不得：

- 把计划检索式写成已经完成的系统检索；
- 根据题名或摘要写文献结论；
- 把未读全文文献写入第二章正式论述；
- 将搜索引擎摘要替代文献阅读；
- 直接继承初稿参考文献中的结论或格式。

## 数据库与来源层级

| 来源组 | 拟使用来源 | 用途 | 备注 |
|---|---|---|---|
| 官方文件 | 教育部官网、国家课程标准发布渠道、学校可访问的政策文件库 | 核验科学思维、核心素养、课程标准表述 | 优先记录文件名、发布机构、年份、章节和页码 |
| 中文学术数据库 | 中国知网、万方、维普、读秀或学校图书馆中文资源 | 物理竞赛试题研究、科学思维教学研究、SOLO中文应用、学位论文 | 具体可用库以学校权限为准 |
| 英文学术数据库 | ERIC、Web of Science、Scopus、EBSCO Education Source、Google Scholar | SOLO原始理论、科学推理/论证测评、内容分析方法、设计型研究 | Google Scholar只作补充发现来源 |
| 方法文献来源 | 教育测量、内容分析、评分者一致性、设计型研究方法书或论文 | 支持编码、信度、一致性和教学转化方法 | 核心方法文献优先阅读全文 |

## 主题块与检索式

### T1 课程标准中的科学思维

中文检索式：

`普通高中物理课程标准 科学思维 模型建构 科学推理 科学论证 质疑创新`

英文补充：

`physics curriculum scientific thinking model construction scientific reasoning argumentation innovation`

目标：核验第二章2.1中科学思维四维度的官方或课程依据。

### T2 科学思维测评与物理问题解决

中文检索式：

`物理教育 科学思维 测评 模型建构 科学推理 科学论证`

英文检索式：

`physics education scientific reasoning model construction scientific argumentation assessment`

目标：支持“本研究分析试题任务要求而非学生真实能力”的边界说明，并为维度操作化提供测评研究依据。

### T3 SOLO理论原始文献与教育应用

中文检索式：

`SOLO 分类理论 物理 教育 试题 分析`

英文检索式：

`SOLO taxonomy structure of observed learning outcomes physics education assessment task analysis`

目标：核验SOLO理论的核心概念、等级含义和用于任务分析时的适用边界。

### T4 SOLO用于试题任务分析的争议

中文检索式：

`SOLO 试题分析 认知要求 学习结果 边界`

英文检索式：

`SOLO taxonomy item analysis cognitive demand limitation assessment`

目标：为“SOLO启发的任务认知结构要求等级”提供限制性依据，避免把试题等级写成学生学习结果等级。

### T5 物理竞赛试题研究

中文检索式：

`全国中学生物理竞赛 复赛试题 分析 科学思维 核心素养`

补充检索式：

`物理竞赛试题 内容分析 认知要求 教学策略`

英文检索式：

`physics olympiad problems analysis cognitive demand scientific reasoning`

目标：确认既有竞赛试题研究主要分析对象、方法和不足，为绪论与第二章研究空白提供依据。

### T6 内容分析与评分者一致性

中文检索式：

`内容分析 编码手册 评分者一致性 Cohen kappa 教育研究`

英文检索式：

`content analysis coding manual interrater reliability Cohen kappa education research`

目标：支持第三章方法中的双评分者、分歧裁决和一致性报告。

### T7 教学转化与设计型研究

中文检索式：

`物理教学 设计型研究 教学转化 评价量规 学生作品`

英文检索式：

`design based research physics education teaching intervention rubric student work`

目标：支持第五、六章中“结果—问题—策略—任务—评价”链条和教师/课堂证据要求。

## 筛选口径

### 纳入标准

- 与科学思维、SOLO、物理竞赛试题、内容分析、评分者一致性或教学转化直接相关；
- 书目信息可核验，至少能定位摘要，核心文献能获得全文；
- 能记录研究问题、样本、方法、发现、局限和可支持的论文主张；
- 经典理论文献不设时间下限，经验研究优先近10年，物理竞赛研究可适当放宽。

### 排除标准

- 仅为解题赏析且不能支持研究设计或文献综述主张；
- 来源、作者、年份或出版信息不可核验；
- 只在二手文献中出现，无法追溯原文；
- 与本研究主线关系弱；
- 重复发表或内容高度重复；
- 只有口号式教学建议，没有样本、方法或证据。

## 记录规则

1. 计划检索式记录在 `search_log.csv`，`results` 写 `待检索`；
2. 实际检索时另起新行，不覆盖计划行；
3. 候选文献先进入 `reference_verification.csv`；
4. 阅读后再进入 `literature_matrix.csv`；
5. 排除文献写入 `exclusion_log.csv`；
6. 只有已核验并实际引用的文献进入 `references.bib`。

## G2-01完成判据

本任务完成后，只能说明数据库、来源组、检索式和筛选口径已经制定；不能说明文献综述已经完成。后续最小任务为 `G2-02`：核验课程标准中的科学思维定义，并将官方来源记录到 `reference_verification.csv` 和 `literature_matrix.csv`。
