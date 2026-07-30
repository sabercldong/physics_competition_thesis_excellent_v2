#!/usr/bin/env python3
"""Merge confirmed same-label prior reviews with a completed V3 delta review."""

from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
from pathlib import Path

from build_v3_author_review_package import (
    OUTPUT,
    PACKAGE_FIELDS,
    REVIEW_FIELDS,
    ROOT,
    build_package_rows,
)
from build_v3_cross_year_audit import read_rows, write_rows
from build_v3_prior_review_migration import (
    CONFIRMATION_FIELDS,
    DELTA_SCOPE,
    PRIOR_REVIEW,
    build_migration_rows,
)


DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prior", type=Path, default=PRIOR_REVIEW)
    parser.add_argument("--delta", type=Path, required=True)
    parser.add_argument("--delta-scope", type=Path, default=DELTA_SCOPE)
    parser.add_argument("--confirmation", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    args = parse_args()
    prior_path = resolve(args.prior)
    delta_path = resolve(args.delta)
    scope_path = resolve(args.delta_scope)
    confirmation_path = resolve(args.confirmation)
    output_path = resolve(args.output)
    if output_path.exists() and not args.force:
        raise SystemExit(f"输出已存在；如确认替换须使用--force: {output_path}")

    confirmation_fields, confirmation_rows = read_rows(confirmation_path)
    if confirmation_fields != CONFIRMATION_FIELDS:
        raise SystemExit("迁移确认表头与G8-80-MIGRATION-PREP规范不一致")
    if len(confirmation_rows) != 1:
        raise SystemExit("迁移确认表必须恰有1行")
    confirmation = confirmation_rows[0]
    missing = [
        field
        for field in CONFIRMATION_FIELDS
        if not confirmation.get(field, "").strip()
    ]
    if missing:
        raise SystemExit("迁移确认字段缺失: " + "、".join(missing))

    prior_hash = sha256(prior_path)
    template_hash = sha256(OUTPUT)
    if confirmation["prior_review_sha256"] != prior_hash:
        raise SystemExit("迁移确认登记的既有复核SHA-256与实际文件不一致")
    if confirmation["v3_review_template_sha256"] != template_hash:
        raise SystemExit("迁移确认登记的V3模板SHA-256与当前模板不一致")
    if confirmation["inherited_row_count"] != "337":
        raise SystemExit("迁移确认的继承行数必须为337")
    if confirmation["delta_row_count"] != "547":
        raise SystemExit("迁移确认的差异补核行数必须为547")
    if (
        confirmation["confirmation_decision"]
        != "确认337行同标签既有复核可迁移至V3"
    ):
        raise SystemExit("迁移确认决定未明确放行337行同标签记录")
    if not DATE_PATTERN.fullmatch(confirmation["confirmation_date"]):
        raise SystemExit("迁移确认日期必须为YYYY-MM-DD")
    if len(confirmation["confirmation_statement"].strip()) < 12:
        raise SystemExit("迁移确认声明少于12个字符")

    validator = ROOT / "07_analysis/scripts/validate_v3_author_review.py"
    delta_validation = subprocess.run(
        [
            sys.executable,
            str(validator),
            str(delta_path),
            "--mode",
            "filled",
            "--review-row-ids-file",
            str(scope_path),
        ],
        cwd=ROOT,
        check=False,
    )
    if delta_validation.returncode:
        raise SystemExit("547行差异补核文件未通过成品校验")

    (
        assessment_rows,
        inheritable_package_rows,
        delta_package_rows,
        _,
        prior_by_key,
    ) = build_migration_rows(prior_path)
    if len(inheritable_package_rows) != 337 or len(delta_package_rows) != 547:
        raise SystemExit("迁移评估计数与337/547门禁不一致")

    delta_fields, delta_rows = read_rows(delta_path)
    expected_fields = [*PACKAGE_FIELDS, *REVIEW_FIELDS]
    if delta_fields != expected_fields:
        raise SystemExit("差异补核表头与V3作者复核规范不一致")
    delta_by_id = {row["review_row_id"]: row for row in delta_rows}
    if len(delta_by_id) != 547:
        raise SystemExit("差异补核文件review_row_id不唯一或行数错误")

    inheritable_ids = {
        row["review_row_id"] for row in inheritable_package_rows
    }
    assessment_by_id = {
        row["review_row_id"]: row for row in assessment_rows
    }
    package_rows, _ = build_package_rows()
    merged_rows = []
    for package in package_rows:
        row_id = package["review_row_id"]
        if row_id in delta_by_id:
            merged_rows.append(delta_by_id[row_id])
            continue
        if row_id not in inheritable_ids:
            raise SystemExit(f"行既不在差异补核也不在继承候选: {row_id}")
        key = (package["item_id"], package["dimension"])
        prior = prior_by_key[key]
        if assessment_by_id[row_id]["migration_relation"] != "标签完全一致":
            raise SystemExit(f"非同标签记录被错误纳入继承: {row_id}")
        present_label = package["present_label"]
        migrated = dict(package)
        migrated.update(
            {
                "actual_author_reviewer_or_code": prior["reviewer_id"],
                "actual_review_date": prior["review_date"],
                "source_checked": prior["source_checked"],
                "question_evidence_decision": prior[
                    "evidence_sufficiency"
                ],
                "solution_evidence_decision": prior[
                    "evidence_sufficiency"
                ],
                "candidate_review_decision": "保持当前候选",
                "rechecked_present_label": present_label,
                "rechecked_level": package["level"],
                "adjacent_level_review": (
                    "认可当前相邻等级排除"
                    if present_label == "是"
                    else "维度未出现，不进入等级复核"
                ),
                "correction_reason": (
                    "迁移自R01既有复核；原相邻等级排除："
                    + prior["adjacent_level_exclusion"]
                ),
                "post_review_evidence_location": (
                    f"{prior['item_text_path']}；题干{prior['question_location']}；"
                    f"解答{prior['solution_location']}"
                ),
                "reviewer_statement": (
                    prior["reviewer_statement"]
                    + f"；{confirmation['confirmer_or_code']}于"
                    f"{confirmation['confirmation_date']}确认同标签记录可迁移至V3。"
                ),
                "author_review_status": "已完成",
            }
        )
        merged_rows.append(migrated)

    write_rows(output_path, expected_fields, merged_rows)
    full_validation = subprocess.run(
        [sys.executable, str(validator), str(output_path), "--mode", "filled"],
        cwd=ROOT,
        check=False,
    )
    if full_validation.returncode:
        output_path.unlink(missing_ok=True)
        raise SystemExit("合并后的884行文件未通过全量校验，已删除失败输出")
    print(f"migrated_rows=337")
    print(f"delta_rows=547")
    print(f"merged_rows={len(merged_rows)}")
    print(f"prior_review_sha256={prior_hash}")
    print(f"v3_template_sha256={template_hash}")
    print(f"output={output_path}")


if __name__ == "__main__":
    main()
