from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EXCLUDED = {"CPHO36-Q04-1", "CPHO36-Q05-3", "CPHO37-Q06-3", "CPHO41-Q01-2"}
SELECTED = ["CPHO41-Q06-3", "CPHO41-Q07-4", "CPHO42-Q04-2"]
DIMENSIONS = ["模型建构", "科学推理", "科学论证", "质疑创新"]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_rows(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    chain = read_rows(ROOT / "07_analysis/data/final_coding_evidence_r01_v1.csv")
    index = {row["item_id"]: row for row in read_rows(ROOT / "03_corpus/item_index.csv")}
    grouped: dict[str, list[dict[str, str]]] = {}
    for row in chain:
        grouped.setdefault(row["item_id"], []).append(row)
    rows = []
    for rank, item_id in enumerate(SELECTED, 1):
        records = grouped.get(item_id, [])
        meta = index.get(item_id, {})
        levels = {row["dimension"]: row["current_level"] for row in records}
        high = [f"{dimension}:{levels.get(dimension, '')}" for dimension in DIMENSIONS if levels.get(dimension) in {"L3", "L4"}]
        all_v2 = len(records) == 4 and all(row["evidence_source"] == "R01-EVIDENCE-REPAIR-V2" for row in records)
        all_locatable = all((ROOT / row["item_text_path"]).exists() and row["question_quote"] and row["solution_quote"] for row in records)
        rows.append({
            "case_rank": str(rank),
            "item_id": item_id,
            "competition_no": meta.get("competition_no", ""),
            "year": meta.get("year", ""),
            "knowledge_primary": meta.get("knowledge_primary", ""),
            "high_level_current_coding": "；".join(high),
            "four_dimension_records": str(len(records)),
            "all_evidence_from_v2_repair": "是" if all_v2 else "否",
            "all_quotes_locatable": "是" if all_locatable else "否",
            "excluded_from_prior_failed_cases": "是" if item_id not in EXCLUDED else "否",
            "selection_decision": "可作为任务结构说明案例" if all_v2 and all_locatable and high and item_id not in EXCLUDED else "不纳入",
            "boundary": "仅说明R01当前编码下的题设—解答任务结构；不重判等级，不证明评分过程、学生困难、教师意见或教学效果。",
        })
    fields = list(rows[0])
    out_dir = ROOT / "07_analysis/results/formal_rater_r01"
    write_rows(out_dir / "r01_case_reselection_v1.csv", fields, rows)
    dossier_fields = [
        "case_rank", "item_id", "dimension", "current_present", "current_level", "question_quote", "question_location",
        "solution_quote", "solution_location", "evidence_source", "evidence_source_sha256", "item_text_path",
    ]
    dossier = []
    for row in rows:
        for record in sorted(grouped[row["item_id"]], key=lambda value: DIMENSIONS.index(value["dimension"])):
            dossier.append({"case_rank": row["case_rank"], **{field: record[field] for field in dossier_fields if field not in {"case_rank", "item_id"}} , "item_id": record["item_id"]})
    write_rows(out_dir / "r01_case_reselection_evidence_dossier_v1.csv", dossier_fields, dossier)
    qa = []
    for row in rows:
        passed = row["selection_decision"] == "可作为任务结构说明案例"
        qa.append({"check_item": row["item_id"], "observed": f"四维={row['four_dimension_records']}；V2={row['all_evidence_from_v2_repair']}；定位={row['all_quotes_locatable']}；排除旧失败案={row['excluded_from_prior_failed_cases']}", "expected": "4；是；是；是", "status": "通过" if passed else "不通过"})
    write_rows(out_dir / "r01_case_reselection_qa_v1.csv", ["check_item", "observed", "expected", "status"], qa)
    print(f"已生成{len(rows)}个R01任务结构案例及{len(dossier)}条证据包记录。")


if __name__ == "__main__":
    main()
