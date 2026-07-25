#!/usr/bin/env python3
"""Report whether legacy R01 package snapshots still match the current worktree.

This is deliberately read-only: it does not rebuild a package, overwrite a
working draft, or copy files that may currently contain parallel edits.
"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
V18_MANIFEST = ROOT / "10_outputs/drafts/ECNU_非全日制专硕论文工作稿_R01_v18_inputs.json"
V17_MANIFEST = ROOT / "10_outputs/drafts/ECNU_非全日制专硕论文工作稿_R01_v17_inputs.json"
PACKAGE_V1 = ROOT / "10_outputs/material_package/R01_current_material_package_manifest_v1.csv"
OUTPUT_CSV = ROOT / "09_quality/r01_legacy_package_snapshot_status_20260725.csv"
OUTPUT_MD = ROOT / "09_quality/r01_legacy_package_snapshot_status_20260725.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def snapshot_status(name: str, manifest: Path) -> tuple[dict[str, str], list[dict[str, str]]]:
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    details: list[dict[str, str]] = []
    for relative_path, expected_hash in payload["source_sha256"].items():
        path = ROOT / relative_path
        actual_hash = sha256(path) if path.is_file() else ""
        details.append({
            "snapshot": name,
            "artifact_id": "",
            "relative_path": relative_path,
            "expected_sha256": expected_hash,
            "actual_sha256": actual_hash,
            "status": "当前" if actual_hash == expected_hash else "已变化或缺失",
        })
    current = sum(row["status"] == "当前" for row in details)
    return ({
        "snapshot": name,
        "kind": "Word输入快照",
        "record_count": str(len(details)),
        "current_count": str(current),
        "status": "当前" if current == len(details) else "历史快照已过期",
        "boundary": "只判断输入哈希；不判断正文质量、学校格式或提交资格。",
    }, details)


def package_status() -> tuple[dict[str, str], list[dict[str, str]]]:
    details: list[dict[str, str]] = []
    for row in read_csv(PACKAGE_V1):
        path = ROOT / row["relative_path"]
        actual_hash = sha256(path) if path.is_file() else ""
        details.append({
            "snapshot": "材料包V1",
            "artifact_id": row["artifact_id"],
            "relative_path": row["relative_path"],
            "expected_sha256": row["sha256"],
            "actual_sha256": actual_hash,
            "status": "当前" if row["exists"] == "是" and actual_hash == row["sha256"] else "已变化或缺失",
        })
    current = sum(row["status"] == "当前" for row in details)
    return ({
        "snapshot": "材料包V1",
        "kind": "材料包快照",
        "record_count": str(len(details)),
        "current_count": str(current),
        "status": "当前" if current == len(details) else "历史快照已过期",
        "boundary": "只判断快照哈希；不重建或覆盖材料包，不判断研究结论。",
    }, details)


def main() -> None:
    summary: list[dict[str, str]] = []
    details: list[dict[str, str]] = []
    for name, manifest in (("V18工作稿", V18_MANIFEST), ("V17工作稿", V17_MANIFEST)):
        record, rows = snapshot_status(name, manifest)
        summary.append(record)
        details.extend(rows)
    record, rows = package_status()
    summary.append(record)
    details.extend(rows)

    with OUTPUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(details[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(details)

    current_v18 = next(row for row in summary if row["snapshot"] == "V18工作稿")
    stale = [row for row in summary if row["status"] != "当前"]
    lines = [
        "# R01 历史快照与当前工作区状态审计（2026-07-25）",
        "",
        "## 结论",
        "",
        f"V18工作稿输入为 {current_v18['current_count']}/{current_v18['record_count']} 当前，可继续作为当前非提交工作稿入口。",
        f"历史快照中有 {len(stale)} 项已过期：" + "、".join(row["snapshot"] for row in stale) + "。",
        "因此，旧V17材料包、内部交接包及其运行手册不能再被标为当前；它们应保留为历史快照，待并行编辑稳定后另行生成新版本。",
        "",
        "## 当前状态",
        "",
        "| 快照 | 类型 | 当前/总数 | 状态 |",
        "|---|---|---:|---|",
    ]
    for row in summary:
        lines.append(f"| {row['snapshot']} | {row['kind']} | {row['current_count']}/{row['record_count']} | {row['status']} |")
    lines.extend([
        "",
        "## 后续动作边界",
        "",
        "1. 不覆盖正文、不删除旧材料包、不把当前未提交改动打包或提交。",
        "2. 待作者确认并行编辑稳定后，使用单独版本号重建材料包清单、内部交接包和复现运行手册。",
        "3. 本审计不判断论文内容正确性、参考文献最终放行、学校格式、评分过程独立性或提交资格。",
    ])
    OUTPUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("历史快照状态：" + "；".join(f"{row['snapshot']}={row['status']}({row['current_count']}/{row['record_count']})" for row in summary))


if __name__ == "__main__":
    main()
