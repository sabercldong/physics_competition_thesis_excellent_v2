# R01 Word 工作稿 V6 QA

## 范围

- 交付：`10_outputs/drafts/ECNU_非全日制专硕论文工作稿_R01_v6.docx`
- 输入清单：`10_outputs/drafts/ECNU_非全日制专硕论文工作稿_R01_v6_inputs.json`
- 生成日期：2026-07-25
- 定位：仅为非提交工作稿；不得作为匿名送审、答辩、归档或最终提交文件。

## 检查结果

| 检查 | 方法 | 结果 | 结论 |
|---|---|---|---|
| DOCX容器 | `unzip -t` | 通过，无压缩包错误 | 通过 |
| 输入追溯 | V6 inputs manifest | 六章、摘要、图件和候选参考文献输入均已记录SHA-256 | 通过 |
| 候选参考文献 | 候选生成器与QA | 8项，新增ST-007；仍明示少于30篇 | 通过 |
| 引用追溯 | `audit_r01_citation_trace.py` | 39条来源出现、33处显式占位；候选来源均有BibTeX键 | 通过 |
| macOS QuickLook | 原生缩略图预览 | 中文封面、摘要、V6版本号和日期均可显示 | 通过（原生首页抽查） |
| LibreOffice渲染 | 沿用V5环境诊断 | 环境缺少可用CJK字体，中文显示为方框 | 不可作为中文逐页排版验收 |

## 结论

V6的容器、输入追溯、候选参考文献和原生中文首页预览均已核对。它同步纳入第五章新增的ST-007受限引文占位与8项候选参考文献。最终提交前仍须在实际Word/提交环境逐页核对字体、目录、分页、学校专硕封皮、签名页、匿名处理和参考文献格式。

## 复跑

```bash
BUNDLED_PY=/Users/dongxingxi/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
$BUNDLED_PY 10_outputs/drafts/build_r01_working_draft.py
unzip -t 10_outputs/drafts/ECNU_非全日制专硕论文工作稿_R01_v6.docx
$BUNDLED_PY 07_analysis/scripts/validate_r01_candidate_references.py
$BUNDLED_PY 07_analysis/scripts/audit_r01_citation_trace.py
```
