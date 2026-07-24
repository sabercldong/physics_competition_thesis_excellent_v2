#!/usr/bin/env python3
"""Build the GB/T 7714 candidate-reference work list from the six allowed source IDs."""

from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MANUSCRIPT_DIR = ROOT / "08_manuscript"
MAPPING_PATH = ROOT / "09_quality/g8_02_bib_lite_mapping.csv"
BIB_PATH = ROOT / "02_literature/references.bib"
OUTPUT_MD = MANUSCRIPT_DIR / "07_candidate_references.md"
OUTPUT_CSV = ROOT / "09_quality/r01_candidate_references_mapping_v1.csv"
SOURCE_ID = re.compile(r"\b(?:CS|ST|METH)-\d{3}\b")
BIB_KEY = re.compile(r"^@\w+\{([^,]+),", re.MULTILINE)
CHAPTERS = [MANUSCRIPT_DIR / f"{index:02d}_{name}.md" for index, name in [
    (1, "introduction"), (2, "theory"), (3, "methods"),
    (4, "results"), (5, "cases_and_diagnosis"), (6, "conclusion"),
]]
FORMATTED = {
    "CS-001": "中华人民共和国教育部. 普通高中物理课程标准（2017年版2020年修订）[S/OL]. 2020-06-03 [2026-07-24]. http://www.moe.gov.cn/srcsite/A26/s8001/202006/t20200603_462199.html.",
    "ST-002": "Bao L, Cai T, Koenig K, et al. Learning and scientific reasoning[J]. Science, 2009, 323(5914): 586-587. DOI:10.1126/science.1167740.",
    "ST-003": "Bao L, Koenig K, Xiao Y, et al. Theoretical model and quantitative assessment of scientific thinking and reasoning[J]. Physical Review Physics Education Research, 2022, 18(1): 010115. DOI:10.1103/PhysRevPhysEducRes.18.010115.",
    "ST-005": "Osborne J, Erduran S, Simon S. Enhancing the quality of argumentation in school science[J]. Journal of Research in Science Teaching, 2004, 41(10): 994-1020. DOI:10.1002/tea.20035.",
    "ST-006": "NGSS Lead States. Next Generation Science Standards: For States, By States[M]. Washington, DC: The National Academies Press, 2013. DOI:10.17226/18290.",
    "METH-004": "Lombard M, Snyder-Duch J, Bracken C C. Content analysis in mass communication: Assessment and reporting of intercoder reliability[J]. Human Communication Research, 2002, 28(4): 587-604. DOI:10.1111/j.1468-2958.2002.tb00826.x.",
}


def first_citation_order() -> list[str]:
    ordered = []
    for chapter in CHAPTERS:
        for line in chapter.read_text(encoding="utf-8").splitlines():
            if "[引文占位：" not in line:
                continue
            for source_id in SOURCE_ID.findall(line):
                if source_id in FORMATTED and source_id not in ordered:
                    ordered.append(source_id)
    return ordered


def main() -> None:
    with MAPPING_PATH.open(encoding="utf-8", newline="") as handle:
        mapping = {row["source_id"]: row for row in csv.DictReader(handle)}
    bib_keys = set(BIB_KEY.findall(BIB_PATH.read_text(encoding="utf-8")))
    ordered = first_citation_order()
    if set(ordered) != set(FORMATTED):
        raise SystemExit("正文来源顺序与六项候选集合不一致：" + ", ".join(ordered))
    rows = []
    for number, source_id in enumerate(ordered, start=1):
        source = mapping.get(source_id)
        if not source or source["can_enter_formal_candidate_list"] != "yes":
            raise SystemExit(f"{source_id} 不在允许候选参考文献清单中")
        if source["bib_key"] not in bib_keys:
            raise SystemExit(f"{source_id} 缺少 BibTeX 键 {source['bib_key']}")
        rows.append({
            "reference_number": number,
            "source_id": source_id,
            "bib_key": source["bib_key"],
            "first_citation_order": number,
            "gbt_7714_candidate_entry": FORMATTED[source_id],
            "allowed_use": source["allowed_use"],
            "blocked_use": source["blocked_use"],
            "remaining_verification": source["format_or_verification_gap"],
        })
    with OUTPUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    lines = [
        "# 参考文献（候选工作稿）",
        "",
        "> 本清单按华东师范大学公开格式基线的GB/T 7714-2015组织，仅列入当前六项可限边界引用来源。它不是最终参考文献表：学校基线要求硕士论文参考文献不少于30篇且含外文文献；SOLO、物理竞赛研究和其余方法文献仍待合法全文阅读与核验，暂不得加入。",
        "",
    ]
    lines.extend(f"[{row['reference_number']}] {row['gbt_7714_candidate_entry']}" for row in rows)
    lines.extend([
        "",
        "## 使用边界",
        "",
        "每条来源的可支持主张、禁止外推及版本/页码缺口见 `09_quality/r01_candidate_references_mapping_v1.csv`。正文中的来源ID占位须在最终定稿前按首次引用顺序转换为编号制引文，并与学校当期学院规范再次核对。",
    ])
    OUTPUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"候选参考文献通过：{len(rows)} 项，按正文首次引用顺序编号。")


if __name__ == "__main__":
    main()
