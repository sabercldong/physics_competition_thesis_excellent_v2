# G2-06-CLAIMS 内容分析与评分者一致性方法文献准备

## 任务定位

本文件启动内容分析、编码手册、评分者一致性和可靠性报告方法文献的候选核验。当前只完成候选来源定位和阅读任务分配，不代表已经阅读全文，也不能直接作为第三章方法定稿依据。

## 候选来源

| 编号 | 来源 | 当前状态 | 可能用途 | 当前不能做的事 |
|---|---|---|---|---|
| METH-001 | Krippendorff, *Content Analysis: An Introduction to Its Methodology*, 4th ed., SAGE, 2018 | SAGE Research Methods与Google Books/出版社线索已定位；全文待读 | 内容分析总体方法、单位化、编码、可靠性和效度候选依据 | 未读全文前不能写具体方法要求或页码 |
| METH-002 | Cohen, 1960, “A Coefficient of Agreement for Nominal Scales” | SAGE DOI页已定位；全文权限待确认 | Cohen's kappa原始来源候选 | 不能直接规定本研究kappa阈值 |
| METH-003 | Landis & Koch, 1977, “The Measurement of Observer Agreement for Categorical Data” | JSTOR/Europe PMC题录已定位；全文权限待确认 | 分类数据观察者一致性和kappa解释候选来源 | 不能把其等级阈值机械作为本研究判据 |
| METH-004 | Lombard, Snyder-Duch & Bracken, 2002, “Content Analysis in Mass Communication: Assessment and Reporting of Intercoder Reliability” | Oxford/Wiley DOI页和开放仓储线索已定位；全文待读 | 编码者一致性评估与报告规范候选来源 | 不能替代教育测量或本项目评分者训练记录 |
| METH-005 | Neuendorf, *The Content Analysis Guidebook*, 2nd ed., SAGE, 2017 | SAGE Research Methods和作者机构页已定位；全文待读 | 内容分析流程、codebook、抽样、编码者训练候选依据 | 未读全文前不能转述具体步骤 |

## 与本项目的关系

| 项目环节 | 需要的方法依据 | 对应候选 |
|---|---|---|
| 小问级分析单位 | 内容分析的单位化、抽样和可追溯记录 | METH-001、METH-005 |
| 编码手册与正反例 | codebook、变量定义、编码者训练 | METH-001、METH-005、METH-004 |
| 双评分者独立编码 | intercoder reliability / interrater agreement | METH-002、METH-003、METH-004 |
| 分歧裁决 | 独立编码后形成唯一裁决版本的记录规则 | METH-004、METH-005 |
| 方法章报告 | 一致性指标、样本、变量、限制和解释边界 | METH-002、METH-003、METH-004 |

## 需要全文阅读后提取的字段

| 字段 | 填写要求 |
|---|---|
| 方法对象 | 文本内容分析、分类评分、一致性统计或编码报告 |
| 关键概念 | unitizing、codebook、intercoder reliability、Cohen kappa、Krippendorff alpha等 |
| 适用条件 | 名义变量、等级变量、双评分者、多评分者、样本大小、变量分布 |
| 报告要求 | 是否需要报告样本量、变量、公式、置信区间或阈值解释 |
| 对本项目的直接用途 | 第三章分析单位、编码手册、双评分者、一致性计算、分歧裁决 |
| 不可迁移之处 | 不适用于教育试题编码或本项目数据结构的部分 |

## 待核验主张

本文件暂支持以下“待核验”主张进入 `claim_evidence_matrix.csv`：

- `C2-04`：维度存在性与结构等级分开编码比单一总分更能保留解释力；
- 第三章后续方法主张：正式编码需报告评分者一致性、分歧裁决和唯一分析表。

这些主张当前不能标为已核验，原因是方法文献尚未阅读全文，真实评分者编码与裁决也尚未完成。

## 写作边界

- 可以写：内容分析和一致性方法文献已进入候选清单；
- 可以写：本项目方法章需要补充单位化、编码手册、双评分者和一致性报告依据；
- 不能写：本项目编码框架已经达到某一一致性标准；
- 不能写：某一kappa阈值已经被确定为本项目正式通过线；
- 不能写：内部Codex模拟结果可替代真实评分者一致性。

## 下一步

1. 按 `content_analysis_reliability_fulltext_request_packet.md` 获取 METH-001 至 METH-005 的合法全文；
2. 获得全文后先填写 `content_analysis_reliability_screening_matrix.csv`；
3. 决定本研究正式报告哪些一致性指标，并记录适用条件与局限；
4. 将全文阅读结果补入 `literature_matrix.csv` 的方法、适用条件和局限字段；
5. 在真实评分者完成编码后，再用方法文献支持第三章正式方法写作。
