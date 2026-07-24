#!/usr/bin/env python3
"""Check that the current material-package audit agrees with project artifacts."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
AUDIT = ROOT / "09_quality/current_material_package_audit_v2.md"
ITEMS = ROOT / "03_corpus/item_index.csv"
CODING = ROOT / "07_analysis/data/final_coding_r01_correction_v1.csv"
REFERENCE_LEDGER = ROOT / "02_literature/reference_verification.csv"
CANDIDATES = ROOT / "09_quality/r01_candidate_references_mapping_v1.csv"
RESULT_QA = ROOT / "09_quality/r01_results_eligibility_qa_v1.csv"
RESULTS_INTEGRATION_QA = ROOT / "09_quality/r01_results_manuscript_integration_qa_v2.csv"
CITATION_TRACE = ROOT / "09_quality/r01_citation_trace_v1.csv"
V17 = ROOT / "10_outputs/drafts/ECNU_非全日制专硕论文工作稿_R01_v17.docx"
V17_MANIFEST = ROOT / "10_outputs/drafts/ECNU_非全日制专硕论文工作稿_R01_v17_inputs.json"
V17_QA = ROOT / "09_quality/r01_working_draft_v17_qa.md"
SNAPSHOT_MANIFEST = ROOT / "10_outputs/material_package/R01_current_material_package_manifest_v1.csv"
OUTPUT_CSV = ROOT / "09_quality/current_material_package_audit_v2_qa.csv"
OUTPUT_MD = ROOT / "09_quality/current_material_package_audit_v2_qa.md"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    audit = AUDIT.read_text(encoding="utf-8")
    item_count = len(rows(ITEMS))
    coding_count = len(rows(CODING))
    ledger = rows(REFERENCE_LEDGER)
    read_count = sum(
        row["full_text_available"].startswith("是") and row["relevant_passage_checked"] == "是"
        for row in ledger
    )
    candidate_count = len(rows(CANDIDATES))
    result_qa = rows(RESULT_QA)
    result_passed = all(row["status"] == "通过" for row in result_qa)
    integration_qa = rows(RESULTS_INTEGRATION_QA) if RESULTS_INTEGRATION_QA.is_file() else []
    integration_passed = bool(integration_qa) and all(row["status"] == "通过" for row in integration_qa)
    trace = rows(CITATION_TRACE)
    trace_total = len(trace)
    trace_placeholders = sum(row["is_citation_placeholder"] == "是" for row in trace)
    manifest = json.loads(V17_MANIFEST.read_text(encoding="utf-8"))
    draft_inputs_current = all(
        (ROOT / path).is_file() and sha256(ROOT / path) == manifest_hash
        for path, manifest_hash in manifest["source_sha256"].items()
    )
    snapshot_rows = rows(SNAPSHOT_MANIFEST) if SNAPSHOT_MANIFEST.is_file() else []
    snapshot_current = bool(snapshot_rows) and all(
        row["exists"] == "是"
        and (ROOT / row["relative_path"]).is_file()
        and sha256(ROOT / row["relative_path"]) == row["sha256"]
        for row in snapshot_rows
    )
    expected = [
        ("MPA-QA-01", "分析单元数", str(item_count), "219", item_count == 219),
        ("MPA-QA-02", "当前编码记录数", str(coding_count), "876", coding_count == 876),
        ("MPA-QA-03", "全文已读来源数", str(read_count), "30", read_count == 30),
        ("MPA-QA-04", "候选工作稿来源数", str(candidate_count), "26", candidate_count == 26),
        ("MPA-QA-05", "距离30篇最小差额", str(max(0, 30 - read_count)), "0", max(0, 30 - read_count) == 0),
        ("MPA-QA-06", "结果资格QA", f"{sum(row['status'] == '通过' for row in result_qa)}/{len(result_qa)}", "51/51", result_passed and len(result_qa) == 51),
        ("MPA-QA-07", "第四章当前结果整合QA", f"{sum(row['status'] == '通过' for row in integration_qa)}/{len(integration_qa)}", "30/30", integration_passed and len(integration_qa) == 30),
        ("MPA-QA-08", "引用追溯", f"{trace_total}/{trace_placeholders}", "57/51", trace_total == 57 and trace_placeholders == 51),
        ("MPA-QA-09", "V17工作稿文件", "存在" if V17.is_file() else "缺失", "存在", V17.is_file()),
        ("MPA-QA-10", "V17输入清单", "存在" if V17_MANIFEST.is_file() else "缺失", "存在", V17_MANIFEST.is_file()),
        ("MPA-QA-11", "V17工作稿QA", "存在" if V17_QA.is_file() else "缺失", "存在", V17_QA.is_file()),
        ("MPA-QA-12", "V17输入新鲜度", "当前" if draft_inputs_current else "已过期或缺失", "当前", draft_inputs_current),
        ("MPA-QA-13", "材料包快照条目数", f"{len(snapshot_rows)}项", "30项", len(snapshot_rows) == 30),
        ("MPA-QA-14", "材料包快照哈希", "当前" if snapshot_current else "已过期或缺失", "当前", snapshot_current),
        ("MPA-QA-15", "审计中的关键数量", "存在" if all(token in audit for token in ["219", "876", "43 / 30 / 26", "数量基线", "51/51", "30/30", "28/28", "V17", "30/30当前"]) else "缺失", "存在", all(token in audit for token in ["219", "876", "43 / 30 / 26", "数量基线", "51/51", "30/30", "28/28", "V17", "30/30当前"])),
        ("MPA-QA-16", "审计中的独立验证边界", "存在" if "自声明" in audit and "项目独立验证" in audit else "缺失", "存在", "自声明" in audit and "项目独立验证" in audit),
    ]
    with OUTPUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["check_id", "check_item", "actual", "expected", "status"])
        for check_id, item, actual, expected_value, passed in expected:
            writer.writerow([check_id, item, actual, expected_value, "通过" if passed else "不通过"])
    failures = [check_id for check_id, _, _, _, passed in expected if not passed]
    OUTPUT_MD.write_text(
        "# 当前材料包审计V2 QA\n\n"
        f"共完成{len(expected)}项检查，{'全部通过' if not failures else '不通过：' + '、'.join(failures)}。"
        "本QA只核对项目内文件、数量和审计边界的一致性，不验证评分者身份、人工过程、外部效度或人类参与者事实。\n",
        encoding="utf-8",
    )
    if failures:
        raise SystemExit("材料包审计QA失败：" + ", ".join(failures))
    print(f"材料包审计V2 QA：{len(expected)}/{len(expected)}通过")


if __name__ == "__main__":
    main()
