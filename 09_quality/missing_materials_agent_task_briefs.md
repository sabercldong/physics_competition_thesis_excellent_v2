# 缺失材料智能体任务卡

## 性质声明

本文件是对 `09_quality/missing_materials_agent_handoff.md` 的扩展说明，供其他智能体、人类助理或资料整理者按项领取任务。它只把缺失材料写成可执行任务卡，不代表任何缺失材料已经补齐，也不放行正式编码、正式统计、论文结果章、教学效果结论或主张矩阵升级。

## 领取总规则

- 项目根目录固定为 `/Users/dongxingxi/physics_competition_thesis_excellent_v2`。
- 领取任何任务前必须先读 `00_READ_ME_FIRST.md`、`AGENTS.md`、`MASTER_PLAN.md`、`PROJECT_STATUS.md`、`TASKS.md` 和 `09_quality/initial_audit_v2.md`。
- 每个智能体领取任务时先声明 `brief_id`、会读取的输入文件、预计交付文件、不会做的事项和验收方式。
- 没有真实来源时写“待核实”“未收到真实材料”或“未见明示证据”，不得自行补齐。
- 智能体不得冒充真实专家、导师、竞赛教师、评分者、教师、学生或校对人。
- 交付后必须进入对应QA；通过QA前，不得把材料写入论文正文，不得升级主张矩阵。
- 任何CSV交付必须为UTF-8 BOM和LF换行。

## 当前派单顺序

1. 先做P0：`AGTB-01` 至 `AGTB-05`，因为它们直接阻塞格式、正式编码、正式统计和引用。
2. 再做P1：`AGTB-06` 至 `AGTB-11`，因为它们决定第五章证据、外部反馈、图件和分值边界。
3. 最后做P2：`AGTB-12`，用于题目与路线锁定；没有真实确认时保持待决定。

## 任务卡总表

| 任务卡 | 对应缺口 | 优先级 | 建议领取者 | 当前放行状态 |
|---|---|---|---|---|
| `AGTB-01` | `AGH-01` 学校格式与提交规则核验任务卡 | P0 | 学校规范资料智能体 | 不放行正文定稿 |
| `AGTB-02` | `AGH-02` 154项人工校对真实回填任务卡 | P0 | 语料人工终核智能体 | 不放行正式编码 |
| `AGTB-03` | `AGH-03` 真实评分者独立编码任务卡 | P0 | 评分者交接协调智能体 | 等待真实评分者和QA |
| `AGTB-04` | `AGH-04` 正式统计与结果复现任务卡 | P0 | 正式统计复现智能体 | 等待正式编码裁决表 |
| `AGTB-05` | `AGH-05` 文献全文与引用核验任务卡 | P0 | 文献全文核验智能体 | 不放行未核引用 |
| `AGTB-06` | `AGH-06` 真实专家/导师/竞赛教师反馈接收任务卡 | P1 | 外部反馈接收智能体 | 不放行专家有效性结论 |
| `AGTB-07` | `AGH-07` 教师访谈或焦点访谈资料任务卡 | P1 | 教师访谈资料智能体 | 不放行教学效果结论 |
| `AGTB-08` | `AGH-08` 问卷资料核查任务卡 | P1 | 问卷数据核验智能体 | 不放行问卷结果 |
| `AGTB-09` | `AGH-09` 课堂/教学实验/学生作品核查任务卡 | P1 | 课堂证据核验智能体 | 不放行教学效果 |
| `AGTB-10` | `AGH-10` C组图件定稿核查任务卡 | P1 | 图件终核智能体 | 不放行论文图件 |
| `AGTB-11` | `AGH-11` D组分值与附属图核查任务卡 | P1 | 分值边界核验智能体 | 不放行分值统计 |
| `AGTB-12` | `AGH-12` 最终题目与研究路线确认任务卡 | P2 | 路线确认整理智能体 | 不自动锁定章节 |

## 逐项任务卡

### AGTB-01 学校格式与提交规则核验任务卡

