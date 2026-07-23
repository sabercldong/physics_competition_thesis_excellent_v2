from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LOCATOR = re.compile(r"(?:第\s*[0-9一二三四五六七八九十]+\s*(?:页|问|式)|page\s*\d+|p\.\s*\d+|式\s*[0-9①②③④⑤⑥⑦⑧⑨⑩])", re.IGNORECASE)
GENERIC = (
    "题干要求",
    "题面要求",
    "题面需要",
    "题干直接给出",
    "题干未要求",
    "题面未需要",
    "当前维度在",
    "A/B一致判定",
)


def read(relative: str) -> list[dict[str, str]]:
    with (ROOT / relative).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def count(rows: list[dict[str, str]], field: str) -> tuple[int, int, int]:
    values = [(row.get(field) or "").strip() for row in rows]
    return len(set(values)), sum(bool(LOCATOR.search(value)) for value in values), sum(value.startswith(GENERIC) for value in values)


def main() -> None:
    sources = [
        ("RATER-A", "07_analysis/data/rater_returns/registered/R01/formal_coding_rater_A_FILLED_20260722_registered_lf.csv", "evidence"),
        ("RATER-B", "07_analysis/data/rater_returns/registered/R01/formal_coding_rater_B_FILLED_20260722_registered_lf.csv", "evidence"),
        ("ADJUDICATION", "07_analysis/data/rater_returns/registered/R01/formal_adjudication_R01_FILLED_20260723_registered_lf.csv", "adjudicated_evidence"),
        ("FINAL", "07_analysis/data/final_coding.csv", "evidence"),
    ]
    output_rows = []
    for source, relative, field in sources:
        rows = read(relative)
        unique, located, generic = count(rows, field)
        output_rows.extend([
            {
                "check_id": f"ADMISS-{source}-01",
                "source": source,
                "metric": "记录数",
                "observed": str(len(rows)),
                "requirement": "876",
                "status": "通过" if len(rows) == 876 else "不通过",
            },
            {
                "check_id": f"ADMISS-{source}-02",
                "source": source,
                "metric": "证据文本去重数",
                "observed": str(unique),
                "requirement": "仅作模板化风险指标，不单独决定可用性",
                "status": "风险提示",
            },
            {
                "check_id": f"ADMISS-{source}-03",
                "source": source,
                "metric": "含页码/问号/式号定位符的证据数",
                "observed": f"{located}/876",
                "requirement": "进入正式结果至少应为876/876；每条记录须能回到题干或解答位置",
                "status": "通过" if located == 876 else "不通过",
            },
            {
                "check_id": f"ADMISS-{source}-04",
                "source": source,
                "metric": "以通用模板句开头的证据数",
                "observed": f"{generic}/876",
                "requirement": "通用模板句不能替代逐条定位证据",
                "status": "风险提示" if generic else "通过",
            },
        ])

    final_rows = read("07_analysis/data/final_coding.csv")
    counts = Counter(row["adjudicator"] for row in final_rows)
    output_rows.append({
        "check_id": "ADMISS-FINAL-05",
        "source": "FINAL",
        "metric": "最终表裁决者字段分布",
        "observed": "；".join(f"{key}:{value}" for key, value in sorted(counts.items())),
        "requirement": "仅用于追溯，不证明逐条证据充分性",
        "status": "风险提示",
    })
    output = ROOT / "09_quality/r01_coding_evidence_admissibility_audit_v1.csv"
    with output.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["check_id", "source", "metric", "observed", "requirement", "status"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(output_rows)
    print(f"wrote {len(output_rows)} checks to {output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
