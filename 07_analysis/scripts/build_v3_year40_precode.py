#!/usr/bin/env python3
"""Build the year-40 V3 mentor-perspective precode batch."""

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
OUTPUT = ROOT / "07_analysis/data/第40届科学思维V3导师视角试编码.csv"


PROFILES = {
    "CPHO40-Q01-1_i": {
        "output": "由两次成像测量求手机镜头的等效焦距",
        "question_lines": (25, 28),
        "solution_lines": (43, 69),
        "模型建构": ("L2", "把两次薄透镜成像和横向放大关系组织为消去未知物距的间接测量模型"),
        "科学推理": ("L3", "联立两组成像与放大关系并利用移动距离消元求等效焦距"),
    },
    "CPHO40-Q01-1_ii": {
        "output": "由测量量求第一位置的物距",
        "question_lines": (25, 29),
        "solution_lines": (70, 73),
        "科学推理": ("L1", "把前一小问所得焦距直接代回既有物距关系"),
    },
    "CPHO40-Q01-2_i": {
        "output": "求双薄透镜组物方和像方主点的位置",
        "question_lines": (30, 33),
        "solution_lines": (75, 123),
        "模型建构": ("L3", "整合两透镜成像、级联放大率、透镜间距和单位放大主平面条件"),
        "科学推理": ("L3", "联立两级成像与放大关系并利用光路可逆性求两个主点"),
    },
    "CPHO40-Q01-2_ii": {
        "output": "求双薄透镜组的物方焦距和像方焦距",
        "question_lines": (30, 35),
        "solution_lines": (124, 137),
        "模型建构": ("L2", "在前问主点模型上加入平行入射与焦点定义"),
        "科学推理": ("L3", "求平行光的最终像位置并分别扣除主点位置得到两侧焦距"),
    },
    "CPHO40-Q02-1": {
        "output": "求活塞中央平衡的临界温度及高温侧微振动频率",
        "question_lines": (37, 40),
        "solution_lines": (60, 95),
        "模型建构": ("L3", "整合两侧理想气体压强、重力、圆弧位移和小角振动建立临界模型"),
        "科学推理": ("L3", "展开非线性运动方程并由线性项符号推出临界温度和频率"),
    },
    "CPHO40-Q02-2": {
        "output": "判断临界温度下中央平衡的稳定性",
        "question_lines": (42, 42),
        "solution_lines": (96, 100),
        "模型建构": ("L2", "在临界点保留线性项消失后的最低非零三阶恢复项"),
        "科学推理": ("L2", "由三阶项的符号判断任意微小偏离后的加速度方向"),
        "科学论证": ("L1", "用三阶恢复力方向支持临界点仍为稳定平衡的结论"),
    },
    "CPHO40-Q02-3": {
        "output": "求低温侧非零平衡位置方程及近临界近似",
        "question_lines": (46, 47),
        "solution_lines": (101, 129),
        "模型建构": ("L3", "把非零平衡方程、左右对称分支和临界点展开组织为分岔模型"),
        "科学推理": ("L3", "建立隐式方程并在临界温度附近展开求两支近似解"),
    },
    "CPHO40-Q02-4": {
        "output": "求低温侧微振动频率及临界温度两侧的温度依赖",
        "question_lines": (49, 51),
        "solution_lines": (130, 175),
        "模型建构": ("L3", "在非零平衡点线性化运动并用平衡条件消去温度"),
        "科学推理": ("L3", "联立局部展开、平衡方程和近临界关系比较临界点两侧频率"),
    },
    "CPHO40-Q02-5": {
        "output": "求活塞由中央运动到任意可达角位置时的角速度",
        "question_lines": (53, 53),
        "solution_lines": (176, 197),
        "模型建构": ("L2", "把非线性运动方程转换为含两侧气体功和重力势能的能量模型"),
        "科学推理": ("L2", "对运动方程积分并代入零初速条件求角速度"),
    },
    "CPHO40-Q03-1_i": {
        "output": "求圆球纯滚动时楔块相对地面的加速度",
        "question_lines": (26, 28),
        "solution_lines": (46, 88),
        "模型建构": ("L3", "整合非惯性系受力、圆球转动、纯滚动约束和系统水平动量"),
        "科学推理": ("L3", "联立平动转动方程、约束关系和动量关系消元求楔块加速度"),
    },
    "CPHO40-Q03-1_ii": {
        "output": "求圆球质心相对楔块的加速度",
        "question_lines": (26, 30),
        "solution_lines": (89, 95),
        "科学推理": ("L1", "把前一小问的楔块加速度代入已建立的整体约束方程"),
    },
    "CPHO40-Q03-1_iii": {
        "output": "求地面对楔块的支持力",
        "question_lines": (26, 32),
        "solution_lines": (96, 120),
        "模型建构": ("L2", "把楔块与圆球视为整体并建立竖直质心动力学模型"),
        "科学推理": ("L2", "由质心竖直加速度和整体竖直受力求地面支持力"),
    },
    "CPHO40-Q03-1_iv": {
        "output": "求楔块对圆球的支持力",
        "question_lines": (26, 34),
        "solution_lines": (130, 139),
        "模型建构": ("L2", "在楔块参考系中建立圆球垂直斜面方向的受力平衡"),
        "科学推理": ("L2", "把楔块加速度代入法向平衡方程求支持力"),
    },
    "CPHO40-Q03-1_v": {
        "output": "求维持纯滚动所需的最小摩擦因数",
        "question_lines": (26, 36),
        "solution_lines": (140, 147),
        "模型建构": ("L1", "用极限静摩擦条件表示纯滚动保持边界"),
        "科学推理": ("L2", "组合前问摩擦力、质心加速度和支持力求临界比值"),
    },
    "CPHO40-Q03-2": {
        "output": "求滚动兼滑动时接触点相对楔块的速度",
        "question_lines": (38, 39),
        "solution_lines": (148, 174),
        "模型建构": ("L3", "重构滑动摩擦下楔块—圆球平动、转动和接触点运动模型"),
        "科学推理": ("L3", "联立动力学方程求恒加速度并组合平动与转动速度"),
    },
    "CPHO40-Q04-1": {
        "output": "求编木拱桥两接触点沿长杆的距离关系",
        "question_lines": (45, 46),
        "solution_lines": (74, 78),
        "模型建构": ("L1", "把圆柱杆接触位置表示为斜杆上的平面几何关系"),
        "科学推理": ("L1", "由接触几何直接求两段长度关系"),
    },
    "CPHO40-Q04-2": {
        "output": "画出关键杆件受力图并列出四根杆的平衡方程",
        "question_lines": (48, 50),
        "solution_lines": (79, 109),
        "模型建构": ("L3", "把六杆对称结构分解为四类杆件并协调接触力、摩擦力与作用反作用"),
        "科学推理": ("L3", "依据各受力图逐杆建立平动与转动力矩平衡方程组"),
    },
    "CPHO40-Q04-3": {
        "output": "求桥结构保持平衡所需的两类静摩擦因数条件",
        "question_lines": (52, 53),
        "solution_lines": (110, 180),
        "模型建构": ("L2", "在杆系平衡方程上加入两类接触面的极限静摩擦约束"),
        "科学推理": ("L3", "求解多杆接触力并分别转化为杆间和地面摩擦因数下界"),
    },
    "CPHO40-Q05-1": {
        "output": "确定电偶极场中点电荷匀速圆周运动的平面和速度",
        "question_lines": (47, 48),
        "solution_lines": (65, 104),
        "模型建构": ("L2", "把偶极场分解为轴向平衡与径向向心运动"),
        "科学推理": ("L3", "先由轴向零力确定圆周平面再由径向分量求速度"),
    },
    "CPHO40-Q05-2_i": {
        "output": "求静止释放后角动量随极角的关系",
        "question_lines": (50, 52),
        "solution_lines": (105, 138),
        "模型建构": ("L3", "把偶极力矩、平面运动和角动量变化组织为角变量模型"),
        "科学推理": ("L3", "用角速度消去时间并积分力矩方程得到角动量函数"),
    },
    "CPHO40-Q05-2_ii": {
        "output": "求径向速率随径向距离的关系",
        "question_lines": (50, 53),
        "solution_lines": (139, 176),
        "模型建构": ("L3", "整合能量守恒、角动量关系和偶极势能建立径向运动模型"),
        "科学推理": ("L3", "消去极角与切向动能并由初始条件求径向速率函数"),
    },
    "CPHO40-Q05-2_iii": {
        "output": "确定有界运动条件并求边界情形轨道",
        "question_lines": (50, 57),
        "solution_lines": (177, 217),
        "模型建构": ("L3", "把径向允许区间、初始极角和边界能量组织为轨道分类模型"),
        "科学推理": ("L3", "按初始角分类径向可达范围并在临界值下恢复平面轨道"),
        "科学论证": ("L2", "以速率非负条件和边界轨道推导支持有界与无界分类"),
    },
    "CPHO40-Q05-2_iv": {
        "output": "求无界运动时径向距离随时间的关系",
        "question_lines": (50, 58),
        "solution_lines": (218, 250),
        "模型建构": ("L2", "把无界条件下的径向速率方程约化为可分离变量模型"),
        "科学推理": ("L3", "分离变量积分并利用初始半径确定时间演化关系"),
    },
    "CPHO40-Q06-1": {
        "output": "求理想导体球在均匀磁场中的磁矩和面电流分布",
        "question_lines": (37, 42),
        "solution_lines": (57, 155),
        "模型建构": ("L3", "以球内零场、磁偶极等效和均匀磁化表面电流共同约束导体球"),
        "科学推理": ("L3", "由边界条件确定磁矩并构造产生同一内外磁场的面电流分布"),
    },
    "CPHO40-Q06-2": {
        "output": "求圆线圈在导体球球心处的交变磁场",
        "question_lines": (43, 43),
        "solution_lines": (156, 176),
        "模型建构": ("L1", "把载流圆线圈表示为轴线上磁场积分模型"),
        "科学推理": ("L2", "利用对称性和毕奥—萨伐尔定律积分得到时变磁场"),
    },
    "CPHO40-Q06-3": {
        "output": "求使导体球悬浮的线圈电流幅值",
        "question_lines": (44, 47),
        "solution_lines": (180, 235),
        "模型建构": ("L3", "整合近均匀线圈场、感生反向磁矩、场梯度力和周期平均平衡"),
        "科学推理": ("L3", "求瞬时安培力并作周期平均后与重力平衡求电流幅值"),
    },
    "CPHO40-Q06-4": {
        "output": "求趋肤层涡电流在一个周期内的平均热功率",
        "question_lines": (48, 50),
        "solution_lines": (236, 290),
        "模型建构": ("L3", "把等效面电流展开为有限趋肤层体电流并建立焦耳热体积分"),
        "科学推理": ("L3", "完成径向和角向积分、趋肤深度代换及时间平均"),
    },
    "CPHO40-Q07-1": {
        "output": "求对流层空气温度随高度的关系",
        "question_lines": (33, 36),
        "solution_lines": (60, 108),
        "模型建构": ("L3", "整合理想气体、静力平衡和缓慢绝热上升建立大气柱模型"),
        "科学推理": ("L3", "联立压强梯度、绝热关系和状态方程并对高度积分"),
    },
    "CPHO40-Q07-2": {
        "output": "求声速与温度关系并讨论各大气层的声速变化",
        "question_lines": (37, 39),
        "solution_lines": (109, 121),
        "模型建构": ("L2", "把绝热状态方程导数与理想气体状态方程组合为声速模型"),
        "科学推理": ("L2", "推出声速温度关系并映射到三层温度梯度"),
        "科学论证": ("L1", "用声速与温度的函数关系支持各层声速升降或不变的判断"),
    },
    "CPHO40-Q07-3": {
        "output": "分类平面分层大气中的声波折射和全反射并画传播路径",
        "question_lines": (40, 47),
        "solution_lines": (122, 150),
        "模型建构": ("L3", "把三层温度映射为两类声速并建立平面界面的声波折射模型"),
        "科学推理": ("L3", "计算声速比和临界角并按入射角分类传播路径"),
        "科学论证": ("L2", "以折射定律可解性和临界角比较支持折射与全反射分类"),
    },
    "CPHO40-Q07-4": {
        "output": "分类球面分层大气中四类远距离声传播情形",
        "question_lines": (49, 53),
        "solution_lines": (152, 185),
        "模型建构": ("L3", "整合球面分层、界面全反射、地球遮挡和四类源—探测器位置"),
        "科学推理": ("L3", "逐类追踪传播路径并用地球切线尺度估算可探测距离"),
        "科学论证": ("L3", "以四类路径比较、全反射条件和两项数量级估算系统支持远近结论"),
    },
    "CPHO40-Q08-1_i": {
        "output": "求使阳极原子K壳层电子电离的最小加速电压",
        "question_lines": (49, 54),
        "solution_lines": (72, 92),
        "模型建构": ("L1", "把电子加速动能与K壳层电离能建立阈值关系"),
        "科学推理": ("L1", "由能量守恒和电离阈值直接求最小电压"),
    },
    "CPHO40-Q08-1_ii": {
        "output": "求该加速电压下连续X射线的最短波长",
        "question_lines": (49, 56),
        "solution_lines": (93, 101),
        "模型建构": ("L1", "把单电子全部动能转化为单个轫致辐射光子的极限情形"),
        "科学推理": ("L1", "由最大光子能量与最短波长关系直接计算"),
    },
    "CPHO40-Q08-1_iii": {
        "output": "由K阿尔法特征线能量求阳极原子的核电荷数",
        "question_lines": (49, 57),
        "solution_lines": (103, 124),
        "模型建构": ("L2", "把类氢能级、有效核电荷和内层电子屏蔽组合为特征谱模型"),
        "科学推理": ("L2", "由谱线能量求有效核电荷并利用整数区间确定核电荷数"),
    },
    "CPHO40-Q08-2": {
        "output": "求康普顿散射后的光子波长和光电子动能",
        "question_lines": (59, 60),
        "solution_lines": (125, 188),
        "模型建构": ("L3", "建立光子与静止电子碰撞的相对论能量—动量守恒模型"),
        "科学推理": ("L3", "联立矢量动量、相对论能量和光子关系消元求波长及动能"),
    },
    "CPHO40-Q08-3": {
        "output": "解释散射谱双峰来源及两峰宽度差异",
        "question_lines": (62, 63),
        "solution_lines": (190, 200),
        "模型建构": ("L2", "以电子非弹性散射、原子准弹性散射和电子动量分布表征两个谱峰"),
        "科学推理": ("L2", "比较两类散射对象的反冲尺度并联系电子动量分布解释峰宽"),
        "科学论证": ("L2", "用康普顿位移、原子反冲近似和动量分布证据支持双峰机制解释"),
    },
}


def main() -> None:
    index_rows = [
        row for row in read_rows(INDEX) if row["competition_no"] == "40"
    ]
    if len(index_rows) != 36 or set(PROFILES) != {row["item_id"] for row in index_rows}:
        raise ValueError("第40届分析单元与人工配置不一致")

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
