from __future__ import annotations

import argparse
import csv
import hashlib
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DIMENSIONS = ["模型建构", "科学推理", "科学论证", "质疑创新"]
RANK = {"未出现": 0, "L1": 1, "L2": 2, "L3": 3, "L4": 4}


def _path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def _write(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="从R01唯一分析表生成案例候选登记，不生成教学结论。")
    parser.add_argument("--input", default="07_analysis/data/final_coding.csv")
    parser.add_argument("--item-index", default="03_corpus/item_index.csv")
    parser.add_argument("--output", default="07_analysis/results/reviewed/r01_formal_case_candidates.csv")
    args = parser.parse_args()

    final_path = _path(args.input)
    index_path = _path(args.item_index)
    output_path = _path(args.output)
    final_rows = _read(final_path)
    index_rows = _read(index_path)
    if len(final_rows) != 876 or len(index_rows) != 219:
        raise ValueError("案例候选只接受876条唯一分析表与219条小问索引。")
    meta = {row["item_id"]: row for row in index_rows}
    grouped: dict[str, dict[str, dict[str, str]]] = defaultdict(dict)
    for row in final_rows:
        grouped[row["item_id"]][row["dimension"]] = row
    if set(grouped) != set(meta) or any(set(rows) != set(DIMENSIONS) for rows in grouped.values()):
        raise ValueError("final_coding与小问索引或四维度结构不一致。")

    source_sha = hashlib.sha256(final_path.read_bytes()).hexdigest()
    candidates = []
    for item_id, dimensions in grouped.items():
        high = [dimension for dimension in DIMENSIONS if RANK[dimensions[dimension]["level"]] >= 3]
        l4 = [dimension for dimension in DIMENSIONS if dimensions[dimension]["level"] == "L4"]
        if not high:
            continue
        item_text = ROOT / "03_corpus/item_texts" / f"{item_id.rsplit('-', 1)[0]}.md"
        info = meta[item_id]
        present_count = sum(dimensions[dimension]["present"] == "1" for dimension in DIMENSIONS)
        selection_score = len(l4) * 100 + len(high) * 10 + present_count
        candidates.append({
            "item_id": item_id,
            "competition_no": info["competition_no"],
            "year": info["year"],
            "question_no": info["question_no"],
            "subquestion_no": info["subquestion_no"],
            "knowledge_primary": info["knowledge_primary"],
            "dimensions_present": present_count,
            "high_level_dimensions": "；".join(f"{dimension}:{dimensions[dimension]['level']}" for dimension in high),
            "l4_dimensions": "；".join(l4),
            "selection_score": selection_score,
            "item_text_path": item_text.relative_to(ROOT).as_posix(),
            "item_text_exists": "是" if item_text.exists() else "否",
            "selection_boundary": "候选依据为裁决后编码与语料可定位性；不是学生困难、教师意见或教学效果证据",
            "source_final_coding_sha256": source_sha,
        })
    candidates.sort(key=lambda row: (-int(row["selection_score"]), -int(row["dimensions_present"]), row["item_id"]))
    for rank, row in enumerate(candidates, 1):
        row["candidate_rank"] = rank
    fields = [
        "candidate_rank", "item_id", "competition_no", "year", "question_no", "subquestion_no", "knowledge_primary",
        "dimensions_present", "high_level_dimensions", "l4_dimensions", "selection_score", "item_text_path", "item_text_exists",
        "selection_boundary", "source_final_coding_sha256",
    ]
    _write(output_path, fields, candidates)
    print(f"已生成{len(candidates)}条R01案例候选：{output_path}")


if __name__ == "__main__":
    main()
