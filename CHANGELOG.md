# CHANGELOG

## 2026-07-14：G3-07R 一致性计算脚本升级

- 更新 `07_analysis/scripts/compute_reliability.py`，支持正式试编码表和双评分者模板两种字段结构；
- 脚本可输出维度存在性一致率、Cohen kappa、双方均判出现时的等级一致率、加权kappa和分歧明细；
- 增加 `--allow-simulated` 保护参数，防止把Codex模拟评分者数据误当正式一致性结果；
- 使用 `04_framework/codex_simulated_round1_coding.csv` 复跑压力测试，已在 `07_analysis/results/generated/` 生成可复现输出；该目录按项目规则不作为提交对象；
- 更新 `04_framework/reliability_plan.md`，补充真实评分者数据回收后的推荐运行命令。

## 2026-07-14：G3-06S/G3-07S Codex模拟双评分者压力测试

- 新增 `04_framework/codex_simulated_round1_coding.csv`，基于24个样本小问生成Codex模拟评分者A/B共192条试编码记录；
- 新增 `04_framework/codex_simulated_disagreement_log.csv`，记录16条模拟分歧，主要集中在科学论证存在性和L3/L4等级边界；
- 新增 `04_framework/codex_simulated_reliability_stats.csv`，计算模拟维度存在性一致率、Cohen kappa、等级一致率和加权kappa；
- 新增 `04_framework/codex_simulated_reliability_report.md`，说明模拟一致性压力测试的数据、结果、局限和对手册训练的启示；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，明确模拟结果只用于训练和风险识别，不能替代真实双人独立编码与正式一致性检验。

## 2026-07-14：G3-05P Codex内部预审与V2草案

- 新增 `04_framework/codex_internal_pre_review_report.md`，记录Codex内部预审的性质、输入材料、主要发现和不可形成的结论；
- 新增 `04_framework/codex_internal_pre_review_log.csv`，结构化记录19条内部预审发现和V2草案处理方式；
- 新增 `04_framework/coding_manual_v2_draft.md`，在V1基础上强化SOLO适配边界、证据优先级、通用排除规则、科学论证边界和质疑创新保守编码原则；
- 新增 `04_framework/codebook_v2_draft.csv`，形成16个维度-等级指标的V2草案结构化版本；
- 新增 `04_framework/rater_training_packet.md` 和 `04_framework/pilot_coding_round1_template.csv`，为后续两名评分者独立试编码准备训练说明和192条空白编码记录；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，明确Codex内部预审不能替代真实专家审查，`expert_review_log.csv` 仍需真实专家意见。

## 2026-07-14：G3-05A 专家审查材料包准备

- 新增 `04_framework/expert_review_packet.md`，说明专家审查目的、对象、评分规则、样本说明、回收处理和当前边界；
- 更新 `04_framework/expert_review_form.md`，补充结构化填写文件、4级评分规则和回收修订要求；
- 新增 `04_framework/expert_panel_template.csv`，用于匿名登记专家背景、邀请状态和反馈回收日期；
- 新增 `04_framework/expert_indicator_review_form.csv`，将 `codebook.csv` 中16个指标转为专家逐项评分表；
- 新增 `04_framework/expert_review_sample_items.csv`，按每届3个样本的原则选取24个样本小问，用于暴露编码手册边界问题；
- 新增 `04_framework/expert_sample_item_review_form.csv`，为24个样本小问生成96条四维度审查记录；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，将当前阶段推进到 `G3：分析框架开发`，并明确 `G3-05` 尚未完成真实专家审查。

## 2026-07-14：G1-07 正式编码前人工校对清单

- 新增 `03_corpus/manual_review_checklist.csv`，将第35—42届60道大题整理为154条人工待核项；
- 新增 `03_corpus/manual_review_summary.md`，说明校对用途、问题类型、优先级、校对原则和当前边界；
- 问题类型包括题干OCR校对、公式与特殊符号校对、题图裁边与图注校对、第35届分值边界复核和第42届第3题解答放大图一致性核对；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，将 `G1-07` 标记为完成，并把下一步调整为按清单人工销项与准备 `G3-05` 专家审查材料包；
- 本轮不改写任何题干、参考解答或论文正文，不把 `pilot_coding.csv` 试编码作为正式统计结果。

