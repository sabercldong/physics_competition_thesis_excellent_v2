#!/usr/bin/env python3
"""Validate bounded manuscript integration of newly read external sources."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[2]
THEORY = ROOT / "08_manuscript/02_theory.md"
METHODS = ROOT / "08_manuscript/03_methods.md"
MAPPING = ROOT / "09_quality/g8_02_bib_lite_mapping.csv"
BIB = ROOT / "02_literature/references.bib"
CLAIMS = ROOT / "09_quality/claim_evidence_matrix.csv"
DRAFT = ROOT / "10_outputs/drafts/ECNU_非全日制专硕论文工作稿_R01_v17.docx"
MANIFEST = ROOT / "10_outputs/drafts/ECNU_非全日制专硕论文工作稿_R01_v17_inputs.json"
OUTPUT_CSV = ROOT / "09_quality/g2_13_controlled_integration_qa_20260725.csv"
OUTPUT_MD = ROOT / "09_quality/g2_13_controlled_integration_qa_20260725.md"


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    theory = THEORY.read_text(encoding="utf-8")
    methods = METHODS.read_text(encoding="utf-8")
    mapping = {row["source_id"]: row for row in csv_rows(MAPPING)}
    claims = {row["claim_id"]: row for row in csv_rows(CLAIMS)}
    bib = BIB.read_text(encoding="utf-8")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    manifest_current = all(
        (ROOT / relative).is_file()
        and hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == recorded
        for relative, recorded in manifest["source_sha256"].items()
    )
    with ZipFile(DRAFT) as archive:
        draft_xml = archive.read("word/document.xml").decode("utf-8")
    sources = {"SOLO-002", "METH-002", "METH-003"}
    checks = [
        ("G213-QA-01", "三项来源均进入许可映射", all(mapping.get(source, {}).get("can_enter_formal_candidate_list") == "yes" for source in sources)),
        ("G213-QA-02", "三项BibTeX键存在", all("@" in bib and "{" + mapping[source]["bib_key"] + "," in bib for source in sources)),
        ("G213-QA-03", "SOLO-002正文限定任务与学生表现边界", "[引文占位：SOLO-002" in theory and "不直接给出当前四维编码或L1至L4的效度依据" in theory),
        ("G213-QA-04", "SOLO-002不迁移学生或教学结论", "不迁移课程目标、学生水平或教学结论" in theory),
        ("G213-QA-05", "METH-002/003正文限定前提与解释", "[引文占位：METH-002、METH-003、METH-007" in methods and "不把任何历史区间设为通过线" in methods),
        ("G213-QA-06", "评分独立性限制仍保留", "评分过程只能按自声明登记" in methods),
        ("G213-QA-07", "METH-001版本缺口仍保留", "METH-001、METH-005" in theory and "目标版本为2018年第4版" in theory),
        ("G213-QA-08", "PCOMP-001只更新阅读状态且不进候选", "PCOMP-001`也已读但因文本层劣化未纳入正文候选" in theory and mapping.get("PCOMP-001", {}).get("can_enter_formal_candidate_list") != "yes"),
        ("G213-QA-09", "SOLO主张矩阵同步受限页码", "SOLO-002 PDF页1及11至12" in claims["C2-03A"]["evidence_location"]),
        ("G213-QA-10", "方法主张矩阵同步阈值限制", "不机械设阈值" in claims["C2-04"]["risk"]),
        ("G213-QA-11", "V17输入清单相对当前源文件一致", manifest_current),
        ("G213-QA-12", "V17说明同步当前候选文献数", f"{len(mapping)}项候选参考文献" in draft_xml),
    ]
    with OUTPUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["check_id", "check_item", "status"])
        for check_id, item, passed in checks:
            writer.writerow([check_id, item, "通过" if passed else "不通过"])
    failures = [check_id for check_id, _, passed in checks if not passed]
    OUTPUT_MD.write_text(
        "# G2-13 新读全文受控接入 QA\n\n"
        f"共{len(checks)}项，{'全部通过' if not failures else '不通过：' + '、'.join(failures)}。"
        "本QA只验证三篇来源的已读页码、许可映射、正文限制语和主张矩阵同步；不核验外部副本授权、评分过程独立性、框架效度、学生能力或教学效果。\n",
        encoding="utf-8",
    )
    if failures:
        raise SystemExit("G2-13受控接入QA失败：" + ", ".join(failures))
    print(f"G2-13受控接入QA：{len(checks)}/{len(checks)}通过")


if __name__ == "__main__":
    main()
