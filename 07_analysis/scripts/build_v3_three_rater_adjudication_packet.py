#!/usr/bin/env python3
"""Build a self-contained adjudication packet for V3/F/G disagreements."""

from __future__ import annotations

import argparse
import csv
import hashlib
import re
import shutil
import unicodedata
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_F = ROOT / (
    "07_analysis/data/v3_independent_validation/incoming/RATER-F/"
    "第35至42届第三版匿名盲评编码表_RATER-F_300行.csv"
)
DEFAULT_G = ROOT / (
    "07_analysis/data/v3_independent_validation/incoming/RATER-G/"
    "第35至42届第三版匿名盲评编码表_RATER-G_300行.csv"
)
DEFAULT_KEY = ROOT / (
    "07_analysis/data/v3_independent_validation/author_only/"
    "独立盲评抽样与V3对照密钥_不得交评分者.csv"
)
DEFAULT_FINAL = ROOT / "07_analysis/data/第35至42届科学思维第三版唯一编码表.csv"
DEFAULT_OUTPUT = ROOT / (
    "07_analysis/data/v3_independent_validation/adjudication/"
    "第三版RATER-F-G三方分歧裁决材料包_146行"
)

DIMENSION_ORDER = {"模型建构": 1, "科学推理": 2, "科学论证": 3, "质疑创新": 4}
LEVELS = {"L1", "L2", "L3", "L4"}
DECISION_FIELDS = [
    "是否已核对原文",
    "裁决后存在性",
    "裁决后等级",
    "裁决依据",
    "复核后证据位置",
    "裁决置信度",
    "待补材料",
    "裁决状态",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_label(present: str, level: str) -> bool:
    return (present == "否" and level == "未出现") or (
        present == "是" and level in LEVELS
    )


def normalize(text: str) -> str:
    value = unicodedata.normalize("NFKC", text or "")
    value = value.replace("−", "-").replace("–", "-").replace("—", "-")
    return re.sub(r"\s+", "", value)


def choose_locatable_evidence(
    original: str,
    rater_g: str,
    rater_f: str,
    source: str,
    minimum_length: int,
    evidence_side: str,
) -> tuple[str, str]:
    normalized_source = normalize(source)
    normalized_original = normalize(original)
    if (
        len(normalized_original) >= minimum_length
        and normalized_original in normalized_source
    ):
        return original.strip(), f"{evidence_side}第三版原引文可在清晰Markdown定位"
    fallbacks = []
    for label, quote in [("RATER-F", rater_f), ("RATER-G", rater_g)]:
        normalized_quote = normalize(quote)
        if len(normalized_quote) >= minimum_length and normalized_quote in normalized_source:
            fallbacks.append((len(normalized_quote), label, quote.strip()))
    if fallbacks:
        _, label, quote = max(fallbacks)
        return (
            quote,
            f"{evidence_side}第三版原引文来自旧文本层且不能逐字匹配清晰Markdown；"
            f"裁决包采用两份可定位回填中信息更完整的{label}连续原文引文",
        )
    raise ValueError(f"{evidence_side}三组引文均不能在清晰Markdown定位")


def validate_inputs(
    f_rows: list[dict[str, str]],
    g_rows: list[dict[str, str]],
    key_rows: list[dict[str, str]],
    final_rows: list[dict[str, str]],
) -> None:
    if len(f_rows) != 300 or len(g_rows) != 300 or len(key_rows) != 300:
        raise ValueError("F、G和对照密钥必须各为300行")
    f_by_id = {row["blind_row_id"].strip(): row for row in f_rows}
    g_by_id = {row["blind_row_id"].strip(): row for row in g_rows}
    key_by_id = {row["blind_row_id"].strip(): row for row in key_rows}
    if not (len(f_by_id) == len(g_by_id) == len(key_by_id) == 300):
        raise ValueError("F、G或对照密钥存在重复blind_row_id")
    if not (set(f_by_id) == set(g_by_id) == set(key_by_id)):
        raise ValueError("F、G与对照密钥主键集合不一致")
    final_by_id = {row["review_row_id"].strip(): row for row in final_rows}
    if len(final_by_id) != len(final_rows):
        raise ValueError("第三版唯一编码表存在重复review_row_id")
    for blind_id, key_row in key_by_id.items():
        f_row = f_by_id[blind_id]
        g_row = g_by_id[blind_id]
        if any(
            f_row[field].strip() != g_row[field].strip()
            for field in list(f_row)[:10]
        ):
            raise ValueError(f"F/G固定字段不一致：{blind_id}")
        if not validate_label(f_row["review_present"].strip(), f_row["review_level"].strip()):
            raise ValueError(f"F标签非法：{blind_id}")
        if not validate_label(g_row["review_present"].strip(), g_row["review_level"].strip()):
            raise ValueError(f"G标签非法：{blind_id}")
        final = final_by_id.get(key_row["source_review_row_id"].strip())
        if final is None:
            raise ValueError(f"第三版源记录缺失：{blind_id}")
        if any(
            [
                final["item_id"].strip() != key_row["item_id"].strip(),
                final["dimension"].strip() != key_row["dimension"].strip(),
                final["present_label"].strip() != key_row["v3_present_label"].strip(),
                final["level"].strip() != key_row["v3_level"].strip(),
            ]
        ):
            raise ValueError(f"第三版源标签与密钥不一致：{blind_id}")


def rule_text(
    dimension: str,
    disagreement_type: str,
    labels: list[str],
    matrix: dict[tuple[str, str], dict[str, str]],
) -> str:
    if disagreement_type == "存在性分歧":
        row = matrix[(dimension, "存在")]
        return (
            f"必要证据：{row['必要证据']}；最低充分判据：{row['最低充分判据']}；"
            f"明确排除：{row['明确排除']}。先判存在性，判否时不得再定级。"
        )
    parts = []
    for level in sorted(set(labels), key=lambda value: int(value[1:])):
        row = matrix[(dimension, level)]
        parts.append(
            f"{level}最低充分判据：{row['最低充分判据']}；明确排除：{row['明确排除']}"
        )
    return "；".join(parts) + "。比较结构而非公式数量、篇幅或背景陌生度。"


def build_rows(
    f_rows: list[dict[str, str]],
    g_rows: list[dict[str, str]],
    key_rows: list[dict[str, str]],
    final_rows: list[dict[str, str]],
    matrix_rows: list[dict[str, str]],
    source_texts: Path,
) -> list[dict[str, str]]:
    g_by_id = {row["blind_row_id"].strip(): row for row in g_rows}
    key_by_id = {row["blind_row_id"].strip(): row for row in key_rows}
    final_by_id = {row["review_row_id"].strip(): row for row in final_rows}
    matrix = {
        (row["维度"].strip(), row["判定层级"].strip()): row for row in matrix_rows
    }
    disagreements: list[dict[str, str]] = []
    for f_row in f_rows:
        blind_id = f_row["blind_row_id"].strip()
        g_row = g_by_id[blind_id]
        key = key_by_id[blind_id]
        final = final_by_id[key["source_review_row_id"].strip()]
        source_file = f_row["source_text_file"].strip()
        source_path = source_texts / source_file
        source = source_path.read_text(encoding="utf-8")
        v3_present = key["v3_present_label"].strip()
        v3_level = key["v3_level"].strip()
        f_present = f_row["review_present"].strip()
        f_level = f_row["review_level"].strip()
        g_present = g_row["review_present"].strip()
        g_level = g_row["review_level"].strip()
        if len({v3_level, f_level, g_level}) == 1:
            continue
        presence_agrees = len({v3_present, f_present, g_present}) == 1
        disagreement_type = "等级分歧" if presence_agrees else "存在性分歧"
        priority = "P1-存在性" if disagreement_type == "存在性分歧" else "P2-等级"
        labels = [label for label in [v3_level, f_level, g_level] if label in LEVELS]
        clean_question, question_note = choose_locatable_evidence(
            final["question_quote"],
            g_row["question_evidence_quote"],
            f_row["question_evidence_quote"],
            source,
            6,
            "题干",
        )
        clean_solution, solution_note = choose_locatable_evidence(
            final["solution_quote"],
            g_row["solution_evidence_quote"],
            f_row["solution_evidence_quote"],
            source,
            8,
            "解答",
        )
        row = {
            "裁决序号": "",
            "优先组": priority,
            "blind_row_id": blind_id,
            "blind_unit_no": f_row["blind_unit_no"].strip(),
            "item_id": f_row["item_id"].strip(),
            "届次": f_row["competition_no"].strip(),
            "年份": f_row["year"].strip(),
            "题号": f_row["question_no"].strip(),
            "小问": f_row["subquestion_no"].strip(),
            "维度": f_row["dimension"].strip(),
            "源文件": source_file,
            "抽样层": key["selection_stratum"].strip(),
            "分歧类型": disagreement_type,
            "三方标签组合": f"第三版={v3_level}；RATER-F={f_level}；RATER-G={g_level}",
            "本行裁决判据": rule_text(
                f_row["dimension"].strip(), disagreement_type, labels, matrix
            ),
            "第三版存在性": v3_present,
            "第三版等级": v3_level,
            "第三版必要输出": final["required_output"].strip(),
            "清晰题干证据": clean_question,
            "清晰解答证据": clean_solution,
            "第三版认知活动": final["necessary_cognitive_activity"].strip(),
            "第三版裁决理由": final["author_review_reason"].strip(),
            "第三版证据位置": final["post_review_evidence_location"].strip(),
            "第三版源记录": final["review_row_id"].strip(),
            "第三版原引文对照说明": f"{question_note}；{solution_note}",
            "RATER-F存在性": f_present,
            "RATER-F等级": f_level,
            "RATER-F题干证据": f_row["question_evidence_quote"].strip(),
            "RATER-F解答证据": f_row["solution_evidence_quote"].strip(),
            "RATER-F证据位置": f_row["evidence_location"].strip(),
            "RATER-F相邻等级排除": f_row["adjacent_level_exclusion"].strip(),
            "RATER-F置信度": f_row["confidence"].strip(),
            "RATER-G存在性": g_present,
            "RATER-G等级": g_level,
            "RATER-G题干证据": g_row["question_evidence_quote"].strip(),
            "RATER-G解答证据": g_row["solution_evidence_quote"].strip(),
            "RATER-G证据位置": g_row["evidence_location"].strip(),
            "RATER-G相邻等级排除": g_row["adjacent_level_exclusion"].strip(),
            "RATER-G置信度": g_row["confidence"].strip(),
            **{field: "" for field in DECISION_FIELDS},
        }
        disagreements.append(row)
    disagreements.sort(
        key=lambda row: (
            1 if row["分歧类型"] == "存在性分歧" else 2,
            int(row["blind_unit_no"].split("-")[1]),
            DIMENSION_ORDER[row["维度"]],
        )
    )
    for index, row in enumerate(disagreements, start=1):
        row["裁决序号"] = f"FGADJ-{index:03d}"
    counts = Counter(row["分歧类型"] for row in disagreements)
    if len(disagreements) != 146 or counts != {"存在性分歧": 59, "等级分歧": 87}:
        raise ValueError(f"分歧数量异常：总数{len(disagreements)}，分类{dict(counts)}")
    return disagreements


def write_instructions(output: Path) -> None:
    (output / "00_开始前必读.md").write_text(
        """# 第三版、RATER-F与RATER-G三方分歧裁决材料包

本包只处理三方标签不完全一致的146行，其中P1存在性分歧59行、P2纯等级分歧87行。裁决顺序必须先P1后P2。三方一致的154行不在本包重复处理。

裁决不是多数票。必须回到清晰题目与参考解答，依据《科学思维编码手册（第三版）》和决策矩阵重新判断。第三版、RATER-F和RATER-G的标签及理由都是待比较证据，不是预设正确答案。

第三版唯一编码表的原引文来自较早文本层，与本包清晰Markdown的排版版本不能逐字匹配。工作表不复制旧文本层乱码，而是在RATER-F/G两份已定位引文中选择信息更完整的一条作为“清晰题干/解答证据”，同时保留第三版标签、裁决理由、证据位置和逐行整理说明。最终判断仍必须打开源Markdown核对。

只填写工作表最后8列，不改动前38列，不增删行、不排序。证据不足时填写“待核实”，不得强行选定标签。完成后填写一次匿名裁决声明即可，不要求每行重复填写日期或声明。
""",
        encoding="utf-8",
    )
    (output / "01_裁决者详细操作指令.md").write_text(
        """# 三方分歧逐条裁决操作指令

## 一、使用文件

1. 先阅读`编码规则/科学思维编码手册_第三版.md`和决策矩阵；
2. 主表为`三方分歧裁决工作表_146行_空白.csv`；
3. 可先处理`存在性分歧59行`，完成后再处理`等级分歧87行`；
4. 每行按`源文件`打开`清晰排版题目与解答/`中的同名Markdown，题图位于其`图件/`子目录。

## 二、每行裁决步骤

1. 核对item_id、小问和维度，完整阅读该小问题干与对应参考解答；
2. 比较第三版、RATER-F、RATER-G三组证据和理由，检查是否错引其他小问；
3. 先判存在性：该认知活动是否是完成本小问不可删除的必要活动；若删除后仍能完成任务，判“否/未出现”；
4. 仅在判“是”后定L1至L4；使用`本行裁决判据`和完整手册判断关系或模型要素的数量、组织方式及升级条件；
5. 填写最后8列。`裁决依据`必须说明为何采用当前标签并排除至少一个相邻标签；`复核后证据位置`必须写明Markdown文件、小问及公式、段落或图件锚点；
6. 不得因三方中两方相同而直接采纳，不得因公式多、篇幅长、背景前沿或计算困难而升级；
7. 无法从现有材料确定时，填`裁决后存在性=待核实`、`裁决后等级=待核实`、`裁决状态=待核实`，并在`待补材料`写明缺什么。

## 三、允许值

- `是否已核对原文`：是；
- `裁决后存在性`：是、否、待核实；
- `裁决后等级`：未出现、L1、L2、L3、L4、待核实；
- `裁决置信度`：高、中、低、待核实；
- `裁决状态`：已裁决、待核实；
- `待补材料`：没有则填“无”，有则具体说明。

## 四、完成标准

- 146行全部有处理状态；
- 已裁决行满足“否/未出现”或“是/L1-L4”的合法组合；
- 每条裁决依据和证据位置均为本题本问的具体内容；
- 不改动固定字段；
- 匿名声明只填写一次，不写真实姓名、单位、电话或邮箱。
""",
        encoding="utf-8",
    )
    (output / "02_匿名裁决声明_回填.md").write_text(
        """# 匿名裁决声明

我确认：本人逐条核对了工作表所列题干、参考解答、三方证据和第三版编码规则；裁决结论为本人判断，未按多数票自动决定，未把他人或自动生成结果冒充为本人裁决。

- 匿名裁决代号：
- 专业背景：
- 完成行数：
- 回填文件名：
- 匿名确认（填写“确认”）：
""",
        encoding="utf-8",
    )


def write_summary(output: Path, rows: list[dict[str, str]]) -> None:
    dimensions = Counter(row["维度"] for row in rows)
    sources = sorted({row["源文件"] for row in rows})
    text = f"""# 材料包统计摘要

- 分歧总数：{len(rows)}行；
- 存在性分歧：{sum(row['分歧类型'] == '存在性分歧' for row in rows)}行；
- 纯等级分歧：{sum(row['分歧类型'] == '等级分歧' for row in rows)}行；
- 涉及分析单元：{len({row['blind_unit_no'] for row in rows})}个；
- 涉及题目Markdown：{len(sources)}份；
- 模型建构：{dimensions['模型建构']}行；
- 科学推理：{dimensions['科学推理']}行；
- 科学论证：{dimensions['科学论证']}行；
- 质疑创新：{dimensions['质疑创新']}行。

工作表最后8列均为空，未预填裁决结论。包内同时保留43份盲评清晰文本和全部配套图件，方便查看同题相邻小问。

第三版原题干与解答引文来自旧文本层，146行均不能与当前清晰Markdown逐字匹配；裁决包因此不复制旧乱码，而使用RATER-F/G中信息更完整且可在清晰Markdown连续定位的引文作为中性文本入口。146条清晰题干引文和146条清晰解答引文均已通过定位检查，第三版标签、理由、证据位置及原引文对照说明仍完整保留。
"""
    (output / "03_材料包统计摘要.md").write_text(text, encoding="utf-8")


def write_manifest(output: Path) -> None:
    rows: list[dict[str, str]] = []
    for path in sorted(file for file in output.rglob("*") if file.is_file()):
        if path.name == "材料包清单与校验值.csv":
            continue
        rows.append(
            {
                "相对路径": str(path.relative_to(output)),
                "字节数": str(path.stat().st_size),
                "SHA-256": sha256(path),
            }
        )
    write_csv(
        output / "材料包清单与校验值.csv",
        ["相对路径", "字节数", "SHA-256"],
        rows,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rater-f", type=Path, default=DEFAULT_F)
    parser.add_argument("--rater-g", type=Path, default=DEFAULT_G)
    parser.add_argument("--key-file", type=Path, default=DEFAULT_KEY)
    parser.add_argument("--final-file", type=Path, default=DEFAULT_FINAL)
    parser.add_argument("--source-package", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    source_texts = args.source_package / "清晰排版题目与解答"
    rules = args.source_package / "编码规则"
    matrix_file = rules / "科学思维编码决策矩阵_第三版.csv"
    if not source_texts.is_dir() or not matrix_file.is_file():
        raise FileNotFoundError("source-package缺少清晰题目解答或第三版决策矩阵")
    if args.output_dir.exists():
        if not args.overwrite:
            raise FileExistsError(f"输出目录已存在：{args.output_dir}")
        shutil.rmtree(args.output_dir)
    args.output_dir.mkdir(parents=True)

    f_rows = read_csv(args.rater_f)
    g_rows = read_csv(args.rater_g)
    key_rows = read_csv(args.key_file)
    final_rows = read_csv(args.final_file)
    matrix_rows = read_csv(matrix_file)
    validate_inputs(f_rows, g_rows, key_rows, final_rows)
    rows = build_rows(
        f_rows, g_rows, key_rows, final_rows, matrix_rows, source_texts
    )
    fields = list(rows[0])
    write_csv(args.output_dir / "三方分歧裁决工作表_146行_空白.csv", fields, rows)
    write_csv(
        args.output_dir / "三方分歧裁决工作表_存在性59行_空白.csv",
        fields,
        [row for row in rows if row["分歧类型"] == "存在性分歧"],
    )
    write_csv(
        args.output_dir / "三方分歧裁决工作表_等级87行_空白.csv",
        fields,
        [row for row in rows if row["分歧类型"] == "等级分歧"],
    )
    index_fields = [
        "裁决序号",
        "优先组",
        "blind_row_id",
        "blind_unit_no",
        "item_id",
        "届次",
        "年份",
        "题号",
        "小问",
        "维度",
        "源文件",
        "分歧类型",
        "三方标签组合",
    ]
    write_csv(args.output_dir / "三方分歧材料索引_146行.csv", index_fields, rows)
    write_instructions(args.output_dir)
    write_summary(args.output_dir, rows)
    shutil.copytree(source_texts, args.output_dir / "清晰排版题目与解答")
    shutil.copytree(rules, args.output_dir / "编码规则")
    write_manifest(args.output_dir)
    print(f"输出目录: {args.output_dir}")
    print("分歧: 146行；存在性: 59行；等级: 87行")
    print(f"文件总数: {sum(1 for path in args.output_dir.rglob('*') if path.is_file())}")


if __name__ == "__main__":
    main()
