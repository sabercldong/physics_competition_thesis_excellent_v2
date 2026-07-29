#!/usr/bin/env python3
"""Build the year-41 V3 mentor-perspective precode batch."""

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
OUTPUT = ROOT / "07_analysis/data/第41届科学思维V3导师视角试编码.csv"


PROFILES = {
    "CPHO41-Q01-1_1": {
        "output": "求高楼—摆锤阻尼器系统受迫稳态振动的振幅",
        "question_lines": (17, 28),
        "solution_lines": (67, 116),
        "模型建构": ("L3", "整合大楼弹簧振子、随楼运动的单摆、小角近似和同频稳态响应"),
        "科学推理": ("L3", "联立摆锤与大楼动力学方程并用稳态试探解消元求振幅"),
    },
    "CPHO41-Q01-1_2": {
        "output": "确定无阻尼器时的共振频率及阻尼器最优调谐条件",
        "question_lines": (30, 31),
        "solution_lines": (117, 139),
        "模型建构": ("L2", "把前问振幅函数约化为无阻尼和加入调谐摆两种参数模型"),
        "科学推理": ("L3", "比较振幅分母的共振条件并对摆长和摆锤质量进行参数优化"),
    },
    "CPHO41-Q01-2": {
        "output": "求近共振风频下无阻尼振幅及达到百分之一振幅所需质量比",
        "question_lines": (32, 34),
        "solution_lines": (142, 152),
        "科学推理": ("L2", "把给定频率与前问调谐摆长代入振幅关系并反求质量比"),
    },
    "CPHO41-Q01-3": {
        "output": "建立含油阻尼的非线性运动方程并说明阻尼不可缺少的原因",
        "question_lines": (35, 42),
        "solution_lines": (153, 181),
        "模型建构": ("L3", "把摆锤相对油池速度、黏滞阻力和大楼—摆锤耦合纳入非线性动力学"),
        "科学推理": ("L2", "分解相对速度与阻尼力并分析共振受抑和停风后能量衰减"),
        "科学论证": ("L2", "以共振振幅受抑和机械能持续耗散两条理由支持阻尼不可缺少的结论"),
    },
    "CPHO41-Q02-1": {
        "output": "求同质台球弹性碰撞后的方向、Q球速度和角速度",
        "question_lines": (30, 32),
        "solution_lines": (66, 115),
        "模型建构": ("L3", "建立无摩擦瞬时碰撞的二维动量、平动能量和转动状态守恒模型"),
        "科学推理": ("L3", "在沿T球方向的坐标系中联立守恒关系并变换回桌面坐标"),
    },
    "CPHO41-Q02-2_1": {
        "output": "求碰撞瞬间Q球接触点速度的两个分量",
        "question_lines": (33, 39),
        "solution_lines": (116, 126),
        "模型建构": ("L2", "把Q球平动和绕质心转动组合为接触点速度模型"),
        "科学推理": ("L2", "用刚体速度合成并代入碰后质心速度与角速度"),
    },
    "CPHO41-Q02-2_2": {
        "output": "求Q球由滑动过渡到纯滚所需时间",
        "question_lines": (33, 40),
        "solution_lines": (127, 163),
        "模型建构": ("L3", "整合滑动摩擦、质心冲量、角冲量和接触点匀减速条件"),
        "科学推理": ("L3", "联立平动转动方程推出接触点减速度并由初速求过渡时间"),
    },
    "CPHO41-Q02-2_3": {
        "output": "求碰撞后至纯滚前Q球质心的参数轨迹",
        "question_lines": (33, 41),
        "solution_lines": (164, 195),
        "模型建构": ("L2", "把恒定接触点速度方向映射为质心的二维恒加速度运动"),
        "科学推理": ("L3", "由摩擦方向和碰后初速度分别积分得到两个坐标随时间关系"),
    },
    "CPHO41-Q02-2_4": {
        "output": "确定纯滚后轨迹形状、最终速度和方向角",
        "question_lines": (33, 43),
        "solution_lines": (196, 214),
        "模型建构": ("L2", "以接触点零相对速度和摩擦消失重构纯滚后的匀速阶段"),
        "科学推理": ("L3", "组合滑动阶段冲量与初始平动转动状态求最终速度分量和方向"),
    },
    "CPHO41-Q02-3": {
        "output": "求球杆冲量使Q球立即纯滚时的击球高度",
        "question_lines": (45, 49),
        "solution_lines": (215, 239),
        "模型建构": ("L2", "建立偏心冲量引起的质心动量、角动量与纯滚约束"),
        "科学推理": ("L2", "联立冲量和冲量矩定理并代入球的转动惯量求高度"),
    },
    "CPHO41-Q02-4_1": {
        "output": "求满足开球纯滚条件时碰后至再纯滚前的质心轨迹",
        "question_lines": (51, 55),
        "solution_lines": (240, 259),
        "科学推理": ("L2", "把第3问给出的初始平动转动关系代入第2问既有轨迹方程"),
    },
    "CPHO41-Q02-4_2": {
        "output": "求30度经验规则情境下Q球最终方向角的正切",
        "question_lines": (51, 56),
        "solution_lines": (260, 265),
        "科学推理": ("L1", "把开球纯滚条件直接代入前问最终方向公式"),
    },
    "CPHO41-Q02-4_3": {
        "output": "求最终方向角的极大值并检验30度经验规则的邻域稳定性",
        "question_lines": (51, 58),
        "solution_lines": (266, 293),
        "科学推理": ("L3", "对既有方向函数求极值并计算极值点附近多组角度"),
        "科学论证": ("L2", "用极大值及正负五度、十度的数值比较支持经验规则在一定范围内成立"),
    },
    "CPHO41-Q03-1": {
        "output": "求使油水混合物表面张力最小的注水温度",
        "question_lines": (32, 45),
        "solution_lines": (59, 106),
        "模型建构": ("L3", "整合等体压强—温度关系、表面张力函数和两种液体绝热混合热平衡"),
        "科学推理": ("L3", "先求表面张力极小的末温再由热量守恒反求注水温度"),
        "科学论证": ("L2", "用函数极值和混合热平衡两段定量证据支持所给注水温度"),
    },
    "CPHO41-Q03-2": {
        "output": "由粒子近邻和汽化热模型导出液体表面张力系数",
        "question_lines": (47, 50),
        "solution_lines": (107, 179),
        "模型建构": ("L3", "把表面与体内近邻键差、表面功、汽化热和粒子尺度组织为微观模型"),
        "科学推理": ("L3", "依次消去键能、粒子数面密度和平均间距得到宏观参数表达式"),
    },
    "CPHO41-Q04-1": {
        "output": "求质子断层扫描所需电子动能并检验极端相对论近似误差",
        "question_lines": (31, 35),
        "solution_lines": (51, 143),
        "模型建构": ("L3", "整合空间分辨率、不确定关系和相对论能量—动量关系建立探测尺度模型"),
        "科学推理": ("L3", "由层析分辨率求最小动量并比较完整相对论与极端相对论能量"),
        "科学论证": ("L2", "用静止质量项的数量级和两种计算结果比较支持误差小于百分之一"),
    },
    "CPHO41-Q04-2": {
        "output": "求带电粒子散射系统总能量及位置不确定度等于间距时的质子速率",
        "question_lines": (37, 41),
        "solution_lines": (144, 215),
        "模型建构": ("L3", "整合非相对论动能、库仑势能、能量守恒和位置—动量不确定关系"),
        "科学推理": ("L3", "传播动量与位置不确定度并施加总能量不变和相对误差条件求速率"),
    },
    "CPHO41-Q05-1": {
        "output": "求Ioffe磁阱中心及邻域磁场的领头阶分布",
        "question_lines": (33, 39),
        "solution_lines": (63, 114),
        "模型建构": ("L3", "建立四根异向长直导线的坐标和磁场矢量叠加模型"),
        "科学推理": ("L3", "计算四线磁场分量并在中心邻域一致保留领头阶"),
    },
    "CPHO41-Q05-2": {
        "output": "证明微小电流环磁矩在外磁场中的势能表达式",
        "question_lines": (40, 43),
        "solution_lines": (115, 130),
        "模型建构": ("L2", "把原子磁矩表示为形状和电流不变的微小电流环"),
        "科学推理": ("L2", "对磁力矩沿转角做功积分并选定势能零点"),
        "科学论证": ("L1", "用磁力矩做功与势能变化关系支持势能等于负磁矩点乘磁场"),
    },
    "CPHO41-Q05-3": {
        "output": "求反平行磁矩原子在Ioffe磁阱邻域所受的力",
        "question_lines": (45, 46),
        "solution_lines": (131, 154),
        "模型建构": ("L2", "把反平行磁矩势能与前问径向线性磁场组合为约束势"),
        "科学推理": ("L2", "对势能取二维梯度并判断力的径向方向"),
    },
    "CPHO41-Q05-4": {
        "output": "求蒸发冷却前后原子团的粒子数、总势能和平均势能",
        "question_lines": (48, 54),
        "solution_lines": (155, 190),
        "模型建构": ("L3", "整合线性径向约束势、均匀面密度和圆柱区域收缩建立原子团模型"),
        "科学推理": ("L3", "对径向势能积分并按半径缩小五倍推导三个尺度关系"),
    },
    "CPHO41-Q06-1": {
        "output": "求双曲线引力轨道渐近角及其范围",
        "question_lines": (33, 40),
        "solution_lines": (69, 82),
        "模型建构": ("L2", "把给定双曲线轨道的无穷远边界表示为渐近线角度条件"),
        "科学推理": ("L2", "由半径为正和偏心率大于一推出角度极限与范围"),
    },
    "CPHO41-Q06-2": {
        "output": "导出引力轨道半通径和偏心率关于能量、角动量的关系",
        "question_lines": (42, 44),
        "solution_lines": (83, 147),
        "模型建构": ("L3", "协调极坐标能量、角动量和圆锥曲线轨道的两种微分表示"),
        "科学推理": ("L3", "消去时间参数并比较关于任意半径恒等式的系数求轨道参数"),
    },
    "CPHO41-Q06-3": {
        "output": "求陨石和掠日星光在牛顿引力模型中的偏折角",
        "question_lines": (46, 52),
        "solution_lines": (148, 193),
        "模型建构": ("L3", "把无穷远入射速度与瞄准距离映射为双曲线能量、角动量和渐近方向"),
        "科学推理": ("L3", "联立轨道参数并作弱偏折近似，再分别代入陨石和星光条件"),
    },
    "CPHO41-Q06-4": {
        "output": "用广义相对论等效折射率模型重算掠日星光偏折角",
        "question_lines": (54, 61),
        "solution_lines": (194, 287),
        "模型建构": ("L3", "把引力势等效折射率、费马变分方程和掠日边界组织为光线轨道模型"),
        "科学推理": ("L3", "由边界确定积分常量并将轨道微分式匹配为圆锥曲线求偏折角"),
    },
    "CPHO41-Q07-1": {
        "output": "由圆环波函数单值性求电子动量量子化取值",
        "question_lines": (53, 55),
        "solution_lines": (103, 120),
        "模型建构": ("L1", "把圆环周期边界条件施加到给定平面波状态"),
        "科学推理": ("L1", "由相位相差整数个周期直接求离散动量"),
    },
    "CPHO41-Q07-2": {
        "output": "求穿入磁通后单电子能量随磁通的关系",
        "question_lines": (57, 67),
        "solution_lines": (121, 133),
        "模型建构": ("L2", "把轴对称磁通、环向矢势和动量最小耦合组织为单粒子模型"),
        "科学推理": ("L2", "由磁通环路积分消去矢势并代入动能关系"),
    },
    "CPHO41-Q07-3_1": {
        "output": "在动量互异约束下确定奇数电子的最低能量占据并验证磁通周期",
        "question_lines": (71, 77),
        "solution_lines": (134, 168),
        "模型建构": ("L2", "把互异量子动量和奇数个连续占据态表示为最低能量构型"),
        "科学推理": ("L3", "重标磁通整数部分并比较平移一个磁通量子前后的占据区间"),
        "科学论证": ("L2", "用占据量子数集合在整数重标后不变支持奇数体系能量周期性"),
    },
    "CPHO41-Q07-3_2": {
        "output": "在总能量最小约束下确定偶数电子占据并完成磁通周期证明",
        "question_lines": (71, 77),
        "solution_lines": (169, 210),
        "模型建构": ("L3", "按磁通小数部分的符号建立偶数电子两类最低能量占据构型"),
        "科学推理": ("L3", "分段比较求和上下限并在磁通平移后重标整数指标"),
        "科学论证": ("L2", "用两个磁通区间的最低能量和式共同支持偶数体系及总体周期结论"),
    },
    "CPHO41-Q07-4": {
        "output": "求奇偶电子体系平均能量随磁通的分段关系并比较端点",
        "question_lines": (79, 81),
        "solution_lines": (212, 320),
        "模型建构": ("L3", "把奇数和偶数电子占据分别转换为磁通区间内的平均能量分段模型"),
        "科学推理": ("L3", "完成平方和、配方及周期端点代换并比较两类体系"),
        "科学论证": ("L2", "用奇偶两组显式能量函数支持零磁通与半磁通端点的相反大小关系"),
    },
    "CPHO41-Q07-5_1": {
        "output": "证明双环最低能量分配及正负动量电子成对存在",
        "question_lines": (83, 90),
        "solution_lines": (322, 340),
        "模型建构": ("L3", "整合双环粒子数分配、奇偶性、磁通端点和正负动量占据"),
        "科学推理": ("L3", "调用奇偶平均能量函数比较最小粒子数差并恢复占据对称性"),
        "科学论证": ("L3", "用两种奇偶分配和两类磁通极小值系统支持最低能量与配对结论"),
    },
    "CPHO41-Q07-5_2": {
        "output": "证明两种双环最低能量体系在大粒子数极限下能量比趋于一",
        "question_lines": (83, 94),
        "solution_lines": (341, 363),
        "模型建构": ("L2", "把两种双环奇偶分配映射为关于同一整数参数的平均能量"),
        "科学推理": ("L2", "分别求两种能量常数并计算粒子数趋于无穷时的比值极限"),
        "科学论证": ("L2", "用两种显式能量表达式及其极限支持能量比趋于一"),
    },
}


def main() -> None:
    index_rows = [
        row for row in read_rows(INDEX) if row["competition_no"] == "41"
    ]
    if len(index_rows) != 32 or set(PROFILES) != {row["item_id"] for row in index_rows}:
        raise ValueError("第41届分析单元与人工配置不一致")

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
                    "solution_text_path": str(source.relative_to(ROOT)),
                    "solution_text_sha256": sha256(source),
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
