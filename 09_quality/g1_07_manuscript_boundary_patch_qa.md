# G1-07-MANUSCRIPT-BOUNDARY-PATCH-QA P0正文门禁补丁应用范围检查

更新时间：2026-07-19

## 性质声明

本报告只检查 `G1-07-MANUSCRIPT-BOUNDARY-PATCH-APPLY-SAFE` 中5条P0人工终核门禁句的应用范围和证据边界。本轮不继续改写正文，不应用第五章P1案例句，不修改 `09_quality/claim_evidence_matrix.csv`，不填写真实校对人、真实校对日期、评分者、专家意见、统计结果、教师证据、课堂材料或教学效果。

## QA结论

- 5条P0门禁句均已落入预期位置：第3章2条，第4章3条。
- 第5章P1案例句未被本轮混入。
- `09_quality/claim_evidence_matrix.csv` 未出现本轮应用记录或新增补丁来源字段；该矩阵仍保留历史未提交改动，等待单独任务处理。
- 关键词扫描命中“显著提升”“课堂效果”等高风险词，但均处于“不能写成/不证明”的禁止语境，不构成正式结果声称。
- 本轮没有发现正式结果数字、显著性结论、专家审查完成、教师验证完成或课堂效果成立的新增越界表述。

## 逐项检查摘要

| 检查项 | 文件 | 位置 | 结论 |
|---|---|---|---|
| QA-001 | `08_manuscript/03_methods.md` | 3.2 | 通过：154项有入口但真实人工销项数为0 |
| QA-002 | `08_manuscript/03_methods.md` | 3.6 | 通过：A/B/C/D四组未发生真实人工终核和评分者流程 |
| QA-003 | `08_manuscript/04_results.md` | 章首说明 | 通过：第四章边界来源化 |
| QA-004 | `08_manuscript/04_results.md` | 4.1 | 通过：219个分析单元仅作语料规模说明 |
| QA-005 | `08_manuscript/04_results.md` | 4.6 | 通过：A/B/C/D四组均无真实销项记录 |
| QA-006 | `08_manuscript/05_cases_and_diagnosis.md` | 章首说明 | 通过：P1案例句未应用 |
| QA-007 | `09_quality/claim_evidence_matrix.csv` | 全表 | 通过：主张矩阵未混入本轮补丁来源 |
| QA-008 | `08_manuscript/03_methods.md` | 3.7 | 通过：高风险词处于禁止语境 |
| QA-009 | `08_manuscript/05_cases_and_diagnosis.md` | 5.1/5.8 | 通过：课堂效果词处于禁止语境 |
| QA-010 | `09_quality/g1_07_manuscript_boundary_patch_apply_log.csv` | APPLY-001至APPLY-005 | 通过：应用记录与正文一致 |

## 剩余风险

1. 第3章、第4章、第5章和 `09_quality/claim_evidence_matrix.csv` 仍有历史未提交改动，本轮QA只检查P0补丁，不判定这些历史改动整体可提交。
2. P1补丁尚未应用，包括第五章案例章门禁句和主张矩阵覆盖建议。
3. 真实人工终核、真实A/B评分者编码、分歧裁决和 `final_coding.csv` 仍不存在，因此第4章仍只能是结果占位。

## 下一步最小任务

`G1-07-MANUSCRIPT-BOUNDARY-P1-PLAN`：在P0补丁QA通过后，评估是否需要应用P1补丁。若继续应用，只处理第三章小结、第五章章首、第五章5.1、第五章5.8和主张矩阵覆盖建议；若真实人工回填文件先到，则优先切回真实回填完整性检查。

## 输出文件

- QA报告：`09_quality/g1_07_manuscript_boundary_patch_qa.md`
- QA表：`09_quality/g1_07_manuscript_boundary_patch_qa.csv`
