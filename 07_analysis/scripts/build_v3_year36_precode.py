#!/usr/bin/env python3
"""Build the year-36 V3 mentor-perspective precode batch."""

from __future__ import annotations

import csv
from pathlib import Path

from build_v3_year35_precode import (
    DIMENSIONS,
    LEVEL_EXCLUSION,
    ROOT,
    absent_fields,
    line_quote,
    question_quote,
    read_rows,
    sha256,
    source_path,
)


INDEX = ROOT / "03_corpus/item_index.csv"
OUTPUT = ROOT / "07_analysis/data/第36届科学思维V3导师视角试编码.csv"


PROFILES = {
    "CPHO36-Q01-1": {
        "output": "确定兼顾盛水量与稳定性的最佳茶水高度",
        "solution_lines": (64, 73),
        "模型建构": ("L3", "整合杯体、茶水质心和支承边界建立倾覆临界优化模型"),
        "科学推理": ("L3", "由组合质心、稳定条件和容量目标确定最佳高度"),
    },
    "CPHO36-Q01-2": {
        "output": "求杯子移至凳边后各凳脚支持力",
        "solution_lines": (144, 153),
        "模型建构": ("L3", "建立偏置载荷下杯—凳整体及三脚支承的空间平衡模型"),
        "科学推理": ("L3", "联立竖直力平衡和多个力矩平衡求支承力分配"),
    },
    "CPHO36-Q02-1": {
        "output": "求把手释放后碰地前的角速度",
        "solution_lines": (63, 72),
        "模型建构": ("L3", "把车体与车轮组织为受约束刚体转动系统并计算总转动惯量"),
        "科学推理": ("L3", "协调几何质心、转动惯量和机械能守恒求碰前状态"),
    },
    "CPHO36-Q02-2": {
        "output": "求碰撞解锁后平板车最终运动状态及能量损失",
        "solution_lines": (119, 129),
        "模型建构": ("L3", "整合瞬时碰撞、车轮锁定、滑动摩擦和最终纯滚动的分阶段模型"),
        "科学推理": ("L3", "串联角动量、冲量、摩擦耗散和滚动约束得到终态"),
    },
    "CPHO36-Q03-1": {
        "output": "求弹丸加速过程中所受磁场力",
        "solution_lines": (72, 81),
        "模型建构": ("L2", "把两根半无限长导轨的磁场和弹丸电流元组织为安培力模型"),
        "科学推理": ("L2", "积分弹丸各电流元所受磁力并完成导轨贡献叠加"),
    },
    "CPHO36-Q03-2": {
        "output": "求弹丸出射速度",
        "solution_lines": (100, 109),
        "模型建构": ("L2", "把恒定磁场力映射为斜轨上的匀加速动力学模型"),
        "科学推理": ("L2", "联立牛顿第二定律和运动学关系求出射速度"),
    },
    "CPHO36-Q03-3": {
        "output": "求加速任意时刻及出射时的恒流源电压",
        "solution_lines": (151, 160),
        "模型建构": ("L3", "整合电阻压降、运动电动势和弹丸运动状态的时变电路模型"),
        "科学推理": ("L3", "由电路功率、电磁感应和位移—时间关系推出电压函数"),
    },
    "CPHO36-Q03-4": {
        "output": "求整个加速过程中恒流源所做的功",
        "solution_lines": (178, 187),
        "模型建构": ("L2", "把源端电压和恒流表示为全过程输入功率模型"),
        "科学推理": ("L3", "对时变电压积分并协调电阻热和机械能去向"),
    },
    "CPHO36-Q03-5": {
        "output": "求理想条件下弹丸动能与电源做功之比",
        "solution_lines": (223, 232),
        "模型建构": ("L2", "建立忽略电阻时电磁系统机械能与磁场能的分配表示"),
        "科学推理": ("L2", "比较出射动能和前问电源功得到能量比例"),
    },
    "CPHO36-Q04-1": {
        "output": "求标准状态空气密度和声速",
        "solution_lines": (97, 106),
        "模型建构": ("L1", "把空气映射为理想气体并采用绝热体积弹性模型"),
        "科学推理": ("L2", "联立状态方程、绝热关系和声速关系求空气参数"),
    },
    "CPHO36-Q04-2": {
        "output": "推导亥姆霍兹共振器的吸声频率",
        "solution_lines": (141, 151),
        "模型建构": ("L3", "把微孔空气柱和腔内压缩气体整合为质量—弹簧振子"),
        "科学推理": ("L3", "由空气柱惯性、腔体压强回复力和简谐振动关系推出频率"),
    },
    "CPHO36-Q04-3": {
        "output": "求吸收两种给定频率所需微孔面积比",
        "solution_lines": (186, 197),
        "科学推理": ("L1", "调用前问频率与面积的单一比例关系求面积比"),
    },
    "CPHO36-Q05-1": {
        "output": "求光纤端面允许的最大入射角",
        "solution_lines": (64, 73),
        "模型建构": ("L2", "建立端面折射与芯—包层全反射的光线几何模型"),
        "科学推理": ("L2", "联立两次折射条件和临界角关系求数值孔径"),
    },
    "CPHO36-Q05-2": {
        "output": "确定微球透镜使平行光聚焦于光纤端面的条件",
        "solution_lines": (82, 91),
        "模型建构": ("L3", "整合微球前后球面折射和光纤端面位置的复合成像模型"),
        "科学推理": ("L3", "连续应用球面折射关系并约束最终像点位置"),
    },
    "CPHO36-Q05-3": {
        "output": "求全部耦合光可长距离传输时的最大光束直径",
        "solution_lines": (132, 141),
        "模型建构": ("L3", "整合微球聚焦孔径与光纤最大接收角的耦合模型"),
        "科学推理": ("L3", "由边缘光线几何、焦距和全反射约束求极限直径"),
    },
    "CPHO36-Q06-1": {
        "output": "求运动π介子衰变产生μ子的最大和最小速率",
        "solution_lines": (57, 67),
        "模型建构": ("L3", "整合质心系二体衰变和实验室系相对论速度变换"),
        "科学推理": ("L3", "由能量动量守恒确定质心系速率并变换两个极端方向"),
    },
    "CPHO36-Q06-2": {
        "output": "估算高空μ子到达地面的存活概率",
        "solution_lines": (205, 215),
        "模型建构": ("L2", "建立实验室飞行时间、时间膨胀和指数衰变模型"),
        "科学推理": ("L3", "协调相对论寿命修正、传播距离和半衰期概率关系"),
    },
    "CPHO36-Q07-1": {
        "output": "估算圆柱雷电云电势差、电荷量和总电能",
        "solution_lines": (145, 161),
        "模型建构": ("L2", "把均匀圆柱雷电云近似为平行板电容器"),
        "科学推理": ("L2", "联立电场、电容、电势差和储能关系完成估算"),
    },
    "CPHO36-Q07-2": {
        "output": "估算雷电云下方的地表电场",
        "solution_lines": (163, 180),
        "模型建构": ("L3", "把导体地面、上下电荷层和镜像电荷整合为空间场模型"),
        "科学推理": ("L3", "叠加两层电荷及其镜像贡献并判断场方向"),
    },
    "CPHO36-Q07-3": {
        "output": "估算闪电通道直径并推导径向电荷密度",
        "solution_lines": (250, 268),
        "模型建构": ("L3", "把通道表示为长圆柱并用恒击穿场约束内部电荷分布"),
        "科学推理": ("L3", "由线电荷、高斯定理和径向积分微分得到尺寸与密度"),
    },
    "CPHO36-Q07-4": {
        "output": "画出电离层光环扩展过程并求给定半径时的径向速度",
        "solution_lines": (292, 311),
        "模型建构": ("L3", "把球面电磁波前与电离层平面的交线建立为传播几何模型"),
        "科学推理": ("L3", "由波前位移和交线几何推出光环表观径向速度"),
    },
    "CPHO36-Q07-5": {
        "output": "求12千米高空悬浮氦气球的体积",
        "solution_lines": (373, 386),
        "模型建构": ("L3", "整合浮力平衡、变温大气静力和理想气体状态模型"),
        "科学推理": ("L3", "由温度廓线推导压强密度并代入悬浮条件"),
    },
}


def main() -> None:
    index_rows = [
        row for row in read_rows(INDEX) if row["competition_no"] == "36"
    ]
    if len(index_rows) != 22 or set(PROFILES) != {row["item_id"] for row in index_rows}:
        raise ValueError("第36届分析单元与人工配置不一致")

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
