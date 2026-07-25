#!/usr/bin/env python3
"""Check that the R01 G3 lifecycle reconciliation matches project-local evidence."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RECONCILIATION = ROOT / "09_quality/r01_g3_framework_lifecycle_reconciliation_20260725.md"
OUTPUT_CSV = ROOT / "09_quality/r01_g3_framework_lifecycle_reconciliation_qa_v1.csv"
OUTPUT_MD = ROOT / "09_quality/r01_g3_framework_lifecycle_reconciliation_qa_v1.md"


def count_rows(path: Path) -> int:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def main() -> None:
    text = RECONCILIATION.read_text(encoding="utf-8")
    required = [
        ("G3-QA-01", "对账文件存在", RECONCILIATION.is_file()),
        ("G3-QA-02", "G3-01状态", "G3-01" in text and "219 个分析单元" in text),
        ("G3-QA-03", "G3-02状态", "G3-02" in text and "四维" in text),
        ("G3-QA-04", "G3-03任务等级边界", "G3-03" in text and "学生真实学习结果" in text),
        ("G3-QA-05", "G3-04培训材料", "G3-04" in text and "边界案例" in text),
        ("G3-QA-06", "G3-05未关闭", "G3-05" in text and "未收到真实专家审查记录" in text),
        ("G3-QA-07", "G3-06声明边界", "G3-06" in text and "不能独立验证评分者身份" in text),
        ("G3-QA-08", "G3-07裁决边界", "G3-07" in text and "142 条分歧" in text),
        ("G3-QA-09", "G3-08未冻结", "G3-08" in text and "未完成" in text),
        ("G3-QA-10", "分析单位数", count_rows(ROOT / "03_corpus/item_index.csv") == 219),
        ("G3-QA-11", "A回填行数", count_rows(ROOT / "07_analysis/data/rater_returns/incoming/R01/formal_coding_rater_A_FILLED_20260722.csv") == 876),
        ("G3-QA-12", "B回填行数", count_rows(ROOT / "07_analysis/data/rater_returns/incoming/R01/formal_coding_rater_B_FILLED_20260722.csv") == 876),
        ("G3-QA-13", "当前唯一编码行数", count_rows(ROOT / "07_analysis/data/final_coding_r01_correction_v1.csv") == 876),
        ("G3-QA-14", "一致性报告存在", (ROOT / "07_analysis/results/formal_rater_r01/r01_rater_reliability_report.md").is_file()),
        ("G3-QA-15", "裁决接收检查存在", (ROOT / "07_analysis/results/formal_rater_r01/r01_adjudication_return_intake_check.md").is_file()),
        ("G3-QA-16", "专家审查包存在", (ROOT / "04_framework/expert_review_packet.md").is_file()),
        ("G3-QA-17", "正式手册边界", "不是经专家审查和导师确认的正式手册" in text),
        ("G3-QA-18", "禁止升级表述", "不可以说" in text and "框架有效" in text),
    ]
    with OUTPUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["check_id", "check_item", "status"])
        writer.writerows((check_id, item, "通过" if passed else "不通过") for check_id, item, passed in required)
    failures = [check_id for check_id, _, passed in required if not passed]
    OUTPUT_MD.write_text(
        "# R01 G3分析框架生命周期对账QA\n\n"
        f"共完成{len(required)}项检查，{'全部通过' if not failures else '不通过：' + '、'.join(failures)}。"
        "本QA只检查项目内文件、数量和边界文本，不验证任何人的身份、互盲、独立过程、专家资格或框架外部效度。\n",
        encoding="utf-8",
    )
    if failures:
        raise SystemExit("G3生命周期对账QA失败：" + ", ".join(failures))
    print(f"R01 G3生命周期对账QA：{len(required)}/{len(required)}通过")


if __name__ == "__main__":
    main()
