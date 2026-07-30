#!/usr/bin/env python3
"""Compare the completed 876-row R01 review with the 884-row V3 package."""

from __future__ import annotations

import argparse
import hashlib
from collections import Counter
from pathlib import Path

from build_v3_author_review_package import (
    OUTPUT,
    PACKAGE_FIELDS,
    REVIEW_FIELDS,
    ROOT,
    build_package_rows,
)
from build_v3_cross_year_audit import read_rows, write_rows


PRIOR_REVIEW = (
    ROOT
    / "07_analysis/data/v3_review_migration/incoming/R01/"
    "R01_第35至42届既有人工复核876行_20260723.csv"
)
ASSESSMENT = ROOT / "07_analysis/results/reviewed/V3既有人工复核迁移评估.csv"
INHERITABLE = (
    ROOT / "07_analysis/results/reviewed/V3既有人工复核同标签继承候选.csv"
)
PACKAGE_DIR = (
    ROOT / "10_outputs/material_package/V3作者实质复核分批包_G8-80-PREP"
)
DELTA_TEMPLATE = PACKAGE_DIR / "V3既有复核差异补核547行_空白.csv"
DELTA_SCOPE = PACKAGE_DIR / "V3既有复核差异补核范围547行.csv"
CONFIRMATION_TEMPLATE = PACKAGE_DIR / "V3既有人工复核迁移确认技术预填.csv"

PRIOR_FIELDS = [
    "packet_version",
    "item_id",
    "competition_no",
    "year",
    "question_no",
    "subquestion_no",
    "dimension",
    "item_text_path",
    "paper_pages",
    "solution_pages",
    "current_present",
    "current_level",
    "current_adjudication_reason",
    "source_final_coding_sha256",
    "reviewer_id",
    "review_date",
    "source_checked",
    "question_trigger_quote",
    "question_location",
    "solution_step_quote",
    "solution_location",
    "evidence_sufficiency",
    "rechecked_present",
    "rechecked_level",
    "adjacent_level_exclusion",
    "recheck_decision",
    "reviewer_statement",
]
ASSESSMENT_FIELDS = [
    "review_row_id",
    "item_id",
    "competition_no",
    "year",
    "question_no",
    "subquestion_no",
    "dimension",
    "prior_review_found",
    "prior_reviewer_id",
    "prior_review_date",
    "prior_source_checked",
    "prior_evidence_sufficiency",
    "prior_present",
    "prior_level",
    "v3_candidate_present",
    "v3_candidate_level",
    "migration_relation",
    "required_action",
    "migration_status",
    "prior_question_location",
    "prior_solution_location",
    "source_prior_review_sha256",
]
DELTA_SCOPE_FIELDS = [
    "review_row_id",
    "item_id",
    "competition_no",
    "year",
    "question_no",
    "subquestion_no",
    "dimension",
    "migration_relation",
    "prior_present",
    "prior_level",
    "v3_candidate_present",
    "v3_candidate_level",
    "required_action",
    "source_prior_review_sha256",
]
CONFIRMATION_FIELDS = [
    "prior_review_sha256",
    "v3_review_template_sha256",
    "inherited_row_count",
    "delta_row_count",
    "confirmer_or_code",
    "confirmation_date",
    "confirmation_decision",
    "confirmation_statement",
]


def resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def build_migration_rows(
    prior_path: Path = PRIOR_REVIEW,
) -> tuple[
    list[dict[str, str]],
    list[dict[str, str]],
    list[dict[str, str]],
    list[dict[str, str]],
    dict[tuple[str, str], dict[str, str]],
]:
    prior_fields, prior_rows = read_rows(prior_path)
    if prior_fields != PRIOR_FIELDS:
        raise ValueError("既有R01复核表字段与27字段归档规范不一致")
    if len(prior_rows) != 876:
        raise ValueError(f"既有R01复核表应为876行，实际为{len(prior_rows)}行")
    prior_by_key = {
        (row["item_id"], row["dimension"]): row for row in prior_rows
    }
    if len(prior_by_key) != 876:
        raise ValueError("既有R01复核表存在重复item_id×dimension")
    if any(
        not row["reviewer_id"].strip()
        or not row["review_date"].strip()
        or row["source_checked"] != "是"
        or row["evidence_sufficiency"] != "充分"
        for row in prior_rows
    ):
        raise ValueError("既有R01复核表存在未完成的身份、日期、来源或证据字段")

    package_rows, _ = build_package_rows()
    package_keys = {(row["item_id"], row["dimension"]) for row in package_rows}
    if not set(prior_by_key).issubset(package_keys):
        raise ValueError("既有R01复核表含当前V3不存在的键")
    prior_hash = hashlib.sha256(prior_path.read_bytes()).hexdigest()

    assessment_rows: list[dict[str, str]] = []
    inheritable_package_rows: list[dict[str, str]] = []
    delta_package_rows: list[dict[str, str]] = []
    delta_scope_rows: list[dict[str, str]] = []
    for package in package_rows:
        key = (package["item_id"], package["dimension"])
        prior = prior_by_key.get(key)
        if prior is None:
            relation = "V3新增分析单元"
            required_action = "必须按V3手册完成本行首次实质复核"
            migration_status = "不可继承：待差异补核"
        elif (
            prior["rechecked_present"] == package["present_label"]
            and prior["rechecked_level"] == package["level"]
        ):
            relation = "标签完全一致"
            required_action = "可列为继承候选；须另行确认V3规则迁移"
            migration_status = "继承候选：尚未确认"
        else:
            relation = "标签发生变化"
            required_action = "必须按V3手册重新判断，不能自动采用任一版本"
            migration_status = "不可继承：待差异补核"

        assessment = {
            "review_row_id": package["review_row_id"],
            "item_id": package["item_id"],
            "competition_no": package["competition_no"],
            "year": package["year"],
            "question_no": package["question_no"],
            "subquestion_no": package["subquestion_no"],
            "dimension": package["dimension"],
            "prior_review_found": "是" if prior else "否",
            "prior_reviewer_id": prior["reviewer_id"] if prior else "",
            "prior_review_date": prior["review_date"] if prior else "",
            "prior_source_checked": prior["source_checked"] if prior else "",
            "prior_evidence_sufficiency": (
                prior["evidence_sufficiency"] if prior else ""
            ),
            "prior_present": prior["rechecked_present"] if prior else "",
            "prior_level": prior["rechecked_level"] if prior else "",
            "v3_candidate_present": package["present_label"],
            "v3_candidate_level": package["level"],
            "migration_relation": relation,
            "required_action": required_action,
            "migration_status": migration_status,
            "prior_question_location": prior["question_location"] if prior else "",
            "prior_solution_location": prior["solution_location"] if prior else "",
            "source_prior_review_sha256": prior_hash,
        }
        assessment_rows.append(assessment)
        if relation == "标签完全一致":
            inheritable_package_rows.append(package)
        else:
            delta_package_rows.append(package)
            delta_scope_rows.append(
                {
                    field: assessment[field] for field in DELTA_SCOPE_FIELDS
                }
            )

    if len(assessment_rows) != 884:
        raise ValueError("迁移评估应为884行")
    if len(inheritable_package_rows) != 337:
        raise ValueError(
            f"同标签继承候选应为337行，实际为{len(inheritable_package_rows)}行"
        )
    if len(delta_package_rows) != 547:
        raise ValueError(
            f"差异补核应为547行，实际为{len(delta_package_rows)}行"
        )
    return (
        assessment_rows,
        inheritable_package_rows,
        delta_package_rows,
        delta_scope_rows,
        prior_by_key,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prior", type=Path, default=PRIOR_REVIEW)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    prior_path = resolve(args.prior)
    (
        assessment_rows,
        inheritable_rows,
        delta_rows,
        delta_scope_rows,
        _,
    ) = build_migration_rows(prior_path)
    write_rows(ASSESSMENT, ASSESSMENT_FIELDS, assessment_rows)
    inherited_ids = {row["review_row_id"] for row in inheritable_rows}
    write_rows(
        INHERITABLE,
        ASSESSMENT_FIELDS,
        [
            row
            for row in assessment_rows
            if row["review_row_id"] in inherited_ids
        ],
    )
    write_rows(
        DELTA_TEMPLATE,
        [*PACKAGE_FIELDS, *REVIEW_FIELDS],
        delta_rows,
    )
    write_rows(DELTA_SCOPE, DELTA_SCOPE_FIELDS, delta_scope_rows)
    write_rows(
        CONFIRMATION_TEMPLATE,
        CONFIRMATION_FIELDS,
        [
            {
                "prior_review_sha256": hashlib.sha256(
                    prior_path.read_bytes()
                ).hexdigest(),
                "v3_review_template_sha256": hashlib.sha256(
                    OUTPUT.read_bytes()
                ).hexdigest(),
                "inherited_row_count": "337",
                "delta_row_count": "547",
                "confirmer_or_code": "",
                "confirmation_date": "",
                "confirmation_decision": "",
                "confirmation_statement": "",
            }
        ],
    )
    relations = Counter(row["migration_relation"] for row in assessment_rows)
    dimensions = Counter(
        row["dimension"]
        for row in assessment_rows
        if row["migration_relation"] != "标签完全一致"
    )
    print(f"assessment_rows={len(assessment_rows)}")
    print(f"inheritable_rows={len(inheritable_rows)}")
    print(f"delta_rows={len(delta_rows)}")
    print(f"relations={dict(sorted(relations.items()))}")
    print(f"delta_by_dimension={dict(sorted(dimensions.items()))}")
    print(f"assessment={ASSESSMENT.relative_to(ROOT)}")
    print(f"delta_template={DELTA_TEMPLATE.relative_to(ROOT)}")
    print(f"delta_scope={DELTA_SCOPE.relative_to(ROOT)}")
    print(
        "confirmation_template="
        f"{CONFIRMATION_TEMPLATE.relative_to(ROOT)}"
    )


if __name__ == "__main__":
    main()
