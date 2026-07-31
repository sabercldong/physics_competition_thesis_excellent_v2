#!/usr/bin/env python3
"""Replace legacy source-ID citation placeholders with formal superscript numbers."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MAPPING = ROOT / "09_quality/r01_candidate_references_mapping_v1.csv"
MANUSCRIPT_DIR = ROOT / "08_manuscript"
AUDIT = ROOT / "09_quality/G8-85正式引文转换登记.csv"
SOURCE_FILES = [
    MANUSCRIPT_DIR / "00_abstract_content_draft.md",
    MANUSCRIPT_DIR / "00_abstract_en_content_draft.md",
    MANUSCRIPT_DIR / "01_introduction.md",
    MANUSCRIPT_DIR / "02_theory.md",
    MANUSCRIPT_DIR / "03_methods.md",
    MANUSCRIPT_DIR / "04_results.md",
    MANUSCRIPT_DIR / "05_cases_and_diagnosis.md",
    MANUSCRIPT_DIR / "06_conclusion.md",
]
PATTERN = re.compile(r"\[引文占位：([^\]]+)\]")


def load_mapping() -> dict[str, str]:
    with MAPPING.open(encoding="utf-8-sig", newline="") as handle:
        return {
            row["source_id"]: row["reference_number"]
            for row in csv.DictReader(handle)
        }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write replacements to manuscript files; otherwise perform a dry run.",
    )
    args = parser.parse_args()
    mapping = load_mapping()
    audit_rows: list[dict[str, str | int]] = []
    missing: set[str] = set()
    marker_count = 0

    for path in SOURCE_FILES:
        text = path.read_text(encoding="utf-8")
        file_index = 0

        def replace(match: re.Match[str]) -> str:
            nonlocal marker_count, file_index
            marker_count += 1
            file_index += 1
            source_ids = [
                source_id.strip()
                for source_id in match.group(1).split("；", 1)[0].split("、")
            ]
            unknown = [source_id for source_id in source_ids if source_id not in mapping]
            missing.update(unknown)
            if unknown:
                return match.group(0)
            numbers = [mapping[source_id] for source_id in source_ids]
            replacement = rf"\textsuperscript{{[{', '.join(numbers)}]}}"
            line_number = text.count("\n", 0, match.start()) + 1
            audit_rows.append(
                {
                    "章节文件": str(path.relative_to(ROOT)),
                    "文件内序号": file_index,
                    "原行号": line_number,
                    "来源ID": "、".join(source_ids),
                    "参考文献编号": "、".join(numbers),
                    "正式上标": replacement,
                }
            )
            return replacement

        converted = PATTERN.sub(replace, text)
        if args.write and converted != text:
            path.write_text(converted, encoding="utf-8")

    if missing:
        raise ValueError(f"Missing reference mappings: {sorted(missing)}")
    if marker_count == 0:
        print("PASS: no legacy citation placeholders remain")
        return

    if args.write:
        with AUDIT.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=[
                    "章节文件",
                    "文件内序号",
                    "原行号",
                    "来源ID",
                    "参考文献编号",
                    "正式上标",
                ],
            )
            writer.writeheader()
            writer.writerows(audit_rows)
        remaining = sum(
            len(PATTERN.findall(path.read_text(encoding="utf-8")))
            for path in SOURCE_FILES
        )
        if remaining:
            raise ValueError(f"{remaining} legacy citation placeholders remain")
        print(
            f"PASS: converted {marker_count} citation markers and wrote "
            f"{AUDIT.relative_to(ROOT)}"
        )
    else:
        print(f"DRY RUN: {marker_count} citation markers are ready for conversion")


if __name__ == "__main__":
    main()
