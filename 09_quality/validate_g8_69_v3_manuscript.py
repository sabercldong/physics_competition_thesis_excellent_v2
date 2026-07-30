#!/usr/bin/env python3
"""Validate the G8-69 manuscript against the V3 unique coding table."""

from __future__ import annotations

import csv
import hashlib
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UNIQUE = ROOT / "07_analysis/data/第35至42届科学思维V3唯一编码表.csv"
RESULTS = ROOT / "08_manuscript/04_results.md"
CASES = ROOT / "08_manuscript/05_cases_and_diagnosis.md"
ABSTRACT = ROOT / "08_manuscript/00_abstract_content_draft.md"
INTRO = ROOT / "08_manuscript/01_introduction.md"
THEORY = ROOT / "08_manuscript/02_theory.md"
METHODS = ROOT / "08_manuscript/03_methods.md"
CONCLUSION = ROOT / "08_manuscript/06_conclusion.md"
TEX = ROOT / "10_outputs/论文初稿_LaTeX/全国中学生物理竞赛复赛理论试题的科学思维要求及教学设计启示.tex"
PDF = ROOT / "10_outputs/论文初稿_LaTeX/build/全国中学生物理竞赛复赛理论试题的科学思维要求及教学设计启示.pdf"
LOG = ROOT / "10_outputs/论文初稿_LaTeX/build/全国中学生物理竞赛复赛理论试题的科学思维要求及教学设计启示.log"
QA_CSV = ROOT / "09_quality/g8_69_v3_manuscript_qa.csv"
QA_MD = ROOT / "09_quality/g8_69_v3_manuscript_qa.md"

