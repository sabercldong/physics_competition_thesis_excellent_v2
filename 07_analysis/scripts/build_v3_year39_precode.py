#!/usr/bin/env python3
"""Build the year-39 V3 mentor-perspective precode batch."""

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
OUTPUT = ROOT / "07_analysis/data/第39届科学思维V3导师视角试编码.csv"


PROFILES = {
    "CPHO39-Q01-1": {
        "output": "由条纹变化求两类反射的相位突变差异",
        "question_lines": (49, 50),
        "solution_lines": (65, 113),
        "模型建构": ("L3", "把迈克尔逊干涉等效为含额外反射相位的等倾薄膜干涉模型"),
        "科学推理": ("L3", "联立中心、边缘条纹和移动前后周期变化求相位差"),
    },
    "CPHO39-Q01-2": {
        "output": "求反射镜移动后的干涉亮条纹数",
        "question_lines": (51, 51),
        "solution_lines": (114, 123),
        "科学推理": ("L1", "直接调用前问已确定的光程差和最大倾角关系计算条纹数"),
    },
    "CPHO39-Q01-3": {
        "output": "由倾斜空槽和注液后的条纹变化求液体折射率",
        "question_lines": (52, 56),
        "solution_lines": (125, 159),
        "模型建构": ("L3", "整合槽内折射、倾斜几何、往返光程和两阶段条纹变化建立测量模型"),
        "科学推理": ("L3", "由折射定律和光程差作小角展开并利用两次周期差求折射率"),
    },
    "CPHO39-Q02-1": {
        "output": "求恒流螺线管弹簧的平衡方程、等效劲度和允许电流范围",
        "question_lines": (26, 35),
        "solution_lines": (48, 136),
        "模型建构": ("L3", "整合弹性势能、磁场能、恒流源做功和平衡微扰建立电磁弹簧模型"),
        "科学推理": ("L3", "由能量变化求平衡和等效劲度并以代数方程极值限定电流"),
    },
    "CPHO39-Q02-2": {
        "output": "求零电阻闭合回路中弹簧的平衡长度和等效劲度",
        "question_lines": (37, 41),
        "solution_lines": (137, 179),
        "模型建构": ("L3", "以磁通守恒替代恒流条件重构弹簧—电感闭合系统能量模型"),
        "科学推理": ("L3", "由磁通约束、电感随长度变化和总能量微扰求平衡与等效劲度"),
    },
    "CPHO39-Q03-1": {
        "output": "求实心球第一次碰撞前的质心速度和自转角速度",
        "question_lines": (50, 50),
        "solution_lines": (61, 80),
        "模型建构": ("L2", "把球在斜面参考系中的飞行表示为平面抛体和绕质心转动模型"),
        "科学推理": ("L2", "由回到斜面的时间和重力分量求碰前速度并判断角速度不变"),
    },
    "CPHO39-Q03-2": {
        "output": "求实心球第一次碰撞后的质心速度和自转角速度",
        "question_lines": (51, 51),
        "solution_lines": (81, 121),
        "模型建构": ("L3", "整合切向冲量、角冲量、弹性碰撞能量和接触点无滑动建立碰撞模型"),
        "科学推理": ("L3", "联立动量、角动量和能量关系求碰后平动转动状态"),
    },
    "CPHO39-Q03-3": {
        "output": "求第n次碰撞后的沿斜面速度和自转角速度",
        "question_lines": (52, 53),
        "solution_lines": (122, 244),
        "模型建构": ("L3", "把飞行阶段速度增量与碰撞映射组织为平动—转动递推模型"),
        "科学推理": ("L3", "求解耦合递推并按碰撞次数奇偶给出通项"),
    },
    "CPHO39-Q03-4": {
        "output": "求前n次碰撞中斜面对球施加的总冲量",
        "question_lines": (54, 54),
        "solution_lines": (245, 285),
        "模型建构": ("L2", "把各次碰撞前后动量变化组织为累计冲量模型"),
        "科学推理": ("L3", "对切向和法向冲量分别求和并代入前问奇偶通项"),
    },
    "CPHO39-Q04-1": {
        "output": "分别写出细杆在实验室系和转动系中的机械能",
        "question_lines": (31, 32),
        "solution_lines": (51, 155),
        "模型建构": ("L3", "在实验室系与随动转动系中分别组织刚体动能、重力势能和离心势能"),
        "科学推理": ("L3", "完成参考系变换并积分杆上各质元的速度或离心势能贡献"),
    },
    "CPHO39-Q04-2": {
        "output": "导出转动系中细杆平衡位形的角度条件",
        "question_lines": (33, 33),
        "solution_lines": (156, 184),
        "模型建构": ("L2", "把重力矩和分布离心力矩表示为角度函数"),
        "科学推理": ("L3", "积分分布力矩并与势能极值条件相互核对得到平衡方程"),
    },
    "CPHO39-Q04-3": {
        "output": "用图解法分类各象限平衡位形数目及参数条件",
        "question_lines": (34, 38),
        "solution_lines": (185, 319),
        "模型建构": ("L3", "把非线性平衡方程转化为正切曲线与移位正弦曲线的交点模型"),
        "科学推理": ("L3", "按象限、相切边界和参数尺度系统分类交点数"),
    },
    "CPHO39-Q04-4": {
        "output": "用各象限受力图检验图解法得到的平衡位形结论",
        "question_lines": (41, 43),
        "solution_lines": (320, 355),
        "模型建构": ("L3", "为各象限建立重力与等效离心力对支点力矩的受力图模型"),
        "科学推理": ("L3", "逐象限比较两类力矩方向并判断能否达到平衡"),
        "科学论证": ("L2", "用独立受力图证据比较多个象限并检验前问图解结论"),
    },
    "CPHO39-Q04-5": {
        "output": "讨论各个平衡位形的稳定性",
        "question_lines": (44, 44),
        "solution_lines": (356, 507),
        "模型建构": ("L3", "把各平衡分支表示为局部力矩斜率或势能曲率模型"),
        "科学推理": ("L3", "按象限、双解分支和相切拐点系统判断微扰后的响应"),
        "科学论证": ("L3", "以恢复力矩、势能二阶导数及拐点检验系统支持各分支稳定性结论"),
    },
    "CPHO39-Q05-1": {
        "output": "写出弹簧1长度和小球加速度满足的运动方程",
        "question_lines": (47, 49),
        "solution_lines": (73, 75),
        "模型建构": ("L2", "把小球、两弹簧和时变外力表示为一维受力与形变量模型"),
        "科学推理": ("L1", "按牛顿第二定律和胡克定律写出单一运动方程"),
    },
    "CPHO39-Q05-2": {
        "output": "求线性增载时两根弹簧长度随时间的解析式",
        "question_lines": (50, 58),
        "solution_lines": (76, 206),
        "模型建构": ("L3", "把移动平衡位置、受迫振动和初始条件整合为非齐次振子模型"),
        "科学推理": ("L3", "求解微分方程并由初始条件确定常量和两弹簧长度"),
    },
    "CPHO39-Q05-3": {
        "output": "分类两弹簧先断条件并解释快拉与慢拉实验现象",
        "question_lines": (60, 64),
        "solution_lines": (207, 275),
        "模型建构": ("L3", "把两弹簧长度差、断裂相位和加载速率组织为事件分类模型"),
        "科学推理": ("L3", "按加载率和振动相位求先断区间并比较区间随加载率的变化"),
        "科学论证": ("L2", "以慢加载和快加载下先断条件的比较解释题述实验现象"),
    },
    "CPHO39-Q05-4": {
        "output": "求确保弹簧2先断及两弹簧同时断裂的加载率条件",
        "question_lines": (65, 66),
        "solution_lines": (276, 304),
        "模型建构": ("L2", "在长度解析式上加入共同临界长度和断裂事件约束"),
        "科学推理": ("L3", "联立达到临界长度时刻与长度差条件求不等式和等式"),
        "科学论证": ("L1", "用同时达到共同临界长度的条件支持两弹簧可同时断裂的判断"),
    },
    "CPHO39-Q06-1": {
        "output": "求扩散与电漂移抵消时金属内部电场",
        "question_lines": (41, 59),
        "solution_lines": (83, 93),
        "模型建构": ("L2", "把电子扩散流和欧姆漂移电流组织为零净流模型"),
        "科学推理": ("L2", "联立斐克定律、扩散系数和零电流条件求电场"),
    },
    "CPHO39-Q06-2": {
        "output": "导出电场及电子数密度满足的微分方程和边界条件",
        "question_lines": (62, 64),
        "solution_lines": (94, 132),
        "模型建构": ("L3", "整合体电荷、表面电荷、高斯定理和扩散电场建立边值模型"),
        "科学推理": ("L3", "消去电场并由真空侧零场条件推得两端边界条件"),
    },
    "CPHO39-Q06-3": {
        "output": "线性化并求解电子数密度扰动",
        "question_lines": (65, 66),
        "solution_lines": (133, 234),
        "模型建构": ("L3", "把非线性密度方程约化为带表面电荷边界的线性双曲函数模型"),
        "科学推理": ("L3", "求解二阶常系数边值问题并确定积分常量"),
    },
    "CPHO39-Q06-4": {
        "output": "导出并求解局域平衡时的温度扰动",
        "question_lines": (67, 70),
        "solution_lines": (235, 291),
        "模型建构": ("L3", "整合局域理想气体压强、薄层力学平衡和电场作用建立温度模型"),
        "科学推理": ("L3", "线性化压强梯度方程并代入密度解得到温度分布"),
    },
    "CPHO39-Q06-5": {
        "output": "求金属两端电势差与温度差之比",
        "question_lines": (71, 74),
        "solution_lines": (292, 325),
        "科学推理": ("L2", "组合前问电场—温度关系或两端积分结果直接求Seebeck系数"),
    },
    "CPHO39-Q07-1": {
        "output": "导出超相对论夸克物质的压强—能量密度状态方程",
        "question_lines": (36, 36),
        "solution_lines": (59, 123),
        "模型建构": ("L3", "把各向同性超相对论粒子对假想器壁的动量交换组织为压强模型"),
        "科学推理": ("L3", "对速度方向和能量分组求平均得到压强与能量密度关系"),
    },
    "CPHO39-Q07-2": {
        "output": "导出夸克物质的压强—数密度—温度状态方程",
        "question_lines": (37, 38),
        "solution_lines": (124, 198),
        "模型建构": ("L3", "把超相对论能量—动量关系与玻尔兹曼分布整合为平均能量模型"),
        "科学推理": ("L3", "计算能量分布积分并代入前问压强关系"),
    },
    "CPHO39-Q07-3": {
        "output": "求夸克物质的定体摩尔热容和热容比",
        "question_lines": (39, 39),
        "solution_lines": (199, 219),
        "模型建构": ("L2", "把平均粒子能量和状态方程映射为摩尔内能与焓模型"),
        "科学推理": ("L2", "分别对内能和焓求温度导数并计算热容比"),
    },
    "CPHO39-Q07-4": {
        "output": "求绝热膨胀降温后火球的半径",
        "question_lines": (41, 45),
        "solution_lines": (220, 232),
        "模型建构": ("L2", "把准静态绝热关系与球形火球体积变化组合为尺度模型"),
        "科学推理": ("L2", "代入热容比并消去体积求温度与半径的比例"),
    },
}


def main() -> None:
    index_rows = [
        row for row in read_rows(INDEX) if row["competition_no"] == "39"
    ]
    if len(index_rows) != 27 or set(PROFILES) != {row["item_id"] for row in index_rows}:
        raise ValueError("第39届分析单元与人工配置不一致")

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
