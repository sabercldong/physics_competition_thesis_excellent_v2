#!/usr/bin/env python3
"""Build the GB/T 7714 candidate-reference work list from allowed, read source IDs."""

from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MANUSCRIPT_DIR = ROOT / "08_manuscript"
MAPPING_PATH = ROOT / "09_quality/g8_02_bib_lite_mapping.csv"
BIB_PATH = ROOT / "02_literature/references.bib"
OUTPUT_MD = MANUSCRIPT_DIR / "07_candidate_references.md"
OUTPUT_CSV = ROOT / "09_quality/r01_candidate_references_mapping_v1.csv"
SOURCE_ID = re.compile(r"\b(?:(?:CS|ST|METH|PCOMP)-\d{3}|SOLO-(?:(?:APP|PHY)-\d{3}|\d{3}))\b")
BIB_KEY = re.compile(r"^@\w+\{([^,]+),", re.MULTILINE)
CHAPTERS = [MANUSCRIPT_DIR / f"{index:02d}_{name}.md" for index, name in [
    (1, "introduction"), (2, "theory"), (3, "methods"),
    (4, "results"), (5, "cases_and_diagnosis"), (6, "conclusion"),
]]
FORMATTED = {
    "CS-001": "中华人民共和国教育部. 普通高中物理课程标准（2017年版2020年修订）[S/OL]. 2020-06-03 [2026-07-24]. http://www.moe.gov.cn/srcsite/A26/s8001/202006/t20200603_462199.html.",
    "SOLO-001": "Biggs J B, Collis K F. Evaluating the quality of learning: The SOLO taxonomy (structure of the observed learning outcome)[M]. New York: Academic Press, 1982. DOI:10.1016/C2013-0-10375-3.",
    "ST-002": "Bao L, Cai T, Koenig K, et al. Learning and scientific reasoning[J]. Science, 2009, 323(5914): 586-587. DOI:10.1126/science.1167740.",
    "ST-003": "Bao L, Koenig K, Xiao Y, et al. Theoretical model and quantitative assessment of scientific thinking and reasoning[J]. Physical Review Physics Education Research, 2022, 18(1): 010115. DOI:10.1103/PhysRevPhysEducRes.18.010115.",
    "ST-005": "Osborne J, Erduran S, Simon S. Enhancing the quality of argumentation in school science[J]. Journal of Research in Science Teaching, 2004, 41(10): 994-1020. DOI:10.1002/tea.20035.",
    "ST-006": "NGSS Lead States. Next Generation Science Standards: For States, By States[M]. Washington, DC: The National Academies Press, 2013. DOI:10.17226/18290.",
    "ST-007": "Etkina E, Van Heuvelen A, White-Brahmia S, et al. Scientific abilities and their assessment[J]. Physical Review Special Topics - Physics Education Research, 2006, 2(2): 020103. DOI:10.1103/PhysRevSTPER.2.020103.",
    "ST-008": "Russ R S, Odden T O B. Intertwining evidence- and model-based reasoning in physics sensemaking: An example from electrostatics[J]. Physical Review Physics Education Research, 2017, 13(2): 020105. DOI:10.1103/PhysRevPhysEducRes.13.020105.",
    "ST-009": "Zwickl B M, Hu D, Finkelstein N, et al. Model-based reasoning in the physics laboratory: Framework and initial results[J]. Physical Review Special Topics - Physics Education Research, 2015, 11(2): 020113. DOI:10.1103/PhysRevSTPER.11.020113.",
    "ST-010": "Pols C F J, Dekkers P J J M, de Vries M J. Integrating argumentation in physics inquiry: A design and evaluation study[J]. Physical Review Physics Education Research, 2023, 19(2): 020170. DOI:10.1103/PhysRevPhysEducRes.19.020170.",
    "ST-011": "Pols C F J, Dekkers P J J M, de Vries M J. Defining and assessing understandings of evidence with the assessment rubric for physics inquiry: Towards integration of argumentation and inquiry[J]. Physical Review Physics Education Research, 2022, 18(1): 010111. DOI:10.1103/PhysRevPhysEducRes.18.010111.",
    "METH-004": "Lombard M, Snyder-Duch J, Bracken C C. Content analysis in mass communication: Assessment and reporting of intercoder reliability[J]. Human Communication Research, 2002, 28(4): 587-604. DOI:10.1111/j.1468-2958.2002.tb00826.x.",
    "METH-006": "Wei B, Wang C, Tan L. Visual representation of optical content in China’s and Singapore’s junior secondary physics textbooks[J]. Physical Review Physics Education Research, 2022, 18(2): 020138. DOI:10.1103/PhysRevPhysEducRes.18.020138.",
    "METH-007": "McHugh M L. Interrater reliability: The kappa statistic[J]. Biochemia Medica, 2012, 22(3): 276-282. DOI:10.11613/BM.2012.031.",
    "METH-008": "于海波, 王宇琪, 伊西凡, 等. 近10年高考物理试卷与课程标准的一致性研究[J]. 物理教师, 2024, 45(5): 67-73.",
    "ST-014": "Wang C, Wei B. Analysis of visual-based physics questions of the senior high school entrance examination in China[J]. Physical Review Physics Education Research, 2024, 20(1): 010112. DOI:10.1103/PhysRevPhysEducRes.20.010112.",
    "METH-009": "Gladys M J, Furst J E, Holdsworth J L, et al. Gender bias in first-year multiple-choice physics examinations[J]. Physical Review Physics Education Research, 2023, 19(2): 020109. DOI:10.1103/PhysRevPhysEducRes.19.020109.",
    "ST-015": "Al-Salmani F, Thacker B. Rubric for assessing thinking skills in free-response exam problems[J]. Physical Review Physics Education Research, 2021, 17(1): 010135. DOI:10.1103/PhysRevPhysEducRes.17.010135.",
    "ST-016": "Lin S-Y, Singh C. Effect of scaffolding on helping introductory physics students solve quantitative problems involving strong alternative conceptions[J]. Physical Review Special Topics - Physics Education Research, 2015, 11(2): 020105. DOI:10.1103/PhysRevSTPER.11.020105.",
    "ST-012": "Teodorescu R E, Bennhold C, Feldman G, et al. New approach to analyzing physics problems: A Taxonomy of Introductory Physics Problems[J]. Physical Review Special Topics - Physics Education Research, 2013, 9(1): 010103. DOI:10.1103/PhysRevSTPER.9.010103.",
    "ST-013": "Kocakaya S, Gonen S. Analysis of Turkish high-school physics-examination questions according to Bloom's taxonomy[J]. Asia-Pacific Forum on Science Learning and Teaching, 2010, 11(1): Article 9, 1-14.",
    "ST-017": "Burkholder E W, Miles J K, Layden T J, et al. Template for teaching and assessment of problem solving in introductory physics[J]. Physical Review Physics Education Research, 2020, 16(1): 010123. DOI:10.1103/PhysRevPhysEducRes.16.010123.",
    "ST-018": "Docktor J L, Dornfeld J, Frodermann E, et al. Assessing student written problem solutions: A problem-solving rubric with application to introductory physics[J]. Physical Review Physics Education Research, 2016, 12(1): 010130. DOI:10.1103/PhysRevPhysEducRes.12.010130.",
    "PCOMP-006": "陈奕帆, 杨欢. 四球探秘——隐藏在一道高中物理竞赛题背后的秘密[J]. 大学物理, 2025, 44(5): 58-64. DOI:10.16854/j.cnki.1000-0712.240228.",
    "ST-019": "Tschisgale P, Kubsch M, Wulff P, et al. Exploring the sequential structure of students’ physics problem-solving approaches using process mining and sequence analysis[J]. Physical Review Physics Education Research, 2025, 21(1): 010111. DOI:10.1103/PhysRevPhysEducRes.21.010111.",
    "ST-020": "Tschisgale P, Maus H, Kieser F, et al. Evaluating GPT- and reasoning-based large language models on Physics Olympiad problems: Surpassing human performance and implications for educational assessment[J]. Physical Review Physics Education Research, 2025, 21(2): 020115. DOI:10.1103/PhysRevPhysEducRes.21.020115.",
    "ST-021": "Meyer A, Fischer S, Friege G. Analyzing problem solving in secondary physics education: A rubric-guided approach to explore individual learning needs[J]. Physical Review Physics Education Research, 2026, 22(1): 010111. DOI:10.1103/3bs7-fnrd.",
    "SOLO-APP-001": "Mol S M, Matos D A S. Uma analise da complexidade de itens de matematica por meio da taxonomia SOLO[J]. Estudos em Avaliacao Educacional, 2025, 36: e11415. DOI:10.18222/eae.v36.11415.",
    "SOLO-PHY-001": "肖雅洁. 基于SOLO分类法的试题评价分析——以一道高考物理题为例[J]. 社会科学前沿, 2020, 9(7): 949-955. DOI:10.12677/ASS.2020.97133.",
    "SOLO-PHY-002": "于海波, 冯薇橦, 杨振东. 2024年高考新课标卷的科学思维考查难度与教学启示——基于SOLO分类理论与LPs理论结合的视角[J]. 物理教师, 2025, 46(2): 67-71.",
    "SOLO-PHY-003": "王贤勇, 喻斌. 基于布鲁姆学习目标和SOLO分类理论的试题对比评析[J]. 物理教师, 2023, 44(1): 84-92.",
    "PCOMP-002": "龚枭. 基于SOLO分类理论的全国中学生物理竞赛复赛理论试题研究[D]. 华中师范大学, 2020.",
    "PCOMP-003": "唐路. 全国中学生物理竞赛试题研究[D]. 湖南师范大学, 2020.",
    "PCOMP-004": "凌国亮, 黄致新, 祝文秀. 基于数理核心素养的全国中学生物理竞赛预赛典型试题分析[J]. 物理教学探讨, 2020(4): 39-42.",
    "PCOMP-007": "凌国亮. 基于数理核心素养的全国中学生物理竞赛预赛试题分析研究[D]. 华中师范大学, 2020.",
    "PCOMP-008": "张豇萌. 基于综合难度模型的全国中学生物理竞赛复赛理论试题研究[D]. 湖南师范大学, 2022.",
}


