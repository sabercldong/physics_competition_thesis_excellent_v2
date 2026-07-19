# G2VE-03 SOLO理论全文与迁移边界入口

## 性质声明

本文件只建立SOLO理论全文与迁移边界的复核入口，目标是把现有材料、全文缺口、可暂用边界句、真实回填字段和禁写边界整理清楚。本文不改写论文正文，不新增或定稿 `references.bib`，不升级主张证据矩阵，不补造SOLO等级定义、页码、专家意见、评分者结果或试题分析结论。

## 输入依据

- `02_literature/solo_taxonomy_source_verification.md`
- `02_literature/solo_fulltext_access_audit.md`
- `02_literature/solo_fulltext_request_packet.md`
- `02_literature/reference_verification.csv`
- `02_literature/literature_matrix.csv`
- `02_literature/literature_theory_verification_entry_v1.csv`
- `09_quality/no_return_reference_p1_gap_queue_v1.csv`
- `09_quality/no_return_reference_p1_evidence_packet_index_v1.csv`
- `09_quality/no_return_reference_p1_backfill_ready_gate_v1.csv`

## 当前结论

SOLO核心来源已经定位，但全文阅读和页码摘录尚未完成。当前只能保留“SOLO启发的任务认知结构要求等级”这一保守表述，用于说明本研究分析的是试题任务要求，而不是学生真实学习结果。

在合法全文、关键页码、迁移边界论证和后续QA完成前，SOLO部分不得定稿，不得写具体等级定义页码，不得声称SOLO已经被证明适用于全国中学生物理竞赛复赛试题分析。

## 现有材料

| 编号 | 来源 | 当前状态 | 可暂用内容 | 不足 |
|---|---|---|---|---|
| `SOLO-001` | Biggs & Collis, 1982, *Evaluating the Quality of Learning: The SOLO Taxonomy* | 书目信息已定位；未获稳定公开全文 | 可说明SOLO原始来源已定位，题名指向“Structure of the Observed Learning Outcome” | 不能写具体层级定义、页码、前结构层级取舍 |
| `SOLO-002` | Biggs & Collis, 1989, “Towards a Model of School-Based Curriculum Development and Assessment Using the SOLO Taxonomy” | DOI、卷期页码和摘要已定位；SAGE全文需权限 | 可说明SOLO有课程开发与评价应用线索 | 不能替代全文阅读，不能支撑完整迁移论证 |

## 全文缺口

当前必须补齐的真实材料包括：

1. `SOLO-001` 合法全文、电子书访问权限、纸本馆藏扫描页或馆际互借材料；
2. `SOLO-002` 出版社全文PDF、HTML全文或学校数据库访问记录；
3. SOLO层级定义相关章节或页码；
4. SOLO用于课程、评价、任务表现或学习结果描述的页码；
5. 是否保留“前结构”层级的原文依据；
6. 将SOLO迁移到“试题认知要求”分析时的适用性与限制说明，且不得把试题直接写成学生SOLO学习结果；
7. 可支持 `C2-03A/C1-04` 的页码级阅读笔记；
8. 与内部L1-L4等级命名、合并或改名相关的边界判断。

## 当前可保留的安全句式

在正文正式定稿前，只能保留以下类型的边界句：

1. SOLO核心来源已定位，但原书和1989年论文仍需合法全文阅读与页码摘录。
2. SOLO原始名称强调观察到的学习结果结构，本研究分析对象则是试题任务要求。
3. 本研究暂采用“SOLO启发的任务认知结构要求等级”表述，以避免把试题直接等同于学生学习结果。
4. 当前L1-L4等级方案属于内部分析框架准备，理论边界和前结构层级取舍仍待全文阅读、正式手册和真实评分者数据共同确认。

## 禁写边界

在全文与QA完成前，不得声称：

- 已阅读全文；
- 已记录Biggs与Collis原书或1989年论文的关键页码；
- SOLO各层级定义已经定稿；
- 前结构层级已被原文或专家正式确认应删除或保留；
- SOLO已经被证明适用于本项目复赛试题编码；
- 试题可以直接被判定为学生SOLO学习结果等级；
- SOLO等级等同于试题难度、公式数量、解题步骤数量、综合性或创新性；
- Codex内部试编码能证明SOLO迁移有效；
- 当前L1-L4等级已经完成理论验证、专家审查或真实评分者一致性检验。

## 真实回填字段

收到合法全文或授权材料后，至少应填写：

| 字段 | 说明 |
|---|---|
| `source_id` | `SOLO-001` 或 `SOLO-002` |
| `access_channel` | 学校数据库、馆际互借、导师提供、出版社授权、纸本馆藏等 |
| `access_date` | 实际获取日期 |
| `version_or_holding` | 数据库平台、馆藏号、PDF版本、扫描范围或授权说明 |
| `pages_checked` | 实际阅读页码或章节范围 |
| `definition_pages` | SOLO核心层级定义页码 |
| `application_context` | 原文用于学习结果、任务表现、课程开发、评价或其他语境 |
| `transfer_boundary` | 迁移到试题认知要求分析时允许与不允许的表述 |
| `prestructural_decision` | 前结构层级是否保留、合并、改名或排除及依据 |
| `claim_ids_supported` | 可支持的主张编号，如 `C2-03A/C1-04` |
| `citation_decision` | 可写入、暂不引用、仅作背景、排除 |
| `remaining_risk` | 仍未解决的理论或证据风险 |

## 下一最小任务

建议进入 `G2VE-03-SOLO-FULLTEXT-BOUNDARY-ENTRY-QA`：检查本入口材料和结构表的编号、路径、CSV编码换行、全文缺口、真实回填字段、安全句式和禁写边界。QA通过后，在未取得SOLO全文前，可继续处理其他不依赖SOLO全文的文献理论入口。
