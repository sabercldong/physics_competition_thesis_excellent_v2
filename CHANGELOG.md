# CHANGELOG

## 2026-07-19：G1-07-A-CLOSURE-PACKET A组真实人工终核回填包

- 新增 `03_corpus/manual_review_a_closure_packet.md` 和 `03_corpus/manual_review_a_closure_packet_v1.csv`，为A组76项高风险OCR、公式与特殊符号问题生成真实人工终核回填入口；
- 核对A组38个材料ID，对应V1视觉转写稿和公式核对表均已定位，入口文件存在率为100%；
- 回填表保留真实校对人、真实校对日期、校对决定、是否需修订、修订说明和复核后证据位置等空白栏位；本轮不代填、不关闭任何条目；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，将下一最小任务调整为 `G1-07-A-CLOSURE-PACKET-QA`，准备按38个材料ID生成题目级校对单视图。

## 2026-07-19：G1-07-COVERAGE-TO-CLOSURE-PLAN 人工校对真实销项计划

- 新增 `03_corpus/manual_review_closure_plan.md` 和 `03_corpus/manual_review_closure_plan_v1.csv`，在154项人工校对入口覆盖审计基础上，建立逐项真实销项路线；
- 将154项分为4类：题面/答案页证据入口加真实人工终核98项、图件终核或必要时重绘47项、补正式评分细则/原卷分值说明8项、真实人工终核和附录图号边界确认1项；
- 记录当前154项均缺真实校对人或真实校对日期，因此真实销项数仍为0；本轮不关闭任何人工校对问题；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，将下一最小任务调整为 `G1-07-A-CLOSURE-PACKET`，优先为A组76项高风险OCR、公式与特殊符号问题生成真实人工终核回填包。

## 2026-07-19：G4-01-NO-RATER-BOUNDARY-APPLY 第3至5章无评分者边界应用审计

- 新增 `09_quality/g4_01_no_rater_boundary_apply_report.md` 和 `09_quality/g4_01_no_rater_boundary_apply_audit.csv`，逐项审查第3章方法准备说明、第4章正式结果占位、第5章候选案例与教学转化证据需求、主张证据矩阵和无评分者边界路线包；
- 关键词扫描命中“显著”“证明”“充分”等高风险词，但逐段核对后均处于禁止外推、不能证明或证据不足语境，未发现需要立即改写的越界结果句；
- 本轮不修改第3至5章正文，也不修改 `09_quality/claim_evidence_matrix.csv`，避免把历史未提交正文和质量矩阵改动一并纳入本次提交；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，将下一最小任务调整为 `G1-07-COVERAGE-TO-CLOSURE-PLAN`：从154项人工校对入口覆盖转向真实销项计划。

## 2026-07-19：G4-01-NO-RATER-BOUNDARY-PACKET 无真实评分者时的边界路线

- 新增 `07_analysis/results/reviewed/g4_01_no_rater_boundary_packet.md`，汇总当前 `G4-01` 所处位置、已准备材料、致命阻塞、可继续做的内部工作和不能提前生成的正式结论；
- 新增 `07_analysis/results/reviewed/g4_01_no_rater_next_routes.csv`，将真实评分者路线、内部边界路线、人工销项路线、教学证据路线、文献与学校规范路线、正式论文定稿路线逐一标明可执行状态、所需输入、允许输出和禁止声称；
- 明确正式 `G4-01` 在没有真实A/B评分者填写表时仍处于阻塞状态，不能计算一致性、不能裁决、不能生成正式结果；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，将下一最小任务调整为 `G4-01-NO-RATER-BOUNDARY-APPLY`；若后续回收真实A/B评分者模板，则立即切回正式 `G4-01`。

## 2026-07-19：G1-07-FOLLOWUP-COVERAGE-AUDIT 人工校对入口覆盖审计

- 新增 `03_corpus/manual_review_coverage_audit.md` 和 `03_corpus/manual_review_coverage_audit_v1.csv`，逐条审计154项人工校对问题的入口覆盖、证据字段、校对人/日期和正式使用边界；
- 核对 `03_corpus/manual_review_checklist.csv` 与 `manual_review_priority_followup.csv`，确认两表均为154条且 `issue_id` 完全一致；
- 记录当前入口覆盖率为100%：A组76项、B组22项、C组47项、D组9项均已建立入口或内部记录；
- 记录真实人工销项数仍为0：154项均未填写真实校对人和真实校对日期，因此不得写成正式人工校对完成；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，将下一步边界调整为：若回收真实A/B评分者模板则进入 `G4-01`，否则只能继续完善内部复核材料和论文证据边界说明。

## 2026-07-19：G1-07-D1-SCORE-35Q01 第35届第1题分值边界核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO35-Q01_score_boundary_check_v1.csv`，登记第35届第1题题面页、答案页、下一题排除边界和分值使用边界；
- 追加更新 `03_corpus/manual_review_d1_batch_log.csv`、`manual_review_d1_render_index.csv` 和 `manual_review_d1_batch_summary.md`，记录D组队列第153项 `CPHO35-Q01-SCORE`；
- 复制第35届第1题题面第1页和答案第6至9页证据图至 `03_corpus/manual_review_renders/G1-07-D1/`，作为本轮分值复核证据页包；
- 更新 `03_corpus/item_texts/CPHO35-Q01.md`、`item_materials.csv`、`item_index.csv`、`manual_review_checklist.csv` 和 `manual_review_priority_followup.csv`，将 `CPHO35-Q01-SCORE` 推进为“分值边界核对入口完成，待最终复核”；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，将下一最小任务调整为 `G1-07-FOLLOWUP-COVERAGE-AUDIT`；
- 本轮明确记录：当前题面第1页可确认第1题和两个小问，但未见大题分值或小问分值标注；答案第6至9页为题面重印和参考解答，未见评分标准或小问分值拆分；第9页下半部进入第2题，仅作下一题排除边界。不得据此生成第35届第1题正式分值统计、评分结论或论文附录分值。

## 2026-07-19：G1-07-D1-SOLFIG-42Q03 第42届第3题解答放大图一致性核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO42-Q03_solution_figure_large_check_v1.csv`，登记第42届第3题题解图3a/3b/3c的小图、放大图、端口标注、连接关系和使用边界；
- 追加更新 `03_corpus/manual_review_d1_batch_log.csv`、`manual_review_d1_render_index.csv` 和 `manual_review_d1_batch_summary.md`，记录D组队列第152项 `CPHO42-Q03-SOLFIG`；
- 复制第42届第3题题面第2至3页、解答第7至10页和题解图放大页第26至27页证据图至 `03_corpus/manual_review_renders/G1-07-D1/`，作为本轮放大图核对证据页包；
- 更新 `03_corpus/item_texts/CPHO42-Q03.md`、`item_materials.csv`、`item_index.csv`、`manual_review_checklist.csv` 和 `manual_review_priority_followup.csv`，将 `CPHO42-Q03-SOLFIG` 推进为“解答放大图一致性核对入口完成，待最终复核”；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，将下一最小任务调整为队列第153项 `CPHO35-Q01-SCORE`；
- 本轮明确记录：第26页对应题解图3a/3b，第27页对应题解图3c；题解图3a-3c是参考解答等效电路图，不是题面图3a-3d的一一原样放大。不得据此声称第42届第3题题面图、题解图、附录用图或图号命名边界已完成正式人工校对。

## 2026-07-19：G1-07-D1-SCORE-35Q07 第35届第7题分值边界核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO35-Q07_score_boundary_check_v1.csv`，登记第35届第7题题面页、答案页、下一题排除边界和分值使用边界；
- 追加更新 `03_corpus/manual_review_d1_batch_log.csv`、`manual_review_d1_render_index.csv` 和 `manual_review_d1_batch_summary.md`，记录D组队列第154项 `CPHO35-Q07-SCORE`；
- 复制第35届第7题题面第4页、答案第31至35页和第36页下一题边界证据图至 `03_corpus/manual_review_renders/G1-07-D1/`，作为本轮分值复核证据页包；
- 更新 `03_corpus/item_texts/CPHO35-Q07.md`、`item_materials.csv`、`item_index.csv`、`manual_review_checklist.csv` 和 `manual_review_priority_followup.csv`，将 `CPHO35-Q07-SCORE` 推进为“分值边界核对入口完成，待最终复核”；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，将下一最小任务纠正为队列第152项 `CPHO42-Q03-SOLFIG`；
- 本轮明确记录：当前题面第4页可确认第7题和两个小问，但未见大题分值或小问分值标注；答案第31至35页为题面重印、图a/图b和参考解答，未见评分标准或小问分值拆分；第35页下半部进入第8题，第36页仅作下一题排除边界。不得据此生成第35届第7题正式分值统计、评分结论或论文附录分值。

## 2026-07-19：G1-07-D1-SCORE-35Q06 第35届第6题分值边界核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO35-Q06_score_boundary_check_v1.csv`，登记第35届第6题题面页、答案页、下一题排除边界和分值使用边界；
- 追加更新 `03_corpus/manual_review_d1_batch_log.csv`、`manual_review_d1_render_index.csv` 和 `manual_review_d1_batch_summary.md`，记录D组队列第151项 `CPHO35-Q06-SCORE`；
- 复制第35届第6题题面第3页和答案第28至31页证据图至 `03_corpus/manual_review_renders/G1-07-D1/`，作为本轮分值复核证据页包；
- 更新 `03_corpus/item_texts/CPHO35-Q06.md`、`item_materials.csv`、`item_index.csv`、`manual_review_checklist.csv` 和 `manual_review_priority_followup.csv`，将 `CPHO35-Q06-SCORE` 推进为“分值边界核对入口完成，待最终复核”；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，将下一最小任务调整为 `G1-07-D1-SCORE-35Q07`；
- 本轮明确记录：当前题面第3页下半部可确认第6题和三个小问，但未见大题分值或小问分值标注；答案第28至31页为题面重印和参考解答，未见评分标准或小问分值拆分；第31页下半部进入第7题，仅作下一题排除边界。不得据此生成第35届第6题正式分值统计、评分结论或论文附录分值。

## 2026-07-18：G1-07-D1-SCORE-35Q05 第35届第5题分值边界核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO35-Q05_score_boundary_check_v1.csv`，登记第35届第5题题面页、答案页、下一题排除边界和分值使用边界；
- 追加更新 `03_corpus/manual_review_d1_batch_log.csv`、`manual_review_d1_render_index.csv` 和 `manual_review_d1_batch_summary.md`，记录D组队列第150项 `CPHO35-Q05-SCORE`；
- 复制第35届第5题题面第2至3页和答案第19至28页证据图至 `03_corpus/manual_review_renders/G1-07-D1/`，作为本轮分值复核证据页包；
- 更新 `03_corpus/item_texts/CPHO35-Q05.md`、`item_materials.csv`、`item_index.csv`、`manual_review_checklist.csv` 和 `manual_review_priority_followup.csv`，将 `CPHO35-Q05-SCORE` 推进为“分值边界核对入口完成，待最终复核”；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，将下一最小任务调整为 `G1-07-D1-SCORE-35Q06`；
- 本轮明确记录：当前题面第2页下部至第3页上部可确认第5题和三个小问，但未见大题分值或小问分值标注；答案第19至28页为参考解答，未见评分标准或小问分值拆分；第28页下部进入第6题，仅作下一题排除边界。不得据此生成第35届第5题正式分值统计、评分结论或论文附录分值。

## 2026-07-17：G1-07-D1-SCORE-35Q08 第35届第8题分值边界核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO35-Q08_score_boundary_check_v1.csv`，登记第35届第8题题面页、答案页、末页边界和分值使用边界；
- 追加更新 `03_corpus/manual_review_d1_batch_log.csv`、`manual_review_d1_render_index.csv` 和 `manual_review_d1_batch_summary.md`，记录D组队列第149项 `CPHO35-Q08-SCORE`；
- 复制第35届第8题题面第5页和答案第35至38页证据图至 `03_corpus/manual_review_renders/G1-07-D1/`，作为本轮分值复核证据页包；
- 更新 `03_corpus/item_texts/CPHO35-Q08.md`、`item_materials.csv`、`item_index.csv`、`manual_review_checklist.csv` 和 `manual_review_priority_followup.csv`，将 `CPHO35-Q08-SCORE` 推进为“分值边界核对入口完成，待最终复核”；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，将下一最小任务调整为 `G1-07-D1-SCORE-35Q05`；
- 本轮明确记录：当前题面第5页可确认第8题和四个小问，但未见大题分值或小问分值标注；答案第35至38页为参考解答，未见评分标准或小问分值拆分；第38页为PDF末页，不存在下一题边界页。不得据此生成第35届第8题正式分值统计、评分结论或论文附录分值。

## 2026-07-17：G1-07-D1-SCORE-35Q04 第35届第4题分值边界核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO35-Q04_score_boundary_check_v1.csv`，登记第35届第4题题面页、答案页、下一题排除边界和分值使用边界；
- 追加更新 `03_corpus/manual_review_d1_batch_log.csv`、`manual_review_d1_render_index.csv` 和 `manual_review_d1_batch_summary.md`，记录D组队列第148项 `CPHO35-Q04-SCORE`；
- 复制第35届第4题题面第2页、答案第16至19页和第20页下一题边界确认图至 `03_corpus/manual_review_renders/G1-07-D1/`，作为本轮分值复核证据页包；
- 更新 `03_corpus/item_texts/CPHO35-Q04.md`、`item_materials.csv`、`item_index.csv`、`manual_review_checklist.csv` 和 `manual_review_priority_followup.csv`，将 `CPHO35-Q04-SCORE` 推进为“分值边界核对入口完成，待最终复核”；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，将下一最小任务调整为 `G1-07-D1-SCORE-35Q08`；
- 本轮明确记录：当前题面第2页可确认第4题和四个小问，但未见大题分值或小问分值标注；答案第16至19页为参考解答，未见评分标准或小问分值拆分；第20页仅作下一题排除边界。不得据此生成第35届第4题正式分值统计、评分结论或论文附录分值。

## 2026-07-17：G1-07-D1-SCORE-35Q03 第35届第3题分值边界核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO35-Q03_score_boundary_check_v1.csv`，登记第35届第3题题面页、答案页、下一题排除边界和分值使用边界；
- 追加更新 `03_corpus/manual_review_d1_batch_log.csv`、`manual_review_d1_render_index.csv` 和 `manual_review_d1_batch_summary.md`，记录D组队列第147项 `CPHO35-Q03-SCORE`；
- 复制第35届第3题题面第1至2页、答案第13至16页和第17页下一题边界确认图至 `03_corpus/manual_review_renders/G1-07-D1/`，作为本轮分值复核证据页包；
- 更新 `03_corpus/item_texts/CPHO35-Q03.md`、`item_materials.csv`、`item_index.csv`、`manual_review_checklist.csv` 和 `manual_review_priority_followup.csv`，将 `CPHO35-Q03-SCORE` 推进为“分值边界核对入口完成，待最终复核”；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，将下一最小任务调整为 `G1-07-D1-SCORE-35Q04`；
- 本轮明确记录：当前题面第1页页底至第2页上半部可确认第3题和四个小问，但未见大题分值或小问分值标注；答案第13至16页为参考解答，未见评分标准或小问分值拆分；第17页仅作下一题排除边界。不得据此生成第35届第3题正式分值统计、评分结论或论文附录分值。

## 2026-07-17：G1-07-D1-SCORE-35Q02 第35届第2题分值边界核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO35-Q02_score_boundary_check_v1.csv`，登记第35届第2题题面页、答案页、下一题排除边界和分值使用边界；
- 新增 `03_corpus/manual_review_d1_batch_log.csv`、`manual_review_d1_render_index.csv` 和 `manual_review_d1_batch_summary.md`，建立D组分值边界复核记录结构；
- 复制第35届第2题题面第1页、答案第9至13页和第14页下一题边界确认图至 `03_corpus/manual_review_renders/G1-07-D1/`，作为本轮分值复核证据页包；
- 更新 `03_corpus/item_texts/CPHO35-Q02.md`、`item_materials.csv`、`item_index.csv`、`manual_review_checklist.csv` 和 `manual_review_priority_followup.csv`，将 `CPHO35-Q02-SCORE` 推进为“分值边界核对入口完成，待最终复核”；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，将下一最小任务调整为 `G1-07-D1-SCORE-35Q03`；
- 本轮明确记录：当前题面第1页可确认第2题和四个小问，但未见大题分值或小问分值标注；答案第9至13页为参考解答，未见评分标准或小问分值拆分；第14页仅作下一题排除边界。不得据此生成第35届第2题正式分值统计、评分结论或论文附录分值。

## 2026-07-17：G1-07-C1-FIG-38Q02 第38届第2题题图核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO38-Q02_figure_check_v1.csv`，登记第38届第2题图2a的来源页、原始裁图、重裁候选、裁框和边界说明；
- 新增 `03_corpus/item_assets/CPHO38-Q02-figure2a-page1-recrop-v1.png`，作为题面图2a重裁候选图；
- 新增 `03_corpus/manual_review_renders/G1-07-C1/CPHO38-Q02-paper-page-1.png`、`CPHO38-Q02-paper-page-1-figure2a-crop-box.png` 和 `CPHO38-Q02-figure2a-check-contact-v1.png`，记录来源页、裁框和原图/候选图对照；
- 更新 `03_corpus/manual_review_c1_batch_log.csv`、`manual_review_c1_render_index.csv` 和 `manual_review_c1_batch_summary.md`，记录C组队列第145项 `CPHO38-Q02-FIG` 的题图核对入口；
- 更新 `03_corpus/manual_review_checklist.csv`、`manual_review_priority_followup.csv`、`item_materials.csv` 和 `item_index.csv`，将 `CPHO38-Q02-FIG` 推进为“题图核对入口完成，待最终复核”；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，将下一最小任务调整为 `G1-07-D1-SCORE-35Q02`；
- 本轮明确记录：原始裁图只保留图2a右侧竖直玻璃管局部和图号，左侧混入第2题题干正文残字；重裁候选从题面第1页生成，去除正文残字并保留竖直玻璃管示意和图2a图号，未纳入第1题图1a或第3题图3a。本轮不改写论文正文，不修改原始PDF，不补造正式论文插图、真实校对人或校对日期。

## 2026-07-17：G1-07-C1-FIG-37Q05 第37届第5题题图核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO37-Q05_figure_check_v1.csv`，登记第37届第5题图5a的来源页、原始裁图、重裁候选、裁框和边界说明；
- 新增 `03_corpus/item_assets/CPHO37-Q05-figure5a-page3-recrop-v1.png`，作为题面图5a重裁候选图；
- 新增 `03_corpus/manual_review_renders/G1-07-C1/CPHO37-Q05-paper-page-3.png`、`CPHO37-Q05-paper-page-3-figure5a-crop-box.png` 和 `CPHO37-Q05-figure5a-check-contact-v1.png`，记录来源页、裁框和原图/候选图对照；
- 更新 `03_corpus/manual_review_c1_batch_log.csv`、`manual_review_c1_render_index.csv` 和 `manual_review_c1_batch_summary.md`，记录C组队列第144项 `CPHO37-Q05-FIG` 的题图核对入口；
- 更新 `03_corpus/manual_review_checklist.csv`、`manual_review_priority_followup.csv`、`item_materials.csv` 和 `item_index.csv`，将 `CPHO37-Q05-FIG` 推进为“题图核对入口完成，待最终复核”；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，将下一最小任务调整为 `G1-07-C1-FIG-38Q02`；
- 本轮明确记录：原始裁图保留相对论飞行器示意图主体、`O-xy` 坐标系、甲乙丙、速度方向箭头、距离 `d`、惯性系 `Σ` 和图号，但左侧与底部混入邻近题干正文；重裁候选从题面第3页生成，去除正文残字并保留图5a主体、关键标签和图号，未纳入同页下半部第6题图件。本轮不改写论文正文，不修改原始PDF，不补造正式论文插图、真实校对人或校对日期。

## 2026-07-17：G1-07-C1-FIG-37Q01 第37届第1题题图核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO37-Q01_figure_check_v1.csv`，登记第37届第1题图1a的来源页、原始裁图、重裁候选、裁框和边界说明；
- 新增 `03_corpus/item_assets/CPHO37-Q01-figure1a-page1-recrop-v1.png`，作为题面图1a重裁候选图；
- 新增 `03_corpus/manual_review_renders/G1-07-C1/CPHO37-Q01-paper-page-1.png`、`CPHO37-Q01-paper-page-1-figure1a-crop-box.png` 和 `CPHO37-Q01-figure1a-check-contact-v1.png`，记录来源页、裁框和原图/候选图对照；
- 更新 `03_corpus/manual_review_c1_batch_log.csv`、`manual_review_c1_render_index.csv` 和 `manual_review_c1_batch_summary.md`，记录C组队列第143项 `CPHO37-Q01-FIG` 的题图核对入口；
- 更新 `03_corpus/manual_review_checklist.csv`、`manual_review_priority_followup.csv`、`item_materials.csv` 和 `item_index.csv`，将 `CPHO37-Q01-FIG` 推进为“题图核对入口完成，待最终复核”；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，将下一最小任务调整为 `G1-07-C1-FIG-37Q05`；
- 本轮明确记录：原始裁图保留空气弹簧模型主体、阀门、附加气室、主气室、篓上负载和图号，但左侧与底部混入邻近题干正文；重裁候选去除正文残字并保留图1a主体、主要标签和图号，未纳入同页下部第2题。本轮不改写论文正文，不修改原始PDF，不补造正式论文插图、真实校对人或校对日期。

## 2026-07-17：G1-07-C1-FIG-36Q02 第36届第2题题图核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO36-Q02_figure_check_v1.csv`，登记第36届第2题图a的来源页、原始裁图、重裁候选、裁框和边界说明；
- 新增 `03_corpus/item_assets/CPHO36-Q02-figure2a-page2-recrop-v1.png`，作为题面图a重裁候选图；
- 新增 `03_corpus/manual_review_renders/G1-07-C1/CPHO36-Q02-paper-page-2.png`、`CPHO36-Q02-paper-page-2-figure2a-crop-box.png` 和 `CPHO36-Q02-figure2a-check-contact-v1.png`，记录来源页、裁框和原图/候选图对照；
- 更新 `03_corpus/manual_review_c1_batch_log.csv`、`manual_review_c1_render_index.csv` 和 `manual_review_c1_batch_summary.md`，记录C组队列第142项 `CPHO36-Q02-FIG` 的题图核对入口；
- 更新 `03_corpus/manual_review_checklist.csv`、`manual_review_priority_followup.csv`、`item_materials.csv` 和 `item_index.csv`，将 `CPHO36-Q02-FIG` 推进为“题图核对入口完成，待最终复核”；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，将下一最小任务调整为 `G1-07-C1-FIG-37Q01`；
- 本轮明确记录：原始裁图保留图a主体、两轮、平板、把手、`2l/l/r/m/2m`、把手前端/末端和图注，未见明显邻近正文残字；重裁候选保留完整图a并排除下方第3题正文；答案页第12页复印题面图a，第14页另有解题图c/d，均不作为本轮题面图销项对象。本轮不改写论文正文，不修改原始PDF，不补造正式论文插图、真实校对人或校对日期。

## 2026-07-17：G1-07-C1-FIG-36Q01 第36届第1题题图核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO36-Q01_figure_check_v1.csv`，登记第36届第1题图a/图b的来源页、原始裁图、重裁候选、裁框和边界说明；
- 新增 `03_corpus/item_assets/CPHO36-Q01-figure1ab-page1-recrop-v1.png`，作为题面图a/图b去除题干残字后的重裁候选图；
- 新增 `03_corpus/manual_review_renders/G1-07-C1/CPHO36-Q01-paper-page-1.png`、`CPHO36-Q01-paper-page-1-figure1ab-crop-box.png` 和 `CPHO36-Q01-figure1ab-check-contact-v1.png`，记录来源页、裁框和原图/候选图对照；
- 更新 `03_corpus/manual_review_c1_batch_log.csv`、`manual_review_c1_render_index.csv` 和 `manual_review_c1_batch_summary.md`，记录C组队列第141项 `CPHO36-Q01-FIG` 的题图核对入口；
- 更新 `03_corpus/manual_review_checklist.csv`、`manual_review_priority_followup.csv`、`item_materials.csv` 和 `item_index.csv`，将 `CPHO36-Q01-FIG` 推进为“题图核对入口完成，待最终复核”；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，将下一最小任务调整为 `G1-07-C1-FIG-36Q02`；
- 本轮明确记录：原始裁图保留图a/图b主体与关键标注，但上方混入题干文字；重裁候选去除上方题干残字并排除下方第2题正文；答案页第10页解题图a/b不作为本轮题面图销项对象。本轮不改写论文正文，不修改原始PDF，不补造正式论文插图、真实校对人或校对日期。

## 2026-07-17：G1-07-C1-FIG-35Q07 第35届第7题题图核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO35-Q07_figure_check_v1.csv`，登记第35届第7题题面页图a/图b、答案页图a和答案页图b的来源页、候选图、裁框和边界说明；
- 新增 `03_corpus/item_assets/CPHO35-Q07-figure7ab-page4-recrop-v1.png`，作为题面页图a/图b保守重裁候选；
- 新增 `03_corpus/item_assets/CPHO35-Q07-figure7a-solution-page32-recrop-v1.png` 和 `CPHO35-Q07-figure7b-solution-page33-recrop-v1.png`，作为答案页图a/图b参考候选，用于补充核对题面页裁图缺失风险；
- 新增 `03_corpus/manual_review_renders/G1-07-C1/CPHO35-Q07-paper-page-4.png`、答案页第32/33页证据、三张裁框定位图和 `CPHO35-Q07-figure7ab-check-contact-v1.png`，记录原始题面裁图、题面候选和答案页参考候选对照；
- 更新 `03_corpus/manual_review_c1_batch_log.csv`、`manual_review_c1_render_index.csv` 和 `manual_review_c1_batch_summary.md`，记录C组队列第140项 `CPHO35-Q07-FIG` 的题图核对入口；
- 更新 `03_corpus/manual_review_checklist.csv`、`manual_review_priority_followup.csv`、`item_materials.csv` 和 `item_index.csv`，将 `CPHO35-Q07-FIG` 推进为“题图核对入口完成，待最终复核”；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，将下一最小任务调整为 `G1-07-C1-FIG-36Q01`；
- 本轮明确记录：原始题面裁图中图a主体、图a标签和底部图注不完整，题面页重裁候选仍受页底排版限制；答案页参考候选只用于后续核对，不等同于正式论文插图定稿；本轮不改写论文正文，不修改原始PDF，不补造正式论文插图、真实校对人或校对日期。

## 2026-07-17：G1-07-C1-FIG-42Q07 第42届第7题题图核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO42-Q07_figure_check_v1.csv`，登记第42届第7题图7a来源页、原始裁图、保留候选图、来源页裁框和新旧对照证据；
- 新增 `03_corpus/item_assets/CPHO42-Q07-figure7a-page5-recrop-v1.png`，保留图7a原始裁图完整主体作为候选图；
- 新增 `03_corpus/manual_review_renders/G1-07-C1/CPHO42-Q07-paper-page-5.png`、`CPHO42-Q07-paper-page-5-figure7a-crop-box.png` 和 `CPHO42-Q07-figure7a-check-contact-v1.png`，记录图7a来源位置和原图/候选图对照；
- 更新 `03_corpus/manual_review_c1_batch_log.csv`、`manual_review_c1_render_index.csv` 和 `manual_review_c1_batch_summary.md`，记录C组队列第139项 `CPHO42-Q07-FIG` 的题图核对入口；
- 更新 `03_corpus/manual_review_checklist.csv`、`manual_review_priority_followup.csv`、`item_materials.csv` 和 `item_index.csv`，将 `CPHO42-Q07-FIG` 推进为“题图核对入口完成，待最终复核”；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，将下一最小任务调整为 `G1-07-C1-FIG-35Q07`；
- 本轮明确记录：图7a原始裁图已保留圆柱形自聚焦光纤、内部螺旋光线路径、`z` 轴方向箭头和图号，第5页上半部第6题尾部不得纳入本题证据；本轮不改写论文正文，不修改原始PDF，不补造正式论文插图、真实校对人或校对日期。

## 2026-07-17：G1-07-C1-FIG-42Q03 第42届第3题题图核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO42-Q03_figure_check_v1.csv`，登记第42届第3题图3a、图3b、图3c、图3d的来源页、原始裁图、候选图、裁框和新旧对照证据；
- 新增或更新 `03_corpus/item_assets/CPHO42-Q03-figure3a-page2-recrop-v1.png`、`CPHO42-Q03-figure3b-page2-recrop-v1.png`、`CPHO42-Q03-figure3c-page3-recrop-v1.png` 和 `CPHO42-Q03-figure3d-page3-recrop-v1.png`，其中图3a、图3c基于原始裁图内部保守修剪，图3b、图3d保留原始裁图完整主体作为候选；
- 新增或更新 `03_corpus/manual_review_renders/G1-07-C1/CPHO42-Q03-paper-page-2.png`、`CPHO42-Q03-paper-page-3.png`、两张裁框定位图和 `CPHO42-Q03-figure3a3b3c3d-check-contact-v1.png`，记录题图来源位置和原图/候选图对照；
- 更新 `03_corpus/manual_review_c1_batch_log.csv`、`manual_review_c1_render_index.csv` 和 `manual_review_c1_batch_summary.md`，记录C组队列第138项 `CPHO42-Q03-FIG` 的题图核对入口；
- 更新 `03_corpus/manual_review_checklist.csv`、`manual_review_priority_followup.csv`、`item_materials.csv` 和 `item_index.csv`，将 `CPHO42-Q03-FIG` 推进为“题图核对入口完成，待最终复核”；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，将下一最小任务调整为 `G1-07-C1-FIG-42Q07`；
- 本轮明确记录：图3a原始裁图底部混入图3b的 `I4` 箭头，图3c原始裁图底部混入题干文字，第3页中部第4题和下部第5题图5a不得纳入本题证据；`CPHO42-Q03-SOLFIG` 解答放大图一致性仍待另行复核；本轮不改写论文正文，不修改原始PDF，不补造正式论文插图、真实校对人或校对日期。

## 2026-07-17：G1-07-C1-FIG-40Q04 第40届第4题题图核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO40-Q04_figure_check_v1.csv`，登记第40届第4题图4a、图4b、图4c、图4d/图4e的来源页、原始裁图、重裁候选图、裁框和新旧对照证据；
- 新增 `03_corpus/item_assets/CPHO40-Q04-figure4a-page2-recrop-v1.png`、`CPHO40-Q04-figure4b-page2-recrop-v1.png`、`CPHO40-Q04-figure4c-page3-recrop-v1.png` 和 `CPHO40-Q04-figure4d4e-page3-recrop-v1.png`，基于第40届试题PDF第2-3页题面证据生成图4a/图4b/图4c/图4d4e候选图；
- 新增 `03_corpus/manual_review_renders/G1-07-C1/CPHO40-Q04-paper-page-2.png`、`CPHO40-Q04-paper-page-3.png`、两张裁框定位图和 `CPHO40-Q04-figure4a4b4c4d4e-check-contact-v1.png`，记录题图来源位置和原图/候选图对照；
- 更新 `03_corpus/manual_review_c1_batch_log.csv`、`manual_review_c1_render_index.csv` 和 `manual_review_c1_batch_summary.md`，记录C组队列第137项 `CPHO40-Q04-FIG` 的题图核对入口；
- 更新 `03_corpus/manual_review_checklist.csv`、`manual_review_priority_followup.csv`、`item_materials.csv` 和 `item_index.csv`，将 `CPHO40-Q04-FIG` 推进为“题图核对入口完成，待最终复核”；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，将下一最小任务调整为 `G1-07-C1-FIG-42Q03`；
- 本轮明确记录：图4a/图4b/图4d/图4e原始裁图混入题干或小问正文，第3页下半部第5题图5a不得纳入本题证据；本轮不改写论文正文，不修改原始PDF，不补造正式论文插图、真实校对人或校对日期。

## 2026-07-17：G1-07-C1-FIG-39Q01 第39届第1题题图核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO39-Q01_figure_check_v1.csv`，登记第39届第1题图1a/图1b来源页、原始裁图、整页重裁候选图、来源页裁框和新旧对照证据；
- 新增 `03_corpus/item_assets/CPHO39-Q01-figure1a-page1-recrop-v1.png` 和 `CPHO39-Q01-figure1b-page1-recrop-v1.png`，基于第39届试题PDF第1页整页题面证据重裁图1a/图1b；
- 新增 `03_corpus/manual_review_renders/G1-07-C1/CPHO39-Q01-paper-page-1.png`、`CPHO39-Q01-paper-page-1-figure1a1b-crop-box.png` 和 `CPHO39-Q01-figure1a1b-check-contact-v1.png`，记录图1a/图1b来源位置和原图/候选图对照；
- 更新 `03_corpus/manual_review_c1_batch_log.csv`、`manual_review_c1_render_index.csv` 和 `manual_review_c1_batch_summary.md`，记录C组队列第136项 `CPHO39-Q01-FIG` 的题图核对入口；
- 更新 `03_corpus/manual_review_checklist.csv`、`manual_review_priority_followup.csv`、`item_materials.csv` 和 `item_index.csv`，将 `CPHO39-Q01-FIG` 推进为“题图核对入口完成，待最终复核”；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，将下一最小任务调整为 `G1-07-C1-FIG-40Q04`；
- 本轮明确记录：图1a原始裁图底部混入下一段题干，图1b原始裁图右侧反射镜文字被裁切；本轮不改写论文正文，不修改原始PDF，不补造正式论文插图、真实校对人或校对日期。

## 2026-07-17：G1-07-C1-FIG-38Q08 第38届第8题题图核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO38-Q08_figure_check_v1.csv`，登记第38届第8题图8a来源页、原始裁图、整页重裁候选图、来源页裁框和新旧对照证据；
- 新增 `03_corpus/item_assets/CPHO38-Q08-figure8a-page3-recrop-v1.png`，基于第38届试题PDF第3页整页题面证据重裁图8a，去除原始裁图左侧与底部正文残字，并保留电动汽车简化模型、前后轮、`L/2`、`M`、`m`、`r`、后轮力矩和图号；
- 新增 `03_corpus/manual_review_renders/G1-07-C1/CPHO38-Q08-paper-page-3.png`、`CPHO38-Q08-paper-page-3-figure8a-crop-box.png` 和 `CPHO38-Q08-figure8a-check-contact-v1.png`，记录图8a来源位置和原图/候选图对照；
- 更新 `03_corpus/manual_review_c1_batch_log.csv`、`manual_review_c1_render_index.csv` 和 `manual_review_c1_batch_summary.md`，记录C组队列第135项 `CPHO38-Q08-FIG` 的题图核对入口；
- 更新 `03_corpus/manual_review_checklist.csv`、`manual_review_priority_followup.csv`、`item_materials.csv` 和 `item_index.csv`，将 `CPHO38-Q08-FIG` 推进为“题图核对入口完成，待最终复核”；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，将下一最小任务调整为 `G1-07-C1-FIG-39Q01`；
- 本轮明确记录：同页图7a和第4页正文不得混入第8题图件证据；本轮不改写论文正文，不修改原始PDF，不补造正式论文插图、真实校对人或校对日期。

## 2026-07-17：G1-07-C1-FIG-38Q07 第38届第7题题图核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO38-Q07_figure_check_v1.csv`，登记第38届第7题图7a来源页、原始裁图、整页重裁候选图、来源页裁框和新旧对照证据；
- 新增 `03_corpus/item_assets/CPHO38-Q07-figure7a-page3-recrop-v1.png`，基于第38届试题PDF第3页整页题面证据重裁图7a，补足原始裁图缺失的完整车身、后轮、`L/2`、`M`、`h`、`r` 等关键标注，并保留坡面、前后轮、`m`、`theta` 和图号；
- 新增 `03_corpus/manual_review_renders/G1-07-C1/CPHO38-Q07-paper-page-3.png`、`CPHO38-Q07-paper-page-3-figure7a-crop-box.png` 和 `CPHO38-Q07-figure7a-check-contact-v1.png`，记录图7a来源位置和原图/候选图对照；
- 更新 `03_corpus/manual_review_c1_batch_log.csv`、`manual_review_c1_render_index.csv` 和 `manual_review_c1_batch_summary.md`，记录C组队列第134项 `CPHO38-Q07-FIG` 的题图核对入口；
- 更新 `03_corpus/manual_review_checklist.csv`、`manual_review_priority_followup.csv`、`item_materials.csv` 和 `item_index.csv`，将 `CPHO38-Q07-FIG` 推进为“题图核对入口完成，待最终复核”，并同步答案页范围为 `16-18`；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，将下一最小任务调整为 `G1-07-C1-FIG-38Q08`；
- 本轮明确记录：第3页上方图6a和下方图8a不得混入第7题图件证据；本轮不改写论文正文，不修改原始PDF，不补造正式论文插图、真实校对人或校对日期。

