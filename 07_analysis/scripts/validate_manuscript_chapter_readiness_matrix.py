#!/usr/bin/env python3
"""Validate the chapter-level readiness matrix against current manuscript files."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MATRIX = ROOT / "09_quality/manuscript_chapter_readiness_matrix_20260725.csv"
OUTPUT_CSV = ROOT / "09_quality/manuscript_chapter_readiness_matrix_qa_v1.csv"
OUTPUT_MD = ROOT / "09_quality/manuscript_chapter_readiness_matrix_qa_v1.md"

EXPECTED = {
    "CH-01": ("08_manuscript/01_introduction.md", 7),
    "CH-02": ("08_manuscript/02_theory.md", 6),
    "CH-03": ("08_manuscript/03_methods.md", 9),
    "CH-04": ("08_manuscript/04_results.md", 8),
    "CH-05": ("08_manuscript/05_cases_and_diagnosis.md", 6),
    "CH-06": ("08_manuscript/06_conclusion.md", 4),
}


def section_count(path: Path) -> int:
    return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.startswith("## "))


def main() -> None:
    with MATRIX.open(encoding="utf-8-sig", newline="") as handle:
        rows = {row["chapter_id"]: row for row in csv.DictReader(handle)}
    checks: list[tuple[str, str, bool]] = [("CH-QA-01", "矩阵记录数", len(rows) == 7)]
    for chapter_id, (relative_path, expected_sections) in EXPECTED.items():
        row = rows.get(chapter_id, {})
        path = ROOT / relative_path
        checks.append((f"{chapter_id}-QA-01", f"{chapter_id}路径", row.get("file_path") == relative_path and path.is_file()))
        checks.append((f"{chapter_id}-QA-02", f"{chapter_id}小节数", section_count(path) == expected_sections))
    abstract = rows.get("ABS-01", {})
    checks.extend([
        ("ABS-QA-01", "摘要路径", "00_abstract_content_draft.md" in abstract.get("file_path", "") and "00_abstract_en_content_draft.md" in abstract.get("file_path", "")),
        ("ABS-QA-02", "摘要文件存在", (ROOT / "08_manuscript/00_abstract_content_draft.md").is_file() and (ROOT / "08_manuscript/00_abstract_en_content_draft.md").is_file()),
        ("CH-QA-02", "第二章阻塞状态", "核心终稿阻塞" in rows["CH-02"]["current_status"]),
        ("CH-QA-03", "第四章描述性边界", "描述性结果" in rows["CH-04"]["allowed_scope"]),
        ("CH-QA-04", "第五章课堂边界", "无教师学生课堂" in rows["CH-05"]["blocking_conditions"]),
        ("CH-QA-05", "摘要格式边界", "格式未定稿" in rows["ABS-01"]["current_status"]),
    ])
    with OUTPUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["check_id", "check_item", "status"])
        writer.writerows((check_id, item, "通过" if passed else "不通过") for check_id, item, passed in checks)
    failures = [check_id for check_id, _, passed in checks if not passed]
    OUTPUT_MD.write_text(
        "# 六章工作稿就绪度矩阵QA\n\n"
        f"共完成{len(checks)}项检查，{'全部通过' if not failures else '不通过：' + '、'.join(failures)}。"
        "本QA仅核对章节文件、小节数和矩阵边界文字；不验证正文的外部事实、引文充分性、方法效度或学校格式。\n",
        encoding="utf-8",
    )
    if failures:
        raise SystemExit("六章工作稿就绪度矩阵QA失败：" + ", ".join(failures))
    print(f"六章工作稿就绪度矩阵QA：{len(checks)}/{len(checks)}通过")


if __name__ == "__main__":
    main()
