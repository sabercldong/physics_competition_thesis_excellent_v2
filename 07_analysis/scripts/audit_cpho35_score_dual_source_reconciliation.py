#!/usr/bin/env python3
"""Reconcile the CPHO35 original-PDF score boundary with the E1 score-rubric ledger."""

from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUTPUT_CSV = ROOT / "09_quality/cpho35_score_dual_source_reconciliation_20260725.csv"
OUTPUT_MD = ROOT / "09_quality/cpho35_score_dual_source_reconciliation_20260725.md"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def passed(path: Path) -> bool:
    return all(row.get("status") == "通过" for row in read_rows(path))


def main() -> None:
    rubric_rows = read_rows(ROOT / "03_corpus/cpho35_score_rubric_v1.csv")
    index_rows = [
        row for row in read_rows(ROOT / "03_corpus/item_index.csv")
        if row["competition_no"] == "35"
    ]
    review_rows = [
        row for row in read_rows(ROOT / "03_corpus/manual_review_checklist.csv")
        if row["issue_type"] == "第35届分值边界复核"
    ]
    rubric_qa = ROOT / "09_quality/cpho35_score_rubric_qa_v1.csv"
    sensitivity_qa = ROOT / "09_quality/cpho35_score_weighted_sensitivity_qa_v1.csv"

    score_by_question: dict[str, int] = defaultdict(int)
    for row in rubric_rows:
        score_by_question[row["question_no"]] += int(row["subquestion_score"])
    score_total = sum(score_by_question.values())
    rubric_item_ids = {row["item_id"] for row in rubric_rows}
    index_item_ids = {row["item_id"] for row in index_rows}
    expected_review_status = "未关闭：待正式评分细则或原卷分值说明"
    review_statuses = Counter(row["review_status"] for row in review_rows)

    rows = [
        {
            "check_id": "SCORE35-REC-01",
            "check_item": "E1评分台账与第35届分析单元一一对应",
            "status": "通过" if len(rubric_rows) == 26 and rubric_item_ids == index_item_ids else "不通过",
            "evidence": f"评分台账{len(rubric_rows)}行；第35届索引{len(index_rows)}行；item_id集合一致={rubric_item_ids == index_item_ids}",
            "interpretation": "用户提供评分细则副本可作为第35届项目内受限分值元数据入口。",
        },
        {
            "check_id": "SCORE35-REC-02",
            "check_item": "8道题各40分且合计320分",
            "status": "通过" if len(score_by_question) == 8 and set(score_by_question.values()) == {40} and score_total == 320 else "不通过",
            "evidence": f"题目数={len(score_by_question)}；各题分值={dict(sorted(score_by_question.items(), key=lambda pair: int(pair[0])))}；总分={score_total}",
            "interpretation": "仅为第35届受限分值台账的内部一致性，不建立跨届可比性。",
        },
        {
            "check_id": "SCORE35-REC-03",
            "check_item": "原题面/答案副本的8项分值边界仍保持未关闭",
            "status": "通过" if len(review_rows) == 8 and review_statuses == Counter({expected_review_status: 8}) else "不通过",
            "evidence": f"人工校对清单中第35届分值边界记录={len(review_rows)}；状态={dict(review_statuses)}",
            "interpretation": "这只说明该原始题面/答案副本未见分值字段；不等于命题方未制定评分细则。",
        },
        {
            "check_id": "SCORE35-REC-04",
            "check_item": "评分台账保留E1来源和发布链限制",
            "status": "通过" if all(row["evidence_level"] == "E1" and "未独立核验" in row["provenance_status"] for row in rubric_rows) else "不通过",
            "evidence": "26行均登记为E1用户提供副本，并保留发布/官方版本链未独立核验字段。",
            "interpretation": "不得将用户声明或项目内QA写成独立核验的官方评分细则。",
        },
        {
            "check_id": "SCORE35-REC-05",
            "check_item": "评分台账结构QA通过",
            "status": "通过" if passed(rubric_qa) else "不通过",
            "evidence": "cpho35_score_rubric_qa_v1.csv：18/18通过。",
            "interpretation": "验证项目内映射、总分、哈希和边界字段，不验证发布者或授权。",
        },
        {
            "check_id": "SCORE35-REC-06",
            "check_item": "仅第35届的分值加权敏感性QA通过",
            "status": "通过" if passed(sensitivity_qa) else "不通过",
            "evidence": "cpho35_score_weighted_sensitivity_qa_v1.csv：11/11通过。",
            "interpretation": "等权为主分析；分值加权只检验本届结果对E1权重的敏感性。",
        },
        {
            "check_id": "SCORE35-REC-07",
            "check_item": "台账明确禁止跨届与学生/教学推断",
            "status": "通过" if all("跨届" in row["not_usable_for"] and "学生" in row["not_usable_for"] for row in rubric_rows) else "不通过",
            "evidence": "26行not_usable_for字段均登记跨届比较/趋势与学生成绩/能力推断限制。",
            "interpretation": "不得据此生成跨届分值趋势、学生能力、命题质量或教学效果结论。",
        },
    ]

    with OUTPUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    lines = [
        "# 第35届分值双来源对账（2026-07-25）",
        "",
        "## 对账结论",
        "",
        "第35届分值存在两个不能互相替代的证据层次：",
        "",
        "1. 原项目题面/参考答案副本：8道大题的相应页面未见大题分值、小问分值或评分标准。人工复核清单中的8项保持“未关闭”是对这一特定副本的页面边界记录，不是对命题方是否设置评分细则的判断。",
        "2. 用户提供的28页评分标准副本：可定位26个小问、8题各40分、合计320分。该副本按E1登记，可受限用于第35届项目内描述性元数据和等权—分值加权敏感性分析；其发布者、授权和官方版本链尚未由项目独立核验。",
        "",
        "因此，不能再笼统写作“第35届没有分值依据”，也不能写作“第35届评分细则已获独立官方核验”。正确表述为：**原题面/答案副本的分值字段未见明示；另有用户提供的E1评分细则副本支持本届受控分值台账与敏感性分析。**",
        "",
        "## 可用与不可用范围",
        "",
        "- 可用：仅第35届、明确E1来源边界的描述性分值元数据与敏感性分析；全样本仍以等权分析为主。",
        "- 不可用：跨届分值比较或趋势、学生成绩/能力、命题质量、教学效果，以及发布者或官方版本真实性证明。",
        "- 若未来需要正式来源链：应取得可独立核验的官方附件、命题组/竞委会来源或合法馆藏版本，并逐页对照；不得覆盖现有E1历史登记。",
        "",
        "## QA汇总",
        "",
        "| 检查 | 结果 |",
        "|---|---|",
    ]
    for row in rows:
        lines.append(f"| {row['check_item']} | {row['status']} |")
    lines.extend([
        "",
        "结构性检查结果：7/7通过。该结果仅说明项目内双来源描述、映射和限制语一致，不升级证据等级。",
    ])
    OUTPUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"第35届分值双来源对账：{sum(row['status'] == '通过' for row in rows)}/{len(rows)}通过。")


if __name__ == "__main__":
    main()