## 2026-07-17：G1-07-C1-FIG-38Q04 第38届第4题题图核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO38-Q04_figure_check_v1.csv`，登记第38届第4题图4a来源页、原始裁图、整页重裁候选图、来源页裁框和新旧对照证据；
- 新增 `03_corpus/item_assets/CPHO38-Q04-figure4a-page2-recrop-v1.png`，基于第38届试题PDF第2页整页题面证据重裁图4a，去除原始裁图底部正文残字并保留环面、`R` 标注、电流方向、`mu` 箭头和图号；
- 新增 `03_corpus/manual_review_renders/G1-07-C1/CPHO38-Q04-paper-page-2.png`、`CPHO38-Q04-paper-page-2-figure4a-crop-box.png` 和 `CPHO38-Q04-figure4a-check-contact-v1.png`，记录图4a来源位置和原图/候选图对照；
- 更新 `03_corpus/manual_review_c1_batch_log.csv`、`manual_review_c1_render_index.csv` 和 `manual_review_c1_batch_summary.md`，记录C组队列第133项 `CPHO38-Q04-FIG` 的题图核对入口；
- 更新 `03_corpus/manual_review_checklist.csv`、`manual_review_priority_followup.csv`、`item_materials.csv` 和 `item_index.csv`，将 `CPHO38-Q04-FIG` 推进为“题图核对入口完成，待最终复核”；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，将下一最小任务调整为 `G1-07-C1-FIG-38Q07`；
- 本轮明确记录：第2页中部第5题图5a不得混入第4题图件证据；本轮不改写论文正文，不修改原始PDF，不补造正式论文插图、真实校对人或校对日期。

## 2026-07-17：G1-07-C1-FIG-38Q03 第38届第3题题图核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO38-Q03_figure_check_v1.csv`，登记第38届第3题图3a来源页、原始裁图、整页重裁候选图、来源页裁框和新旧对照证据；
- 新增 `03_corpus/item_assets/CPHO38-Q03-figure3a-page1-recrop-v1.png`，基于第38届试题PDF第1页整页题面证据重裁图3a，去除原始裁图下方正文残字并保留 `v0/omega0`、`1/2/3`、`O` 点、上下平行板、`x/y` 坐标轴和图号；
- 新增 `03_corpus/manual_review_renders/G1-07-C1/CPHO38-Q03-paper-page-1.png`、`CPHO38-Q03-paper-page-1-figure3a-crop-box.png` 和 `CPHO38-Q03-figure3a-check-contact-v1.png`，记录图3a来源位置和原图/候选图对照；
- 更新 `03_corpus/manual_review_c1_batch_log.csv`、`manual_review_c1_render_index.csv` 和 `manual_review_c1_batch_summary.md`，记录C组队列第132项 `CPHO38-Q03-FIG` 的题图核对入口；
- 更新 `03_corpus/manual_review_checklist.csv`、`manual_review_priority_followup.csv`、`item_materials.csv` 和 `item_index.csv`，将 `CPHO38-Q03-FIG` 推进为“题图核对入口完成，待最终复核”；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，将下一最小任务调整为 `G1-07-C1-FIG-38Q04`；
- 本轮明确记录：第1页上方第1题图1a和第2题图2a不得混入第3题图件证据；本轮不改写论文正文，不修改原始PDF，不补造正式论文插图、真实校对人或校对日期。

## 2026-07-17：G1-07-C1-FIG-38Q01 第38届第1题题图核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO38-Q01_figure_check_v1.csv`，登记第38届第1题图1a来源页、原始裁图、内部修剪候选图、来源页裁框、内部修剪框和新旧对照证据；
- 新增 `03_corpus/item_assets/CPHO38-Q01-figure1a-page1-recrop-v1.png`，基于原始裁图内部保守修剪，去除左侧正文残边并保留平凸透镜光路、入射平行光、曲面轮廓、`P/O`、`r0`、`n`、焦点 `F` 和图号；
- 新增 `03_corpus/manual_review_renders/G1-07-C1/CPHO38-Q01-paper-page-1.png`、`CPHO38-Q01-paper-page-1-figure1a-crop-box.png`、`CPHO38-Q01-figure1a-internal-trim-box.png` 和 `CPHO38-Q01-figure1a-check-contact-v1.png`，记录图1a来源位置、内部修剪范围和新旧对照；
- 更新 `03_corpus/manual_review_c1_batch_log.csv`、`manual_review_c1_render_index.csv` 和 `manual_review_c1_batch_summary.md`，记录C组队列第131项 `CPHO38-Q01-FIG` 的题图核对入口；
- 更新 `03_corpus/manual_review_checklist.csv`、`manual_review_priority_followup.csv`、`item_materials.csv` 和 `item_index.csv`，将 `CPHO38-Q01-FIG` 推进为“题图核对入口完成，待最终复核”；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，将下一最小任务调整为 `G1-07-C1-FIG-38Q03`；
- 本轮明确记录：候选图只做内部修剪，不补字、不重绘；第1页中下部第2题图2a和底部第3题图3a不得混入第1题图件证据；本轮不改写论文正文，不修改原始PDF，不补造正式论文插图、真实校对人或校对日期。

## 2026-07-17：G1-07-C1-FIG-37Q07 第37届第7题题图核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO37-Q07_figure_check_v1.csv`，登记第37届第7题图7a来源页、原始裁图、内部修剪候选图、来源页裁框、内部修剪框和新旧对照证据；
- 新增 `03_corpus/item_assets/CPHO37-Q07-figure7a-page4-recrop-v1.png`，基于原始裁图内部保守修剪，去除左侧正文残边并保留双黑洞质量点 `M/m`、质心 `O`、连接线、旋转箭头和图号；
- 新增 `03_corpus/manual_review_renders/G1-07-C1/CPHO37-Q07-paper-page-4.png`、`CPHO37-Q07-paper-page-4-figure7a-crop-box.png`、`CPHO37-Q07-figure7a-internal-trim-box.png` 和 `CPHO37-Q07-figure7a-check-contact-v1.png`，记录图7a来源位置、内部修剪范围和新旧对照；
- 更新 `03_corpus/manual_review_c1_batch_log.csv`、`manual_review_c1_render_index.csv` 和 `manual_review_c1_batch_summary.md`，记录C组队列第130项 `CPHO37-Q07-FIG` 的题图核对入口；
- 更新 `03_corpus/manual_review_checklist.csv`、`manual_review_priority_followup.csv`、`item_materials.csv` 和 `item_index.csv`，将 `CPHO37-Q07-FIG` 推进为“题图核对入口完成，待最终复核”；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，将下一最小任务调整为 `G1-07-C1-FIG-38Q01`；
- 本轮明确记录：候选图只做内部修剪，不补字、不重绘；第4页顶部第6题尾部和下方第8题图8a不得混入第7题图件证据；本轮不改写论文正文，不修改原始PDF，不补造正式论文插图、真实校对人或校对日期。

## 2026-07-17：G1-07-C1-FIG-37Q06 第37届第6题题图核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO37-Q06_figure_check_v1.csv`，登记第37届第6题图6a/图6b来源页、原始裁图、内部修剪候选图、裁框定位、内部修剪框和新旧对照证据；
- 新增 `03_corpus/item_assets/CPHO37-Q06-figure6a-page3-recrop-v1.png` 和 `CPHO37-Q06-figure6b-page3-recrop-v1.png`，基于原始裁图内部保守修剪，去除主要正文残边并保留光纤环、`CCW/CW`、A点、`Omega`、`R`、光纤端口、`n0/n1/n2`、入射角 `i` 和图号；
- 新增 `03_corpus/manual_review_renders/G1-07-C1/CPHO37-Q06-paper-page-3.png`、`CPHO37-Q06-paper-page-3-figure6a6b-crop-box.png`、`CPHO37-Q06-figure6a6b-internal-trim-box.png` 和 `CPHO37-Q06-figure6a6b-check-contact-v1.png`，记录题图来源位置、内部修剪范围和新旧对照；
- 更新 `03_corpus/manual_review_c1_batch_log.csv`、`manual_review_c1_render_index.csv` 和 `manual_review_c1_batch_summary.md`，记录C组队列第129项 `CPHO37-Q06-FIG` 的题图核对入口；
- 更新 `03_corpus/manual_review_checklist.csv`、`manual_review_priority_followup.csv`、`item_materials.csv` 和 `item_index.csv`，将 `CPHO37-Q06-FIG` 推进为“题图核对入口完成，待最终复核”；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，将下一最小任务调整为 `G1-07-C1-FIG-37Q07`；
- 本轮明确记录：候选图只做内部修剪，不补字、不重绘；本轮不改写论文正文，不修改原始PDF，不补造正式论文插图、真实校对人或校对日期。

## 2026-07-17：G1-07-C1-FIG-36Q05 第36届第5题题图核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO36-Q05_figure_check_v1.csv`，登记第36届第5题图a来源页、原始裁图、重裁候选图、裁框定位和新旧对照证据；
- 新增 `03_corpus/item_assets/CPHO36-Q05-figure-a-page5-recrop-v1.png`，基于第36届试题PDF第5页整页渲染图重裁图a，保留微球透镜、激光束、光纤、`n/n1/n2/O` 标注和图注；
- 新增 `03_corpus/manual_review_renders/G1-07-C1/CPHO36-Q05-paper-page-5.png`、`CPHO36-Q05-paper-page-5-figure-a-crop-box.png` 和 `CPHO36-Q05-figure-a-check-contact-v1.png`，记录题图来源位置、原图/候选图对照和第6题正文边界；
- 更新 `03_corpus/manual_review_c1_batch_log.csv`、`manual_review_c1_render_index.csv` 和 `manual_review_c1_batch_summary.md`，记录C组队列第128项 `CPHO36-Q05-FIG` 的题图核对入口；
- 更新 `03_corpus/manual_review_checklist.csv`、`manual_review_priority_followup.csv`、`item_materials.csv` 和 `item_index.csv`，将 `CPHO36-Q05-FIG` 推进为“题图核对入口完成，待最终复核”；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，将下一最小任务调整为 `G1-07-C1-FIG-37Q06`；
- 本轮明确记录：原始裁图未见明显邻近正文残字，候选图未纳入第6题正文；本轮不改写论文正文，不修改原始PDF，不补造正式论文插图、真实校对人或校对日期。

## 2026-07-17：G1-07-C1-FIG-36Q04 第36届第4题题图核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO36-Q04_figure_check_v1.csv`，登记第36届第4题图a/图b来源页、原始裁图、重裁候选图、裁框定位和新旧对照证据；
- 新增 `03_corpus/item_assets/CPHO36-Q04-figure1-page4-recrop-v1.png`，基于第36届试题PDF第4页整页渲染图重裁题图，保留图a微孔竹板照片、图b微孔竹板装置简化图、右侧亥姆霍兹共振器模型、`S/l/V0` 标注和两条图注；
- 新增 `03_corpus/manual_review_renders/G1-07-C1/CPHO36-Q04-paper-page-4.png`、`CPHO36-Q04-paper-page-4-figure1-crop-box.png` 和 `CPHO36-Q04-figure1-check-contact-v1.png`，记录题图来源位置、原图/候选图对照和第5题正文边界；
- 更新 `03_corpus/manual_review_c1_batch_log.csv`、`manual_review_c1_render_index.csv` 和 `manual_review_c1_batch_summary.md`，记录C组队列第127项 `CPHO36-Q04-FIG` 的题图核对入口；
- 更新 `03_corpus/manual_review_checklist.csv`、`manual_review_priority_followup.csv`、`item_materials.csv` 和 `item_index.csv`，将 `CPHO36-Q04-FIG` 推进为“题图核对入口完成，待最终复核”；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，将下一最小任务调整为 `G1-07-C1-FIG-36Q05`；
- 本轮明确记录：候选图未纳入第5题正文，仍需最终版式复核；本轮不改写论文正文，不修改原始PDF，不补造正式论文插图、真实校对人或校对日期。

## 2026-07-17：G1-07-C1-FIG-35Q06 第35届第6题题图核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO35-Q06_figure_check_v1.csv`，登记第35届第6题题图来源页、原始裁图、重裁候选图、裁框定位和新旧对照证据；
- 新增 `03_corpus/item_assets/CPHO35-Q06-figure1-page3-recrop-v1.png`，基于第35届试题PDF第3页整页渲染图重裁同心球壳示意图，去除原始裁图左侧题干残字，并保留完整同心球壳、`R1/R2/r` 标注；
- 新增 `03_corpus/manual_review_renders/G1-07-C1/CPHO35-Q06-paper-page-3.png`、`CPHO35-Q06-paper-page-3-figure1-crop-box.png` 和 `CPHO35-Q06-figure1-check-contact-v1.png`，记录题图来源位置和原图/候选图对照；
- 更新 `03_corpus/manual_review_c1_batch_log.csv`、`manual_review_c1_render_index.csv` 和 `manual_review_c1_batch_summary.md`，记录C组队列第126项 `CPHO35-Q06-FIG` 的题图核对入口；
- 更新 `03_corpus/manual_review_checklist.csv`、`manual_review_priority_followup.csv`、`item_materials.csv` 和 `item_index.csv`，将 `CPHO35-Q06-FIG` 推进为“题图核对入口完成，待最终复核”；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，将下一最小任务调整为 `G1-07-C1-FIG-36Q04`；
- 本轮明确记录：原页未印出单独图号或图注，候选图仍需最终版式复核；本轮不改写论文正文，不修改原始PDF，不补造正式论文插图、真实校对人或校对日期。

## 2026-07-17：G1-07-C1-FIG-41Q06 第41届第6题题图核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO41-Q06_figure_check_v1.csv`，登记第41届第6题图6a页面位置、原始裁图、重裁候选图、裁框定位和新旧对照证据；
- 新增 `03_corpus/item_assets/CPHO41-Q06-figure6a-page4-recrop-v1.png`，基于第41届试题PDF第4页整页渲染图重裁图6a，补足原始裁图缺失或不完整的 `v0` 箭头和 `b` 标注，并保留两条轨迹、中心天体符号、`Delta phi` 和图号；
- 新增 `03_corpus/manual_review_renders/G1-07-C1/CPHO41-Q06-paper-page-4.png`、`CPHO41-Q06-paper-page-4-figure6a-crop-box.png` 和 `CPHO41-Q06-figure6a-check-contact-v1.png`，记录题图来源位置、原图/候选图对照和同页第7题图7a/图7b边界；
- 更新 `03_corpus/manual_review_c1_batch_log.csv`、`manual_review_c1_render_index.csv` 和 `manual_review_c1_batch_summary.md`，记录C组队列第125项 `CPHO41-Q06-FIG` 的题图核对入口；
- 更新 `03_corpus/manual_review_checklist.csv`、`manual_review_priority_followup.csv`、`item_materials.csv` 和 `item_index.csv`，将 `CPHO41-Q06-FIG` 推进为“题图核对入口完成，待最终复核”；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，将下一最小任务调整为 `G1-07-C1-FIG-35Q06`；
- 本轮明确记录：第4页下半部进入第7题，图7a/图7b不得纳入第6题图件证据；本轮不改写论文正文，不修改原始PDF，不补造正式论文插图、真实校对人或校对日期。

## 2026-07-17：G1-07-C1-FIG-41Q05 第41届第5题题图核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO41-Q05_figure_check_v1.csv`，登记第41届第5题图5a页面位置、原始裁图、重裁候选图、裁框定位和新旧对照证据；
- 新增 `03_corpus/item_assets/CPHO41-Q05-figure5a-page3-recrop-v1.png`，基于第41届试题PDF第3页整页渲染图重裁图5a，去除原始裁图左侧题干残字，并保留四角导线电流方向、`I`、`x/y` 轴、`O`、`P(x,y)`、`a/b` 和图号；
- 新增 `03_corpus/manual_review_renders/G1-07-C1/CPHO41-Q05-paper-page-3.png`、`CPHO41-Q05-paper-page-3-figure5a-crop-box.png` 和 `CPHO41-Q05-figure5a-check-contact-v1.png`，记录题图来源位置、原图/候选图对照和同页第4题、第6题边界；
- 更新 `03_corpus/manual_review_c1_batch_log.csv`、`manual_review_c1_render_index.csv` 和 `manual_review_c1_batch_summary.md`，记录C组队列第124项 `CPHO41-Q05-FIG` 的题图核对入口；
- 更新 `03_corpus/manual_review_checklist.csv`、`manual_review_priority_followup.csv`、`item_materials.csv` 和 `item_index.csv`，将 `CPHO41-Q05-FIG` 推进为“题图核对入口完成，待最终复核”；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，将下一最小任务调整为 `G1-07-C1-FIG-41Q06`；
- 本轮明确记录：候选图左侧 `x` 轴延伸处贴近裁边，正式论文或附录使用前仍需最终版式复核；本轮不改写论文正文，不修改原始PDF，不补造正式论文插图、真实校对人或校对日期。

## 2026-07-17：G1-07-C1-FIG-41Q01 第41届第1题题图核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO41-Q01_figure_check_v1.csv`，登记第41届第1题图1a页面位置、原始裁图、重裁候选图、裁框定位和新旧对照证据；
- 新增 `03_corpus/item_assets/CPHO41-Q01-figure1a-page1-recrop-v1.png`，基于第41届试题PDF第1页整页渲染图重裁图1a，补足原始裁图缺失的摆长 `l` 和偏角 `theta` 标注，并保留摆锤 `m`、质量块 `M`、外力 `F`、弹簧、地面和图号；
- 新增 `03_corpus/manual_review_renders/G1-07-C1/CPHO41-Q01-paper-page-1.png`、`CPHO41-Q01-paper-page-1-figure1a-crop-box.png` 和 `CPHO41-Q01-figure1a-check-contact-v1.png`，记录题图来源位置、原图/候选图对照和同页第2题图2a边界；
- 更新 `03_corpus/manual_review_c1_batch_log.csv`、`manual_review_c1_render_index.csv` 和 `manual_review_c1_batch_summary.md`，记录C组队列第123项 `CPHO41-Q01-FIG` 的题图核对入口；
- 更新 `03_corpus/manual_review_checklist.csv`、`manual_review_priority_followup.csv`、`item_materials.csv` 和 `item_index.csv`，将 `CPHO41-Q01-FIG` 推进为“题图核对入口完成，待最终复核”；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，将下一最小任务调整为 `G1-07-C1-FIG-41Q05`；
- 本轮明确记录：原始裁图上方摆线、`l` 和 `theta` 标注被截断，重裁候选图补足关键标注且未混入第2题图2a；本轮不改写论文正文，不修改原始PDF，不补造正式论文插图、真实校对人或校对日期。

## 2026-07-17：G1-07-C1-FIG-40Q07 第40届第7题题图核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO40-Q07_figure_check_v1.csv`，登记第40届第7题题面图7a页面位置、原始裁图、重裁候选图、裁框定位和新旧对照证据；
- 新增 `03_corpus/item_assets/CPHO40-Q07-figure7a-page4-recrop-v1.png`，基于第40届试题PDF第4页整页渲染图重裁图7a，补足原始裁图缺失的上半部大气分层环形结构，并保留对流层、同温层、逆温层、地球和图号；
- 新增 `03_corpus/manual_review_renders/G1-07-C1/CPHO40-Q07-paper-page-4.png`、`CPHO40-Q07-paper-page-4-figure7a-crop-box.png` 和 `CPHO40-Q07-figure7a-check-contact-v1.png`，记录题图来源位置、原图/候选图对照和同页第6题图6a边界；
- 更新 `03_corpus/manual_review_c1_batch_log.csv`、`manual_review_c1_render_index.csv` 和 `manual_review_c1_batch_summary.md`，记录C组队列第122项 `CPHO40-Q07-FIG` 的题图核对入口；
- 更新 `03_corpus/manual_review_checklist.csv`、`manual_review_priority_followup.csv`、`item_materials.csv` 和 `item_index.csv`，将 `CPHO40-Q07-FIG` 推进为“题图核对入口完成，待最终复核”；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，将下一最小任务调整为 `G1-07-C1-FIG-41Q01`；
- 本轮明确记录：图7a与邻近正文贴近，候选图仍可见残字，正式论文或附录使用前建议最终复核后重绘或版式清理；答案题解图7a/7b/7c/7d未在本项中销项；本轮不改写论文正文，不修改原始PDF，不补造正式论文插图、真实校对人或校对日期。

## 2026-07-17：G1-07-C1-FIG-40Q06 第40届第6题题图核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO40-Q06_figure_check_v1.csv`，登记第40届第6题图6a页面位置、原始裁图、保守重裁候选图、裁框定位和新旧对照证据；
- 新增 `03_corpus/item_assets/CPHO40-Q06-figure6a-page4-recrop-v1.png`，基于第40届试题PDF第4页整页渲染图保守重裁图6a，保留导体球、`z` 轴、`a`、`h`、线圈、`O`、`b`、`I=I_0 cos(omega t)` 和图号；
- 新增 `03_corpus/manual_review_renders/G1-07-C1/CPHO40-Q06-paper-page-4.png`、`CPHO40-Q06-paper-page-4-figure6a-crop-box.png` 和 `CPHO40-Q06-figure6a-check-contact-v1.png`，记录题图来源位置、原图/候选图对照和同页第7题图7a边界；
- 更新 `03_corpus/manual_review_c1_batch_log.csv`、`manual_review_c1_render_index.csv` 和 `manual_review_c1_batch_summary.md`，记录C组队列第121项 `CPHO40-Q06-FIG` 的题图核对入口；
- 更新 `03_corpus/manual_review_checklist.csv`、`manual_review_priority_followup.csv`、`item_materials.csv` 和 `item_index.csv`，将 `CPHO40-Q06-FIG` 推进为“题图核对入口完成，待最终复核”；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，将下一最小任务调整为 `G1-07-C1-FIG-40Q07`；
- 本轮明确记录：图6a与左侧题干正文贴近，候选图仍可见残字，正式论文或附录使用前建议最终复核后重绘或版式清理；本轮不改写论文正文，不修改原始PDF，不补造正式论文插图、真实校对人或校对日期。

## 2026-07-17：G1-07-C1-FIG-40Q01 第40届第1题题图核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO40-Q01_figure_check_v1.csv`，登记第40届第1题图1a页面位置、原始裁图、重裁候选图、裁框定位和新旧对照证据；
- 新增 `03_corpus/item_assets/CPHO40-Q01-figure1a-page1-recrop-v1.png`，基于第40届试题PDF第1页整页渲染图重裁图1a，保留透镜组和薄透镜两套物像关系示意、`H/H'`、物距/像距、透镜组虚线框、薄透镜标注和图注，并裁去下方第(1)问题干正文；
- 新增 `03_corpus/manual_review_renders/G1-07-C1/CPHO40-Q01-paper-page-1.png`、`CPHO40-Q01-paper-page-1-figure1a-crop-box.png` 和 `CPHO40-Q01-figure1a-check-contact-v1.png`，记录题图来源位置、原图/候选图对照和同页第2题图2a边界；
- 更新 `03_corpus/manual_review_c1_batch_log.csv`、`manual_review_c1_render_index.csv` 和 `manual_review_c1_batch_summary.md`，记录C组队列第120项 `CPHO40-Q01-FIG` 的题图核对入口；
- 更新 `03_corpus/manual_review_checklist.csv`、`manual_review_priority_followup.csv`、`item_materials.csv` 和 `item_index.csv`，将 `CPHO40-Q01-FIG` 推进为“题图核对入口完成，待最终复核”；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，将下一最小任务调整为 `G1-07-C1-FIG-40Q06`；
- 本轮不改写论文正文，不修改原始PDF，不补造图注、正式论文插图、真实校对人或校对日期。

## 2026-07-17：G1-07-C1-FIG-39Q03 第39届第3题题图核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO39-Q03_figure_check_v1.csv`，登记第39届第3题图3a页面位置、原始裁图、重裁候选图、裁框定位和新旧对照证据；
- 新增 `03_corpus/item_assets/CPHO39-Q03-figure3a-page2-recrop-v1.png`，基于第39届试题PDF第2页整页渲染图重裁图3a，去除左侧邻近题干残字，并保留实心球、`V` 箭头、`x/y` 坐标、斜面、水平面、`theta` 角和图号；
- 新增 `03_corpus/manual_review_renders/G1-07-C1/CPHO39-Q03-paper-page-2.png`、`CPHO39-Q03-paper-page-2-figure3a-crop-box.png` 和 `CPHO39-Q03-figure3a-check-contact-v1.png`，记录题图来源位置、原图/候选图对照和同页第4题图4a边界；
- 更新 `03_corpus/manual_review_c1_batch_log.csv`、`manual_review_c1_render_index.csv` 和 `manual_review_c1_batch_summary.md`，记录C组队列第119项 `CPHO39-Q03-FIG` 的题图核对入口；
- 更新 `03_corpus/manual_review_checklist.csv`、`manual_review_priority_followup.csv`、`item_materials.csv` 和 `item_index.csv`，将 `CPHO39-Q03-FIG` 推进为“题图核对入口完成，待最终复核”；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，将下一最小任务调整为 `G1-07-C1-FIG-40Q01`；
- 本轮不改写论文正文，不修改原始PDF，不补造图注、正式论文插图、真实校对人或校对日期。

## 2026-07-17：G1-07-C1-FIG-38Q06 第38届第6题题图核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO38-Q06_figure_check_v1.csv`，登记第38届第6题图6a页面位置、原始裁图、重裁候选图、裁框定位和新旧对照证据；
- 新增 `03_corpus/item_assets/CPHO38-Q06-figure6a-page3-recrop-v1.png`，基于第38届试题PDF第3页整页渲染图重裁图6a，保留同轴圆筒主体、`r1/r2`、`m`、`q`、`-q` 和图号；
- 新增 `03_corpus/manual_review_renders/G1-07-C1/CPHO38-Q06-paper-page-3.png`、`CPHO38-Q06-paper-page-3-figure6a-crop-box.png` 和 `CPHO38-Q06-figure6a-check-contact-v1.png`，记录题图来源位置、原图/候选图对照和同页第7题、第8题边界；
- 更新 `03_corpus/manual_review_c1_batch_log.csv`、`manual_review_c1_render_index.csv` 和 `manual_review_c1_batch_summary.md`，记录C组队列第118项 `CPHO38-Q06-FIG` 的题图核对入口；
- 更新 `03_corpus/manual_review_checklist.csv`、`manual_review_priority_followup.csv`、`item_materials.csv` 和 `item_index.csv`，将 `CPHO38-Q06-FIG` 推进为“题图核对入口完成，待最终复核”，并同步答案页范围为 `14-16`；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，将下一最小任务调整为 `G1-07-C1-FIG-39Q03`；
- 本轮不改写论文正文，不修改原始PDF，不补造图注、正式论文插图、真实校对人或校对日期。

## 2026-07-17：G1-07-C1-FIG-38Q05 第38届第5题题图核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO38-Q05_figure_check_v1.csv`，登记第38届第5题图5a页面位置、原始裁图、重裁候选图、裁框定位和新旧对照证据；
- 新增 `03_corpus/item_assets/CPHO38-Q05-figure5a-page2-recrop-v1.png`，基于第38届试题PDF第2页整页渲染图重裁图5a，去除上下邻近题干残字，并保留原子炉、准直管、减速管、冷原子实验腔、激光方向、线圈说明和图号；
- 新增 `03_corpus/manual_review_renders/G1-07-C1/CPHO38-Q05-paper-page-2.png`、`CPHO38-Q05-paper-page-2-figure5a-crop-box.png` 和 `CPHO38-Q05-figure5a-check-contact-v1.png`，记录题图来源位置、原图/候选图对照和版式边界；
- 更新 `03_corpus/manual_review_c1_batch_log.csv`、`manual_review_c1_render_index.csv` 和 `manual_review_c1_batch_summary.md`，记录C组队列第117项 `CPHO38-Q05-FIG` 的题图核对入口；
- 更新 `03_corpus/manual_review_checklist.csv`、`manual_review_priority_followup.csv`、`item_materials.csv` 和 `item_index.csv`，将 `CPHO38-Q05-FIG` 推进为“题图核对入口完成，待最终复核”；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，将下一最小任务调整为 `G1-07-C1-FIG-38Q06`；
- 本轮不改写论文正文，不修改原始PDF，不补造图注、正式论文插图、真实校对人或校对日期。

## 2026-07-17：G1-07-C1-FIG-37Q08 第37届第8题题图核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO37-Q08_figure_check_v1.csv`，登记第37届第8题图8a/图8b页面位置、原始裁图、保守修剪候选图、裁框定位、原图内部修剪框和新旧对照证据；
- 新增 `03_corpus/item_assets/CPHO37-Q08-figure8a-page4-recrop-v1.png` 和 `CPHO37-Q08-figure8b-page5-recrop-v1.png`，基于原始裁图内部保守修剪，去除主要邻近题干残字，并保留电光调制器光路、等效电路、关键标注和图号；
- 新增 `03_corpus/manual_review_renders/G1-07-C1/CPHO37-Q08-paper-page-4.png`、`CPHO37-Q08-paper-page-5.png`、两页裁框定位图、原图内部修剪框和 `CPHO37-Q08-figure8a8b-check-contact-v1.png`；
- 更新 `03_corpus/manual_review_c1_batch_log.csv`、`manual_review_c1_render_index.csv` 和 `manual_review_c1_batch_summary.md`，记录C组队列第116项 `CPHO37-Q08-FIG` 的题图核对入口；
- 更新 `03_corpus/manual_review_checklist.csv`、`manual_review_priority_followup.csv`、`item_materials.csv` 和 `item_index.csv`，将 `CPHO37-Q08-FIG` 推进为“题图核对入口完成，待最终复核”；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，将下一最小任务调整为 `G1-07-C1-FIG-38Q05`；
- 本轮不改写论文正文，不修改原始PDF，不补造图注、正式论文插图、真实校对人或校对日期。

## 2026-07-17：G1-07-C1-FIG-37Q03 第37届第3题题图核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO37-Q03_figure_check_v1.csv`，登记第37届第3题图3a页面位置、原始裁图、重裁候选图、裁框定位和新旧对照证据；
- 新增 `03_corpus/item_assets/CPHO37-Q03-figure1-page2-recrop-v1.png`，对原始裁图进行保守内部修剪，去除左侧正文残字和底部题干残行，保留电路主体、元件标注、箭头、接地符号和图号；
- 新增 `03_corpus/manual_review_renders/G1-07-C1/CPHO37-Q03-paper-page-2.png`、`CPHO37-Q03-paper-page-2-figure1-crop-box.png` 和 `CPHO37-Q03-figure1-check-contact-v1.png`，记录整页来源位置、图3a嵌入正文的边界、原图/候选图对照和内部修剪框；
- 更新 `03_corpus/manual_review_c1_batch_log.csv`、`manual_review_c1_render_index.csv` 和 `manual_review_c1_batch_summary.md`，记录C组队列第115项 `CPHO37-Q03-FIG` 的题图核对入口；
- 更新 `03_corpus/manual_review_checklist.csv`、`manual_review_priority_followup.csv`、`item_materials.csv` 和 `item_index.csv`，将 `CPHO37-Q03-FIG` 推进为“题图核对入口完成，待最终复核”；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，将下一最小任务调整为 `G1-07-C1-FIG-37Q08`；
- 本轮不改写论文正文，不修改原始PDF，不补造图注、正式论文插图、真实校对人或校对日期。

## 2026-07-17：G1-07-C1-FIG-35Q04 第35届第4题题图核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO35-Q04_figure_check_v1.csv`，登记第35届第4题题图页面位置、原始裁图、重裁候选图、裁框定位和新旧对照证据；
- 新增 `03_corpus/item_assets/CPHO35-Q04-figure1-page2-recrop-v1.png`，基于第35届试题PDF第2页整页渲染图重裁题图，去除左侧正文残边；
- 新增 `03_corpus/manual_review_renders/G1-07-C1/CPHO35-Q04-paper-page-2-figure1-crop-box.png` 和 `CPHO35-Q04-figure1-check-contact-v1.png`，记录题图来源位置、原图/候选图对照以及上方第3题尾部、下方第5题边界；
- 更新 `03_corpus/manual_review_c1_batch_log.csv`、`manual_review_c1_render_index.csv` 和 `manual_review_c1_batch_summary.md`，记录C组队列第114项 `CPHO35-Q04-FIG` 的题图核对入口；
- 更新 `03_corpus/manual_review_checklist.csv`、`manual_review_priority_followup.csv`、`item_materials.csv`、`item_index.csv` 和 `03_corpus/item_texts/CPHO35-Q04.md`，将 `CPHO35-Q04-FIG` 推进为“题图核对入口完成，待最终复核”；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，将下一最小任务调整为 `G1-07-C1-FIG-37Q03`；
- 本轮不改写论文正文，不修改原始PDF，不补造图注、正式论文插图、真实校对人或校对日期。

## 2026-07-17：G1-07-C1-FIG-35Q03 第35届第3题题图核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO35-Q03_figure_check_v1.csv`，登记第35届第3题题图页面位置、原始裁图、重裁候选图、裁框定位和新旧对照证据；
- 新增 `03_corpus/item_assets/CPHO35-Q03-figure1-page1-recrop-v1.png`，基于第35届试题PDF第1页整页渲染图重裁题图，去除原始裁图左侧邻近题干残字；
- 新增 `03_corpus/manual_review_renders/G1-07-C1/CPHO35-Q03-paper-page-1-figure1-crop-box.png` 和 `CPHO35-Q03-figure1-check-contact-v1.png`，记录题图来源位置、原图/候选图对照以及页底边界；
- 更新 `03_corpus/manual_review_c1_batch_log.csv`、`manual_review_c1_render_index.csv` 和 `manual_review_c1_batch_summary.md`，记录C组队列第113项 `CPHO35-Q03-FIG` 的题图核对入口；
- 更新 `03_corpus/manual_review_checklist.csv`、`manual_review_priority_followup.csv`、`item_materials.csv`、`item_index.csv` 和 `03_corpus/item_texts/CPHO35-Q03.md`，将 `CPHO35-Q03-FIG` 推进为“题图核对入口完成，待最终复核”；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，将下一最小任务调整为 `G1-07-C1-FIG-35Q04`；
- 本轮不改写论文正文，不修改原始PDF，不补造图注、正式论文插图、真实校对人或校对日期。

## 2026-07-16：G1-07-C1-FIG-35Q02 第35届第2题题图核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO35-Q02_figure_check_v1.csv`，登记第35届第2题题图页面位置、原始裁图、重裁候选图、裁框定位和新旧对照证据；
- 新增 `03_corpus/item_assets/CPHO35-Q02-figure1-page1-recrop-v1.png`，基于第35届试题PDF第1页整页渲染图重裁题图，补足原始裁图缺失的 `-A0`、`O`、`x` 坐标标注；
- 新增 `03_corpus/manual_review_renders/G1-07-C1/CPHO35-Q02-paper-page-1-figure1-crop-box.png` 和 `CPHO35-Q02-figure1-check-contact-v1.png`，记录题图来源位置、原图/候选图对照以及正文边界；
- 更新 `03_corpus/manual_review_c1_batch_log.csv`、`manual_review_c1_render_index.csv` 和 `manual_review_c1_batch_summary.md`，记录C组队列第112项 `CPHO35-Q02-FIG` 的题图核对入口；
- 更新 `03_corpus/manual_review_checklist.csv`、`manual_review_priority_followup.csv`、`item_materials.csv`、`item_index.csv` 和 `03_corpus/item_texts/CPHO35-Q02.md`，将 `CPHO35-Q02-FIG` 推进为“题图核对入口完成，待最终复核”；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，将下一最小任务调整为 `G1-07-C1-FIG-35Q03`；
- 本轮不改写论文正文，不修改原始PDF，不补造图注、正式论文插图、真实校对人或校对日期。

