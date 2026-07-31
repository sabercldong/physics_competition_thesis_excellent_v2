# G2-05-ACCESS-REST 科学思维剩余文献访问审计

## 任务范围

本轮审计对象为 `ST-001`、`ST-002` 和 `ST-004`。目标是确认能否通过稳定、可说明来源的渠道进行全文阅读，并更新可写入项目的证据边界。本文件不是正式综述。

## 审计结论

| 编号 | 文献 | 本轮访问结果 | 当前处理 | 正文边界 |
|---|---|---|---|---|
| ST-001 | Lawson (1978), *Journal of Research in Science Teaching* | Wiley DOI/题录线索存在；自动访问 Wiley PDF 返回 403；PubMed 未检出；PER-Central 为题录/引用线索，未获得全文 | 继续全文待读 | 不得转述测验题项结构、信度、效度或开发过程 |
| ST-002 | Bao et al. (2009), *Science* | PubMed 元数据已核验；作者个人站点 PDF 可访问，含 Science 正文与 Supporting Online Material | 已读作者站开放 PDF，纳入部分核验 | 可用于区分内容知识、科学推理测评和试题任务要求；正式引用前需人工对照 Science DOI/SOM 页面 |
| ST-004 | Zhou et al. (2016), *Thinking Skills and Creativity* | ScienceDirect 自动访问返回 403；PubMed XML 摘要与 PMC 题录可读；NCBI OA接口返回非开放获取；PMC网页/PDF自动访问受 reCAPTCHA 阻断 | 摘要与元数据已核验，全文仍待读 | 可登记为任务情境与控制变量推理候选，不得作为已读全文结论 |

## 本轮可进入证据链的内容

1. `ST-002` 可以进入 `C2-02` 的部分核验：它提供测评研究证据，说明物理内容知识表现与科学推理测验表现需要区分。
2. `ST-004` 只能进入候选/摘要层级：PubMed 摘要表明其研究关注任务情境、数据呈现和控制变量推理，但未阅读全文，不能写具体结果。
3. `ST-001` 继续作为经典测评工具来源候选：未获得全文前，不能写 Lawson 测验结构、题项维度、信效度或适用对象。

## 排除或保留待核的来源

- ResearchGate 页面显示 `ST-004` 有作者上传全文线索，但本轮自动访问返回 403，且版权/版本状态不宜直接作为正式引用依据，因此不纳入已读证据。
- PMC 记录包含 `ST-004` 的 `PMC4772877` 与 `NIHMS745588` 标识，但 NCBI OA 接口返回 `idIsNotOpenAccess`，本轮不把它当作开放全文。
- Wiley 与 ScienceDirect 自动访问均受权限或反爬挑战限制，后续应通过学校数据库、图书馆、馆际互借或作者授权获取。

## 后续获取建议

1. 通过学校数据库或图书馆请求 `ST-001` Wiley 全文；
2. 通过 ScienceDirect/Elsevier 机构权限或 NIHMS/PMC 可用页面人工访问 `ST-004` 全文；
3. 对 `ST-002`，人工打开 Science DOI 页面与 Supporting Online Material 页面，确认作者站 PDF 与出版社版本一致后再写正式页码和图表编号。

## 2026-07-14 二次审计补充

| 编号 | 新增线索 | 可用程度 | 处理决定 |
|---|---|---|---|
| ST-001 | PER-Central 详情页可读，显示格式含 `application/pdf` 和 `text/html`，但访问权为订阅/购买，并标明 Wiley 版权；PhysPort 的 CTSR 页面将该文列为研究依据，并提供测验用途、适用层级、研究验证摘要和下载限制 | 题录、摘要式介绍和二级测评资源可用；原文全文仍不可读 | `ST-001` 仍保持全文待读；PhysPort 只能作为后续理解 Lawson 测验的辅助线索，不能替代 Lawson (1978) 原文 |
| ST-004 | ScienceDirect 文章预览页可读，显示题名、作者、DOI、Highlights、Abstract、Introduction、Section snippets、References 和 Cited by；页面仍标注 `Article preview` 与 `View full text`，版权归 Elsevier | 预览/摘要层面可用；全文仍不可读 | `ST-004` 可更新为“ScienceDirect预览与PubMed摘要已核验”，但不得写作已阅读全文或转述完整方法、数据表和发展水平框架 |

## 精确获取路径

### ST-001

- Wiley DOI：`https://onlinelibrary.wiley.com/doi/10.1002/tea.3660150103`
- PER-Central：`https://www.per-central.org/items/detail.cfm?ID=12387`
- PhysPort CTSR：`https://www.physport.org/assessments/assessment.cfm?A=CTSR`
- 请求方式：学校图书馆数据库、Wiley订阅、馆际互借、Article Galaxy/Research Solutions 合规文献传递。

### ST-004

- ScienceDirect：`https://www.sciencedirect.com/science/article/abs/pii/S1871187115300407`
- PubMed：`https://pubmed.ncbi.nlm.nih.gov/26949425/`
- PMC记录：`https://pmc.ncbi.nlm.nih.gov/articles/PMC4772877/`
- 请求方式：ScienceDirect/Elsevier机构权限、学校图书馆、PMC人工页面访问、作者授权或馆际互借。

## 写作保护线

- `ST-001`：可以写“Lawson测验是候选测评来源，已定位题录和测评资源页”；不能写“原文报告了哪些信度/效度数值”。
- `ST-004`：可以写“控制变量推理任务情境与数据呈现是候选问题，ScienceDirect/PubMed摘要支持其作为待读来源”；不能写“该研究已经被本项目完整用于结果解释”。
