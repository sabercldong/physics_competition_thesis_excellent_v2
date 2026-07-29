#!/usr/bin/env python3
"""Build the year-38 V3 mentor-perspective precode batch."""

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
OUTPUT = ROOT / "07_analysis/data/第38届科学思维V3导师视角试编码.csv"


PROFILES = {
    "CPHO38-Q01-1": {
        "output": "由等光程条件求平凸透镜凸面的极坐标方程和直角坐标标准式",
        "question_lines": (14, 16),
        "solution_lines": (47, 88),
        "模型建构": ("L3", "整合旋转对称、等光程和极坐标到直角坐标变换建立非球面透镜模型"),
        "科学推理": ("L3", "由光程相等关系导出曲面方程并化为旋转双曲面标准式"),
    },
    "CPHO38-Q01-2_i": {
        "output": "求插入平凹透镜凹面的极坐标方程和直角坐标标准式",
        "question_lines": (17, 21),
        "solution_lines": (122, 155),
        "模型建构": ("L3", "整合原平凸透镜光路、虚焦点等光程和平凹透镜折射建立复合光学模型"),
        "科学推理": ("L3", "协调两透镜光程关系并将凹面方程转换为旋转双曲面标准式"),
    },
    "CPHO38-Q01-2_ii": {
        "output": "求入射与出射平行圆光束的横截面半径比",
        "question_lines": (17, 23),
        "solution_lines": (159, 170),
        "模型建构": ("L2", "把两透镜边缘光线半径和最大倾角表示为光束口径映射"),
        "科学推理": ("L2", "调用两曲面极坐标关系并消去公共角度求半径比"),
    },
    "CPHO38-Q02-1": {
        "output": "求过程A中封闭气体对外所做的功",
        "question_lines": (33, 34),
        "solution_lines": (68, 89),
        "模型建构": ("L2", "把水银柱缓慢上升表示为恒压理想气体膨胀过程"),
        "科学推理": ("L2", "由初末体积、压强和等压功关系求气体做功"),
    },
    "CPHO38-Q02-2": {
        "output": "判断过程B能否缓慢稳定发生并求气体吸热量",
        "question_lines": (35, 37),
        "solution_source": "CPHO38-Q03",
        "solution_lines": (44, 83),
        "模型建构": ("L3", "整合变长水银柱、理想气体状态和热力学第一定律建立全过程模型"),
        "科学推理": ("L3", "由状态方程检验温度—水银高度单调性并计算内能增量和外功"),
        "科学论证": ("L1", "用状态方程解在全过程连续单调存在支持缓慢稳定发生的判断"),
    },
    "CPHO38-Q03-1": {
        "output": "求超球第一次碰撞后的平动速度和转动角速度",
        "question_lines": (18, 18),
        "solution_lines": (92, 147),
        "模型建构": ("L3", "整合碰撞冲量、角冲量、弹性形变和接触点无滑动建立刚体碰撞模型"),
        "科学推理": ("L3", "联立动量、角动量、能量和接触点速度反向关系求碰后状态"),
    },
    "CPHO38-Q03-2": {
        "output": "求超球第二次碰撞后的平动速度和转动角速度",
        "question_lines": (19, 19),
        "solution_source": "CPHO38-Q04",
        "solution_lines": (42, 53),
        "科学推理": ("L2", "调用第一次碰撞得到的更新关系并处理上板碰撞时力矩符号反转"),
    },
    "CPHO38-Q03-3": {
        "output": "求超球第三次碰撞后的平动速度和转动角速度",
        "question_lines": (20, 24),
        "solution_source": "CPHO38-Q04",
        "solution_lines": (55, 71),
        "科学推理": ("L2", "再次调用碰撞更新关系并代入第二次碰撞状态完成递推"),
    },
    "CPHO38-Q04-1": {
        "output": "求远距离两永磁针之间的相互作用势能",
        "question_lines": (19, 19),
        "solution_lines": (81, 131),
        "模型建构": ("L3", "把永磁针等效为小电流环并由远场磁场建立磁偶极相互作用模型"),
        "科学推理": ("L3", "对电流元磁场作远场展开和环路积分后代入磁矩势能关系"),
    },
    "CPHO38-Q04-2": {
        "output": "确定固定位置时永磁针的稳定平衡方向",
        "question_lines": (20, 21),
        "solution_lines": (132, 161),
        "模型建构": ("L2", "把磁相互作用势能表示为磁矩方向角的函数"),
        "科学推理": ("L2", "由力矩为零和势能二阶变化判定稳定平衡角"),
    },
    "CPHO38-Q04-3": {
        "output": "求永磁针的竖直受力平衡位置并判断其稳定性",
        "question_lines": (22, 23),
        "solution_source": "CPHO38-Q05",
        "solution_lines": (59, 74),
        "模型建构": ("L2", "把磁相互作用势能与重力势能组合为竖直位置模型"),
        "科学推理": ("L2", "由一阶导数求平衡位置并由二阶导数判定稳定性"),
        "科学论证": ("L1", "以势能二阶导数为负支持该受力平衡位置不稳定的结论"),
    },
    "CPHO38-Q05-1": {
        "output": "求准直后钾原子的方均根速率",
        "question_lines": (24, 24),
        "solution_lines": (85, 97),
        "模型建构": ("L1", "把单自由度原子热运动映射为能量均分模型"),
        "科学推理": ("L1", "调用单自由度能量均分关系直接求方均根速率"),
    },
    "CPHO38-Q05-2": {
        "output": "求激光共振散射造成的减速度和停止距离",
        "question_lines": (25, 27),
        "solution_lines": (98, 125),
        "模型建构": ("L3", "把单光子动量、散射速率、平均辐射力和匀减速运动整合为减速模型"),
        "科学推理": ("L3", "由微观动量传递求宏观加速度并进一步求停止距离"),
    },
    "CPHO38-Q05-3": {
        "output": "求运动原子保持共振所需的激光频率失谐量",
        "question_lines": (28, 29),
        "solution_lines": (126, 155),
        "模型建构": ("L2", "建立原子参考系中的相对论多普勒频移与跃迁共振条件"),
        "科学推理": ("L2", "作低速近似并由共振等式推出频率失谐量"),
    },
    "CPHO38-Q05-4": {
        "output": "求使原子沿减速管始终共振的磁场分布",
        "question_lines": (30, 36),
        "solution_source": "CPHO38-Q06",
        "solution_lines": (39, 60),
        "模型建构": ("L3", "整合速度—位置关系、多普勒失谐和塞曼频移建立空间补偿模型"),
        "科学推理": ("L3", "联立三种关系并施加入口边界条件推出磁场函数及取值范围"),
    },
    "CPHO38-Q06-1": {
        "output": "求同轴带电圆筒系统的电场分布",
        "question_lines": (19, 19),
        "solution_lines": (71, 81),
        "模型建构": ("L2", "利用柱对称把同轴圆筒表示为分区域径向电场模型"),
        "科学推理": ("L2", "按高斯面包围电荷情况分区应用高斯定理"),
    },
    "CPHO38-Q06-2": {
        "output": "求同向旋转带电圆筒系统的磁场分布",
        "question_lines": (21, 21),
        "solution_lines": (82, 92),
        "模型建构": ("L2", "把旋转面电荷等效为方向相反的圆柱面电流并分区表示磁场"),
        "科学推理": ("L2", "由安培环路定理叠加内外圆筒贡献得到分段磁场"),
    },
    "CPHO38-Q06-3": {
        "output": "求点电荷能够到达外圆筒的角速度条件",
        "question_lines": (23, 25),
        "solution_lines": (93, 134),
        "模型建构": ("L3", "整合径向电场做功、轴向磁场角冲量和径向到达条件建立带电粒子模型"),
        "科学推理": ("L3", "联立角动量演化、动能定理和径向动能非负条件推出角速度上限"),
    },
    "CPHO38-Q06-4": {
        "output": "求外筒加速旋转时内筒角速度、外力矩冲量和总机械角动量",
        "question_lines": (26, 30),
        "solution_source": "CPHO38-Q07",
        "solution_lines": (54, 87),
        "模型建构": ("L3", "把时变磁场、感应电场、双筒转动和外力矩整合为角动量传递模型"),
        "科学推理": ("L3", "连续应用电磁感应、转动动力学和角动量定理求三个关联输出"),
    },
    "CPHO38-Q07-1": {
        "output": "求斜坡加速时前后轮正压力和前轮不离地的安全加速度",
        "question_lines": (21, 23),
        "solution_lines": (99, 130),
        "模型建构": ("L3", "建立车身质心平动、法向平衡和绕质心力矩平衡的车辆模型"),
        "科学推理": ("L3", "联立力与力矩方程并施加前轮正压力为零的临界条件"),
    },
    "CPHO38-Q07-2": {
        "output": "求后轮驱动力矩作用下汽车的加速度",
        "question_lines": (25, 27),
        "solution_lines": (132, 158),
        "模型建构": ("L3", "整合车身平动、前后轮转动和无滑动约束建立动力学模型"),
        "科学推理": ("L3", "联立轮轴力矩、轮地摩擦和整车质心运动方程求加速度"),
    },
    "CPHO38-Q07-3": {
        "output": "求水平与坡面最大加速度及保持无滑动所需摩擦系数",
        "question_lines": (29, 35),
        "solution_source": "CPHO38-Q08",
        "solution_lines": (59, 90),
        "模型建构": ("L3", "在车辆动力学模型中加入传动比、坡度和轮地静摩擦约束"),
        "科学推理": ("L3", "分别代入两种坡度并比较驱动力与正压力求摩擦系数下限"),
    },
    "CPHO38-Q08-1": {
        "output": "求永磁直流电机的力矩—转速关系及最大力矩、转速和功率",
        "question_lines": (19, 23),
        "solution_lines": (101, 144),
        "模型建构": ("L3", "整合线圈受力矩、反电动势和含内阻供电电路建立电机模型"),
        "科学推理": ("L3", "由电流随转速变化推出力矩函数并完成多个极值和截距计算"),
    },
    "CPHO38-Q08-2": {
        "output": "求电动汽车从静止加速时的车速—时间关系",
        "question_lines": (27, 32),
        "solution_lines": (145, 196),
        "模型建构": ("L3", "把电机力矩—转速特性、变速器和整车加速度整合为速度微分模型"),
        "科学推理": ("L3", "建立并求解一阶动力学方程得到车速指数响应"),
    },
    "CPHO38-Q08-3": {
        "output": "求加速时间、电池耗能和电池能量转化效率",
        "question_lines": (33, 37),
        "solution_lines": (199, 246),
        "模型建构": ("L3", "整合速度响应、电池瞬时功率和车辆平动转动机械能建立能量模型"),
        "科学推理": ("L3", "由速度反解时间、积分电功率并与机械能增量比较求效率"),
    },
}


def main() -> None:
    index_rows = [
        row for row in read_rows(INDEX) if row["competition_no"] == "38"
    ]
    if len(index_rows) != 25 or set(PROFILES) != {row["item_id"] for row in index_rows}:
        raise ValueError("第38届分析单元与人工配置不一致")

    rows: list[dict[str, str]] = []
    for item in index_rows:
        item_id = item["item_id"]
        profile = PROFILES[item_id]
        source = source_path(item_id)
        solution_source = source_path(profile.get("solution_source", item_id))
        q_quote = line_quote(source, profile["question_lines"])
        s_quote = line_quote(solution_source, profile["solution_lines"])
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
                    "solution_text_path": str(solution_source.relative_to(ROOT)),
                    "solution_text_sha256": sha256(solution_source),
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
                        f"参考解答第{item['page_solution']}页；"
                        f"{solution_source.relative_to(ROOT)}第"
                        f"{profile['solution_lines'][0]}—"
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
                    "notes": "不携带V2标签；跨页解答按独立路径和哈希绑定；不得直接并入正式V3唯一编码表",
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