- 对应总清单：`AGH-01`；
- 优先级：P0；
- 建议领取者：学校规范资料智能体；
- 先读文件：00_READ_ME_FIRST.md;AGENTS.md;01_positioning/school_requirements_request_packet.md;01_positioning/school_requirements_register.csv；
- 执行动作：只从学校官网、学院通知、导师或用户提供文件读取规则；逐条记录来源、日期、适用范围和原文位置；无法定位来源时写待核实；把文件或截图另存到用户指定的非公开资料区并在登记表标路径。；
- 交付物：更新01_positioning/school_requirements_register.csv；补充01_positioning/school_requirements_request_packet.md的已获得/未获得状态；新增规则来源说明或文件索引。；
- 验收门槛：每条规则必须有来源、日期或文件版本、适用范围、原文位置；没有来源的规则不得进入格式定稿。；
- 禁止边界：不得猜测学校模板、字数、查重率、AI披露、匿名评审、引用格式或优秀论文标准；不得把网络泛化规则当成本校规则。；
- 交付后QA：学校格式适配QA；通过前不能定稿版式、匿名版或提交版。；
- 当前放行状态：不放行正文定稿。

### AGTB-02 154项人工校对真实回填任务卡

- 对应总清单：`AGH-02`；
- 优先级：P0；
- 建议领取者：语料人工终核智能体；
- 先读文件：03_corpus/manual_review_real_return_priority_packet.md;03_corpus/manual_review_real_return_priority_packet_v1.csv;03_corpus/manual_review_remaining_return_handoff_register.md;03_corpus/manual_review_remaining_return_handoff_register_v1.csv;03_corpus/manual_review_return_integration_protocol.md；
- 执行动作：按A组首批38个题目级材料包和B/C/D剩余78项逐项核对；对照原PDF、页面证据图、V1转写稿、公式核对表、候选图；每项填写校对人或代号、日期、决定、修订说明和复核后证据位置；不确定时保留待核实并说明原因。；
- 交付物：真实回填副本；接收登记更新；每个issue_id的核对决定；必要修订说明；复核后证据路径；不能销项清单。；
- 验收门槛：154项中每个关闭候选必须有真实校对人或代号、日期、决定和证据路径；不能只写已检查；冲突项必须进冲突登记。；
- 禁止边界：不得代填虚构校对人、日期或决定；不得把内部OCR、公式入口、候选图或智能体视觉判断写成真实人工终核；不得关闭证据不足条目。；
- 交付后QA：路线A接收QA和人工终核整合QA；通过前不放行正式编码。；
- 当前放行状态：不放行正式编码。

### AGTB-03 真实评分者独立编码任务卡

- 对应总清单：`AGH-03`；
- 优先级：P0；
- 建议领取者：评分者交接协调智能体；
- 先读文件：04_framework/rater_independent_coding_instructions_v1.md;04_framework/rater_handoff_lock_v1.md;07_analysis/data/formal_coding_rater_A_template.csv;07_analysis/data/formal_coding_rater_B_template.csv;07_analysis/data/formal_adjudication_template.csv；
- 执行动作：先确认AGTB-02已通过QA；向真实评分者A/B分发表格和说明；保持独立填写；回收时登记评分者代码、资质说明、日期和版本；整理分歧但不替评分者裁决。；
- 交付物：评分者A正式编码表；评分者B正式编码表；评分者交接记录；分歧清单；裁决准备表。；
- 验收门槛：两名评分者独立填写；每条编码含证据摘录；评分者代码、日期、版本和文件校验值完整；分歧可追踪到题号和分析单元。；
- 禁止边界：不得由智能体冒充真实评分者；不得复制内部候选编码为正式编码；不得伪造一致性或裁决结果。；
- 交付后QA：正式编码字段QA、一致性计算准备QA、分歧裁决QA。；
- 当前放行状态：等待真实评分者和QA。

### AGTB-04 正式统计与结果复现任务卡

