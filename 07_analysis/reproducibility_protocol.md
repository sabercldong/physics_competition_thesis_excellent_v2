# R01 当前冻结材料包复现协议

本协议对应当前冻结编码表 `07_analysis/data/final_coding_r01_correction_v1.csv`（219个分析单元、876条四维记录）。它规定如何复建或核验项目内的证据链、描述统计、案例、引用链和非提交工作稿；不验证评分者身份、独立性或实际人工过程。

## 输入与输出边界

- 冻结编码、登记回填、补证与更正裁决保留在 `07_analysis/data/` 与 `07_analysis/results/formal_rater_r01/`；脚本输出只能回写其指定路径。
- 正文组装输入为中英文摘要内容底稿、`08_manuscript/01_introduction.md` 至 `06_conclusion.md`，以及候选参考文献 `08_manuscript/07_candidate_references.md`。
- V17 Word 文件只是非提交工作稿。它不包含真实个人信息、封皮、签名、匿名送审处理或当期学院格式终验。
- 所有复现输出只描述试题与参考解答呈现的任务认知要求，不得外推为学生能力、教学效果、因果、显著性、长期趋势或第35届分值差异。

## 推荐运行顺序

在项目根目录运行：

```bash
# 1. 重建当前编码—证据链（仅在需从登记回填重新生成时运行）
python3 07_analysis/scripts/build_r01_current_evidence_chain.py \
  --repair-v1 07_analysis/data/rater_returns/incoming/R01/r01_evidence_repair_R01_FILLED_20260723.csv \
  --repair-v2 07_analysis/data/rater_returns/incoming/R01/r01_evidence_repair_R01_FILLED_20260723_V2.csv \
  --registered-repair-v2 07_analysis/data/rater_returns/registered/R01/r01_evidence_repair_R01_FILLED_20260723_V2_registered_lf.csv \
  --output 07_analysis/data/final_coding_evidence_r01_v1.csv \
  --qa-output 07_analysis/results/formal_rater_r01/r01_current_evidence_chain_qa_v1.csv \
  --force

# 2. 核验结果、案例与引用链
python3 07_analysis/scripts/validate_r01_results_eligibility.py
python3 07_analysis/scripts/validate_r01_results_manuscript_integration_v2.py
python3 07_analysis/scripts/validate_r01_conclusion_rq_alignment.py
python3 07_analysis/scripts/validate_r01_abstract_alignment.py
python3 07_analysis/scripts/audit_r01_current_chapter_evidence.py
python3 07_analysis/scripts/validate_r01_teaching_design_materials.py
python3 07_analysis/scripts/validate_r01_student_artifact_observation_rubric.py
python3 07_analysis/scripts/validate_r01_g3_framework_lifecycle_reconciliation.py
python3 07_analysis/scripts/build_r01_case_reselection.py
python3 07_analysis/scripts/validate_r01_case_reselection.py
python3 07_analysis/scripts/build_r01_candidate_references.py
python3 07_analysis/scripts/validate_r01_candidate_references.py
python3 07_analysis/scripts/audit_r01_citation_trace.py

# 3. 重建非提交工作稿并检查输入新鲜度
python3 10_outputs/drafts/build_r01_working_draft.py
python3 07_analysis/scripts/validate_working_draft_freshness.py --require-current

# 4. 核验材料包快照、总状态与运行手册入口
python3 07_analysis/scripts/build_r01_material_package_snapshot.py --validate
python3 07_analysis/scripts/build_r01_internal_material_package.py --force
python3 07_analysis/scripts/build_r01_internal_material_package.py --validate
python3 07_analysis/scripts/validate_current_material_package_audit.py
python3 07_analysis/scripts/validate_r01_reproducibility_runbook.py
python3 07_analysis/scripts/validate_r01_full_package_healthcheck.py
```

## 当前预期状态

- 当前编码与证据链：876条记录；证据链由840条V6来源、32条V2补证和4条ADJ-02更正来源组成。
- 结果资格QA：51/51通过；第四章当前结果整合QA：35/35通过；结论章对齐QA：16/16通过；案例重选QA：7/7通过。
- 中英文摘要对齐QA：28/28通过；它只核验两份摘要内容底稿与冻结结果和边界的一致性，学校格式与官方英文赛事名仍待定稿。
- 候选参考文献QA：7/7通过；当前候选来源36项；引用追溯为72条来源出现、61处显式占位。新增的4项SOLO相邻应用与5项国内竞赛研究只用于已登记的受限边界，不替代SOLO原典、不验证本项目框架，也不迁移国内研究的统计、成绩或教学结论。
- 当前章节证据审计：12/12通过；第二章文献闭合与旧主张矩阵版本差异作为侧车事项登记。
- 教学设计材料QA：21/21通过；它只核验矩阵、两套未实施设计材料与R01案例的项目内对应关系，不验证学生/教师参与、课堂实施、量规信效度或教学效果。
- 学生作品过程性观察记录量规QA：12/12通过；它只核验三个案例的观察指标、空白模板和非推断边界，不产生学生数据，也不验证信度、效度或教学效果。
- G3生命周期对账QA：18/18通过；它只区分项目内可复算规则与未闭合的专家/正式冻结边界。
- V17工作稿输入新鲜度：9/9当前；材料包快照：43/43当前；材料包审计：16/16通过。
- 内部非提交交接包：默认42项，不含原始试卷/解答或V17；若需本地携带V17，必须显式使用 `--include-local-draft` 后另行校验。
- 全链路健康检查：16项已有门禁必须同时通过；其结果写入 `09_quality/r01_full_package_healthcheck_v1.csv`。

## 不能由本协议证明的事项

该协议不证明RATER-A/B、ADJ-01/02或R01的身份、互盲、独立性、实际人工操作、框架外部效度、文献最终格式、中文逐页版式、学生作品真实性或人类参与者事实。上述事项只能依靠真实登记材料、学校当期规定与相应的外部审核闭合。
