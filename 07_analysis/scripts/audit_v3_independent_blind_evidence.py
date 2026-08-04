#!/usr/bin/env python3
"""Audit evidence quality in a completed V3 independent blind-coding return."""

from __future__ import annotations

import argparse
import collections
import csv
import re
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SOURCE_DIR = (
    ROOT
    / "07_analysis/data/v3_independent_validation/handoff_RATER-C"
    / "原题与参考解答"
)
OUTPUT_FIELDS = (
    "blind_row_id",
    "blind_unit_no",
    "item_id",
    "dimension",
    "review_present",
    "review_level",
    "issue_codes",
    "question_evidence_quote",
    "solution_evidence_quote",
    "evidence_location",
    "adjacent_level_exclusion",
    "confidence",
)
GENERIC_REASONS = {
    "标准。",
    "纯计算。",
    "推导。",
    "计算。",
    "两步推理。l2。",
    "无主张-证据。",
    "四项门槛不满足。",
}
REVIEW_FIELDS = (
    "independent_reviewer_id",
    "review_date",
    "review_present",
    "review_level",
    "question_evidence_quote",
    "solution_evidence_quote",
    "evidence_location",
    "adjacent_level_exclusion",
    "confidence",
    "reviewer_statement",
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def normalize(text: str) -> str:
    value = unicodedata.normalize("NFKC", text or "")
    value = value.replace("−", "-").replace("–", "-").replace("—", "-")
    return re.sub(r"\s+", "", value)


def quote_is_locatable(quote: str, source: str) -> bool:
    normalized_quote = normalize(quote)
    return bool(normalized_quote) and normalized_quote in normalize(source)


def location_is_specific(location: str, filename: str) -> bool:
    if filename not in location:
        return False
    has_subquestion = bool(re.search(r"第?\s*[（(]\s*[^）)]+\s*[）)]\s*问?|小问", location))
    has_anchor = bool(re.search(r"式|段|行|页|图|表|题干|解答|原文", location))
    return has_subquestion and has_anchor


def solution_section(source: str, subquestion_no: str) -> str | None:
    """Return the Markdown solution section belonging to one analysis unit."""
    value = subquestion_no.strip()
    variants = {value}
    if "-" in value:
        major, minor = value.split("-", 1)
        variants.update({f"{major}.{minor}", f"{major}）（{minor}"})
    lines = source.splitlines()
    solution_start = next(
        (
            index + 1
            for index, line in enumerate(lines)
            if re.match(r"^##\s+参考解答", line.strip())
        ),
        None,
    )
    if solution_start is None:
        return None
    start = None
    for index in range(solution_start, len(lines)):
        line = lines[index]
        if not re.match(r"^####\s*", line):
            continue
        heading = normalize(line)
        if any(
            normalize(f"（{variant}）") in heading
            or normalize(f"({variant})") in heading
            for variant in variants
        ):
            start = index
            break
    if start is None:
        return None
    end = len(lines)
    for index in range(start + 1, len(lines)):
        if re.match(r"^####\s*", lines[index]):
            end = index
            break
    return "\n".join(lines[start:end])


def audit(
    rows: list[dict[str, str]], source_dir: Path, allow_partial: bool = False
) -> tuple[list[dict[str, str]], dict[str, int]]:
    source_texts = {
        path.name: path.read_text(encoding="utf-8") for path in source_dir.glob("*.md")
    }
    normalized_sources = {name: normalize(text) for name, text in source_texts.items()}
    active_rows: list[dict[str, str]] = []
    for row in rows:
        values = [row[field].strip() for field in REVIEW_FIELDS]
        if allow_partial and not any(values):
            continue
        active_rows.append(row)
    reason_items: dict[str, set[str]] = collections.defaultdict(set)
    for row in active_rows:
        reason = normalize(row["adjacent_level_exclusion"])
        if reason:
            reason_items[reason].add(row["item_id"])

    worklist: list[dict[str, str]] = []
    counts: collections.Counter[str] = collections.Counter()
    for row in active_rows:
        issues: list[str] = []
        if any(not row[field].strip() for field in REVIEW_FIELDS):
            issues.append("PARTIAL_REVIEW_ROW")
        source = source_texts.get(row["source_text_file"], "")
        question_quote = row["question_evidence_quote"].strip()
        solution_quote = row["solution_evidence_quote"].strip()
        reason = row["adjacent_level_exclusion"].strip()

        if len(normalize(question_quote)) < 6:
            issues.append("QUESTION_QUOTE_TOO_SHORT")
        if not quote_is_locatable(question_quote, source):
            issues.append("QUESTION_QUOTE_NOT_LOCATABLE")
            normalized_quote = normalize(question_quote)
            if len(normalized_quote) >= 8 and any(
                normalized_quote in text
                for name, text in normalized_sources.items()
                if name != row["source_text_file"]
            ):
                issues.append("QUESTION_QUOTE_MATCHES_OTHER_FILE")
        if len(normalize(solution_quote)) < 8:
            issues.append("SOLUTION_QUOTE_TOO_SHORT")
        if not quote_is_locatable(solution_quote, source):
            issues.append("SOLUTION_QUOTE_NOT_LOCATABLE")
            normalized_quote = normalize(solution_quote)
            if len(normalized_quote) >= 8 and any(
                normalized_quote in text
                for name, text in normalized_sources.items()
                if name != row["source_text_file"]
            ):
                issues.append("SOLUTION_QUOTE_MATCHES_OTHER_FILE")
        else:
            own_section = solution_section(source, row["subquestion_no"])
            if own_section is None:
                issues.append("SOLUTION_SUBQUESTION_SECTION_NOT_FOUND")
            elif not quote_is_locatable(solution_quote, own_section):
                issues.append("SOLUTION_QUOTE_OUTSIDE_SUBQUESTION")
        if row["source_text_file"] not in row["evidence_location"]:
            issues.append("EVIDENCE_LOCATION_WRONG_FILE")
        if not location_is_specific(row["evidence_location"], row["source_text_file"]):
            issues.append("EVIDENCE_LOCATION_NOT_SPECIFIC")
        if len(normalize(reason)) < 18 or reason.lower() in GENERIC_REASONS:
            issues.append("ADJACENT_REASON_TOO_GENERIC")
        if "?" in reason or "？" in reason:
            issues.append("ADJACENT_REASON_UNRESOLVED_QUESTION")
        if reason and len(reason_items[normalize(reason)]) >= 3:
            issues.append("ADJACENT_REASON_REUSED_ACROSS_ITEMS")

        if issues:
            output = {field: row[field] for field in OUTPUT_FIELDS if field != "issue_codes"}
            output["issue_codes"] = "|".join(issues)
            output = {field: output[field] for field in OUTPUT_FIELDS}
            worklist.append(output)
            counts.update(issues)

    counts["ROWS_TOTAL"] = len(rows)
    counts["ROWS_AUDITED"] = len(active_rows)
    counts["ROWS_FLAGGED"] = len(worklist)
    counts["ROWS_ALL_HIGH_CONFIDENCE"] = sum(
        row["confidence"] == "高" for row in active_rows
    )
    return worklist, dict(counts)


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--source-dir", type=Path, default=DEFAULT_SOURCE_DIR)
    parser.add_argument("--worklist", type=Path, required=True)
    parser.add_argument(
        "--allow-partial",
        action="store_true",
        help="Skip fully blank rows while auditing an in-progress return.",
    )
    args = parser.parse_args()

    rows = read_csv(args.input.resolve())
    worklist, counts = audit(rows, args.source_dir.resolve(), args.allow_partial)
    write_csv(args.worklist.resolve(), worklist)
    for key in sorted(counts):
        print(f"{key}={counts[key]}")
    if worklist:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
