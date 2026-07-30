#!/usr/bin/env python3
"""Split the 547-row V3 migration delta into four year-preserving batches."""

from __future__ import annotations

from build_v3_author_review_package import (
    PACKAGE_FIELDS,
    REVIEW_FIELDS,
    ROOT,
)
from build_v3_cross_year_audit import read_rows, write_rows
from build_v3_prior_review_migration import (
    DELTA_SCOPE,
    DELTA_SCOPE_FIELDS,
    DELTA_TEMPLATE,
)


OUTPUT_DIR = (
    ROOT
    / "10_outputs/material_package/V3作者实质复核分批包_G8-80-PREP/"
    "V3差异补核分届批次_G8-80-MIGRATION"
)
BATCHES = {
    "Y35-36": {
        "competitions": {"35", "36"},
        "rows": 111,
        "items": 48,
        "template": OUTPUT_DIR / "第35至36届差异补核111行_空白.csv",
        "scope": OUTPUT_DIR / "第35至36届差异补核范围111行.csv",
    },
    "Y37-38": {
        "competitions": {"37", "38"},
        "rows": 122,
        "items": 46,
        "template": OUTPUT_DIR / "第37至38届差异补核122行_空白.csv",
        "scope": OUTPUT_DIR / "第37至38届差异补核范围122行.csv",
    },
    "Y39-40": {
        "competitions": {"39", "40"},
        "rows": 160,
        "items": 63,
        "template": OUTPUT_DIR / "第39至40届差异补核160行_空白.csv",
        "scope": OUTPUT_DIR / "第39至40届差异补核范围160行.csv",
    },
    "Y41-42": {
        "competitions": {"41", "42"},
        "rows": 154,
        "items": 61,
        "template": OUTPUT_DIR / "第41至42届差异补核154行_空白.csv",
        "scope": OUTPUT_DIR / "第41至42届差异补核范围154行.csv",
    },
}
MANIFEST = OUTPUT_DIR / "V3差异补核分届批次清单.csv"
MANIFEST_FIELDS = [
    "batch_id",
    "competition_scope",
    "review_row_count",
    "item_count",
    "template_path",
    "scope_path",
    "current_status",
]


def build_batches() -> tuple[
    dict[str, list[dict[str, str]]],
    dict[str, list[dict[str, str]]],
    list[dict[str, str]],
]:
    template_fields, template_rows = read_rows(DELTA_TEMPLATE)
    scope_fields, scope_rows = read_rows(DELTA_SCOPE)
    if template_fields != [*PACKAGE_FIELDS, *REVIEW_FIELDS]:
        raise ValueError("547行差异补核模板表头不符合V3规范")
    if scope_fields != DELTA_SCOPE_FIELDS:
        raise ValueError("547行差异补核范围表头不符合迁移规范")
    if len(template_rows) != 547 or len(scope_rows) != 547:
        raise ValueError("差异补核模板和范围均应为547行")

    scope_by_id = {row["review_row_id"]: row for row in scope_rows}
    if len(scope_by_id) != 547:
        raise ValueError("差异补核范围存在重复review_row_id")

    batch_templates: dict[str, list[dict[str, str]]] = {}
    batch_scopes: dict[str, list[dict[str, str]]] = {}
    manifest_rows: list[dict[str, str]] = []
    all_ids: list[str] = []
    for batch_id, config in BATCHES.items():
        competitions = config["competitions"]
        rows = [
            row
            for row in template_rows
            if row["competition_no"] in competitions
        ]
        row_ids = {row["review_row_id"] for row in rows}
        scopes = [
            row for row in scope_rows if row["review_row_id"] in row_ids
        ]
        item_count = len({row["item_id"] for row in rows})
        if len(rows) != config["rows"]:
            raise ValueError(
                f"{batch_id}应为{config['rows']}行，实际为{len(rows)}行"
            )
        if item_count != config["items"]:
            raise ValueError(
                f"{batch_id}应涉及{config['items']}题，实际为{item_count}题"
            )
        if len(scopes) != len(rows):
            raise ValueError(f"{batch_id}模板与范围行数不一致")
        batch_templates[batch_id] = rows
        batch_scopes[batch_id] = scopes
        all_ids.extend(row["review_row_id"] for row in rows)
        manifest_rows.append(
            {
                "batch_id": batch_id,
                "competition_scope": "、".join(sorted(competitions)),
                "review_row_count": str(len(rows)),
                "item_count": str(item_count),
                "template_path": str(config["template"].relative_to(ROOT)),
                "scope_path": str(config["scope"].relative_to(ROOT)),
                "current_status": "空白：待R01完成V3差异补核",
            }
        )

    canonical_ids = [row["review_row_id"] for row in template_rows]
    if len(all_ids) != len(set(all_ids)):
        raise ValueError("分届批次之间存在重复review_row_id")
    if set(all_ids) != set(canonical_ids):
        raise ValueError("分届批次并集未精确覆盖547行")
    return batch_templates, batch_scopes, manifest_rows


def main() -> None:
    batch_templates, batch_scopes, manifest_rows = build_batches()
    fields = [*PACKAGE_FIELDS, *REVIEW_FIELDS]
    for batch_id, config in BATCHES.items():
        write_rows(config["template"], fields, batch_templates[batch_id])
        write_rows(
            config["scope"],
            DELTA_SCOPE_FIELDS,
            batch_scopes[batch_id],
        )
        print(
            f"{batch_id}: rows={len(batch_templates[batch_id])}, "
            f"items={len({row['item_id'] for row in batch_templates[batch_id]})}"
        )
    write_rows(MANIFEST, MANIFEST_FIELDS, manifest_rows)
    print(f"manifest={MANIFEST.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
