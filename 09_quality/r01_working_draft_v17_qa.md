# R01 非提交工作稿 V17 QA

## 范围

本检查覆盖 `G2-04-READ-EXAM001 + G8-02-EXAM001-WORKING-DRAFT-INTEGRATION` 生成的 `10_outputs/drafts/ECNU_非全日制专硕论文工作稿_R01_v17.docx`。V17为材料整合工作稿，不是提交版、匿名送审版或学校格式终验版。

## 输入与追溯

- 输入清单：`10_outputs/drafts/ECNU_非全日制专硕论文工作稿_R01_v17_inputs.json`。
- 候选来源为21项；`build_r01_candidate_references.py`与`validate_r01_candidate_references.py`均通过，后者为6/6。
- `audit_r01_citation_trace.py`检出52条来源ID出现、46处显式引文占位；`METH-008`有候选映射和BibTeX键`yu2024physicsconsistency`。

## 文本与容器检查

| 检查项 | 结果 | 结论 |
|---|---|---|
| DOCX容器 | `unzip -t`检查全部文件OK | 通过 |
| 第三章受限段落 | DOCX XML检出`METH-008`，并保留SEC模型、高考数据和命题结论不迁移的限制 | 通过 |
| 参考文献条目 | DOCX XML检出于海波等（2024）条目 | 通过 |
| 页面规格 | LibreOffice结构性转换PDF为25页、595.304 x 841.89 pt（A4） | 通过 |
| 中文渲染 | 当前LibreOffice环境缺少可用CJK字体，中文仍不作为逐页排版终验 | 不放行中文排版 |

## 受限使用核对

`METH-008`只支持中国物理考试文本分析应公开样本、分析维度、拆分规则、编码示例和汇总方式。V17不采用SEC模型、四级认知水平定义、高考25套试卷、Porter系数、趋势或命题建议；也不将该来源写作竞赛研究、学生能力、教学效果或本项目编码效度证据。

## 输入新鲜度复核

`validate_working_draft_freshness.py`将V17输入清单中的8项SHA-256与当前摘要、六章源文件和候选参考文献逐项比较，结果为8/8当前。该结论只表示V17仍对应当前输入文件，不评价这些输入的学术质量，也不替代中文逐页排版终验。

## 复跑命令

```bash
python3 07_analysis/scripts/build_r01_candidate_references.py
python3 07_analysis/scripts/validate_r01_candidate_references.py
python3 07_analysis/scripts/audit_r01_citation_trace.py
python3 10_outputs/drafts/build_r01_working_draft.py
python3 07_analysis/scripts/validate_working_draft_freshness.py --require-current
unzip -t 10_outputs/drafts/ECNU_非全日制专硕论文工作稿_R01_v17.docx
```