## 2026-07-13：G1-06 第42届全卷整理与试编码

- 新增 `03_corpus/item_texts/CPHO42-Q01.md` 至 `03_corpus/item_texts/CPHO42-Q07.md`，整理第42届7道题题干OCR与参考解答抽取文本；
- 新增第42届第2、3、5、6、7题共10张题图裁切资产，保存于 `03_corpus/item_assets/`；
- 更新 `03_corpus/item_materials.csv`，登记第42届7道题的文本文件、题图文件、页码、抽取方式和校对状态；
- 更新 `03_corpus/item_index.csv`，补齐第42届29个分析单元的知识模块、情境、表征、数学工具和答案结构元数据；
- 更新 `04_framework/pilot_coding.csv`，追加第42届29个分析单元共116条 Codex 试编码记录；
- 将 `G1-06` 标记为完成：第35—42届共219个分析单元均已完成试处理；这些记录仍为试编码，正式结果前必须进行人工校对、专家审查、双人独立编码和分歧处理。

## 2026-07-13：G1-06 第41届全卷整理与试编码

- 新增 `03_corpus/item_texts/CPHO41-Q01.md` 至 `03_corpus/item_texts/CPHO41-Q07.md`，整理第41届7道题题干OCR与参考解答抽取文本；
- 新增第41届第1、2、5、6、7题题图裁切资产，保存于 `03_corpus/item_assets/`；
- 更新 `03_corpus/item_materials.csv`，登记第41届7道题的文本文件、题图文件、页码、抽取方式和校对状态；
- 更新 `03_corpus/item_index.csv`，补齐第41届32个分析单元的知识模块、情境、表征、数学工具和答案结构元数据；
- 更新 `04_framework/pilot_coding.csv`，追加第41届32个分析单元共128条 Codex 试编码记录；
- 第41届试题页使用扫描页OCR，参考解答使用PDF文本层；相关题干、公式、特殊符号、图注和OCR错字必须在正式编码前人工校对。

## 2026-07-13：G1-06 第40届全卷整理与试编码

- 新增 `03_corpus/item_texts/CPHO40-Q01.md` 至 `03_corpus/item_texts/CPHO40-Q08.md`，整理第40届8道题题干OCR与参考解答抽取文本；
- 新增第40届第1—8题题图裁切资产，保存于 `03_corpus/item_assets/`；
- 更新 `03_corpus/item_materials.csv`，登记第40届8道题的文本文件、题图文件、页码、抽取方式和校对状态；
- 更新 `03_corpus/item_index.csv`，依据题面视觉复核将第40届由21个骨架条目细化为36个分析单元，并补齐知识模块、情境、表征、数学工具和答案结构元数据；
- 更新 `04_framework/pilot_coding.csv`，追加第40届36个分析单元共144条 Codex 试编码记录；
- 第40届试题页使用扫描页OCR，参考解答使用PDF文本层；相关题干、公式、特殊符号、图注和OCR错字必须在正式编码前人工校对。

## 2026-07-13：G1-06 第39届全卷整理与试编码

- 新增 `03_corpus/item_texts/CPHO39-Q01.md` 至 `03_corpus/item_texts/CPHO39-Q07.md`，整理第39届7道题题干与参考解答抽取文本；
- 新增第39届第1、3、4、6题题图裁切资产，保存于 `03_corpus/item_assets/`；
- 更新 `03_corpus/item_materials.csv`，登记第39届7道题的文本文件、题图文件、页码、抽取方式和校对状态；
- 更新 `03_corpus/item_index.csv`，补齐第39届27个小问的知识模块、情境、表征、数学工具和答案结构元数据；
- 更新 `04_framework/pilot_coding.csv`，追加第39届27个小问共108条 Codex 试编码记录；
- 第39届PDF文本层可用；相关公式、特殊符号和图注仍需在正式编码前人工校对。

## 2026-07-13：G1-06 第38届全卷整理与试编码