- 对应总清单：`AGH-04`；
- 优先级：P0；
- 建议领取者：正式统计复现智能体；
- 先读文件：07_analysis/results/reviewed/prep30_formal_data_dictionary.csv;07_analysis/results/reviewed/prep30_formal_output_placeholders.csv;07_analysis/results/reviewed/prep30_analysis_readiness_report.md;03_corpus/route_b_task_boundary_v1.csv；
- 执行动作：只在正式裁决唯一表存在且通过QA后启动；冻结输入数据；运行可复现脚本；生成分布、共现、分组比较和图表；记录软件版本、脚本路径、样本量、异常和解释边界。；
- 交付物：07_analysis/results/formal/正式输出表；图形；运行日志；统计口径说明；结果解释边界；可复现README。；
- 验收门槛：每个结果都能从正式输入表和脚本重现；每张表图有样本量、字段口径、脚本来源和限制说明。；
- 禁止边界：不得使用内部预演结果当正式结果；不得在无脚本输出时写百分比、趋势、p值、效应量、显著性或长期规律。；
- 交付后QA：G5结果复现QA；通过后才给第四章写作任务。；
- 当前放行状态：等待正式编码裁决表。

### AGTB-05 文献全文与引用核验任务卡

- 对应总清单：`AGH-05`；
- 优先级：P0；
- 建议领取者：文献全文核验智能体；
- 先读文件：09_quality/no_return_reference_claim_queue.md;09_quality/no_return_reference_claim_queue_v1.csv;09_quality/no_return_reference_p1_gap_queue.md;09_quality/no_return_reference_p1_gap_queue_v1.csv;02_literature/reference_verification.csv;02_literature/literature_matrix.csv；
- 执行动作：合法获取全文或确认无法获取；阅读全文中与主张相关的章节；记录页码、图表编号、原文支持范围和局限；把不能支持的主张列入排除或降格队列；提出bib修订建议但不直接把未核文献升格。；
- 交付物：阅读笔记；页码/图表复核表；引用动作队列；排除来源登记；可核验bib修订建议；未获全文清单。；
- 验收门槛：每条拟引用来源有完整书目信息、访问来源、已读位置、支持的具体主张和不能支持的边界。；
- 禁止边界：不得用搜索摘要、题录、目录或未读全文替代阅读；不得编造文献结论；不得新增未核验正式参考文献。；
- 交付后QA：引用QA和主张矩阵侧车合并准备。；
- 当前放行状态：不放行未核引用。

### AGTB-06 真实专家/导师/竞赛教师反馈接收任务卡

- 对应总清单：`AGH-06`；
- 优先级：P1；
- 建议领取者：外部反馈接收智能体；
- 先读文件：04_framework/expert_review_packet.md;04_framework/expert_review_form.md;04_framework/expert_review_sample_items.csv;04_framework/expert_review_log.csv;AGENTS.md；
- 执行动作：准备审查材料和匿名化说明；只接收真实人员反馈；登记人员类别、日期、反馈文本或附件、采纳/未采纳决定；若用户决定不做外部审查，则记录为未开展，不把内部预审改写成专家审查。；
- 交付物：04_framework/expert_review_log.csv更新；反馈摘录；采纳说明；未采纳理由；修订建议清单；未开展说明。；
- 验收门槛：每条反馈有真实来源、日期、材料版本、反馈内容和处理决定；匿名化规则明确。；
- 禁止边界：不得让智能体冒充专家、导师或竞赛教师；不得把Codex内部预审、模拟审查或用户口头偏好写成真实专家审查。；
- 交付后QA：外部反馈QA；通过后才可作为边界性外部反馈证据。；
- 当前放行状态：不放行专家有效性结论。

### AGTB-07 教师访谈或焦点访谈资料任务卡