## 2026-07-16：G1-07-C1-FIG-42Q06 第42届第6题题图核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO42-Q06_figure_check_v1.csv`，登记图6a页面位置、原始裁图、顶部修剪候选图、裁框定位和新旧对照证据；
- 新增 `03_corpus/item_assets/CPHO42-Q06-figure6a-page4-recrop-v1.png`，对原始裁图进行顶部修剪，去除上一题参数残字，保留转速仪图6a主体、关键物理标注和图号；
- 新增 `03_corpus/manual_review_renders/G1-07-C1/CPHO42-Q06-paper-page-4-figure6a-crop-box.png` 和 `CPHO42-Q06-figure6a-check-contact-v1.png`，记录图6a来源位置、原图/候选图对照以及顶部残字边界；
- 更新 `03_corpus/manual_review_c1_batch_log.csv`、`manual_review_c1_render_index.csv` 和 `manual_review_c1_batch_summary.md`，记录C组队列第111项 `CPHO42-Q06-FIG` 的题图核对入口；
- 更新 `03_corpus/manual_review_checklist.csv`、`manual_review_priority_followup.csv`、`item_materials.csv`、`item_index.csv` 和 `03_corpus/item_texts/CPHO42-Q06.md`，将 `CPHO42-Q06-FIG` 推进为“题图核对入口完成，待最终复核”；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，将下一最小任务调整为 `G1-07-C1-FIG-35Q02`；
- 本轮不改写论文正文，不修改原始PDF，不补造图注、正式论文插图、真实校对人或校对日期。

## 2026-07-16：G1-07-C1-FIG-40Q08 第40届第8题题图核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO40-Q08_figure_check_v1.csv`，登记图8a/图8b页面位置、原始裁图、重裁候选图、裁框定位和新旧对照证据；
- 新增 `03_corpus/item_assets/CPHO40-Q08-figure8a-page5-recrop-v1.png` 和 `CPHO40-Q08-figure8b-page5-recrop-v1.png`，基于第40届试题PDF第5页整页渲染图重裁图8a/图8b，去除原裁图底部第(1)问题干残字；
- 新增 `03_corpus/manual_review_renders/G1-07-C1/CPHO40-Q08-paper-page-5-figure8a8b-crop-box.png` 和 `CPHO40-Q08-figure8a8b-check-contact-v1.png`，记录图8a/图8b来源位置、原图/候选图对照以及下方题干边界；
- 更新 `03_corpus/manual_review_c1_batch_log.csv`、`manual_review_c1_render_index.csv` 和 `manual_review_c1_batch_summary.md`，记录C组队列第110项 `CPHO40-Q08-FIG` 的题图核对入口；
- 更新 `03_corpus/manual_review_checklist.csv`、`manual_review_priority_followup.csv`、`item_materials.csv`、`item_index.csv` 和 `03_corpus/item_texts/CPHO40-Q08.md`，将 `CPHO40-Q08-FIG` 推进为“题图核对入口完成，待最终复核”；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，将下一最小任务调整为 `G1-07-C1-FIG-42Q06`；
- 本轮不改写论文正文，不修改原始PDF，不补造图注、正式论文插图、真实校对人或校对日期。

## 2026-07-16：G1-07-C1-FIG-40Q05 第40届第5题题图核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO40-Q05_figure_check_v1.csv`，登记图5a页面位置、原始裁图、重裁候选图、裁框定位和新旧对照证据；
- 新增 `03_corpus/item_assets/CPHO40-Q05-figure5a-page3-recrop-v1.png`，基于第40届试题PDF第3页整页渲染图重裁图5a，去除原裁图左侧题干残字和下方小问文字；
- 新增 `03_corpus/manual_review_renders/G1-07-C1/CPHO40-Q05-paper-page-3-figure5a-crop-box.png` 和 `CPHO40-Q05-figure5a-check-contact-v1.png`，记录图5a来源位置、原图/候选图对照以及左侧、下方题干边界；
- 更新 `03_corpus/manual_review_c1_batch_log.csv`、`manual_review_c1_render_index.csv` 和 `manual_review_c1_batch_summary.md`，记录C组队列第109项 `CPHO40-Q05-FIG` 的题图核对入口；
- 更新 `03_corpus/manual_review_checklist.csv`、`manual_review_priority_followup.csv`、`item_materials.csv`、`item_index.csv` 和 `03_corpus/item_texts/CPHO40-Q05.md`，将 `CPHO40-Q05-FIG` 推进为“题图核对入口完成，待最终复核”；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，将下一最小任务调整为 `G1-07-C1-FIG-40Q08`；
- 本轮不改写论文正文，不修改原始PDF，不补造图注、正式论文插图、真实校对人或校对日期。

## 2026-07-16：G1-07-C1-FIG-40Q02 第40届第2题题图核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO40-Q02_figure_check_v1.csv`，登记图2a页面位置、原始裁图、重裁候选图、裁框定位和新旧对照证据；
- 新增 `03_corpus/item_assets/CPHO40-Q02-figure2a-page1-recrop-v1.png`，基于第40届试题PDF第1页整页渲染图重裁图2a，去除原裁图左侧、上方和下方邻近题干文字；
- 新增 `03_corpus/manual_review_renders/G1-07-C1/CPHO40-Q02-paper-page-1-figure2a-crop-box.png` 和 `CPHO40-Q02-figure2a-check-contact-v1.png`，记录图2a来源位置、原图/候选图对照以及左侧、下方题干边界；
- 更新 `03_corpus/manual_review_c1_batch_log.csv`、`manual_review_c1_render_index.csv` 和 `manual_review_c1_batch_summary.md`，记录C组队列第108项 `CPHO40-Q02-FIG` 的题图核对入口；
- 更新 `03_corpus/manual_review_checklist.csv`、`manual_review_priority_followup.csv`、`item_materials.csv`、`item_index.csv` 和 `03_corpus/item_texts/CPHO40-Q02.md`，将 `CPHO40-Q02-FIG` 推进为“题图核对入口完成，待最终复核”；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，将下一最小任务调整为 `G1-07-C1-FIG-40Q05`；
- 本轮不改写论文正文，不修改原始PDF，不补造图注、正式论文插图、真实校对人或校对日期。

## 2026-07-16：G1-07-C1-FIG-39Q06 第39届第6题题图核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO39-Q06_figure_check_v1.csv`，登记图6a页面位置、原始裁图、重裁候选图、裁框定位和新旧对照证据；
- 新增 `03_corpus/item_assets/CPHO39-Q06-figure6a-page3-recrop-v1.png`，基于第39届试题PDF第3页整页渲染图重裁图6a，去除原裁图上方第5题尾部文字和下方第6题题干文字；
- 新增 `03_corpus/manual_review_renders/G1-07-C1/CPHO39-Q06-paper-page-3-figure6a-crop-box.png` 和 `CPHO39-Q06-figure6a-check-contact-v1.png`，记录图6a来源位置、原图/候选图对照以及上方、下方题干边界；
- 更新 `03_corpus/manual_review_c1_batch_log.csv`、`manual_review_c1_render_index.csv` 和 `manual_review_c1_batch_summary.md`，记录C组队列第107项 `CPHO39-Q06-FIG` 的题图核对入口；
- 更新 `03_corpus/manual_review_checklist.csv`、`manual_review_priority_followup.csv`、`item_materials.csv` 和 `item_index.csv`，将 `CPHO39-Q06-FIG` 推进为“题图核对入口完成，待最终复核”；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，将下一最小任务调整为 `G1-07-C1-FIG-40Q02`；
- 本轮不改写论文正文，不修改原始PDF，不补造图注、正式论文插图、真实校对人或校对日期。

## 2026-07-16：G1-07-C1-FIG-39Q04 第39届第4题题图核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO39-Q04_figure_check_v1.csv`，登记图4a页面位置、原始裁图、重裁候选图、裁框定位和新旧对照证据；
- 新增 `03_corpus/item_assets/CPHO39-Q04-figure4a-page2-recrop-v1.png`，基于第39届试题PDF第2页整页渲染图重裁图4a，去除原裁图左侧和底部邻近题干文字；
- 新增 `03_corpus/manual_review_renders/G1-07-C1/CPHO39-Q04-paper-page-2-figure4a-crop-box.png` 和 `CPHO39-Q04-figure4a-check-contact-v1.png`，记录图4a来源位置、原图/候选图对照以及左侧、下方题干边界；
- 更新 `03_corpus/manual_review_c1_batch_log.csv`、`manual_review_c1_render_index.csv` 和 `manual_review_c1_batch_summary.md`，记录C组队列第106项 `CPHO39-Q04-FIG` 的题图核对入口；
- 更新 `03_corpus/manual_review_checklist.csv`、`manual_review_priority_followup.csv`、`item_materials.csv` 和 `item_index.csv`，将 `CPHO39-Q04-FIG` 推进为“题图核对入口完成，待最终复核”；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，将下一最小任务调整为 `G1-07-C1-FIG-39Q06`；
- 本轮不改写论文正文，不修改原始PDF，不补造图注、正式论文插图、真实校对人或校对日期。

## 2026-07-16：G1-07-C1-FIG-36Q07 第36届第7题题图核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO36-Q07_figure_check_v1.csv`，登记图a页面位置、原始裁图、重裁候选图、裁框定位和新旧对照证据；
- 新增 `03_corpus/item_assets/CPHO36-Q07-figure-a-page6-recrop-v1.png`，基于第36届试题PDF第6页整页渲染图重裁图a，去除原裁图上下邻近题干文字；
- 新增 `03_corpus/manual_review_renders/G1-07-C1/CPHO36-Q07-paper-page-6-figure-a-crop-box.png` 和 `CPHO36-Q07-figure-a-check-contact-v1.png`，记录图a来源位置、原图/候选图对照和上下题干边界；
- 更新 `03_corpus/manual_review_c1_batch_log.csv`、`manual_review_c1_render_index.csv` 和 `manual_review_c1_batch_summary.md`，记录C组队列第105项 `CPHO36-Q07-FIG` 的题图核对入口；
- 更新 `03_corpus/manual_review_checklist.csv`、`manual_review_priority_followup.csv`、`item_materials.csv` 和 `item_index.csv`，将 `CPHO36-Q07-FIG` 推进为“题图核对入口完成，待最终复核”；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，将下一最小任务调整为 `G1-07-C1-FIG-39Q04`；
- 本轮不改写论文正文，不修改原始PDF，不补造图注、正式论文插图、真实校对人或校对日期。

## 2026-07-16：G1-07-C1-FIG-36Q03 第36届第3题题图核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO36-Q03_figure_check_v1.csv`，登记图a页面位置、原始裁图、重裁候选图、裁框定位和新旧对照证据；
- 新增 `03_corpus/item_assets/CPHO36-Q03-figure-a-page3-recrop-v1.png`，基于第36届试题PDF第3页整页渲染图重裁图a，去除原裁图底部第(1)问文字；
- 新增 `03_corpus/manual_review_renders/G1-07-C1/CPHO36-Q03-paper-page-3-figure-a-crop-box.png` 和 `CPHO36-Q03-figure-a-check-contact-v1.png`，记录图a来源位置、原图/候选图对照和第4题下方边界；
- 更新 `03_corpus/manual_review_c1_batch_log.csv`、`manual_review_c1_render_index.csv` 和 `manual_review_c1_batch_summary.md`，记录C组队列第104项 `CPHO36-Q03-FIG` 的题图核对入口；
- 更新 `03_corpus/manual_review_checklist.csv`、`manual_review_priority_followup.csv`、`item_materials.csv` 和 `item_index.csv`，将 `CPHO36-Q03-FIG` 推进为“题图核对入口完成，待最终复核”；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，将下一最小任务调整为 `G1-07-C1-FIG-36Q07`；
- 本轮不改写论文正文，不修改原始PDF，不补造图注、正式论文插图、真实校对人或校对日期。

## 2026-07-16：G1-07-C1-FIG-42Q05 第42届第5题题图核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO42-Q05_figure_check_v1.csv`，登记图5a/图5b页面位置、原始裁图、图5b重裁候选图、裁框定位和新旧对照证据；
- 新增 `03_corpus/item_assets/CPHO42-Q05-figure5b-page4-recrop-v1.png`，基于第42届试题PDF第4页整页渲染图重裁图5b，去除原裁图左侧正文残字和底部正文；
- 新增 `03_corpus/manual_review_renders/G1-07-C1/CPHO42-Q05-paper-pages-3-4-figure5a5b-crop-box.png` 和 `CPHO42-Q05-figure5a5b-check-contact-v1.png`，记录第3页图5a、第4页图5b和第6题图6a边界；
- 更新 `03_corpus/manual_review_c1_batch_log.csv`、`manual_review_c1_render_index.csv` 和 `manual_review_c1_batch_summary.md`，记录C组队列第103项 `CPHO42-Q05-FIG` 的题图核对入口；
- 更新 `03_corpus/manual_review_checklist.csv`、`manual_review_priority_followup.csv`、`item_materials.csv` 和 `item_index.csv`，将 `CPHO42-Q05-FIG` 推进为“题图核对入口完成，待最终复核”；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，将下一最小任务调整为 `G1-07-C1-FIG-36Q03`；
- 本轮不改写论文正文，不修改原始PDF，不补造图注、正式论文插图、真实校对人或校对日期。

## 2026-07-16：G1-07-C1-FIG-42Q02 第42届第2题题图核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO42-Q02_figure_check_v1.csv`，登记图2a/图2b页面位置、原始裁图、修剪候选图、裁框定位和新旧对照证据；
- 新增 `03_corpus/item_assets/CPHO42-Q02-figure2a-page1-recrop-v1.png` 和 `CPHO42-Q02-figure2b-page1-recrop-v1.png`，分别修剪图2a底部图2b横线和图2b底部页码残字；
- 新增 `03_corpus/manual_review_renders/G1-07-C1/CPHO42-Q02-paper-page-1-figure2a2b-crop-box.png` 和 `CPHO42-Q02-figure2a2b-check-contact-v1.png`，记录整页来源位置和原图/候选图对照；
- 更新 `03_corpus/manual_review_c1_batch_log.csv`、`manual_review_c1_render_index.csv` 和 `manual_review_c1_batch_summary.md`，记录C组队列第102项 `CPHO42-Q02-FIG` 的题图核对入口；
- 更新 `03_corpus/manual_review_checklist.csv`、`manual_review_priority_followup.csv`、`item_materials.csv` 和 `item_index.csv`，将 `CPHO42-Q02-FIG` 推进为“题图核对入口完成，待最终复核”；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，将下一最小任务调整为 `G1-07-C1-FIG-42Q05`；
- 本轮不改写论文正文，不修改原始PDF，不重绘题图，不补造图注、正式论文插图、真实校对人或校对日期；图2b顶部 `VA` 标注仍需最终复核。

## 2026-07-16：G1-07-C1-FIG-40Q03 第40届第3题题图核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO40-Q03_figure_check_v1.csv`，登记图3a页面位置、原始裁图、重裁候选图、裁框定位和新旧对照证据；
- 新增 `03_corpus/item_assets/CPHO40-Q03-figure3a-page2-recrop-v1.png`，从第40届试题PDF第2页整页渲染图重裁图3a，保留球、楔块、水平地面线、角度 `theta` 和“图3a”，去除原裁图左侧邻近题干残字；
- 新增 `03_corpus/manual_review_renders/G1-07-C1/CPHO40-Q03-paper-page-2-figure3a-crop-box.png` 和 `CPHO40-Q03-figure3a-check-contact-v1.png`，记录裁框来源和原图/重裁图/整页位置三联对照；
- 新增 `03_corpus/manual_review_c1_batch_log.csv`、`manual_review_c1_render_index.csv` 和 `manual_review_c1_batch_summary.md`，记录C组队列第101项 `CPHO40-Q03-FIG` 的题图核对入口；
- 更新 `03_corpus/manual_review_checklist.csv`、`manual_review_priority_followup.csv`、`item_materials.csv` 和 `item_index.csv`，将 `CPHO40-Q03-FIG` 推进为“题图核对入口完成，待最终复核”；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，将下一最小任务调整为 `G1-07-C1-FIG-42Q02`；
- 本轮不改写论文正文，不修改原始PDF，不重绘题图，不补造图注、正式论文插图、真实校对人或校对日期。

## 2026-07-16：G1-07-B1-FORMULA-39Q02 第39届第2题公式核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO39-Q02_formula_check_v1.csv`，依据第39届合并PDF第6-8页登记长直螺线管磁场、电感、弹性势能、恒流源做功、平衡方程、等效劲度、电流范围、零电阻闭合回路磁通守恒和评分标准等29条公式核对入口；
- 更新 `03_corpus/manual_review_b1_batch_log.csv`、`manual_review_b1_render_index.csv` 和 `manual_review_b1_batch_summary.md`，记录队列第098项 `CPHO39-Q02-FORMULA` 的证据边界，并将下一最小任务调整为C组队列第101项 `CPHO40-Q03-FIG`；
- 新增第39届第2题共5张页面证据图：题面第2页、答案第6-8页和第9页下一题边界确认图；视觉检查确认第2题题面位于试题PDF第2页上半部，答案第8页以式(23)和评分标准结束，第9页进入第3题；
- 更新 `03_corpus/item_texts/CPHO39-Q02.md`、`03_corpus/item_materials.csv`、`03_corpus/item_index.csv`、`03_corpus/manual_review_checklist.csv` 和 `03_corpus/manual_review_priority_followup.csv`，将 `CPHO39-Q02-FORMULA` 推进为“答案公式核对入口完成，待最终复核”，并将第39届第2题两个小问答案页入口统一为 `6-8`；
- 标记 `mu0`、`Psi`、`l/l0/l_p/l_p_prime`、`I0/I0_prime`、恒流源做功负号、式(13)等效劲度、式(16)根号范围、式(18)磁能表达、式(22)(23)撇号和评分标准为待最终复核；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，记录B组第098项已建立公式核对入口，并将下一最小任务调整为 `G1-07-C1-FIG-40Q03`；队列第099项和第100项仍需真实确认记录才能正式销项；
- 本轮不改写论文正文，不修改原始PDF，不生成正式编码结果、正式统计、正式案例结论、真实评分者记录或人工校对签名。

## 2026-07-16：G1-07-B1-FORMULA-36Q06 第36届第6题公式核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO36-Q06_formula_check_v1.csv`，依据第36届合并PDF第29-33页登记pi介子衰变、相对论动量能量、mu子静止系速度、速度变换、最大/最小速率、半衰期法和平均寿命法概率等31条公式核对入口；
- 更新 `03_corpus/manual_review_b1_batch_log.csv`、`manual_review_b1_render_index.csv` 和 `manual_review_b1_batch_summary.md`，记录队列第097项 `CPHO36-Q06-FORMULA` 的证据边界，并将B组下一最小任务调整为队列第098项 `CPHO39-Q02-FORMULA`；
- 新增第36届第6题共7张页面证据图：题面第5页、答案第29-33页和第34页下一题边界确认图；视觉检查确认第33页上半部仍为第6题另一解法、概率结果和评分标准，第33页下半部进入第7题；
- 更新 `03_corpus/item_texts/CPHO36-Q06.md`、`03_corpus/item_materials.csv`、`03_corpus/item_index.csv`、`03_corpus/manual_review_checklist.csv` 和 `03_corpus/manual_review_priority_followup.csv`，将 `CPHO36-Q06-FORMULA` 推进为“答案公式核对入口完成，待最终复核”，并将第36届第6题两个小问答案页入口由 `29-32` 纠偏为 `29-33`；
- 标记 pi/mu/nu上下标、`m_pi/m_mu` 数字、相对论速度变换长式、`u_min/u_max`、`T_1/2^(0)`、`tau_0`、`rho_max` 两套结果和评分标准为待最终复核；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，记录B组第097项已建立公式核对入口，并将下一最小任务调整为 `G1-07-B1-FORMULA-39Q02`；
- 本轮不改写论文正文，不修改原始PDF，不生成正式编码结果、正式统计、正式案例结论、真实评分者记录或人工校对签名。

## 2026-07-16：G1-07-B1-FORMULA-36Q02 第36届第2题公式核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO36-Q02_formula_check_v1.csv`，依据第36届合并PDF第11-18页登记碰前角速度、质心速度、碰撞冲量、滑滚阶段、纯滚阶段、总位移和评分标准等43条公式核对入口；
- 更新 `03_corpus/manual_review_b1_batch_log.csv`、`manual_review_b1_render_index.csv` 和 `manual_review_b1_batch_summary.md`，记录队列第096项 `CPHO36-Q02-FORMULA` 的证据边界，并将B组下一最小任务调整为队列第097项 `CPHO36-Q06-FORMULA`；
- 新增第36届第2题共11张页面证据图：题面第1-2页、答案第11-18页和第19页下一题边界确认图；视觉检查确认第18页上半部仍为第2题式(24)(25)、总位移和评分标准，第18页下半部进入第3题；
- 更新 `03_corpus/item_texts/CPHO36-Q02.md`、`03_corpus/item_materials.csv`、`03_corpus/item_index.csv`、`03_corpus/manual_review_checklist.csv` 和 `03_corpus/manual_review_priority_followup.csv`，将 `CPHO36-Q02-FORMULA` 推进为“答案公式核对入口完成，待最终复核”，并将第36届第2题两个小问答案页入口由 `11-17` 纠偏为 `11-18`；
- 标记 `omega=sqrt(gr/l)` 根号、`v_C1` 分量、碰撞冲量负号、阶段I/II下标、式(19)(24)(25)长式和评分标准为待最终复核；同题 `CPHO36-Q02-FIG` 仍待人工校对；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，记录B组第096项已建立公式核对入口，并将下一最小任务调整为 `G1-07-B1-FORMULA-36Q06`；
- 本轮不改写论文正文，不修改原始PDF，不生成正式编码结果、正式统计、正式案例结论、真实评分者记录或人工校对签名。

## 2026-07-16：G1-07-B1-FORMULA-36Q01 第36届第1题公式核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO36-Q01_formula_check_v1.csv`，依据第36届合并PDF第8-11页登记质心公式、最佳高度、几何关系、力平衡、力矩平衡、支持力一般式、正压力条件和支持力变化等33条公式核对入口；
- 更新 `03_corpus/manual_review_b1_batch_log.csv`、`manual_review_b1_render_index.csv` 和 `manual_review_b1_batch_summary.md`，记录队列第095项 `CPHO36-Q01-FORMULA` 的证据边界，并将B组下一最小任务调整为队列第096项 `CPHO36-Q02-FORMULA`；
- 新增第36届第1题共6张页面证据图：题面第1页、答案第8-11页和第12页下一题边界确认图；视觉检查确认第11页仍为第1题，包含式(10)-(14)、`N_B>0` 条件和评分标准，第11页下部进入第2题；
- 更新 `03_corpus/item_texts/CPHO36-Q01.md`、`03_corpus/item_materials.csv`、`03_corpus/item_index.csv`、`03_corpus/manual_review_checklist.csv` 和 `03_corpus/manual_review_priority_followup.csv`，将 `CPHO36-Q01-FORMULA` 推进为“答案公式核对入口完成，待最终复核”，并将第36届第1题两个小问答案页入口由 `8-10` 纠偏为 `8-11`；
- 标记 `y_CM`、`lambda=rho*pi*r^2`、`h_max` 根号、`O'A/O'B/O'O''` 几何关系、`Q/P`、式(9)两种力矩写法、`N_B/N_A/N_C` 展开式、`N_B>0` 条件、`Delta N_B` 与 `Delta N_A=Delta N_C` 最终式为待最终复核；同题 `CPHO36-Q01-FIG` 仍待人工校对；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，记录B组第095项已建立公式核对入口，并将下一最小任务调整为 `G1-07-B1-FORMULA-36Q02`；
- 本轮不改写论文正文，不修改原始PDF，不生成正式编码结果、正式统计、正式案例结论、真实评分者记录或人工校对签名；按用户要求完成后提交Git。

## 2026-07-16：G1-07-B1-FORMULA-35Q07 第35届第7题公式核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO35-Q07_formula_check_v1.csv`，依据第35届合并PDF第31-35页登记题面光学说明、图a/图b尺寸标注、单缝暗纹条件、空间周期、`d1/d2/d'`、`p/R/p'/R'` 等29条公式核对入口；
- 更新 `03_corpus/manual_review_b1_batch_log.csv`、`manual_review_b1_render_index.csv` 和 `manual_review_b1_batch_summary.md`，记录队列第094项 `CPHO35-Q07-FORMULA` 的证据边界，并将B组下一最小任务调整为队列第095项 `CPHO36-Q01-FORMULA`；
- 新增第35届第7题共7张页面证据图：题面第4页、答案第31-35页和第36页下一题边界确认图；视觉检查确认第31页上半部为第6题收尾，第7题从第31页下半部开始，第35页上半部为第7题收尾，第35页下半部进入第8题；
- 更新 `03_corpus/item_texts/CPHO35-Q07.md`、`03_corpus/item_materials.csv`、`03_corpus/item_index.csv`、`03_corpus/manual_review_checklist.csv` 和 `03_corpus/manual_review_priority_followup.csv`，将 `CPHO35-Q07-FORMULA` 推进为“答案公式核对入口完成，待最终复核”，并将第35届第7题两个小问答案页入口统一为 `31-35`；
- 标记 `phi/phi'`、`X1/X2/X'`、`d1/d2/d'`、`p/R/p'/R'`、小角近似、图a/图b尺寸标注和“4级亮纹失踪”说明为待最终复核；同题 `CPHO35-Q07-FIG` 与 `CPHO35-Q07-SCORE` 仍待人工校对；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，记录B组第094项已建立公式核对入口，并将下一最小任务调整为 `G1-07-B1-FORMULA-36Q01`；
- 本轮不改写论文正文，不修改原始PDF，不生成正式编码结果、正式统计、正式案例结论、真实评分者记录或人工校对签名；按用户要求完成后提交Git。

## 2026-07-16：G1-07-B1-FORMULA-35Q01 第35届第1题公式核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO35-Q01_formula_check_v1.csv`，依据第35届合并PDF第6-9页登记题面给定积分、能量守恒、角动量守恒、周期运动上下界、落地速度、方向角、极坐标方程、时间积分、`a/b/c` 与 `Delta`、最终时间表达式和临界时间等34条公式核对入口；
- 更新 `03_corpus/manual_review_b1_batch_log.csv`、`manual_review_b1_render_index.csv` 和 `manual_review_b1_batch_summary.md`，记录队列第093项 `CPHO35-Q01-FORMULA` 的证据边界，并将B组下一最小任务调整为队列第094项 `CPHO35-Q07-FORMULA`；
- 新增第35届第1题共5张页面证据图：题面第1页、答案第6-9页；视觉检查确认第9页上半部仍为第1题式⑭时间积分、参数 `a/b/c`、`Delta`、式⑮最终时间表达式和临界时间结果，第9页下半部进入第2题；
- 更新 `03_corpus/item_texts/CPHO35-Q01.md`、`03_corpus/item_materials.csv`、`03_corpus/item_index.csv`、`03_corpus/manual_review_checklist.csv` 和 `03_corpus/manual_review_priority_followup.csv`，将 `CPHO35-Q01-FORMULA` 推进为“答案公式核对入口完成，待最终复核”，并将第35届第1题两个小问答案页入口由 `6-8` 纠偏为 `6-9`；
- 标记 `v0min`、周期运动上下界、落地速度根号、`alpha` 展开式、极坐标能量式、径向速度式、式⑭时间积分、`a/b/c` 与 `Delta` 定义、式⑮最终时间表达式和临界时间为待最终复核；同题 `CPHO35-Q01-SCORE` 仍待人工复核；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，记录B组第093项已建立公式核对入口，并将下一最小任务调整为 `G1-07-B1-FORMULA-35Q07`；
- 本轮不改写论文正文，不修改原始PDF，不生成正式编码结果、正式统计、正式案例结论、真实评分者记录或人工校对签名；按用户要求完成后提交Git。

## 2026-07-16：G1-07-B1-FORMULA-39Q01 第39届第1题公式核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO39-Q01_formula_check_v1.csv`，依据第39届合并PDF第5-6页登记相位突变差异、等倾干涉亮纹条件、反射镜移动周期、亮条纹数、石英槽倾角、光程差、折射率公式和评分标准等30条公式核对入口；
- 更新 `03_corpus/manual_review_b1_batch_log.csv`、`manual_review_b1_render_index.csv` 和 `manual_review_b1_batch_summary.md`，记录队列第092项 `CPHO39-Q01-FORMULA` 的证据边界，并将B组下一最小任务调整为队列第093项 `CPHO35-Q01-FORMULA`；
- 新增第39届第1题共4张页面证据图：题面第1页、答案第5-6页和第7页下一题边界确认图；视觉检查确认第1题题面完整位于试题PDF第1页，答案第6页上半部仍为第1题，第6页下半部进入第2题，第7页为第2题延续；
- 更新 `03_corpus/item_texts/CPHO39-Q01.md`、`03_corpus/item_materials.csv`、`03_corpus/item_index.csv`、`03_corpus/manual_review_checklist.csv` 和 `03_corpus/manual_review_priority_followup.csv`，将 `CPHO39-Q01-FORMULA` 推进为“答案公式核对入口完成，待最终复核”，并将第39届第1题三个小问答案页入口统一为 `5-6`；
- 标记 `Delta phi`、`gamma_M`、`Delta d`、亮条纹数 `m`、`theta/i`、`Delta L(theta)`、根号范围、`Delta N=N2-N1=7`、`n=1.41` 和评分标准为待最终复核；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，记录B组第092项已建立公式核对入口，并将下一最小任务调整为 `G1-07-B1-FORMULA-35Q01`；
- 本轮不改写论文正文，不修改原始PDF，不生成正式编码结果、正式统计、正式案例结论、真实评分者记录或人工校对签名；按用户要求完成后提交Git。

## 2026-07-16：G1-07-B1-FORMULA-36Q05 第36届第5题公式核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO36-Q05_formula_check_v1.csv`，依据第36届合并PDF第24-29页登记光纤全反射条件、球面折射成像、虚物符号、微球透镜等效焦距、几何方法、长根式表达式和评分标准等46条公式核对入口；
- 更新 `03_corpus/manual_review_b1_batch_log.csv`、`manual_review_b1_render_index.csv` 和 `manual_review_b1_batch_summary.md`，记录队列第091项 `CPHO36-Q05-FORMULA` 的证据边界，并将B组下一最小任务调整为队列第092项 `CPHO39-Q01-FORMULA`；
- 新增第36届第5题共8张页面证据图：题面第4-5页、答案第24-29页；视觉检查确认第5题题面从试题PDF第4页下部开始并延续至第5页上部，答案第29页上半部仍包含第5题解法三收尾和评分标准，下半部进入第6题；
- 更新 `03_corpus/item_texts/CPHO36-Q05.md`、`03_corpus/item_materials.csv`、`03_corpus/item_index.csv`、`03_corpus/manual_review_checklist.csv` 和 `03_corpus/manual_review_priority_followup.csv`，将 `CPHO36-Q05-FORMULA` 推进为“答案公式核对入口完成，待最终复核”，并将第36届第5题三个小问答案页入口由 `24-28` 纠偏为 `24-29`；
- 标记 `n0/n/n1/n2` 下标、`theta/theta_prime`、`O/O'`、球面折射符号、`r2=-D/2`、近轴近似、长根式表达式和第29页评分边界为待最终复核；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，记录B组第091项已建立公式核对入口，并将下一最小任务调整为 `G1-07-B1-FORMULA-39Q01`；
- 本轮不改写论文正文，不修改原始PDF，不生成正式编码结果、正式统计、正式案例结论、真实评分者记录或人工校对签名；按用户要求完成后提交Git。

## 2026-07-16：G1-07-B1-FORMULA-36Q04 第36届第4题公式核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO36-Q04_formula_check_v1.csv`，依据第36届合并PDF第21-24页登记题面声速与体积弹性模量关系、理想气体密度、绝热过程、空气柱简谐振动、亥姆霍兹共振频率、面积比和评分标准等31条公式核对入口；
- 更新 `03_corpus/manual_review_b1_batch_log.csv`、`manual_review_b1_render_index.csv` 和 `manual_review_b1_batch_summary.md`，记录队列第090项 `CPHO36-Q04-FORMULA` 的证据边界，并将B组下一最小任务调整为队列第091项 `CPHO36-Q05-FORMULA`；
- 新增第36届第4题共6张页面证据图：题面第3-4页、答案第21-24页；视觉检查确认第4题题面从试题PDF第3页下半部开始，第4页上半部结束，答案第24页上半部仍包含第4题式(13)至式(17)和评分标准，下半部进入第5题；
- 更新 `03_corpus/item_texts/CPHO36-Q04.md`、`03_corpus/item_materials.csv`、`03_corpus/item_index.csv`、`03_corpus/manual_review_checklist.csv` 和 `03_corpus/manual_review_priority_followup.csv`，将 `CPHO36-Q04-FORMULA` 推进为“答案公式核对入口完成，待最终复核”，并将第36届第4题三个小问答案页入口由 `21-23` 纠偏为 `21-24`；
- 标记小写 `l` 与大写 `I` 字形混淆、`V0` 下标、`kappa/rho`、`gamma=7/5`、`p_biao/rho_biao`、圆频率根号、`f0` 根号覆盖范围、`S1/S2` 面积比方向和页内第5题边界为待最终复核；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，记录B组第090项已建立公式核对入口，并将下一最小任务调整为 `G1-07-B1-FORMULA-36Q05`；
- 本轮不改写论文正文，不修改原始PDF，不生成正式编码结果、正式统计、正式案例结论、真实评分者记录或人工校对签名；按用户要求完成后提交Git。

## 2026-07-16：G1-07-B1-FORMULA-35Q06 第35届第6题公式核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO35-Q06_formula_check_v1.csv`，依据第35届合并PDF第28-31页登记题面常量、外表面辐射求 `T2`、球壳导热求 `T1`、多次反射吸收、几何因子 `k`、热稳定条件和 `T0 = 227 K` 等38条公式核对入口；
- 更新 `03_corpus/manual_review_b1_batch_log.csv`、`manual_review_b1_render_index.csv` 和 `manual_review_b1_batch_summary.md`，记录队列第089项 `CPHO35-Q06-FORMULA` 的证据边界，并将B组下一最小任务调整为队列第090项 `CPHO36-Q04-FORMULA`；
- 新增第35届第6题共5张页面证据图：题面第3页、答案第28-31页；视觉检查确认第6题题面完整位于试题PDF第3页下半部，答案第28页上半部为第5题收尾，第6题从第28页下半部开始，第31页上半部给出 `T0 = 227 K` 并结束，下半部进入第7题；
- 更新 `03_corpus/item_texts/CPHO35-Q06.md`、`03_corpus/item_materials.csv`、`03_corpus/item_index.csv`、`03_corpus/manual_review_checklist.csv` 和 `03_corpus/manual_review_priority_followup.csv`，将 `CPHO35-Q06-FORMULA` 推进为“答案公式核对入口完成，待最终复核”，并将第35届第6题三个小问答案页入口统一为 `28-31`；
- 标记 `e/E` 大小写、`T/T0/T1/T2` 下标、`Q_prime/Q_doubleprime`、角积分几何因子 `k`、式⑬与式⑭级数因子关系、`1-(1-e)k(1-E)` 分母、`R1/R2/r` 平方和导热系数单位为待最终复核；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，记录B组第089项已建立公式核对入口，并将下一最小任务调整为 `G1-07-B1-FORMULA-36Q04`；
- 本轮不改写论文正文，不修改原始PDF，不生成正式编码结果、正式统计、正式案例结论、真实评分者记录或人工校对签名；按用户要求完成后提交Git。

## 2026-07-15：G1-07-B1-FORMULA-35Q05 第35届第5题公式核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO35-Q05_formula_check_v1.csv`，依据第35届合并PDF第19-28页登记题面变量、旋转参考系、受力方程、坐标变换、五种解法、三频谱线、弱场间隔和边界等50条公式核对入口；
- 更新 `03_corpus/manual_review_b1_batch_log.csv`、`manual_review_b1_render_index.csv` 和 `manual_review_b1_batch_summary.md`，记录队列第088项 `CPHO35-Q05-FORMULA` 的证据边界，并将B组下一最小任务调整为队列第089项 `CPHO35-Q06-FORMULA`；
- 新增第35届第5题共12张页面证据图：题面第2-3页、答案第19-28页；视觉检查确认第5题题面从试题PDF第2页下部开始，第3页上部结束，答案第19页上半部为第4题收尾，第5题从第19页中下部开始，第28页上半部结束且下半部进入第6题；
- 更新 `03_corpus/item_texts/CPHO35-Q05.md`、`03_corpus/item_materials.csv`、`03_corpus/item_index.csv`、`03_corpus/manual_review_checklist.csv` 和 `03_corpus/manual_review_priority_followup.csv`，将 `CPHO35-Q05-FORMULA` 推进为“答案公式核对入口完成，待最终复核”，并将第35届第5题三个小问答案页入口统一为 `19-28`；
- 标记题面 `B=(2m/e)omega_L`、科里奥利力、`omega_L` 方向、prime符号、二阶导数点号、`sqrt(omega_0^2+omega_L^2)` 根号范围、`A_+/A_-` 相位组合、极坐标 `rho/theta` 点号、重复式号和第35届第5题分值边界为待最终复核；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，记录B组第088项已建立公式核对入口，并将下一最小任务调整为 `G1-07-B1-FORMULA-35Q06`；
- 本轮不改写论文正文，不修改原始PDF，不生成正式编码结果、正式统计、正式案例结论、真实评分者记录或人工校对签名；按用户要求完成后提交Git。

