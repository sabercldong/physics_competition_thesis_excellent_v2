# 当前研究材料包完成度审计（V2）

审计日期：2026-07-25
审计对象：第35—42届全国中学生物理竞赛复赛试题任务认知要求分析的当前六章材料包。
审计目的：以当前冻结数据、脚本输出、工作稿与文献台账为准，区分可用于论文**非提交工作稿**的部分、未闭合证据与不得作出的结论。本文件不替代学校、导师、评阅人或真实参与者材料的最终核验。

## 一、当前可复现、可写入工作稿的部分

| 模块 | 当前状态 | 直接证据 | 可支持的写作范围 |
|---|---|---|---|
| 试题语料与分析单位 | 第35—42届复赛语料已按小问/相对独立任务拆为219个分析单元 | `03_corpus/item_index.csv`；`03_corpus/item_texts/`；`03_corpus/raw_papers/`；`03_corpus/raw_solutions/` | 语料范围、小问级分析单位与材料定位 |
| 当前编码与证据链 | 冻结更正表与证据链各876行，键集合与当前编码值逐键一致 | `07_analysis/data/final_coding_r01_correction_v1.csv`；`07_analysis/data/final_coding_evidence_r01_v1.csv` | 当前语料和当前规则下的可追溯描述性编码 |
| 描述性统计与结果资格 | 结果资格QA为51/51通过，统计可回到冻结表与版本化输出 | `07_analysis/scripts/validate_r01_results_eligibility.py`；`09_quality/r01_results_eligibility_qa_v1.csv`；`07_analysis/results/formal_rater_r01/correction_v1/` | 四维出现、等级分布、共现与归档评分记录的一致性描述 |
| 第四章与图件 | 结果章数值、边界句与冻结输出可逐项断言 | `08_manuscript/04_results.md`；`08_manuscript/figures/`；结果资格QA的`RE-QA-M*`与`RE-QA-B*` | 描述性结果；不作显著性、因果、学生能力或教学效果推断 |
| 案例与教学转化材料 | 案例保持题干—解答定位；教学部分已建立任务、支架与过程性产出设计参照 | `08_manuscript/05_cases_and_diagnosis.md`；`07_analysis/results/formal_rater_r01/r01_case_reselection_evidence_dossier_v1.csv` | 从任务结构提出待实施的教学任务、支架与评价设计建议 |
| 候选引用链 | 21项已读且限边界来源已连接正文ID、BibTeX、映射和候选参考文献 | `08_manuscript/07_candidate_references.md`；`09_quality/g8_02_bib_lite_mapping.csv`；`09_quality/r01_candidate_references_qa_v1.md`；`09_quality/r01_citation_trace_v1.md` | 仅按每条来源登记的允许范围支撑理论、方法或任务设计边界 |
| Word工作稿 | V17无个人信息的工作稿、输入哈希清单与QA已生成；DOCX容器、A4分页和新增中英文参考文献可定位，当前8项输入哈希均与清单一致 | `10_outputs/drafts/ECNU_非全日制专硕论文工作稿_R01_v17.docx`；`10_outputs/drafts/ECNU_非全日制专硕论文工作稿_R01_v17_inputs.json`；`09_quality/r01_working_draft_v17_qa.md`；`09_quality/r01_working_draft_v17_freshness_qa.csv` | 材料组织、文本、英文条目与结构性版式检查 |
| 学校公开规则基线 | 专业学位封皮/签名页附件、GB/T 7714-2015、30篇基线、匿名评审与当期查重处理规则均已登记 | `01_positioning/school_requirements_register.csv`；`01_positioning/ecnu_official_thesis_format_sources.md` | 最终格式与提交准备的公开基线，不替代答辩期学院细则 |

## 二、当前量化核对

