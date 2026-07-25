#!/usr/bin/env python3
"""Validate the final-reference action queue against the candidate mapping."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MAPPING = ROOT / "09_quality/r01_candidate_references_mapping_v1.csv"
QUEUE = ROOT / "09_quality/r01_final_reference_action_queue_20260725.csv"
OUTPUT = ROOT / "09_quality/r01_final_reference_action_queue_qa_20260725.csv"


def load(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    mapping = load(MAPPING)
    queue = load(QUEUE)
    expected = {row["source_id"] for row in mapping}
    actual = {row["source_id"] for row in queue}
    checks = [
        ("REFQ-01", "候选数与队列数", len(mapping) == len(queue), f"{len(mapping)} / {len(queue)}"),
        ("REFQ-02", "来源ID一一对应", expected == actual, f"缺失={','.join(sorted(expected - actual)) or '无'}；额外={','.join(sorted(actual - expected)) or '无'}"),
        ("REFQ-03", "候选状态边界", all(row["current_final_status"] == "候选条目，未最终放行" for row in queue), "所有条目均未放行"),
        ("REFQ-04", "优先级完整", all(row["priority"] in {"P1", "P2"} for row in queue), "P1/P2分类完整"),
        ("REFQ-05", "禁止捷径声明", all(row["prohibited_shortcut"] for row in queue), "39条均有禁止捷径说明"),
        ("REFQ-06", "内部身份不一致升级为P1", all(row["priority"] == "P1" for row in queue if "项目内候选著录DOI与BibTeX字段不一致" in row["remaining_verification"]), "内部身份不一致条目不得留在P2"),
    ]
    with OUTPUT.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["check_id", "check_item", "status", "evidence"])
        for check_id, item, passed, evidence in checks:
            writer.writerow([check_id, item, "通过" if passed else "不通过", evidence])
    failed = [check_id for check_id, _, passed, _ in checks if not passed]
    if failed:
        raise SystemExit("最终参考文献行动清单QA失败：" + ", ".join(failed))
    print(f"最终参考文献行动清单QA：{len(checks)}/{len(checks)}通过。")


if __name__ == "__main__":
    main()
