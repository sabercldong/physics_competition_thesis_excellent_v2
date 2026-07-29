#!/usr/bin/env python3
"""Build the year-35 V3 mentor-perspective precode batch.

The output is an AI-assisted precode for substantive author review. It is not
merged into the formal V3 table and does not represent an external rater.
"""

from __future__ import annotations

import csv
import hashlib
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
INDEX = ROOT / "03_corpus/item_index.csv"
OUTPUT = ROOT / "07_analysis/data/第35届科学思维V3导师视角试编码.csv"
DIMENSIONS = ("模型建构", "科学推理", "科学论证", "质疑创新")


PROFILES = {
    "CPHO35-Q01-1": {
        "output": "确定物体绕地球作周期运动的初速度条件",
        "solution_lines": (105, 111),
        "模型建构": ("L2", "把发射状态表示为中心力场中的能量与角动量模型"),
        "科学推理": ("L3", "联立束缚能量、轨道几何和临界条件推出速度区间"),
    },
    "CPHO35-Q01-2": {
        "output": "求落地速度大小、方向和飞行时间",
        "solution_lines": (205, 211),
        "模型建构": ("L3", "协调中心力轨道、能量角动量守恒和径向时间积分"),
        "科学推理": ("L3", "由多项守恒关系及积分边界形成完整落地状态推理链"),
    },
    "CPHO35-Q02-1": {
        "output": "确定小球至多向右运动时的静止位置和初振幅条件",
        "solution_lines": (128, 135),
        "模型建构": ("L2", "建立弹簧势能、摩擦功和首次停止位置的分段模型"),
        "科学推理": ("L2", "由功能关系与静摩擦条件推出位置和参数区间"),
    },
    "CPHO35-Q02-2": {
        "output": "确定首次返向后至多向左运动时的静止位置和条件",
        "solution_lines": (178, 185),
        "模型建构": ("L3", "整合向右阶段、返向阶段和摩擦阈值的分段运动模型"),
        "科学推理": ("L3", "串联两阶段功能关系和方向切换条件完成分类判断"),
    },
    "CPHO35-Q02-3": {
        "output": "求完成n次往返后的静止位置和初振幅条件",
        "solution_lines": (247, 254),
        "模型建构": ("L3", "把各次左右端点和摩擦耗散组织为递推模型"),
        "科学推理": ("L3", "由端点递推、奇偶状态和停止条件得到通项区间"),
    },
    "CPHO35-Q02-4": {
        "output": "求完成n次往返直至静止的总路程",
        "solution_lines": (294, 301),
        "模型建构": ("L2", "用总机械能损失表示全过程摩擦功和总路程"),
        "科学推理": ("L2", "将前问终态代入总功能关系推出路程"),
    },
    "CPHO35-Q03-1": {
        "output": "求细杆打击中心到转轴的距离",
        "solution_lines": (118, 125),
        "模型建构": ("L2", "协调定轴转动和质心平动以定义打击中心条件"),
        "科学推理": ("L2", "联立角加速度与质心加速度关系求作用点"),
    },
    "CPHO35-Q03-2": {
        "output": "求撤轴前细杆转过给定角度时的转轴作用力",
        "solution_lines": (152, 159),
        "模型建构": ("L3", "整合碰撞后的复合刚体、定轴转动和质心动力学模型"),
        "科学推理": ("L3", "由碰撞守恒、转动能量和质心动力学形成多阶段推理链"),
    },
    "CPHO35-Q03-3": {
        "output": "求撤轴后杆端位置随时间的表达式",
        "solution_lines": (232, 239),
        "模型建构": ("L3", "将撤轴后的质心平抛与绕质心匀角转动整合为平面运动模型"),
        "科学推理": ("L3", "协调临界撤轴状态、质心轨迹和转动相位得到端点坐标"),
    },
    "CPHO35-Q03-4": {
        "output": "求撤轴后杆再转半圈时两端高度差",
        "solution_lines": (262, 270),
        "科学推理": ("L2", "由角位移确定时刻并代入竖直坐标关系"),
    },
    "CPHO35-Q04-1": {
        "output": "求四根通电导线产生的总磁场空间分布",
        "solution_lines": (126, 132),
        "模型建构": ("L2", "建立四根导线的坐标、方向和单线磁场矢量表示"),
        "科学推理": ("L2", "按电流方向逐项计算并完成矢量叠加"),
    },
    "CPHO35-Q04-2": {
        "output": "求原点附近总磁场的一阶近似",
        "solution_lines": (165, 171),
        "模型建构": ("L2", "把全空间磁场转化为原点邻域的局部线性模型"),
        "科学推理": ("L3", "对四个分量一致展开并保留一阶项后完成约化"),
    },
    "CPHO35-Q04-3": {
        "output": "求原子在原点附近所受磁场力",
        "solution_lines": (190, 197),
        "模型建构": ("L2", "把局部磁场大小映射为束缚势能并建立力的梯度表示"),
        "科学推理": ("L2", "由磁场近似、势能关系和梯度推出二维作用力"),
    },
    "CPHO35-Q04-4": {
        "output": "确定最易逸出位置并求临界逸出动能",
        "solution_lines": (225, 232),
        "模型建构": ("L3", "把全局磁场、束缚势垒和逸出路径整合为临界能量模型"),
        "科学推理": ("L3", "比较空间方向上的势垒并由能量差确定逸出阈值"),
    },
    "CPHO35-Q05-1": {
        "output": "选择转动参考系并建立、求解价电子运动方程",
        "solution_lines": (95, 107),
        "模型建构": ("L3", "选择适当转动系并整合回复力、洛伦兹力和惯性力"),
        "科学推理": ("L3", "由参考系变换和动力学方程约束求得简谐振动解"),
    },
    "CPHO35-Q05-2": {
        "output": "把转动系中的电子运动解变换到实验室系",
        "solution_lines": (195, 203),
        "模型建构": ("L2", "协调转动系与实验室系的坐标和相位表示"),
        "科学推理": ("L2", "利用坐标变换将两个旋转分量还原为实验室运动"),
    },
    "CPHO35-Q05-3": {
        "output": "证明谱线分裂为三条并求弱磁场频率间隔",
        "solution_lines": (218, 246),
        "模型建构": ("L2", "把电子运动分解为三个频率分量并映射为光谱线"),
        "科学推理": ("L3", "合成振动分量并结合弱场近似推出三条频率及等间隔"),
        "科学论证": ("L1", "用三个可定位的振动频率支持谱线一分为三的主张"),
    },
    "CPHO35-Q06-1": {
        "output": "求球壳外表面稳态温度",
        "solution_lines": (104, 111),
        "模型建构": ("L1", "把稳态输入热流映射为外表面净辐射平衡"),
        "科学推理": ("L2", "联立斯特藩定律和稳态能量守恒求温度"),
    },
    "CPHO35-Q06-2": {
        "output": "求球壳内表面稳态温度",
        "solution_lines": (121, 132),
        "模型建构": ("L2", "建立球对称稳态导热和径向面积变化模型"),
        "科学推理": ("L3", "由傅里叶定律建立径向微分关系并按内外边界积分"),
    },
    "CPHO35-Q06-3": {
        "output": "求内球稳态温度",
        "solution_lines": (158, 170),
        "模型建构": ("L3", "整合内球与球壳间的发射、吸收和多次辐射能量平衡"),
        "科学推理": ("L3", "协调两表面几何、比辐射率和净热流关系求内球温度"),
    },
    "CPHO35-Q07-1": {
        "output": "由弹簧衍射图估算钢丝直径、弹簧半径和螺距",
        "solution_lines": (121, 133),
        "模型建构": ("L2", "把两组衍射周期分别映射为钢丝直径和相邻丝间距"),
        "科学推理": ("L3", "联结图像测量、小角衍射关系和螺旋几何完成尺度估算"),
    },
    "CPHO35-Q07-2": {
        "output": "由X射线衍射图估算DNA螺旋半径和螺距",
        "solution_lines": (187, 200),
        "模型建构": ("L3", "把弹簧衍射—螺旋几何模型迁移并约束到DNA图像"),
        "科学推理": ("L3", "综合条纹角度、空间周期、波长和距离推得纳米尺度结构"),
    },
    "CPHO35-Q08-1": {
        "output": "求核跃迁发射反冲能和发射频率差",
        "solution_lines": (133, 146),
        "模型建构": ("L2", "建立光子发射与原子核反冲的能量—动量模型"),
        "科学推理": ("L2", "联立能量和动量守恒并作小量近似求频移"),
    },
    "CPHO35-Q08-2": {
        "output": "求核跃迁吸收反冲能和吸收频率差",
        "solution_lines": (183, 192),
        "模型建构": ("L2", "建立光子吸收与激发核反冲的能量—动量模型"),
        "科学推理": ("L2", "联立吸收过程守恒关系并作小量近似求频移"),
    },
    "CPHO35-Q08-3": {
        "output": "判断静止自由核之间能否发生共振吸收并说明理由",
        "solution_lines": (216, 233),
        "模型建构": ("L2", "把发射谱和吸收谱表示为具有能级宽度的两个频率区间"),
        "科学推理": ("L3", "比较反冲频移与线宽并检验两个频率区间的重叠条件"),
        "科学论证": ("L2", "以发射、吸收频率区间比较和数量级证据支持不能共振的结论"),
    },
    "CPHO35-Q08-4": {
        "output": "求运动晶体发生共振的速度范围并设计微小频移测量原理",
        "solution_lines": (253, 262),
        "模型建构": ("L3", "整合无反冲晶体、能级宽度、多普勒调谐和测量装置模型"),
        "科学推理": ("L3", "由共振区间和多普勒关系推出速度窗口及测量灵敏度"),
        "科学论证": ("L1", "用多普勒补偿关系说明所提测量原理为何可行"),
        "质疑创新": ("L2", "在给定灵敏度约束下提出移动吸收晶体的测量方案并给出计算"),
    },
}