## 2026-07-15：G1-07-B1-FORMULA-39Q07 第39届第7题公式核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO39-Q07_formula_check_v1.csv`，依据第39届合并PDF第27-29页登记题面分布函数、压强-能量密度关系、解法二压强积分、平均能量积分、`P=n k_B T`、摩尔热容、热容比、绝热膨胀半径和评分标准等31条公式核对入口；
- 更新 `03_corpus/manual_review_b1_batch_log.csv`、`manual_review_b1_render_index.csv` 和 `manual_review_b1_batch_summary.md`，记录队列第087项 `CPHO39-Q07-FORMULA` 的证据边界，并将B组下一最小任务调整为队列第088项 `CPHO35-Q05-FORMULA`；
- 新增第39届第7题共4张页面证据图：题面第4页、答案第27-29页；视觉检查确认第7题题面从试题PDF第4页中下部开始，上方为第6题尾部，答案第27页上半部为第6题评分标准，第7题答案从第27页中部开始，第28页覆盖第(1)(2)问积分推导和状态方程，第29页覆盖第(3)(4)问、最终半径和评分标准，且为PDF末页；
- 更新 `03_corpus/item_texts/CPHO39-Q07.md`、`03_corpus/item_materials.csv`、`03_corpus/item_index.csv`、`03_corpus/manual_review_checklist.csv` 和 `03_corpus/manual_review_priority_followup.csv`，将 `CPHO39-Q07-FORMULA` 推进为“答案公式核对入口完成，待最终复核”，并将第39届第7题四个小问答案页入口统一为 `27-29`；
- 标记题面分布函数、矢量点乘、上标 `(+)`、各向同性 `1/3` 因子、`beta=(k_B T)^(-1)`、`g(beta)` 导数、`C_P/C_V`、绝热指数、最终半径和评分标准为待最终复核；解题图7a/7b仅为答案推导图，未作真实人工销项；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，记录B组第087项已建立公式核对入口，并将下一最小任务调整为 `G1-07-B1-FORMULA-35Q05`；
- 本轮不改写论文正文，不修改原始PDF，不生成正式编码结果、正式统计、正式案例结论、真实评分者记录或人工校对签名；按用户要求完成后提交Git。

## 2026-07-15：G1-07-B1-FORMULA-39Q05 第39届第5题公式核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO39-Q05_formula_check_v1.csv`，依据第39届合并PDF第20-23页登记题面分段外力、运动方程、两种解法、初始条件、长度差、先断条件、相位区间、给定 `L` 条件、同时断裂关系和评分标准等38条公式核对入口；
- 更新 `03_corpus/manual_review_b1_batch_log.csv`、`manual_review_b1_render_index.csv` 和 `manual_review_b1_batch_summary.md`，记录队列第086项 `CPHO39-Q05-FORMULA` 的证据边界，并将B组下一最小任务调整为队列第087项 `CPHO39-Q07-FORMULA`；
- 新增第39届第5题共6张页面证据图：题面第3页、答案第20-23页和第24页下一题边界确认图；视觉检查确认第5题题面位于试题PDF第3页中上部且无题图，答案第20页为起点，第21页覆盖第(2)问收尾和第(3)问开头，第22页覆盖第(3)问相位条件，第23页上半部为第(4)问和评分标准，第23页下半部与第24页进入第6题；
- 更新 `03_corpus/item_texts/CPHO39-Q05.md`、`03_corpus/item_materials.csv`、`03_corpus/item_index.csv`、`03_corpus/manual_review_checklist.csv` 和 `03_corpus/manual_review_priority_followup.csv`，将 `CPHO39-Q05-FORMULA` 推进为“答案公式核对入口完成，待最终复核”，并将第39届第5题四个小问答案页入口统一为 `20-23`；
- 标记二阶导数、平衡位置上横线、`omega=sqrt(k/m)`、`sqrt(m/k)`、`arcsin` 相位区间、端点开闭、`x1` 点号、给定 `L` 条件和同时断裂关系为待最终复核；本题无题图，但公式与评分标准仍未完成真实人工销项；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，记录B组第086项已建立公式核对入口，并将下一最小任务调整为 `G1-07-B1-FORMULA-39Q07`；
- 本轮不改写论文正文，不修改原始PDF，不生成正式编码结果、正式统计、正式案例结论、真实评分者记录或人工校对签名；按用户要求完成后提交Git。

## 2026-07-15：G1-07-B1-FORMULA-39Q03 第39届第3题公式核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO39-Q03_formula_check_v1.csv`，依据第39届合并PDF第9-12页登记题面变量、抛体运动、碰撞动量/角动量、递推关系、三种解法、总冲量和评分标准等45条公式核对入口；
- 更新 `03_corpus/manual_review_b1_batch_log.csv`、`manual_review_b1_render_index.csv` 和 `manual_review_b1_batch_summary.md`，记录队列第085项 `CPHO39-Q03-FORMULA` 的证据边界，并将B组下一最小任务调整为队列第086项 `CPHO39-Q05-FORMULA`；
- 新增第39届第3题共6张页面证据图：题面第2页、答案第9-12页和第13页下一题边界确认图；视觉检查确认第3题题面位于试题PDF第2页中部，答案第9页为起点，第10-11页覆盖第(3)问三种解法，第12页上半部为第(4)问式㉖至㉛和评分标准，第12页下半部与第13页进入第4题；
- 更新 `03_corpus/item_texts/CPHO39-Q03.md`、`03_corpus/item_materials.csv`、`03_corpus/item_index.csv`、`03_corpus/manual_review_checklist.csv` 和 `03_corpus/manual_review_priority_followup.csv`，将 `CPHO39-Q03-FORMULA` 推进为“答案公式核对入口完成，待最终复核”，并将第39届第3题四个小问答案页入口统一为 `9-12`；
- 保留同题 `CPHO39-Q03-FIG` 为未销项状态；式⑨中的 `I`、`2/5` 和 `10/7` 等系数、prime/doubleprime式号、矩阵 `A`、`A^2=J`、总冲量矢量和单位矢量均标记为待最终复核；
- 更新 `PROJECT_STATUS.md`、`TASKS.md` 和 `03_corpus/manual_review_priority_followup_summary.md`，记录B组第085项已建立公式核对入口，并将下一最小任务调整为 `G1-07-B1-FORMULA-39Q05`；
- 本轮不改写论文正文，不修改原始PDF，不生成正式编码结果、正式统计、正式案例结论、真实评分者记录或人工校对签名；按用户要求完成后提交Git。

## 2026-07-15：G1-07-B1-FORMULA-35Q08 第35届第8题公式核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO35-Q08_formula_check_v1.csv`，依据第35届合并PDF第35-38页登记题面常量、发射/吸收守恒方程、频率差、反冲能、共振条件、无反冲能量与频率范围、多普勒速度范围和频率变化测量速度等41条公式核对入口；
- 更新 `03_corpus/manual_review_b1_batch_log.csv`、`manual_review_b1_render_index.csv` 和 `manual_review_b1_batch_summary.md`，记录队列第084项 `CPHO35-Q08-FORMULA` 的证据边界，并将B组下一最小任务调整为队列第085项 `CPHO39-Q03-FORMULA`；
- 新增第35届第8题共5张页面证据图：题面第5页、答案第35-38页；视觉检查确认第8题题面完整位于试题PDF第5页且无题图，答案第35页上部为第7题尾部，第8题从题面重印和参考解答开始，第36-38页覆盖式①至式⑳，第38页为答案收尾且为PDF末页；
- 更新 `03_corpus/item_texts/CPHO35-Q08.md`、`03_corpus/item_materials.csv`、`03_corpus/item_index.csv`、`03_corpus/manual_review_checklist.csv` 和 `03_corpus/manual_review_priority_followup.csv`，将 `CPHO35-Q08-FORMULA` 推进为“答案公式核对入口完成，待最终复核”，并将第35届第8题四个小问答案页入口统一为 `35-38`；
- 保留同题 `CPHO35-Q08-SCORE` 为未销项状态；`nu_e/nu_a` 表述差异、`Gamma` 线宽范围、重复式号⑰、多普勒根号近似、式⑲速度单位与式⑳正负号均标记为待最终复核；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，记录B组第084项已建立公式核对入口，并将下一最小任务调整为 `G1-07-B1-FORMULA-39Q03`；
- 本轮不改写论文正文，不修改原始PDF，不生成正式编码结果、正式统计、正式案例结论、真实评分者记录或人工校对签名；按用户要求完成后提交Git。

## 2026-07-15：G1-07-B1-FORMULA-35Q04 第35届第4题公式核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO35-Q04_formula_check_v1.csv`，依据第35届合并PDF第16-19页登记题面变量、导线坐标、`B1` 至 `B4`、总磁场、近原点展开、势能、作用力、逸出位置和动能等36条公式核对入口；
- 更新 `03_corpus/manual_review_b1_batch_log.csv`、`manual_review_b1_render_index.csv` 和 `manual_review_b1_batch_summary.md`，记录队列第083项 `CPHO35-Q04-FORMULA` 的证据边界，并将B组下一最小任务调整为队列第084项 `CPHO35-Q08-FORMULA`；
- 新增第35届第4题共6张页面证据图：题面第2页、答案第16-19页和第20页下一题边界确认图；视觉检查确认第4题题面位于试题PDF第2页中部，答案第16页为题面重印和参考解答起点，第17-18页为核心公式，第19页上半部为式⑳和答案结束，第20页已进入第5题；
- 更新 `03_corpus/item_texts/CPHO35-Q04.md`、`03_corpus/item_materials.csv`、`03_corpus/item_index.csv`、`03_corpus/manual_review_checklist.csv` 和 `03_corpus/manual_review_priority_followup.csv`，将 `CPHO35-Q04-FORMULA` 推进为“答案公式核对入口完成，待最终复核”，并将第35届第4题四个小问答案页入口统一为 `16-19`；
- 保留同题 `CPHO35-Q04-FIG` 和 `CPHO35-Q04-SCORE` 为未销项状态；`B1` 至 `B4` 正负号、式⑤长式、式⑫/⑮/⑯/⑲/⑳根号覆盖范围、`3sqrt(3)/8` 系数和式⑳中 `-1` 是否在根号外均标记为待最终复核；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，记录B组第083项已建立公式核对入口，并将下一最小任务调整为 `G1-07-B1-FORMULA-35Q08`；
- 本轮不改写论文正文，不修改原始PDF，不生成正式编码结果、正式统计、正式案例结论、真实评分者记录或人工校对签名；按用户要求完成后提交Git。

## 2026-07-15：G1-07-B1-FORMULA-35Q03 第35届第3题公式核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO35-Q03_formula_check_v1.csv`，依据第35届合并PDF第13-16页登记题面变量、打击中心、碰撞后质心位置、角速度、转动惯量、轴力分量、撤轴后平抛叠加转动和高度差等42条公式核对入口；
- 更新 `03_corpus/manual_review_b1_batch_log.csv`、`manual_review_b1_render_index.csv` 和 `manual_review_b1_batch_summary.md`，记录队列第082项 `CPHO35-Q03-FORMULA` 的证据边界，并将B组下一最小任务调整为队列第083项 `CPHO35-Q04-FORMULA`；
- 新增第35届第3题共7张页面证据图：题面第1-2页、答案第13-16页和第17页下一题边界确认图；视觉检查确认第3题题面从第1页页底开始至第2页上半部结束，答案从第13页中部开始至第16页式⑳结束，第16页下半部和第17页进入第4题；
- 更新 `03_corpus/item_texts/CPHO35-Q03.md`、`03_corpus/item_materials.csv`、`03_corpus/item_index.csv`、`03_corpus/manual_review_checklist.csv` 和 `03_corpus/manual_review_priority_followup.csv`，将 `CPHO35-Q03-FORMULA` 推进为“答案公式核对入口完成，待最终复核”，并将第35届第3题四个小问答案页入口统一为 `13-16`；
- 保留同题 `CPHO35-Q03-FIG` 和 `CPHO35-Q03-SCORE` 为未销项状态；`l/1` 混淆、`L_c/x_B/y_B/omega_0/omega'/beta'` 上下标和撇号、式⑨/⑮/⑲/⑳根号和绝对值范围均标记为待最终复核；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，记录B组第082项已建立公式核对入口，并将下一最小任务调整为 `G1-07-B1-FORMULA-35Q04`；
- 本轮不改写论文正文，不修改原始PDF，不生成正式编码结果、正式统计、正式案例结论、真实评分者记录或人工校对签名；按用户要求完成后提交Git。

## 2026-07-15：G1-07-B1-FORMULA-35Q02 第35届第2题公式核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO35-Q02_formula_check_v1.csv`，依据第35届合并PDF第9-13页登记题面变量、摩擦阈值、往返递推、最终位置四段式、总路程三段式和边界等41条公式核对入口；
- 更新 `03_corpus/manual_review_b1_batch_log.csv`、`manual_review_b1_render_index.csv` 和 `manual_review_b1_batch_summary.md`，记录队列第081项 `CPHO35-Q02-FORMULA` 的证据边界，并将B组下一最小任务调整为队列第082项 `CPHO35-Q03-FORMULA`；
- 新增第35届第2题共7张页面证据图：题面第1页、答案第9-13页和第14页下一题边界确认图；视觉检查确认第2题位于试题PDF第1页中部，答案从第9页下半部开始至第13页式⑳结束，第13页下方和第14页进入第3题；
- 更新 `03_corpus/item_texts/CPHO35-Q02.md`、`03_corpus/item_materials.csv`、`03_corpus/item_index.csv`、`03_corpus/manual_review_checklist.csv` 和 `03_corpus/manual_review_priority_followup.csv`，将 `CPHO35-Q02-FORMULA` 推进为“答案公式核对入口完成，待最终复核”，并将第35届第2题四个小问答案页入口统一为 `9-13`；
- 保留同题 `CPHO35-Q02-FIG` 和 `CPHO35-Q02-SCORE` 为未销项状态；式①至式⑳的阈值、不等号开闭、`B1/A1/Bn/An` 上下标和式⑱至式⑳总路程分段均标记为待最终复核；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，记录B组第081项已建立公式核对入口，并将下一最小任务调整为 `G1-07-B1-FORMULA-35Q03`；
- 本轮不改写论文正文，不修改原始PDF，不生成正式编码结果、正式统计、正式案例结论、真实评分者记录或人工校对签名；按用户要求完成后提交Git。

## 2026-07-15：G1-07-B1-FORMULA-39Q06 第39届第6题公式核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO39-Q06_formula_check_v1.csv`，依据第39届合并PDF第23-27页登记题面模型设定、斐克定律、扩散系数、高斯定理、边界条件、线性化方程、`delta n(x)`、`delta T(x)`、Seebeck系数和评分标准等44条公式核对入口；
- 更新 `03_corpus/manual_review_b1_batch_log.csv`、`manual_review_b1_render_index.csv` 和 `manual_review_b1_batch_summary.md`，记录队列第080项 `CPHO39-Q06-FORMULA` 的证据边界，并将B组下一最小任务调整为队列第081项 `CPHO35-Q02-FORMULA`；
- 新增第39届第6题共8张页面证据图：题面第3-4页、答案第23-27页和第28页下一题边界确认图；视觉检查确认第6题题面从PDF第3页下部开始至第4页中部结束，答案从第23页底部开始至第27页评分标准结束，第28页进入第7题；
- 更新 `03_corpus/item_texts/CPHO39-Q06.md`、`03_corpus/item_materials.csv`、`03_corpus/item_index.csv`、`03_corpus/manual_review_checklist.csv` 和 `03_corpus/manual_review_priority_followup.csv`，将 `CPHO39-Q06-FORMULA` 推进为“答案公式核对入口完成，待最终复核”，并将第39届第6题五个小问答案页入口统一为 `23-27`；
- 保留同题 `CPHO39-Q06-FIG` 为未销项状态；`sqrt(T(x))`、`sqrt(T0)`、`lambda` 定义、`sigma_+`/`sigma_-` 左右边界符号、`delta T(x)` 长式、Seebeck系数整体负一次方和评分标准式号引用均标记为待最终复核；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，记录B组第080项已建立公式核对入口，并将下一最小任务调整为 `G1-07-B1-FORMULA-35Q02`；
- 本轮不改写论文正文，不修改原始PDF，不生成正式编码结果、正式统计、正式案例结论、真实评分者记录或人工校对签名；按用户要求完成后提交Git。

## 2026-07-15：G1-07-B1-FORMULA-39Q04 第39届第4题公式核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO39-Q04_formula_check_v1.csv`，依据第39届合并PDF第12-19页登记题面常量、L系与S系机械能、平衡力矩条件、tan/cot两套图解法、第III象限参数条件、受力图入口、微扰法、势能法、稳定性判断和评分标准等56条公式核对入口；
- 更新 `03_corpus/manual_review_b1_batch_log.csv`、`manual_review_b1_render_index.csv` 和 `manual_review_b1_batch_summary.md`，记录队列第079项 `CPHO39-Q04-FORMULA` 的证据边界，并将B组下一最小任务调整为队列第080项 `CPHO39-Q06-FORMULA`；
- 新增第39届第4题共11张页面证据图：题面第2-3页、答案第12-19页和第20页下一题边界确认图；视觉检查确认第4题题面从PDF第2页下部开始至第3页顶部结束，答案从第12页下部开始至第19页评分标准结束，第20页进入第5题；
- 更新 `03_corpus/item_texts/CPHO39-Q04.md`、`03_corpus/item_materials.csv`、`03_corpus/item_index.csv`、`03_corpus/manual_review_checklist.csv` 和 `03_corpus/manual_review_priority_followup.csv`，将 `CPHO39-Q04-FORMULA` 推进为“答案公式核对入口完成，待最终复核”，并将第39届第4题五个小问答案页入口统一为 `12-19`；
- 保留同题 `CPHO39-Q04-FIG` 为未销项状态；第14页式(14)符号、第15至17页第III象限参数条件的幂次/不等号、第17至19页稳定性推导和解题图4a/4a'/4b均标记为待最终复核；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，记录B组第079项已建立公式核对入口，并将下一最小任务调整为 `G1-07-B1-FORMULA-39Q06`；
- 本轮不改写论文正文，不修改原始PDF，不生成正式编码结果、正式统计、正式案例结论、真实评分者记录或人工校对签名，也不提交Git。

## 2026-07-15：G1-07-B1-FORMULA-36Q07 第36届第7题公式核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO36-Q07_formula_check_v1.csv`，依据第36届合并PDF第35-40页登记题面常量、平行板电容模型、镜像电荷法、圆盘法、闪电通道电荷密度、光环几何速度、大气压强积分、空气密度、气球体积和评分标准等50条公式核对入口；
- 更新 `03_corpus/manual_review_b1_batch_log.csv`、`manual_review_b1_render_index.csv` 和 `manual_review_b1_batch_summary.md`，记录队列第078项 `CPHO36-Q07-FORMULA` 的证据边界，并将B组下一最小任务调整为队列第079项 `CPHO39-Q04-FORMULA`；
- 新增第36届第7题共11张页面证据图：题面第5-7页、答案第33-40页；视觉检查确认第7题题面从PDF第5页下部开始至第7页上部结束，答案第33-34页为题面重印，第35页开始参考解答，第40页给出第(5)问结果和评分标准并为PDF末页；
- 更新 `03_corpus/item_texts/CPHO36-Q07.md`、`03_corpus/item_materials.csv`、`03_corpus/item_index.csv`、`03_corpus/manual_review_checklist.csv` 和 `03_corpus/manual_review_priority_followup.csv`，将 `CPHO36-Q07-FORMULA` 推进为“答案公式核对入口完成，待最终复核”，并将第36届第7题五个小问答案页入口统一为 `33-40`；
- 保留同题 `CPHO36-Q07-FIG` 为未销项状态；第36页圆盘法地表电场表达式、第37至38页几何线段分母、第4问频率关系和第40页 `rho_1` 单位均标记为待最终复核；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，记录B组第078项已建立公式核对入口，并将下一最小任务调整为 `G1-07-B1-FORMULA-39Q04`；
- 本轮不改写论文正文，不修改原始PDF，不生成正式编码结果、正式统计、正式案例结论、真实评分者记录或人工校对签名，也不提交Git。

## 2026-07-15：G1-07-B1-FORMULA-36Q03 第36届第3题公式核对入口

- 新增 `03_corpus/manual_review_transcripts/CPHO36-Q03_formula_check_v1.csv`，依据第36届合并PDF第18-21页登记磁场、安培力、加速度、出射速度、磁通量、电动势、电源端电压、恒流源做功、出射动能和能量比等28条公式核对入口；
- 新增 `03_corpus/manual_review_b1_batch_log.csv`、`manual_review_b1_render_index.csv` 和 `manual_review_b1_batch_summary.md`，启动B组中风险公式校对入口建设，并记录队列第077项 `CPHO36-Q03-FORMULA` 的证据边界；
- 新增第36届第3题共6张页面证据图：题面第2-3页、答案第18-21页；视觉检查确认第3题题面从PDF第2页下半部开始，第3页上半部结束，答案从第18页中下部开始至第21页评分标准结束；
- 更新 `03_corpus/item_texts/CPHO36-Q03.md`、`03_corpus/item_materials.csv`、`03_corpus/item_index.csv`、`03_corpus/manual_review_checklist.csv` 和 `03_corpus/manual_review_priority_followup.csv`，将第36届第3题答案页范围由 `18-20` 纠偏为 `18-21`；
- 将 `CPHO36-Q03-FORMULA` 推进为“答案公式核对入口完成，待最终复核”；不填写校对人和校对日期，不关闭同题 `CPHO36-Q03-FIG` 图件问题；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，记录B组第077项已建立公式核对入口，并将下一最小任务调整为 `G1-07-B1-FORMULA-36Q07`；
- 本轮不改写论文正文，不修改原始PDF，不生成正式编码结果、正式统计、正式案例结论、真实评分者记录或人工校对签名，也不提交Git。

## 2026-07-15：G1-07-A1-TRANSCRIBE-41Q04 第41届第4题V1转写

- 新增 `03_corpus/manual_review_transcripts/CPHO41-Q04_transcription_v1.md`，基于第41届试题PDF第3页渲染图完成第4题题面V1视觉转写，覆盖质子断层扫描、狭义相对论与极端相对论比较、非相对论散射、固定靶和质子速率估算等题面条件；
- 新增 `03_corpus/manual_review_transcripts/CPHO41-Q04_formula_check_v1.csv`，依据答案PDF第9-11页登记不确定关系、相对论能量-动量关系、极端相对论近似、非相对论散射总能量、能量不确定度、`Delta r/r` 根号和入射质子速率等关键公式核对入口；
- 新增第41届第4题共4张页面证据图：题面第3页、答案第9-11页；视觉检查确认第4题题面完整位于试题PDF第3页上部，同页中下部进入第5题和第6题，答案从PDF第9页下半部开始至第11页评分标准结束，第11页下半部进入第5题；
- 更新 `03_corpus/item_texts/CPHO41-Q04.md`，挂接V1转写稿、公式核对表和页面证据，明确原OCR文本仅作错误来源对照，不得用于正式编码证据；
- 更新 `03_corpus/manual_review_checklist.csv` 和 `03_corpus/manual_review_priority_followup.csv`，将 `CPHO41-Q04-OCR` 推进为“V1视觉转写完成，待最终复核”，将 `CPHO41-Q04-FORMULA` 推进为“答案公式核对入口完成，待最终复核”；不填写校对人和校对日期，不关闭人工销项；
- 更新 `03_corpus/manual_review_a1_batch_log.csv`、`manual_review_a1_render_index.csv` 和 `manual_review_a1_batch_summary.md`，登记A组队列第075-076项的证据、边界和下一步；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，记录A组76项均已建立阶段性证据入口或转写入口，并将下一最小任务调整为 `G1-07-B1-FORMULA-36Q03`；
- 本轮不改写论文正文，不修改原始PDF，不生成正式编码结果、正式统计、正式案例结论、真实评分者记录或人工校对签名，也不提交Git。

## 2026-07-15：G1-07-A1-TRANSCRIBE-41Q03 第41届第3题V1转写

- 新增 `03_corpus/manual_review_transcripts/CPHO41-Q03_transcription_v1.md`，基于第41届试题PDF第2页渲染图完成第3题题面V1视觉转写，覆盖表面张力、油气混合物、等体压强系数、注入“水”温度和分子模型推导等题面条件；
- 新增 `03_corpus/manual_review_transcripts/CPHO41-Q03_formula_check_v1.csv`，依据答案PDF第7-9页登记表面张力关系、等体压强系数、最小值温度、注入水温、分子邻近数模型、摩尔体积和最终表面张力系数表达式等关键公式核对入口；
- 新增第41届第3题共4张页面证据图：题面第2页、答案第7-9页；视觉检查确认第3题题面位于试题PDF第2页下半部，第2页上半部为第2题尾部，答案从PDF第7页下半部开始至第9页评分标准结束，第9页下半部进入第4题；
- 更新 `03_corpus/item_texts/CPHO41-Q03.md`，挂接V1转写稿、公式核对表和页面证据，明确原OCR文本仅作错误来源对照，不得用于正式编码证据；
- 更新 `03_corpus/manual_review_checklist.csv` 和 `03_corpus/manual_review_priority_followup.csv`，将 `CPHO41-Q03-OCR` 推进为“V1视觉转写完成，待最终复核”，将 `CPHO41-Q03-FORMULA` 推进为“答案公式核对入口完成，待最终复核”；不填写校对人和校对日期，不关闭人工销项；
- 更新 `03_corpus/manual_review_a1_batch_log.csv`、`manual_review_a1_render_index.csv` 和 `manual_review_a1_batch_summary.md`，登记A组队列第073-074项的证据、边界和下一步；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，记录第41届第3题已完成V1转写入口，并将下一最小任务调整为 `G1-07-A1-TRANSCRIBE-41Q04`；
- 本轮不改写论文正文，不修改原始PDF，不生成正式编码结果、正式统计、正式案例结论、真实评分者记录或人工校对签名，也不提交Git。

## 2026-07-15：G1-07-A1-TRANSCRIBE-38Q02 第38届第2题V1转写

- 新增 `03_corpus/manual_review_transcripts/CPHO38-Q02_transcription_v1.md`，基于第38届合并PDF第1页渲染图完成第2题题面V1视觉转写，覆盖薄壁玻璃管、水银封闭理想气体、绝热光滑活塞、定体摩尔热容、过程A/B和计算精度等题面条件；
- 新增 `03_corpus/manual_review_transcripts/CPHO38-Q02_formula_check_v1.csv`，依据PDF第7-8页登记过程A初末态、等压做功、过程B状态方程、稳定性判定、摩尔数、内能增加、气体做功、吸热量和评分标准等关键公式核对入口；
- 新增第38届第2题共3张页面证据图：题面第1页、答案第7-8页；视觉检查确认第2题题面位于试题PDF第1页中下部，第1页上部为第1题、下部进入第3题，答案从PDF第7页中部开始至第8页评分标准结束；
- 更新 `03_corpus/item_texts/CPHO38-Q02.md`，挂接V1转写稿、公式核对表、页面证据和图2a题图证据，明确原OCR文本仅作错误来源对照，不得用于正式编码证据；
- 更新 `03_corpus/manual_review_checklist.csv` 和 `03_corpus/manual_review_priority_followup.csv`，将 `CPHO38-Q02-OCR` 推进为“V1视觉转写完成，待最终复核”，将 `CPHO38-Q02-FORMULA` 推进为“答案公式核对入口完成，待最终复核”，并将第38届第2题答案页范围由 `7` 纠偏为 `7-8`；`CPHO38-Q02-FIG` 保持未销项，不填写校对人和校对日期；
- 更新 `03_corpus/manual_review_a1_batch_log.csv`、`manual_review_a1_render_index.csv` 和 `manual_review_a1_batch_summary.md`，登记A组队列第071-072项的证据、边界和下一步；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，记录第38届第2题已完成V1转写入口，并将下一最小任务调整为 `G1-07-A1-TRANSCRIBE-41Q03`；
- 本轮不改写论文正文，不修改原始PDF，不关闭第38届第2题图件问题，不生成正式编码结果、正式统计、正式案例结论、真实评分者记录或人工校对签名，也不提交Git。

## 2026-07-15：G1-07-A1-TRANSCRIBE-37Q05 第37届第5题V1转写

- 新增 `03_corpus/manual_review_transcripts/CPHO37-Q05_transcription_v1.md`，基于第37届合并PDF第3页渲染图完成第5题题面V1视觉转写，覆盖惯性系 `Sigma`、坐标系 `O-xy`、三艘飞行器速度、光信号往返时间、货物速度和图5a边界等题面条件；
- 新增 `03_corpus/manual_review_transcripts/CPHO37-Q05_formula_check_v1.csv`，依据PDF第14-15页登记相对论速度合成、时间膨胀、甲乙追及时间、货物速度分量、发射速度大小、发射角、洛伦兹时间变换和评分标准等关键公式核对入口；
- 新增第37届第5题共3张页面证据图：题面第3页、答案第14-15页；视觉检查确认第5题题面位于试题PDF第3页上半部，第3页下半部进入第6题，答案从PDF第14页页首开始至第15页评分标准结束；
- 更新 `03_corpus/item_texts/CPHO37-Q05.md`，挂接V1转写稿、公式核对表、页面证据和图5a题图证据，明确原OCR文本仅作错误来源对照，不得用于正式编码证据；
- 更新 `03_corpus/manual_review_a1_batch_log.csv`、`manual_review_a1_render_index.csv` 和 `manual_review_a1_batch_summary.md`，登记A组队列第069-070项的证据、边界和下一步；
- 更新 `03_corpus/manual_review_checklist.csv` 和 `03_corpus/manual_review_priority_followup.csv`，将 `CPHO37-Q05-OCR` 推进为“V1视觉转写完成，待最终复核”，将 `CPHO37-Q05-FORMULA` 推进为“答案公式核对入口完成，待最终复核”；`CPHO37-Q05-FIG` 保持未销项，不填写校对人和校对日期；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，记录第37届第5题已完成V1转写入口，并将下一最小任务调整为 `G1-07-A1-TRANSCRIBE-38Q02`；
- 本轮不改写论文正文，不修改原始PDF，不关闭第37届第5题图件问题，不生成正式编码结果、正式统计、正式案例结论、真实评分者记录或人工校对签名，也不提交Git。

## 2026-07-15：G1-07-A1-TRANSCRIBE-37Q04 第37届第4题V1转写

- 新增 `03_corpus/manual_review_transcripts/CPHO37-Q04_transcription_v1.md`，基于第37届合并PDF第2页渲染图完成第4题题面V1视觉转写，覆盖劳伦斯、回旋加速器、Tevatron、高能质子同步加速器、最大回旋圆轨道周长、最大能量、靶质子、反质子产生反应和已知常量等题面条件；
- 新增 `03_corpus/manual_review_transcripts/CPHO37-Q04_formula_check_v1.csv`，依据PDF第12-13页登记相对论运动方程、相对论动量、回旋半径、最小磁感应强度、洛伦兹不变质量、反质子产生阈能、Tevatron能量比较和评分标准等关键公式核对入口；
- 新增第37届第4题共3张页面证据图：题面第2页、答案第12-13页；视觉检查确认第4题题面从试题PDF第2页下半部开始并在本页结束，第2页上半部为第3题，答案从PDF第12页页首开始至第13页评分标准结束；
- 更新 `03_corpus/item_texts/CPHO37-Q04.md`，挂接V1转写稿、公式核对表和页面证据，明确原OCR文本仅作错误来源对照，不得用于正式编码证据；
- 更新 `03_corpus/manual_review_a1_batch_log.csv`、`manual_review_a1_render_index.csv` 和 `manual_review_a1_batch_summary.md`，登记A组队列第067-068项的证据、边界和下一步；
- 更新 `03_corpus/manual_review_checklist.csv` 和 `03_corpus/manual_review_priority_followup.csv`，将 `CPHO37-Q04-OCR` 推进为“V1视觉转写完成，待最终复核”，将 `CPHO37-Q04-FORMULA` 推进为“答案公式核对入口完成，待最终复核”；不填写校对人和校对日期，不关闭人工销项；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，记录第37届第4题已完成V1转写入口，并将下一最小任务调整为 `G1-07-A1-TRANSCRIBE-37Q05`；
- 本轮不改写论文正文，不修改原始PDF，不生成正式编码结果、正式统计、正式案例结论、真实评分者记录或人工校对签名，也不提交Git。

## 2026-07-15：G1-07-A1-TRANSCRIBE-37Q02 第37届第2题V1转写

- 新增 `03_corpus/manual_review_transcripts/CPHO37-Q02_transcription_v1.md`，基于第37届合并PDF第1页渲染图完成第2题题面V1视觉转写，覆盖台球母球、滑动摩擦因数、水平冲量、击打高度、纯滚动时间以及B点位置/速度/加速度等题面条件；
- 新增 `03_corpus/manual_review_transcripts/CPHO37-Q02_formula_check_v1.csv`，依据PDF第7-9页登记动量/角动量关系、滑动摩擦阶段运动方程、纯滚动时间、质心速度、B点运动学表达式、加速度和评分标准等关键公式核对入口；
- 新增第37届第2题共4张页面证据图：题面第1页、答案第7-9页；视觉检查确认第2题题面位于试题PDF第1页下半部，答案从PDF第7页下半部开始，至第9页上半部评分标准结束，第9页下半部进入第3题；
- 更新 `03_corpus/item_texts/CPHO37-Q02.md`，挂接V1转写稿、公式核对表和页面证据，明确原OCR文本仅作错误来源对照，不得用于正式编码证据；
- 更新 `03_corpus/manual_review_a1_batch_log.csv`、`manual_review_a1_render_index.csv` 和 `manual_review_a1_batch_summary.md`，登记A组队列第065-066项的证据、边界和下一步；
- 更新 `03_corpus/manual_review_checklist.csv` 和 `03_corpus/manual_review_priority_followup.csv`，将 `CPHO37-Q02-OCR` 推进为“V1视觉转写完成，待最终复核”，将 `CPHO37-Q02-FORMULA` 推进为“答案公式核对入口完成，待最终复核”；不填写校对人和校对日期，不关闭人工销项；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，记录第37届第2题已完成V1转写入口，并将下一最小任务调整为 `G1-07-A1-TRANSCRIBE-37Q04`；
- 本轮不改写论文正文，不修改原始PDF，不生成正式编码结果、正式统计、正式案例结论、真实评分者记录或人工校对签名，也不提交Git。

## 2026-07-15：G1-07-A1-TRANSCRIBE-37Q01 第37届第1题V1转写

- 新增 `03_corpus/manual_review_transcripts/CPHO37-Q01_transcription_v1.md`，基于第37届合并PDF第1页渲染图完成第1题题面V1视觉转写，覆盖空气弹簧、主气室、附加气室、簧上负载、有效承载面积、阀门开闭、等温过程和绝热过程等题面条件；
- 新增 `03_corpus/manual_review_transcripts/CPHO37-Q01_formula_check_v1.csv`，依据PDF第6-7页登记作用力公式、过程方程、劲度系数通式、阀门关闭等温/绝热结果、阀门打开低频/高频结果和评分标准等关键公式核对入口；
- 新增第37届第1题共3张页面证据图：题面第1页、答案第6-7页；视觉检查确认第1题题面从试题PDF第1页中部开始，至第(2)问结束，第1页下部进入第2题；答案从PDF第6页页首开始，至第7页中部评分标准结束，第7页下半部进入第2题；
- 更新 `03_corpus/item_texts/CPHO37-Q01.md`，挂接V1转写稿、公式核对表和页面证据，明确原OCR文本仅作错误来源对照，不得用于正式编码证据；
- 更新 `03_corpus/manual_review_a1_batch_log.csv`、`manual_review_a1_render_index.csv` 和 `manual_review_a1_batch_summary.md`，登记A组队列第063-064项的证据、边界和下一步；
- 更新 `03_corpus/manual_review_checklist.csv` 和 `03_corpus/manual_review_priority_followup.csv`，将 `CPHO37-Q01-OCR` 推进为“V1视觉转写完成，待最终复核”，将 `CPHO37-Q01-FORMULA` 推进为“答案公式核对入口完成，待最终复核”；不填写校对人和校对日期，不关闭人工销项；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，记录第37届第1题已完成V1转写入口，并将下一最小任务调整为 `G1-07-A1-TRANSCRIBE-37Q02`；
- 本轮不改写论文正文，不修改原始PDF，不关闭第37届第1题题图问题，不生成正式编码结果、正式统计、正式案例结论、真实评分者记录或人工校对签名，也不提交Git。