def first_citation_order() -> list[str]:
    ordered = []
    for chapter in CHAPTERS:
        for line in chapter.read_text(encoding="utf-8").splitlines():
            if "[引文占位：" not in line:
                continue
            for source_id in SOURCE_ID.findall(line):
                if source_id in FORMATTED and source_id not in ordered:
                    ordered.append(source_id)
    return ordered


def main() -> None:
    with MAPPING_PATH.open(encoding="utf-8", newline="") as handle:
        mapping = {row["source_id"]: row for row in csv.DictReader(handle)}
    bib_keys = set(BIB_KEY.findall(BIB_PATH.read_text(encoding="utf-8")))
    ordered = first_citation_order()
    if set(ordered) != set(FORMATTED):
        raise SystemExit("正文来源顺序与候选集合不一致：" + ", ".join(ordered))
    rows = []
    for number, source_id in enumerate(ordered, start=1):
        source = mapping.get(source_id)
        if not source or source["can_enter_formal_candidate_list"] != "yes":
            raise SystemExit(f"{source_id} 不在允许候选参考文献清单中")
        if source["bib_key"] not in bib_keys:
            raise SystemExit(f"{source_id} 缺少 BibTeX 键 {source['bib_key']}")
        rows.append({
            "reference_number": number,
            "source_id": source_id,
            "bib_key": source["bib_key"],
            "first_citation_order": number,
            "gbt_7714_candidate_entry": FORMATTED[source_id],
            "allowed_use": source["allowed_use"],
            "blocked_use": source["blocked_use"],
            "remaining_verification": source["format_or_verification_gap"],
        })
    with OUTPUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    lines = [
        "# 参考文献（候选工作稿）",
        "",
        f"> 本清单按华东师范大学公开格式基线的GB/T 7714-2015组织，仅列入当前{len(rows)}项已阅读、可限边界引用来源。它不是最终参考文献表：学校基线要求硕士论文参考文献不少于30篇且含外文文献；SOLO-002、部分国内物理竞赛研究和其余方法文献仍待完整阅读、页码或格式核验，暂不得加入。",
        "",
    ]
    lines.extend(f"[{row['reference_number']}] {row['gbt_7714_candidate_entry']}" for row in rows)
    lines.extend([
        "",
        "## 使用边界",
        "",
        "每条来源的可支持主张、禁止外推及版本/页码缺口见 `09_quality/r01_candidate_references_mapping_v1.csv`。正文中的来源ID占位须在最终定稿前按首次引用顺序转换为编号制引文，并与学校当期学院规范再次核对。",
    ])
    OUTPUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"候选参考文献通过：{len(rows)} 项，按正文首次引用顺序编号。")


if __name__ == "__main__":
    main()