- 新增 `03_corpus/item_texts/CPHO38-Q01.md` 至 `03_corpus/item_texts/CPHO38-Q08.md`，整理第38届8道题题干与参考解答抽取文本；
- 新增第38届第1—8题题图裁切资产，保存于 `03_corpus/item_assets/`；
- 更新 `03_corpus/item_materials.csv`，登记第38届8道题的文本文件、题图文件、页码、抽取方式和校对状态；
- 更新 `03_corpus/item_index.csv`，补齐第38届25个小问的知识模块、情境、表征、数学工具和答案结构元数据；
- 更新 `04_framework/pilot_coding.csv`，追加第38届25个小问共100条 Codex 试编码记录；
- 第38届题干部分使用页面OCR并经视觉定位大题边界；相关公式、特殊符号、图注和OCR错字必须在正式编码前人工校对。

## 2026-07-13：G1-06 第37届全卷OCR整理与试编码

- 新增 `03_corpus/item_texts/CPHO37-Q01.md` 至 `03_corpus/item_texts/CPHO37-Q08.md`，整理第37届8道题题干与参考解答OCR抽取文本；
- 新增第37届第1、3、5、6、7、8题题图裁切资产，保存于 `03_corpus/item_assets/`；
- 更新 `03_corpus/item_materials.csv`，登记第37届8道题的文本文件、题图文件、页码、抽取方式和校对状态；
- 更新 `03_corpus/item_index.csv`，补齐第37届22个小问的知识模块、情境、表征、数学工具和答案结构元数据，并按页面视觉复核修正答案页定位；
- 更新 `04_framework/pilot_coding.csv`，追加第37届22个小问共88条 Codex 试编码记录；
- 第37届PDF文本层仅有页码，本轮采用扫描页OCR；相关题干、解答、公式和特殊符号必须在正式编码前人工校对。

## 2026-07-13：G1-06 第36届全卷整理与试编码

- 新增 `03_corpus/item_texts/CPHO36-Q01.md` 至 `03_corpus/item_texts/CPHO36-Q07.md`，整理第36届7道题题干与参考解答抽取文本；
- 新增第36届第1、2、3、4、5、7题题图裁切资产，保存于 `03_corpus/item_assets/`；
- 更新 `03_corpus/item_materials.csv`，登记第36届7道题的文本文件、题图文件、页码、抽取方式和校对状态；
- 更新 `03_corpus/item_index.csv`，补齐第36届22个小问的知识模块、情境、表征、数学工具和答案结构元数据；
- 更新 `04_framework/pilot_coding.csv`，追加第36届22个小问共88条 Codex 试编码记录；
- 根据用户确认，处理过程中不再做外部真伪检验，直接将已导入PDF作为本研究试题材料；这些记录仍为试编码，不作为正式统计结果。

## 2026-07-13：G1-06 第35届全卷整理与试编码

- 新增 `03_corpus/item_texts/CPHO35-Q03.md` 至 `03_corpus/item_texts/CPHO35-Q08.md`，补齐第35届第3—8题题干与参考解答抽取文本；
- 新增第35届第3、4、6、7题题图裁切资产，保存于 `03_corpus/item_assets/`；
- 更新 `03_corpus/item_materials.csv`，登记第35届8道题的文本文件、题图文件、页码、抽取方式和校对状态；
- 更新 `03_corpus/item_index.csv`，补齐第35届第3—8题共20个小问的知识模块、情境、表征、数学工具和答案结构元数据；
- 更新 `04_framework/pilot_coding.csv`，追加第35届第3—8题共80条 Codex 试编码记录；
- 第35届现有26个小问均已有四维度试编码，共104条；这些记录仍为试编码，不作为正式统计结果。

## 2026-07-13：G1-06/G3 试题整理与理论试分析样例

