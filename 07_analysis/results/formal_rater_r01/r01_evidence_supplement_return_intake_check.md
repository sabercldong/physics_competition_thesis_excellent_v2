# R01 全量证据补正回填接收检查

接收日期：2026-07-23  
任务：`G4-09-R01-EVIDENCE-SUPPLEMENT-RETURN-INTAKE`

## 接收与保存

- 用户提交文件：`/Users/dongxingxi/Desktop/论文人工复核回填/R01/r01_evidence_supplement_R01_FILLED_20260723.csv`
- 原样归档：`07_analysis/data/rater_returns/incoming/R01/r01_evidence_supplement_R01_FILLED_20260723.csv`
- 原件SHA-256：`4fde05648decf0de498c0691b1c28f9cb7dc43c975a1e91c0c2e8f2d1fd4c88d`
- 规范化登记副本：`07_analysis/data/rater_returns/registered/R01/r01_evidence_supplement_R01_FILLED_20260723_registered_lf.csv`
- 登记副本SHA-256：`a37bca6de3a4fd294a9cf63fe270cfcd4cc970d72459c0c50b357072f4d88ee6`
- 原件以只读权限保存；规范化副本仅将CSV换行规范化为UTF-8 BOM与LF。

## 自声明登记

用户声明R01于2026-07-23逐行独立核对题干、参考解答及定位信息，且未将智能体或他人判断冒充为本人结论。本项目仅记录该自声明，不能独立验证实际复核过程。

## 结构检查

`validate_r01_evidence_supplement.py` 的8项字段、记录数、不可变键、工作字段、枚举、逻辑和保持/更正决定检查均通过。

## 内容定位检查

结构通过不等于证据可采纳。全量内容检查结果见 `r01_evidence_supplement_return_content_qa_v1.csv`：

- 876条中有441条题干引语写为“未找到触发语”；
- 686条解答步骤写为“未找到对应步骤”；
- 825条同时填“证据充分”，但至少一侧证据不能在对应整理文本中逐字定位；
- 题干引语和解答步骤分别只有66种、24种去重文本，且存在“题干含论证动词”等非原文标签。

因此，本回填状态为**已接收、结构通过、内容不放行**。它不能解除R01暂定结果门禁，不能恢复第四章正式结论资格，也不能进入第五章案例机制分析。

## 需要的更正

补正回填必须为每行提供实际出现在对应 `item_text_path` 的题干短引文与解答短引文；若确实找不到一侧证据，应将 `evidence_sufficiency` 改为“不足”，而不是“充分”。完成后以新的文件名再次提交；原件保留，不覆盖。为避免通用标签混入，题干引语必须为原文短句，不得使用“题干含论证动词”“条件”等概括词。
