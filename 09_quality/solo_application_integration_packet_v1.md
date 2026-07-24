# 第二章 SOLO 应用文献受控接入包（V1）

## 用途与边界

本包原为四篇已经完成全文阅读的SOLO应用来源准备一次性、可复核的接入动作。该动作已于2026-07-25完成：两段受限背景文字已写入 `08_manuscript/02_theory.md`，并同步接入BibTeX、候选映射、候选参考文献、引用追溯与V17工作稿。本记录保留接入前的原始边界和复跑顺序，供后续审计；它不替代 `SOLO-001`、`SOLO-002` 原典全文。

四篇来源均只可作为相邻应用或边界性证据：它们能够补强“分析对象是试题/项目任务要求而不是学生表现”“结构复杂性不能被经验难度、分值或公式数量替代”“分析单位、材料范围、规则和汇总方式必须公开”。它们不能证明本项目 L1--L4 的理论定义、四维框架效度、评分者身份/独立性、学生能力、教学效果，或第35届分值结论。

## 当前接入条件

| 项目 | 状态 | 证据 |
|---|---|---|
| 四篇来源全文与相关段落已读 | 已满足 | `02_literature/reference_verification.csv`；四篇阅读札记 |
| 四篇来源的可支持/禁止迁移范围 | 已满足 | 本包 CSV 与各阅读札记 |
| 关键 SOLO 原典全文与页码 | 未满足 | `SOLO-001`、`SOLO-002` 仍为待读核心来源 |
| 第二章受限正文接入 | 已完成 | 2.2节与2.3节各保留一段来源ID占位与禁止迁移语句 |
| BibTeX、候选映射、候选清单和追溯链接入 | 已完成 | 4条BibTeX与映射已登记；候选来源30项；引用追溯61条来源出现、55条显式占位 |
| V17、快照、内部交接包与总审计复跑 | 已完成 | V17输入9/9当前；快照30/30；内部交接包29/29；材料包审计16/16 |

## 建议正文动作

已在2.2的“SOLO理论及适用边界”中接入下列**受限背景段**，并保留对应来源ID：

> 已读的相邻应用研究表明，SOLO可被用于描述试题或项目预设的认知复杂性，但此类分析须明确其对象是任务要求而非学生实际作答；任务的结构复杂性也不能由经验难度、分值、公式数量或区分度直接替代。[引文占位：SOLO-APP-001、SOLO-PHY-001；仅支持任务要求与学生表现、经验难度的区分]

已在2.3的“两层编码”说明后接入下列**报告透明度段**：

> 相邻高中物理试题分析还提示，若同时使用题干、情境、图表与参考答案说明任务结构，应公开分析单位、材料范围、判定规则、示例与汇总方式，并把这些材料分析与学生作答、正式分值和成绩证据分开记录。[引文占位：SOLO-PHY-002、SOLO-PHY-003；仅支持透明报告与任务—学生表现区分，不采用其SOLO-LPs乘积、分值加权或学生结论]

这两段均不得删除第二章已有的原典全文缺口、前结构取舍、外部效度、评分过程自声明和第35届分值限制。若四篇来源中的任一条不能在拟写段落中保持其限定用途，则不接入该条，不以“凑足参考文献数量”为理由扩写。

## 一次性接入顺序

1. 逐句对照四篇阅读札记，确认第二章只保留本包所列的有限范围。
2. 核验4个来源ID均已进入正文占位、`references.bib`、`g8_02_bib_lite_mapping.csv`及候选参考文献。
3. 运行候选参考文献、引用追溯、V17输入新鲜度、快照、内部交接包、总审计、运行手册与全链路健康检查。
4. 若第二章后续改写或引文范围调整，必须重新执行上述链路；不得删除原典全文、前结构取舍、外部效度和第35届分值限制。

## 必跑命令

```bash
python3 07_analysis/scripts/validate_solo_application_integration_packet.py
python3 07_analysis/scripts/build_r01_candidate_references.py
python3 07_analysis/scripts/validate_r01_candidate_references.py
python3 07_analysis/scripts/audit_r01_citation_trace.py
python3 10_outputs/drafts/build_r01_working_draft.py
python3 07_analysis/scripts/validate_working_draft_freshness.py --require-current
python3 07_analysis/scripts/build_r01_material_package_snapshot.py
python3 07_analysis/scripts/build_r01_material_package_snapshot.py --validate
python3 07_analysis/scripts/validate_current_material_package_audit.py
python3 07_analysis/scripts/validate_r01_reproducibility_runbook.py
```

本包现记录“受限接入已完成”。这不表示SOLO原典已经读完、L1至L4理论取舍已经闭合、框架已获外部效度，或第二章已经形成最终文献综述。
