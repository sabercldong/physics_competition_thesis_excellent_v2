# Git工作流

## 初始化

```bash
git init
git add .
git commit -m "初始化优秀硕士论文重建项目"
```

## 分支命名

```text
work/G0-01-material-inventory
work/G1-05-item-index
work/G3-04-coding-manual-v1
work/G4-04-descriptive-results
work/G7-02-results-chapter
review/advisor-round-1
```

## 提交原则

- 数据录入、分析脚本、结果输出和正文解释分别提交；
- 一次提交只处理一个可审查问题；
- 所有导师修改写入 `09_quality/advisor_feedback_log.csv`；
- 不使用破坏性Git命令；
- 重要里程碑打标签，例如 `M3-framework-frozen`。
