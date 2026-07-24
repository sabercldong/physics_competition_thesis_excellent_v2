# R01 非提交工作稿 V13 QA

## 范围

本检查覆盖 `G8-02-ST016-WORKING-DRAFT-INTEGRATION` 生成的 `10_outputs/drafts/ECNU_非全日制专硕论文工作稿_R01_v13.docx`。V13 是材料整合工作稿，不是提交版、匿名送审版或学校格式终验版。

## 输入与追溯

- 输入清单：`10_outputs/drafts/ECNU_非全日制专硕论文工作稿_R01_v13_inputs.json`。
- 清单记录六章、摘要草稿和候选参考文献的 SHA-256；其中第五章 SHA-256 为 `52f6118d23df3253b5b3868d3e7426985c1596796fe5b2c47a5e9d2a16456655`。
- 候选来源为 16 项；`build_r01_candidate_references.py` 和 `validate_r01_candidate_references.py` 均通过，后者为 6/6。
- `audit_r01_citation_trace.py` 检出 47 条来源 ID 出现、41 处显式引文占位；`ST-016` 已有候选映射和 BibTeX 键 `linsingh2015scaffolding`。

## 文本与容器检查

| 检查项 | 结果 | 结论 |
|---|---|---|
| DOCX 容器 | `unzip -t` 检查全部文件 OK | 通过 |
| 第五章受限段落 | PDF 文本可检出“独立尝试”“预测—核对—比较—说明”及 `ST-016` | 通过 |
| 参考文献条目 | PDF 文本可检出 `[16] Lin S-Y, Singh C.` | 通过 |
| 页面规格 | PDF 为 25 页，595.304 x 841.89 pt（A4） | 通过 |
| 中文渲染 | LibreOffice 环境缺少可用 CJK 字体，中文仍呈方框 | 不作为中文排版终验 |

## 受限使用核对

`ST-016` 仅支持第五章把独立尝试、预测/核对、相邻情境比较和条件说明组织为可收集的任务步骤。V13 未迁移其大学样本、摩擦/张力题、课堂比较、统计量、评分量规或教学效果；也不将该段写成对本项目学生困难或教学有效性的证据。

## 复跑命令

```bash
python3 07_analysis/scripts/build_r01_candidate_references.py
python3 07_analysis/scripts/validate_r01_candidate_references.py
python3 07_analysis/scripts/audit_r01_citation_trace.py
python3 10_outputs/drafts/build_r01_working_draft.py
unzip -t 10_outputs/drafts/ECNU_非全日制专硕论文工作稿_R01_v13.docx
```
