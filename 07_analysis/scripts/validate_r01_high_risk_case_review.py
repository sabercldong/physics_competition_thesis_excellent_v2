from __future__ import annotations

import argparse
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def resolve(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path

def main() -> None:
    parser = argparse.ArgumentParser(description="验证R01 16条高风险案例实质审查回填。")
    parser.add_argument("--input", required=True)
    parser.add_argument("--template", default="07_analysis/data/rater_returns/templates/R01/r01_high_risk_case_review_template_v1.csv")
    parser.add_argument("--qa-output", required=True)
    args = parser.parse_args()
    with resolve(args.input).open(encoding="utf-8-sig", newline="") as h: rows=list(csv.DictReader(h))
    with resolve(args.template).open(encoding="utf-8-sig", newline="") as h: template=list(csv.DictReader(h))
    same_keys=[(r['item_id'],r['dimension']) for r in rows]==[(r['item_id'],r['dimension']) for r in template]
    fields=('case_reviewer_id','case_review_date','source_rechecked','evidence_support_decision','support_explanation','recommended_present','recommended_level','recommended_decision','reviewer_statement')
    complete=all(all(r[f].strip() for f in fields) for r in rows)
    valid=all(r['evidence_support_decision'] in {'充分支持','需补充引文','不支持当前编码'} and r['source_rechecked']=='是' for r in rows)
    level=all((r['recommended_present']=='否')==(r['recommended_level']=='未出现') for r in rows)
    decision=all((r['recommended_present']==r['current_present'] and r['recommended_level']==r['current_level'])==(r['recommended_decision']=='保持当前裁决') for r in rows)
    checks=[('记录数',len(rows),'16',len(rows)==16),('不可变键与模板同序','一致' if same_keys else '不一致','一致',same_keys),('工作字段完整','完整' if complete else '有空值','完整',complete),('决定与来源枚举','合法' if valid else '非法','合法',valid),('推荐存在性等级逻辑','合法' if level else '非法','合法',level),('保持或更正逻辑','合法' if decision else '非法','合法',decision)]
    with resolve(args.qa_output).open('w',encoding='utf-8-sig',newline='') as h:
        w=csv.DictWriter(h,fieldnames=['check_item','observed','expected','status'],lineterminator='\n');w.writeheader()
        for item,observed,expected,ok in checks:w.writerow({'check_item':item,'observed':observed,'expected':expected,'status':'通过' if ok else '不通过'})
    print(f"高风险案例回填检查：{sum(ok for *_,ok in checks)}/{len(checks)}通过")

if __name__ == '__main__': main()
