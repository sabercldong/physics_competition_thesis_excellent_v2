# R01 Word 工作稿 V9 QA

- 交付：`10_outputs/drafts/ECNU_非全日制专硕论文工作稿_R01_v9.docx`；输入：同名 `inputs.json`。
- 候选文献生成器：11项；候选清单QA：6/6通过。
- 引文追溯：42条来源出现、36处显式占位；11项候选来源均有BibTeX键。
- DOCX：`unzip -t`通过；`python-docx`已断言V9版本号、ST-010候选文献、第五章ST-010来源段落及输入清单哈希均存在。
- 限制：仅为非提交工作稿。既有QuickLook中文预览结论可作为结构性参考；当前LibreOffice运行时缺少CJK字体，不能替代实际Word环境的逐页中文排版终验。