| 项目 | 当前值 | 复核入口 | 解释边界 |
|---|---:|---|---|
| 分析单元 | 219 | `03_corpus/item_index.csv` | 语料与分析单位事实，不代表学生样本 |
| 当前编码/证据链记录 | 876 / 876 | `final_coding_r01_correction_v1.csv`；`final_coding_evidence_r01_v1.csv` | 每单元四维记录，不等于学生作答 |
| 结果资格检查 | 51/51通过 | `r01_results_eligibility_qa_v1.csv` | 验证项目内数值与追溯，不验证评分者身份或独立性 |
| 期望存在性一致率 / kappa | 96.12% / 0.9053 | 结果资格QA `RE-QA-R1`、`RE-QA-R2` | 仅归档A/B记录的内部一致描述 |
| 共同出现等级比较 / 一致率 / 加权kappa | 607 / 82.21% / 0.8638 | 结果资格QA `RE-QA-R3`至`RE-QA-R5` | 不构成框架外部效度或独立过程验证 |
| 文献台账 / 全文已读 / 工作稿候选 | 39 / 26 / 21 | `final_reference_closure_matrix_v1.md` | 21项已进入V17候选工作稿；另有4项SOLO应用与1项竞赛案例文献待正文稳定后受控接入 |
| 当前与30篇基线的最小全文阅读差额 | 4 | `final_reference_closure_matrix_v1.md` | 数量达标仍不自动满足相关性、著录和格式要求 |
| V17工作稿 | 25页A4；输入新鲜度8/8当前 | `r01_working_draft_v17_qa.md`；`r01_working_draft_v17_freshness_qa.csv` | 当前LibreOffice环境不能验证中文逐页排版 |

## 三、尚未闭合的关键缺口

| 缺口 | 当前事实 | 关闭条件 | 影响 |
|---|---|---|---|
| 最终文献综述 | 已读26条、工作稿候选21条，低于学校公开的至少30篇基线 | 再完成至少4条具有明确章节用途的合法全文阅读，并逐篇完成书目信息、允许主张、不可迁移范围与正文闭环 | 不能形成最终参考文献表或最终理论综述 |
| SOLO原典与理论取舍 | Biggs与Collis原典及1989论文尚未取得可用于关键定义的合法全文阅读；四条相邻应用文献仍待第二章稳定后整合 | 获得合法全文、记录关键页码并明确本项目L1-L4取舍；第二章稳定后再处理已读应用文献 | 不得把任务等级写成学生真实SOLO学习结果，理论章不能终稿 |
| 中国物理竞赛研究脉络 | 核心竞赛研究多为题录/摘要或受限全文 | 合法取得核心研究全文，摘录样本、单位、方法、发现与局限 | 国内研究比较和研究空白不得定稿 |
| 第35届分值 | 八道题的正式评分细则或原卷分值说明仍缺失 | 获得正式分值来源并登记 | 禁止分值加权、跨届分值比较、相关或趋势结论 |
| 人类参与者证据 | 无真实教师访谈、问卷、课堂记录或学生作品；伦理/备案要求也未提供 | 先取得伦理/备案与知情材料，再按真实记录开展并保存原始资料 | 第五章不能诊断学生困难、写教师共识或主张教学有效 |
| 最终格式与提交信息 | 已有公开校级基线，但答辩期学院补充要求、个人信息、AI披露与最终封皮/签名页状态未闭合 | 以实际答辩期学院通知完成逐项核对，按真实信息生成最终版与匿名版 | V15不得送审、答辩、归档或正式提交 |
| 中文版面终验 | 当前LibreOffice运行环境缺少可用CJK字体，渲染中文为方框 | 在具备中文字体的Word/WPS/校方模板环境逐页检查 | 当前PDF渲染只能证明结构、分页和英文条目，不证明中文排版 |

## 四、当前禁止的表述

1. 不把876条编码、四维分布、一致率或等级统计解释为学生能力、学生困难、教学效果、因果关系、显著性或长期命题趋势。
2. 不把RATER-A/B、ADJ-01/02和R01的自声明过程写成项目独立验证的评分者身份、独立性或专家效度证据。
3. 不对第35届进行分值统计、分值加权、跨届分值比较、相关或趋势结论。
4. 不将SOLO启发的任务认知结构等级写成学生学习结果等级。
5. 不把V15、19项候选来源或当前格式映射称为可提交终稿、盲审版或最终参考文献表。

## 五、当前可交付物与下一最小任务

当前可交付的是“可复现的六章非提交工作稿材料包”：小问级语料、冻结编码和证据链、可复算描述统计、结果图件、案例与待实施教学设计材料、21项限边界候选引用链、V17工作稿及学校公开格式基线。

下一最小任务：优先合法取得并阅读一篇与SOLO原典理论或中国物理竞赛试题研究直接相关的核心来源；若暂无合法全文入口，则保持该缺口，并先向学院或图书馆索取来源/格式材料，不以泛主题文献替代核心理论和国内研究脉络。

## 六、复跑依据

```bash
python3 07_analysis/scripts/validate_r01_results_eligibility.py
python3 07_analysis/scripts/validate_r01_candidate_references.py
python3 07_analysis/scripts/audit_r01_citation_trace.py
python3 07_analysis/scripts/validate_working_draft_freshness.py --require-current
```