- 对应总清单：`AGH-07`；
- 优先级：P1；
- 建议领取者：教师访谈资料智能体；
- 先读文件：05_fieldwork/data_collection_log.csv;05_fieldwork/ethics_and_data_management_plan.md;05_fieldwork/consent_template.md;MASTER_PLAN.md;AGENTS.md；
- 执行动作：确认是否有真实访谈；若有，整理同意记录、时间、对象类别、录音或文字、转写、匿名化编号和编码规则；若没有，输出未收集说明和第五章不能写的结论清单。；
- 交付物：05_fieldwork/interview_log.csv；访谈转写或来源索引；教师反馈编码表；匿名化说明；不能支持结论清单。；
- 验收门槛：每条教师反馈可回到真实访谈记录；元数据和匿名化编号完整；教师意见与试题客观统计分开。；
- 禁止边界：不得编造教师、访谈、反馈、身份或日期；不得用教师意见证明试题客观分布或教学效果。；
- 交付后QA：教师证据QA；通过后仅支持教学转化边界性论述。；
- 当前放行状态：不放行教学效果结论。

### AGTB-08 问卷资料核查任务卡

- 对应总清单：`AGH-08`；
- 优先级：P1；
- 建议领取者：问卷数据核验智能体；
- 先读文件：05_fieldwork/data_collection_log.csv;05_fieldwork/ethics_and_data_management_plan.md;01_positioning/non_inheritable_claims_inventory.md;09_quality/initial_audit_v2.md；
- 执行动作：核查是否存在真实问卷、题项、发放记录和原始数据；若有，建立匿名化数据、清洗日志和分析脚本；若没有，登记为无真实问卷材料，并给出正文删除/占位建议。；
- 交付物：05_fieldwork/questionnaire_manifest.csv；匿名化原始数据索引；清洗日志；分析脚本；结果边界说明；无数据删减建议。；
- 验收门槛：样本量、题项、发放时间、数据文件、清洗过程和统计脚本可复查；无真实数据则明确不能写问卷结果。；
- 禁止边界：不得继承初稿问卷比例；不得编造60名学生、均值、t值、p值、显著性或问卷信效度。；
- 交付后QA：问卷QA；无数据则转正文删减/占位任务。；
- 当前放行状态：不放行问卷结果。

### AGTB-09 课堂/教学实验/学生作品核查任务卡

- 对应总清单：`AGH-09`；
- 优先级：P1；
- 建议领取者：课堂证据核验智能体；
- 先读文件：06_teaching_validation/classroom_data_manifest.csv;05_fieldwork/ethics_and_data_management_plan.md;05_fieldwork/data_collection_log.csv;MASTER_PLAN.md;AGENTS.md；
- 执行动作：核查是否有真实课堂实施、教学方案、实施偏离、学生作品、评分量规和前后任务；若有，匿名化并建立索引；若没有，明确第五章只能写设计方案或采证工具，不能写效果。；
- 交付物：06_teaching_validation/classroom_data_manifest.csv更新；学生作品索引；评分量规；实施偏离记录；教学迭代说明；不能支持结论清单。；
- 验收门槛：每个教学效果主张能回到真实课堂或学生作品；评分标准和实施过程可复查；短期变化解释有边界。；
- 禁止边界：不得编造课堂、学生作品、对照组、前后测、显著提升或长期科学思维提升；不得把教学策略方案写成验证结果。；
- 交付后QA：教学验证QA；通过前第五章不得写效果结论。；
- 当前放行状态：不放行教学效果。

### AGTB-10 C组图件定稿核查任务卡

- 对应总清单：`AGH-10`；
- 优先级：P1；
- 建议领取者：图件终核智能体；
- 先读文件：03_corpus/no_return_c_figure_queue.md;03_corpus/no_return_c_figure_queue_v1.csv;03_corpus/manual_review_c_closure_packet.md;03_corpus/manual_review_c_closure_packet_v1.csv；
- 执行动作：逐项对照原PDF页面、原裁图、候选图、对照图和图件核对入口；判断保留、重裁、重绘或弃用；填写核对人、日期、论文可用性和证据路径；边界不清时保留待核实。；
- 交付物：C组图件真实回填表；图件定稿决定；重绘需求清单；最终证据路径；不可用图件清单。；
- 验收门槛：每个图件决定有真实核对人/日期/证据路径；图号、图注、裁边和论文可用性可复查。；
- 禁止边界：不得把候选图当最终图；不得自行确认论文可用性；不得无证据重绘或改写图注。；
- 交付后QA：C组图件QA；通过前不能插入论文定稿图。；
- 当前放行状态：不放行论文图件。

