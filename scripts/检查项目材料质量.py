#!/usr/bin/env python3
"""检查当前有效论文材料的数量、文字、链接与主键完整性。"""

from __future__ import annotations

import csv
import hashlib
import re
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote


项目根目录 = Path(__file__).resolve().parents[1]
当前材料根目录 = 项目根目录 / "10_outputs/当前有效材料_Markdown版"
质量目录 = 项目根目录 / "09_quality"
检查结果路径 = 质量目录 / "项目材料质量检查_G8-90.csv"
重复登记路径 = 质量目录 / "项目材料重复文件登记_G8-90.csv"
报告路径 = 质量目录 / "G8-90项目材料清理与美化报告.md"

维度 = {"模型建构", "科学推理", "科学论证", "质疑创新"}
链接模式 = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


def 读取表格(路径: Path) -> list[dict[str, str]]:
    with 路径.open("r", encoding="utf-8-sig", newline="") as 文件:
        return list(csv.DictReader(文件))


def 写入表格(路径: Path, 表头: list[str], 数据: list[dict[str, object]]) -> None:
    with 路径.open("w", encoding="utf-8-sig", newline="") as 文件:
        写入器 = csv.DictWriter(文件, fieldnames=表头, lineterminator="\n")
        写入器.writeheader()
        写入器.writerows(数据)


def 文件哈希(路径: Path) -> str:
    计算器 = hashlib.sha256()
    with 路径.open("rb") as 文件:
        for 分块 in iter(lambda: 文件.read(1024 * 1024), b""):
            计算器.update(分块)
    return 计算器.hexdigest()


def 本地链接错误() -> list[tuple[str, str]]:
    错误: list[tuple[str, str]] = []
    for 路径 in 当前材料根目录.rglob("*.md"):
        内容 = 路径.read_text(encoding="utf-8")
        for 原链接 in 链接模式.findall(内容):
            目标 = unquote(原链接.strip().strip("<>").split("#", 1)[0])
            if not 目标 or 目标.startswith(("http://", "https://", "mailto:")):
                continue
            if not (路径.parent / 目标).resolve().exists():
                错误.append((路径.relative_to(项目根目录).as_posix(), 原链接))
    return 错误


def 生成检查() -> tuple[list[dict[str, object]], list[dict[str, object]], dict[str, object]]:
    题干文件 = sorted((当前材料根目录 / "02_试题题干与参考解答").glob("CPHO??-Q??.md"))
    图件 = sorted((当前材料根目录 / "02_试题题干与参考解答/图件").glob("*.png"))
    评分文件 = sorted((当前材料根目录 / "03_逐题评分标准").glob("CPHO??-Q??_评分标准.md"))
    原卷对应文本 = sorted((当前材料根目录 / "04_原始PDF对应文本").glob("*.md"))
    Markdown文件 = sorted(当前材料根目录.rglob("*.md"))

    空文件: list[Path] = []
    不可读文件: list[Path] = []
    旧版本写法: list[Path] = []
    for 路径 in Markdown文件:
        内容 = 路径.read_text(encoding="utf-8")
        if not 内容.strip():
            空文件.append(路径)
        if "�" in 内容 or re.search(r"[\ue000-\uf8ff]", 内容):
            不可读文件.append(路径)
        if re.search(r"(?i)\bv3\b", 内容):
            旧版本写法.append(路径)

    索引路径 = 项目根目录 / "03_corpus/item_index.csv"
    编码路径 = 项目根目录 / "07_analysis/data/作者授权采用分析版/第35至42届科学思维作者授权采用分析表.csv"
    索引数据 = 读取表格(索引路径)
    编码数据 = 读取表格(编码路径)
    索引分析单元 = {str(行.get("item_id", "")) for 行 in 索引数据}
    索引大题 = {
        匹配.group(0)
        for 行 in 索引数据
        if (匹配 := re.match(r"CPHO\d+-Q\d+", str(行.get("item_id", ""))))
    }
    编码键 = [(str(行.get("item_id", "")), str(行.get("dimension", ""))) for 行 in 编码数据]
    编码按单元: dict[str, set[str]] = defaultdict(set)
    for 分析单元, 当前维度 in 编码键:
        编码按单元[分析单元].add(当前维度)

    断链 = 本地链接错误()
    论文PDF = 项目根目录 / "10_outputs/华东师大2025格式论文/build/全国中学生物理竞赛复赛试题的科学思维要求与教学启示.pdf"
    图册PDF = 项目根目录 / "10_outputs/全量复赛题干解析与TikZ图册/build/全量题干解析与TikZ图册.pdf"
    答辩PPT = 项目根目录 / "10_outputs/答辩PPT/全国中学生物理竞赛复赛理论试题的科学思维要求及教学设计启示_答辩PPT.pptx"

    检查: list[dict[str, object]] = []

    def 添加(编号: str, 项目: str, 期望: object, 实际: object, 通过: bool, 说明: str) -> None:
        检查.append(
            {
                "检查编号": 编号,
                "检查项目": 项目,
                "期望": 期望,
                "实际": 实际,
                "结果": "通过" if 通过 else "失败",
                "说明": 说明,
            }
        )

    添加("M01", "复赛大题数", 60, len(索引大题), len(索引大题) == 60, "按届次与大题号去重")
    添加("M02", "分析单元索引", 221, len(索引数据), len(索引数据) == 221, "以item_index.csv为准")
    添加("M03", "分析单元主键唯一", 221, len(索引分析单元), len(索引分析单元) == 221, "不得重复或空缺")
    添加("M04", "正式编码记录", 884, len(编码数据), len(编码数据) == 884, "221个单元乘以4个维度")
    添加("M05", "编码主键唯一", 884, len(set(编码键)), len(set(编码键)) == 884, "item_id与dimension联合主键")
    完整维度单元 = sum(1 for 当前维度 in 编码按单元.values() if 当前维度 == 维度)
    添加("M06", "每单元四维完整", 221, 完整维度单元, 完整维度单元 == 221, "模型建构、科学推理、科学论证、质疑创新")
    添加("M07", "逐题题干与解答Markdown", 60, len(题干文件), len(题干文件) == 60, "每道大题一份可读文本")
    添加("M08", "逐题评分标准Markdown", 60, len(评分文件), len(评分文件) == 60, "每道大题一份评分入口")
    添加("M09", "原始PDF对应文本", 10, len(原卷对应文本), len(原卷对应文本) == 10, "第35至40届合并卷，第41至42届试题和解答分开")
    添加("M10", "题图与解题图", "数量大于0", len(图件), bool(图件), "当前Markdown共享图件目录")
    添加("M11", "Markdown空文件", 0, len(空文件), not 空文件, "当前有效材料全量扫描")
    添加("M12", "Markdown不可读字符", 0, len(不可读文件), not 不可读文件, "检查替换字符和私用区字符")
    添加("M13", "当前材料使用中文版本名", 0, len(旧版本写法), not 旧版本写法, "统一写作第三版")
    添加("M14", "Markdown本地链接断链", 0, len(断链), not 断链, "包括题图、解题图、PDF、PPT与交叉索引")
    添加("M15", "当前论文PDF", "存在且非空", 论文PDF.stat().st_size if 论文PDF.exists() else 0, 论文PDF.exists() and 论文PDF.stat().st_size > 0, "当前LaTeX编译成果")
    添加("M16", "当前全量图册PDF", "存在且非空", 图册PDF.stat().st_size if 图册PDF.exists() else 0, 图册PDF.exists() and 图册PDF.stat().st_size > 0, "第35至42届60道大题")
    添加("M17", "当前答辩PPT", "存在且非空", 答辩PPT.stat().st_size if 答辩PPT.exists() else 0, 答辩PPT.exists() and 答辩PPT.stat().st_size > 0, "当前答辩材料")

    哈希分组: dict[str, list[Path]] = defaultdict(list)
    for 路径 in sorted(当前材料根目录.rglob("*")):
        if 路径.is_file():
            哈希分组[文件哈希(路径)].append(路径)
    重复登记 = []
    for 哈希, 路径组 in sorted(哈希分组.items()):
        if len(路径组) < 2:
            continue
        重复登记.append(
            {
                "SHA256": 哈希,
                "重复数量": len(路径组),
                "文件路径": " | ".join(路径.relative_to(项目根目录).as_posix() for 路径 in 路径组),
                "处理意见": "当前阅读包内完全重复，后续生成时应合并或保留唯一入口",
            }
        )

    附加信息 = {
        "Markdown文件数": len(Markdown文件),
        "图件数": len(图件),
        "重复组数": len(重复登记),
        "断链明细": 断链,
    }
    return 检查, 重复登记, 附加信息


