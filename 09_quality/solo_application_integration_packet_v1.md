# 第二章 SOLO 应用文献受控接入包（V1）

## 用途与边界

本包为四篇已经完成全文阅读、但尚未接入当前候选工作稿的 SOLO 应用来源准备一次性、可复核的接入动作。它服务于第二章的核验式草稿，不替代 `SOLO-001`、`SOLO-002` 原典全文，也不修改 `08_manuscript/02_theory.md`。该正文文件目前存在并行未提交修改；在编辑窗口稳定前，不得将本包中的建议段落直接写入正文。

四篇来源均只可作为相邻应用或边界性证据：它们能够补强“分析对象是试题/项目任务要求而不是学生表现”“结构复杂性不能被经验难度、分值或公式数量替代”“分析单位、材料范围、规则和汇总方式必须公开”。它们不能证明本项目 L1--L4 的理论定义、四维框架效度、评分者身份/独立性、学生能力、教学效果，或第35届分值结论。

## 当前接入条件

| 项目 | 状态 | 证据 |
|---|---|---|
| 四篇来源全文与相关段落已读 | 已满足 | `02_literature/reference_verification.csv`；四篇阅读札记 |
| 四篇来源的可支持/禁止迁移范围 | 已满足 | 本包 CSV 与各阅读札记 |
| 关键 SOLO 原典全文与页码 | 未满足 | `SOLO-001`、`SOLO-002` 仍为待读核心来源 |
| 第二章编辑窗口稳定 | 未满足 | `08_manuscript/02_theory.md` 有并行未提交修改 |
| BibTeX、候选映射、候选清单和追溯链接入 | 未开始 | 必须在正文实际新增来源 ID 的同一轮完成 |

## 建议正文动作

待第二章稳定后，可在 2.2 的“SOLO理论及适用边界”末尾加入下列**受限背景段**，并仅在实际完成引用映射后保留对应来源 ID：

> 已读的相邻应用研究表明，SOLO可被用于描述试题或项目预设的认知复杂性，但此类分析须明确其对象是任务要求而非学生实际作答；任务的结构复杂性也不能由经验难度、分值、公式数量或区分度直接替代。[引文占位：SOLO-APP-001、SOLO-PHY-001；仅支持任务要求与学生表现、经验难度的区分]

可在 2.3 的“两层编码”说明后加入下列**报告透明度段**：

> 相邻高中物理试题分析还提示，若同时使用题干、情境、图表与参考答案说明任务结构，应公开分析单位、材料范围、判定规则、示例与汇总方式，并把这些材料分析与学生作答、正式分值和成绩证据分开记录。[引文占位：SOLO-PHY-002、SOLO-PHY-003；仅支持透明报告与任务—学生表现区分，不采用其SOLO-LPs乘积、分值加权或学生结论]

这两段均不得删除第二章已有的原典全文缺口、前结构取舍、外部效度、评分过程自声明和第35届分值限制。若四篇来源中的任一条不能在拟写段落中保持其限定用途，则不接入该条，不以“凑足参考文献数量”为理由扩写。

## 一次性接入顺序

1. 确认 `08_manuscript/02_theory.md` 的并行编辑已交接，并逐句对照四篇阅读札记；不覆盖现有边界句。
2. 将实际使用的来源 ID 加入正文占位；只使用本包所列两段的有限范围。
3. 在 `02_literature/references.bib` 补入实际使用来源的 BibTeX；在 `09_quality/g8_02_bib_lite_mapping.csv` 写入 `yes` 映射、允许用途、禁止用途和正文位置。
4. 扩展 `build_r01_candidate_references.py` 的来源 ID 识别规则与格式化条目，仅让正文已实际出现且映射合格的来源进入候选工作稿参考文献；同步审阅 `audit_r01_citation_trace.py` 的规则。
5. 按顺序运行候选参考文献生成、候选 QA、引用追溯、V17工作稿重建与输入新鲜度校验；随后重建并校验21项材料包快照，最后运行总审计和运行手册 QA。
6. 更新 `PROJECT_STATUS.md`、`TASKS.md`、`CHANGELOG.md` 和必要的主张—证据侧车；单独提交正文/引用链变更，避免混入并行文件。

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

本包当前只验证“接入准备是否齐全”。它不表示建议正文已经写入、四篇来源已经进入候选参考文献、V17已经刷新，或第二章已形成最终文献综述。
