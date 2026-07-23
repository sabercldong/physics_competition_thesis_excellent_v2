from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SELECTED = {
    "CASE-R01-01": "CPHO36-Q04-1",
    "CASE-R01-02": "CPHO36-Q05-3",
    "CASE-R01-03": "CPHO37-Q06-3",
    "CASE-R01-04": "CPHO41-Q01-2",
}
GENERIC_MARKERS = (
    "题干要求",
    "题面需要",
    "题干直接给出",
    "题面未需要",
    "当前维度在",
)


def read_csv(relative: str) -> list[dict[str, str]]:
    with (ROOT / relative).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    rows = []
    for rater, relative in (
        ("RATER-A", "07_analysis/data/rater_returns/registered/R01/formal_coding_rater_A_FILLED_20260722_registered_lf.csv"),
        ("RATER-B", "07_analysis/data/rater_returns/registered/R01/formal_coding_rater_B_FILLED_20260722_registered_lf.csv"),
    ):
        coding_rows = read_csv(relative)
        evidence = [(row.get("evidence") or "").strip() for row in coding_rows]
        generic = sum(text.startswith(GENERIC_MARKERS) for text in evidence)
        rows.append({
            "check_id": f"CASE-EVID-{rater}-01",
            "scope": rater,
            "metric": "编码证据文本去重计数",
            "observed": str(len(set(evidence))),
            "expected_or_boundary": "876条记录应能提供可定位的逐条证据；去重计数只用于识别模板化风险，不单独判定真实性",
            "status": "风险提示",
        })
        rows.append({
            "check_id": f"CASE-EVID-{rater}-02",
            "scope": rater,
            "metric": "以通用句式开头的证据条数",
            "observed": f"{generic}/876",
            "expected_or_boundary": "若案例进入机制正文，需补题干/解答位置与具体触发语，不能仅保留通用模板句",
            "status": "风险提示",
        })

    final_rows = read_csv("07_analysis/data/final_coding.csv")
    final_by_item = Counter(row["item_id"] for row in final_rows)
    for case_id, item_id in SELECTED.items():
        rows.append({
            "check_id": f"CASE-EVID-{case_id}",
            "scope": case_id,
            "metric": "最终编码四维度记录完整性",
            "observed": str(final_by_item[item_id]),
            "expected_or_boundary": "4",
            "status": "通过" if final_by_item[item_id] == 4 else "不通过",
        })

    output = ROOT / "09_quality/r01_case_evidence_structural_audit_v1.csv"
    fields = ["check_id", "scope", "metric", "observed", "expected_or_boundary", "status"]
    with output.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {len(rows)} checks to {output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