## 2026-07-15：G1-07-A1-TRANSCRIBE-42Q07 第42届第7题V1转写

- 新增 `03_corpus/manual_review_transcripts/CPHO42-Q07_transcription_v1.md`，基于第42届试题PDF第5页渲染图完成第7题题面V1视觉转写，覆盖自聚焦光纤、柱坐标、折射率根号公式、边界条件、离轴最远距离和直角坐标轨迹等题面条件；
- 新增 `03_corpus/manual_review_transcripts/CPHO42-Q07_formula_check_v1.csv`，依据答案PDF第20-25页登记主解法微分方程、不变量、`rho_max`、`x(z)`、`y(z)`、解法二和评分标准等关键公式核对入口；
- 新增第42届第7题共7张页面证据图：题面第5页、答案第20-25页；视觉检查确认第7题题面从试题PDF第5页中部开始至页末结束，答案从第20页下部开始至第25页评分标准结束；
- 更新 `03_corpus/item_texts/CPHO42-Q07.md`，挂接V1转写稿、公式核对表和页面证据，明确原OCR文本仅作错误来源对照，不得用于正式编码证据；
- 更新 `03_corpus/manual_review_a1_batch_log.csv`、`manual_review_a1_render_index.csv` 和 `manual_review_a1_batch_summary.md`，登记A组队列第061-062项的证据、边界和下一步；
- 更新 `03_corpus/manual_review_checklist.csv` 和 `03_corpus/manual_review_priority_followup.csv`，将 `CPHO42-Q07-OCR` 推进为“V1视觉转写完成，待最终复核”，将 `CPHO42-Q07-FORMULA` 推进为“答案公式核对入口完成，待最终复核”；不填写校对人和校对日期，不关闭人工销项；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，记录第42届第7题已完成V1转写入口，并将下一最小任务调整为 `G1-07-A1-TRANSCRIBE-37Q01`；
- 本轮不改写论文正文，不修改原始PDF，不关闭第42届第7题图件问题，不生成正式编码结果、正式统计、正式案例结论、真实评分者记录或人工校对签名，也不提交Git。

## 2026-07-15：G1-07-A1-TRANSCRIBE-42Q04 第42届第4题V1转写

- 新增 `03_corpus/manual_review_transcripts/CPHO42-Q04_transcription_v1.md`，基于第42届试题PDF第3页渲染图完成第4题题面V1视觉转写，覆盖真空激光加速、单色平面电磁波、相对论电子动力学、最大能量、入射角和辐射阻尼能量损失等题面条件；
- 新增 `03_corpus/manual_review_transcripts/CPHO42-Q04_formula_check_v1.csv`，依据答案PDF第10-14页登记相对论运动方程、动量与能量、位置隐函数、最大能量与入射角、辐射阻尼能量损失、`-40%` 数值结果和评分标准等关键公式核对入口；
- 新增第42届第4题共6张页面证据图：题面第3页、答案第10-14页；视觉检查确认第4题题面从试题PDF第3页中部开始，第3页下半部结束，答案从第10页中部开始至第14页上半部评分标准结束；
- 更新 `03_corpus/item_texts/CPHO42-Q04.md`，挂接V1转写稿、公式核对表和页面证据，明确原OCR文本仅作错误来源对照，不得用于正式编码证据；
- 更新 `03_corpus/manual_review_a1_batch_log.csv`、`manual_review_a1_render_index.csv` 和 `manual_review_a1_batch_summary.md`，登记A组队列第059-060项的证据、边界和下一步；
- 更新 `03_corpus/manual_review_checklist.csv` 和 `03_corpus/manual_review_priority_followup.csv`，将 `CPHO42-Q04-OCR` 推进为“V1视觉转写完成，待最终复核”，将 `CPHO42-Q04-FORMULA` 推进为“答案公式核对入口完成，待最终复核”；不填写校对人和校对日期，不关闭人工销项；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，记录第42届第4题已完成V1转写入口，并将下一最小任务调整为 `G1-07-A1-TRANSCRIBE-42Q07`；
- 本轮不改写论文正文，不修改原始PDF，不生成正式编码结果、正式统计、正式案例结论、真实评分者记录或人工校对签名，也不提交Git。

## 2026-07-15：G1-07-A1-TRANSCRIBE-42Q03 第42届第3题V1转写

- 新增 `03_corpus/manual_review_transcripts/CPHO42-Q03_transcription_v1.md`，基于第42届试题PDF第2-3页渲染图完成第3题题面V1视觉转写，覆盖量子霍尔效应器件、端口接法、接触电阻、双器件连接和三重并联测量等题面条件；
- 新增 `03_corpus/manual_review_transcripts/CPHO42-Q03_formula_check_v1.csv`，依据答案PDF第7-10页和题解图放大页第26-27页登记霍尔电阻定义、断开/闭合开关推导、三重并联方程组、误差阶 `epsilon^2/epsilon^3`、评分标准和评分说明等关键公式核对入口；
- 新增第42届第3题共8张页面证据图：题面第2-3页、答案第7-10页、题解图放大页第26-27页；视觉检查确认第3题题面从试题PDF第2页下半部开始，第3页中上部结束，答案从第7页下半部开始至第10页中部评分标准和说明结束；
- 更新 `03_corpus/item_texts/CPHO42-Q03.md`，挂接V1转写稿、公式核对表和页面证据，明确原OCR文本仅作错误来源对照，不得用于正式编码证据；
- 更新 `03_corpus/manual_review_a1_batch_log.csv`、`manual_review_a1_render_index.csv` 和 `manual_review_a1_batch_summary.md`，登记A组队列第057-058项的证据、边界和下一步；
- 更新 `03_corpus/manual_review_checklist.csv` 和 `03_corpus/manual_review_priority_followup.csv`，将 `CPHO42-Q03-OCR` 推进为“V1视觉转写完成，待最终复核”，将 `CPHO42-Q03-FORMULA` 推进为“答案公式核对入口完成，待最终复核”；不填写校对人和校对日期，不关闭人工销项；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，记录第42届第3题已完成V1转写入口，并将下一最小任务调整为 `G1-07-A1-TRANSCRIBE-42Q04`；
- 本轮不改写论文正文，不修改原始PDF，不关闭第42届第3题题图或答案图件问题，不生成正式编码结果、正式统计、正式案例结论、真实评分者记录或人工校对签名，也不提交Git。

## 2026-07-15：G1-07-A1-TRANSCRIBE-42Q01 第42届第1题V1转写

- 新增 `03_corpus/manual_review_transcripts/CPHO42-Q01_transcription_v1.md`，基于第42届试题PDF第1页渲染图完成第1题题面V1视觉转写，覆盖磁光陷阱原子气、玻尔兹曼分布、`z = h` 平面测量、纵向数密度、原子流、极值时间和有效展宽等题面条件；
- 新增 `03_corpus/manual_review_transcripts/CPHO42-Q01_formula_check_v1.csv`，依据答案PDF第1-4页登记归一化分布函数、自由落体反推关系、`n(t)` 与 `I(t)` 闭式、强约束低温极限、`t_n/t_I` 替代解法、`sigma_t` 和评分标准等关键公式核对入口；
- 新增 `03_corpus/manual_review_renders/G1-07-A1/CPHO42-Q01-paper-page-1.png`、`CPHO42-Q01-solution-page-01.png`、`CPHO42-Q01-solution-page-02.png`、`CPHO42-Q01-solution-page-03.png` 和 `CPHO42-Q01-solution-page-04.png` 共5张页面证据图；视觉检查确认第1题完整位于试题PDF第1页上半部，第1页下半部进入第2题；第1题答案从答案PDF第1页开始，至第4页中部评分标准结束，第4页下半部进入第2题；
- 更新 `03_corpus/item_texts/CPHO42-Q01.md`，挂接V1转写稿、公式核对表和页面证据，明确原OCR文本仅作错误来源对照，不得用于正式编码证据；
- 更新 `03_corpus/manual_review_a1_batch_log.csv`、`manual_review_a1_render_index.csv` 和 `manual_review_a1_batch_summary.md`，登记A组队列第055-056项的证据、边界和下一步；
- 更新 `03_corpus/manual_review_checklist.csv` 和 `03_corpus/manual_review_priority_followup.csv`，将 `CPHO42-Q01-OCR` 推进为“V1视觉转写完成，待最终复核”，将 `CPHO42-Q01-FORMULA` 推进为“答案公式核对入口完成，待最终复核”；不填写校对人和校对日期，不关闭人工销项；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，记录第42届第1题已完成V1转写入口，并将下一最小任务调整为 `G1-07-A1-TRANSCRIBE-42Q03`；
- 本轮不改写论文正文，不修改原始PDF，不生成正式编码结果、正式统计、正式案例结论、真实评分者记录或人工校对签名，也不提交Git。

## 2026-07-15：G1-07-A1-TRANSCRIBE-40Q04 第40届第4题V1转写

- 新增 `03_corpus/manual_review_transcripts/CPHO40-Q04_transcription_v1.md`，基于第40届合并PDF第2-3页渲染图完成第4题题面V1视觉转写，覆盖编木拱桥、短杆、长杆、木材开槽、杆间静摩擦因数、地面静摩擦因数、几何量 `a/b/R` 和图4a至图4e等题面条件；
- 新增 `03_corpus/manual_review_transcripts/CPHO40-Q04_formula_check_v1.csv`，依据答案PDF第12-13页登记几何关系、C/D受力图、A/B/C/D杆力平衡、D杆力矩平衡、长分式求解、杆间摩擦因数 `mu`、地面摩擦因数 `mu'` 和评分参考等关键公式核对入口；
- 新增 `03_corpus/manual_review_renders/G1-07-A1/CPHO40-Q04-paper-page-2.png`、`CPHO40-Q04-paper-page-3.png`、`CPHO40-Q04-solution-page-12.png` 和 `CPHO40-Q04-solution-page-13.png` 共4张页面证据图；视觉检查确认第4题从试题PDF第2页下半部开始，延续至第3页上半部结束，第2页上半部为第2题尾部和第3题，第3页下半部进入第5题；第4题答案从PDF第12页页首开始，至第13页评分参考结束，第13页下半部进入第5题；
- 更新 `03_corpus/item_texts/CPHO40-Q04.md`，挂接V1转写稿、公式核对表和页面证据，明确原OCR文本仅作错误来源对照，不得用于正式编码证据；
- 更新 `03_corpus/manual_review_a1_batch_log.csv`、`manual_review_a1_render_index.csv` 和 `manual_review_a1_batch_summary.md`，登记A组队列第053-054项的证据、边界和下一步；
- 更新 `03_corpus/manual_review_checklist.csv` 和 `03_corpus/manual_review_priority_followup.csv`，将 `CPHO40-Q04-OCR` 推进为“V1视觉转写完成，待最终复核”，将 `CPHO40-Q04-FORMULA` 推进为“答案公式核对入口完成，待最终复核”；不填写校对人和校对日期，不关闭人工销项；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，记录第40届第4题已完成V1转写入口，并将下一最小任务调整为 `G1-07-A1-TRANSCRIBE-42Q01`；
- 本轮不改写论文正文，不修改原始PDF，不关闭第40届第4题题图问题，不生成正式编码结果、正式统计、正式案例结论、真实评分者记录或人工校对签名，也不提交Git。

## 2026-07-15：G1-07-A1-TRANSCRIBE-38Q08 第38届第8题V1转写

- 新增 `03_corpus/manual_review_transcripts/CPHO38-Q08_transcription_v1.md`，基于第38届合并PDF第3-4页渲染图完成第8题题面V1视觉转写，覆盖电动汽车简化模型、永磁直流电机、线圈参数、开路电压、内阻、变速比、加速时间、电池能量和能量转化效率等题面条件；
- 新增 `03_corpus/manual_review_transcripts/CPHO38-Q08_formula_check_v1.csv`，依据答案PDF第18-20页登记线圈力矩、反电动势、总电阻、力矩-转速关系、最大功率、最高车速、最大加速度、加速时间、电池能量、机械能增量和效率等关键公式核对入口；
- 新增 `03_corpus/manual_review_renders/G1-07-A1/CPHO38-Q08-paper-page-3.png`、`CPHO38-Q08-paper-page-4.png`、`CPHO38-Q08-solution-page-18.png`、`CPHO38-Q08-solution-page-19.png` 和 `CPHO38-Q08-solution-page-20.png` 共5张页面证据图；视觉检查确认第8题从试题PDF第3页底部开始，延续至第4页上半部结束，第3页上半部为第6题尾部和第7题；第8题答案从PDF第18页下半部开始，至第20页评分参考结束，第18页上半部为第7题尾部和评分参考；
- 更新 `03_corpus/item_texts/CPHO38-Q08.md`，挂接V1转写稿、公式核对表和页面证据，明确原OCR文本仅作错误来源对照，不得用于正式编码证据；
- 更新 `03_corpus/manual_review_a1_batch_log.csv`、`manual_review_a1_render_index.csv` 和 `manual_review_a1_batch_summary.md`，登记A组队列第051-052项的证据、边界和下一步；
- 更新 `03_corpus/manual_review_checklist.csv` 和 `03_corpus/manual_review_priority_followup.csv`，将 `CPHO38-Q08-OCR` 推进为“V1视觉转写完成，待最终复核”，将 `CPHO38-Q08-FORMULA` 推进为“答案公式核对入口完成，待最终复核”；不填写校对人和校对日期，不关闭人工销项；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，记录第38届第8题已完成V1转写入口，并将下一最小任务调整为 `G1-07-A1-TRANSCRIBE-40Q04`；
- 本轮不改写论文正文，不修改原始PDF，不关闭第38届第8题题图问题，不生成正式编码结果、正式统计、正式案例结论、真实评分者记录或人工校对签名，也不提交Git。

## 2026-07-15：G1-07-A1-TRANSCRIBE-38Q07 第38届第7题V1转写

- 新增 `03_corpus/manual_review_transcripts/CPHO38-Q07_transcription_v1.md`，基于第38届合并PDF第3页渲染图完成第7题题面V1视觉转写，覆盖汽车斜坡加速模型、前后轮、车身质心高度、滑动摩擦因数、转动惯量、发动机力矩、传动比和A型电动汽车参数等题面条件；
- 新增 `03_corpus/manual_review_transcripts/CPHO38-Q07_formula_check_v1.csv`，依据答案PDF第16-18页登记前后轮正压力、力矩平衡、安全加速度、滚动约束、后轮驱动力矩、传动比、水平/30度上坡加速度、后轮正压力/摩擦力和摩擦系数下限等关键公式核对入口；
- 新增 `03_corpus/manual_review_renders/G1-07-A1/CPHO38-Q07-paper-page-3.png`、`CPHO38-Q07-solution-page-16.png`、`CPHO38-Q07-solution-page-17.png` 和 `CPHO38-Q07-solution-page-18.png` 共4张页面证据图；视觉检查确认第7题完整位于试题PDF第3页中部，第3页上部为第6题尾部且下部进入第8题；第7题答案从PDF第16页下半部开始，至第18页上半部评分参考结束，第18页下半部进入第8题；
- 更新 `03_corpus/item_texts/CPHO38-Q07.md`，挂接V1转写稿、公式核对表和页面证据，明确原OCR文本仅作错误来源对照，不得用于正式编码证据；
- 更新 `03_corpus/manual_review_a1_batch_log.csv`、`manual_review_a1_render_index.csv` 和 `manual_review_a1_batch_summary.md`，登记A组队列第049-050项的证据、边界和下一步；
- 更新 `03_corpus/manual_review_checklist.csv` 和 `03_corpus/manual_review_priority_followup.csv`，将 `CPHO38-Q07-OCR` 推进为“V1视觉转写完成，待最终复核”，将 `CPHO38-Q07-FORMULA` 推进为“答案公式核对入口完成，待最终复核”；同时将答案页范围由 `16-17` 纠偏为 `16-18`；不填写校对人和校对日期，不关闭人工销项；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，记录第38届第7题已完成V1转写入口，并将下一最小任务调整为 `G1-07-A1-TRANSCRIBE-38Q08`；
- 本轮不改写论文正文，不修改原始PDF，不关闭第38届第7题题图问题，不生成正式编码结果、正式统计、正式案例结论、真实评分者记录或人工校对签名，也不提交Git。

## 2026-07-15：G1-07-A1-TRANSCRIBE-38Q04 第38届第4题V1转写

- 新增 `03_corpus/manual_review_transcripts/CPHO38-Q04_transcription_v1.md`，基于第38届合并PDF第2页渲染图完成第4题题面V1视觉转写，覆盖永磁针电流环模型、磁矩 `mu=IS`、`S=pi R^2`、坐标系、稳定平衡和受力平衡条件等题面信息；
- 新增 `03_corpus/manual_review_transcripts/CPHO38-Q04_formula_check_v1.csv`，依据答案PDF第10-12页登记毕奥-萨伐尔积分、远场近似、磁场方向、相互作用势能、力矩平衡、稳定平衡角、受力平衡位置和评分参考等关键公式核对入口；
- 新增 `03_corpus/manual_review_renders/G1-07-A1/CPHO38-Q04-paper-page-2.png`、`CPHO38-Q04-solution-page-10.png`、`CPHO38-Q04-solution-page-11.png` 和 `CPHO38-Q04-solution-page-12.png` 共4张页面证据图；视觉检查确认第4题完整位于试题PDF第2页上半部，第2页中部进入第5题；第4题答案从PDF第10页下半部开始，至第12页上半部评分参考结束，第12页下半部进入第5题；
- 更新 `03_corpus/item_texts/CPHO38-Q04.md`，挂接V1转写稿、公式核对表和页面证据，明确原OCR文本仅作错误来源对照，不得用于正式编码证据；
- 更新 `03_corpus/manual_review_a1_batch_log.csv`、`manual_review_a1_render_index.csv` 和 `manual_review_a1_batch_summary.md`，登记A组队列第047-048项的证据、边界和下一步；
- 更新 `03_corpus/manual_review_checklist.csv` 和 `03_corpus/manual_review_priority_followup.csv`，将 `CPHO38-Q04-OCR` 推进为“V1视觉转写完成，待最终复核”，将 `CPHO38-Q04-FORMULA` 推进为“答案公式核对入口完成，待最终复核”；同时将答案页范围由 `10-11` 纠偏为 `10-12`；不填写校对人和校对日期，不关闭人工销项；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，记录第38届第4题已完成V1转写入口，并将下一最小任务调整为 `G1-07-A1-TRANSCRIBE-38Q07`；
- 本轮不改写论文正文，不修改原始PDF，不关闭第38届第4题题图问题，不生成正式编码结果、正式统计、正式案例结论、真实评分者记录或人工校对签名，也不提交Git。

## 2026-07-15：G1-07-A1-TRANSCRIBE-38Q03 第38届第3题V1转写

- 新增 `03_corpus/manual_review_transcripts/CPHO38-Q03_transcription_v1.md`，基于第38届合并PDF第1页渲染图完成第3题题面V1视觉转写，覆盖均质超球、上下平行硬板、右手螺旋坐标系、三次碰撞、`v_0x`、`omega_0z` 和 `J=2mr^2/5` 等题面条件；
- 新增 `03_corpus/manual_review_transcripts/CPHO38-Q03_formula_check_v1.csv`，依据答案PDF第8-10页登记动量定理、角动量定理、无滑动条件、力矩反号、第1/2/3次碰撞后的速度和角速度结果及评分参考等关键公式核对入口；
- 新增 `03_corpus/manual_review_renders/G1-07-A1/CPHO38-Q03-paper-page-1.png`、`CPHO38-Q03-solution-page-08.png`、`CPHO38-Q03-solution-page-09.png` 和 `CPHO38-Q03-solution-page-10.png` 共4张页面证据图；视觉检查确认第3题完整位于试题PDF第1页底部，第1页上半部为第1题且中部为第2题；第3题答案从PDF第8页底部开始，至第10页上半部评分参考结束，第10页下半部进入第4题；
- 更新 `03_corpus/item_texts/CPHO38-Q03.md`，挂接V1转写稿、公式核对表和页面证据，明确原OCR文本仅作错误来源对照，不得用于正式编码证据；
- 更新 `03_corpus/manual_review_a1_batch_log.csv`、`manual_review_a1_render_index.csv` 和 `manual_review_a1_batch_summary.md`，登记A组队列第045-046项的证据、边界和下一步；
- 更新 `03_corpus/manual_review_checklist.csv` 和 `03_corpus/manual_review_priority_followup.csv`，将 `CPHO38-Q03-OCR` 推进为“V1视觉转写完成，待最终复核”，将 `CPHO38-Q03-FORMULA` 推进为“答案公式核对入口完成，待最终复核”；同时将答案页范围由 `8-9` 纠偏为 `8-10`；不填写校对人和校对日期，不关闭人工销项；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，记录第38届第3题已完成V1转写入口，并将下一最小任务调整为 `G1-07-A1-TRANSCRIBE-38Q04`；
- 本轮不改写论文正文，不修改原始PDF，不关闭第38届第3题题图问题，不生成正式编码结果、正式统计、正式案例结论、真实评分者记录或人工校对签名，也不提交Git。

## 2026-07-15：G1-07-A1-TRANSCRIBE-38Q01 第38届第1题V1转写

- 新增 `03_corpus/manual_review_transcripts/CPHO38-Q01_transcription_v1.md`，基于第38届合并PDF第1页渲染图完成第1题题面V1视觉转写，覆盖平凸透镜、平凹透镜、折射率 `n/n'`、`r_0/r_0'`、`theta_max` 和光束横截面半径比等题面条件；
- 新增 `03_corpus/manual_review_transcripts/CPHO38-Q01_formula_check_v1.csv`，依据答案PDF第5-7页登记等光程关系、极坐标方程、双曲线标准形式、撇号变量、光束半径比 `k` 和评分参考等关键公式核对入口；
- 新增 `03_corpus/manual_review_renders/G1-07-A1/CPHO38-Q01-paper-page-1.png`、`CPHO38-Q01-solution-page-05.png`、`CPHO38-Q01-solution-page-06.png` 和 `CPHO38-Q01-solution-page-07.png` 共4张页面证据图；视觉检查确认第1题位于试题PDF第1页上半部，第1页中下部进入第2题且底部进入第3题；第1题答案从PDF第5页页首开始，至第7页上半部评分参考结束，第7页中下部进入第2题；
- 更新 `03_corpus/item_texts/CPHO38-Q01.md`，挂接V1转写稿、公式核对表和页面证据，明确原OCR文本仅作错误来源对照，不得用于正式编码证据；
- 更新 `03_corpus/manual_review_a1_batch_log.csv`、`manual_review_a1_render_index.csv` 和 `manual_review_a1_batch_summary.md`，登记A组队列第043-044项的证据、边界和下一步；
- 更新 `03_corpus/manual_review_checklist.csv` 和 `03_corpus/manual_review_priority_followup.csv`，将 `CPHO38-Q01-OCR` 推进为“V1视觉转写完成，待最终复核”，将 `CPHO38-Q01-FORMULA` 推进为“答案公式核对入口完成，待最终复核”；同时将答案页范围由 `5-6` 纠偏为 `5-7`；不填写校对人和校对日期，不关闭人工销项；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，记录第38届第1题已完成V1转写入口，并将下一最小任务调整为 `G1-07-A1-TRANSCRIBE-38Q03`；
- 本轮不改写论文正文，不修改原始PDF，不关闭第38届第1题题图问题，不生成正式编码结果、正式统计、正式案例结论、真实评分者记录或人工校对签名，也不提交Git。

## 2026-07-15：G1-07-A1-TRANSCRIBE-37Q07 第37届第7题V1转写

- 新增 `03_corpus/manual_review_transcripts/CPHO37-Q07_transcription_v1.md`，基于第37届合并PDF第4页渲染图完成第7题题面V1视觉转写，覆盖LIGO探测双黑洞并合引力波、旋近/并合/衰荡阶段、牛顿近似、辐射功率量纲分析、两黑洞初始距离和半距转角等题面条件；
- 新增 `03_corpus/manual_review_transcripts/CPHO37-Q07_formula_check_v1.csv`，依据答案PDF第18-19页登记量纲分析、辐射功率 `P = alpha G I^2 omega^6/c^5`、圆周运动条件、系统能量、转动惯量、角速度微分方程、旋转一圈时间和半距转角等关键公式核对入口；
- 新增 `03_corpus/manual_review_renders/G1-07-A1/CPHO37-Q07-paper-page-4.png`、`CPHO37-Q07-solution-page-18.png` 和 `CPHO37-Q07-solution-page-19.png` 共3张页面证据图；视觉检查确认第7题完整位于PDF第4页中部，第4页顶部为第6题尾部且第4页下部进入第8题；第7题答案从PDF第18页页首开始，至第19页上半部评分标准结束，第19页下半部进入第8题；
- 更新 `03_corpus/item_texts/CPHO37-Q07.md`，挂接V1转写稿、公式核对表和页面证据，明确原OCR文本仅作错误来源对照，不得用于正式编码证据；
- 更新 `03_corpus/manual_review_a1_batch_log.csv`、`manual_review_a1_render_index.csv` 和 `manual_review_a1_batch_summary.md`，登记A组队列第041-042项的证据、边界和下一步；
- 更新 `03_corpus/manual_review_checklist.csv` 和 `03_corpus/manual_review_priority_followup.csv`，将 `CPHO37-Q07-OCR` 推进为“V1视觉转写完成，待最终复核”，将 `CPHO37-Q07-FORMULA` 推进为“答案公式核对入口完成，待最终复核”；不填写校对人和校对日期，不关闭人工销项；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，记录第37届第7题已完成V1转写入口，并将下一最小任务调整为 `G1-07-A1-TRANSCRIBE-38Q01`；
- 本轮不改写论文正文，不修改原始PDF，不关闭第37届第7题题图问题，不生成正式编码结果、正式统计、正式案例结论、真实评分者记录或人工校对签名，也不提交Git。

## 2026-07-15：G1-07-A1-TRANSCRIBE-37Q06 第37届第6题V1转写

- 新增 `03_corpus/manual_review_transcripts/CPHO37-Q06_transcription_v1.md`，基于第37届合并PDF第3-4页渲染图完成第6题题面V1视觉转写，覆盖光纤陀螺仪、Sagnac效应、分束器、逆时针/顺时针传播、光纤全反射、密绕 `N` 匝光纤、相位差和谐振式光学陀螺系统等题面条件；
- 新增 `03_corpus/manual_review_transcripts/CPHO37-Q06_formula_check_v1.csv`，依据答案PDF第16-17页登记折射定律、全反射临界条件、传播时间、相位差、折射率无关结论、共振条件、路径长度和 `Omega` 与 `Delta f` 关系等关键公式核对入口；
- 新增 `03_corpus/manual_review_renders/G1-07-A1/CPHO37-Q06-paper-page-3.png`、`CPHO37-Q06-paper-page-4.png` 和 `CPHO37-Q06-solution-page-16.png` 至 `CPHO37-Q06-solution-page-18.png` 共5张页面证据图；视觉检查确认第6题题面从PDF第3页下半部开始，延续至第4页顶部结束，第3页上半部为第5题且第4页中部为第7题、下部进入第8题；第6题答案从PDF第16页页首开始，至第17页评分标准结束，第18页为第7题答案后边界；
- 更新 `03_corpus/item_texts/CPHO37-Q06.md`，挂接V1转写稿、公式核对表和页面证据，明确原OCR文本仅作错误来源对照，不得用于正式编码证据；
- 更新 `03_corpus/manual_review_a1_batch_log.csv`、`manual_review_a1_render_index.csv` 和 `manual_review_a1_batch_summary.md`，登记A组队列第039-040项的证据、边界和下一步；
- 更新 `03_corpus/manual_review_checklist.csv` 和 `03_corpus/manual_review_priority_followup.csv`，将 `CPHO37-Q06-OCR` 推进为“V1视觉转写完成，待最终复核”，将 `CPHO37-Q06-FORMULA` 推进为“答案公式核对入口完成，待最终复核”；不填写校对人和校对日期，不关闭人工销项；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，记录第37届第6题已完成V1转写入口，并将下一最小任务调整为 `G1-07-A1-TRANSCRIBE-37Q07`；
- 本轮不改写论文正文，不修改原始PDF，不关闭第37届第6题题图问题，不生成正式编码结果、正式统计、正式案例结论、真实评分者记录或人工校对签名，也不提交Git。

## 2026-07-15：G1-07-A1-TRANSCRIBE-41Q06 第41届第6题V1转写

- 新增 `03_corpus/manual_review_transcripts/CPHO41-Q06_transcription_v1.md`，基于第41届试题PDF第3-4页渲染图完成第6题题面V1视觉转写，覆盖广义相对论预言、埃丁顿日全食观测、圆锥曲线轨道、半通径与偏心率、陨石/星光偏折、费马原理、弱场相对折射率和光线轨迹方程等题面条件；
- 新增 `03_corpus/manual_review_transcripts/CPHO41-Q06_formula_check_v1.csv`，依据答案PDF第13-16页登记轨道方程条件、系统能量、角动量、`p/e` 与 `E/L` 关系、牛顿偏折角、星光牛顿偏折角、弱场折射率方程、等效轨道参数和广义相对论偏折角 `4GM_sun/(c^2 R_sun)` 等关键公式核对入口；
- 新增 `03_corpus/manual_review_renders/G1-07-A1/CPHO41-Q06-paper-page-3.png`、`CPHO41-Q06-paper-page-4.png` 和 `CPHO41-Q06-solution-page-13.png` 至 `CPHO41-Q06-solution-page-17.png` 共7张页面证据图；视觉检查确认第6题题面从试题PDF第3页底部开始，延续至第4页中部结束，第3页上部为第5题且第4页下半部进入第7题；第6题答案从答案PDF第13页下部开始，至第16页评分标准结束，第16页下部和第17页进入第7题；
- 更新 `03_corpus/item_texts/CPHO41-Q06.md`，挂接V1转写稿、公式核对表和页面证据，明确原OCR文本仅作错误来源对照，不得用于正式编码证据；
- 更新 `03_corpus/manual_review_a1_batch_log.csv`、`manual_review_a1_render_index.csv` 和 `manual_review_a1_batch_summary.md`，登记A组队列第037-038项的证据、边界和下一步；
- 更新 `03_corpus/manual_review_checklist.csv` 和 `03_corpus/manual_review_priority_followup.csv`，将 `CPHO41-Q06-OCR` 推进为“V1视觉转写完成，待最终复核”，将 `CPHO41-Q06-FORMULA` 推进为“答案公式核对入口完成，待最终复核”；不填写校对人和校对日期，不关闭人工销项；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，记录第41届第6题已完成V1转写入口，并将下一最小任务调整为 `G1-07-A1-TRANSCRIBE-37Q06`；
- 本轮不改写论文正文，不修改原始PDF，不关闭第41届第6题题图问题，不生成正式编码结果、正式统计、正式案例结论、真实评分者记录或人工校对签名，也不提交Git。

## 2026-07-15：G1-07-A1-TRANSCRIBE-41Q05 第41届第5题V1转写

- 新增 `03_corpus/manual_review_transcripts/CPHO41-Q05_transcription_v1.md`，基于第41届试题PDF第3页渲染图完成第5题题面V1视觉转写，覆盖诺贝尔奖背景、Ioffe势阱、四根无限长直导线、坐标系、`P(x,y,0)`、磁矩势能、磁场力和蒸发冷却圆柱区域等题面条件；
- 新增 `03_corpus/manual_review_transcripts/CPHO41-Q05_formula_check_v1.csv`，依据答案PDF第11-13页登记无限长直导线磁场、`B_x/B_y` 长式、小量近似、`W_m=-S·B` 证明、磁场力分量、约束势能、`N_1/E_1/bar(E)_1` 和冷却后 `N_2/E_2/bar(E)_2` 等关键公式核对入口；
- 新增 `03_corpus/manual_review_renders/G1-07-A1/CPHO41-Q05-paper-page-3.png`、`CPHO41-Q05-paper-page-4.png` 和 `CPHO41-Q05-solution-page-11.png` 至 `CPHO41-Q05-solution-page-14.png` 共6张页面证据图；视觉检查确认第5题题面完整位于试题PDF第3页中部至下部，第3页上部为第4题尾部且下部进入第6题；第5题答案从答案PDF第11页下部开始，至第13页评分标准结束，第13页下部和第14页进入第6题；
- 更新 `03_corpus/item_texts/CPHO41-Q05.md`，挂接V1转写稿、公式核对表和页面证据，明确原OCR文本仅作错误来源对照，不得用于正式编码证据；
- 更新 `03_corpus/manual_review_a1_batch_log.csv`、`manual_review_a1_render_index.csv` 和 `manual_review_a1_batch_summary.md`，登记A组队列第035-036项的证据、边界和下一步；
- 更新 `03_corpus/manual_review_checklist.csv` 和 `03_corpus/manual_review_priority_followup.csv`，将 `CPHO41-Q05-OCR` 推进为“V1视觉转写完成，待最终复核”，将 `CPHO41-Q05-FORMULA` 推进为“答案公式核对入口完成，待最终复核”；不填写校对人和校对日期，不关闭人工销项；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，记录第41届第5题已完成V1转写入口，并将下一最小任务调整为 `G1-07-A1-TRANSCRIBE-41Q06`；
- 本轮不改写论文正文，不修改原始PDF，不关闭第41届第5题题图问题，不生成正式编码结果、正式统计、正式案例结论、真实评分者记录或人工校对签名，也不提交Git。

## 2026-07-15：G1-07-A1-TRANSCRIBE-41Q01 第41届第1题V1转写

- 新增 `03_corpus/manual_review_transcripts/CPHO41-Q01_transcription_v1.md`，基于第41届试题PDF第1页渲染图完成第1题题面V1视觉转写，覆盖高层建筑风致晃动、调谐质量阻尼器、摆锤质量 `m`、摆臂长度 `l`、谐振子质量 `M`、劲度系数 `k`、强迫力 `F(t)=H cos(omega t)`、`sqrt(0.99)` 倍频率和阻尼力 `f=-gamma v'` 等题面条件；
- 新增 `03_corpus/manual_review_transcripts/CPHO41-Q01_formula_check_v1.csv`，依据答案PDF第1-3页登记耦合运动方程、稳定振幅、`omega_0=sqrt(g/l)`、无阻尼共振频率、阻尼器条件 `l=Mg/k`、第(2)问质量比 `101/9900`、相对速度分量和带阻尼非线性方程等关键公式核对入口；
- 新增 `03_corpus/manual_review_renders/G1-07-A1/CPHO41-Q01-paper-page-1.png`、`CPHO41-Q01-paper-page-2.png` 和 `CPHO41-Q01-solution-page-01.png` 至 `CPHO41-Q01-solution-page-04.png` 共6张页面证据图；视觉检查确认第1题题面位于试题PDF第1页中部至下半部，第1页更下部进入第2题，第2页为边界页；第1题答案从答案PDF第1页开始，至第3页上半部评分标准结束，第3页下半部和第4页进入第2题；
- 更新 `03_corpus/item_texts/CPHO41-Q01.md`，挂接V1转写稿、公式核对表和页面证据，明确原OCR文本仅作错误来源对照，不得用于正式编码证据；
- 更新 `03_corpus/manual_review_a1_batch_log.csv`、`manual_review_a1_render_index.csv` 和 `manual_review_a1_batch_summary.md`，登记A组队列第033-034项的证据、边界和下一步；
- 更新 `03_corpus/manual_review_checklist.csv` 和 `03_corpus/manual_review_priority_followup.csv`，将 `CPHO41-Q01-OCR` 推进为“V1视觉转写完成，待最终复核”，将 `CPHO41-Q01-FORMULA` 推进为“答案公式核对入口完成，待最终复核”；同时恢复优先队列表为154行并保持第035-036项为第41届第5题；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，记录第41届第1题已完成V1转写入口，并将下一最小任务调整为 `G1-07-A1-TRANSCRIBE-41Q05`；
- 本轮不改写论文正文，不修改原始PDF，不关闭第41届第1题题图问题，不生成正式编码结果、正式统计、正式案例结论、真实评分者记录或人工校对签名，也不提交Git。

