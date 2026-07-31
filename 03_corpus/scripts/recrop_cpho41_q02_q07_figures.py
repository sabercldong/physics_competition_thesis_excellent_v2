#!/usr/bin/env python3
"""Re-crop source-backed figure candidates for CPHO41 Q02 and Q07."""

from __future__ import annotations

import csv
import hashlib
from dataclasses import dataclass
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
ASSET_DIR = ROOT / "03_corpus" / "item_assets"
RENDER_DIR = ROOT / "03_corpus" / "manual_review_renders" / "G1-07-A1"
TRANSCRIPT_DIR = ROOT / "03_corpus" / "manual_review_transcripts"


@dataclass(frozen=True)
class CropSpec:
    asset_id: str
    material_id: str
    source_page: Path
    box: tuple[int, int, int, int]
    output_name: str
    description: str
    visual_check: str
    boundary_note: str


SPECS = [
    CropSpec(
        asset_id="CPHO41-Q02-FIG2A-RECROP-V1",
        material_id="CPHO41-Q02",
        source_page=RENDER_DIR / "CPHO41-Q02-paper-page-1.png",
        box=(3080, 4380, 3835, 5150),
        output_name="CPHO41-Q02-figure2a-page1-recrop-v1.png",
        description="第41届第2题图2a重裁候选图",
        visual_check="保留图2a、Q/T球、x/y轴、phi/theta/v_T/v_Q标记和图号。",
        boundary_note="从题面第1页原始渲染图重裁；因原排版图件紧邻正文，仍保留少量边缘空白，不作为正式人工销项。",
    ),
    CropSpec(
        asset_id="CPHO41-Q02-FIG2B-RECROP-V1",
        material_id="CPHO41-Q02",
        source_page=RENDER_DIR / "CPHO41-Q02-paper-page-2.png",
        box=(2960, 640, 3840, 1535),
        output_name="CPHO41-Q02-figure2b-page2-recrop-v1.png",
        description="第41届第2题图2b重裁候选图",
        visual_check="保留图2b、Q/T球、x/y轴、v_T、v_Q0、theta_f、phi等标记。",
        boundary_note="从题面第2页原始渲染图重裁；去除旧裁切中的下方题干残边，不作为正式人工销项。",
    ),
    CropSpec(
        asset_id="CPHO41-Q02-FIG2C-RECROP-V1",
        material_id="CPHO41-Q02",
        source_page=RENDER_DIR / "CPHO41-Q02-paper-page-2.png",
        box=(3130, 1660, 3850, 2185),
        output_name="CPHO41-Q02-figure2c-page2-recrop-v1.png",
        description="第41届第2题图2c重裁候选图",
        visual_check="保留图2c、球杆/球/桌面、M、omega_0、v_0、h和图号。",
        boundary_note="从题面第2页原始渲染图重裁；为保留M、h和左侧箭头，左缘仍可能有轻微邻近正文残边，不作为正式人工销项。",
    ),
    CropSpec(
        asset_id="CPHO41-Q02-TABLE-RECROP-V1",
        material_id="CPHO41-Q02",
        source_page=RENDER_DIR / "CPHO41-Q02-paper-page-2.png",
        box=(520, 3020, 3300, 3350),
        output_name="CPHO41-Q02-table-page2-recrop-v1.png",
        description="第41届第2题第(4.3)问空表重裁候选图",
        visual_check="保留phi、theta_f两行表头及六个取值栏，左右边框完整。",
        boundary_note="从题面第2页原始渲染图重裁；表格较宽，保留少量上下空白以避免裁边，不作为正式人工销项。",
    ),
    CropSpec(
        asset_id="CPHO41-Q07-FIG7A-RECROP-V1",
        material_id="CPHO41-Q07",
        source_page=RENDER_DIR / "CPHO41-Q07-paper-page-4.png",
        box=(3150, 3510, 3900, 3995),
        output_name="CPHO41-Q07-figure7a-page4-recrop-v1.png",
        description="第41届第7题图7a重裁候选图",
        visual_check="保留圆环、电子符号和图7a图号。",
        boundary_note="从题面第4页原始渲染图重裁；图7a旧裁切基本可用，本轮统一生成来源明确候选图，不作为正式人工销项。",
    ),
    CropSpec(
        asset_id="CPHO41-Q07-FIG7B-RECROP-V1",
        material_id="CPHO41-Q07",
        source_page=RENDER_DIR / "CPHO41-Q07-paper-page-4.png",
        box=(3210, 4265, 3900, 5015),
        output_name="CPHO41-Q07-figure7b-page4-recrop-v1.png",
        description="第41届第7题图7b重裁候选图",
        visual_check="保留圆环、电子符号、磁通箭头、Phi标记和图7b图号。",
        boundary_note="从题面第4页原始渲染图重裁；去除旧裁切左侧邻近题干残边，不作为正式人工销项。",
    ),
]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def write_manifest(rows: list[dict[str, str]]) -> None:
    manifest = ASSET_DIR / "CPHO41_Q02_Q07_recrop_manifest.csv"
    fieldnames = [
        "asset_id",
        "material_id",
        "description",
        "source_page",
        "crop_box_left_top_right_bottom",
        "output_file",
        "output_size_px",
        "file_sha256",
        "visual_check",
        "boundary_note",
    ]
    with manifest.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_review(rows: list[dict[str, str]]) -> None:
    review = TRANSCRIPT_DIR / "CPHO41_Q02_Q07_figure_recrop_review_v1.md"
    lines = [
        "# CPHO41-Q02/Q07 题图重裁候选记录 V1",
        "",
        "任务：`G1-07-A1-FIG-REDRAW-41Q02-Q07`",
        "",
        "## 处理边界",
        "",
        "- 本轮只从已渲染的原始题面页面重新裁切图件，不重绘、不补字、不修图、不改动 `00_originals/` 或原始PDF；",
        "- 新图件是来源明确的候选图，可用于后续人工复核、附录准备或正式图件重绘参考；",
        "- 因未填写真实校对人和校对日期，本轮不关闭 `CPHO41-Q02-FIG` 或 `CPHO41-Q07-FIG`；",
        "- 若正式论文需要高清出版图，仍建议在人工确认后依据这些候选图重绘矢量版或重新导出高分辨率图。",
        "",
        "## 输出清单",
        "",
        "| 图件 | 输出文件 | 来源页 | 裁切框 | 复核要点 |",
        "|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['asset_id']} | `{row['output_file']}` | `{row['source_page']}` | "
            f"`{row['crop_box_left_top_right_bottom']}` | {row['visual_check']} |"
        )
    lines.extend(
        [
            "",
            "## 当前判断",
            "",
            "1. 第41届第2题图2a、图2b、图2c和第(4.3)问空表已形成重裁候选版，旧裁切中的邻近题干或公式残边风险有所降低。",
            "2. 第41届第7题图7a和图7b已形成统一重裁候选版，其中图7b旧裁切左侧邻近题干残边已通过重裁处理。",
            "3. 所有候选图均来自 `03_corpus/manual_review_renders/G1-07-A1/` 的页面证据图，生成信息登记在 `03_corpus/item_assets/CPHO41_Q02_Q07_recrop_manifest.csv`。",
            "4. 本记录不等同于真实人工校对完成，不生成正式编码证据摘录，也不替代后续论文用图的最终审定。",
            "",
            "## 后续最小动作",
            "",
            "- 若继续处理图件：人工打开六张候选图与原PDF页对照，确认图号、变量、箭头、电子符号和表格边框是否完整，再决定是否关闭FIG项；",
            "- 若转向扩大语料校对：继续 `G1-07-A1-TRANSCRIBE-40Q03`，处理A组后续高风险OCR/公式问题。",
            "",
        ]
    )
    review.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    rows: list[dict[str, str]] = []
    for spec in SPECS:
        source = Image.open(spec.source_page).convert("RGB")
        crop = source.crop(spec.box)
        output = ASSET_DIR / spec.output_name
        crop.save(output)
        rows.append(
            {
                "asset_id": spec.asset_id,
                "material_id": spec.material_id,
                "description": spec.description,
                "source_page": rel(spec.source_page),
                "crop_box_left_top_right_bottom": ",".join(str(v) for v in spec.box),
                "output_file": rel(output),
                "output_size_px": f"{crop.size[0]}x{crop.size[1]}",
                "file_sha256": sha256_file(output),
                "visual_check": spec.visual_check,
                "boundary_note": spec.boundary_note,
            }
        )
    write_manifest(rows)
    write_review(rows)
    print(f"Wrote {len(rows)} recropped assets")


if __name__ == "__main__":
    main()
