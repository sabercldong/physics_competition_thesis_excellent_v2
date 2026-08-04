#!/usr/bin/env python3
"""Build the researcher confirmation package for 146 candidate adjudications."""

from __future__ import annotations

import csv
import hashlib
import shutil
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ADJUDICATION_ROOT = (
    ROOT / "07_analysis/data/v3_independent_validation/adjudication"
)
CANDIDATE_DIR = ADJUDICATION_ROOT / "模型辅助候选裁决_146行_20260803"
CANDIDATE = CANDIDATE_DIR / "三方分歧模型辅助候选裁决表_146行_待研究者确认.csv"
SOURCE_PACKET = ADJUDICATION_ROOT / "第三版RATER-F-G三方分歧裁决材料包_146行"
OUT = ADJUDICATION_ROOT / "研究者确认材料包_146行_20260803"


RESEARCHER_FIELDS = [
    "是否完整阅读原题与解答",
    "研究者决定",
    "最终存在性",
    "最终等级",
    "研究者裁决依据",
    "研究者证据定位",
    "研究者置信度",
    "待补材料",
    "确认状态",
]


OUTPUT_FIELDS = [
    "工作序号",
    "确认优先级",
    "裁决序号",
    "第三版源记录",
    "blind_row_id",
    "blind_unit_no",
    "item_id",
    "届次",
    "年份",
    "题号",
    "小问",
    "维度",
    "分歧类型",
    "完整题目与解答文件",
    "本行裁决判据",
    "第三版标签",
    "RATER-F标签",
    "RATER-G标签",
    "候选裁决标签",
    "候选裁决置信度",
    "清晰题干证据",
    "清晰解答证据",
    "第三版裁决理由",
    "RATER-F相邻等级排除",
    "RATER-G相邻等级排除",
    "候选裁决依据",
    "候选证据位置",
    *RESEARCHER_FIELDS,
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


def source_label(row: dict[str, str], prefix: str) -> str:
    return "未出现" if row[f"{prefix}存在性"] == "否" else row[f"{prefix}等级"]


def candidate_label(row: dict[str, str]) -> str:
    return "未出现" if row["裁决后存在性"] == "否" else row["裁决后等级"]


def priority(row: dict[str, str]) -> tuple[int, str]:
    low = row["裁决置信度"] == "低"
    changed = source_label(row, "第三版") != candidate_label(row)
    if low and changed:
        return 1, "第一阶段：低置信度且拟变更"
    if low:
        return 2, "第一阶段：低置信度但拟保持"
    if changed:
        return 3, "第二阶段：中置信度拟变更"
    return 4, "第三阶段：中置信度且拟保持"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_text(path: Path, text: str) -> None:
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def main() -> None:
    source_rows = read_csv(CANDIDATE)
    if len(source_rows) != 146:
        raise SystemExit(f"候选裁决应为146行，实测{len(source_rows)}行")
    if len({row["裁决序号"] for row in source_rows}) != 146:
        raise SystemExit("候选裁决序号不唯一")

    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    shutil.copytree(SOURCE_PACKET / "编码规则", OUT / "编码规则")
    shutil.copytree(
        SOURCE_PACKET / "清晰排版题目与解答",
        OUT / "完整题目与解答",
    )

    rows: list[dict[str, str]] = []
    ordered = sorted(source_rows, key=lambda row: (priority(row)[0], row["裁决序号"]))
    for number, row in enumerate(ordered, start=1):
        _, priority_text = priority(row)
        output = {
            "工作序号": f"RC-{number:03d}",
            "确认优先级": priority_text,
            "裁决序号": row["裁决序号"],
            "第三版源记录": row["第三版源记录"],
            "blind_row_id": row["blind_row_id"],
            "blind_unit_no": row["blind_unit_no"],
            "item_id": row["item_id"],
            "届次": row["届次"],
            "年份": row["年份"],
            "题号": row["题号"],
            "小问": row["小问"],
            "维度": row["维度"],
            "分歧类型": row["分歧类型"],
            "完整题目与解答文件": f"完整题目与解答/{row['源文件']}",
            "本行裁决判据": row["本行裁决判据"],
            "第三版标签": source_label(row, "第三版"),
            "RATER-F标签": source_label(row, "RATER-F"),
            "RATER-G标签": source_label(row, "RATER-G"),
            "候选裁决标签": candidate_label(row),
            "候选裁决置信度": row["裁决置信度"],
            "清晰题干证据": row["清晰题干证据"],
            "清晰解答证据": row["清晰解答证据"],
            "第三版裁决理由": row["第三版裁决理由"],
            "RATER-F相邻等级排除": row["RATER-F相邻等级排除"],
            "RATER-G相邻等级排除": row["RATER-G相邻等级排除"],
            "候选裁决依据": row["裁决依据"],
            "候选证据位置": row["复核后证据位置"],
        }
        output.update({field: "" for field in RESEARCHER_FIELDS})
        rows.append(output)

    table = OUT / "研究者逐行确认表_146行_待回填.csv"
    write_csv(table, OUTPUT_FIELDS, rows)
    index_fields = [
        "工作序号",
        "确认优先级",
        "裁决序号",
        "item_id",
        "维度",
        "分歧类型",
        "第三版标签",
        "候选裁决标签",
        "候选裁决置信度",
        "完整题目与解答文件",
    ]
    write_csv(OUT / "研究者确认工作顺序索引_146行.csv", index_fields, rows)

    counts = Counter(row["确认优先级"] for row in rows)
    write_text(
        OUT / "00_开始前必读.md",
        f"""
# 研究者确认材料包

本包用于确认第三版、RATER-F和RATER-G三方存在分歧的146条记录。候选结论不是正式裁决，研究者必须打开本包内的完整题目与参考解答后逐行决定。

只编辑：`研究者逐行确认表_146行_待回填.csv`。

工作顺序：

1. 第一阶段50行：低置信度记录，其中拟变更37行、拟保持13行；
2. 第二阶段57行：中置信度但相对第三版拟变更；
3. 第三阶段39行：中置信度且相对第三版拟保持。

分组实测：

- 低置信度且拟变更：{counts['第一阶段：低置信度且拟变更']}行；
- 低置信度但拟保持：{counts['第一阶段：低置信度但拟保持']}行；
- 中置信度拟变更：{counts['第二阶段：中置信度拟变更']}行；
- 中置信度且拟保持：{counts['第三阶段：中置信度且拟保持']}行。

完整关闭本轮裁决需要146行全部确认。若先完成前107行，可以先提交阶段性验收，但不能据此更新正式884行主表和论文统计。
""",
    )
    write_text(
        OUT / "01_逐行确认操作指令.md",
        """
# 逐行确认操作指令

## 一、每行必须怎样做

1. 根据`完整题目与解答文件`打开对应Markdown，完整阅读本小问、前后问和参考解答；需要图件时打开同目录`图件/`中的图片。
2. 对照`本行裁决判据`与`编码规则/科学思维编码手册_第三版.md`，先判断维度是否出现，再取最低充分等级。
3. 候选结论只用于定位争议，不得因多数意见或候选置信度直接照抄。
4. 在表格最后9列填写研究者结论；不要修改前27列。

## 二、最后9列的填写规则

- `是否完整阅读原题与解答`：只填`是`。尚未完整阅读时保留空白。
- `研究者决定`：只填`确认候选`、`保留第三版`、`另行裁决`或`待核实`。
- `最终存在性`：填`是`、`否`或`待核实`。
- `最终等级`：出现时填`L1`至`L4`；不出现填`未出现`；待核实时填`待核实`。
- `研究者裁决依据`：结合本小问写明必要认知活动，并排除相邻等级或存在门槛；不得只写“同意”“按候选”或“多数一致”。
- `研究者证据定位`：至少写明Markdown文件名、小问号和题干/解答位置，例如`CPHO35-Q05.md，第(3)问题干；参考解答(3)弱场展开段`。
- `研究者置信度`：已确认行填`高`、`中`或`低`；待核实行填`待核实`。
- `待补材料`：没有缺项填`无`；待核实时写清缺什么材料或哪一处无法判定。
- `确认状态`：填`已确认`或`待核实`。

## 三、决定与标签必须一致

- `确认候选`：最终标签必须等于`候选裁决标签`。
- `保留第三版`：最终标签必须等于`第三版标签`。
- `另行裁决`：最终标签可以不同，但必须由题干、解答和第三版规则直接支持。
- 判`否`时必须写`否/未出现`；判`是`时必须写`是/L1-L4`。

## 四、提交前检查

1. 146行最后9列全部填写；
2. 前27列未改；
3. 每行证据定位都含对应Markdown文件名；
4. 只在`02_研究者确认声明_完成后填写.md`统一填写一次代号和日期，不在每行重复。
""",
    )
    write_text(
        OUT / "02_研究者确认声明_完成后填写.md",
        """
# 研究者确认声明

研究者或确认代号：

确认完成日期：

确认范围：第三版、RATER-F与RATER-G三方分歧共146条。

本人已逐条打开本材料包中的完整题目与参考解答，依据科学思维编码手册第三版独立作出确认、保留、另行裁决或待核实决定。本人理解候选结论只用于定位争议，最终回填内容为本人研究判断。
""",
    )
    write_text(
        OUT / "03_完成后如何返回.md",
        """
# 完成后如何返回

1. 将完成后的主表另存为`研究者逐行确认表_146行_已完成.csv`，保留空白模板不动。
2. 在`02_研究者确认声明_完成后填写.md`中统一填写一次研究者代号和完成日期。
3. 两个完成文件保留在本材料包根目录，告知项目其绝对路径即可。
4. 项目接收后会自动检查行数、固定字段、标签逻辑、理由长度和证据定位；若有问题，只返工问题清单中的具体行。

阶段性返回也可以，但只有146行全部完成且验收通过后，才能生成新的裁决后主表并重算论文统计。
""",
    )

    # Preserve the candidate source used to construct the locked confirmation table.
    shutil.copy2(CANDIDATE, OUT / "候选裁决完整证据表_只读.csv")

    manifest_rows: list[dict[str, str]] = []
    for path in sorted(p for p in OUT.rglob("*") if p.is_file()):
        if path.name == "材料清单与校验值.csv":
            continue
        manifest_rows.append(
            {
                "相对路径": path.relative_to(OUT).as_posix(),
                "文件大小_字节": str(path.stat().st_size),
                "SHA-256": sha256(path),
            }
        )
    write_csv(
        OUT / "材料清单与校验值.csv",
        ["相对路径", "文件大小_字节", "SHA-256"],
        manifest_rows,
    )

    print(f"OUTPUT={OUT}")
    print(f"ROWS={len(rows)}")
    print(f"FILES={len(manifest_rows) + 1}")
    print(f"LOW_CONFIDENCE={sum(row['候选裁决置信度'] == '低' for row in rows)}")
    print(
        "CHANGED_FROM_V3="
        f"{sum(row['第三版标签'] != row['候选裁决标签'] for row in rows)}"
    )
    print(f"RESEARCHER_FIELDS_BLANK={sum(not row[field] for row in rows for field in RESEARCHER_FIELDS)}")


if __name__ == "__main__":
    main()