## 2026-07-15：G1-07-A1-TRANSCRIBE-40Q07 第40届第7题V1转写

- 新增 `03_corpus/manual_review_transcripts/CPHO40-Q07_transcription_v1.md`，基于第40届试题/答案合并PDF第4-5页渲染图完成第7题题面V1视觉转写，覆盖对流层、同温层、逆温层、绝热上升、摩尔质量 `mu`、`gamma`、密度 `rho`、声速、声波折射/全反射、声源和探测气球四种空间组合等题面条件；
- 新增 `03_corpus/manual_review_transcripts/CPHO40-Q07_formula_check_v1.csv`，依据答案PDF第19-21页登记气体密度、静力平衡、绝热温度梯度、声速、同温层内外声速比、折射关系、临界角、`l_1/l_2` 几何估算和A/B/C/D四种远距离传播结论等关键公式核对入口；
- 新增 `03_corpus/manual_review_renders/G1-07-A1/CPHO40-Q07-paper-page-4.png`、`CPHO40-Q07-paper-page-5.png` 和 `CPHO40-Q07-solution-page-19.png` 至 `CPHO40-Q07-solution-page-22.png` 共6张页面证据图；视觉检查确认第7题题面从试题PDF第4页底部“七、”开始，延续至第5页顶部第(4)问结束，第4页上部为第6题、第5页中部进入第8题；第7题答案从PDF第19页下半部“七、”开始，至第21页中部评分标准结束，第21页下部和第22页进入第8题；
- 更新 `03_corpus/item_texts/CPHO40-Q07.md`，挂接V1转写稿、公式核对表和页面证据，明确原OCR文本仅作错误来源对照，不得用于正式编码证据；
- 更新 `03_corpus/manual_review_a1_batch_log.csv`、`manual_review_a1_render_index.csv` 和 `manual_review_a1_batch_summary.md`，登记A组队列第031-032项的证据、边界和下一步；
- 更新 `03_corpus/manual_review_checklist.csv` 和 `03_corpus/manual_review_priority_followup.csv`，将 `CPHO40-Q07-OCR` 推进为“V1视觉转写完成，待最终复核”，将 `CPHO40-Q07-FORMULA` 推进为“答案公式核对入口完成，待最终复核”；不填写校对人和校对日期，不关闭人工销项；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，记录第40届第7题已完成V1转写入口，并将下一最小任务调整为 `G1-07-A1-TRANSCRIBE-41Q01`；
- 本轮不改写论文正文，不修改原始PDF，不关闭第40届第7题题图问题，不生成正式编码结果、正式统计、正式案例结论、真实评分者记录或人工校对签名，也不提交Git。

## 2026-07-15：G1-07-A1-TRANSCRIBE-40Q06 第40届第6题V1转写

- 新增 `03_corpus/manual_review_transcripts/CPHO40-Q06_transcription_v1.md`，基于第40届试题/答案合并PDF第4页渲染图完成第6题题面V1视觉转写，覆盖涡电流、线圈半径 `b`、交变电流 `I(t)=I_0 cos(omega t)`、导体球半径 `a`、电导率 `sigma`、球心高度 `h`、趋肤深度 `delta`、真空磁导率 `mu_0`、理想导体球、磁偶极矩和面电流密度等题面条件；
- 新增 `03_corpus/manual_review_transcripts/CPHO40-Q06_formula_check_v1.csv`，依据答案PDF第16-19页登记球外总磁场、法向连续条件、磁偶极矩、面电流密度、线圈轴线磁场、磁偶极受力、平均安培力、悬浮电流 `I_0`、趋肤层体电流、焦耳热功率和平均热功率等关键公式核对入口；
- 新增 `03_corpus/manual_review_renders/G1-07-A1/CPHO40-Q06-paper-page-4.png` 和 `CPHO40-Q06-solution-page-16.png` 至 `CPHO40-Q06-solution-page-20.png` 共6张页面证据图；视觉检查确认第6题题面位于试题PDF第4页中部，第4页上部为第5题尾部、下部进入第7题；第6题答案从PDF第16页下部“六、”开始，至第19页上部评分标准结束，第19页下半部和第20页进入第7题；
- 更新 `03_corpus/item_texts/CPHO40-Q06.md`，挂接V1转写稿、公式核对表和页面证据，明确原OCR文本仅作错误来源对照，不得用于正式编码证据；
- 更新 `03_corpus/manual_review_a1_batch_log.csv`、`manual_review_a1_render_index.csv` 和 `manual_review_a1_batch_summary.md`，登记A组队列第029-030项的证据、边界和下一步；
- 更新 `03_corpus/manual_review_checklist.csv` 和 `03_corpus/manual_review_priority_followup.csv`，将 `CPHO40-Q06-OCR` 推进为“V1视觉转写完成，待最终复核”，将 `CPHO40-Q06-FORMULA` 推进为“答案公式核对入口完成，待最终复核”；不填写校对人和校对日期，不关闭人工销项；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，记录第40届第6题已完成V1转写入口，并将下一最小任务调整为 `G1-07-A1-TRANSCRIBE-40Q07`；
- 本轮不改写论文正文，不修改原始PDF，不关闭第40届第6题题图问题，不生成正式编码结果、正式统计、正式案例结论、真实评分者记录或人工校对签名，也不提交Git。

## 2026-07-15：G1-07-A1-TRANSCRIBE-40Q01 第40届第1题V1转写

- 新增 `03_corpus/manual_review_transcripts/CPHO40-Q01_transcription_v1.md`，基于第40届试题/答案合并PDF第1页渲染图完成第1题题面V1视觉转写，覆盖手机相机镜头、共轴理想透镜组、主点 `H/H'`、物距 `u`、刻度尺长度 `l`、像长 `l_1/l_2`、焦距 `f_1/f_2`、光心 `O_1/O_2`、主平面和物方/像方焦距等题面条件；
- 新增 `03_corpus/manual_review_transcripts/CPHO40-Q01_formula_check_v1.csv`，依据答案PDF第6-7页登记薄透镜成像公式、横向放大率、等效焦距 `F`、物距 `u_1`、两透镜成像公式、透镜组放大率、主点位置、像方焦点位置和物方/像方焦距等关键公式核对入口；
- 新增 `03_corpus/manual_review_renders/G1-07-A1/CPHO40-Q01-paper-page-1.png` 和 `CPHO40-Q01-solution-page-06.png` 至 `CPHO40-Q01-solution-page-08.png` 共4张页面证据图；视觉检查确认第1题题面从试题PDF第1页中部“一、”开始，至同页中下部第(2)(ii)结束，第1页下部进入第2题；第1题答案从PDF第6页页首“一、”开始，至第7页中部评分参考结束，第7页下部和第8页进入第2题；
- 更新 `03_corpus/item_texts/CPHO40-Q01.md`，挂接V1转写稿、公式核对表和页面证据，明确原OCR文本仅作错误来源对照，不得用于正式编码证据；
- 更新 `03_corpus/manual_review_a1_batch_log.csv`、`manual_review_a1_render_index.csv` 和 `manual_review_a1_batch_summary.md`，登记A组队列第027-028项的证据、边界和下一步；
- 更新 `03_corpus/manual_review_checklist.csv` 和 `03_corpus/manual_review_priority_followup.csv`，将 `CPHO40-Q01-OCR` 推进为“V1视觉转写完成，待最终复核”，将 `CPHO40-Q01-FORMULA` 推进为“答案公式核对入口完成，待最终复核”；不填写校对人和校对日期，不关闭人工销项；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，记录第40届第1题已完成V1转写入口，并将下一最小任务调整为 `G1-07-A1-TRANSCRIBE-40Q06`；
- 本轮不改写论文正文，不修改原始PDF，不关闭第40届第1题题图问题，不生成正式编码结果、正式统计、正式案例结论、真实评分者记录或人工校对签名，也不提交Git。

## 2026-07-15：G1-07-A1-TRANSCRIBE-38Q06 第38届第6题V1转写

- 新增 `03_corpus/manual_review_transcripts/CPHO38-Q06_transcription_v1.md`，基于第38届试题/答案合并PDF第3页渲染图完成第6题题面V1视觉转写，覆盖同轴带电薄壁圆筒、半径 `r_1/r_2`、单位长度质量 `m`、单位长度电荷 `q/-q`、电容率 `epsilon_0`、磁导率 `mu_0`、点电荷质量 `mu`、电荷量 `Q`、外力矩总冲量矩 `J` 和总机械角动量 `L` 等题面条件；
- 新增 `03_corpus/manual_review_transcripts/CPHO38-Q06_formula_check_v1.csv`，依据答案PDF第14-16页登记电场分布、等效电流、磁场分布、点电荷角动量与动能、到达外筒条件、感应电场、内外圆筒角速度关系、外力矩总冲量矩和总机械角动量等关键公式核对入口；
- 新增 `03_corpus/manual_review_renders/G1-07-A1/CPHO38-Q06-paper-page-3.png` 和 `CPHO38-Q06-solution-page-14.png` 至 `CPHO38-Q06-solution-page-17.png` 共5张页面证据图；视觉检查确认第6题题面从试题PDF第3页页首开始并在同页上半部结束，第3页下半部进入第7题和第8题；第6题答案从PDF第14页下半部“六、”开始，至第16页上半部评分参考结束，第14页上半部为第5题答案尾部和评分参考，第16页下半部和第17页进入第7题；
- 更新 `03_corpus/item_texts/CPHO38-Q06.md`，挂接V1转写稿、公式核对表和页面证据，明确原OCR文本仅作错误来源对照，不得用于正式编码证据；
- 更新 `03_corpus/manual_review_a1_batch_log.csv`、`manual_review_a1_render_index.csv` 和 `manual_review_a1_batch_summary.md`，登记A组队列第025-026项的证据、边界和下一步；
- 更新 `03_corpus/manual_review_checklist.csv` 和 `03_corpus/manual_review_priority_followup.csv`，将 `CPHO38-Q06-OCR` 推进为“V1视觉转写完成，待最终复核”，将 `CPHO38-Q06-FORMULA` 推进为“答案公式核对入口完成，待最终复核”；同时将第38届第6题相关答案页范围由 `14-15` 纠偏为 `14-16`；不填写校对人和校对日期，不关闭人工销项；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，记录第38届第6题已完成V1转写入口，并将下一最小任务调整为 `G1-07-A1-TRANSCRIBE-40Q01`；
- 本轮不改写论文正文，不修改原始PDF，不关闭第38届第6题题图问题，不生成正式编码结果、正式统计、正式案例结论、真实评分者记录或人工校对签名，也不提交Git。

## 2026-07-15：G1-07-A1-TRANSCRIBE-38Q05 第38届第5题V1转写

- 新增 `03_corpus/manual_review_transcripts/CPHO38-Q05_transcription_v1.md`，基于第38届试题/答案合并PDF第2页渲染图完成第5题题面V1视觉转写，覆盖原子激光制冷、塞曼减速装置、多普勒效应、塞曼效应、散射速率 `Gamma`、塞曼系数 `beta`、磁感应强度函数 `B(z)` 和题给常量等题面条件；
- 新增 `03_corpus/manual_review_transcripts/CPHO38-Q05_formula_check_v1.csv`，依据答案PDF第12-14页登记能量均分、`40K` 原子质量、方均根速率、光子动量、减速加速度、减速距离、多普勒频移、塞曼补偿磁场函数 `B(z)`、数值式和取值范围等关键公式核对入口；
- 新增 `03_corpus/manual_review_renders/G1-07-A1/CPHO38-Q05-paper-page-2.png` 和 `CPHO38-Q05-solution-page-11.png` 至 `CPHO38-Q05-solution-page-14.png` 共5张页面证据图；视觉检查确认第5题题面从试题PDF第2页中部开始并在本页结束，第2页上半部为第4题尾部；第5题答案从PDF第12页下半部“五、”开始，至第14页上半部评分参考结束，第12页上半部为第4题尾部和评分参考，第14页下半部进入第6题；
- 更新 `03_corpus/item_texts/CPHO38-Q05.md`，挂接V1转写稿、公式核对表和页面证据，明确原OCR文本仅作错误来源对照，不得用于正式编码证据；
- 更新 `03_corpus/manual_review_a1_batch_log.csv`、`manual_review_a1_render_index.csv` 和 `manual_review_a1_batch_summary.md`，登记A组队列第023-024项的证据、边界和下一步；
- 更新 `03_corpus/manual_review_checklist.csv` 和 `03_corpus/manual_review_priority_followup.csv`，将 `CPHO38-Q05-OCR` 推进为“V1视觉转写完成，待最终复核”，将 `CPHO38-Q05-FORMULA` 推进为“答案公式核对入口完成，待最终复核”；同时将第38届第5题相关答案页范围由 `12-13` 纠偏为 `12-14`；不填写校对人和校对日期，不关闭人工销项；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，记录第38届第5题已完成V1转写入口，并将下一最小任务调整为 `G1-07-A1-TRANSCRIBE-38Q06`；
- 本轮不改写论文正文，不修改原始PDF，不关闭第38届第5题题图问题，不生成正式编码结果、正式统计、正式案例结论、真实评分者记录或人工校对签名，也不提交Git。

## 2026-07-15：G1-07-A1-TRANSCRIBE-37Q08 第37届第8题V1转写

- 新增 `03_corpus/manual_review_transcripts/CPHO37-Q08_transcription_v1.md`，基于第37届试题/答案合并PDF第4-5页渲染图完成第8题题面V1视觉转写，覆盖电光调制、铌酸锂电光晶体、起偏器 `P_1`、检偏器 `P_2`、坐标轴 `x_1/x_2/x_3`、快慢轴 `x_1'/x_2'`、半波电压 `V_pi`、`1/4` 波片、等效电路、低效率条件和并联谐振补偿等题面条件；
- 新增 `03_corpus/manual_review_transcripts/CPHO37-Q08_formula_check_v1.csv`，依据答案PDF第19-21页登记折射率变化、相位差、半波电压、未加/加 `1/4` 波片的光强透过率、复阻抗、低效率条件、并联谐振和 `|V_c| approx |V|` 等关键公式核对入口；
- 新增 `03_corpus/manual_review_renders/G1-07-A1/CPHO37-Q08-paper-page-4.png`、`CPHO37-Q08-paper-page-5.png` 和 `CPHO37-Q08-solution-page-19.png` 至 `CPHO37-Q08-solution-page-21.png` 共5张页面证据图；视觉检查确认第8题从试题PDF第4页底部开始，延续至第5页并结束，第4页上部为第6题尾部和第7题；第8题答案从PDF第19页下半部“八、”开始，至第21页评分标准结束，第19页上半部为第7题结尾和评分标准；
- 更新 `03_corpus/item_texts/CPHO37-Q08.md`，挂接V1转写稿、公式核对表和页面证据，明确原OCR文本仅作错误来源对照，不得用于正式编码证据；
- 更新 `03_corpus/manual_review_a1_batch_log.csv`、`manual_review_a1_render_index.csv` 和 `manual_review_a1_batch_summary.md`，登记A组队列第021-022项的证据、边界和下一步；
- 更新 `03_corpus/manual_review_checklist.csv` 和 `03_corpus/manual_review_priority_followup.csv`，将 `CPHO37-Q08-OCR` 推进为“V1视觉转写完成，待最终复核”，将 `CPHO37-Q08-FORMULA` 推进为“答案公式核对入口完成，待最终复核”；不填写校对人和校对日期，不关闭人工销项；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，记录第37届第8题已完成V1转写入口，并将下一最小任务调整为 `G1-07-A1-TRANSCRIBE-38Q05`；
- 本轮不改写论文正文，不修改原始PDF，不关闭第37届第8题题图问题，不生成正式编码结果、正式统计、正式案例结论、真实评分者记录或人工校对签名，也不提交Git。

## 2026-07-15：G1-07-A1-TRANSCRIBE-37Q03 第37届第3题V1转写

- 新增 `03_corpus/manual_review_transcripts/CPHO37-Q03_transcription_v1.md`，基于第37届试题/答案合并PDF第2页渲染图完成第3题题面V1视觉转写，覆盖负微分电阻、隧道二极管、高频扼流圈 RFC、恒压直流电源 `V_0`、端电压 `V_D`、`R_0`、初始条件、谐振、RLC阻尼振荡和最大平均功率等题面条件；
- 新增 `03_corpus/manual_review_transcripts/CPHO37-Q03_formula_check_v1.csv`，依据答案PDF第9-11页登记回路方程、指数解与初始条件、特征方程、特征根、谐振电流与频率、阻尼振荡条件、电流与频率、工作电压范围、`V_0` 和最大平均功率等关键公式核对入口；
- 新增 `03_corpus/manual_review_renders/G1-07-A1/CPHO37-Q03-paper-page-2.png` 和 `CPHO37-Q03-solution-page-09.png` 至 `CPHO37-Q03-solution-page-11.png` 共4张页面证据图；视觉检查确认第3题题面位于试题PDF第2页上半部，第2页下半部进入第4题；第3题答案从PDF第9页中部“三、”开始，至第11页评分标准结束，第9页上部为第2题结尾和评分标准；
- 更新 `03_corpus/item_texts/CPHO37-Q03.md`，挂接V1转写稿、公式核对表和页面证据，明确原OCR文本仅作错误来源对照，不得用于正式编码证据；
- 更新 `03_corpus/manual_review_a1_batch_log.csv`、`manual_review_a1_render_index.csv` 和 `manual_review_a1_batch_summary.md`，登记A组队列第019-020项的证据、边界和下一步；
- 更新 `03_corpus/manual_review_checklist.csv` 和 `03_corpus/manual_review_priority_followup.csv`，将 `CPHO37-Q03-OCR` 推进为“V1视觉转写完成，待最终复核”，将 `CPHO37-Q03-FORMULA` 推进为“答案公式核对入口完成，待最终复核”；不填写校对人和校对日期，不关闭人工销项；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，记录第37届第3题已完成V1转写入口，并将下一最小任务调整为 `G1-07-A1-TRANSCRIBE-37Q08`；
- 本轮不改写论文正文，不修改原始PDF，不关闭第37届第3题题图问题，不生成正式编码结果、正式统计、正式案例结论、真实评分者记录或人工校对签名，也不提交Git。

## 2026-07-15：G1-07-A1-TRANSCRIBE-42Q06 第42届第6题V1转写

- 新增 `03_corpus/manual_review_transcripts/CPHO42-Q06_transcription_v1.md`，基于第42届试题PDF第4-5页渲染图完成第6题题面V1视觉转写，覆盖转速仪简化模型、轴承A/B、质量 `m_1/m_2`、匀质细杆、坐标系 O-xyz、单位矢量、盘簧回复力矩、匀速转动、冲击后角速度、小振动频率和一阶近似等题面条件；
- 新增 `03_corpus/manual_review_transcripts/CPHO42-Q06_formula_check_v1.csv`，依据答案PDF第16-20页登记力矩平衡、离心力矩积分、`omega_0`存在条件、角动量矢量、轴承作用力、z方向角动量守恒、机械能守恒、`Omega_0`根式、小振动角频率和 `omega(t)` 一阶近似等关键公式核对入口；
- 新增 `03_corpus/manual_review_renders/G1-07-A1/CPHO42-Q06-paper-page-4.png`、`CPHO42-Q06-paper-page-5.png` 和 `CPHO42-Q06-solution-page-16.png` 至 `CPHO42-Q06-solution-page-20.png` 共7张页面证据图；视觉检查确认第6题题面从试题PDF第4页下部开始，延续至第5页上半部结束，第4页上部为第5题尾部，第5页下半部进入第7题；第6题答案从答案PDF第16页下部开始，至第20页评分标准结束，第16页上部为第5题答案尾部，第20页底部进入第7题；
- 更新 `03_corpus/item_texts/CPHO42-Q06.md`，挂接V1转写稿、公式核对表和页面证据，明确原OCR文本仅作错误来源对照，不得用于正式编码证据；
- 更新 `03_corpus/manual_review_a1_batch_log.csv`、`manual_review_a1_render_index.csv` 和 `manual_review_a1_batch_summary.md`，登记A组队列第017-018项的证据、边界和下一步；
- 更新 `03_corpus/manual_review_checklist.csv` 和 `03_corpus/manual_review_priority_followup.csv`，将 `CPHO42-Q06-OCR` 推进为“V1视觉转写完成，待最终复核”，将 `CPHO42-Q06-FORMULA` 推进为“答案公式核对入口完成，待最终复核”；不填写校对人和校对日期，不关闭人工销项；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，记录第42届第6题已完成V1转写入口，并将下一最小任务调整为 `G1-07-A1-TRANSCRIBE-37Q03`；
- 本轮不改写论文正文，不修改原始PDF，不关闭第42届第6题题图问题，不生成正式编码结果、正式统计、正式案例结论、真实评分者记录或人工校对签名，也不提交Git。

## 2026-07-15：G1-07-A1-TRANSCRIBE-40Q08 第40届第8题V1转写

- 新增 `03_corpus/manual_review_transcripts/CPHO40-Q08_transcription_v1.md`，基于第40届试题/答案合并PDF第5页渲染图完成第8题题面V1视觉转写，覆盖X射线光谱与光电子能谱仪器结构、轫致辐射谱、特征谱、K壳层/L壳层、K_alpha线、里德堡常量、康普顿散射、光电子动能和散射光谱峰来源等题面条件；
- 新增 `03_corpus/manual_review_transcripts/CPHO40-Q08_formula_check_v1.csv`，依据答案PDF第21-23页登记最低加速电压、连续谱最短波长、K_alpha能量、莫塞莱关系、有效核电荷数、相对论能量动量、康普顿波长差、光电子动能和光谱峰来源等关键公式核对入口；
- 新增 `03_corpus/manual_review_renders/G1-07-A1/CPHO40-Q08-paper-page-5.png` 和 `CPHO40-Q08-solution-page-21.png` 至 `CPHO40-Q08-solution-page-23.png` 共4张页面证据图；视觉检查确认第8题题面从试题PDF第5页中部开始并在本页结束，第5页上部为第7题尾部；第8题答案从PDF第21页下部开始，至第23页评分标准结束且第23页为PDF末页；
- 更新 `03_corpus/item_texts/CPHO40-Q08.md`，挂接V1转写稿、公式核对表和页面证据，明确原OCR文本仅作错误来源对照，不得用于正式编码证据；
- 更新 `03_corpus/manual_review_a1_batch_log.csv`、`manual_review_a1_render_index.csv` 和 `manual_review_a1_batch_summary.md`，登记A组队列第015-016项的证据、边界和下一步；
- 更新 `03_corpus/manual_review_checklist.csv` 和 `03_corpus/manual_review_priority_followup.csv`，将 `CPHO40-Q08-OCR` 推进为“V1视觉转写完成，待最终复核”，将 `CPHO40-Q08-FORMULA` 推进为“答案公式核对入口完成，待最终复核”；不填写校对人和校对日期，不关闭人工销项；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，记录第40届第8题已完成V1转写入口，并将下一最小任务调整为 `G1-07-A1-TRANSCRIBE-42Q06`；
- 本轮不改写论文正文，不修改原始PDF，不关闭第40届第8题题图问题，不生成正式编码结果、正式统计、正式案例结论、真实评分者记录或人工校对签名，也不提交Git。

## 2026-07-15：G1-07-A1-TRANSCRIBE-40Q05 第40届第5题V1转写

- 新增 `03_corpus/manual_review_transcripts/CPHO40-Q05_transcription_v1.md`，基于第40届试题/答案合并PDF第3-4页渲染图完成第5题题面V1视觉转写，覆盖电偶极子、点电荷、位置矢量、初始条件、电场与电势、圆周运动、角动量、径向速率、有界运动条件和无界运动距离变化等题面条件；
- 新增 `03_corpus/manual_review_transcripts/CPHO40-Q05_formula_check_v1.csv`，依据答案PDF第13-16页登记 `theta_0`、`v_0`、`L(theta)`、`v_r(r)`、有界条件、边界半圆轨道和 `r(t)` 等关键公式核对入口；
- 新增 `03_corpus/manual_review_renders/G1-07-A1/CPHO40-Q05-paper-page-3.png`、`CPHO40-Q05-paper-page-4.png` 和 `CPHO40-Q05-solution-page-13.png` 至 `CPHO40-Q05-solution-page-16.png` 共6张页面证据图；视觉检查确认第5题题面从试题PDF第3页下部开始并延续至第4页顶部，第4页中部已进入第6题；第5题答案从PDF第13页下部开始，至第16页评分标准结束，第16页下部已进入第6题，后续内容仅作边界确认；
- 更新 `03_corpus/item_texts/CPHO40-Q05.md`，挂接V1转写稿、公式核对表和页面证据，明确原OCR文本仅作错误来源对照，不得用于正式编码证据；
- 更新 `03_corpus/manual_review_a1_batch_log.csv`、`manual_review_a1_render_index.csv` 和 `manual_review_a1_batch_summary.md`，登记A组队列第013-014项的证据、边界和下一步；
- 更新 `03_corpus/manual_review_checklist.csv` 和 `03_corpus/manual_review_priority_followup.csv`，将 `CPHO40-Q05-OCR` 推进为“V1视觉转写完成，待最终复核”，将 `CPHO40-Q05-FORMULA` 推进为“答案公式核对入口完成，待最终复核”；不填写校对人和校对日期，不关闭人工销项；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，记录第40届第5题已完成V1转写入口，并将下一最小任务调整为 `G1-07-A1-TRANSCRIBE-40Q08`；
- 本轮不改写论文正文，不修改原始PDF，不关闭第40届第5题题图问题，不生成正式编码结果、正式统计、正式案例结论、真实评分者记录或人工校对签名，也不提交Git。

## 2026-07-15：G1-07-A1-TRANSCRIBE-40Q02 第40届第2题V1转写

- 新增 `03_corpus/manual_review_transcripts/CPHO40-Q02_transcription_v1.md`，基于第40届试题/答案合并PDF第1-2页渲染图完成第2题题面V1视觉转写，覆盖半圆玻璃管、活塞、两侧理想气体、临界温度、正中央稳定性、非零平衡位置、小振动圆频率和角速度等题面条件；
- 新增 `03_corpus/manual_review_transcripts/CPHO40-Q02_formula_check_v1.csv`，依据答案PDF第7-9页登记切向运动方程、小量展开、临界温度 `T_c`、`T = T_c` 三阶稳定性、非零平衡位置 `theta_0`、`omega_0(theta_0)`、温度略大于/略小于 `T_c` 的频率依赖和角速度能量积分等关键公式核对入口；
- 新增 `03_corpus/manual_review_renders/G1-07-A1/CPHO40-Q02-paper-page-1.png`、`CPHO40-Q02-paper-page-2.png` 和 `CPHO40-Q02-solution-page-07.png` 至 `CPHO40-Q02-solution-page-09.png` 共5张页面证据图；视觉检查确认第2题题面从试题PDF第1页下部开始并延续至第2页上部，第2页中部已进入第3题；第2题答案至PDF第9页评分标准结束，第9页下部已进入第3题，后续内容仅作边界确认；
- 更新 `03_corpus/item_texts/CPHO40-Q02.md`，挂接V1转写稿、公式核对表和页面证据，明确原OCR文本仅作错误来源对照，不得用于正式编码证据；
- 更新 `03_corpus/manual_review_a1_batch_log.csv`、`manual_review_a1_render_index.csv` 和 `manual_review_a1_batch_summary.md`，登记A组队列第011-012项的证据、边界和下一步；
- 更新 `03_corpus/manual_review_checklist.csv` 和 `03_corpus/manual_review_priority_followup.csv`，将 `CPHO40-Q02-OCR` 推进为“V1视觉转写完成，待最终复核”，将 `CPHO40-Q02-FORMULA` 推进为“答案公式核对入口完成，待最终复核”；不填写校对人和校对日期，不关闭人工销项；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，记录第40届第2题已完成V1转写入口，并将下一最小任务调整为 `G1-07-A1-TRANSCRIBE-40Q05`；
- 本轮不改写论文正文，不修改原始PDF，不关闭第40届第2题题图问题，不生成正式编码结果、正式统计、正式案例结论、真实评分者记录或人工校对签名，也不提交Git。

## 2026-07-15：G1-07-A1-TRANSCRIBE-42Q05 第42届第5题V1转写

- 新增 `03_corpus/manual_review_transcripts/CPHO42-Q05_transcription_v1.md`，基于第42届试题PDF第3-4页渲染图完成第5题题面V1视觉转写，覆盖约瑟夫森结结构、相位差、约瑟夫森方程、外磁场下相位变化、穿透深度、并联等效电路、势函数、小振动频率和等离子体角频率等题面条件；
- 新增 `03_corpus/manual_review_transcripts/CPHO42-Q05_formula_check_v1.csv`，依据答案PDF第14-16页登记直流电压下 `j(t)` 与周期、外磁场下 `delta(y)`、总电流 `I_J`、`lambda_J`、三支路电流、相位微分方程、等效势、势阱条件、小振动角频率、`omega_J` 和 `c_bar/c` 等关键公式核对入口；
- 新增 `03_corpus/manual_review_renders/G1-07-A1/CPHO42-Q05-paper-page-3.png`、`CPHO42-Q05-paper-page-4.png` 和 `CPHO42-Q05-solution-page-14.png` 至 `CPHO42-Q05-solution-page-16.png` 共5张页面证据图；视觉检查确认第5题题面从试题PDF第3页底部开始并延续至第4页中下部，第4页下部已进入第6题；第5题答案至答案PDF第16页评分标准结束，第16页下方已进入第6题，后续内容仅作边界确认；
- 更新 `03_corpus/item_texts/CPHO42-Q05.md`，挂接V1转写稿、公式核对表和页面证据，明确原OCR文本仅作错误来源对照，不得用于正式编码证据；
- 更新 `03_corpus/manual_review_a1_batch_log.csv`、`manual_review_a1_render_index.csv` 和 `manual_review_a1_batch_summary.md`，登记A组队列第009-010项的证据、边界和下一步；
- 更新 `03_corpus/manual_review_checklist.csv` 和 `03_corpus/manual_review_priority_followup.csv`，将 `CPHO42-Q05-OCR` 推进为“V1视觉转写完成，待最终复核”，将 `CPHO42-Q05-FORMULA` 推进为“答案公式核对入口完成，待最终复核”；不填写校对人和校对日期，不关闭人工销项；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，记录第42届第5题已完成V1转写入口，并将下一最小任务调整为 `G1-07-A1-TRANSCRIBE-40Q02`；
- 本轮不改写论文正文，不修改原始PDF，不关闭第42届第5题题图问题，不生成正式编码结果、正式统计、正式案例结论、真实评分者记录或人工校对签名，也不提交Git。

## 2026-07-15：G1-07-A1-TRANSCRIBE-42Q02 第42届第2题V1转写

- 新增 `03_corpus/manual_review_transcripts/CPHO42-Q02_transcription_v1.md`，基于第42届试题PDF第1-2页渲染图完成第2题题面V1视觉转写，覆盖重离子束探针、二次离子、普罗卡-格林平行板能量分析器、二级聚焦、上下半平面电流和测量位置电势等题面条件；
- 新增 `03_corpus/manual_review_transcripts/CPHO42-Q02_formula_check_v1.csv`，依据答案PDF第4-7页登记平行板内运动、`XD`表达式、二级聚焦条件、`theta_I = pi/6`、`VA`、离轴接收距离 `s`、电流比例、`K2` 和 `Phi` 等关键公式核对入口；
- 新增 `03_corpus/manual_review_renders/G1-07-A1/CPHO42-Q02-paper-page-1.png`、`CPHO42-Q02-paper-page-2.png` 和 `CPHO42-Q02-solution-page-04.png` 至 `CPHO42-Q02-solution-page-07.png` 共6张页面证据图；视觉检查确认第2题题面从试题PDF第1页下部开始并延续至第2页上半部，第2题答案至答案PDF第7页评分标准结束，第7页下半部已进入第3题，仅作边界确认；
- 更新 `03_corpus/item_texts/CPHO42-Q02.md`，挂接V1转写稿、公式核对表和页面证据，明确原OCR文本仅作错误来源对照，不得用于正式编码证据；
- 更新 `03_corpus/manual_review_a1_batch_log.csv`、`manual_review_a1_render_index.csv` 和 `manual_review_a1_batch_summary.md`，登记A组队列第007-008项的证据、边界和下一步；
- 更新 `03_corpus/manual_review_checklist.csv` 和 `03_corpus/manual_review_priority_followup.csv`，将 `CPHO42-Q02-OCR` 推进为“V1视觉转写完成，待最终复核”，将 `CPHO42-Q02-FORMULA` 推进为“答案公式核对入口完成，待最终复核”；不填写校对人和校对日期，不关闭人工销项；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，记录第42届第2题已完成V1转写入口，并将下一最小任务调整为 `G1-07-A1-TRANSCRIBE-42Q05`；
- 本轮不改写论文正文，不修改原始PDF，不关闭第42届第2题题图问题，不生成正式编码结果、正式统计、正式案例结论、真实评分者记录或人工校对签名，也不提交Git。

## 2026-07-15：G1-07-A1-TRANSCRIBE-40Q03 第40届第3题V1转写

- 新增 `03_corpus/manual_review_transcripts/CPHO40-Q03_transcription_v1.md`，基于第40届试题/答案合并PDF第2页渲染图完成第3题题面V1视觉转写，覆盖楔块、匀质圆球、无滑滚动、连滚带滑、`a0`、`ac`、`N`、`N1`、`mu0` 和 `Delta t` 等题面条件；
- 新增 `03_corpus/manual_review_transcripts/CPHO40-Q03_formula_check_v1.csv`，依据答案第9至11页登记动力学基本式、水平方向动量关系、楔块加速度、圆球相对加速度、支持力、最小摩擦因数、连滚带滑条件和接触点 `P` 相对速度等关键公式核对入口；
- 新增 `03_corpus/manual_review_renders/G1-07-A1/CPHO40-Q03-paper-page-2.png` 和 `CPHO40-Q03-solution-page-09.png` 至 `CPHO40-Q03-solution-page-12.png` 共5张页面证据图；视觉检查确认第3题答案至PDF第11页结束，第12页已进入第4题，仅作边界确认；
- 更新 `03_corpus/item_texts/CPHO40-Q03.md`，挂接V1转写稿、公式核对表和页面证据，明确原OCR文本仅作错误来源对照，不得用于正式编码证据；
- 更新 `03_corpus/manual_review_a1_batch_log.csv`、`manual_review_a1_render_index.csv` 和 `manual_review_a1_batch_summary.md`，登记A组队列第005-006项的证据、边界和下一步；
- 更新 `03_corpus/manual_review_checklist.csv` 和 `03_corpus/manual_review_priority_followup.csv`，将 `CPHO40-Q03-OCR` 推进为“V1视觉转写完成，待最终复核”，将 `CPHO40-Q03-FORMULA` 推进为“答案公式核对入口完成，待最终复核”；不填写校对人和校对日期，不关闭人工销项；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，记录第40届第3题已完成V1转写入口，并将下一最小任务调整为 `G1-07-A1-TRANSCRIBE-42Q02`；
- 本轮不改写论文正文，不修改原始PDF，不关闭第40届第3题题图问题，不生成正式编码结果、正式统计、正式案例结论、真实评分者记录或人工校对签名，也不提交Git。

## 2026-07-15：G1-07-A1-FIG-FINALCHECK-41Q02-Q07 题图内部视觉终检

- 新增 `03_corpus/manual_review_transcripts/CPHO41_Q02_Q07_figure_finalcheck_v1.csv`，逐张登记第41届第2题图2a、图2b、图2c、空表及第41届第7题图7a、图7b的关键要素、内部视觉判断、残余风险、后续建议和关闭边界；
- 新增 `03_corpus/manual_review_transcripts/CPHO41_Q02_Q07_figure_finalcheck_summary.md`，汇总本轮内部视觉终检的材料、判断、可用边界和下一步建议；
- 新增 `03_corpus/manual_review_renders/G1-07-A1/CPHO41_Q02_Q07_recrop_finalcheck_contact_v1.png`，作为6张重裁候选图的内部终检预览图；
- 更新 `03_corpus/item_texts/CPHO41-Q02.md` 和 `03_corpus/item_texts/CPHO41-Q07.md`，挂接图件内部终检记录；其中第41届第2题明确图2c因原页贴近正文，正式论文使用前建议重绘；
- 更新 `03_corpus/manual_review_checklist.csv` 和 `03_corpus/manual_review_priority_followup.csv`，将 `CPHO41-Q02-FIG` 与 `CPHO41-Q07-FIG` 推进为“内部视觉终检完成，待人工确认”；不填写校对人和校对日期，不关闭人工销项；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，将下一最小任务调整为 `G1-07-A1-TRANSCRIBE-40Q03`，继续处理A组后续高风险OCR/公式问题；
- 本轮不改写论文正文，不修改原始PDF，不重绘图件，不关闭人工校对项，不补造真实人工校对、专家意见、评分者记录、正式编码结果、统计结论或案例结论，也不提交Git。

