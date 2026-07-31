# R01 内部非提交交接包

本目录由 `07_analysis/scripts/build_r01_internal_material_package.py` 从当前SHA-256快照生成，用于项目内部交接、复现和写作核对；不是公开发布包、匿名送审包、答辩包或学校提交包。

默认不含原始试卷、参考解答、受版权限制的文献全文、可识别个人资料、私人数据或V17 Word工作稿。若以 `--include-local-draft` 显式生成，V17仍只限本地内部使用，禁止作为正式提交或公开分发件。

每个副本都保留其源路径和SHA-256。校验命令：

```bash
python3 07_analysis/scripts/build_r01_internal_material_package.py --validate
```
