#!/usr/bin/env python3
"""Register and screen a completed V3 author substantive-review return."""

from __future__ import annotations

import argparse
import hashlib
import re
import shutil
import stat
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

from build_v3_author_review_package import ROOT
from build_v3_cross_year_audit import read_rows, write_rows


DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
GENERIC_REASON_PATTERN = re.compile(
    r"^(同意|无问题|无需修改|保持当前候选|符合标准|证据充分|结论正确|"
    r"核对无误|通过无需修订|未发现问题|认可当前判断)[。；，,\s]*$"
)
FLAG_FIELDS = [
    "flag_id",
    "severity",
    "category",
    "record_count",
    "item_count",
    "example_review_row_ids",
    "detail",
    "required_action",
]
REGISTER_FIELDS = [
    "intake_id",
    "received_original_filename",
    "source_path",
    "archived_original_path",
    "source_sha256",
    "archive_sha256",
    "file_size_bytes",
    "intake_date",
    "received_by",
    "review_row_count",
    "reviewer_codes",
    "review_dates",
    "structural_validation_status",
    "quality_flag_count",
    "high_risk_flag_count",
    "pending_record_count",
    "intake_status",
    "release_status",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--intake-date", required=True)
    parser.add_argument("--received-by", required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args()


def resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalized(value: str) -> str:
    return re.sub(r"\s+", "", value.strip())


def add_group_flag(
    flags: list[dict[str, str]],
    *,
    severity: str,
    category: str,
    rows: list[dict[str, str]],
    detail: str,
    required_action: str,
) -> None:
    flags.append(
        {
            "flag_id": f"V3INT-FLAG-{len(flags) + 1:03d}",
            "severity": severity,
            "category": category,
            "record_count": str(len(rows)),
            "item_count": str(len({row["item_id"] for row in rows})),
            "example_review_row_ids": "；".join(
                row["review_row_id"] for row in rows[:12]
            ),
            "detail": detail,
            "required_action": required_action,
        }
    )


def build_quality_flags(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    flags: list[dict[str, str]] = []

    generic_rows = [
        row
        for row in rows
        if GENERIC_REASON_PATTERN.fullmatch(
            row["correction_reason"].strip()
        )
    ]
    if generic_rows:
        add_group_flag(
            flags,
            severity="高",
            category="通用理由",
            rows=generic_rows,
            detail="更正理由仅为同意、无问题、符合标准等通用结论，未体现本题证据。",
            required_action="逐行返回题干、解答和相邻等级边界，改写为题目针对性理由。",
        )

    reason_groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    evidence_groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        reason_groups[normalized(row["correction_reason"])].append(row)
        evidence_groups[normalized(row["post_review_evidence_location"])].append(row)

    for reason, grouped_rows in sorted(reason_groups.items()):
        item_count = len({row["item_id"] for row in grouped_rows})
        if reason and item_count >= 5:
            add_group_flag(
                flags,
                severity="高",
                category="跨题重复理由",
                rows=grouped_rows,
                detail=f"同一更正理由逐字复用于{item_count}个不同分析单元。",
                required_action="人工抽查全部命中行；不能证明逐题判断时退回补正。",
            )

    for evidence, grouped_rows in sorted(evidence_groups.items()):
        item_count = len({row["item_id"] for row in grouped_rows})
        if evidence and item_count >= 9:
            add_group_flag(
                flags,
                severity="中",
                category="跨题重复证据位置",
                rows=grouped_rows,
                detail=f"同一复核后证据位置逐字复用于{item_count}个不同分析单元。",
                required_action="核对路径或页码是否足以逐题定位；必要时补充具体题号和位置。",
            )

    same_item_reason_rows: list[dict[str, str]] = []
    rows_by_item: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        rows_by_item[row["item_id"]].append(row)
    for item_rows in rows_by_item.values():
        reasons = {normalized(row["correction_reason"]) for row in item_rows}
        if len(item_rows) == 4 and len(reasons) == 1:
            same_item_reason_rows.extend(item_rows)
    if same_item_reason_rows:
        add_group_flag(
            flags,
            severity="中",
            category="同题四维理由完全相同",
            rows=same_item_reason_rows,
            detail="部分分析单元的四个维度使用完全相同的更正理由。",
            required_action="人工确认理由是否分别回应四个维度；通用整题摘要不能替代逐维判断。",
        )

    pending_rows = [
        row
        for row in rows
        if row["candidate_review_decision"] == "待核实"
        or row["author_review_status"] in {"待补证", "待裁决"}
    ]
    if pending_rows:
        add_group_flag(
            flags,
            severity="高",
            category="未闭合记录",
            rows=pending_rows,
            detail="完成副本仍含待核实、待补证或待裁决记录。",
            required_action="逐项解决或登记为正式阻塞；不得进入唯一编码表。",
        )

    correction_rows = [
        row for row in rows if row["candidate_review_decision"] == "更正候选"
    ]
    if correction_rows:
        add_group_flag(
            flags,
            severity="信息",
            category="候选更正",
            rows=correction_rows,
            detail="作者复核提出候选标签更正。",
            required_action="G8-80人工QA逐项确认更正理由和双侧证据后再写入唯一表。",
        )

    reviewer_codes = {
        row["actual_author_reviewer_or_code"].strip() for row in rows
    }
    review_dates = {row["actual_review_date"].strip() for row in rows}
    if len(reviewer_codes) > 1 or len(review_dates) > 1:
        add_group_flag(
            flags,
            severity="信息",
            category="复核元数据不唯一",
            rows=rows,
            detail=(
                f"复核代号共{len(reviewer_codes)}个，复核日期共{len(review_dates)}个。"
            ),
            required_action="确认是否为真实分批或多人过程，并在接收报告中说明。",
        )

    return flags


def markdown_escape(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def build_report(
    register: dict[str, str],
    flags: list[dict[str, str]],
    validator_output: str,
) -> str:
    flag_lines = [
        "| 标记 | 严重度 | 类别 | 记录数 | 题目数 | 处置 |",
        "|---|---|---|---:|---:|---|",
    ]
    for flag in flags:
        flag_lines.append(
            "| {flag_id} | {severity} | {category} | {record_count} | "
            "{item_count} | {action} |".format(
                flag_id=flag["flag_id"],
                severity=flag["severity"],
                category=flag["category"],
                record_count=flag["record_count"],
                item_count=flag["item_count"],
                action=markdown_escape(flag["required_action"]),
            )
        )
    if not flags:
        flag_lines.append("| 无 | 无 | 未发现程序性风险 | 0 | 0 | 仍需G8-80人工QA |")

    return f"""# V3作者实质复核完成副本接收报告

## 接收登记

- 接收编号：`{register["intake_id"]}`
- 原始文件名：`{register["received_original_filename"]}`
- 原件SHA-256：`{register["source_sha256"]}`
- 归档副本SHA-256：`{register["archive_sha256"]}`
- 文件字节数：{register["file_size_bytes"]}
- 复核行数：{register["review_row_count"]}
- 复核代号：{register["reviewer_codes"]}
- 复核日期：{register["review_dates"]}
- 接收状态：{register["intake_status"]}
- 放行状态：{register["release_status"]}

## 程序检查

全量成品校验通过。校验输出：

```text
{validator_output.strip()}
```

## 质量标记

{chr(10).join(flag_lines)}

## 边界

本报告只证明接收副本与归档副本哈希一致、884行结构通过，并列出程序可发现的质量风险。它不证明复核身份真实性、逐题阅读过程或编码判断正确，也不自动放行V3唯一编码表、论文统计或正文结果。所有记录仍须执行G8-80人工QA。
"""


def main() -> None:
    args = parse_args()
    if not DATE_PATTERN.fullmatch(args.intake_date):
        raise SystemExit("--intake-date必须为YYYY-MM-DD")
    if not args.received_by.strip():
        raise SystemExit("--received-by不得为空")

    source = resolve(args.input)
    if not source.is_file():
        raise SystemExit(f"输入文件不存在: {source}")
    validator = ROOT / "07_analysis/scripts/validate_v3_author_review.py"
    validation = subprocess.run(
        [sys.executable, str(validator), str(source), "--mode", "filled"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    validator_output = validation.stdout + validation.stderr
    if validation.returncode:
        print(validator_output, end="")
        raise SystemExit("结构或字段校验失败：未创建接收归档")

    _, rows = read_rows(source)
    source_hash = sha256(source)
    intake_id = f"V3INT-{args.intake_date.replace('-', '')}-{source_hash[:12]}"
    output_dir = resolve(args.output_dir)
    archive_path = output_dir / f"{intake_id}_{source.name}"
    if source.resolve() == archive_path.resolve():
        raise SystemExit("输入文件不能同时作为归档输出")

    output_dir.mkdir(parents=True, exist_ok=True)
    if archive_path.exists() and sha256(archive_path) != source_hash:
        raise SystemExit(f"同名归档已存在但哈希不一致: {archive_path}")
    if not archive_path.exists():
        shutil.copyfile(source, archive_path)
    archive_path.chmod(
        stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH
    )
    archive_hash = sha256(archive_path)
    if archive_hash != source_hash:
        archive_path.unlink(missing_ok=True)
        raise SystemExit("归档副本哈希与来件不一致，已删除归档副本")

    flags = build_quality_flags(rows)
    high_risk_count = sum(flag["severity"] == "高" for flag in flags)
    pending_count = sum(
        row["candidate_review_decision"] == "待核实"
        or row["author_review_status"] in {"待补证", "待裁决"}
        for row in rows
    )
    reviewer_codes = sorted(
        {row["actual_author_reviewer_or_code"].strip() for row in rows}
    )
    review_dates = sorted({row["actual_review_date"].strip() for row in rows})
    release_status = (
        "不放行：存在高风险质量标记"
        if high_risk_count
        else "不放行：待G8-80人工QA"
    )
    register = {
        "intake_id": intake_id,
        "received_original_filename": source.name,
        "source_path": str(source),
        "archived_original_path": str(archive_path),
        "source_sha256": source_hash,
        "archive_sha256": archive_hash,
        "file_size_bytes": str(source.stat().st_size),
        "intake_date": args.intake_date,
        "received_by": args.received_by.strip(),
        "review_row_count": str(len(rows)),
        "reviewer_codes": "；".join(reviewer_codes),
        "review_dates": "；".join(review_dates),
        "structural_validation_status": "通过：全量filled模式0错误",
        "quality_flag_count": str(len(flags)),
        "high_risk_flag_count": str(high_risk_count),
        "pending_record_count": str(pending_count),
        "intake_status": "已登记：待G8-80人工QA",
        "release_status": release_status,
    }

    register_path = output_dir / f"{intake_id}_接收登记.csv"
    flags_path = output_dir / f"{intake_id}_质量标记.csv"
    report_path = output_dir / f"{intake_id}_接收报告.md"
    write_rows(register_path, REGISTER_FIELDS, [register])
    write_rows(flags_path, FLAG_FIELDS, flags)
    with report_path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(build_report(register, flags, validator_output))

    print(f"intake_id={intake_id}")
    print(f"source_sha256={source_hash}")
    print(f"archive_sha256={archive_hash}")
    print(f"quality_flags={len(flags)}")
    print(f"high_risk_flags={high_risk_count}")
    print(f"pending_records={pending_count}")
    print(f"release_status={release_status}")
    print(f"output_dir={output_dir}")


if __name__ == "__main__":
    main()
