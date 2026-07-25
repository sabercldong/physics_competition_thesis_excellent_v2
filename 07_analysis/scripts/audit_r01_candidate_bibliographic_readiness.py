#!/usr/bin/env python3
"""Audit structural bibliographic readiness of the bounded R01 reference list."""

from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MAPPING_PATH = ROOT / "09_quality/r01_candidate_references_mapping_v1.csv"
BIB_PATH = ROOT / "02_literature/references.bib"
OUTPUT_CSV = ROOT / "09_quality/r01_candidate_bibliographic_readiness_20260725.csv"
OUTPUT_MD = ROOT / "09_quality/r01_candidate_bibliographic_readiness_20260725.md"

BIB_ENTRY = re.compile(r"@(\w+)\{([^,]+),(.*?)(?=^@|\Z)", re.MULTILINE | re.DOTALL)
BIB_FIELD = re.compile(r'^\s*(\w+)\s*=\s*[\{"]', re.MULTILINE)
TYPE_MARKER = re.compile(r"\[(?:J|M|D|S/OL)\]")
DOI = re.compile(r"DOI:\S+", re.IGNORECASE)
URL = re.compile(r"https?://\S+", re.IGNORECASE)
JOURNAL_LOCATOR = re.compile(r",\s*\d{4}(?:,\s*\d+)?\s*\([^)]*\)\s*:|,\s*\d{4},\s*\d+\s*:")
BOOK_LOCATOR = re.compile(r"\[M\]\.\s+[^:]+:\s+[^,]+,\s*\d{4}")
THESIS_LOCATOR = re.compile(r"\[D\]\.\s+[^,]+,\s*\d{4}")
STANDARD_LOCATOR = re.compile(r"\[S/OL\]\.\s+\d{4}-\d{2}-\d{2}\s+\[\d{4}-\d{2}-\d{2}\]\.")


def parse_bib() -> dict[str, dict[str, object]]:
    entries: dict[str, dict[str, object]] = {}
    for entry_type, key, body in BIB_ENTRY.findall(BIB_PATH.read_text(encoding="utf-8")):
        entries[key] = {"entry_type": entry_type, "fields": set(BIB_FIELD.findall(body))}
    return entries


def has_locator(entry: str) -> bool:
    if TYPE_MARKER.search(entry) is None:
        return False
    if "[J]" in entry:
        return bool(DOI.search(entry) or JOURNAL_LOCATOR.search(entry))
    if "[M]" in entry:
        return bool(DOI.search(entry) or BOOK_LOCATOR.search(entry))
    if "[D]" in entry:
        return bool(THESIS_LOCATOR.search(entry))
    return bool(STANDARD_LOCATOR.search(entry) and URL.search(entry))


def main() -> None:
    with MAPPING_PATH.open(encoding="utf-8-sig", newline="") as handle:
        candidates = list(csv.DictReader(handle))
    bib = parse_bib()
    rows: list[dict[str, str]] = []
    for row in candidates:
        key = row["bib_key"]
        fields = bib.get(key, {}).get("fields", set())
        entry = row["gbt_7714_candidate_entry"].strip()
        required_bib_fields = {"author", "title", "year"}
        bib_fields_ready = required_bib_fields <= fields
        entry_type_ready = bool(TYPE_MARKER.search(entry))
        locator_ready = has_locator(entry)
        structural_ready = bib_fields_ready and entry_type_ready and locator_ready
        rows.append({
            "reference_number": row["reference_number"],
            "source_id": row["source_id"],
            "bib_key": key,
            "bib_entry_exists": "是" if key in bib else "否",
            "bib_core_fields_author_title_year": "是" if bib_fields_ready else "否",
            "candidate_type_marker": TYPE_MARKER.search(entry).group(0) if TYPE_MARKER.search(entry) else "缺失",
            "publication_locator_ready": "是" if locator_ready else "否",
            "candidate_structure_ready": "是" if structural_ready else "否",
            "final_reference_ready": "否",
            "remaining_verification": row["remaining_verification"],
            "boundary_note": "结构性就绪仅表示可生成候选著录；不表示全文、版本、页码、学校格式或最终引用充分性已闭合。",
        })

    with OUTPUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    structure_count = sum(row["candidate_structure_ready"] == "是" for row in rows)
    markdown = [
        "# R01 候选参考文献书目信息就绪度审计（2026-07-25）",
        "",
        f"审计对象为当前 {len(rows)} 项限边界候选来源。BibTeX核心字段（作者、题名、年份）、候选条目类型标识和出版定位信息均由脚本逐条核对；结果为结构性就绪 {structure_count}/{len(rows)}。",
        "",
        "这不是最终参考文献放行：每一条仍保留原映射表中的全文、版本/页码或学校格式核验事项，故最终参考文献就绪度为 0/36。该数字不表示条目无价值，而是禁止把候选工作稿误写为提交版文后表。",
        "",
        "出版定位规则为：期刊条目需有 DOI 或年份—卷期—页码/文章号；图书需有 DOI 或出版地—出版社—年份；学位论文需有授予单位—年份；标准在线条目需有发布日期、访问日期与 URL。审计不联网验证 DOI/URL 可访问性，不判断文献是否足以支持具体论断，也不替代学校答辩期格式要求。",
    ]
    OUTPUT_MD.write_text("\n".join(markdown) + "\n", encoding="utf-8")
    if structure_count != len(rows):
        missing = [row["source_id"] for row in rows if row["candidate_structure_ready"] != "是"]
        raise SystemExit("候选条目结构不完整：" + ", ".join(missing))
    print(f"候选参考文献书目信息审计：{structure_count}/{len(rows)}结构性就绪；最终文后表 0/{len(rows)}放行。")


if __name__ == "__main__":
    main()
