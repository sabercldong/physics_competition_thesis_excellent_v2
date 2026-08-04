#!/usr/bin/env python3
"""Build the author-authorized analysis table without overwriting the V3 baseline."""

from __future__ import annotations

import csv
import hashlib
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BASELINE = ROOT / "07_analysis/data/第35至42届科学思维第三版唯一编码表.csv"
ADJUDICATION = (
    ROOT
    / "07_analysis/data/v3_independent_validation/adjudication"
    / "完整原文复核_146行_20260803/第二轮交叉审计后结果"
    / "第二轮交叉审计后完整原文候选裁决表_146行.csv"
)
OUTPUT_DIR = ROOT / "07_analysis/data/作者授权采用分析版"
OUTPUT = OUTPUT_DIR / "第35至42届科学思维作者授权采用分析表.csv"
ADOPTION = OUTPUT_DIR / "三方分歧交叉审计后采用记录.csv"
PROVENANCE = OUTPUT_DIR / "作者授权采用分析版来源登记.csv"

VALID_LABELS = {"未出现", "L1", "L2", "L3", "L4"}
DIMENSIONS = {"模型建构", "科学推理", "科学论证", "质疑创新"}


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def label_pair(label: str) -> tuple[str, str, str]:
    if label == "未出现":
        return "0", "否", "未出现"
    return "1", "是", label