LEVEL_EXCLUSION = {
    "L1": "一个核心结构足以完成任务；未出现两个需协调的认知要素，故不取L2。",
    "L2": "存在两个以上需协调的局部要素，不能降为L1；尚未形成多阶段相互约束的统一结构，故不取L3。",
    "L3": "多个规律、条件或阶段相互约束，不能降为L2；未要求超出当前任务的一般化或自主重构，故不取L4。",
    "L4": "任务要求超出当前特例并形成可迁移的新结构，低等级不足以解释该要求。",
}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_path(item_id: str) -> Path:
    match = re.match(r"(CPHO\d+-Q\d+)", item_id)
    if not match:
        raise ValueError(item_id)
    return ROOT / "03_corpus/item_texts" / f"{match.group(1)}.md"


def question_quote(path: Path, subquestion_no: str) -> str:
    text = path.read_text(encoding="utf-8-sig")
    question_part = text.split("## 参考解答", maxsplit=1)[0]
    line_marker = re.compile(
        rf"(?m)^[ \t]*(?:（{re.escape(subquestion_no)}）|\({re.escape(subquestion_no)}\))"
    )
    matches = list(line_marker.finditer(question_part))
    next_pattern = r"(?m)^[ \t]*(?:（\d+）|\(\d+\))"
    if not matches:
        inline_marker = re.compile(
            rf"(?:（{re.escape(subquestion_no)}）|\({re.escape(subquestion_no)}\))"
        )
        matches = list(inline_marker.finditer(question_part))
        next_pattern = r"(?:（\d+）|\(\d+\))"
    if not matches:
        raise ValueError(f"未找到题干小问: {path.name} #{subquestion_no}")
    start = matches[-1].start()
    next_marker = re.search(
        next_pattern,
        question_part[matches[-1].end():],
    )
    end = (
        matches[-1].end() + next_marker.start()
        if next_marker
        else question_part.find("```", matches[-1].end())
    )
    if end < start:
        end = len(question_part)
    return question_part[start:end].strip()


