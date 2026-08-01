#!/usr/bin/env python3
"""为项目全部数据材料建立中文命名入口和可追溯目录。"""

from __future__ import annotations

import argparse
import csv
import hashlib
import os
import re
import shutil
import subprocess
from collections import Counter
from datetime import datetime
from pathlib import Path


项目根目录 = Path(__file__).resolve().parents[1]
输出根目录 = 项目根目录 / "10_outputs" / "论文数据材料_中文整理版"
链接根目录 = 输出根目录 / "材料链接"

扫描目录 = [
    "scripts",
    "00_originals",
    "01_positioning",
    "02_literature",
    "03_corpus",
    "04_framework",
    "05_fieldwork",
    "06_teaching_validation",
    "07_analysis/data",
    "07_analysis/results",
    "07_analysis/scripts",
    "08_manuscript",
    "09_quality",
    "10_outputs",
]

扫描根文件 = [
    "00_READ_ME_FIRST.md",
    "MASTER_PLAN.md",
    "AGENTS.md",
    "PROJECT_STATUS.md",
    "TASKS.md",
    "CHANGELOG.md",
    "DATA_MANAGEMENT.md",
]

忽略文件名 = {".DS_Store", ".gitkeep"}
忽略后缀 = {".aux", ".log", ".toc", ".out", ".pyc"}
忽略目录名 = {"__pycache__"}

分类顺序 = [
    "01_原始项目材料",
    "02_研究定位与文献资料",
    "03_原始试题与参考答案",
    "04_题目语料与题图",
    "05_人工校对与复核",
    "06_编码框架与判定规则",
    "07_正式编码与裁决",
    "08_统计分析结果",
    "09_调查与教学验证材料",
    "10_论文图表与章节源稿",
    "11_质量核查与证据台账",
    "12_论文与图册成果",
    "13_复现程序",
    "99_其他材料",
]

英文词对照 = {
    "adjudication": "裁决",
    "analysis": "分析",
    "archive": "历史归档",
    "audit": "审计",
    "baseline": "基线",
    "batch": "批次",
    "boundary": "边界",
    "build": "构建",
    "candidate": "候选",
    "case": "案例",
    "chapter": "章节",
    "checklist": "清单",
    "citation": "引文",
    "closure": "关闭",
    "codebook": "编码手册",
    "coding": "编码",
    "cooccurrence": "共现",
    "competition": "届次",
    "consent": "知情同意",
    "correction": "更正",
    "current": "当前",
    "data": "数据",
    "decision": "决定",
    "descriptive": "描述统计",
    "dimension": "维度",
    "disagreement": "分歧",
    "distribution": "分布",
    "draft": "草稿",
    "entry": "入口",
    "evidence": "证据",
    "expert": "专家",
    "figure": "图",
    "final": "最终",
    "formal": "正式",
    "framework": "框架",
    "generated": "生成结果",
    "handoff": "交接",
    "healthcheck": "健康检查",
    "index": "索引",
    "input": "输入",
    "instructions": "填写说明",
    "internal": "内部",
    "intake": "接收",
    "item": "题目",
    "knowledge": "知识模块",
    "level": "层级",
    "lock": "冻结",
    "log": "日志",
    "manifest": "清单",
    "manual": "人工",
    "matrix": "矩阵",
    "metadata": "元数据",
    "output": "输出",
    "overview": "概览",
    "package": "材料包",
    "paper": "试题",
    "pilot": "试编码",
    "plan": "方案",
    "presence": "出现情况",
    "protocol": "规范",
    "qa": "质量检查",
    "quality": "质量",
    "queue": "队列",
    "raw": "原始",
    "readiness": "就绪度",
    "reference": "参考文献",
    "register": "登记表",
    "reliability": "一致性",
    "render": "渲染",
    "report": "报告",
    "results": "结果",
    "result": "结果",
    "return": "回填",
    "reviewed": "已复核",
    "review": "复核",
    "route": "路线",
    "rater": "评分者",
    "score": "分值",
    "script": "程序",
    "solution": "解答",
    "source": "来源",
    "status": "状态",
    "summary": "汇总",
    "supplement": "补充",
    "table": "表",
    "template": "模板",
    "trace": "追溯",
    "training": "培训",
    "transcription": "转写",
    "validation": "验证",
    "visual": "视觉核查",
    "worklist": "工作清单",
    "working": "工作",
}