- 新增 `04_framework/item_analysis_workflow.md`，固定题干、解答、题图、元数据和试编码的处理顺序；
- 新增 `03_corpus/item_texts/CPHO35-Q01.md` 与 `03_corpus/item_texts/CPHO35-Q02.md`，整理第35届第1、2题题干与参考解答抽取文本；
- 新增 `03_corpus/item_assets/CPHO35-Q02-figure1-page1-raw.png`，裁取第35届第2题题图原图；
- 新增 `03_corpus/item_materials.csv`，登记样例题目的文本文件、题图文件、页码和抽取状态；
- 更新 `03_corpus/item_index.csv`，回填第35届第1、2题共6个小问的知识模块、情境、表征、数学工具和答案结构元数据；
- 更新 `04_framework/codebook.csv`，补入四个科学思维维度及 L1-L4 认知结构要求草案；
- 更新 `04_framework/pilot_coding.csv`，完成第35届第1、2题共6个小问的 Codex 试编码样例，共24条；
- 更新项目状态和任务清单，将 `G1-06` 与 `G3-04` 标记为进行中。

## 2026-07-13：G1-05 小问级索引

- 更新 `03_corpus/item_index.csv`，建立第35—42届复赛试题小问级骨架索引，共204条；
- 为每条记录登记届次、年份、题号、小问号、试题页码、答案起始页和所属大题分值边界；
- 对知识模块、情境、表征、数学工具、答案结构统一标记为 `待编码`，留待 `G1-06`；
- 对第37、40、41、42届及第38届部分页面保留 OCR 待人工复核标记；
- 更新项目状态和任务清单，将 `G1-05` 标记为完成。

## 2026-07-13：用户确认语料并转入索引

- 用户确认已导入的第35—42届PDF即为本研究使用的复赛试题/答案；
- 停止继续进行官方网页来源检索；
- 将 `G1-01`、`G1-02`、`G1-03` 标记为完成，将下一步调整为 `G1-05` 小问级索引；
- 在 `03_corpus/metadata_verification.md` 中保留资料来源边界说明。

## 2026-07-13：G1 本地候选语料导入

- 从 `/Users/dongxingxi/Downloads/35-42届复赛试题` 复制第35—42届复赛试题/答案候选PDF到 `03_corpus/raw_papers/` 和 `03_corpus/raw_solutions/`；
- 更新 `03_corpus/paper_inventory.csv`，登记届次、候选年份、文件路径、页数、SHA-256和来源等级；
- 更新 `03_corpus/provenance_log.csv`，记录本地来源路径、导入日期、校验值和初始核验状态；
- 将候选文件来源等级暂定为 `S3`，后续由用户确认为当前研究语料；
- 更新项目状态和任务清单，将 `G1-01`、`G1-02` 标为进行中，将 `G1-04` 标为完成。

## 2026-07-13：G1-03 PDF内部元数据核验

- 新增 `03_corpus/metadata_verification.md`；
- 对第35—42届候选PDF进行文本抽取、PDF信息读取和扫描页OCR；
- 核验第36—42届的PDF内部年份/日期、题数、总分和主要分值结构；
- 记录第35届仍需复核考试日期与分值；
- 在 `03_corpus/paper_inventory.csv` 的备注中写入每届PDF内部核验结论；
- 将 `G1-03` 标记为进行中；后续已根据用户确认转入小问级索引准备。

## 2026-07-13：G0-01 资料盘点

- 新增 `01_positioning/material_inventory.md`；
- 核对 `00_originals/` 三份原始材料的校验值与清单一致；
- 将项目资料分为“真实存在、仅在初稿出现、当前缺失、需要导师确认”四类；
- 评估路线A、路线B、路线C的数据需求、方法风险、时间成本和预期贡献；
- 明确初稿中的年份、试题统计、问卷结果、实验数据、显著性结论和参考文献目前不能继承；
- 更新项目状态与任务清单，将下一最小任务调整为 `G0-02`。

## 2026-07-13 — 优秀论文版V2

- 重建项目定位与论文主线；
- 新增稳健型、进阶型题目与研究路线；
- 将SOLO使用调整为“SOLO启发的任务认知结构等级”；
- 新增专家审查、双人编码、分歧裁决、课堂设计型研究模板；
- 新增优秀论文评分标准、质量关卡和答辩准备模块；
- 新增可复现数据检查与一致性分析脚本；
- 保存三份原始材料并标记为只读参考。
