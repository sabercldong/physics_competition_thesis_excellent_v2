#!/usr/bin/env python3
"""Audit source-ID placeholders in the six Markdown chapters against allowed BibTeX entries."""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MANUSCRIPT_DIR = ROOT / "08_manuscript"
MAPPING_PATH = ROOT / "09_quality/g8_02_bib_lite_mapping.csv"
BIB_PATH = ROOT / "02_literature/references.bib"
OUTPUT_CSV = ROOT / "09_quality/r01_citation_trace_v1.csv"
OUTPUT_MD = ROOT / "09_quality/r01_citation_trace_v1.md"
CHAPTERS = [MANUSCRIPT_DIR / f"{index:02d}_{name}.md" for index, name in [
    (1, "introduction"),
    (2, "theory"),
    (3, "methods"),
    (4, "results"),
    (5, "cases_and_diagnosis"),
    (6, "conclusion"),
]]
SOURCE_ID = re.compile(r"\b(?:(?:CS|ST|METH|PCOMP)-\d{3}|SOLO-(?:APP|PHY)-\d{3})\b")
BIB_KEY = re.compile(r"^@\w+\{([^,]+),", re.MULTILINE)


def load_mapping() -> dict[str, dict[str, str]]:
    with MAPPING_PATH.open(encoding="utf-8", newline="") as handle:
        return {row["source_id"]: row for row in csv.DictReader(handle)}


def main() -> None:
    mapping = load_mapping()
    bib_keys = set(BIB_KEY.findall(BIB_PATH.read_text(encoding="utf-8")))
    rows: list[dict[str, str]] = []
    citation_counts: Counter[str] = Counter()
    all_counts: Counter[str] = Counter()

    for chapter in CHAPTERS:
        for line_number, line in enumerate(chapter.read_text(encoding="utf-8").splitlines(), start=1):
            source_ids = SOURCE_ID.findall(line)
            if not source_ids:
                continue
            is_placeholder = "[引文占位：" in line
            for source_id in source_ids:
                all_counts[source_id] += 1
                if is_placeholder:
                    citation_counts[source_id] += 1
                source = mapping.get(source_id)
                eligible = source is not None and source["can_enter_formal_candidate_list"] == "yes"
                bib_key = source["bib_key"] if source else ""
                bib_present = str(bool(bib_key and bib_key in bib_keys)).lower()
                result = "通过" if eligible and bib_present == "true" else (
                    "待补全文/不得升级" if source is None else "BibTeX缺失"
                )
                rows.append({
                    "chapter_file": str(chapter.relative_to(ROOT)),
                    "line_number": str(line_number),
                    "source_id": source_id,
                    "is_citation_placeholder": "是" if is_placeholder else "否（背景提及/图示/待补提示）",
                    "formal_candidate": "是" if eligible else "否",
                    "bib_key": bib_key or "[无正式候选键]",
                    "bib_key_present": bib_present if bib_key else "不适用",
                    "allowed_use": source["allowed_use"] if source else "仅按阅读状态作为待补或候选来源，不支撑正式结论",
                    "blocked_use": source["blocked_use"] if source else "不得作为正式参考文献或正文结论依据",
                    "trace_result": result,
                })

    fieldnames = list(rows[0]) if rows else []
    with OUTPUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    eligible_ids = sorted(source_id for source_id in citation_counts if source_id in mapping)
    missing_bib = sorted({row["source_id"] for row in rows if row["formal_candidate"] == "是" and row["bib_key_present"] != "true"})
    pending_ids = sorted(source_id for source_id in all_counts if source_id not in mapping)
    total_placeholder_occurrences = sum(citation_counts.values())
    md = [
        "# G8-02-R01-CITATION-TRACE：六章来源占位追溯（V1）",
        "",
        "## 范围与判断",
        "",
        "本检查只对六章 Markdown 中出现的来源 ID 进行追溯。它验证来源 ID、已许可的候选参考文献映射和工作版 BibTeX 键之间的对应关系；不验证文献全文质量，不替代学校最终引文格式，也不把待读全文来源升格为正式引用。",
        "",
        "## 结果",
        "",
        f"- 检出的来源 ID 出现次数：{sum(all_counts.values())}；其中显式 `[引文占位]` 出现次数：{total_placeholder_occurrences}。",
        f"- 已进入限边界正式候选的来源 ID：{', '.join(eligible_ids) or '无'}。",
        f"- 这些候选来源的 BibTeX 键均存在：{'是' if not missing_bib else '否，缺失：' + ', '.join(missing_bib)}。",
        f"- 仍为待补全文或仅候选的来源 ID：{', '.join(pending_ids) or '无'}。",
        "",
        "## 结论边界",
        "",
        f"1. 当前{len(eligible_ids)}项正式候选来源仍只按 `g8_02_bib_lite_mapping.csv` 中的允许范围使用，不能证明编码框架有效、学生能力、教学效果或外部效度。",
        f"2. 本轮检出的待补全文或仅候选来源（{', '.join(pending_ids) or '无'}）仅作为待补提示；它们没有被映射为正式候选参考文献。",
        "3. 最终定稿前仍须依据华东师范大学当期规范，把来源 ID 占位替换为统一的正文引文与参考文献表，并逐条复核版本、页码和 DOI/URL 规则。",
        "",
        "## 复跑",
        "",
        "```bash",
        "python3 07_analysis/scripts/audit_r01_citation_trace.py",
        "```",
    ]
    OUTPUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")

    if missing_bib:
        raise SystemExit("已许可候选来源缺少 BibTeX 键：" + ", ".join(missing_bib))
    print(f"引用追溯通过：{len(rows)} 条来源出现，{total_placeholder_occurrences} 条显式引文占位。")


if __name__ == "__main__":
    main()
