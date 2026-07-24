# R01 非提交工作稿 V16 QA

## 范围

本检查覆盖 `G2-05-READ-ST018 + G8-02-ST018-WORKING-DRAFT-INTEGRATION` 生成的 `10_outputs/drafts/ECNU_非全日制专硕论文工作稿_R01_v16.docx`。V16为材料整合工作稿，不是提交版、匿名送审版或学校格式终验版。

## 输入与追溯

- 输入清单：`10_outputs/drafts/ECNU_非全日制专硕论文工作稿_R01_v16_inputs.json`。
- 候选来源为20项；`build_r01_candidate_references.py`与`validate_r01_candidate_references.py`均通过，后者为6/6。
- `audit_r01_citation_trace.py`检出51条来源ID出现、45处显式引文占位；`ST-018`有候选映射和BibTeX键`docktor2016maps`。

## 文本与容器检查

| 检查项 | 结果 | 结论 |
|---|---|---|
| DOCX容器 | `unzip -t`检查全部文件OK | 通过 |
| 第五章受限段落 | PDF文本在第21页检出`ST-018`及外部量规、学生样本和效度结论不迁移限制 | 通过 |
| 参考文献条目 | PDF文本在第24页检出Docktor等条目 | 通过 |
| 页面规格 | PDF为25页，595.304 x 841.89 pt（A4） | 通过 |
| 中文渲染 | LibreOffice环境缺少可用CJK字体，中文仍呈方框 | 不作为中文排版终验 |

## 受限使用核对

`ST-018`只支持未来真实学生书面作答的条件性评价设计，并要求其与当前试题任务要求编码分开。V16不采用MAPS量规，不迁移大学样本、学生作答、访谈、评分、效度、信度、统计量或教学结论；也不将该段写作当前学生能力、困难或教学有效性的证据。

## 复跑命令

```bash
python3 07_analysis/scripts/build_r01_candidate_references.py
python3 07_analysis/scripts/validate_r01_candidate_references.py
python3 07_analysis/scripts/audit_r01_citation_trace.py
python3 10_outputs/drafts/build_r01_working_draft.py
unzip -t 10_outputs/drafts/ECNU_非全日制专硕论文工作稿_R01_v16.docx
```