## 2026-07-15：G1-07-A1-FIG-REDRAW-41Q02-Q07 题图重裁候选图

- 新增 `03_corpus/scripts/recrop_cpho41_q02_q07_figures.py`，记录第41届第2题和第7题题图重裁的来源页、裁切框、输出文件和边界说明；
- 新增6张题图重裁候选图：`CPHO41-Q02-figure2a-page1-recrop-v1.png`、`CPHO41-Q02-figure2b-page2-recrop-v1.png`、`CPHO41-Q02-figure2c-page2-recrop-v1.png`、`CPHO41-Q02-table-page2-recrop-v1.png`、`CPHO41-Q07-figure7a-page4-recrop-v1.png`、`CPHO41-Q07-figure7b-page4-recrop-v1.png`；
- 新增 `03_corpus/item_assets/CPHO41_Q02_Q07_recrop_manifest.csv`，登记6张候选图的来源页、裁切坐标、输出尺寸、SHA-256校验值、复核要点和边界说明；
- 新增 `03_corpus/manual_review_transcripts/CPHO41_Q02_Q07_figure_recrop_review_v1.md`，说明本轮只从题面渲染页重裁，不重绘、不补字、不修图，不代表真实人工校对完成；
- 更新 `03_corpus/item_texts/CPHO41-Q02.md` 和 `03_corpus/item_texts/CPHO41-Q07.md`，挂接题图重裁候选图与复核记录入口；
- 更新 `03_corpus/manual_review_checklist.csv` 和 `03_corpus/manual_review_priority_followup.csv`，将 `CPHO41-Q02-FIG` 与 `CPHO41-Q07-FIG` 推进为“重裁候选图已生成，待人工确认”；不填写校对人和校对日期；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，将下一最小任务调整为候选图人工对照确认，或继续 `G1-07-A1-TRANSCRIBE-40Q03`；
- 本轮不改写论文正文，不修改原始PDF，不关闭人工校对项，不补造题图、专家意见、评分者记录、正式编码结果、统计结论或案例结论，也不提交Git。

## 2026-07-15：G1-07-A1-FINALIZE-41Q02-Q07 终复核准备记录

- 新增 `03_corpus/manual_review_transcripts/CPHO41_Q02_Q07_final_review_summary.md`，汇总第41届第2题和第7题V1转写、公式核对、页面证据、题图风险和不可声称边界；
- 新增 `03_corpus/manual_review_transcripts/CPHO41_Q02_Q07_final_review_v1.csv`，逐项登记 `CPHO41-Q02-OCR`、`CPHO41-Q02-FORMULA`、`CPHO41-Q02-FIG`、`CPHO41-Q07-OCR`、`CPHO41-Q07-FORMULA`、`CPHO41-Q07-FIG` 的证据、复核判断、剩余阻塞和下一步；
- 更新 `03_corpus/item_texts/CPHO41-Q02.md` 和 `03_corpus/item_texts/CPHO41-Q07.md`，挂接终复核准备记录入口；
- 更新 `03_corpus/manual_review_checklist.csv` 和 `03_corpus/manual_review_priority_followup.csv`，将两题OCR/公式问题推进为“终复核记录已建，未销项”，将两题图件问题推进为“题图风险复查完成，待重裁/重绘”；不填写校对人和校对日期；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，将下一最小任务调整为第41届第2题/第7题题图重裁或继续处理A组后续高风险OCR/公式问题；
- 本轮不改写论文正文，不修改原始PDF，不生成正式编码结果、正式统计、正式案例结论、真实评分者记录或人工校对签名，也不声称两题已完成正式人工校对。

## 2026-07-15：G1-07-A1-TRANSCRIBE-41Q07 第41届第7题V1转写

- 新增 `03_corpus/manual_review_transcripts/CPHO41-Q07_transcription_v1.md`，基于第41届试题PDF第4-5页渲染图完成第7题题面V1视觉转写，覆盖题干、第(1)至第(5.2)问、图7a/7b说明和待复核点；
- 新增 `03_corpus/manual_review_transcripts/CPHO41-Q07_formula_check_v1.csv`，依据答案PDF第16-19页登记单值条件、动量量子化、磁通与矢势、单电子能量、总能量周期、平均能量分段、奇偶比较、两环最低能量和极限比值的核对入口；
- 更新 `03_corpus/item_texts/CPHO41-Q07.md`，挂接V1转写稿、公式核对表和页面证据，明确原OCR文本仅保留为错误来源对照，不得用于正式编码证据；
- 更新 `03_corpus/manual_review_checklist.csv` 和 `03_corpus/manual_review_priority_followup.csv`，将 `CPHO41-Q07-OCR` 状态推进为“V1视觉转写完成，待最终复核”，将 `CPHO41-Q07-FORMULA` 状态推进为“答案公式核对入口完成，待最终复核”；不填写校对人和校对日期，不声称人工校对全部完成；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，记录第41届第7题已完成V1转写入口，并将下一最小任务调整为第41届第2题/第7题最终复核或继续处理A组后续高风险题目；
- 本轮不改写论文正文，不修改原始PDF，不关闭第7题题图问题，不生成正式编码结果、正式统计、正式案例结论、真实评分者记录或人工校对签名。

## 2026-07-15：G1-07-A1-TRANSCRIBE-41Q02 第41届第2题V1转写

- 新增 `03_corpus/manual_review_transcripts/CPHO41-Q02_transcription_v1.md`，基于第41届试题PDF第1-2页渲染图完成第2题题面V1视觉转写，覆盖题干、第(1)至第(4.3)问、图2a/2b/2c和空表说明；
- 新增 `03_corpus/manual_review_transcripts/CPHO41-Q02_formula_check_v1.csv`，依据答案PDF第3-7页登记第(1)问碰撞结果、第(2.1)至第(2.4)问接触点速度/纯滚时间/轨迹/最终速度、第(3)问击球高度、第(4)问30度经验规则公式和表格数值的核对入口；
- 更新 `03_corpus/item_texts/CPHO41-Q02.md`，挂接V1转写稿、公式核对表和页面证据，明确原OCR文本仅保留为错误来源对照，不得用于正式编码证据；
- 更新 `03_corpus/manual_review_checklist.csv` 和 `03_corpus/manual_review_priority_followup.csv`，将 `CPHO41-Q02-OCR` 状态推进为“V1视觉转写完成，待最终复核”，将 `CPHO41-Q02-FORMULA` 状态推进为“答案公式核对入口完成，待最终复核”；不填写校对人和校对日期，不声称人工校对全部完成；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，记录第41届第2题已完成V1转写入口，并将下一最小任务调整为第41届第7题转写或第2题最终复核；
- 本轮不改写论文正文，不修改原始PDF，不关闭第2题题图问题，不生成正式编码结果、正式统计、正式案例结论、真实评分者记录或人工校对签名。

## 2026-07-14：G1-07-A1 首批A组高风险校对证据包

- 新增 `03_corpus/manual_review_a1_batch_log.csv`，登记A组前4项 `CPHO41-Q02-OCR`、`CPHO41-Q02-FORMULA`、`CPHO41-Q07-OCR`、`CPHO41-Q07-FORMULA` 的批次、影响小问、页面证据、当前文本风险、处置决定和下一步动作；
- 新增 `03_corpus/manual_review_a1_render_index.csv`，索引第41届第2题和第7题题面/答案PDF渲染页，共13张页面证据图；
- 新增 `03_corpus/manual_review_a1_batch_summary.md`，说明本批只建立证据包，不代表题干、公式、答案证据或小问边界已经完成正式校对；
- 新增 `03_corpus/manual_review_renders/G1-07-A1/` 下13张PNG页面图，覆盖第41届第2题题面第1-2页、答案第3-7页，第41届第7题题面第4-5页、答案第16-19页；
- 更新 `03_corpus/manual_review_checklist.csv` 和 `03_corpus/manual_review_priority_followup.csv`，将上述4项回填为“A1证据包已建，未销项”，并在 `resolution_note` 中说明仍需逐字重转写和逐式公式核对；`reviewer` 与 `review_date` 保持为空，避免误写成已完成校对；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，记录 `G1-07-A1` 已启动，并将下一最小任务调整为 `G1-07-A1-TRANSCRIBE-41Q02`；
- 本轮不改写论文正文，不修改原始PDF，不补造题干、公式、答案、校对人、校对日期、正式编码结果、统计结论或案例结论，也不提交Git。

## 2026-07-14：G1-07-FOLLOWUP 人工校对优先队列

- 新增 `03_corpus/manual_review_priority_followup.csv`，将154条人工校对待核项按正式编码影响程度分为A/B/C/D四组，并给出队列序号、推荐批次、受影响小问数、关闭条件和不得声称内容；
- 新增 `03_corpus/manual_review_priority_followup_summary.md`，汇总A组76条直接阻塞正式编码证据问题、B组22条影响正式编码证据问题、C组47条图像表征/案例/附录图件问题和D组9条元数据或附属证据问题，并列出A组优先处理前12项；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，记录 `G1-07-FOLLOWUP` 已完成，并将下一最小任务调整为 `G1-07-A1`；
- 本轮不修改题干、答案、题图、原始PDF、试编码或正式编码结果，不填写虚假校对人和日期，不声称人工校对已完成，也不提交Git。

## 2026-07-14：G8-09-PREP 最终提交阻塞项总表

- 新增 `09_quality/g8_09_final_pre_submission_blockers.csv`，登记20项最终提交前阻塞项，覆盖人工校对、真实A/B评分者独立编码、一致性、分歧裁决、`final_coding.csv`、第四章正式结果、第五章教学证据、文献全文、学校规范、参考文献、摘要结论、附录数据说明、匿名版、AI/伦理声明、最终输出、Git版本点和全论文终审；
- 新增 `09_quality/g8_09_blocker_closure_protocol.md`，规定阻塞项优先级、最低销项证据、推荐销项顺序、关闭记录要求和不得用于销项的材料；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，记录 `G8-09-PREP` 已完成，并将下一最小任务调整为 `G1-07-FOLLOWUP`；若收到真实A/B评分者回收文件，则优先回到 `G4-01`；
- 本轮不改写论文正文，不关闭任何阻塞项，不生成正式编码结果、`final_coding.csv`、正式图表、教师/学生/课堂证据、导师意见、专家意见、学校规范、AI披露定稿、伦理审批、Word/PDF、匿名版或最终提交包，也不提交Git。

## 2026-07-14：G8-08-PREP 最终提交与归档包准备

- 新增 `09_quality/g8_08_prep_final_submission_readiness.csv`，登记14项最终提交材料准备度，覆盖学校格式Word/PDF、匿名评审版、第1至5章边界稿、结论、摘要、`final_coding.csv`、正式图表、参考文献、附录、数据可用性、AI使用声明、伦理声明和最终提交包；
- 新增 `09_quality/g8_08_prep_archive_package_manifest.csv`，整理10类可归档研究准备材料，区分项目规则、原始审计、语料索引、编码框架、内部预演、正文草稿、文献工作包、附录/数据说明、教师课堂模板和最终输出目录；
- 新增 `09_quality/g8_08_prep_finalization_roadmap.md`，说明当前可归档材料、当前不能生成的提交材料、最短最终化路线和短期无法取得外部材料时的稳妥处理方式；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，记录 `G8-08-PREP` 已完成，并将下一最小任务调整为 `G8-09-PREP`；
- 本轮不改写论文正文，不生成Word/PDF，不生成匿名评审版，不声明查重通过，不补造正式编码结果、`final_coding.csv`、导师意见、学校规范、AI披露要求、伦理审批、教师数据、学生数据或课堂证据，也不提交Git。

## 2026-07-14：G8-07-PREP 学校规范与匿名评审版检查准备

- 新增 `09_quality/g8_07_prep_school_format_checklist.csv`，登记14项学校提交前格式检查准备项，覆盖论文模板、写作规范、字数、引用格式、匿名评审、查重、AI披露、伦理要求、优秀论文标准、提交流程、Mermaid/图表、附录、数据可用性、摘要与结论；
- 新增 `09_quality/g8_07_prep_anonymous_review_risk_register.csv`，登记8项匿名评审风险，覆盖作者导师信息、本地路径、致谢资助、真实评分者/专家、教师学生课堂材料、试题来源、AI使用痕迹和审计日志公开范围；
- 新增 `09_quality/g8_07_prep_markdown_to_submission_plan.md`，整理当前Markdown/CSV材料包转学校提交版的顺序、当前不能生成的提交材料、可先准备的材料和进入正式 `G8-07` 的前置条件；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，记录 `G8-07-PREP` 已完成，并将下一最小任务调整为 `G8-08-PREP`；
- 本轮不改写论文正文，不生成Word/PDF，不生成匿名评审版，不声明查重通过，不补造学校规范、AI披露要求、伦理审批、导师意见、评分者数据、教师数据、学生数据或课堂证据，也不提交Git。

## 2026-07-14：G8-06-PREP 模拟答辩与高风险问题清单准备版

- 新增 `09_quality/g8_06_prep_defense_risk_questions.csv`，登记16项高风险追问，覆盖原初稿禁用结果、语料规模、人工校对、真实评分者、正式结果、SOLO理论、文献综述、教学转化、案例选择、创新性、可复现性、伦理数据、学校规范、英文术语、范围控制和最终闭环；
- 新增 `09_quality/g8_06_prep_defense_gate.csv`，建立10项答辩门禁，标明当前状态、风险等级、能否回答、可答类型、阻塞问题和下一步动作；
- 新增 `09_quality/g8_06_prep_simulated_response_boundaries.md`，整理模拟问答的可使用回答边界、不可声称内容、高风险追问优先级和后续补证顺序；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，记录 `G8-06-PREP` 已完成，并将下一最小任务调整为 `G8-07-PREP`；
- 本轮不改写论文正文，不生成正式结果，不生成答辩结论，不补造导师意见、专家意见、评分者数据、教师数据、学生数据、课堂证据、实验结果、显著性结论或文献结论，也不提交Git。

## 2026-07-14：G8-05-LOG-TEMPLATE 导师/人工反馈记录模板

- 新增 `09_quality/g8_05_feedback_log_template.csv`，建立真实反馈登记字段，包括来源类型、来源标识、接收日期、涉及章节、反馈摘要、证据状态、处理决定、责任文件和关闭状态；
- 新增 `09_quality/g8_05_feedback_decision_protocol.md`，规定反馈处理决定类型、证据状态、关闭条件、推荐工作流和当前不可填写内容；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，记录 `G8-05-LOG-TEMPLATE` 已完成，并将下一最小任务调整为 `G8-06-PREP`；
- 本轮不填写任何导师、专家、教师、同门或作者反馈，不生成审阅通过结论，不改写论文正文，不补造评分者数据、教师数据、学生数据、课堂证据或文献结论，也不提交Git。

## 2026-07-14：G8-05-PREP 导师/人工反馈闭环材料包准备

- 新增 `09_quality/g8_05_prep_feedback_packet.md`，说明第1至5章当前可审阅版本、建议审阅顺序、高优先级确认问题、关键缺口和使用边界；
- 新增 `09_quality/g8_05_prep_review_questions.csv`，登记12项需人工确认的问题，覆盖研究路线、研究问题、SOLO术语、内部预审边界、第四章结果占位、第五章证据状态、真实评分者、教师/课堂材料、文献全文、学校规范、案例选择和草稿形态；
- 新增 `09_quality/g8_05_prep_review_index.csv`，整理15项可审阅文件索引，标明审阅用途、当前状态、是否优先阅读和注意事项；
- 新增 `09_quality/g8_05_prep_gap_register.csv`，登记10项高风险缺口，覆盖真实评分者编码、分歧裁决、`final_coding.csv`、人工校对、教师/课堂证据、SOLO全文、竞赛文献全文、学校规范、真实专家审查和摘要/结论缺口；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，记录 `G8-05-PREP` 已完成，并将下一最小任务调整为 `G8-05-LOG-TEMPLATE`；
- 本轮不改写论文正文、不生成正式统计、不制作正式图表、不选择正式案例、不补造导师意见、专家意见、评分者数据、教师数据、学生数据或课堂证据，也不提交Git。

## 2026-07-14：G8-04-VERIFY-LITE 第1至5章最终残留轻核查

- 新增 `09_quality/g8_04_verify_lite_audit.csv`，登记12项残留风险核查，覆盖过强结论词、内部预演数字、初稿禁用数字、路径残留、正式分析文件称呼、候选案例边界、教学证据边界和引文占位；
- 新增 `09_quality/g8_04_verify_lite_report.md`，汇总未发现的高风险残留、已修订位置、仍需保留的边界和下一步 `G8-05-PREP`；
- 更新 `08_manuscript/02_theory.md`，补全内部版编码手册和codebook的项目内路径，并统一理论框架图中的“结果—问题—策略—任务—评价”写法；
- 更新 `08_manuscript/04_results.md`，将多处 `final_coding.csv` 补为“裁决后的唯一分析表（final_coding.csv）”，继续强调正式结果尚未生成；
- 更新 `08_manuscript/05_cases_and_diagnosis.md`，将下一步中的 `final_coding.csv` 补为“裁决后的唯一分析表（final_coding.csv）”；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，记录 `G8-04-VERIFY-LITE` 已完成，并将下一最小任务调整为 `G8-05-PREP`；
- 本轮不生成正式统计、不制作正式图表、不选择正式案例、不补造 `final_coding.csv`、导师意见、评分者数据、教师数据、学生数据或课堂证据，也不提交Git。

## 2026-07-14：G8-04-FORMAT-LITE 第1至5章格式与占位轻审

- 新增 `09_quality/g8_04_format_lite_audit.csv`，登记12项标题层级、表格格式、Mermaid图、术语写法、文件路径、引文占位和第五章表格语气检查；
- 新增 `09_quality/g8_04_format_lite_report.md`，汇总本轮检查结论、已修订位置、仍需保留的边界和下一步 `G8-04-VERIFY-LITE`；
- 更新 `08_manuscript/01_introduction.md`，将技术路线图中的“SOLO启发等级框架”改为“SOLO启发的任务认知结构要求等级框架”，并统一“结果—问题—策略—任务—评价”写法；
- 更新 `08_manuscript/03_methods.md`，统一正文中的“第35至42届”写法，并补全 `internal_analysis_candidate_v0.csv`、A/B正式空白模板、裁决模板、G4-01交接报告和prep30门槛表的项目内相对路径；
- 更新 `08_manuscript/04_results.md`，统一“第35至42届”写法，补入“裁决后的唯一分析表（final_coding.csv）”表述，并将4.5标题补为“届次、模块、情境、表征和数学工具差异正式输出占位”；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，记录 `G8-04-FORMAT-LITE` 已完成，并将下一最小任务调整为 `G8-04-VERIFY-LITE`；
- 本轮不生成正式统计、不制作正式图表、不选择正式案例、不补造 `final_coding.csv`、评分者数据、教师数据、学生数据或课堂证据，也不提交Git。

## 2026-07-14：G8-04-PREP 第1至5章术语与交叉引用预审

- 新增 `09_quality/g8_04_prep_term_crossref_audit.csv`，登记12项第1至5章术语、章节状态和交叉引用检查，覆盖“正式结果占位、内部预演、候选材料、待核实分析提纲、采证提纲、final_coding.csv、SOLO启发等级”等术语；
- 新增 `09_quality/g8_04_prep_report.md`，汇总本轮标准术语、主要发现、已修订位置和下一步格式检查任务；
- 更新 `08_manuscript/01_introduction.md`，将后续章节推进顺序从“正式结果、案例机制、教学转化”改为当前草稿状态下的“结果占位、案例候选、教学转化证据准备”；
- 更新 `08_manuscript/02_theory.md`，将过时的“建立检索式、核验课程标准”下一步改为继续补齐SOLO全文、物理竞赛试题研究、方法文献和主张证据矩阵闭环；
- 更新 `08_manuscript/03_methods.md`，将两处仍指向“内部预演结果”的第四章说明改为“正式结果占位与证据边界说明”；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，记录 `G8-04-PREP` 已完成，并将下一最小任务调整为 `G8-04-FORMAT-LITE`；
- 本轮不生成正式统计、不制作正式图表、不选择正式案例、不补造 `final_coding.csv`、评分者数据、教师数据、学生数据或课堂证据，也不提交Git。

## 2026-07-14：G8-03-APPLY-LITE 第4章与第5章轻量正文处理

- 更新 `08_manuscript/04_results.md`，将第四章改为“正式结果占位与边界说明”，保留第35至42届、219个分析单元和154条待核项等语料结构事实，删除具体内部维度分布、等级分布、共现计数和P0/P1复核数量的正文报告；
- 更新 `08_manuscript/05_cases_and_diagnosis.md`，将候选案例表改为候选材料清单，将模型建构、科学推理、科学论证和质疑创新案例段落改为待核实分析提纲，将教师/学生困难表改为采证提纲；
- 新增 `09_quality/g8_03_apply_lite_revision_log.csv`，登记8项正文修订、关联处理建议、证据边界和剩余工作；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，记录 `G8-03-APPLY-LITE` 已完成，并将下一最小任务调整为 `G8-04-PREP` 术语、编号、交叉引用和格式统一审计；
- 本轮不改第1至3章、不生成正式统计、不制作正式图表、不补造 `final_coding.csv`、评分者数据、教师数据、学生数据或课堂证据，也不提交Git。

## 2026-07-14：G8-03-FOLLOWUP 第1至5章内部数字句处理建议

- 新增 `09_quality/g8_03_followup_manuscript_number_actions.csv`，逐章登记40条正文数字、候选案例和结果性句子的处理建议，标明保留、维持边界、改为占位、移入质量说明、移入候选材料或后续删除条件；
- 新增 `09_quality/g8_03_followup_manuscript_number_report.md`，汇总第1至3章可保留的准备事实、第4章正式稿需收缩的内部预演数字、第5章需降为候选池或采证提纲的案例和教学困难表；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，将下一最小任务调整为 `G8-03-APPLY-LITE`；
- 本轮不改写正文、不生成正式统计、不制作正式图表、不补造 `final_coding.csv`、评分者数据、教师数据、学生数据或课堂证据。

## 2026-07-14：G8-03-PREP 统计与图表可复现检查准备

- 新增 `09_quality/g8_03_result_reproducibility_gate.csv`，建立20项数字、图表和结果性表述门禁清单，覆盖语料范围、219个分析单元、154条待核项、876条内部试编码记录、正式门槛、维度分布预演、等级分布预演、共现预演、分组比较预演、P0/P1复核、典型案例候选、教学转化种子和正式图表占位；
- 新增 `09_quality/g8_03_result_reproducibility_report.md`，说明哪些内容可作为语料或准备事实，哪些必须降格为内部预演，哪些正式图表必须等待 `final_coding.csv`；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，将下一最小任务调整为 `G8-03-FOLLOWUP`；
- 本轮不改写正文、不生成正式统计、不制作正式图表、不把内部预演数字写成正式结果，也不补造评分者、教师、学生或课堂证据。

## 2026-07-14：G8-02-BIB-LITE 正式参考文献候选清单与占位映射

- 新增 `09_quality/g8_02_bib_lite_mapping.csv`，将 `CS-001`、`ST-002`、`ST-003`、`ST-005`、`ST-006` 和 `METH-004` 映射到 `references.bib` 条目、正文占位分布、可支持主张、禁止外推边界、格式缺口和后续动作；
- 新增 `09_quality/g8_02_bib_lite_exclusion_register.csv`，明确 `SOLO-001/002`、`PCOMP-001` 至 `PCOMP-005`、`METH-001/002/003/005`、`ST-001/ST-004` 当前不得进入正式候选参考文献清单；
- 新增 `09_quality/g8_02_bib_lite_report.md`，汇总六项正式候选、排除项、学校格式缺口和下一最小任务；
- 更新 `02_literature/references.bib` 文件说明，将其定位为工作版BibTeX清单，并标注 `biggs1982solo` 与 `biggs1989solo` 仍为全文待读工作候选；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，将下一最小任务调整为 `G8-03-PREP`；
- 本轮不改写正文、不生成最终学校格式参考文献、不补造页码/图表号，也不把待读全文来源加入正式候选清单。

## 2026-07-14：G8-02-APPLY-LITE 第1至5章保守引用占位接入

- 更新 `08_manuscript/01_introduction.md`，为课程标准依据、任务要求与学生能力边界、教学转化边界、文献综述线索和研究内容中的一致性报告/教学转化设计补充保守来源ID占位；
- 更新 `08_manuscript/02_theory.md`，将 `CS-001`、`ST-002`、`ST-003`、`METH-004`、`ST-005`、`ST-006` 接入科学思维四维度、任务要求边界、两层编码报告边界和理论框架图；
- 更新 `08_manuscript/03_methods.md`，为研究对象边界、评分者一致性报告流程、正式编码数据处理、教学转化设计和质量控制补充来源ID占位；
- 更新 `08_manuscript/04_results.md`，只为内部预演结果的解释边界和正式结果章质量报告边界补充来源ID占位，不用外部文献支撑内部数字；
- 更新 `08_manuscript/05_cases_and_diagnosis.md`，为科学论证案例设计和教学转化任务—支架—评价链条补充 `ST-005`、`ST-006` 占位，同时保留“不证明教学效果”的边界；
- 新增 `09_quality/g8_02_apply_lite_revision_log.csv`，登记9处引用占位修订、关联来源、支持主张和保留边界；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，将下一最小任务调整为 `G8-02-BIB-LITE`；
- 本轮不新增文献池、不写未复核页码或图表号、不把SOLO/物理竞赛/METH其余待读全文来源写成正式综述，也不提交Git。

## 2026-07-14：G8-02-VERIFY-FIRST 优先来源版本与支撑语句核验

- 新增 `09_quality/g8_02_verify_first_report.md`，汇总 `CS-001`、`ST-002`、`ST-003`、`ST-005`、`ST-006` 和 `METH-004` 的版本核验结论、可支持正文语句和禁止外推边界；
- 新增 `09_quality/g8_02_verify_first_sources.csv`，逐项记录6个优先来源的候选参考文献格式、在线或本地证据、页码/定位状态、允许使用范围、禁止使用范围和后续动作；
- 更新 `08_manuscript/reference_readiness_register.csv`，将 `ST-002`、`ST-003`、`ST-005`、`ST-006` 和 `METH-004` 从候选状态升级为“限边界性引用”，同时保留出版社PDF、补充材料、图表编号或中外框架边界的后续复核要求；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，将下一最小任务调整为 `G8-02-APPLY-LITE`；
- 本轮不改写正文、不新增文献池、不把待读全文来源写成正式综述，不补造页码、图表号、学校引用格式或教学效果证据。

## 2026-07-14：G8-02-PREP 第1至5章引文核验入口表

- 新增 `09_quality/g8_02_citation_verification_entry.md`，说明第1至5章引文核验范围、四类判定口径、分章使用边界、不能继承的原初稿引文内容和下一最小任务；
- 新增 `09_quality/g8_02_citation_verification_entry.csv`，逐项登记23类正文相关来源，将其分为6项“可引用”、2项“只能作线索”、13项“待读全文”和2项“不得引用”，并写明允许用途、禁止用途、补证动作和证据文件；
- 新增 `09_quality/g8_02_citation_action_queue.csv`，把 `CS-001`、`ST-002`、`ST-003`、`ST-005`、`ST-006` 和 `METH-004` 列为优先版本/页码/正文支撑语句复核对象；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，将 `G8-02` 标为进行中，并把下一最小任务调整为 `G8-02-VERIFY-FIRST`；
- 本轮不改写正文、不新增参考文献、不进行外部检索、不把题录/摘要/预览/工作版bib写成正式引用，也不提交Git。

## 2026-07-14：G8-01-APPLY 第1至5章正文降格修订

- 更新 `08_manuscript/01_introduction.md`，将研究内容改为计划性表述，明确无真实教师或课堂证据时第五章只能保留为教学转化设计建议，并将方法价值表述降格为减少混淆风险；
- 更新 `08_manuscript/02_theory.md`，区分课程标准已核验与SOLO/方法/竞赛文献未全文核验，将“两层编码”从方法贡献降格为设计意图，保留真实评分者一致性和分歧裁决门槛；
- 更新 `08_manuscript/03_methods.md`，明确Codex内部预审不是专家效度证据，A/B空白模板不能写成真实评分者数据，第三章仍为研究设计与准备状态；
- 更新 `08_manuscript/04_results.md`，将章节标题改为“内部预演结果”，把维度分布、等级分布、共现模式和分组比较解释降格为预演观察、候选检查路径和风险提示；
- 更新 `08_manuscript/05_cases_and_diagnosis.md`，将章节标题改为“典型试题机制与教学转化证据准备”，把候选案例、质疑创新判断和教学错位诊断收束为待复核线索与证据需求；
- 新增 `09_quality/g8_01_apply_revision_log.csv`，记录5项正文降格修订、关联队列、修订后证据边界和未完成事项；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，记录 `G8-01-APPLY` 已完成，并把下一最小任务调整为 `G8-02-PREP` 引文逐条核验入口表；
- 本轮不生成正式编码结果、不选择正式案例、不写教学验证、不补造专家/教师/学生/问卷/课堂/显著性证据，也不提交Git。

## 2026-07-14：G8-01-PREP 跨章节主张—证据预审

- 新增 `09_quality/cross_chapter_claim_audit_prep.md`，对第1至5章草稿进行跨章节证据体检，明确可保留、需降格、待补证和必须删除/不得出现的主张类型；
- 新增 `09_quality/cross_chapter_claim_audit_prep.csv`，逐条登记25项章节主张或文本风险，包括第一章研究空白候选、第二章SOLO边界、第三章专家/评分者流程、第四章内部预演数字、第五章候选案例和教师/课堂证据缺口；
- 新增 `09_quality/cross_chapter_revision_queue.csv`，形成12项后续正文降格修订队列，优先处理第四章内部预演结果、第五章质疑创新和教师/学生困难、第三章专家审查与真实评分者边界；
- 更新 `09_quality/claim_evidence_matrix.csv`，补充 `C3-01`、`C3-02`、`C4-01`、`C4-02`、`C5-01`、`C5-02` 和 `CX-01`，把第三章至第五章及跨章节禁止继承主张纳入证据矩阵；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，将 `G8-01` 标为进行中，记录 `G8-01-PREP` 已完成，并把下一最小任务调整为 `G8-01-APPLY` 第一轮正文降格修订；
- 本轮不改写第1至5章正文，不生成正式结果，不补造专家、评分者、教师、学生、问卷、课堂、显著性或参考文献证据。

## 2026-07-14：G7-08-PREP 参考文献、附录和数据说明预备清单

- 新增 `08_manuscript/g7_08_reference_appendix_data_prep.md`，汇总第1至5章当前正文状态、参考文献使用原则、附录候选结构、数据说明边界和后续定稿入口；
- 新增 `08_manuscript/reference_readiness_register.csv`，区分课程标准、SOLO理论、物理竞赛研究、科学思维测评、科学论证教学、科学实践框架和方法文献的可引用状态、允许用途、禁止用途和下一步补证要求；
- 新增 `08_manuscript/appendix_material_register.csv`，登记语料来源、小问索引、编码定义、评分者交接、正式编码模板、风险门槛、图表脚本、教师课堂模板和主张证据矩阵等附录候选；
- 新增 `08_manuscript/data_availability_prep_register.csv`，登记原始初稿材料、复赛试题语料、小问级索引、人工校对清单、内部编码数据、正式空白模板、正式分析表缺口、分析脚本、教师课堂数据缺口和主张证据矩阵的数据可用性边界；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，将 `G7-08` 标为进行中，并把下一最小任务调整为 `G8-01-PREP` 跨章节主张—证据预审；
- 本轮不新增参考文献，不补造正式附录，不定稿数据可用性声明，不写正式编码结果、教师/课堂证据、教学效果或学校格式要求。

## 2026-07-14：G7-05-PREP 第一章绪论证据边界版

- 更新 `08_manuscript/01_introduction.md`，将原占位稿扩展为第一章证据边界版，包含研究背景与问题提出、核心概念与研究边界、文献综述线索、研究问题、研究内容、技术路线、研究价值和创新候选；
- 新增 `09_quality/chapter1_intro_evidence_boundary.csv`，逐条登记第一章可使用主张、证据等级、允许写法、禁止写法和后续补证要求；
- 更新 `09_quality/claim_evidence_matrix.csv`，新增 `C1-01` 至 `C1-06`，覆盖课程标准依据、小问级语料基础、试题任务要求与学生能力边界、SOLO启发表述、研究空白候选和创新候选边界；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，将 `G7-05` 标为进行中，并把下一最小任务调整为 `G7-08-PREP` 参考文献、附录和数据说明预备清单；
- 本轮不写正式统计结果、不引用未核验文献结论、不写教师/课堂效果、不写显著性结论、不把内部预演或原初稿数字作为正式论文发现。

## 2026-07-14：G4-01-PREP-LOCK 评分者交接包冻结

- 新增 `04_framework/rater_handoff_lock_v1.md`，冻结评分者交接包的文件清单、阅读顺序、发放前检查、回收入口规则和后续出口；
- 新增 `04_framework/rater_handoff_lock_manifest.csv`，逐项登记本次交接冻结包的材料、接收对象、使用边界和下一步动作；
- 新增 `04_framework/rater_independent_coding_instructions_v1.md`，明确评分者A/B独立填写要求、可用判断依据、字段取值、待核实处理和提交前自查；
- 新增 `04_framework/rater_handoff_file_rules.csv`，规定A/B模板发放、回收、检查、一致性、分歧日志和裁决文件的命名规则；
- 新增 `04_framework/rater_handoff_unresolved_risks.csv`，列出人工校对未销项、真实评分者缺失、一致性未发生、裁决未发生、内部预演误用、教师课堂证据缺失、文献全文核验不完整和学校规范缺失等风险；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，将 `G4-01-PREP-LOCK` 标记为完成，并把下一最小任务调整为 `G7-05-PREP` 第一章绪论证据边界草稿；
- 本轮不启动真实评分者编码、不填写A/B模板、不计算一致性、不裁决分歧、不生成正式结果表，也不把内部预演写成正式论文结论。

## 2026-07-14：G3-04-QA 评分者培训包索引与字段对齐

- 新增 `04_framework/rater_training_package_index.md` 和 `04_framework/rater_training_package_index.csv`，将分析单位定义、codebook草案、评分者培训手册、边界案例库、证据分歧协议、A/B正式空白模板、裁决模板和回收核对表整理为可交接包；
- 新增 `04_framework/rater_training_field_alignment_audit.csv`，逐字段检查 `formal_coding_rater_A/B_template.csv`、`formal_adjudication_template.csv`、评分者培训手册、证据协议和回收核对表之间的对应关系；
- 新增 `04_framework/rater_training_return_checklist.csv`，规定交接前、A/B模板回收、分歧裁决前后需要检查的记录数、字段取值、证据完整性、版本信息、待核实标记和复制内部预演风险；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，将 `G3-04-QA` 记录为完成，并把下一最小任务调整为 `G4-01-PREP-LOCK` 评分者交接包冻结；
- 本轮不启动真实评分者编码、不回填A/B模板、不生成分歧清单、不计算一致性、不形成正式论文结果。

## 2026-07-14：G3-04-DRAFT 评分者培训版手册候选稿

- 新增 `04_framework/rater_training_manual_formal_draft.md`，将分析单位、维度定义、等级边界、字段填写、停止条件和分歧处理顺序整理为评分者培训版候选稿；
- 新增 `04_framework/boundary_case_bank_formal_draft.csv`，从 P0/P1 内部复核风险、证据补强清单和人工校对队列中抽取16个训练候选案例，用于训练 L3/L4 边界、质疑创新触发条件、证据薄弱和材料待核实处理；
- 新增 `04_framework/evidence_note_and_disagreement_protocol_formal_draft.md`，规定证据摘记最低格式、可接受/不可接受证据、把握度、分歧类型、裁决记录字段和正式统计入口规则；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，将 `G3-04` 继续标为进行中，并把下一最小任务调整为 `G3-04-QA` 培训包字段对齐与回收核对表；
- 本轮不进行真实评分者编码、不计算一致性、不裁决分歧、不把边界案例写作正式结果。