def main() -> None:
    检查, 重复登记, 附加信息 = 生成检查()
    写入表格(
        检查结果路径,
        ["检查编号", "检查项目", "期望", "实际", "结果", "说明"],
        检查,
    )
    写入表格(
        重复登记路径,
        ["SHA256", "重复数量", "文件路径", "处理意见"],
        重复登记,
    )
    通过数 = sum(行["结果"] == "通过" for 行 in 检查)
    报告 = f"""# G8-90 项目材料清理与美化报告

## 处理结果

| 项目 | 结果 |
|---|---:|
| 质量检查 | {通过数}/{len(检查)}通过 |
| 复赛大题 | 60道 |
| 分析单元 | 221个 |
| 正式编码 | 884条 |
| 当前Markdown | {附加信息['Markdown文件数']}份 |
| 题图与解题图 | {附加信息['图件数']}张 |
| 断链 | {len(附加信息['断链明细'])}条 |
| 完全重复组 | {附加信息['重复组数']}组 |

## 本次清理

- 根目录增加唯一中文材料入口，把论文、图册、试题、编码、统计、PPT和学校格式材料收束到同一页。
- 当前有效材料包按“题干与解答—评分标准—编码框架—正式编码—统计结果—论文交付”重排阅读顺序。
- 修复10份原始PDF对应文本中的题图和解题图链接，所有本地Markdown链接纳入自动检查。
- 根目录结构说明和输出目录说明已改为当前版，不再把初始空模板或旧工作稿写成当前成果。
- 历史数据和原始依据保留用于追溯，未覆盖、未伪装为当前主数据。

## 可复现入口

```bash
python3 scripts/生成当前有效材料Markdown包.py
python3 scripts/检查项目材料质量.py
python3 scripts/生成中文数据材料包.py
```

详细检查见 `项目材料质量检查_G8-90.csv`，完全重复文件见 `项目材料重复文件登记_G8-90.csv`。
"""
    报告路径.write_text(报告, encoding="utf-8")

    失败 = [行 for 行 in 检查 if 行["结果"] != "通过"]
    if 失败:
        raise SystemExit(f"失败：{len(失败)}项材料质量检查未通过")
    print(f"通过：{len(检查)}/{len(检查)}项材料质量检查")


if __name__ == "__main__":
    main()
