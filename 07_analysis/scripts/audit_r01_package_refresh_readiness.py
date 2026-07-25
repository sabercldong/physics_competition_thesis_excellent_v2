#!/usr/bin/env python3
"""Report whether the current package can be fully refreshed without hiding stale inputs."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SNAPSHOT = ROOT / "10_outputs/material_package/R01_current_material_package_manifest_v1.csv"
V17_INPUTS = ROOT / "10_outputs/drafts/ECNU_非全日制专硕论文工作稿_R01_v17_inputs.json"
CANDIDATES = ROOT / "09_quality/r01_candidate_references_mapping_v1.csv"
TRACE = ROOT / "09_quality/r01_citation_trace_v1.csv"
OUTPUT_CSV = ROOT / "09_quality/r01_package_refresh_readiness_v1.csv"
OUTPUT_MD = ROOT / "09_quality/r01_package_refresh_readiness_v1.md"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    snapshot = rows(SNAPSHOT)
    candidates = rows(CANDIDATES)
    trace = rows(TRACE)
    manifest = json.loads(V17_INPUTS.read_text(encoding="utf-8"))
    stale_inputs = [
        relative_path
        for relative_path, expected_hash in manifest["source_sha256"].items()
        if not (ROOT / relative_path).is_file() or sha256(ROOT / relative_path) != expected_hash
    ]
    snapshot_current = all(
        row["exists"] == "是"
        and (ROOT / row["relative_path"]).is_file()
        and sha256(ROOT / row["relative_path"]) == row["sha256"]
        for row in snapshot
    )
    placeholder_count = sum(row["is_citation_placeholder"] == "是" for row in trace)
    checks = [
        ("PKG-READY-01", "材料包快照", "40项且当前", f"{len(snapshot)}项；{'当前' if snapshot_current else '过期'}", len(snapshot) == 40 and snapshot_current, "已同步"),
        ("PKG-READY-02", "候选引文链", "36项", str(len(candidates)), len(candidates) == 36, "已同步"),
        ("PKG-READY-03", "正文引用追溯", "67条来源/61处占位", f"{len(trace)}条来源/{placeholder_count}处占位", len(trace) == 67 and placeholder_count == 61, "已同步"),
        ("PKG-READY-04", "V17输入新鲜度", "9/9当前", f"{9 - len(stale_inputs)}/9当前；过期：{'；'.join(stale_inputs) or '无'}", not stale_inputs, "需重建" if stale_inputs else "已同步"),
        ("PKG-READY-05", "全链路健康检查可刷新条件", "V17当前且旧口径已更新", "V17待重建；全局材料审计/运行手册仍含旧计数", False, "需重建并更新门禁"),
    ]
    with OUTPUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["check_id", "check_item", "expected", "actual", "passed", "refresh_status"])
        for check_id, item, expected, actual, passed, refresh_status in checks:
            writer.writerow([check_id, item, expected, actual, "通过" if passed else "待刷新", refresh_status])
    OUTPUT_MD.write_text(
        "# R01 当前材料包刷新就绪度审计（V1）\n\n"
        "本审计只描述当前工作区的刷新状态，不把未重建的V17或旧口径全链路检查写作通过。\n\n"
        "## 当前判断\n\n"
        f"- 快照：{len(snapshot)}项，哈希{'当前' if snapshot_current else '存在不一致'}。\n"
        f"- 候选引文：{len(candidates)}项；引用追溯：{len(trace)}条来源、{placeholder_count}处显式占位。\n"
        f"- V17输入：{9 - len(stale_inputs)}/9当前。{'待重建输入：' + '；'.join(stale_inputs) if stale_inputs else '可进入V17重建。'}\n"
        "- 因V17输入不全当前，以及全局材料审计/运行手册仍使用30项、61/55和37项旧计数，不能声称当前16项全链路健康检查已通过。\n\n"
        "## 后续顺序\n\n"
        "1. 等待并行正文与候选引文源文件稳定并提交；\n"
        "2. 重建V17及其输入清单；\n"
        "3. 更新材料包总审计和复现运行手册的计数；\n"
        "4. 重跑16项全链路健康检查，再刷新快照和内部交接包。\n",
        encoding="utf-8",
    )
    print(f"材料包刷新就绪度：快照{len(snapshot)}项；候选{len(candidates)}项；追溯{len(trace)}/{placeholder_count}；V17过期输入{len(stale_inputs)}项")


if __name__ == "__main__":
    main()