def line_quote(path: Path, line_range: tuple[int, int]) -> str:
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    start, end = line_range
    return "\n".join(lines[start - 1:end]).strip()


def absent_fields(dimension: str, output: str) -> tuple[str, str, str, str]:
    if dimension == "模型建构":
        activity = "题面未要求为本小问新建或调整对象—变量—约束表示"
        reason = f"完成“{output}”只需调用前问已经建立的关系并代入当前条件，本小问不自动继承前问的模型建构标签。"
    elif dimension == "科学推理":
        activity = "题面未要求从条件经过物理关系推出新结论"
        reason = f"完成“{output}”只涉及直接读数、照抄或机械代入，未达到科学推理存在门槛。"
    elif dimension == "科学论证":
        activity = "题面未要求围绕主张组织证据—理由关系"
        reason = f"完成“{output}”主要依靠建模或推理，不要求解释主张为何可信、比较论据或检验适用边界。"
    elif dimension == "质疑创新":
        activity = "题面未要求评价局限、提出替代、修正模型或开放设计"
        reason = f"完成“{output}”具有明确约束和标准求解目标，不包含主动改变既有模型或非唯一方案选择。"
    else:
        raise ValueError(dimension)
    return activity, "否", "未出现", reason


def main() -> None:
    index_rows = [
        row for row in read_rows(INDEX) if row["competition_no"] == "35"
    ]
    if len(index_rows) != 26 or set(PROFILES) != {row["item_id"] for row in index_rows}:
        raise ValueError("第35届分析单元与人工配置不一致")

    rows: list[dict[str, str]] = []
    for item in index_rows:
        item_id = item["item_id"]
        profile = PROFILES[item_id]
        source = source_path(item_id)
        q_quote = question_quote(source, item["subquestion_no"])
        s_quote = line_quote(source, profile["solution_lines"])
        for dimension in DIMENSIONS:
            if dimension in profile:
                level, activity = profile[dimension]
                present = "是"
                reason = (
                    f"完成“{profile['output']}”必须执行“{activity}”；"
                    f"该活动达到{dimension}{level}的最低充分标准。"
                )
                exclusion = LEVEL_EXCLUSION[level]
            else:
                activity, present, level, reason = absent_fields(
                    dimension, profile["output"]
                )
                exclusion = "未达到该维度存在门槛，因此不进入L1—L4分级。"

            rows.append(
                {
                    "item_id": item_id,
                    "competition_no": item["competition_no"],
                    "year": item["year"],
                    "question_no": item["question_no"],
                    "subquestion_no": item["subquestion_no"],
                    "dimension": dimension,
                    "analysis_unit": item["analysis_unit"],
                    "item_text_path": str(source.relative_to(ROOT)),
                    "item_text_sha256": sha256(source),
                    "page_paper": item["page_paper"],
                    "page_solution": item["page_solution"],
                    "required_output": profile["output"],
                    "question_quote": q_quote,
                    "question_location": f"题面第{item['page_paper']}页，第（{item['subquestion_no']}）问",
                    "solution_quote": s_quote,
                    "solution_location": (
                        f"参考解答第{item['page_solution']}页，"
                        f"项目文本第{profile['solution_lines'][0]}—"
                        f"{profile['solution_lines'][1]}行"
                    ),
                    "necessary_cognitive_activity": activity,
                    "present_label": present,
                    "level": level,
                    "decision_reason": reason,
                    "adjacent_level_exclusion": exclusion,
                    "confidence": "中",
                    "coder_id": "AI-MENTOR-PRECODE",
                    "coding_date": "2026-07-29",
                    "review_status": "AI辅助导师视角试编码；待作者实质复核",
                    "notes": "不携带V2标签；不得直接并入正式V3唯一编码表",
                }
            )

    fieldnames = list(rows[0])
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)
    print(f"rows={len(rows)}")
    print(OUTPUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
