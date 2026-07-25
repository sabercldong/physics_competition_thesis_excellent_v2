#!/usr/bin/env python3
"""Create a source-level closure register for citation placeholders in the six chapters."""

from __future__ import annotations

import csv
import re
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MANUSCRIPT = ROOT / "08_manuscript"
MAPPING = ROOT / "09_quality/g8_02_bib_lite_mapping.csv"
REFERENCES = ROOT / "02_literature/reference_verification.csv"
BIB = ROOT / "02_literature/references.bib"
OUTPUT_CSV = ROOT / "09_quality/r01_citation_closure_readiness_20260725.csv"
OUTPUT_MD = ROOT / "09_quality/r01_citation_closure_readiness_20260725.md"
QA_CSV = ROOT / "09_quality/r01_citation_closure_readiness_qa_v1.csv"
QA_MD = ROOT / "09_quality/r01_citation_closure_readiness_qa_v1.md"
CHAPTERS = [MANUSCRIPT / f"{index:02d}_{name}.md" for index, name in [
    (1, "introduction"), (2, "theory"), (3, "methods"), (4, "results"),
    (5, "cases_and_diagnosis"), (6, "conclusion"),
]]
SOURCE_ID = re.compile(r"\b(?:(?:CS|ST|METH|PCOMP)-\d{3}|SOLO-(?:(?:APP|PHY)-\d{3}|\d{3}))\b")
BIB_KEY = re.compile(r"^@\w+\{([^,]+),", re.MULTILINE)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    mapping = {row["source_id"]: row for row in read_csv(MAPPING)}
    reference = {row["id"]: row for row in read_csv(REFERENCES)}
    bib_keys = set(BIB_KEY.findall(BIB.read_text(encoding="utf-8")))
    occurrences: dict[str, list[tuple[str, int, bool]]] = defaultdict(list)
    for chapter in CHAPTERS:
        for line_number, line in enumerate(chapter.read_text(encoding="utf-8").splitlines(), start=1):
            is_placeholder = "[引文占位：" in line
            for source_id in SOURCE_ID.findall(line):
                occurrences[source_id].append((chapter.name, line_number, is_placeholder))

    rows: list[dict[str, str]] = []
    for source_id in sorted(occurrences):
        found = occurrences[source_id]
        source = mapping.get(source_id, {})
        ref = reference.get(source_id, {})
        candidate = source.get("can_enter_formal_candidate_list") == "yes"
        bib_key = source.get("bib_key", "")
        bib_ok = bool(bib_key and bib_key in bib_keys)
        if candidate and bib_ok:
            status = "候选可用，待学校格式与逐条版本复核"
        else:
            status = "待补全文/不得升级"
        locations = "；".join(f"{name}:{line}" for name, line, _ in found)
        rows.append({
            "source_id": source_id,
            "source_occurrences": str(len(found)),
            "explicit_placeholder_occurrences": str(sum(marked for _, _, marked in found)),
            "manuscript_locations": locations,
            "formal_candidate": "是" if candidate else "否",
            "bib_key": bib_key or "[无正式候选键]",
            "bib_key_present": "是" if bib_ok else "否/不适用",
            "full_text_status": ref.get("full_text_available", "未在核验台账登记"),
            "passage_checked": ref.get("relevant_passage_checked", "未在核验台账登记"),
            "allowed_use": source.get("allowed_use", "仅作为待补提示，不支撑正式结论"),
            "blocked_use": source.get("blocked_use", "不得作为正式参考文献或正文结论依据"),
            "format_or_verification_gap": source.get("format_or_verification_gap", ref.get("notes", "待补核验")),
            "remaining_action": source.get("remaining_action", "取得合法全文、完成页码阅读和受控引用决定"),
            "closure_status": status,
        })

    fields = list(rows[0])
    for path in [OUTPUT_CSV, QA_CSV]:
        path.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    candidate_rows = [row for row in rows if row["formal_candidate"] == "是"]
    pending_rows = [row for row in rows if row["closure_status"] == "待补全文/不得升级"]
    checks = [
        ("CCQA-01", "六章文件存在", "6/6", f"{sum(path.is_file() for path in CHAPTERS)}/6", all(path.is_file() for path in CHAPTERS)),
        ("CCQA-02", "来源级清单覆盖正文来源ID", str(len(occurrences)), str(len(rows)), set(occurrences) == {row["source_id"] for row in rows}),
        ("CCQA-03", "来源级清单定位数覆盖正文出现数", str(sum(len(value) for value in occurrences.values())), str(sum(int(row["source_occurrences"]) for row in rows)), sum(len(value) for value in occurrences.values()) == sum(int(row["source_occurrences"]) for row in rows)),
        ("CCQA-04", "候选来源均有BibTeX键", str(len(candidate_rows)), str(sum(row["bib_key_present"] == "是" for row in candidate_rows)), all(row["bib_key_present"] == "是" for row in candidate_rows)),
        ("CCQA-05", "待补来源保持禁止升级", str(len(pending_rows)), str(sum(row["formal_candidate"] == "否" for row in pending_rows)), all(row["formal_candidate"] == "否" for row in pending_rows)),
        ("CCQA-06", "待补来源均有行动说明", str(len(pending_rows)), str(sum(bool(row["remaining_action"]) for row in pending_rows)), all(row["remaining_action"] for row in pending_rows)),
    ]
    with QA_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["check_id", "check_item", "expected", "actual", "status"])
        for check in checks:
            writer.writerow([*check[:4], "通过" if check[4] else "不通过"])
    failures = [check[0] for check in checks if not check[4]]
    OUTPUT_MD.write_text(
        "# R01引文关闭就绪度清单\n\n"
        f"正文检出{len(rows)}个来源ID、{sum(len(value) for value in occurrences.values())}次出现；"
        f"其中{len(candidate_rows)}项为受限候选，{len(pending_rows)}项仍待补全文或不得升级。\n\n"
        "本清单把每个来源定位至正文行号，并继承候选映射的允许用途、禁止用途和下一步。"
        "它不将候选条目变成最终参考文献，不验证全文质量或学校格式，也不允许待补来源进入实质结论。\n",
        encoding="utf-8",
    )
    QA_MD.write_text(
        "# R01引文关闭就绪度QA\n\n"
        f"共{len(checks)}项检查，{'全部通过' if not failures else '不通过：' + '、'.join(failures)}。"
        "本QA仅验证来源ID覆盖、行号定位、候选BibTeX键和待补来源隔离；不验证文献全文、引用充分性或学校最终格式。\n",
        encoding="utf-8",
    )
    if failures:
        raise SystemExit("引文关闭就绪度QA失败：" + ", ".join(failures))
    print(f"R01引文关闭就绪度QA：{len(checks)}/{len(checks)}通过；候选{len(candidate_rows)}项，待补{len(pending_rows)}项")


if __name__ == "__main__":
    main()