EXPECTED_SHA = "c026c2c48a6ff97987896261b1a3403b35e91c9e619e352809812c0e4095c8d5"
DIMENSIONS = ("模型建构", "科学推理", "科学论证", "质疑创新")
EXPECTED_PRESENCE = {"模型建构": 202, "科学推理": 221, "科学论证": 36, "质疑创新": 2}
EXPECTED_LEVELS = {
    "模型建构": {"L1": 9, "L2": 77, "L3": 116, "L4": 0},
    "科学推理": {"L1": 13, "L2": 69, "L3": 139, "L4": 0},
    "科学论证": {"L1": 14, "L2": 16, "L3": 6, "L4": 0},
    "质疑创新": {"L1": 0, "L2": 2, "L3": 0, "L4": 0},
}
EXPECTED_CASES = {
    "CPHO41-Q06-3": {"模型建构": "L3", "科学推理": "L3", "科学论证": "未出现", "质疑创新": "未出现"},
    "CPHO41-Q07-4": {"模型建构": "L3", "科学推理": "L3", "科学论证": "L2", "质疑创新": "未出现"},
    "CPHO42-Q04-2": {"模型建构": "L3", "科学推理": "L3", "科学论证": "未出现", "质疑创新": "未出现"},
    "CPHO37-Q06-3": {"模型建构": "L3", "科学推理": "L3", "科学论证": "未出现", "质疑创新": "未出现"},
    "CPHO40-Q03-1_i": {"模型建构": "L3", "科学推理": "L3", "科学论证": "未出现", "质疑创新": "未出现"},
    "CPHO40-Q03-1_ii": {"模型建构": "未出现", "科学推理": "L1", "科学论证": "未出现", "质疑创新": "未出现"},
    "CPHO40-Q03-1_iii": {"模型建构": "L2", "科学推理": "L2", "科学论证": "未出现", "质疑创新": "未出现"},
    "CPHO40-Q03-1_iv": {"模型建构": "L2", "科学推理": "L2", "科学论证": "未出现", "质疑创新": "未出现"},
    "CPHO40-Q03-1_v": {"模型建构": "L1", "科学推理": "L2", "科学论证": "未出现", "质疑创新": "未出现"},
    "CPHO40-Q07-3": {"模型建构": "L3", "科学推理": "L3", "科学论证": "L2", "质疑创新": "未出现"},
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


checks: list[dict[str, str]] = []


def check(check_id: str, category: str, condition: bool, detail: str) -> None:
    checks.append(
        {
            "检查编号": check_id,
            "类别": category,
            "结果": "通过" if condition else "失败",
            "说明": detail,
        }
    )


with UNIQUE.open("r", encoding="utf-8-sig", newline="") as handle:
    rows = list(csv.DictReader(handle))

item_ids = {row["item_id"] for row in rows}
key_counts = Counter((row["item_id"], row["dimension"]) for row in rows)
dimensions_by_item: dict[str, set[str]] = defaultdict(set)
for row in rows:
    dimensions_by_item[row["item_id"]].add(row["dimension"])

check("G8-69-QA-01", "数据源", sha256(UNIQUE) == EXPECTED_SHA, f"唯一表SHA-256={sha256(UNIQUE)}")
check("G8-69-QA-02", "数据源", len(rows) == 884, f"编码记录={len(rows)}")
check("G8-69-QA-03", "数据源", len(item_ids) == 221, f"分析单元={len(item_ids)}")
check(
    "G8-69-QA-04",
    "数据源",
    all(count == 1 for count in key_counts.values()) and len(key_counts) == 884,
    f"唯一复合键={len(key_counts)}，重复键={sum(1 for count in key_counts.values() if count != 1)}",
)
check(
    "G8-69-QA-05",
    "数据源",
    all(dimensions_by_item[item_id] == set(DIMENSIONS) for item_id in item_ids),
    "221个分析单元均覆盖四维度",
)

presence = Counter()
levels: dict[str, Counter[str]] = defaultdict(Counter)
case_levels: dict[str, dict[str, str]] = defaultdict(dict)
for row in rows:
    level = row["level"].strip()
    if level != "未出现":
        presence[row["dimension"]] += 1
        levels[row["dimension"]][level] += 1
    if row["item_id"] in EXPECTED_CASES:
        case_levels[row["item_id"]][row["dimension"]] = level

check("G8-69-QA-06", "统计复算", dict(presence) == EXPECTED_PRESENCE, f"四维出现数={dict(presence)}")
check(
    "G8-69-QA-07",
    "统计复算",
    all({level: levels[dimension][level] for level in ("L1", "L2", "L3", "L4")} == EXPECTED_LEVELS[dimension] for dimension in DIMENSIONS),
    "四维L1至L4频数与V3正式统计一致",
)
check("G8-69-QA-08", "案例标签", case_levels == EXPECTED_CASES, f"核对案例分析单元={len(case_levels)}")

abstract_text = read_text(ABSTRACT)
intro_text = read_text(INTRO)
theory_text = read_text(THEORY)
methods_text = read_text(METHODS)
results_text = read_text(RESULTS)
cases_text = read_text(CASES)
conclusion_text = read_text(CONCLUSION)
current_result_text = "\n".join((abstract_text, intro_text, theory_text, results_text, cases_text, conclusion_text))

required_current_phrases = (
    "221个分析单元",
    "884条V3唯一编码记录",
    "模型建构、科学推理、科学论证和质疑创新分别出现于202、221、36和2个单元",
    "模型建构L3、科学推理L3、科学论证L2",
)
check(
    "G8-69-QA-09",
    "正文口径",
    all(phrase in current_result_text for phrase in required_current_phrases),
    "摘要、正文与结论包含V3正式口径和案例标签",
)

forbidden_current_phrases = (
    "共形成219个分析单元和876条",
    "四维分别出现于203、219、106和84",
    "科学论证与质疑创新共同出现于40个单元",
    "模型建构L1、科学推理L3、科学论证L1",
    "模型建构L1、科学推理L1、科学论证L3",
)
check(
    "G8-69-QA-10",
    "旧口径清理",
    not any(phrase in current_result_text for phrase in forbidden_current_phrases),
    "摘要、理论、结果、案例和结论未发现旧V2当前结果表述",
)
check(
    "G8-69-QA-11",
    "历史边界",
    "研究早期按219个分析单元形成876条V2记录" in methods_text
    and "不作为V3正式统计来源" in methods_text,
    "方法章只以明确历史边界保留V2口径",
)

figure_names = (
    "图4-1_四维度出现比例_V3.pdf",
    "图4-2_四维度等级构成_V3.pdf",
    "图4-3_各届次维度出现比例_V3.pdf",
    "图4-4_维度组合分布_V3.pdf",
)
figure_dir = ROOT / "08_manuscript/figures/v3_final"
check(
    "G8-69-QA-12",
    "图件",
    all((figure_dir / name).exists() and name in results_text for name in figure_names),
    "第四章引用四幅v3_final正式PDF图件",
)
check("G8-69-QA-13", "生成物", TEX.exists() and TEX.stat().st_size > 0, f"LaTeX源文件={TEX}")
check("G8-69-QA-14", "生成物", PDF.exists() and PDF.stat().st_size > 0, f"PDF字节数={PDF.stat().st_size if PDF.exists() else 0}")

log_text = read_text(LOG) if LOG.exists() else ""
fatal_tokens = ("Overfull", "Undefined control sequence", "Citation", "Reference", "Emergency stop", "Fatal error")
fatal_hits = [token for token in fatal_tokens if token in log_text]
check("G8-69-QA-15", "LaTeX", not fatal_hits, f"阻断性日志命中={fatal_hits or '无'}")
check(
    "G8-69-QA-16",
    "解释边界",
    "不能由100%的出现率推断所有小问结构相同或学生具有相应能力" in abstract_text
    and "不把比例起伏解释为逐年上升、下降或命题方向变化" in results_text,
    "科学推理饱和与届次描述边界已写入正文",
)

failed = [row for row in checks if row["结果"] == "失败"]
with QA_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=("检查编号", "类别", "结果", "说明"),
        lineterminator="\n",
    )
    writer.writeheader()
    writer.writerows(checks)

summary = [
    "# G8-69 V3论文口径验收报告",
    "",
    f"- 检查总数：{len(checks)}",
    f"- 通过：{len(checks) - len(failed)}",
    f"- 失败：{len(failed)}",
    f"- 唯一编码表SHA-256：`{sha256(UNIQUE)}`",
    f"- 正式PDF：`{PDF.relative_to(ROOT)}`",
    "",
    "## 验收结论",
    "",
]
if failed:
    summary.append("验收未通过，以下检查仍需处理：")
    summary.extend(f"- {row['检查编号']}：{row['说明']}" for row in failed)
else:
    summary.extend(
        [
            "16项检查全部通过。摘要、理论框架、方法章当前口径、第四章、六个案例和结论均与221个分析单元、884条V3唯一编码记录一致。",
            "",
            "旧219/876口径只在方法章作为早期V2历史过程出现，并已明确排除出V3正式统计。第四章只引用 `v3_final` 目录中的四幅正式图件；LaTeX日志未发现越界、未定义引用或编译错误。",
        ]
    )
QA_MD.write_text("\n".join(summary) + "\n", encoding="utf-8")

print(f"checks={len(checks)} passed={len(checks) - len(failed)} failed={len(failed)}")
raise SystemExit(1 if failed else 0)
