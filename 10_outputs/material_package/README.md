# R01 当前材料包快照与内部交接入口

`R01_current_material_package_manifest_v1.csv` 是当前非提交材料包的校验清单，不是最终论文提交包。CSV逐项记录文件用途、分发边界与SHA-256。复跑方法见 `07_analysis/reproducibility_protocol.md`；未闭合条件见 `09_quality/current_material_package_audit_v2.md`。

运行 `07_analysis/scripts/build_r01_internal_material_package.py --force` 可生成 `R01_internal_handoff_v1/`：默认复制43项允许内部交接的材料，并保留来源路径和SHA-256；不含原始试卷/解答、受限文献全文、私人数据或V17。该目录只用于项目内部交接和复现，不是公开发布包、匿名送审包、答辩包或正式提交包。

原始试卷与解答的权利状态、学校格式、真实参与者材料和V17工作稿的提交资格均不因本清单而改变。
