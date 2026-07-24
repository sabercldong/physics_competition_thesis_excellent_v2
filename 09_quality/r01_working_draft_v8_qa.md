# R01 Word 工作稿 V8 QA

- 交付：`10_outputs/drafts/ECNU_非全日制专硕论文工作稿_R01_v8.docx`；输入：同名 `inputs.json`。
- 候选文献生成器：10项；候选清单QA：6/6通过。
- 引文追溯：41条来源出现、35处显式占位；候选来源均有BibTeX键。
- DOCX：`unzip -t` 通过；`python-docx` 已断言V8版本号、ST-009参考文献和正文来源文本均存在。
- 限制：仅为非提交工作稿。QuickLook中文预览的V7检查仍适用；LibreOffice环境缺少CJK字体，不能替代实际Word环境的逐页排版终验。
