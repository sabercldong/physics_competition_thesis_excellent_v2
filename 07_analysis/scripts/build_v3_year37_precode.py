#!/usr/bin/env python3
"""Build the year-37 V3 mentor-perspective precode batch."""

from __future__ import annotations

import csv

from build_v3_year35_precode import (
    DIMENSIONS,
    LEVEL_EXCLUSION,
    ROOT,
    absent_fields,
    line_quote,
    read_rows,
    sha256,
    source_path,
)


INDEX = ROOT / "03_corpus/item_index.csv"
OUTPUT = ROOT / "07_analysis/data/第37届科学思维V3导师视角试编码.csv"


PROFILES = {
    "CPHO37-Q01-1": {
        "output": "推导辅助气室未连通时空气弹簧的等温和绝热刚度",
        "question_lines": (36, 41),
        "solution_lines": (51, 71),
        "模型建构": ("L3", "整合活塞位移、气体体积变化和等温或绝热状态方程建立空气弹簧模型"),
        "科学推理": ("L3", "对两种状态方程作微分并比较过程指数对刚度的影响"),
    },
    "CPHO37-Q01-2": {
        "output": "推导辅助气室连通后低频和高频条件下的空气弹簧刚度",
        "question_lines": (42, 43),
        "solution_lines": (85, 93),
        "模型建构": ("L3", "把主气室、辅助气室和连接管中的快慢气体交换整合为分频模型"),
        "科学推理": ("L3", "分别约束低频等温连通和高频绝热隔离状态并推出刚度关系"),
    },
    "CPHO37-Q02-1": {
        "output": "求圆柱受水平冲量后达到纯滚动所需时间",
        "question_lines": (32, 32),
        "solution_lines": (43, 64),
        "模型建构": ("L3", "整合冲量引起的平动转动初态、滑动摩擦和纯滚动终止条件"),
        "科学推理": ("L3", "联立线动量、角动量、摩擦冲量和滚动约束确定转变时刻"),
    },
    "CPHO37-Q02-2": {
        "output": "求纯滚动后圆柱上一点的位置、速度和加速度",
        "question_lines": (33, 34),
        "solution_lines": (79, 94),
        "模型建构": ("L3", "把圆柱质心平动与绕质心转动整合为质点的平面运动模型"),
        "科学推理": ("L3", "由滚动相位、坐标变换及逐次求导得到运动学量"),
    },
    "CPHO37-Q03-1": {
        "output": "求负微分电阻RLC电路电流解中的待定指数",
        "question_lines": (35, 39),
        "solution_lines": (55, 72),
        "模型建构": ("L3", "把负微分电阻、电感、电容和电阻组织为二阶动态电路模型"),
        "科学推理": ("L3", "由回路方程、初始条件和特征根结构确定指数参数"),
    },
    "CPHO37-Q03-2": {
        "output": "确定电路形成无阻尼振荡的条件并求电流和频率",
        "question_lines": (41, 42),
        "solution_lines": (92, 100),
        "科学推理": ("L2", "调用前问特征方程并令有效阻尼为零以求振荡条件与频率"),
    },
    "CPHO37-Q03-3": {
        "output": "说明电路发生阻尼振荡的条件并求电流和频率",
        "question_lines": (43, 44),
        "solution_lines": (101, 118),
        "科学推理": ("L3", "由特征根判别、初始条件和阻尼频率关系推出完整时域解"),
        "科学论证": ("L1", "用特征根判别式支持电路在给定参数范围内发生阻尼振荡的主张"),
    },
    "CPHO37-Q03-4": {
        "output": "求负微分电阻工作范围内的最大平均功率和信号源电压",
        "question_lines": (46, 49),
        "solution_lines": (119, 132),
        "模型建构": ("L3", "整合直流偏置、交流振幅、器件工作区和负载功率建立约束优化模型"),
        "科学推理": ("L3", "由电压范围约束交流振幅并对平均功率取极值"),
    },
    "CPHO37-Q04-1": {
        "output": "求质子同步加速器达到给定能量所需的最小磁感应强度",
        "question_lines": (31, 34),
        "solution_lines": (50, 65),
        "模型建构": ("L2", "建立相对论动量、洛伦兹力和加速器轨道半径的对应模型"),
        "科学推理": ("L2", "由总能量求动量并代入圆周运动关系确定磁场下限"),
    },
    "CPHO37-Q04-2": {
        "output": "求产生质子反质子对的阈值并判断现有加速器能否实现",
        "question_lines": (36, 40),
        "solution_lines": (94, 111),
        "模型建构": ("L3", "整合实验室系碰撞与质心系阈值状态的相对论能量动量模型"),
        "科学推理": ("L3", "利用四动量不变量求阈值并与加速器最大能量比较"),
        "科学论证": ("L1", "以阈值能量和设备能量的定量比较支持可行性判断"),
    },
    "CPHO37-Q05-1": {
        "output": "求飞船发出信号的传播时间及追上另一飞船的时刻",
        "question_lines": (34, 37),
        "solution_lines": (48, 65),
        "模型建构": ("L3", "把两飞船世界线、光信号传播和参考系变换整合为时空模型"),
        "科学推理": ("L3", "联立相对运动、光速不变和洛伦兹变换求多个事件时刻"),
    },
    "CPHO37-Q05-2": {
        "output": "求货物在不同参考系中的发射速度方向和接收时刻",
        "question_lines": (38, 41),
        "solution_lines": (69, 101),
        "模型建构": ("L3", "整合二维速度分解、相对论速度变换和货物接收事件几何"),
        "科学推理": ("L3", "连续变换速度分量并以世界线交点约束接收时刻"),
    },
    "CPHO37-Q06-1": {
        "output": "求光纤端面允许的最大入射角",
        "question_lines": (20, 23),
        "solution_lines": (42, 58),
        "模型建构": ("L2", "建立端面折射与芯包层界面全反射的光线模型"),
        "科学推理": ("L2", "联立斯涅耳定律和临界角条件求最大入射角"),
    },
    "CPHO37-Q06-2": {
        "output": "求旋转光纤环的传播时间差和相位差并判断其折射率依赖性",
        "question_lines": (23, 27),
        "solution_lines": (59, 88),
        "模型建构": ("L3", "整合旋转环路、顺逆向传播路径和介质中光速建立Sagnac模型"),
        "科学推理": ("L3", "分别求顺逆向时间并消去折射率得到相位差"),
        "科学论证": ("L1", "以相位差表达式中折射率消去的结果支持其与折射率无关的判断"),
    },
    "CPHO37-Q06-3": {
        "output": "推导谐振式光纤陀螺仪角速度与谐振频率差的关系",
        "question_lines": (30, 35),
        "solution_lines": (89, 107),
        "模型建构": ("L3", "把顺逆向环形谐振条件与旋转引起的传播时间差整合为测量模型"),
        "科学推理": ("L3", "由相位闭合条件和频率差近似推出角速度表达式"),
    },
    "CPHO37-Q07-1": {
        "output": "由量纲分析导出双黑洞引力波辐射功率表达式",
        "question_lines": (23, 26),
        "solution_lines": (38, 51),
        "模型建构": ("L3", "选取转动惯量、角速度和光速并与引力常量构成辐射功率模型"),
        "科学推理": ("L3", "联立质量、长度和时间量纲方程确定各物理量指数"),
    },
    "CPHO37-Q07-2": {
        "output": "求双黑洞从初态旋转一周所需时间",
        "question_lines": (28, 29),
        "solution_lines": (52, 94),
        "模型建构": ("L3", "整合圆轨道引力、引力波功率和轨道能量耗散建立旋近模型"),
        "科学推理": ("L3", "由能量变化方程求距离演化并积分角速度得到一周时间"),
    },
    "CPHO37-Q07-3": {
        "output": "求双黑洞间距减半时已经转过的角度",
        "question_lines": (31, 32),
        "solution_lines": (95, 101),
        "模型建构": ("L2", "把前问距离演化与角速度关系组合为角位移模型"),
        "科学推理": ("L3", "消去时间并按距离边界积分得到累计转角"),
    },
    "CPHO37-Q08-1": {
        "output": "求电光晶体引起的相位、光强变化和半波电压",
        "question_lines": (45, 51),
        "solution_lines": (72, 95),
        "模型建构": ("L3", "把正交偏振分解、双折射相位积累和检偏器投影整合为电光调制模型"),
        "科学推理": ("L3", "由折射率变化推导相位差、光强和半波条件"),
    },
    "CPHO37-Q08-2": {
        "output": "求加入四分之一波片后的透过率关系并说明其作用",
        "question_lines": (52, 57),
        "solution_lines": (96, 117),
        "模型建构": ("L3", "在电光调制模型中加入四分之一波片的固定相移和小信号近似"),
        "科学推理": ("L3", "比较加片前后的传递函数并推出线性化关系"),
        "科学论证": ("L2", "以加片前后的透过率函数比较支持波片实现线性工作区的解释"),
    },
    "CPHO37-Q08-3": {
        "output": "证明高频条件下电光晶体实际电压远小于信号电压",
        "question_lines": (58, 62),
        "solution_lines": (118, 128),
        "模型建构": ("L2", "把电光晶体等效电容与线路电阻表示为交流分压模型"),
        "科学推理": ("L2", "由复阻抗分压和高频极限推出晶体端电压"),
        "科学论证": ("L1", "用高频渐近关系支持调制效率极低的结论"),
    },
    "CPHO37-Q08-4": {
        "output": "证明并联谐振补偿后晶体端电压可等于信号电压",
        "question_lines": (63, 64),
        "solution_lines": (129, 139),
        "模型建构": ("L3", "整合电容、电感、分流电阻和源电阻建立并联谐振补偿模型"),
        "科学推理": ("L3", "求等效阻抗并在谐振和电阻尺度条件下推出端电压关系"),
        "科学论证": ("L2", "以补偿前后阻抗与端电压的比较支持效率提高的结论"),
    },
}


def main() -> None:
    index_rows = [
        row for row in read_rows(INDEX) if row["competition_no"] == "37"
    ]
    if len(index_rows) != 22 or set(PROFILES) != {row["item_id"] for row in index_rows}:
        raise ValueError("第37届分析单元与人工配置不一致")

    rows: list[dict[str, str]] = []
    for item in index_rows:
        item_id = item["item_id"]
        profile = PROFILES[item_id]
        source = source_path(item_id)
        q_quote = line_quote(source, profile["question_lines"])
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
                    "question_location": (
                        f"题面第{item['page_paper']}页，第（{item['subquestion_no']}）问；"
                        f"项目文本第{profile['question_lines'][0]}—"
                        f"{profile['question_lines'][1]}行"
                    ),
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

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(rows[0]),
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)
    print(f"rows={len(rows)}")
    print(OUTPUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