## 2026-07-14：G3-01/G3-02/G3-03-DRAFT 分析单位与编码定义正式草案

- 新增 `04_framework/analysis_unit_and_coding_definitions_formal_draft.md`，从内部冻结版手册抽取分析对象、分析单位、拆分/合并规则、纳入排除规则、证据优先级、科学思维四维度操作性定义和SOLO启发等级定义；
- 新增 `04_framework/codebook_v2_formal_draft.csv`，将16个维度-等级指标整理为正式草案版 codebook，并为每项写入待真实评分者试编码和导师确认的使用边界；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，将 `G3-01`、`G3-02`、`G3-03` 标为进行中，明确当前只是正式草案，不是正式编码手册V2冻结版；
- 下一最小任务调整为 `G3-04-DRAFT`：补充边界案例、证据摘记格式、分歧记录规则和正式评分者模板字段对齐；
- 本轮不进行正式编码、不计算一致性、不把内部预演结果或草案定义写成正式论文结果。

## 2026-07-14：G0-03-PREP 学校规范索取清单与登记表

- 新增 `01_positioning/school_requirements_request_packet.md`，整理学校论文模板、写作规范、字数、引用格式、匿名评审、查重、AI使用声明、伦理要求、优秀论文标准和提交流程的索取清单；
- 新增 `01_positioning/school_requirements_register.csv`，为后续收到学校或学院文件后的来源、版本、适用范围、影响文件、状态和下一步动作建立登记表；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，将 `G0-03` 标为进行中，明确本轮只完成准备机制，不代表已经获得学校模板、引用规范、匿名评审规则或优秀论文评审细则；
- 下一最小任务调整为 `G3-01/G3-02/G3-03`，将分析单位、排除规则、科学思维维度和SOLO启发等级从内部手册抽出为正式草案；若作者提供学校规范文件，则优先回到 `G0-03` 登记并更新格式门槛；
- 本轮不改写论文正文，不预设学校字数、引用格式、匿名处理范围、AI披露文本或优秀论文评分细则。

## 2026-07-14：G0-02-INTERNAL 路线A/B/C内部收敛备忘

- 新增 `01_positioning/route_convergence_memo.md`，基于当前语料、正式编码准备、人工校对风险、文献全文缺口、教师/课堂证据缺口和G0-04/G0-05边界，对路线A、路线B、路线C进行内部收敛判断；
- 更新 `01_positioning/scope_decision_memo.md`，将模板改为当前项目的实际范围备忘，记录已有资料、缺失资料、路线A/B/C可行性、风险和内部建议；
- 更新 `01_positioning/title_decision.md`，把方案A标为默认工作题目，方案B标为有真实课堂材料时的条件性升级题目，方案C标为当前不建议默认使用；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，将 `G0-02` 标为进行中，明确当前只是内部路线收敛，不等同于导师正式确认；下一最小任务调整为 `G0-03-PREP` 学校模板与优秀论文标准索取清单；
- 本轮不写论文正文，不伪造导师意见、教师数据、课堂材料、专家审查、问卷结果、准实验或显著性结论。

## 2026-07-14：G0-05 伦理与数据管理方案

- 升级 `DATA_MANAGEMENT.md`，将原有简要原则扩展为全项目数据分级、采集前门槛、知情同意、匿名化、清洗版本、公开复现包、正文写作门槛和AI工具使用边界；
- 新增 `05_fieldwork/ethics_and_data_management_plan.md`，明确教师访谈、问卷、专家咨询、课堂设计型研究和准实验/前后测的最低证据包、路线分流、匿名编号、正文可用性判定和暂不执行事项；
- 新增 `05_fieldwork/consent_log.csv`、`05_fieldwork/data_collection_log.csv` 和 `06_teaching_validation/classroom_data_manifest.csv`，作为后续真实同意记录、采集记录和课堂材料登记的空白模板；
- 更新 `05_fieldwork/consent_template.md`，补充研究目的、参与内容、自愿退出、隐私匿名化、录音、数据保存和成果使用说明；
- 更新 `.gitignore`，排除 `99_private_data/`、田野/课堂私有原始材料目录、私有身份对应表和常见音视频文件，避免真实姓名、联系方式、签名、录音、录像和未匿名学生作品进入公开仓库；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，将 `G0-05` 标为完成，并把下一最小任务调整为 `G0-02` 路线A/B/C内部收敛备忘；
- 本轮不进行真实招募、问卷发放、访谈、课堂实施、学生作品收集、前后测、专家意见回收或任何显著性检验。

## 2026-07-14：G0-04 初稿不可继承数字与表述清单

- 新增 `01_positioning/non_inheritable_claims_inventory.md`，逐类登记原始初稿、问卷初稿和汇报PPT中不得直接进入新版论文的年份、试题统计、SOLO趋势、专家验证、问卷结果、教学实验、显著性结论、前后测均值、参考文献和模板化致谢；
- 更新 `09_quality/unverified_claims.csv`，补登记复赛英文误译、2020至2027届次年份、力学40%至50%、情境复杂度趋势、SOLO跃迁、得分率/区分度相关、问卷结果、平行班实验、测评卷信效度、八周干预、四组前后测均值/t值/p值、分层提升和未核验参考文献；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，将 `G0-04` 标为完成，并把下一最小任务调整为 `G0-05` 伦理与数据管理方案；
- 本轮不改写论文正文，不补造数据、文献、问卷、课堂、专家意见或显著性结果；所有初稿结果性表述仍为E0，不得作为正式论文结论。

## 2026-07-14：G2-04-FULLTEXT-ACCESS 物理竞赛研究文献访问审计

- 新增 `02_literature/physics_competition_access_audit.md`，记录 `PCOMP-001` 至 `PCOMP-005` 的合法访问状态、来源线索、排除边界、获取优先级和写作边界；
- 更新 `02_literature/physics_competition_fulltext_request_packet.md`，加入二次请求文本，并将后续获取优先级调整为先取 `PCOMP-002` 与 `PCOMP-003` 学位论文全文；
- 更新 `02_literature/physics_competition_screening_matrix.csv`、`reference_verification.csv`、`literature_matrix.csv`、`search_log.csv` 和 `09_quality/claim_evidence_matrix.csv`，将 `PCOMP-001` 与 `PCOMP-005` 标为仅有CNKI题录和《物理教学》目录线索，将 `PCOMP-002`、`PCOMP-003`、`PCOMP-004` 标为仅有CNKI引用/题录线索；
- 补登记 `PCOMP-005` 到文献核验表和文献矩阵，明确其为单题赏析候选，不作为系统综述核心证据；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，将下一最小任务调整为 `G0-04` 建立不可使用的初稿数字与表述清单；
- 本轮未新增已读全文，不能转述候选文献的样本范围、统计结果、研究结论、教学建议或研究空白。

## 2026-07-14：G2-METHOD-ACCESS-REST 方法文献二次访问审计

- 更新 `02_literature/content_analysis_reliability_access_audit.md`，补充 `METH-001`、`METH-002`、`METH-003`、`METH-005` 的二次合法访问审计、精确获取路径和排除来源；
- 更新 `02_literature/content_analysis_reliability_fulltext_request_packet.md`，加入二次请求文本，并将后续动作调整为申请剩余四项全文或关键章节；
- 更新 `02_literature/content_analysis_reliability_screening_matrix.csv`、`reference_verification.csv`、`literature_matrix.csv` 和 `search_log.csv`，明确 Google Books 只支持书目/目录/预览核验，SAGE/JSTOR/PubMed/OpenAIRE/Semantic Scholar 只支持题录、摘要或访问状态核验；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，将 `G2-METHOD-ACCESS-REST` 标为完成，并把下一步调整为 `G2-04-FULLTEXT-ACCESS` 物理竞赛试题研究候选文献全文获取审计；
- 本轮未新增已读全文；不得将非授权PDF、Sci-Hub/Scribd链接、Google Books预览或SAGE受限页写成正式方法依据。

## 2026-07-14：G2-05-ACCESS-ST001-ST004 二次访问审计

- 更新 `02_literature/scientific_thinking_access_audit.md`，补充 ST-001 的 PER-Central、PhysPort、Wiley 精确线索，以及 ST-004 的 ScienceDirect、PubMed、PMC 精确线索；
- 更新 `02_literature/scientific_thinking_fulltext_request_packet.md`，加入 ST-001/ST-004 精确图书馆/馆际互借请求文本；
- 更新 `scientific_thinking_screening_matrix.csv`、`reference_verification.csv`、`literature_matrix.csv` 和 `search_log.csv`，把 ST-001 标为“PER-Central/PhysPort线索已定位但全文未获”，把 ST-004 标为“ScienceDirect预览与PubMed摘要已核验但全文未读”；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，将下一步调整为在外部权限未到位时并行推进方法文献或物理竞赛研究全文获取；
- 本轮没有新增已读全文，不把 PhysPort 摘要、PER-Central题录或 ScienceDirect预览写成正式综述结论。

## 2026-07-14：G2-05-READ-ST002 与剩余科学思维文献访问审计

- 新增 `02_literature/scientific_thinking_st002_reading_notes.md`，完成 Bao 等 (2009) 作者个人站点PDF阅读，并通过 PubMed 核验题录；
- 新增 `02_literature/scientific_thinking_access_audit.md`，审计 ST-001、ST-002 和 ST-004 的全文访问状态；
- 更新 `scientific_thinking_screening_matrix.csv`、`reference_verification.csv`、`literature_matrix.csv`、`search_log.csv`、`references.bib`、`concept_map_and_gap_candidates.md` 和 `claim_evidence_matrix.csv`；
- 将 ST-002 纳入 `C2-02` 的部分核验，支持区分内容知识、科学推理测评表现和试题任务要求；
- 明确 ST-001 仍未获全文，ST-004 仅完成 PubMed 摘要/题录核验，均不得转述为已读全文结论；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，将下一最小任务调整为获取 ST-001 与 ST-004 全文，或并行推进方法文献/物理竞赛文献全文获取。

## 2026-07-14：G2-05-READ-ST005 科学论证教学文献全文摘录

- 新增 `02_literature/scientific_thinking_st005_reading_notes.md`，完成 Osborne、Erduran 与 Simon (2004) 关于科学课堂论证教学与评价支架的UCL开放仓储PDF阅读；
- 更新 `02_literature/scientific_thinking_fulltext_request_packet.md` 和 `scientific_thinking_screening_matrix.csv`，将 `ST-005` 标为已读UCL开放仓储PDF，并记录版本复核风险；
- 更新 `02_literature/reference_verification.csv`、`literature_matrix.csv`、`search_log.csv`、`references.bib`、`02_literature/concept_map_and_gap_candidates.md` 和 `09_quality/claim_evidence_matrix.csv`，为 `C2-06` 补充科学论证教学中的任务、支架和评价框架证据；
- 该文可支持第五章教学转化需具备竞争性任务、证据材料、教师追问、写作框架和论证质量评价，但不能作为物理竞赛教学策略有效性、学生能力提升或本项目课堂验证完成的证据。

## 2026-07-14：G2-05-READ-ST006 科学实践框架官方文本摘录

- 新增 `02_literature/scientific_thinking_st006_reading_notes.md`，完成 NGSS Appendix F 官方在线章节阅读，提取科学与工程实践、任务表现、评价对象和中外框架可比边界；
- 更新 `02_literature/scientific_thinking_screening_matrix.csv`，将 `ST-006` 标为已读官方在线章节，并记录摘录文件、证据要点和剩余风险；
- 更新 `02_literature/reference_verification.csv`、`literature_matrix.csv`、`search_log.csv`、`references.bib`、`02_literature/concept_map_and_gap_candidates.md` 和 `09_quality/claim_evidence_matrix.csv`，将 `C2-06` 从“待核验”调整为“部分核验”；
- 该文本仅作为科学与工程实践、任务表现和评价量规的国际框架参照，不能替代中国普通高中物理课程标准，不能证明物理竞赛教学策略有效，也不能代替真实教师、课堂或学生作品证据。

## 2026-07-14：G2-05-READ-ST003 科学思维测评文献全文摘录

- 新增 `02_literature/scientific_thinking_st003_reading_notes.md`，完成 Bao 等 (2022) 关于科学思维与科学推理理论模型及量化测评的开放全文内容摘录；
- 更新 `02_literature/scientific_thinking_screening_matrix.csv`，新增阅读状态、摘录文件、证据要点和剩余风险字段，并将 `ST-003` 标为已完成开放全文内容阅读；
- 更新 `02_literature/reference_verification.csv`、`literature_matrix.csv`、`search_log.csv`、`references.bib` 和 `09_quality/claim_evidence_matrix.csv`，将 `C2-02` 从“待核验”调整为“部分核验”，并把 `ST-003` 作为 `C2-04` 的辅助参照；
- 该文仅支持区分任务认知要求、学生作答表现和量化测评模型，不能替代中国课程标准、不能证明本项目编码框架有效，也不能说明学生实际能力或教学效果；正式引用前仍需人工下载APS PDF复核页码和图表编号。

## 2026-07-14：G2-METHOD-READ-METH004 方法文献全文摘录

- 新增 `02_literature/content_analysis_reliability_meth004_reading_notes.md`，完成 Lombard、Snyder-Duch 与 Bracken (2002) 关于内容分析编码者一致性评估与报告的全文方法摘录；
- 更新 `02_literature/content_analysis_reliability_screening_matrix.csv`，新增阅读状态、摘录文件、方法要点和剩余风险字段，并将 `METH-004` 标为已读全文；
- 更新 `02_literature/reference_verification.csv`、`literature_matrix.csv`、`search_log.csv`、`references.bib` 和 `09_quality/claim_evidence_matrix.csv`，将 `C2-04` 从“待核验”调整为“部分核验”；
- 该文仅支持逐变量一致性报告、指标选择说明、训练/样本/分歧处理记录等方法边界，不能证明本项目编码框架有效，不能替代真实评分者数据，也不能直接确定本项目一致性阈值。

## 2026-07-14：G2-METHOD-ACCESS-AUDIT 方法文献合法获取审计

- 新增 `02_literature/content_analysis_reliability_access_audit.md`，记录 `METH-001` 至 `METH-005` 的合法访问状态、来源线索、排除线索、阅读顺序和写作边界；
- 更新 `02_literature/content_analysis_reliability_screening_matrix.csv`、`reference_verification.csv`、`literature_matrix.csv` 和 `search_log.csv`，将 `METH-004` 标为有开放仓储线索、可优先安排合法全文阅读，将 `METH-001`、`METH-002`、`METH-003`、`METH-005` 标为仍需机构权限或馆际互借；
- 更新 `02_literature/content_analysis_reliability_fulltext_request_packet.md`、`PROJECT_STATUS.md` 和 `TASKS.md`，将下一步调整为优先阅读 `METH-004` 并继续申请其余方法文献全文；
- 当前仍不得写成已阅读全文、已完成方法综述、已确定一致性阈值或已形成第三章正式方法结论。

## 2026-07-14：G2-METHOD-FULLTEXT-PACKET 方法文献全文获取包

- 新增 `02_literature/content_analysis_reliability_fulltext_request_packet.md`，整理 `METH-001` 至 `METH-005` 的全文获取优先级、图书馆/导师请求文本、获取后阅读记录模板、阅读问题和写作边界；
- 新增 `02_literature/content_analysis_reliability_screening_matrix.csv`，为内容分析、codebook、评分者一致性和kappa解释等方法候选文献建立筛选决策、综述角色、待提取字段和正文边界；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，将下一步调整为合法获取全文并填写方法文献筛选矩阵；
- 当前仍不得写成已获全文、已完成方法综述、已确定一致性阈值或已验证本项目编码框架。

## 2026-07-14：G2-06-CLAIMS 主张证据矩阵与方法文献候选

- 更新 `09_quality/claim_evidence_matrix.csv`，新增 `C2-02`、`C2-04`、`C2-05`、`C2-06`，全部标为“待核验”，分别对应任务要求/学生能力边界、两层编码方法依据、竞赛试题研究空白候选和教学转化边界；
- 新增 `02_literature/content_analysis_reliability_review_prep.md`，整理内容分析、编码手册、评分者一致性和一致性报告方法文献候选；
- 更新 `02_literature/search_log.csv`，新增5条方法文献定位记录，覆盖Krippendorff内容分析、Cohen kappa、Landis & Koch分类一致性、Lombard等编码者一致性报告和Neuendorf内容分析指南；
- 更新 `02_literature/reference_verification.csv` 与 `02_literature/literature_matrix.csv`，新增 `METH-001` 至 `METH-005` 及对应文献矩阵记录；当前均为候选或全文待读状态，不能作为正式方法结论；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，将下一步调整为方法文献全文获取请求包和筛选矩阵。

## 2026-07-14：G2-06-PREP 概念关系图与研究空白候选清单

- 新增 `02_literature/concept_map_and_gap_candidates.md`，基于课程标准、SOLO阶段性来源核验、物理竞赛试题研究候选来源、科学思维测评与教学研究候选来源，整理概念关系图和研究空白候选清单；
- 文件明确区分课程标准E2证据、SOLO/竞赛/科学思维候选E1证据和项目内部准备材料，避免把候选文献线索写成已证明研究空白；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，将 `G2-06` 标为进行中，并把下一步调整为主张—证据矩阵补充和内容分析/评分者一致性方法文献核验。

## 2026-07-14：G2-05-FULLTEXT-PACKET 科学思维测评与教学研究全文获取包

- 新增 `02_literature/scientific_thinking_fulltext_request_packet.md`，整理ST-001至ST-006的全文获取优先级、图书馆/导师请求文本、获取后阅读记录模板和写作边界；
- 新增 `02_literature/scientific_thinking_screening_matrix.csv`，为科学思维测评与教学研究候选文献建立筛选决策、综述角色、待提取字段和写作边界；
- 更新 `02_literature/scientific_thinking_review_prep.md`，将后续动作指向全文获取包和筛选矩阵；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，明确 `G2-05` 仍为进行中，当前尚未获得全文或完成正式综述。

## 2026-07-14：G2-05-PREP 科学思维测评与教学研究综述准备

- 新增 `02_literature/scientific_thinking_review_prep.md`，记录科学思维测评、科学推理、控制变量任务、科学论证教学和国际科学实践框架的候选来源与写作边界；
- 更新 `02_literature/search_log.csv`，新增6条G2-05实际定位记录，覆盖Lawson形式推理测验、Bao等科学推理与科学思维测评研究、Zhou等控制变量推理任务、Osborne等科学论证教学和NGSS科学实践框架；
- 更新 `02_literature/reference_verification.csv`，新增 `ST-001` 至 `ST-006` 作为候选来源；当前均不得直接写成正式综述结论；
- 更新 `02_literature/literature_matrix.csv`，新增 `LM-ST-001` 至 `LM-ST-006`，以“全文待读”状态登记研究问题、理论、样本、方法和边界；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，将 `G2-05` 标为进行中；本轮不完成正式综述，不写入论文正文结论。

## 2026-07-14：G2-04-FULLTEXT-PACKET 物理竞赛试题研究全文获取包

- 新增 `02_literature/physics_competition_fulltext_request_packet.md`，整理PCOMP-001至PCOMP-005的全文获取优先级、图书馆/导师请求文本、获取后阅读记录模板和写作边界；
- 新增 `02_literature/physics_competition_screening_matrix.csv`，为物理竞赛试题研究候选文献建立筛选决策、综述角色、待提取字段和写作边界；
- 更新 `02_literature/physics_competition_review_prep.md`，将后续动作指向全文获取包和筛选矩阵；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，明确 `G2-04` 仍为进行中，当前尚未获得全文或完成正式综述。

## 2026-07-14：G2-04-PREP 物理竞赛试题研究综述准备

- 新增 `02_literature/physics_competition_review_prep.md`，记录物理竞赛试题研究的阶段性检索范围、候选文献、实践材料排除边界、初步综述结构和全文获取清单；
- 更新 `02_literature/search_log.csv`，新增5条G2-04实际定位记录，覆盖预赛卷量化分析、复赛SOLO研究、竞赛试题整体研究、核心素养视角和复赛单题赏析线索；
- 更新 `02_literature/reference_verification.csv`，新增 `PCOMP-001` 至 `PCOMP-004` 作为候选来源；当前均未获全文，不可转述结论；
- 更新 `02_literature/literature_matrix.csv`，新增 `LM-PCOMP-001` 至 `LM-PCOMP-004`，以“全文待读”状态登记研究问题、样本和方法待核字段；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，将 `G2-04` 标为进行中；本轮不完成正式综述，不写入论文正文结论。

## 2026-07-14：G2-03B-FULLTEXT-PACKET SOLO全文获取请求包

- 新增 `02_literature/solo_fulltext_request_packet.md`，整理Biggs与Collis 1982年SOLO原书和1989年SOLO课程开发/评价论文的全文获取请求清单；
- 写入可直接发送给图书馆/馆际互借和导师的请求文本，并附获取后阅读记录模板、重点摘录问题和正文写作边界；
- 更新 `02_literature/solo_fulltext_access_audit.md`，将后续动作指向请求包；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，明确该任务只完成全文获取准备，不代表已获得全文、阅读全文或完成SOLO理论定稿；
- `G2-03` 仍为进行中；等待全文期间可并行启动 `G2-04` 物理竞赛试题研究综述准备。

## 2026-07-14：G2-03B-ACCESS SOLO全文获取审计

- 新增 `02_literature/solo_fulltext_access_audit.md`，记录SOLO原书与1989年SOLO课程开发/评价论文的公开全文获取情况；
- 更新 `02_literature/search_log.csv`，新增两条全文获取审计记录，说明未发现稳定公开全文或全文需访问权限；
- 更新 `02_literature/reference_verification.csv`，将 `SOLO-001` 与 `SOLO-002` 的全文状态改为需图书馆、出版社授权访问或学校数据库补齐；
- 更新 `02_literature/solo_taxonomy_source_verification.md` 和 `08_manuscript/02_theory.md`，明确当前只能使用“SOLO启发”这一保守表述，不能写成全文已读或理论定稿；
- `G2-03` 仍为进行中，下一步为 `G2-03B-FULLTEXT` 合法全文获取与关键页码摘录。

## 2026-07-14：G2-03A SOLO理论来源阶段性核验

- 新增 `02_literature/solo_taxonomy_source_verification.md`，记录SOLO理论来源的阶段性核验结果与后续全文阅读要求；
- 更新 `02_literature/reference_verification.csv`，新增 `SOLO-001` 和 `SOLO-002`，分别记录Biggs与Collis 1982年SOLO原书和1989年SOLO用于课程开发与评价论文的出版信息；
- 更新 `02_literature/literature_matrix.csv` 与 `02_literature/search_log.csv`，登记SOLO来源定位、摘要/简介层面的阶段性判断和全文待读边界；
- 更新 `02_literature/references.bib`，新增 `biggs1982solo` 与 `biggs1989solo`，并标注正式引用前仍需补全文阅读页码；
- 更新 `09_quality/claim_evidence_matrix.csv`，新增 `C2-03A`，明确本研究只能表述为“SOLO启发的任务认知结构要求等级”；
- 更新 `08_manuscript/02_theory.md` 的2.2节，避免将试题编码直接写成学生学习结果等级；`G2-03` 仍未完成，后续需补原书全文阅读和任务/试题分析争议文献。

## 2026-07-14：G2-02 课程标准中科学思维定义核验

- 核验教育部官方通知页 `教育部关于印发普通高中课程方案和语文等学科课程标准（2017年版2020年修订）的通知`，定位附件包中的 `普通高中物理课程标准（2017年版2020年修订）.pdf`；
- 新增 `02_literature/curriculum_standard_verification.md`，记录官方发布页、发文字号、附件、SHA-256、PDF页码和正文页码；
- 更新 `02_literature/reference_verification.csv` 与 `02_literature/literature_matrix.csv`，新增课程标准官方来源记录 `CS-001` 与 `LM-CS-001`；
- 更新 `02_literature/search_log.csv`，新增一条G2-02实际核验记录；更新 `02_literature/references.bib`，加入 `moe2020physicscurriculum`；
- 更新 `09_quality/claim_evidence_matrix.csv`，新增 `C2-01`，说明科学思维四维度的课程标准依据与边界；
- 更新 `08_manuscript/02_theory.md`，将2.1中四维度的官方依据由待补改为已登记来源；当前仍需补充SOLO理论、科学思维测评、内容分析方法和专家审查证据。

## 2026-07-14：G2-01 文献数据库与检索式制定

- 新增 `02_literature/search_strategy_g2_01.md`，制定第二章文献核验的数据库/来源组、主题块检索式、纳入排除标准、记录规则和完成判据；
- 更新 `02_literature/search_log.csv`，登记14条计划检索式，覆盖课程标准、科学思维测评、SOLO理论、SOLO任务分析边界、物理竞赛试题研究、内容分析与评分者一致性、教学转化与设计型研究；
- 明确本轮记录均为计划检索式，结果数为“待检索”，筛选数和纳入数为0，不代表已完成真实检索、文献筛选、全文阅读或引用核验；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，将 `G2-01` 标为完成，下一步调整为 `G2-02` 课程标准中科学思维定义核验。

## 2026-07-14：G7-04-PREP 第二章文献与理论核验式草稿

- 更新 `08_manuscript/02_theory.md`，将空章节扩展为第二章核验式理论草稿；
- 写入科学思维四维度的暂定操作化方向，并明确该划分仍需课程标准和科学思维研究文献核验；
- 写入SOLO理论的使用边界，强调本研究分析的是试题任务认知结构要求，不直接测量学生真实学习结果；
- 写入小问级“两层编码”逻辑、维度与等级结构、正式使用条件和理论框架图；
- 新增 `02_literature/literature_review_workplan.md`，列出第二章待核验主题块、核验流程、主张编号和禁止事项；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，将 `G7-04` 与 `G2-01` 标为进行中；第二章仍需文献检索、全文阅读和引用核验后才能定稿。

## 2026-07-14：G7-03-PREP 第五章案例机制与教学诊断预备稿

- 更新 `08_manuscript/05_cases_and_diagnosis.md`，将空章节扩展为第五章内部预备稿；
- 写入案例选择原则、内部候选案例池和案例进入正式正文的最低证据条件；
- 基于 `batch10_typical_case_candidates.csv` 和已整理题干/解答文本，列出 CPHO35-Q08-4、CPHO36-Q07-4/5、CPHO39-Q05-3/4、CPHO42-Q07-3 等候选案例及其边界；
- 写入模型建构、科学推理、科学论证和质疑创新四类案例分析路径，并明确候选案例不能替代正式双评分者编码、分歧裁决和人工校对销项；
- 写入教师/学生困难证据缺口和教学错位诊断框架，明确当前不得书写真实教师观点、学生困难分布、课堂可行性或教学效果；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，将 `G7-03` 标为进行中；第五章仍需正式编码、案例裁决、案例证据表和真实教师或课堂证据后才能定稿。

## 2026-07-14：G4-01-PREP评分者交接检查与第三、四章草稿启动

- 新增 `07_analysis/scripts/build_g4_01_prep_handoff.py`，检查评分者交接包是否具备最低条件；
- 新增 `g4_01_prep_rater_package_index.csv`、`g4_01_prep_handoff_audit.csv` 和 `g4_01_prep_handoff_report.md`，确认评分者A/B模板和裁决模板均为876条记录，可进入评分者交接准备，但不能进入正式结果分析；
- 更新 `08_manuscript/03_methods.md`，写入研究设计、语料来源、分析单位、编码手册、专家审查边界、试编码与一致性准备、正式编码流程、教师/课堂研究设计和质量控制；
- 更新 `08_manuscript/04_results.md`，写入内部预演版语料特征、维度分布、等级分布、共现模式、分组比较占位、结果稳健性与边界；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，将 `G4-01-PREP` 标为完成，并将 `G7-01`、`G7-02` 标为进行中；第三、四章仍需正式编码结果后定稿。

## 2026-07-14：G4-00W1—G4-00Y10 正式编码前30项准备任务

- 新增 `07_analysis/scripts/build_formal_coding_prep30_outputs.py`，一键生成正式编码前30项准备输出；
- 新增 `prep30_combined_review_master.csv`、`prep30_gate_register.csv`、`prep30_manual_priority_queue.csv`、`prep30_evidence_strengthening_master.csv`、`prep30_l4_review_master.csv`、`prep30_innovation_review_master.csv` 和 `prep30_confidence_review_master.csv`，汇总P0/P1建议、门槛、校对、证据、L4、质疑创新和把握度风险；
- 新增 `07_analysis/data/formal_coding_rater_A_template.csv`、`formal_coding_rater_B_template.csv` 和 `formal_adjudication_template.csv`，作为真实评分者独立编码和后续裁决的空白模板；
- 新增 `prep30_rater_briefing.md`、`prep30_adjudication_protocol.md`、`prep30_version_route.csv`、`prep30_rater_handoff_checklist.csv`、`prep30_formal_coding_field_validation.csv` 和 `prep30_disagreement_type_schema.csv`，用于评分者交接、版本控制、字段校验和分歧裁决准备；
- 新增 `prep30_formal_output_placeholders.csv`、`prep30_claim_evidence_placeholders.csv`、`prep30_final_figure_table_placeholders.csv`、`prep30_manuscript_gate_table.csv`、`prep30_results_chapter_placeholder.md` 和 `prep30_teaching_evidence_gate.csv`，明确正式结果、图表、主张证据、结果章和教学转化仍需等待正式编码与真实证据；
- 新增 `prep30_archive_manifest.csv`、`prep30_next_task_route.csv`、`prep30_analysis_readiness_report.md` 和 `prep30_completion_report.md`，记录归档、下轮任务、准备度和30项完成情况；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，将 `G4-00W1`—`G4-00Y10` 标为完成，并将下一步调整为 `G4-01-PREP` 评分者交接检查。

## 2026-07-14：G4-00V1—G4-00V10 P1内部复核建议

- 新增 `07_analysis/scripts/build_p1_internal_review_outputs.py`，对P1优先记录生成内部复核建议；
- 新增 `07_analysis/results/reviewed/p1_internal_review_log.csv`，形成176条P1记录的建议版复核日志；
- 新增 `p1_internal_revision_suggestions.csv`、`p1_l4_boundary_checklist.csv`、`p1_confidence_review_queue.csv` 和 `p1_manual_issue_linkage.csv`，分别记录P1修订建议、L4边界复核、中等把握度队列和人工校对联动；
- 新增 `p1_internal_candidate_overlay.csv`、`p1_internal_impact_preview.csv`、`p1_item_review_summary.csv` 和 `p1_next_gate_plan.csv`，用于候选表覆盖、影响预演、题目汇总和后续门槛规划；
- 新增 `p1_internal_review_report.md`，汇总P1范围、建议类型和正式边界；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，将 `G4-00V1`—`G4-00V10` 标为完成，并保留 `G4-01`、`G4-02` 等正式任务未完成。

## 2026-07-14：G4-00U1—G4-00U10 P0内部复核建议

- 新增 `07_analysis/scripts/build_p0_internal_review_outputs.py`，对P0优先记录生成内部复核建议；
- 新增 `07_analysis/results/reviewed/p0_internal_review_log.csv`，形成120条P0记录的建议版复核日志；
- 新增 `07_analysis/results/reviewed/p0_internal_revision_suggestions.csv`，记录P0记录的建议保留、证据补强、待核实或后续P1复核建议；
- 新增 `07_analysis/results/reviewed/p0_internal_candidate_overlay.csv`，在内部候选表上叠加P0建议字段；
- 新增 `p0_internal_impact_preview.csv`、`p0_evidence_strengthening_checklist.csv`、`p0_item_review_summary.csv` 和 `p0_next_p1_review_plan.csv`，分别用于影响预演、证据补强、题目汇总和下一轮P1计划；
- 新增 `p0_internal_review_report.md`，汇总P0范围、建议类型和正式边界；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，将 `G4-00U1`—`G4-00U10` 标为完成，并保留 `G4-01`、`G4-02` 等正式任务未完成。

## 2026-07-14：G4-00T1—G4-00T10 后续10项内部预演任务

- 新增 `07_analysis/scripts/build_internal_batch10_outputs.py`，一键生成后续10项内部预演输出；
- 新增 `07_analysis/results/reviewed/batch10_preformal_review_triage.csv`，对296条样本复核记录进行优先级分流；
- 新增 `07_analysis/results/reviewed/batch10_formal_readiness_map.csv`，说明正式双人编码、分歧裁决和正式唯一分析表当前仍受阻塞；
- 新增 `07_analysis/data/internal_analysis_candidate_v0.csv`，形成876条内部分析候选记录，并保留风险标记；
- 新增 `batch10_internal_overall_presence.csv`、`batch10_internal_level_distribution.csv`、`batch10_internal_cooccurrence.csv` 和 `batch10_internal_group_comparisons.csv`，生成内部描述统计、等级分布、维度共现和分组比较预演；
- 新增 `batch10_typical_case_candidates.csv`，整理30个典型试题案例候选；
- 新增 `batch10_internal_boundary_memo.md`，说明内部预演结果的稳健性风险和正式使用前置条件；
- 新增 `batch10_teaching_transfer_seed_matrix.csv`，形成4条教学转化种子矩阵；
- 新增 `batch10_completion_report.md`，记录10项内部任务完成情况和正式任务仍未完成的边界；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，将 `G4-00T1`—`G4-00T10` 标为完成，并保留 `G4-00T-REVIEW`、`G4-01` 和 `G4-02` 等正式任务未完成。

## 2026-07-14：G4-00F/G4-00S 正式编码前复核样本包与记录表

- 新增 `07_analysis/scripts/build_preformal_review_packet.py`，依据内部质量问题清单自动抽取正式编码前复核样本；
- 新增 `07_analysis/results/reviewed/preformal_review_sample_items.csv`，形成74个分析单元的复核样本表，覆盖第35—42届并优先纳入质疑创新、证据薄弱、L4、人工校对未销项和中等把握度记录；
- 新增 `07_analysis/results/reviewed/preformal_review_coding_records.csv`，整理样本对应的296条四维度内部编码记录；
- 新增 `07_analysis/results/reviewed/preformal_review_manual_issues.csv`，整理样本关联的99条人工校对问题；
- 新增 `07_analysis/results/reviewed/preformal_review_packet.md`，说明样本包性质、输入输出、分届覆盖、风险覆盖、复核流程和禁止事项；
- 新增 `07_analysis/scripts/build_preformal_review_log.py`、`preformal_review_log.csv` 和 `preformal_review_log_protocol.md`，建立296条复核记录空表；所有记录均为待复核，不代表完成校对、修订或裁决；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，将 `G4-00F` 与 `G4-00S` 标为完成，并将下一步调整为 `G4-00T` 样本包逐条复核记录。

## 2026-07-14：G4-00R 内部编码数据质量检查

- 新增 `07_analysis/scripts/audit_internal_coding_quality.py`，对内部分析底稿执行字段、维度、存在性、等级、把握度、证据文本和人工校对关联检查；
- 新增 `07_analysis/results/reviewed/internal_coding_quality_issues.csv`，形成正式编码前问题清单；
- 新增 `07_analysis/results/reviewed/internal_coding_quality_report.md`，汇总结构性致命问题、高优先级风险、编码把握度、L4边界、质疑创新保守复核和内部维度分布预警；
- 检查结果显示结构性致命问题为0，但源试编码仍来自 `coding_manual_v1`，且全部分析单元均关联未销项校对风险；当前结果仍不得写入论文正式结果；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，将 `G4-00R` 标为完成，并将下一步调整为 `G4-00F` 正式编码前复核样本包。

## 2026-07-14：G3-08I/G4-00I 内部版V2冻结与描述分析准备

- 新增 `04_framework/coding_manual_v2_internal.md`，将编码手册V2草案冻结为内部分析准备版本，并明确其不能替代真实专家审查、导师确认、真实双评分者一致性检验或正式编码手册；
- 新增 `04_framework/codebook_v2_internal.csv`，将16个维度-等级指标标记为 `V2内部冻结-仅限内部分析`；
- 新增 `07_analysis/data/internal_coding_v1.csv`，把219个分析单元的小问级元数据与876条 Codex 试编码合并为内部分析底稿；
- 新增 `07_analysis/scripts/build_internal_descriptive_tables.py`，可复现生成内部描述统计预演表和内部说明；
- 新增 `07_analysis/results/reviewed/internal_descriptive_summary.md`，记录数据范围、预演表、致命边界和下一步最小任务；
- 更新 `PROJECT_STATUS.md` 和 `TASKS.md`，将 `G3-08I` 与 `G4-00I` 标为完成，同时保留 `G3-08` 正式编码手册冻结和正式 `G4` 分析为未完成。

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
