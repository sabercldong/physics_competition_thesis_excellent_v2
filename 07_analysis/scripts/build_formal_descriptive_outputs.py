from __future__ import annotations

import argparse
import csv
import hashlib
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DIMENSIONS = ["模型建构", "科学推理", "科学论证", "质疑创新"]
LEVELS = ["L1", "L2", "L3", "L4"]


def _path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def _write_csv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _write_report(path: Path, *, input_path: Path, final_sha: str, items: int, outputs: list[Path]) -> None:
    path.write_text(
        "# R01 正式描述统计输出说明\n\n"
        f"输入：`{input_path.relative_to(ROOT).as_posix()}`（SHA-256：`{final_sha}`）\n\n"
        f"分析单位：{items} 个独立小问；四个维度各一条记录，共 {items * len(DIMENSIONS)} 条裁决后编码记录。\n\n"
        "本批输出仅为描述性统计。它描述题目任务要求的编码结果，不能推断学生能力、教学效果、长期趋势、因果关系或统计显著性。"
        "本批全样本输出不使用分值权重；第35届分值敏感性分析如需使用，须单列为仅本届、E1来源边界下的辅助材料。\n\n"
        "## 输出文件\n\n"
        + "\n".join(f"- `{output.relative_to(ROOT).as_posix()}`" for output in outputs)
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="从唯一分析表生成正式描述统计输出。")
    parser.add_argument("--input", default="07_analysis/data/final_coding.csv")
    parser.add_argument("--item-index", default="03_corpus/item_index.csv")
    parser.add_argument("--output-dir", default="07_analysis/results/reviewed")
    args = parser.parse_args()

    input_path = _path(args.input)
    index_path = _path(args.item_index)
    output_dir = _path(args.output_dir)
    final_rows = _read_csv(input_path)
    index_rows = _read_csv(index_path)
    if len(final_rows) != 876:
        raise ValueError(f"final_coding.csv 应为876条记录，实际为{len(final_rows)}")
    if len(index_rows) != 219:
        raise ValueError(f"item_index.csv 应为219个分析单位，实际为{len(index_rows)}")

    item_meta = {row["item_id"]: row for row in index_rows}
    by_item: dict[str, dict[str, dict[str, str]]] = defaultdict(dict)
    for row in final_rows:
        if row["item_id"] not in item_meta:
            raise ValueError(f"final_coding.csv 含无法映射的item_id：{row['item_id']}")
        if row["dimension"] not in DIMENSIONS:
            raise ValueError(f"未知维度：{row['dimension']}")
        if row["present"] not in {"0", "1"}:
            raise ValueError(f"present必须为0/1：{row['present']}")
        if row["dimension"] in by_item[row["item_id"]]:
            raise ValueError(f"重复item-dimension：{row['item_id']} / {row['dimension']}")
        by_item[row["item_id"]][row["dimension"]] = row
    if set(by_item) != set(item_meta):
        raise ValueError("final_coding与item_index的分析单位集合不一致")
    if any(set(dimensions) != set(DIMENSIONS) for dimensions in by_item.values()):
        raise ValueError("每个分析单位必须恰有四个维度")

    final_sha = hashlib.sha256(input_path.read_bytes()).hexdigest()
    total_items = len(item_meta)
    presence_rows = []
    level_rows = []
    for dimension in DIMENSIONS:
        dimension_rows = [dimensions[dimension] for dimensions in by_item.values()]
        present_items = sum(row["present"] == "1" for row in dimension_rows)
        presence_rows.append({
            "dimension": dimension,
            "items_present": present_items,
            "total_items": total_items,
            "proportion": round(present_items / total_items, 6),
            "source_final_coding_sha256": final_sha,
        })
        for level in LEVELS:
            count = sum(row["level"] == level for row in dimension_rows)
            level_rows.append({
                "dimension": dimension,
                "level": level,
                "count": count,
                "present_items_total": present_items,
                "proportion_among_present": round(count / present_items, 6) if present_items else "",
                "source_final_coding_sha256": final_sha,
            })

    cooccurrence_rows = []
    for offset, left in enumerate(DIMENSIONS):
        for right in DIMENSIONS[offset + 1 :]:
            left_n = sum(dimensions[left]["present"] == "1" for dimensions in by_item.values())
            right_n = sum(dimensions[right]["present"] == "1" for dimensions in by_item.values())
            both_n = sum(
                dimensions[left]["present"] == "1" and dimensions[right]["present"] == "1"
                for dimensions in by_item.values()
            )
            union_n = left_n + right_n - both_n
            cooccurrence_rows.append({
                "dimension_a": left,
                "dimension_b": right,
                "items_both_present": both_n,
                "items_a_present": left_n,
                "items_b_present": right_n,
                "items_either_present": union_n,
                "jaccard": round(both_n / union_n, 6) if union_n else "",
                "source_final_coding_sha256": final_sha,
            })

    def grouped_presence(group_field: str) -> list[dict[str, object]]:
        grouped_items: dict[str, list[str]] = defaultdict(list)
        for item_id, meta in item_meta.items():
            grouped_items[meta[group_field]].append(item_id)
        rows = []
        for group_value in sorted(grouped_items):
            item_ids = grouped_items[group_value]
            for dimension in DIMENSIONS:
                present_items = sum(by_item[item_id][dimension]["present"] == "1" for item_id in item_ids)
                rows.append({
                    group_field: group_value,
                    "dimension": dimension,
                    "items_present": present_items,
                    "total_items": len(item_ids),
                    "proportion": round(present_items / len(item_ids), 6),
                    "source_final_coding_sha256": final_sha,
                })
        return rows

    output_dir.mkdir(parents=True, exist_ok=True)
    outputs = {
        "final_dimension_presence.csv": (["dimension", "items_present", "total_items", "proportion", "source_final_coding_sha256"], presence_rows),
        "final_level_distribution.csv": (["dimension", "level", "count", "present_items_total", "proportion_among_present", "source_final_coding_sha256"], level_rows),
        "final_dimension_cooccurrence.csv": (["dimension_a", "dimension_b", "items_both_present", "items_a_present", "items_b_present", "items_either_present", "jaccard", "source_final_coding_sha256"], cooccurrence_rows),
        "final_year_dimension_presence.csv": (["year", "dimension", "items_present", "total_items", "proportion", "source_final_coding_sha256"], grouped_presence("year")),
        "final_knowledge_dimension_presence.csv": (["knowledge_primary", "dimension", "items_present", "total_items", "proportion", "source_final_coding_sha256"], grouped_presence("knowledge_primary")),
    }
    written = []
    for name, (fields, rows) in outputs.items():
        path = output_dir / name
        _write_csv(path, fields, rows)
        written.append(path)
    report_path = output_dir / "final_descriptive_output_report.md"
    _write_report(report_path, input_path=input_path, final_sha=final_sha, items=total_items, outputs=written)
    print("已生成正式描述统计输出：")
    for path in written:
        print(path)


if __name__ == "__main__":
    main()
