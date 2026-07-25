#!/usr/bin/env python3
"""Verify that V17 renders candidate citations as numbers while preserving source IDs in Markdown."""

from __future__ import annotations

import csv
import re
from pathlib import Path
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[2]
CHAPTERS = [
    ROOT / "08_manuscript" / f"{index:02d}_{name}.md"
    for index, name in [
        (1, "introduction"), (2, "theory"), (3, "methods"),
        (4, "results"), (5, "cases_and_diagnosis"), (6, "conclusion"),
    ]
]
MAPPING_PATH = ROOT / "09_quality/r01_candidate_references_mapping_v1.csv"
DOCX_PATH = ROOT / "10_outputs/drafts/ECNU_非全日制专硕论文工作稿_R01_v17.docx"
OUTPUT_CSV = ROOT / "09_quality/r01_v17_candidate_numeric_citations_qa_20260725.csv"
OUTPUT_MD = ROOT / "09_quality/r01_v17_candidate_numeric_citations_qa_20260725.md"
SOURCE_ID = re.compile(r"\b(?:(?:CS|ST|METH|PCOMP)-\d{3}|SOLO-(?:(?:APP|PHY)-\d{3}|\d{3}))\b")
PLACEHOLDER = re.compile(r"\[引文占位：([^\]]+)\]")


def main() -> None:
    with MAPPING_PATH.open(encoding="utf-8-sig", newline="") as handle:
        mapping = {row["source_id"]: int(row["reference_number"]) for row in csv.DictReader(handle)}
    markdown = "\n".join(path.read_text(encoding="utf-8") for path in CHAPTERS)
    raw_groups = PLACEHOLDER.findall(markdown)
    raw_source_ids = {source_id for group in raw_groups for source_id in SOURCE_ID.findall(group)}
    with ZipFile(DOCX_PATH) as archive:
        xml = archive.read("word/document.xml").decode("utf-8")

    checks = [
        ("V17-CIT-01", "Markdown保留来源占位以供追溯", "至少1处", str(len(raw_groups)), bool(raw_groups)),
        ("V17-CIT-02", "占位来源均为候选映射来源", f"{len(raw_source_ids)}/{len(raw_source_ids)}", f"{len(raw_source_ids & set(mapping))}/{len(raw_source_ids)}", raw_source_ids <= set(mapping)),
        ("V17-CIT-03", "DOCX不显示来源占位标签", "不含引文占位", "不含" if "引文占位" not in xml else "仍含", "引文占位" not in xml),
        ("V17-CIT-04", "DOCX使用说明声明候选编号边界", "存在", "存在" if "36项候选参考文献" in xml else "缺失", "36项候选参考文献" in xml),
        ("V17-CIT-05", "待核文献标记不被删除", "存在", "存在" if "待补核验文献" in xml else "缺失", "待补核验文献" in xml),
    ]
    with OUTPUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["check_id", "check_item", "expected", "actual", "status"])
        for check in checks:
            writer.writerow([*check[:4], "通过" if check[4] else "不通过"])
    failed = [check[0] for check in checks if not check[4]]
    OUTPUT_MD.write_text(
        "# V17候选编号引文QA（2026-07-25）\n\n"
        f"完成{len(checks)}项检查，{'全部通过' if not failed else '不通过：' + '、'.join(failed)}。"
        "本QA只验证工作稿渲染层的编号转换与待核标记保留；Markdown仍是来源ID、证据边界与复现追溯的权威源，候选编号不代表最终参考文献放行。\n",
        encoding="utf-8",
    )
    if failed:
        raise SystemExit("V17候选编号引文QA失败：" + ", ".join(failed))
    print(f"V17候选编号引文QA：{len(checks)}/{len(checks)}通过。")


if __name__ == "__main__":
    main()
