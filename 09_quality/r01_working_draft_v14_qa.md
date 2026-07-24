# R01 非提交工作稿 V14 QA

## 范围

本检查覆盖 `G8-02-ST012-ST013-METHODS-INTEGRATION` 生成的 `10_outputs/drafts/ECNU_非全日制专硕论文工作稿_R01_v14.docx`。V14 为材料整合工作稿，不是提交版、匿名送审版或学校格式终验版。

## 输入与追溯

- 输入清单：`10_outputs/drafts/ECNU_非全日制专硕论文工作稿_R01_v14_inputs.json`。
- 候选来源为18项；`build_r01_candidate_references.py` 和 `validate_r01_candidate_references.py` 均通过，后者为6/6。
- `audit_r01_citation_trace.py` 检出49条来源ID出现、43处显式引文占位；`ST-012` 与 `ST-013` 均有候选映射和BibTeX键。

## 文本与容器检查

| 检查项 | 结果 | 结论 |
|---|---|---|
| DOCX容器 | `unzip -t`检查全部文件OK | 通过 |
| 第三章受限段落 | PDF文本在第12页检出`ST-012`、`ST-013`及TIPP/Bloom不迁移限制 | 通过 |
| 参考文献条目 | PDF文本在第23页检出Teodorescu等与Kocakaya、Gonen条目 | 通过 |
| 页面规格 | PDF为25页，595.304 x 841.89 pt（A4） | 通过 |
| 中文渲染 | LibreOffice环境缺少可用CJK字体，中文仍呈方框 | 不作为中文排版终验 |

## 受限使用核对

两条来源只支持公开任务分析的语料范围、单位、判据、示例和分歧处理，并区分题目任务要求与学生实际表现。V14不采用TIPP或Bloom类别，不迁移其样本、比例、卡方、显著性、一致性或教学结论，也不将其写为本项目编码框架、学生能力或教学效果的验证。

## 复跑命令

```bash
python3 07_analysis/scripts/build_r01_candidate_references.py
python3 07_analysis/scripts/validate_r01_candidate_references.py
python3 07_analysis/scripts/audit_r01_citation_trace.py
python3 10_outputs/drafts/build_r01_working_draft.py
unzip -t 10_outputs/drafts/ECNU_非全日制专硕论文工作稿_R01_v14.docx
```
