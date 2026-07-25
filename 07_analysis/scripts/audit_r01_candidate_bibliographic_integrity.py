#!/usr/bin/env python3
"""Check internal identity consistency for the current candidate-reference mapping."""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MAPPING = ROOT / "09_quality/r01_candidate_references_mapping_v1.csv"
BIB = ROOT / "02_literature/references.bib"
OUTPUT_CSV = ROOT / "09_quality/r01_candidate_bibliographic_integrity_20260725.csv"
OUTPUT_MD = ROOT / "09_quality/r01_candidate_bibliographic_integrity_20260725.md"

ENTRY_RE = re.compile(r"@(\w+)\{([^,]+),(.*?)(?=^@|\Z)", re.MULTILINE | re.DOTALL)
FIELD_RE = re.compile(r'^\s*(\w+)\s*=\s*[{"]([^}"]+)[}"]', re.MULTILINE)
DOI_RE = re.compile(r"DOI:([^\s]+)", re.IGNORECASE)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def parse_bib() -> dict[str, dict[str, str]]:
    entries: dict[str, dict[str, str]] = {}
    for _entry_type, key, body in ENTRY_RE.findall(BIB.read_text(encoding="utf-8")):
        entries[key] = {field.lower(): value.strip() for field, value in FIELD_RE.findall(body)}
    return entries


def normalise_doi(value: str) -> str:
    return value.strip().rstrip(".,;)").lower()


def main() -> None:
    mapping_rows = read_csv(MAPPING)
    bib = parse_bib()
    numbers = [int(row["reference_number"]) for row in mapping_rows]
    source_ids = [row["source_id"] for row in mapping_rows]
    bib_keys = [row["bib_key"] for row in mapping_rows]
    candidate_dois = {
        row["bib_key"]: normalise_doi(match.group(1))
        for row in mapping_rows
        if (match := DOI_RE.search(row["gbt_7714_candidate_entry"]))
    }
    bib_dois = {key: normalise_doi(fields["doi"]) for key, fields in bib.items() if fields.get("doi")}
    mapped_dois = [bib_dois[key] for key in bib_keys if key in bib_dois]
    duplicate_dois = {doi for doi, count in Counter(mapped_dois).items() if count > 1}

    rows: list[dict[str, str]] = []
    for row in mapping_rows:
        key = row["bib_key"]
        fields = bib.get(key, {})
        candidate_doi = candidate_dois.get(key, "")
        bib_doi = bib_dois.get(key, "")
        doi_status = "不适用（候选条目未列DOI）" if not candidate_doi else ("一致" if candidate_doi == bib_doi else "不一致")
        year_status = "一致" if fields.get("year") and fields["year"] in row["gbt_7714_candidate_entry"] else "不一致"
        identity_status = "通过" if key in bib and doi_status != "不一致" and year_status == "一致" and bib_doi not in duplicate_dois else "待核实"
        rows.append({
            "reference_number": row["reference_number"],
            "source_id": row["source_id"],
            "bib_key": key,
            "bib_entry_exists": "是" if key in bib else "否",
            "bib_year": fields.get("year", ""),
            "candidate_entry_year_consistency": year_status,
            "bib_doi": bib_doi or "无",
            "candidate_entry_doi": candidate_doi or "无",
            "doi_consistency": doi_status,
            "duplicate_bib_doi": "是" if bib_doi in duplicate_dois else "否",
            "internal_identity_status": identity_status,
            "boundary_note": "仅检查项目内映射、候选著录与BibTeX的一致性；不验证外部元数据、版本、页码、授权、学校格式或最终放行资格。",
        })
    summary = [
        {"reference_number": "SUMMARY-01", "source_id": "映射行数", "bib_key": str(len(mapping_rows)), "bib_entry_exists": "通过" if len(mapping_rows) == 39 else "不通过", "bib_year": "", "candidate_entry_year_consistency": "", "bib_doi": "", "candidate_entry_doi": "", "doi_consistency": "", "duplicate_bib_doi": "", "internal_identity_status": "", "boundary_note": "当前候选映射应为39项。"},
        {"reference_number": "SUMMARY-02", "source_id": "连续参考编号", "bib_key": f"{min(numbers)}-{max(numbers)}", "bib_entry_exists": "通过" if numbers == list(range(1, len(mapping_rows) + 1)) else "不通过", "bib_year": "", "candidate_entry_year_consistency": "", "bib_doi": "", "candidate_entry_doi": "", "doi_consistency": "", "duplicate_bib_doi": "", "internal_identity_status": "", "boundary_note": "编号须连续且唯一。"},
        {"reference_number": "SUMMARY-03", "source_id": "来源和BibTeX键唯一", "bib_key": f"来源{len(set(source_ids))}/{len(source_ids)}；键{len(set(bib_keys))}/{len(bib_keys)}", "bib_entry_exists": "通过" if len(set(source_ids)) == len(source_ids) and len(set(bib_keys)) == len(bib_keys) else "不通过", "bib_year": "", "candidate_entry_year_consistency": "", "bib_doi": "", "candidate_entry_doi": "", "doi_consistency": "", "duplicate_bib_doi": "", "internal_identity_status": "", "boundary_note": "来源ID和BibTeX键须唯一。"},
    ]
    write_csv(OUTPUT_CSV, rows + summary)
    passed = sum(row["internal_identity_status"] == "通过" for row in rows)
    issues = [row for row in rows if row["internal_identity_status"] != "通过"]
    markdown = [
        "# R01 候选参考文献内部身份一致性审计（2026-07-25）", "",
        f"本审计检查当前{len(rows)}项候选来源在项目内的编号、来源ID、BibTeX键、年份和DOI字段是否相互一致。内部身份一致 {passed}/{len(rows)}；待核实 {len(issues)} 项。", "",
        "这不是外部书目认证或最终参考文献放行。即使内部一致，也仍需按最终核对队列检查实际使用版本、页码或章节、正文定位、合法访问/稳定定位和学院当期格式。",
    ]
    if issues:
        markdown.extend(["", "## 待核实项", "", "| 来源ID | BibTeX键 | 原因 |", "|---|---|---|"])
        for row in issues:
            reasons = []
            if row["bib_entry_exists"] != "是": reasons.append("BibTeX条目缺失")
            if row["candidate_entry_year_consistency"] != "一致": reasons.append("候选著录年份不一致")
            if row["doi_consistency"] == "不一致": reasons.append("候选著录DOI与BibTeX不一致")
            if row["duplicate_bib_doi"] == "是": reasons.append("BibTeX DOI重复")
            markdown.append(f"| {row['source_id']} | {row['bib_key']} | {'；'.join(reasons)} |")
    OUTPUT_MD.write_text("\n".join(markdown) + "\n", encoding="utf-8")
    print(f"候选参考文献内部身份审计：{passed}/{len(rows)}通过；待核实{len(issues)}项。")


if __name__ == "__main__":
    main()
