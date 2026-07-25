#!/usr/bin/env python3
"""Validate page-level, bounded intake of user-provided CPHO research PDFs."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MAP = ROOT / "02_literature/physics_competition_page_level_claim_map_v1.csv"
NOTES = ROOT / "02_literature/physics_competition_page_level_reading_notes_20260725.md"
PACKET = ROOT / "02_literature/physics_competition_theory_insertion_packet_20260725.md"
OUTPUT = ROOT / "09_quality/pcomp_page_level_intake_qa_v1.csv"
REPORT = ROOT / "09_quality/pcomp_page_level_intake_qa_v1.md"
EXPECTED_IDS = {"PCOMP-002", "PCOMP-003", "PCOMP-004", "PCOMP-007", "PCOMP-008"}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    rows = read_csv(MAP)
    notes = NOTES.read_text(encoding="utf-8")
    packet = PACKET.read_text(encoding="utf-8")
    checks: list[tuple[str, str, bool, str]] = []

    def check(check_id: str, item: str, passed: bool, source: str) -> None:
        checks.append((check_id, item, passed, source))

    ids = {row["source_id"] for row in rows}
    check("PCOMP-PAGE-QA-01", "五项用户提供来源均有页码级映射", ids == EXPECTED_IDS, MAP.name)
    check("PCOMP-PAGE-QA-02", "映射至少14条且每条均有PDF页", len(rows) >= 14 and all(row["pdf_page"].isdigit() for row in rows), MAP.name)
    check("PCOMP-PAGE-QA-03", "所有映射均保持E1", all(row["evidence_level"] == "E1" for row in rows), MAP.name)
    check("PCOMP-PAGE-QA-04", "龚枭页码覆盖对象、内容与统计起点", {(row["source_id"], row["pdf_page"]) for row in rows} >= {("PCOMP-002", "12"), ("PCOMP-002", "15"), ("PCOMP-002", "24")}, MAP.name)
    check("PCOMP-PAGE-QA-05", "唐路映射明确题目与成绩资料分开", any(row["source_id"] == "PCOMP-003" and "成绩" in row["source_observation"] for row in rows), MAP.name)
    check("PCOMP-PAGE-QA-06", "张豇萌映射明确八因素和成绩资料边界", any(row["source_id"] == "PCOMP-008" and "八因素" in row["source_observation"] for row in rows), MAP.name)
    check("PCOMP-PAGE-QA-07", "阅读补充保留五来源与不可迁移边界", all(source_id in notes for source_id in EXPECTED_IDS) and "不采用" in notes, NOTES.name)
    check("PCOMP-PAGE-QA-08", "插入包未直接改写并行第二章", "不直接写入正文" in packet and "08_manuscript/02_theory.md" in packet, PACKET.name)
    check("PCOMP-PAGE-QA-09", "插入段包含五来源页码占位", all(source_id in packet for source_id in EXPECTED_IDS) and "PDF第12、15、24页" in packet, PACKET.name)
    forbidden = ["显著", "证明", "学生能力", "趋势"]
    check("PCOMP-PAGE-QA-10", "插入段不迁移禁用结论", not any(token in packet.split("## 合并后核验")[0] for token in forbidden), PACKET.name)

    with OUTPUT.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(("check_id", "check_item", "status", "source"))
        for check_id, item, passed, source in checks:
            writer.writerow((check_id, item, "通过" if passed else "不通过", source))
    failures = [check_id for check_id, _, passed, _ in checks if not passed]
    REPORT.write_text(
        "# 国内物理竞赛研究页码级接收QA\n\n"
        f"检查结果：{len(checks) - len(failures)}/{len(checks)}通过。\n\n"
        "本QA只检查五份用户提供全文的页码映射、受限插入包和禁用边界；"
        "不验证外部PDF的出版链、来源作者的统计/分类有效性或本项目的理论效度。\n",
        encoding="utf-8",
    )
    if failures:
        raise SystemExit("国内竞赛研究页码级接收QA未通过：" + ", ".join(failures))
    print(f"国内竞赛研究页码级接收QA：{len(checks)}/{len(checks)}通过")


if __name__ == "__main__":
    main()