def 运行命令(*参数: str) -> str:
    结果 = subprocess.run(
        参数,
        cwd=项目根目录,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return 结果.stdout


def git状态表() -> tuple[set[str], dict[str, str]]:
    已跟踪 = set(运行命令("git", "ls-files", "-z").split("\0"))
    状态: dict[str, str] = {}
    原始 = subprocess.run(
        ["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"],
        cwd=项目根目录,
        check=True,
        stdout=subprocess.PIPE,
    ).stdout.decode("utf-8", errors="replace")
    条目 = 原始.split("\0")
    序号 = 0
    while 序号 < len(条目):
        条 = 条目[序号]
        序号 += 1
        if not 条:
            continue
        标记 = 条[:2]
        路径 = 条[3:]
        if 标记[0] in {"R", "C"} and 序号 < len(条目):
            路径 = 条目[序号]
            序号 += 1
        状态[路径] = 标记
    return 已跟踪, 状态


def 应纳入(路径: Path) -> bool:
    相对 = 路径.relative_to(项目根目录)
    if 输出根目录 in 路径.parents or 路径 == 输出根目录:
        return False
    if any(部分 in 忽略目录名 for 部分 in 相对.parts):
        return False
    if 路径.name in 忽略文件名:
        return False
    if 路径.suffix.lower() in 忽略后缀:
        return False
    if 路径.name.endswith(".synctex.gz"):
        return False
    return 路径.is_file()


def 收集材料() -> list[Path]:
    材料: set[Path] = set()
    for 目录 in 扫描目录:
        根 = 项目根目录 / 目录
        if not 根.exists():
            continue
        for 路径 in 根.rglob("*"):
            if 应纳入(路径):
                材料.add(路径)
    for 文件名 in 扫描根文件:
        路径 = 项目根目录 / 文件名
        if 路径.exists() and 应纳入(路径):
            材料.add(路径)
    return sorted(材料, key=lambda 值: 值.relative_to(项目根目录).as_posix())


def 分类(相对路径: str) -> str:
    if 相对路径 in {"00_READ_ME_FIRST.md", "MASTER_PLAN.md", "AGENTS.md"}:
        return "01_原始项目材料"
    if 相对路径 in {"PROJECT_STATUS.md", "TASKS.md", "CHANGELOG.md", "DATA_MANAGEMENT.md"}:
        return "11_质量核查与证据台账"
    if 相对路径.startswith("scripts/"):
        return "13_复现程序"
    if 相对路径.startswith("00_originals/"):
        return "01_原始项目材料"
    if 相对路径.startswith(("01_positioning/", "02_literature/")):
        return "02_研究定位与文献资料"
    if 相对路径.startswith(("03_corpus/raw_papers/", "03_corpus/raw_solutions/")):
        return "03_原始试题与参考答案"
    if 相对路径.startswith(("03_corpus/item_texts/", "03_corpus/item_assets/")):
        return "04_题目语料与题图"
    if 相对路径.startswith("03_corpus/") and any(
        词 in 相对路径.lower()
        for 词 in ("manual", "review", "return", "no_return", "queue", "human_reviewer")
    ):
        return "05_人工校对与复核"
    if 相对路径.startswith("03_corpus/"):
        if Path(相对路径).suffix.lower() in {".py", ".sh"}:
            return "13_复现程序"
        return "04_题目语料与题图"
    if 相对路径.startswith("04_framework/"):
        return "06_编码框架与判定规则"
    if 相对路径.startswith("07_analysis/data/") or (
        相对路径.startswith("07_analysis/results/formal_rater_r01/")
        and "/correction_v1/" not in 相对路径
    ):
        return "07_正式编码与裁决"
    if 相对路径.startswith("07_analysis/results/"):
        return "08_统计分析结果"
    if 相对路径.startswith(("05_fieldwork/", "06_teaching_validation/")):
        return "09_调查与教学验证材料"
    if 相对路径.startswith("08_manuscript/"):
        return "10_论文图表与章节源稿"
    if 相对路径.startswith("09_quality/"):
        return "11_质量核查与证据台账"
    if 相对路径.startswith("10_outputs/"):
        if Path(相对路径).suffix.lower() in {".py", ".sh"}:
            return "13_复现程序"
        return "12_论文与图册成果"
    if 相对路径.startswith("07_analysis/scripts/") or Path(相对路径).suffix.lower() in {
        ".py",
        ".sh",
    }:
        return "13_复现程序"
    return "99_其他材料"


def 材料状态(相对路径: str) -> str:
    当前主文件 = {
        "03_corpus/item_index.csv",
        "07_analysis/data/第35至42届科学思维第三版唯一编码表.csv",
    }
    if 相对路径 in 当前主文件:
        return "当前主数据"
    if 相对路径.startswith("07_analysis/results/第三版正式结果/"):
        return "当前主分析结果"
    if 相对路径.startswith("07_analysis/results/复分析_G8-34/"):
        return "当前复分析结果"
    if 相对路径.startswith(("03_corpus/raw_papers/", "03_corpus/raw_solutions/")):
        return "原始依据"
    if 相对路径.startswith("03_corpus/item_texts/"):
        return "当前题目语料"
    if 相对路径.endswith(
        (
            "中学生物理竞赛复赛试题的科学思维要求与教学转化研究.pdf",
            "全量题干解析与TikZ图册.pdf",
        )
    ):
        return "当前成果"
    if any(片段 in 相对路径 for 片段 in ("/archive/", "/drafts/", "historical", "placeholder")):
        return "历史或中间版本"
    if "template" in 相对路径.lower():
        return "空白模板"
    return "项目材料"


def 文件用途(类别: str) -> str:
    return {
        "01_原始项目材料": "保存原初稿与初始附件，仅作历史对照",
        "02_研究定位与文献资料": "支持研究范围、理论与文献追溯",
        "03_原始试题与参考答案": "作为题目语料的原始依据",
        "04_题目语料与题图": "提供题干、解答、元数据与图件",
        "05_人工校对与复核": "记录OCR、公式、图件和人工复核过程",
        "06_编码框架与判定规则": "规定分析单位、维度与等级判定",
        "07_正式编码与裁决": "保存评分、分歧、裁决和证据链",
        "08_统计分析结果": "保存描述统计、复分析与敏感性结果",
        "09_调查与教学验证材料": "保存伦理、采集和教学验证模板或记录",
        "10_论文图表与章节源稿": "保存论文正文、图表和参考文献源文件",
        "11_质量核查与证据台账": "保存主张、证据、格式和复现质量检查",
        "12_论文与图册成果": "保存可阅读的论文、图册和交付文件",
        "13_复现程序": "保存生成、检查和统计复现程序",
        "99_其他材料": "保存未归入以上类别的项目材料",
    }[类别]


def 文件哈希(路径: Path) -> str:
    计算器 = hashlib.sha256()
    with 路径.open("rb") as 文件:
        for 分块 in iter(lambda: 文件.read(1024 * 1024), b""):
            计算器.update(分块)
    return 计算器.hexdigest()


def 提取中文标题(路径: Path) -> str:
    if 路径.suffix.lower() != ".md" or 路径.stat().st_size > 2_000_000:
        return ""
    try:
        with 路径.open("r", encoding="utf-8", errors="ignore") as 文件:
            for _ in range(30):
                行 = 文件.readline()
                if not 行:
                    break
                匹配 = re.match(r"^#{1,3}\s+(.+?)\s*$", 行)
                if 匹配 and re.search(r"[\u4e00-\u9fff]", 匹配.group(1)):
                    return 匹配.group(1)
    except OSError:
        return ""
    return ""


def 题目标签(相对路径: str) -> str:
    文件名 = Path(相对路径).stem
    匹配 = re.search(r"CPHO(\d+)[-_]Q(\d+)", 文件名, flags=re.IGNORECASE)
    if not 匹配:
        匹配 = re.search(r"cpho_(\d+)_\d{4}", 文件名, flags=re.IGNORECASE)
        if 匹配:
            return f"第{int(匹配.group(1))}届"
        return ""
    届次 = int(匹配.group(1))
    题号 = int(匹配.group(2))
    标签 = f"第{届次}届第{题号:02d}题"
    小问 = re.search(r"Q\d+[-_](\d+)(?:\\D|$)", 文件名, flags=re.IGNORECASE)
    if 小问:
        标签 += f"第{int(小问.group(1))}小问"
    return 标签


def 类型标签(相对路径: str) -> str:
    小写 = 相对路径.lower()
    if "/item_texts/" in 小写:
        return "题干与参考解答整理"
    if "/raw_papers/" in 小写:
        return "复赛试题"
    if "/raw_solutions/" in 小写:
        return "参考答案"
    if "formula_check" in 小写:
        return "公式核对表"
    if "transcription" in 小写:
        return "题面人工转写"
    if "solution" in 小写 and any(后缀 in 小写 for 后缀 in (".png", ".jpg", ".pdf")):
        return "解答图"
    if any(词 in 小写 for 词 in ("figure", "figures", "-fig", "_fig")):
        return "题图"
    if "render" in 小写:
        return "复核渲染页"
    if "/questions/" in 小写:
        return "图册题目源稿"
    if "/markdown/assets/" in 小写:
        return "题目与解析配图"
    if "/markdown/" in 小写:
        return "题干解析阅读稿"
    if "/tikz/" in 小写:
        return "绘图源文件"
    return ""


def 通用中文标签(路径: Path) -> str:
    原名 = 路径.stem
    标签 = 原名
    标签 = re.sub(r"CPHO\d+[-_]Q\d+(?:[-_]\d+)?", "", 标签, flags=re.IGNORECASE)
    标签 = re.sub(r"\bR0*1\b", "复核批次01", 标签, flags=re.IGNORECASE)
    标签 = re.sub(r"\bADJ[-_]?0*(\d+)\b", r"裁决批次\1", 标签, flags=re.IGNORECASE)
    标签 = re.sub(r"\bG(\d+)[-_](\d+)\b", r"任务\1之\2", 标签, flags=re.IGNORECASE)
    标签 = re.sub(r"\bv(\d+)\b", r"第\1版", 标签, flags=re.IGNORECASE)
    for 英文, 中文 in sorted(英文词对照.items(), key=lambda 对: -len(对[0])):
        标签 = re.sub(rf"(?i)(?<![A-Za-z]){re.escape(英文)}(?![A-Za-z])", 中文, 标签)
    标签 = re.sub(r"(?i)\brater[-_]?a\b", "评分者甲", 标签)
    标签 = re.sub(r"(?i)\brater[-_]?b\b", "评分者乙", 标签)
    标签 = re.sub(r"[A-Za-z]+", "", 标签)
    标签 = re.sub(r"[_\-\s]+", "_", 标签)
    标签 = re.sub(r"[^\u4e00-\u9fff0-9（）()_，、至第年月日]", "", 标签)
    标签 = 标签.strip("_")
    return 标签


def 中文文件名(路径: Path, 类别: str, 序号: int) -> str:
    相对路径 = 路径.relative_to(项目根目录).as_posix()
    题目标识 = 题目标签(相对路径)
    类型 = 类型标签(相对路径)
    标题 = 提取中文标题(路径)
    通用 = 通用中文标签(路径)

    if 题目标识:
        描述 = "_".join(部分 for 部分 in (题目标识, 类型, 通用) if 部分)
    elif 标题:
        描述 = 通用中文标签(Path(标题)) or 通用
    else:
        描述 = 通用
    if len(描述) < 2:
        描述 = 类别.split("_", 1)[1] + "材料"
    描述 = 描述[:72].rstrip("_")
    return f"材料{序号:04d}_{描述}{路径.suffix.lower()}"


def 写入表格(路径: Path, 表头: list[str], 行: list[dict[str, object]]) -> None:
    with 路径.open("w", encoding="utf-8-sig", newline="") as 文件:
        写入器 = csv.DictWriter(文件, fieldnames=表头, lineterminator="\n")
        写入器.writeheader()
        写入器.writerows(行)


def 生成材料包(复制模式: bool) -> None:
    材料 = 收集材料()
    已跟踪, 状态标记 = git状态表()

    临时目录 = 输出根目录 / "材料链接_生成中"
    if 临时目录.exists():
        shutil.rmtree(临时目录)
    临时目录.mkdir(parents=True, exist_ok=True)

    总目录: list[dict[str, object]] = []
    分类计数: Counter[str] = Counter()
    状态计数: Counter[str] = Counter()
    中文路径集合: set[str] = set()

    for 序号, 源路径 in enumerate(材料, start=1):
        相对路径 = 源路径.relative_to(项目根目录).as_posix()
        类别 = 分类(相对路径)
        分类计数[类别] += 1
        类内序号 = 分类计数[类别]
        名称 = 中文文件名(源路径, 类别, 类内序号)
        目标目录 = 临时目录 / 类别
        目标目录.mkdir(parents=True, exist_ok=True)
        目标 = 目标目录 / 名称
        if 目标.exists() or 目标.is_symlink():
            raise RuntimeError(f"中文目标重名：{目标}")
        if 复制模式:
            shutil.copy2(源路径, 目标)
            入口类型 = "副本"
        else:
            目标.symlink_to(os.path.relpath(源路径, 目标.parent))
            入口类型 = "相对链接"

        中文相对路径 = (Path("材料链接") / 类别 / 名称).as_posix()
        if 中文相对路径 in 中文路径集合:
            raise RuntimeError(f"中文路径重复：{中文相对路径}")
        中文路径集合.add(中文相对路径)

        if 相对路径 not in 已跟踪:
            git状态 = "未纳入Git"
        elif 相对路径 in 状态标记:
            git状态 = f"已跟踪但工作区有改动（{状态标记[相对路径]}）"
        else:
            git状态 = "已跟踪且工作区无改动"
        状态计数[git状态] += 1
        文件状态 = 材料状态(相对路径)
        统计 = 源路径.stat()
        总目录.append(
            {
                "材料编号": f"数据材料{序号:04d}",
                "材料类别": 类别.split("_", 1)[1],
                "中文文件名": 名称,
                "中文相对路径": 中文相对路径,
                "原始相对路径": 相对路径,
                "入口类型": 入口类型,
                "材料状态": 文件状态,
                "用途说明": 文件用途(类别),
                "文件类型": 源路径.suffix.lower().lstrip(".") or "无扩展名",
                "文件大小（字节）": 统计.st_size,
                "修改时间": datetime.fromtimestamp(统计.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                "Git状态": git状态,
                "SHA256": 文件哈希(源路径),
            }
        )

    if 链接根目录.exists() or 链接根目录.is_symlink():
        if 链接根目录.is_symlink() or 链接根目录.is_file():
            链接根目录.unlink()
        else:
            shutil.rmtree(链接根目录)
    临时目录.rename(链接根目录)

    总目录表头 = [
        "材料编号",
        "材料类别",
        "中文文件名",
        "中文相对路径",
        "原始相对路径",
        "入口类型",
        "材料状态",
        "用途说明",
        "文件类型",
        "文件大小（字节）",
        "修改时间",
        "Git状态",
        "SHA256",
    ]
    写入表格(输出根目录 / "数据材料总目录.csv", 总目录表头, 总目录)

    分类统计 = [
        {
            "材料类别": 类别.split("_", 1)[1],
            "文件数量": 分类计数.get(类别, 0),
            "说明": 文件用途(类别),
        }
        for 类别 in 分类顺序
        if 分类计数.get(类别, 0)
    ]
    写入表格(
        输出根目录 / "数据材料分类统计.csv",
        ["材料类别", "文件数量", "说明"],
        分类统计,
    )

    按原路径 = {str(行["原始相对路径"]): 行 for 行 in 总目录}

    def 中文入口(原路径: str, 显示文字: str) -> str:
        行 = 按原路径.get(原路径)
        if not 行:
            return f"- {显示文字}：未纳入，待核实"
        return f"- [{显示文字}](./{行['中文相对路径']})"

    当前导航 = f"""# 当前主数据导航

本页只列当前研究与交付最常用的主文件。全部历史版本、过程材料和逐文件哈希见 `数据材料总目录.csv`。

## 一、语料主入口

{中文入口("03_corpus/item_index.csv", "第35至42届221个分析单元题目索引")}

- [原始试题与参考答案（{分类计数.get("03_原始试题与参考答案", 0)}个文件）](./材料链接/03_原始试题与参考答案/)
- [题目语料与题图（{分类计数.get("04_题目语料与题图", 0)}个文件）](./材料链接/04_题目语料与题图/)
- [人工校对与复核（{分类计数.get("05_人工校对与复核", 0)}个文件）](./材料链接/05_人工校对与复核/)

## 二、编码与证据主入口

{中文入口("04_framework/科学思维编码手册_第三版.md", "科学思维编码手册第三版")}

{中文入口("04_framework/科学思维编码决策矩阵_第三版.csv", "科学思维编码决策矩阵第三版")}

{中文入口("07_analysis/data/第35至42届科学思维第三版唯一编码表.csv", "当前第三版正式编码表（884行）")}

{中文入口("07_analysis/data/第35至42届科学思维第三版唯一编码表.csv", "当前第三版编码证据链（884行，与编码字段同表保存）")}

- [正式编码与裁决材料](./材料链接/07_正式编码与裁决/)

## 三、统计结果主入口

{中文入口("07_analysis/results/第三版正式结果/描述统计生成说明.md", "当前第三版描述统计报告")}

{中文入口("07_analysis/results/复分析_G8-34/最终编码数据复分析报告_G8-34.md", "最终编码数据独立复分析报告")}

- [全部统计分析结果](./材料链接/08_统计分析结果/)

## 四、论文与图册主入口

{中文入口("10_outputs/论文初稿_LaTeX/build/全国中学生物理竞赛复赛理论试题的科学思维要求及教学设计启示.pdf", "当前论文LaTeX PDF")}

{中文入口("10_outputs/全量复赛题干解析与TikZ图册/build/全量题干解析与TikZ图册.pdf", "第35至42届全量题干解析与TikZ图册PDF")}

- [论文图表与章节源稿](./材料链接/10_论文图表与章节源稿/)
- [论文与图册全部成果](./材料链接/12_论文与图册成果/)

## 五、如何判断哪个版本可用

1. 优先使用总目录中标为“当前主数据”“当前主分析结果”“当前复分析结果”或“当前成果”的文件。
2. “历史或中间版本”仅用于追溯，不得替代当前编码表、证据链或更正后统计结果。
3. “空白模板”不含真实研究结果。
4. 如需复算，使用“原始相对路径”；如需阅读和交接，直接使用本包中文入口。
"""
    (输出根目录 / "当前主数据导航.md").write_text(当前导航, encoding="utf-8")

    断链 = [
        路径
        for 路径 in 链接根目录.rglob("*")
        if 路径.is_symlink() and not 路径.exists()
    ]
    非中文文件名 = [
        路径
        for 路径 in 链接根目录.rglob("*")
        if 路径.is_file() or 路径.is_symlink()
        if re.search(r"[A-Za-z]", 路径.stem)
    ]
    当前编码 = 项目根目录 / "07_analysis/data/第35至42届科学思维第三版唯一编码表.csv"
    当前证据 = 当前编码

    def 数据行数(路径: Path) -> int:
        with 路径.open("r", encoding="utf-8-sig", newline="") as 文件:
            return sum(1 for _ in csv.DictReader(文件))

    检查 = [
        {
            "检查项目": "已纳入数据材料",
            "期望": "数量大于0",
            "实际": len(总目录),
            "结果": "通过" if 总目录 else "失败",
        },
        {
            "检查项目": "中文相对路径唯一",
            "期望": len(总目录),
            "实际": len(中文路径集合),
            "结果": "通过" if len(总目录) == len(中文路径集合) else "失败",
        },
        {
            "检查项目": "中文入口无断链",
            "期望": 0,
            "实际": len(断链),
            "结果": "通过" if not 断链 else "失败",
        },
        {
            "检查项目": "中文文件名不含英文字母",
            "期望": 0,
            "实际": len(非中文文件名),
            "结果": "通过" if not 非中文文件名 else "失败",
        },
        {
            "检查项目": "当前正式编码记录数",
            "期望": 884,
            "实际": 数据行数(当前编码),
            "结果": "通过" if 数据行数(当前编码) == 884 else "失败",
        },
        {
            "检查项目": "当前编码证据链记录数",
            "期望": 884,
            "实际": 数据行数(当前证据),
            "结果": "通过" if 数据行数(当前证据) == 884 else "失败",
        },
    ]
    写入表格(
        输出根目录 / "质量检查结果.csv",
        ["检查项目", "期望", "实际", "结果"],
        检查,
    )

    说明 = f"""# 论文数据材料中文整理版

生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 使用入口

1. 先打开 `当前主数据导航.md`，直接进入当前编码、统计、论文和图册。
2. 再打开 `数据材料分类统计.csv`，了解各类材料数量。
3. 需要找历史或过程材料时，打开 `数据材料总目录.csv`，按“材料状态”筛选。
4. 需要复现分析时，以总目录中的“原始相对路径”为准，机器分析路径没有被改动。

## 本次整理范围

本包共登记 {len(总目录)} 个文件，覆盖原始项目材料、研究定位与文献资料、原始试题与参考答案、题目语料与题图、人工校对与复核、编码框架、正式编码与裁决、统计结果、调查与教学验证材料、论文源稿、质量台账、成果文件和复现程序。

编译缓存和无研究内容的占位文件未纳入，包括 `.aux`、`.log`、`.toc`、`.pyc`、`.gitkeep`、`__pycache__` 和同步缓存。

## 中文命名原则

- 第35至42届题目统一命名为“第某届第某题”。
- 题面、解答、公式核对、题图、解析图和复核渲染页分别标明材料类型。
- 评分者、裁决、质量检查、版本和任务号转写为中文说明。
- 每个中文文件名前保留中文材料序号，防止同名覆盖。
- 文件扩展名保留通用格式，如 `.csv`、`.md`、`.pdf`，扩展名不是材料名称。

## 重要边界

- `07_analysis/data/第35至42届科学思维第三版唯一编码表.csv` 是当前描述性分析使用的正式编码表，并在同一记录中保存题干、解答和等级判定证据。
- `07_analysis/results/第三版正式结果/` 保存当前主分析输出。
- `07_analysis/results/复分析_G8-34/` 保存独立描述性复分析输出。
- 历史版本和中间过程保留用于追溯，不得替代上述当前主文件。
- 本包只重组入口和名称，不改变任何源文件内容、证据等级或研究结论。

## 版本控制说明

{chr(10).join(f"- {状态}：{数量}个" for 状态, 数量 in sorted(状态计数.items()))}

中文入口默认采用相对链接，避免把约数百兆的语料重复复制一遍。若需要移动到项目外独立使用，可运行：

```bash
python3 scripts/生成中文数据材料包.py --复制
```

复制模式会以相同中文目录生成实体副本，并继续保留原路径、哈希和状态对照。
"""
    (输出根目录 / "使用说明.md").write_text(说明, encoding="utf-8")

    if any(行["结果"] != "通过" for 行 in 检查):
        raise RuntimeError("中文数据材料包质量检查未全部通过")
    print(f"已整理 {len(总目录)} 个文件")
    print(f"输出目录：{输出根目录}")
    print(f"入口模式：{'实体副本' if 复制模式 else '相对链接'}")


def main() -> None:
    解析器 = argparse.ArgumentParser(description="生成中文命名的论文数据材料包")
    解析器.add_argument(
        "--复制",
        action="store_true",
        help="生成实体副本；默认生成不占额外空间的相对链接",
    )
    参数 = 解析器.parse_args()
    输出根目录.mkdir(parents=True, exist_ok=True)
    生成材料包(复制模式=参数.复制)


if __name__ == "__main__":
    main()