### AGTB-11 D组分值与附属图核查任务卡

- 对应总清单：`AGH-11`；
- 优先级：P1；
- 建议领取者：分值边界核验智能体；
- 先读文件：03_corpus/no_return_d_score_solfig_queue.md;03_corpus/no_return_d_score_solfig_queue_v1.csv;03_corpus/manual_review_d_closure_packet.md;03_corpus/manual_review_d_closure_packet_v1.csv；
- 执行动作：查找第35届正式评分细则或可核验证据；逐题确认是否存在大题分值、分问分值或评分标准；核对第42届第3题解答放大图与附录图号边界；找不到时写未见明示证据。；
- 交付物：D组分值/附属图真实核对表；缺失说明；可用证据路径；不得用项清单。；
- 验收门槛：每项有真实核对记录；找不到证据时明确未见明示证据且不推断；附属图边界说明可定位到页。；
- 禁止边界：不得猜测第35届分值或分问分值；不得生成第35届分值统计；不得确认第42届第3题附属图定稿边界。；
- 交付后QA：D组QA；通过前不放行分值统计或附图结论。；
- 当前放行状态：不放行分值统计。

### AGTB-12 最终题目与研究路线确认任务卡

- 对应总清单：`AGH-12`；
- 优先级：P2；
- 建议领取者：路线确认整理智能体；
- 先读文件：01_positioning/route_convergence_memo.md;01_positioning/title_decision.md;01_positioning/scope_decision_memo.md;MASTER_PLAN.md;PROJECT_STATUS.md；
- 执行动作：汇总当前证据状态和路线A/B/C条件；区分用户决定、导师决定和项目内部建议；登记是否保留问卷、课堂验证、外部审查或只做边界性教学转化；输出未确认项。；
- 交付物：路线确认记录；题目建议；章节删减/保留建议；未确认项清单；后续任务切换建议。；
- 验收门槛：确认来源清楚；用户决定和导师决定分开；未确认事项保持待决定；章节建议不依赖虚构材料。；
- 禁止边界：不得冒充导师决定；不得写导师已确认；不得为了正文完整保留无真实证据的问卷、准实验或教学效果章。；
- 交付后QA：章节结构锁定QA或继续待决定。；
- 当前放行状态：不自动锁定章节。

## 交付回报模板

其他智能体完成任务后，应按以下格式回报：

- 领取任务卡：`AGTB-XX`；
- 新增或修改文件：列出路径；
- 使用的真实来源：列出文件、链接、日期或用户提供材料；
- 已能支持的论文内容：只写证据能支持的范围；
- 仍不能支持的论文内容：明确列出禁写结论；
- 需要进入的QA：列出下一步；
- 建议Git提交信息：中文、单一任务。

## 当前不能写入论文的结论

- 不能声称154项人工终核问题已经真实销项。
- 不能声称已有真实评分者A/B独立编码、一致性计算或分歧裁决。
- 不能声称已有正式维度分布、SOLO等级分布、共现关系、趋势、p值、效应量或显著性。
- 不能声称已有真实专家、导师或竞赛教师审查。
- 不能声称已有真实问卷结果、教师访谈结论、课堂实验结果、学生作品分析或教学策略显著有效。
- 不能继承初稿中的年份、比例、问卷、实验、显著性和未核验参考文献结论。

## 下一最小任务

`G1-07-MISSING-MATERIALS-AGENT-TASK-BRIEFS-QA`：检查本任务卡CSV和报告是否编号连续、字段完整、输入路径可定位、禁止边界充分，并确认没有把任何缺失材料写成已完成证据。

## 输出边界

本任务只新增任务卡报告和CSV索引，并更新项目台账；不修改 `00_originals/`，不修改 `08_manuscript/`，不修改 `09_quality/claim_evidence_matrix.csv`，不修改 `02_literature/references.bib`，不创建 `03_corpus/manual_review_returns/`。
