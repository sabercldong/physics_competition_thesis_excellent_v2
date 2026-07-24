# G2-03B-ACCESS SOLO全文获取审计

## 任务定位

本文件记录对SOLO核心文献全文获取情况的审计。当前目标不是扩写SOLO理论，而是确认哪些材料已经可合法访问、哪些只能使用元数据或摘要、哪些必须通过图书馆或学校数据库补齐。

## 获取尝试记录

| 编号 | 文献 | 检查来源 | 当前可访问内容 | 全文状态 | 处理决定 |
|---|---|---|---|---|---|
| SOLO-001 | Biggs & Collis, 1982, *Evaluating the Quality of Learning: The SOLO Taxonomy* | ScienceDirect图书页；UNESCO/Google Books等书目信息 | 题名、作者、出版机构、年份、ISBN/馆藏层面信息 | 未发现稳定公开全文；需图书馆或合法电子书渠道 | 保留为核心理论来源候选，不能写具体页码或详细层级定义 |
| SOLO-002 | Biggs & Collis, 1989, “Towards a Model of School-Based Curriculum Development and Assessment Using the SOLO Taxonomy” | SAGE DOI页；ERIC记录 | 题名、作者、期刊、卷期页码、DOI、摘要 | SAGE全文需访问权限；ERIC记录未提供开放全文 | 可谨慎引用摘要层面“课程开发与评价”用途，正式论述前需阅读全文 |

## 2026-07-25 复核补记

- 重新核验 ScienceDirect 图书页、SAGE DOI页和出版社 PagePlace 预览。PagePlace预览仍只覆盖14页书目信息、目录与前言片段，不含第二章层级定义或编码规则正文；其范围见 `solo_original_preview_verification_20260725.md`。
- 搜索引擎曾返回 `johnbiggs.com.au/academic/solo-taxonomy/` 的旧摘要，但2026-07-25直接访问该域名只得到“Website Under Redevelopment”停放页，已无可读取的作者说明或图示。该旧摘要不得作为当前可核验来源，更不得替代原书全文。
- 检索到的来源不明整本PDF不具有明确授权信息，按项目规则不下载、不阅读、不登记为全文；只保留出版社、图书馆、DOI页、正式机构库或明确开放许可版本作为合法入口。

## 当前可形成的最低结论

1. SOLO原书与1989年应用论文的书目信息均可追溯；
2. SOLO原始名称与1989年摘要均指向“学习结果/表现复杂性”的描述语言；
3. 本研究不能把试题本身直接称为学生SOLO学习结果等级；
4. 第二章只能继续使用“SOLO启发的任务认知结构要求等级”这一保守表述；
5. 正式定稿前必须补齐全文阅读记录、关键页码和任务/试题分析迁移边界文献。

## 对正文的约束

- 可以写：SOLO来源已定位，当前用于启发任务结构复杂性分类；
- 可以写：本研究分析的是试题要求，不是学生实际学习结果；
- 不能写：Biggs与Collis原书第几页如何定义各层级；
- 不能写：SOLO已经被证明适用于本研究的物理竞赛试题编码；
- 不能写：当前L1-L4方案已经完成理论验证。

## 后续最小动作

已整理 `02_literature/solo_fulltext_request_packet.md`，可直接用于图书馆、馆际互借、导师协助或出版社授权访问请求。继续 `G2-03B-FULLTEXT`：通过学校图书馆、馆际互借、出版社授权访问或其他合法渠道获取SOLO原书与1989年论文全文；完成后补录关键页码、可摘录短句、层级定义和迁移边界。
