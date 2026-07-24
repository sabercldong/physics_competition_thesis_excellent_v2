# 输出目录说明

## 当前可使用的工作稿

`drafts/ECNU_非全日制专硕论文工作稿_R01_v17.docx` 是当前自动生成的六章非提交工作稿。它用于审阅文本组织、表格、图件与26项限边界候选参考文献，并有输入哈希清单与新鲜度QA。

V17不是匿名送审版、答辩版、归档版或正式提交版：它不含真实个人信息、封皮/签名页、当期学院格式终验或中文逐页版式验收。当前环境缺少可用CJK字体，不能以LibreOffice渲染替代Word/WPS中的中文排版检查。

## 可交付材料包

- 冻结编码与证据链：`07_analysis/data/final_coding_r01_correction_v1.csv`、`final_coding_evidence_r01_v1.csv`；
- 描述统计、图件与资格QA：`07_analysis/results/formal_rater_r01/correction_v1/`、`09_quality/r01_results_eligibility_qa_v1.csv`；
- 六章Markdown与候选参考文献：`08_manuscript/`；
- 可复跑命令：`07_analysis/reproducibility_protocol.md`；
- 22项关键文件的SHA-256快照：`material_package/R01_current_material_package_manifest_v1.csv`（复跑前先执行快照校验）；
- 内部非提交交接包：运行 `07_analysis/scripts/build_r01_internal_material_package.py --force` 后生成 `material_package/R01_internal_handoff_v1/`；默认21项，不含原始试卷/解答或V17；
- 当前材料包边界与缺口：`09_quality/current_material_package_audit_v2.md`。

## 最终输出前仍需闭合

学校当期格式、匿名送审与AI披露规则、关键理论/竞赛文献全文、第35届正式分值，以及真实教师/学生/课堂证据（仅在希望主张教学验证时）均未闭合。不得把当前材料包写作最终定稿或教学效果证据。
