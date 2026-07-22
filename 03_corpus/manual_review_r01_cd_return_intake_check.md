# G1-07-R01-CD-RETURN-INTAKE R01 C/D组人工回填接收检查

接收日期：2026-07-22

## C组：接收通过，待整合QA

R01 C组原件覆盖47行（099-145）。与C组空白包相比，33项不可变字段无差异；9个组别必填字段均完整；47项决定均为允许值“通过无需修订”；141条项目内证据路径均存在。原件保留为UTF-8 BOM与CRLF，另存LF登记副本。

| 文件 | 路径 | SHA-256 |
|---|---|---|
| 原件 | `03_corpus/manual_review_returns/incoming/REMAINING-C/return_20260722_C_R01_filled.csv` | `9422e41785e66a48e63c2f190b72bac811cd775ce6567266328d13ec26b30435` |
| LF登记副本 | `03_corpus/manual_review_returns/registered/REMAINING-C/return_20260722_C_R01_filled_registered_lf.csv` | `67a505c0950624facf25e4b832a1d087a98b8a33580d5460076b67396d12ec4a` |

范围限制：R01仅明确`CPHO41-Q02`与`CPHO40-Q03`为视觉API抽查，不扩展为47项均逐图视觉核验。C组未销项、未放行论文图件或正式结果，待`G1-07-R01-C-RETURN-INTEGRATION-QA`。

## D组：原件隔离，需更正后重交

D组原件已字节保留，但未通过接收检查，不能登记为“全部通过”。9行均填写“通过无需修订”，而D组允许决定要求使用逐行完整表述。更关键的是，8项第35届分值问题的关闭门槛是“正式评分细则或原卷分值说明”，当前仅填写答案页范围，不能构成分值来源；第42届第3题SOLFIG也需使用其专用允许决定。

| 文件 | 路径 | SHA-256 |
|---|---|---|
| 隔离原件 | `03_corpus/manual_review_returns/quarantine/REMAINING-D/return_20260722_D_R01_filled.csv` | `d2885f660926427da48f0a668de0b8957a26ae3f652db2f04ac441d594eaa24c` |

更正规则：8项分值行如未实际获得正式评分细则或原卷分值说明，应选择“待核实：当前PDF仍未明示分值”；如已获得，应填写“通过：获得正式评分细则或原卷分值说明”，并在证据字段写来源文件、页码和实际分值。SOLFIG行应从本行允许选项中选择，并写清题面图与题解图的边界说明。不得覆盖该隔离原件；请另交修订副本。
