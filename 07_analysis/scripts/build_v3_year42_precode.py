#!/usr/bin/env python3
"""Build the year-42 V3 mentor-perspective precode batch."""

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
OUTPUT = ROOT / "07_analysis/data/第42届科学思维V3导师视角试编码.csv"


PROFILES = {
    "CPHO42-Q01-1": {
        "output": "求磁光陷阱撤除前原子气的归一化相空间分布函数",
        "question_lines": (15, 29),
        "solution_lines": (48, 67),
        "科学推理": ("L2", "利用三方向高斯积分和总原子数归一化条件确定比例系数"),
        "model_absence_reason": "题目已直接给出相空间分布函数的指数形式，本小问只需通过归一化确定比例系数，未要求新建或调整对象—变量—约束表示。",
    },
    "CPHO42-Q01-2": {
        "output": "求释放后探测平面的纵向数密度和原子流随时间的关系",
        "question_lines": (23, 31),
        "solution_lines": (68, 123),
        "模型建构": ("L3", "把自由落体反演、初始相空间分布和探测平面的密度及通量积分统一起来"),
        "科学推理": ("L3", "由末态位置速度反推初态并分别完成数密度和带速度权重的积分"),
    },
    "CPHO42-Q01-3": {
        "output": "求低温强约束极限下数密度峰和原子流峰对应的时间",
        "question_lines": (33, 35),
        "solution_lines": (125, 210),
        "科学推理": ("L3", "对前问两个时间函数分别求极值并作低温渐近展开保留首个温度修正"),
    },
    "CPHO42-Q01-4": {
        "output": "求数密度时间峰附近高斯分布的有效展宽",
        "question_lines": (37, 39),
        "solution_lines": (215, 250),
        "模型建构": ("L2", "把数密度峰附近的对数二阶展开映射为局部高斯展宽模型"),
        "科学推理": ("L3", "利用驻点条件、二阶泰勒展开和低温极限匹配高斯指数系数"),
    },
    "CPHO42-Q02-1_1": {
        "output": "求离子在平行板能量分析器中的水平接收距离",
        "question_lines": (51, 59),
        "solution_lines": (93, 116),
        "模型建构": ("L3", "整合板间斜抛、板外无场直线运动和入射接收几何建立分段轨迹"),
        "科学推理": ("L3", "由电场加速度、动能和各段几何距离消去速度与时间"),
    },
    "CPHO42-Q02-1_2": {
        "output": "确定二级聚焦入射角并求接收距离和极板电压",
        "question_lines": (51, 63),
        "solution_lines": (117, 159),
        "模型建构": ("L2", "把前问接收距离函数扩展为入射角微扰下的二级聚焦模型"),
        "科学推理": ("L3", "展开到角度偏差二阶并令一阶二阶系数同时为零求参数"),
    },
    "CPHO42-Q02-1_3": {
        "output": "求偏离入射狭缝中心的离子在接收板上的位置偏差",
        "question_lines": (65, 67),
        "solution_lines": (161, 177),
        "模型建构": ("L2", "协调入射偏移、板间运动和倾斜接收板几何"),
        "科学推理": ("L2", "联立水平垂直坐标及出板后的直线斜率求位置映射"),
    },
    "CPHO42-Q02-2_1": {
        "output": "求非严格二级聚焦时中心入射对应的接收板偏差",
        "question_lines": (69, 72),
        "solution_lines": (183, 198),
        "科学推理": ("L1", "在前问一般位置映射中令入射偏移为零得到接收偏差"),
    },
    "CPHO42-Q02-2_2": {
        "output": "由上下半平面接收电流反演二次离子束动能",
        "question_lines": (69, 76),
        "solution_lines": (201, 221),
        "模型建构": ("L2", "把均匀狭缝入射区间映射为上下接收板的电流份额"),
        "科学推理": ("L2", "由两侧电流比例反求分界入射位置并代回轨迹关系求动能"),
    },
    "CPHO42-Q02-2_3": {
        "output": "由一次和二次离子能量测量求等离子体测量位置的电势",
        "question_lines": (78, 85),
        "solution_lines": (224, 273),
        "模型建构": ("L3", "整合直接电离能量守恒、离子电势能变化和分析器动能反演"),
        "科学推理": ("L3", "依次消去电子及电离能小量并联立两种电荷态的动能关系求电势"),
    },
    "CPHO42-Q03-1": {
        "output": "设计不受接触电阻影响的霍尔电阻测量接法并证明",
        "question_lines": (31, 48),
        "solution_lines": (81, 91),
        "模型建构": ("L2", "把自主选择的通流端口和测压端口映射到给定等效电路"),
        "科学推理": ("L2", "沿所选端口回路计算电压差并由霍尔电阻定义消去接触电阻"),
        "科学论证": ("L1", "用一个具体端口接法的回路电压支持测量结果与接触电阻无关"),
        "质疑创新": ("L2", "在非唯一端口组合中自主提出满足抗接触电阻约束的测量接法并给出证据"),
    },
    "CPHO42-Q03-2_1": {
        "output": "比较双器件断路与连通接法的霍尔电阻及接触电阻误差",
        "question_lines": (49, 68),
        "solution_lines": (92, 136),
        "模型建构": ("L3", "建立双量子霍尔器件在开关断开和闭合时的两套耦合等效电路"),
        "科学推理": ("L3", "分别列写基尔霍夫方程并比较接触电阻误差的一阶与二阶量级"),
        "科学论证": ("L3", "用两套显式电阻表达式和小量阶分析系统支持连通接法误差更小"),
    },
    "CPHO42-Q03-2_2": {
        "output": "求三重并联系统霍尔电阻并证明接触电阻误差阶",
        "question_lines": (70, 74),
        "solution_lines": (138, 212),
        "模型建构": ("L3", "整合两个器件、多端口三重并联、零接触电阻假设和测量端口"),
        "科学推理": ("L3", "联立多回路方程消去支路电流并对最终电阻式执行三阶小量分析"),
        "科学论证": ("L3", "用完整多回路解和误差项因子分解支持相对误差为三阶量"),
    },
    "CPHO42-Q04-1_1": {
        "output": "求静止电子在平面激光场中的相对论动量和能量",
        "question_lines": (29, 38),
        "solution_lines": (65, 122),
        "模型建构": ("L3", "整合平面电磁波、相对论洛伦兹力和能量动量关系建立电子动力学"),
        "科学推理": ("L3", "由分量运动方程识别守恒量并消去纵向动量得到能量表达式"),
    },
    "CPHO42-Q04-1_2": {
        "output": "求电子位置坐标与时间的隐式关系",
        "question_lines": (36, 40),
        "solution_lines": (124, 154),
        "模型建构": ("L2", "引入随波相位变量并把电子三维运动约化为平面参数轨迹"),
        "科学推理": ("L3", "利用前问动量和守恒量分别积分横向及纵向坐标"),
    },
    "CPHO42-Q04-2": {
        "output": "求给定初能电子的最大加速能量及对应入射角",
        "question_lines": (42, 44),
        "solution_lines": (157, 284),
        "模型建构": ("L3", "把任意初始相对论动量、平面波相位和能量守恒量组织为参数优化模型"),
        "科学推理": ("L3", "先对相位取极值再在动量约束下对入射角求极值并验证极大性"),
    },
    "CPHO42-Q04-3": {
        "output": "估算强激光中电子一个周期的辐射阻尼相对能量损失",
        "question_lines": (46, 55),
        "solution_lines": (288, 325),
        "模型建构": ("L2", "把激光强度与电磁场振幅关系接入给定辐射损失微分方程"),
        "科学推理": ("L3", "由坡印廷矢量求场强并积分能量损失方程后代入周期和数值"),
    },
    "CPHO42-Q05-1": {
        "output": "求恒定结电压下约瑟夫森电流密度及其周期",
        "question_lines": (34, 40),
        "solution_lines": (80, 92),
        "科学推理": ("L1", "对题给相位时间方程直接积分并代入电流密度关系识别周期"),
        "model_absence_reason": "题目已直接给出相位变化率与电流密度关系，本小问只需积分、代入并识别周期，未要求新建或调整对象—变量—约束表示。",
    },
    "CPHO42-Q05-2_1": {
        "output": "求均匀外磁场下相位分布、总约瑟夫森电流及零点",
        "question_lines": (41, 47),
        "solution_lines": (95, 123),
        "模型建构": ("L2", "把局部相位梯度和电流密度沿结的横向截面积整合为总电流"),
        "科学推理": ("L2", "积分相位梯度并对正弦电流密度作空间积分后求零点"),
    },
    "CPHO42-Q05-2_2": {
        "output": "证明含自生磁场的相位方程并求约瑟夫森穿透深度",
        "question_lines": (49, 50),
        "solution_lines": (124, 141),
        "模型建构": ("L2", "把安培环路定理与相位梯度关系组合为自洽场—相位模型"),
        "科学推理": ("L2", "对相位梯度求导并消去磁场梯度得到非线性方程及尺度"),
        "科学论证": ("L1", "用安培环路定理和相位梯度两条关系支持所给正弦型相位方程"),
    },
    "CPHO42-Q05-3_1": {
        "output": "建立并联结、电阻和电容三支路的相位动力学方程",
        "question_lines": (52, 59),
        "solution_lines": (144, 160),
        "模型建构": ("L3", "把理想约瑟夫森结、电阻、电容和外加偏置电流整合为并联电路模型"),
        "科学推理": ("L3", "分别把三支路电流写成相位及其导数并用节点电流关系合并"),
    },
    "CPHO42-Q05-3_2": {
        "output": "求相位等效势、势阱条件、稳定点和小振动频率",
        "question_lines": (61, 66),
        "solution_lines": (162, 214),
        "模型建构": ("L3", "把无耗散相位方程重构为单位质量粒子的势能和小振动模型"),
        "科学推理": ("L3", "积分得到等效能量并依次判断驻点、稳定性、势阱范围和曲率频率"),
        "科学论证": ("L2", "用一阶驻点和二阶曲率比较支持势阱存在范围及稳定平衡分支"),
    },
    "CPHO42-Q05-3_3": {
        "output": "求约瑟夫森结区电磁波速与真空光速之比",
        "question_lines": (68, 70),
        "solution_lines": (217, 230),
        "模型建构": ("L2", "把等离子体频率、穿透深度和平行板电容组合为结区波速模型"),
        "科学推理": ("L3", "联立前问尺度关系消去结面积、电流密度和基本常数后代入参数"),
    },
    "CPHO42-Q06-1_1": {
        "output": "求转速仪稳态角速度并讨论不同质量关系下的存在条件",
        "question_lines": (51, 58),
        "solution_lines": (79, 118),
        "模型建构": ("L3", "在共转参考系中整合盘簧、重力和离心力矩建立稳态模型"),
        "科学推理": ("L3", "由力矩平衡求角速度并按质量关系和角度象限分类判断实根条件"),
        "科学论证": ("L3", "用分质量关系和分角度区间的符号分析系统支持稳态存在条件"),
    },
    "CPHO42-Q06-1_2": {
        "output": "求转速仪相对中心的角动量及两轴承作用力",
        "question_lines": (59, 60),
        "solution_lines": (120, 212),
        "模型建构": ("L3", "整合两质点与匀质杆角动量、质心运动和双轴承力矩约束"),
        "科学推理": ("L3", "由角动量变化率、质心定理和质点系角动量定理解出力分量"),
    },
    "CPHO42-Q06-2_1": {
        "output": "由冲击后最大摆角求初始角速度",
        "question_lines": (62, 66),
        "solution_lines": (217, 254),
        "模型建构": ("L3", "把轴向角动量守恒、转动动能、盘簧势能和最大摆角状态统一起来"),
        "科学推理": ("L3", "先由角动量守恒消去转轴角速度再用机械能守恒反求冲击初速"),
    },
    "CPHO42-Q06-2_2": {
        "output": "求细杆在稳态角附近小幅振动的角频率",
        "question_lines": (62, 68),
        "solution_lines": (258, 307),
        "模型建构": ("L3", "把角动量约束代入总能量并在稳态角附近建立二阶小振动模型"),
        "科学推理": ("L3", "展开等效能量到振幅二阶并以正曲率识别简谐频率"),
    },
    "CPHO42-Q06-2_3": {
        "output": "求小振动过程中转速仪竖轴角速度的一阶时间变化",
        "question_lines": (62, 71),
        "solution_lines": (312, 320),
        "科学推理": ("L2", "把前问简谐角位移代入既有角动量关系并作振幅一阶展开"),
    },
    "CPHO42-Q07-1": {
        "output": "导出自聚焦光纤中三维光线的径向和角向微分方程",
        "question_lines": (29, 42),
        "solution_lines": (56, 134),
        "模型建构": ("L3", "把梯度折射率光纤分层、空间曲线切向量和界面折射定律统一起来"),
        "科学推理": ("L3", "对相邻薄层传播方向作一阶展开并分别使用共面和折射角条件"),
    },
    "CPHO42-Q07-2": {
        "output": "求给定初始条件下光线离轴线的最远距离",
        "question_lines": (44, 47),
        "solution_lines": (137, 174),
        "模型建构": ("L3", "把两个光线微分方程积分为不变量并施加初始与转向点条件"),
        "科学推理": ("L3", "消去角向导数并在径向速度为零时求代数方程的物理解"),
    },
    "CPHO42-Q07-3": {
        "output": "求光线在直角坐标系中的三维螺旋轨迹",
        "question_lines": (44, 48),
        "solution_lines": (179, 232),
        "模型建构": ("L3", "把柱坐标不变量转换为直角坐标耦合方程并建立振子型轨迹"),
        "科学推理": ("L3", "排除不符初始条件的常半径分支并由边界条件确定四个待定系数"),
    },
}


def main() -> None:
    index_rows = [
        row for row in read_rows(INDEX) if row["competition_no"] == "42"
    ]
    if len(index_rows) != 31 or set(PROFILES) != {row["item_id"] for row in index_rows}:
        raise ValueError("第42届分析单元与人工配置不一致")

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
                if dimension == "模型建构" and "model_absence_reason" in profile:
                    reason = profile["model_absence_reason"]
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
