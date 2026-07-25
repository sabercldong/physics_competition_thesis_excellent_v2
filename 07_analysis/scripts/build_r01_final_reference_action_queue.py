#!/usr/bin/env python3
"""Build a source-by-source final-reference verification queue from candidate mappings."""

from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MAPPING = ROOT / "09_quality/r01_candidate_references_mapping_v1.csv"
BIB = ROOT / "02_literature/references.bib"
OUTPUT_CSV = ROOT / "09_quality/r01_final_reference_action_queue_20260725.csv"
OUTPUT_MD = ROOT / "09_quality/r01_final_reference_action_queue_20260725.md"

PROVENANCE_TERMS = ("用户提供", "外部PDF", "授权", "发布链", "独立发布")
VERSION_TERMS = ("页码", "版本", "PDF", "出版社", "SOM", "postprint", "全书", "附录")
ENTRY_RE = re.compile(r"@(\w+)\{([^,]+),(.*?)(?=^@|\Z)", re.MULTILINE | re.DOTALL)
FIELD_RE = re.compile(r'^\s*(\w+)\s*=\s*[{"]([^}"]+)[}"]', re.MULTILINE)
DOI_RE = re.compile(r"DOI:([^\s]+)", re.IGNORECASE)


def normalise_doi(value: str) -> str:
    return value.strip().rstrip(".,;)").lower()


def parse_bib_dois() -> dict[str, str]:
    dois: dict[str, str] = {}
    for _entry_type, key, body in ENTRY_RE.findall(BIB.read_text(encoding="utf-8")):
        fields = {field.lower(): value.strip() for field, value in FIELD_RE.findall(body)}
        if fields.get("doi"):
            dois[key] = normalise_doi(fields["doi"])
    return dois


def priority(note: str, has_internal_identity_issue: bool) -> tuple[str, str]:
    if has_internal_identity_issue:
        return "P1", "先核对候选著录与BibTeX的内部身份字段，再核对实际使用版本、正文定位和学院格式；未核对前不得将任一字段视为最终值。"
    if any(term in note for term in PROVENANCE_TERMS):
        return "P1", "核对可引用版本、出版信息与项目可记录的来源链；不把副本来源声明写成独立认证。"
    if any(term in note for term in VERSION_TERMS):
        return "P1", "核对正文实际使用版本、页码/图表定位或出版社版本，再与候选条目逐项比对。"
    return "P2", "待学院当期格式确认后，按指定标准核对著录类型、标点、访问日期和中外文排序。"


def main() -> None:
    with MAPPING.open(encoding="utf-8-sig", newline="") as handle:
        candidates = list(csv.DictReader(handle))
    bib_dois = parse_bib_dois()
    rows: list[dict[str, str]] = []
    for candidate in candidates:
        note = candidate["remaining_verification"].strip()
        candidate_doi_match = DOI_RE.search(candidate["gbt_7714_candidate_entry"])
        candidate_doi = normalise_doi(candidate_doi_match.group(1)) if candidate_doi_match else ""
        bib_doi = bib_dois.get(candidate["bib_key"], "")
        has_internal_identity_issue = bool(candidate_doi and candidate_doi != bib_doi)
        if has_internal_identity_issue:
            note = f"{note}；项目内候选著录DOI与BibTeX字段不一致，需核对后统一"
        level, action = priority(note, has_internal_identity_issue)
        rows.append({
            "reference_number": candidate["reference_number"],
            "source_id": candidate["source_id"],
            "bib_key": candidate["bib_key"],
            "priority": level,
            "current_final_status": "候选条目，未最终放行",
            "remaining_verification": note,
            "minimum_next_action": action,
            "completion_evidence_required": "作者/导师确认的当期学院著录规则；所用版本与正文定位的一致记录；必要时来源访问/版本核对记录。",
            "prohibited_shortcut": "不得因候选条目已有DOI、PDF、编号或工作稿渲染而标为最终参考文献。",
        })
    with OUTPUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    counts = {level: sum(row["priority"] == level for row in rows) for level in ("P1", "P2")}
    OUTPUT_MD.write_text(
        "# R01最终参考文献核对行动清单（2026-07-25）\n\n"
        "## 当前状态\n\n"
        f"当前候选来源共{len(rows)}项；所有条目均为“候选条目，未最终放行”。"
        f"其中P1（版本/页码/来源链核对）{counts['P1']}项，P2（学院格式落版）{counts['P2']}项。\n\n"
        "## 使用顺序\n\n"
        "先按P1逐条确认实际使用版本与正文定位，再取得作者/导师确认的学院当期格式，最后按P2统一生成文后表。"
        "用户提供或外部副本的来源链记录只说明项目内接收状态，不替代独立发布链认证。\n\n"
        "## 不可跳过的边界\n\n"
        "候选编号、BibTeX结构完整、工作稿渲染成功和DOI存在都不足以放行最终参考文献。"
        "本清单不补造页码、版本、授权、学校规则或引文充分性判断。\n",
        encoding="utf-8",
    )
    print(f"最终参考文献行动清单：{len(rows)}项；P1={counts['P1']}，P2={counts['P2']}。")


if __name__ == "__main__":
    main()
