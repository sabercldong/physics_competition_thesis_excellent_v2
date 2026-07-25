#!/usr/bin/env python3
"""Validate the V18 non-submission draft's title, manifest, and citation rendering."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[2]
DOCX = ROOT / "10_outputs/drafts/ECNU_非全日制专硕论文工作稿_R01_v18.docx"
MANIFEST = ROOT / "10_outputs/drafts/ECNU_非全日制专硕论文工作稿_R01_v18_inputs.json"
TITLE = "中学生物理竞赛复赛试题的科学思维要求与教学转化研究"
STATUS = "内部工作题目，待作者/导师确认"
OUTPUT_CSV = ROOT / "09_quality/r01_v18_working_draft_qa_20260725.csv"
OUTPUT_MD = ROOT / "09_quality/r01_v18_working_draft_qa_20260725.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    with ZipFile(DOCX) as archive:
        xml = archive.read("word/document.xml").decode("utf-8")
    current_sources = all(
        (ROOT / relative).is_file() and sha256(ROOT / relative) == recorded
        for relative, recorded in manifest["source_sha256"].items()
    )
    checks = [
        ("V18-01", "DOCX存在", DOCX.is_file(), "V18 DOCX可读取"),
        ("V18-02", "内部工作题目", TITLE in xml, "封面显示25字内部候选"),
        ("V18-03", "确认状态", STATUS in xml, "封面副标题保留待确认状态"),
        ("V18-04", "非提交边界", "非提交工作稿" in xml, "DOCX声明非提交用途"),
        ("V18-05", "引文渲染", "引文占位" not in xml and "39项候选参考文献" in xml, "不显示来源占位且声明39项候选"),
        ("V18-06", "待核标记", "待补核验文献" in xml, "待核文献标记未删除"),
        ("V18-07", "输入哈希", current_sources, f"{len(manifest['source_sha256'])}项输入均与清单一致"),
    ]
    with OUTPUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["check_id", "check_item", "status", "evidence"])
        for check_id, item, passed, evidence in checks:
            writer.writerow([check_id, item, "通过" if passed else "不通过", evidence])
    failed = [check_id for check_id, _, passed, _ in checks if not passed]
    OUTPUT_MD.write_text(
        "# R01 V18非提交工作稿QA（2026-07-25）\n\n"
        f"完成{len(checks)}项检查，{'全部通过' if not failed else '不通过：' + '、'.join(failed)}。"
        "V18是当前输入哈希对应的工作稿快照；候选题目仍待作者或导师确认，"
        "候选编号与工作稿可读性不构成最终参考文献、学院格式或学校提交资格。\n",
        encoding="utf-8",
    )
    if failed:
        raise SystemExit("V18工作稿QA失败：" + ", ".join(failed))
    print(f"V18工作稿QA：{len(checks)}/{len(checks)}通过。")


if __name__ == "__main__":
    main()
