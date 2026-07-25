#!/usr/bin/env python3
"""Validate the bounded SOLO-application integration packet before chapter editing."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REFERENCE = ROOT / "02_literature/reference_verification.csv"
PACKET = ROOT / "09_quality/solo_application_integration_packet_v1.csv"
PACKET_MD = ROOT / "09_quality/solo_application_integration_packet_v1.md"
THEORY = ROOT / "08_manuscript/02_theory.md"
OUTPUT_CSV = ROOT / "09_quality/solo_application_integration_packet_v1_qa.csv"
OUTPUT_MD = ROOT / "09_quality/solo_application_integration_packet_v1_qa.md"

REQUIRED = {
    "SOLO-APP-001": ("molmatos2025solo", "02_literature/solo_task_analysis_mol_matos_2025_reading_notes.md"),
    "SOLO-PHY-001": ("xiao2020solo", "02_literature/solo_physics_item_xiao_2020_reading_notes.md"),
    "SOLO-PHY-002": ("yu2025sololps", "02_literature/solo_physics_exam_yu_2025_reading_notes.md"),
    "SOLO-PHY-003": ("wangyu2023bloomsolo", "02_literature/solo_bloom_physics_item_comparison_wang_yu_2023_reading_notes.md"),
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    references = {row["id"]: row for row in read_csv(REFERENCE)}
    packet_rows = {row["source_id"]: row for row in read_csv(PACKET)}
    packet_text = PACKET_MD.read_text(encoding="utf-8")
    theory_text = THEORY.read_text(encoding="utf-8")

    checks: list[tuple[str, str, str, str, bool]] = []
    checks.append((
        "SAIP-QA-01", "接入包来源覆盖", str(len(REQUIRED)), str(len(packet_rows)),
        set(packet_rows) == set(REQUIRED),
    ))
    for source_id, (bib_key, note) in REQUIRED.items():
        source = references.get(source_id, {})
        row = packet_rows.get(source_id, {})
        checks.append((
            f"SAIP-QA-{len(checks) + 1:02d}", f"{source_id} 全文与相关段落", "是/是",
            f"{source.get('full_text_available', '缺失')}/{source.get('relevant_passage_checked', '缺失')}",
            source.get("full_text_available", "").startswith("是") and source.get("relevant_passage_checked") == "是",
        ))
        checks.append((
            f"SAIP-QA-{len(checks) + 1:02d}", f"{source_id} 阅读札记", "存在", "存在" if (ROOT / note).is_file() else "缺失",
            (ROOT / note).is_file(),
        ))
        checks.append((
            f"SAIP-QA-{len(checks) + 1:02d}", f"{source_id} 拟用BibTeX键", bib_key,
            row.get("bib_key", "缺失"), row.get("bib_key") == bib_key,
        ))
        checks.append((
            f"SAIP-QA-{len(checks) + 1:02d}", f"{source_id} 禁止迁移", "已登记",
            "已登记" if row.get("blocked_use") else "缺失", bool(row.get("blocked_use")),
        ))
    checks.append((
        f"SAIP-QA-{len(checks) + 1:02d}", "原典全文缺口仍保留", "存在",
        "存在" if "SOLO-002" in theory_text and "[待补核验文献]" in theory_text else "缺失",
        "SOLO-002" in theory_text and "[待补核验文献]" in theory_text,
    ))
    required_terms = [
        "不替代 `SOLO-001`、`SOLO-002` 原典全文",
        "SOLO-APP-001、SOLO-PHY-001",
        "SOLO-PHY-002、SOLO-PHY-003",
        "分值加权或学生结论",
        "学生实际作答",
    ]
    checks.append((
        f"SAIP-QA-{len(checks) + 1:02d}", "建议段落与禁止外推边界", "存在",
        "存在" if all(term in packet_text for term in required_terms) else "缺失",
        all(term in packet_text for term in required_terms),
    ))
    checks.append((
        f"SAIP-QA-{len(checks) + 1:02d}", "一次性接入复跑链", "存在",
        "存在" if "build_r01_candidate_references.py" in packet_text and "build_r01_material_package_snapshot.py --validate" in packet_text else "缺失",
        "build_r01_candidate_references.py" in packet_text and "build_r01_material_package_snapshot.py --validate" in packet_text,
    ))

    with OUTPUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["check_id", "check_item", "expected", "actual", "status"])
        for check in checks:
            writer.writerow([*check[:4], "通过" if check[4] else "不通过"])
    failures = [check[0] for check in checks if not check[4]]
    OUTPUT_MD.write_text(
        "# SOLO应用文献受控接入包 QA（V1）\n\n"
        f"共完成{len(checks)}项检查，{'全部通过' if not failures else '不通过：' + '、'.join(failures)}。"
        "本QA只核对已读来源、接入包和现有理论边界的一致性；不表示正文已改写、原典已读、框架已获外部效度或学生/教师/课堂证据已存在。\n",
        encoding="utf-8",
    )
    if failures:
        raise SystemExit("SOLO应用接入包QA失败：" + ", ".join(failures))
    print(f"SOLO应用文献受控接入包QA：{len(checks)}/{len(checks)}通过")


if __name__ == "__main__":
    main()
