# R01 Word 工作稿 V5 QA

## 范围

- 交付：`10_outputs/drafts/ECNU_非全日制专硕论文工作稿_R01_v5.docx`
- 输入清单：`10_outputs/drafts/ECNU_非全日制专硕论文工作稿_R01_v5_inputs.json`
- 生成日期：2026-07-25
- 定位：仅为非提交工作稿；不得作为匿名送审、答辩、归档或最终提交文件。

## 检查结果

| 检查 | 方法 | 结果 | 结论 |
|---|---|---|---|
| DOCX 容器 | `unzip -t` | 通过，无压缩包错误 | 通过 |
| 输入追溯 | V5 inputs manifest | 六章、摘要、图件和候选参考文献输入均已记录SHA-256 | 通过 |
| 候选参考文献 | 读取生成后的第22页文本 | 7项，含 METH-006；仍明示少于30篇 | 通过 |
| LibreOffice 渲染 | `render_docx.py` 生成23页PNG | 文本可渲染，但环境缺少可用中文字体，中文显示为方框 | 不可作为中文排版验收 |
| macOS QuickLook | 原生缩略图预览 | 中文封面、摘要、V5版本号和日期均可显示 | 通过（原生预览抽查） |

## 结论

V5 的容器、输入追溯、候选参考文献和原生中文预览均已核对。LibreOffice 渲染不能用于中文字体与逐页排版终验，原因是运行环境缺少可用CJK字体；最终提交前仍须在实际 Word/提交环境逐页核验。该限制不影响本工作稿作为材料组织版本的用途。

## 复跑

```bash
BUNDLED_PY=/Users/dongxingxi/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
$BUNDLED_PY 10_outputs/drafts/build_r01_working_draft.py
unzip -t 10_outputs/drafts/ECNU_非全日制专硕论文工作稿_R01_v5.docx
```
