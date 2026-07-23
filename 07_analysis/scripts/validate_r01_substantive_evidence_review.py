from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def path(value: str) -> Path:
    p = Path(value)
    return p if p.is_absolute() else ROOT / p

def compact(value: str) -> str:
    return re.sub(r"\s+", "", value or "")

def main() -> None:
    parser = argparse.ArgumentParser(description="验证R01 58条实质证据审查回填。")
    parser.add_argument("--input", required=True)
    parser.add_argument("--template", default="07_analysis/data/rater_returns/templates/R01/r01_substantive_evidence_review_template_v1.csv")
    parser.add_argument("--qa-output", required=True)
    args = parser.parse_args()
    with path(args.input).open(encoding="utf-8-sig", newline="") as h: rows = list(csv.DictReader(h))
    with path(args.template).open(encoding="utf-8-sig", newline="") as h: template = list(csv.DictReader(h))
    keys = ("item_id", "dimension")
    same_keys = [tuple(r[k] for k in keys) for r in rows] == [tuple(r[k] for k in keys) for r in template]
    complete = all(all(r[f].strip() for f in ("substantive_reviewer_id","substantive_review_date","source_rechecked","evidence_support_decision","support_explanation","recommended_present","recommended_level","recommended_decision","reviewer_statement")) for r in rows)
    valid_decision = all(r["evidence_support_decision"] in {"充分支持","需补充引文","不支持当前编码"} for r in rows)
    valid_source = all(r["source_rechecked"] == "是" for r in rows)
    present_logic = all((r["recommended_present"] == "否") == (r["recommended_level"] == "未出现") for r in rows)
    decision_logic = all((r["recommended_present"] == r["current_present"] and r["recommended_level"] == r["current_level"]) == (r["recommended_decision"] == "保持当前裁决") for r in rows)
    replacement_ok = all(r["evidence_support_decision"] != "需补充引文" or (r["replacement_solution_quote"].strip() and compact(r["replacement_solution_quote"]) in compact(path(r["item_text_path"]).read_text(encoding="utf-8"))) for r in rows)
    checks=[("记录数",len(rows),"58",len(rows)==58),("不可变键与模板同序","一致" if same_keys else "不一致","一致",same_keys),("工作字段完整","完整" if complete else "有空值","完整",complete),("来源复查","58/58" if valid_source else "存在非是","58/58",valid_source),("审查决定枚举","合法" if valid_decision else "非法","合法",valid_decision),("推荐存在性等级逻辑","合法" if present_logic else "非法","合法",present_logic),("保持或更正逻辑","合法" if decision_logic else "非法","合法",decision_logic),("替代引文定位","通过" if replacement_ok else "不通过","通过",replacement_ok)]
    with path(args.qa_output).open("w",encoding="utf-8-sig",newline="") as h:
        w=csv.DictWriter(h,fieldnames=["check_item","observed","expected","status"],lineterminator="\n");w.writeheader()
        for item,observed,expected,ok in checks:w.writerow({"check_item":item,"observed":observed,"expected":expected,"status":"通过" if ok else "不通过"})
    print(f"实质审查回填检查：{sum(ok for *_,ok in checks)}/{len(checks)}通过")

if __name__ == "__main__": main()