def main() -> None:
    baseline_fields, baseline_rows = read_csv(BASELINE)
    adjudication_fields, adjudication_rows = read_csv(ADJUDICATION)

    if len(baseline_rows) != 884:
        raise SystemExit(f"第三版基线应为884行，实际为{len(baseline_rows)}行")
    if len(adjudication_rows) != 146:
        raise SystemExit(f"交叉审计表应为146行，实际为{len(adjudication_rows)}行")
    required_adjudication_fields = {
        "裁决序号",
        "第三版源记录",
        "item_id",
        "维度",
        "交叉审计后裁决标签",
        "交叉审计后裁决依据",
        "交叉审计后证据位置",
        "交叉审计后置信度",
        "交叉审计后状态",
    }
    if not required_adjudication_fields.issubset(adjudication_fields):
        missing = sorted(required_adjudication_fields - set(adjudication_fields))
        raise SystemExit(f"交叉审计表缺少字段：{missing}")

    baseline_by_id = {row["review_row_id"]: row for row in baseline_rows}
    if len(baseline_by_id) != 884:
        raise SystemExit("第三版基线review_row_id存在重复")
    adjudication_by_id = {
        row["第三版源记录"]: row for row in adjudication_rows
    }
    if len(adjudication_by_id) != 146:
        raise SystemExit("交叉审计表第三版源记录存在重复")

    adoption_rows: list[dict[str, str]] = []
    changed = 0
    for review_id, adjudication in adjudication_by_id.items():
        baseline = baseline_by_id.get(review_id)
        if baseline is None:
            raise SystemExit(f"交叉审计记录无法映射第三版：{review_id}")
        if baseline["item_id"] != adjudication["item_id"]:
            raise SystemExit(f"item_id不一致：{review_id}")
        if baseline["dimension"] != adjudication["维度"]:
            raise SystemExit(f"维度不一致：{review_id}")
        final_label = adjudication["交叉审计后裁决标签"]
        if final_label not in VALID_LABELS:
            raise SystemExit(f"非法裁决标签：{review_id}/{final_label}")
        if not adjudication["交叉审计后裁决依据"].strip():
            raise SystemExit(f"裁决依据为空：{review_id}")
        if not adjudication["交叉审计后证据位置"].strip():
            raise SystemExit(f"证据位置为空：{review_id}")
        old_label = baseline["level"]
        changed += final_label != old_label
        adoption_rows.append(
            {
                "裁决序号": adjudication["裁决序号"],
                "review_row_id": review_id,
                "item_id": baseline["item_id"],
                "届次": baseline["competition_no"],
                "维度": baseline["dimension"],
                "第三版标签": old_label,
                "作者授权采用标签": final_label,
                "是否改变第三版": "是" if final_label != old_label else "否",
                "采用依据": adjudication["交叉审计后裁决依据"],
                "证据位置": adjudication["交叉审计后证据位置"],
                "复核置信度": adjudication["交叉审计后置信度"],
                "采用状态": "作者授权采用计算辅助全文复核结果",
            }
        )

    output_rows: list[dict[str, str]] = []
    for baseline in baseline_rows:
        updated = dict(baseline)
        adjudication = adjudication_by_id.get(baseline["review_row_id"])
        if adjudication:
            final_label = adjudication["交叉审计后裁决标签"]
            present, present_label, level = label_pair(final_label)
            updated["present"] = present
            updated["present_label"] = present_label
            updated["level"] = level
            updated["candidate_present_label"] = present_label
            updated["candidate_level"] = level
        output_rows.append(updated)

    if len(output_rows) != 884:
        raise SystemExit("作者授权采用分析表行数异常")
    item_dimensions = Counter((row["item_id"], row["dimension"]) for row in output_rows)
    if len(item_dimensions) != 884 or any(count != 1 for count in item_dimensions.values()):
        raise SystemExit("item_id×dimension联合主键不唯一")
    if len({row["item_id"] for row in output_rows}) != 221:
        raise SystemExit("作者授权采用分析表分析单元数不是221")
    if {row["dimension"] for row in output_rows} != DIMENSIONS:
        raise SystemExit("作者授权采用分析表维度集合异常")
    for row in output_rows:
        if row["present"] == "1" and row["level"] not in {"L1", "L2", "L3", "L4"}:
            raise SystemExit(f"出现性与等级冲突：{row['review_row_id']}")
        if row["present"] == "0" and row["level"] != "未出现":
            raise SystemExit(f"出现性与等级冲突：{row['review_row_id']}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(OUTPUT, baseline_fields, output_rows)
    adoption_fields = [
        "裁决序号",
        "review_row_id",
        "item_id",
        "届次",
        "维度",
        "第三版标签",
        "作者授权采用标签",
        "是否改变第三版",
        "采用依据",
        "证据位置",
        "复核置信度",
        "采用状态",
    ]
    write_csv(ADOPTION, adoption_fields, adoption_rows)

    provenance_rows = [
        {
            "文件角色": "只读基线",
            "文件路径": BASELINE.relative_to(ROOT).as_posix(),
            "SHA256": sha256(BASELINE),
            "记录数": "884",
            "说明": "保留第三版正式基线，不被本任务覆盖",
        },
        {
            "文件角色": "交叉审计输入",
            "文件路径": ADJUDICATION.relative_to(ROOT).as_posix(),
            "SHA256": sha256(ADJUDICATION),
            "记录数": "146",
            "说明": "三方分歧完整原文复核与第二轮交叉审计结果",
        },
        {
            "文件角色": "作者授权采用分析表",
            "文件路径": OUTPUT.relative_to(ROOT).as_posix(),
            "SHA256": sha256(OUTPUT),
            "记录数": "884",
            "说明": "用于重建论文描述统计；不冒充新增真人裁决",
        },
        {
            "文件角色": "逐条采用记录",
            "文件路径": ADOPTION.relative_to(ROOT).as_posix(),
            "SHA256": sha256(ADOPTION),
            "记录数": "146",
            "说明": f"相对第三版改变{changed}条标签",
        },
    ]
    write_csv(
        PROVENANCE,
        ["文件角色", "文件路径", "SHA256", "记录数", "说明"],
        provenance_rows,
    )

    counts = Counter(
        (row["dimension"], row["level"])
        for row in output_rows
    )
    summary = OUTPUT_DIR / "作者授权采用分析版生成说明.md"
    summary.write_text(
        "# 作者授权采用分析版生成说明\n\n"
        "本分析版以第三版884行只读表为基线，只替换三方分歧经完整原文复核与"
        "第二轮交叉审计后形成的146条标签。作者已授权采用该结果。该过程属于"
        "计算辅助的证据复核，不表述为新增真人评分者或专家裁决。\n\n"
        "884行分析表沿用第三版33字段结构以兼容既有统计程序；其中标签字段为"
        "正式采用值。对146条复核记录，最终采用依据、证据位置和置信度应以"
        "《三方分歧交叉审计后采用记录》为准，不应把基线中的旧复核理由解释为"
        "改变后标签的最终依据。\n\n"
        f"- 分析单元：221个；\n"
        f"- 编码记录：884行；\n"
        f"- 进入采用流程：146行；\n"
        f"- 相对第三版改变：{changed}行；\n"
        f"- 第三版基线SHA-256：`{sha256(BASELINE)}`；\n"
        f"- 作者授权采用分析表SHA-256：`{sha256(OUTPUT)}`。\n\n"
        "## 四维标签分布\n\n"
        "| 维度 | 未出现 | L1 | L2 | L3 | L4 |\n"
        "|---|---:|---:|---:|---:|---:|\n"
        + "\n".join(
            f"| {dimension} | {counts[(dimension, '未出现')]} | "
            f"{counts[(dimension, 'L1')]} | {counts[(dimension, 'L2')]} | "
            f"{counts[(dimension, 'L3')]} | {counts[(dimension, 'L4')]} |"
            for dimension in ("模型建构", "科学推理", "科学论证", "质疑创新")
        )
        + "\n",
        encoding="utf-8",
    )

    print(f"baseline_sha256={sha256(BASELINE)}")
    print(f"analysis_sha256={sha256(OUTPUT)}")
    print(f"adoption_sha256={sha256(ADOPTION)}")
    print(f"rows={len(output_rows)}")
    print(f"items={len({row['item_id'] for row in output_rows})}")
    print(f"adjudicated={len(adoption_rows)}")
    print(f"changed={changed}")


if __name__ == "__main__":
    main()
