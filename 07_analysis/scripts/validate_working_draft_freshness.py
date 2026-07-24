#!/usr/bin/env python3
"""Compare the V16 working-draft manifest with its current source files."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = ROOT / "10_outputs/drafts/ECNU_非全日制专硕论文工作稿_R01_v16_inputs.json"
OUTPUT_CSV = ROOT / "09_quality/r01_working_draft_v16_freshness_qa.csv"
OUTPUT_MD = ROOT / "09_quality/r01_working_draft_v16_freshness_qa.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--require-current",
        action="store_true",
        help="Exit nonzero when any V16 source differs from the manifest.",
    )
    args = parser.parse_args()

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    checks: list[dict[str, str]] = []
    changed: list[str] = []
    for relative_path, recorded_hash in manifest["source_sha256"].items():
        path = ROOT / relative_path
        if not path.is_file():
            current_hash = "[缺失]"
            status = "缺失"
            changed.append(relative_path)
        else:
            current_hash = sha256(path)
            status = "当前" if current_hash == recorded_hash else "已变更"
            if status != "当前":
                changed.append(relative_path)
        checks.append(
            {
                "source_path": relative_path,
                "manifest_sha256": recorded_hash,
                "current_sha256": current_hash,
                "status": status,
            }
        )

    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=checks[0].keys(), lineterminator="\n")
        writer.writeheader()
        writer.writerows(checks)

    current_count = sum(check["status"] == "当前" for check in checks)
    state = "当前" if not changed else "已过期"
    lines = [
        "# R01工作稿V16输入新鲜度QA",
        "",
        f"检查了{len(checks)}项V16输入：{current_count}项当前，{len(changed)}项已变更或缺失。",
        f"结论：V16相对当前源文件为**{state}**。",
        "",
        "本检查只比较输入哈希，不判断变更质量，不重生成DOCX，也不把未提交源文件变更纳入V16。",
    ]
    if changed:
        lines.extend(["", "## 需重新生成前先审阅的输入", ""])
        lines.extend(f"- `{relative_path}`" for relative_path in changed)
    OUTPUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"V16输入新鲜度QA：{current_count}/{len(checks)}当前；状态：{state}")
    if args.require_current and changed:
        raise SystemExit("V16相对当前源文件已过期：" + ", ".join(changed))


if __name__ == "__main__":
    main()
