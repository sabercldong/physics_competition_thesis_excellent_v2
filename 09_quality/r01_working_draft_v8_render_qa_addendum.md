# R01 Word工作稿V8输入与渲染QA补充（2026-07-25）

本文件补充 r01_working_draft_v8_qa.md 的渲染与输入新鲜度结论，不覆盖其历史记录。

## 输入新鲜度

对六章源文件和候选参考文献逐项复算SHA-256后，7项值均与 V8 inputs.json 一致。因此，V8没有因当前源文件滞后而需要重生成V9。

## 结构检查

DOCX容器通过 unzip -t。python-docx 检查确认封面V8标识、非提交说明、第四章、Zwickl参考文献、实际标题“参考文献（候选工作稿）”和个人姓名排除均通过。文档共有250个段落、7张表和4个嵌入图件。

## 原生预览

macOS QuickLook直接预览DOCX首页，中文、封面层级和工作稿标识均可见。

## 渲染尝试与限制

按文档QA流程以LibreOffice渲染出25页A4 PDF及逐页PNG，分页标记有效。但是当前LibreOffice运行时无法绘制中文，PNG出现方框。字体探针显示该问题同时发生于Arial Unicode MS、PingFang SC、Songti SC、Heiti SC和Hiragino Sans GB，故属于当前LibreOffice渲染环境限制，而非V8文本缺失或分页失败。

## 放行结论

V8的源文件追溯、DOCX结构和macOS原生中文首页预览通过。LibreOffice逐页中文视觉渲染不通过，不能作为V8或后续工作稿的中文排版终验。V8继续仅为非提交工作稿，不得替代专硕封皮、签名页、匿名送审件、答辩件或归档件。
