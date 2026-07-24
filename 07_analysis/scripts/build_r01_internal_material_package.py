#!/usr/bin/env python3
"""Assemble a checksum-verified internal, non-submission R01 handoff directory."""

from __future__ import annotations

import argparse
import csv
import hashlib
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE_MANIFEST = ROOT / "10_outputs/material_package/R01_current_material_package_manifest_v1.csv"
PACKAGE_DIR = ROOT / "10_outputs/material_package/R01_internal_handoff_v1"
PACKAGE_MANIFEST = PACKAGE_DIR / "R01_internal_handoff_manifest_v1.csv"
PACKAGE_README = PACKAGE_DIR / "README.md"
LOCAL_DRAFT_ID = "PKG-21"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def allowed_rows(include_local_draft: bool) -> list[dict[str, str]]:
    rows = read_rows(SOURCE_MANIFEST)
    selected = [row for row in rows if row["distribution_boundary"].startswith("可随材料包提供")]
    if include_local_draft:
        selected.extend(row for row in rows if row["artifact_id"] == LOCAL_DRAFT_ID)
    return selected


def build(include_local_draft: bool, force: bool) -> None:
    if PACKAGE_DIR.exists():
        if not force:
            raise SystemExit(f"交接目录已存在：{PACKAGE_DIR}；确认需要重建时加 --force")
        shutil.rmtree(PACKAGE_DIR)
    selected = allowed_rows(include_local_draft)
    PACKAGE_DIR.mkdir(parents=True)
    copied: list[dict[str, str]] = []
    for row in selected:
        source = ROOT / row["relative_path"]
        if not source.is_file() or row["exists"] != "是" or sha256(source) != row["sha256"]:
            raise SystemExit(f"当前源文件与材料包快照不一致：{row['artifact_id']}")
        destination = PACKAGE_DIR / "artifacts" / row["relative_path"]
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        copied.append({
            "artifact_id": row["artifact_id"],
            "relative_path": row["relative_path"],
            "package_relative_path": destination.relative_to(PACKAGE_DIR).as_posix(),
            "distribution_boundary": row["distribution_boundary"],
            "source_sha256": row["sha256"],
            "package_sha256": sha256(destination),
        })
    with PACKAGE_MANIFEST.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(copied[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(copied)
    PACKAGE_README.write_text(
        "# R01 内部非提交交接包\n\n"
        "本目录由 `07_analysis/scripts/build_r01_internal_material_package.py` 从当前SHA-256快照生成，"
        "用于项目内部交接、复现和写作核对；不是公开发布包、匿名送审包、答辩包或学校提交包。\n\n"
        "默认不含原始试卷、参考解答、受版权限制的文献全文、可识别个人资料、私人数据或V17 Word工作稿。"
        "若以 `--include-local-draft` 显式生成，V17仍只限本地内部使用，禁止作为正式提交或公开分发件。\n\n"
        "每个副本都保留其源路径和SHA-256。校验命令：\n\n"
        "```bash\n"
        "python3 07_analysis/scripts/build_r01_internal_material_package.py --validate\n"
        "```\n",
        encoding="utf-8",
    )
    print(f"已生成R01内部交接包：{len(copied)}项，目录：{PACKAGE_DIR.relative_to(ROOT)}")


def validate() -> None:
    if not PACKAGE_MANIFEST.is_file() or not PACKAGE_README.is_file():
        raise SystemExit("内部交接包未生成，请先运行构建命令")
    rows = read_rows(PACKAGE_MANIFEST)
    current = {row["artifact_id"]: row for row in read_rows(SOURCE_MANIFEST)}
    always_required = {row["artifact_id"] for row in allowed_rows(False)}
    actual_ids = {row["artifact_id"] for row in rows}
    failures: list[str] = []
    for row in rows:
        source = ROOT / row["relative_path"]
        package_file = PACKAGE_DIR / row["package_relative_path"]
        source_row = current.get(row["artifact_id"])
        if (
            source_row is None
            or not source.is_file()
            or not package_file.is_file()
            or sha256(source) != row["source_sha256"]
            or sha256(package_file) != row["package_sha256"]
            or source_row["sha256"] != row["source_sha256"]
            or row["package_sha256"] != row["source_sha256"]
        ):
            failures.append(row["artifact_id"])
    forbidden = [row["relative_path"] for row in rows if any(token in row["relative_path"] for token in ["00_originals/", "raw_papers/", "raw_solutions/"])]
    missing = sorted(always_required - actual_ids)
    extra = sorted(actual_ids - always_required - {LOCAL_DRAFT_ID})
    if failures or forbidden or missing or extra:
        details = failures + [f"禁止文件：{path}" for path in forbidden] + [f"缺少：{item}" for item in missing] + [f"未许可：{item}" for item in extra]
        raise SystemExit("内部交接包校验失败：" + ", ".join(details))
    print(f"R01内部交接包校验：{len(rows)}/{len(rows)}通过")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--include-local-draft", action="store_true", help="显式加入仅限本地的V17 Word工作稿")
    parser.add_argument("--force", action="store_true", help="删除旧交接目录后重建")
    parser.add_argument("--validate", action="store_true", help="校验现有交接包与当前快照")
    args = parser.parse_args()
    validate() if args.validate else build(args.include_local_draft, args.force)
