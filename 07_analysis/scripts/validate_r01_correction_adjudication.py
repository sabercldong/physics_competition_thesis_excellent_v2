from __future__ import annotations

import argparse, csv
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
def resolve(v:str)->Path:
 p=Path(v); return p if p.is_absolute() else ROOT/p
def main()->None:
 p=argparse.ArgumentParser(description='验证R01四条编码更正裁决回填。');p.add_argument('--input',required=True);p.add_argument('--template',default='07_analysis/data/rater_returns/templates/R01/r01_correction_adjudication_template_v1.csv');p.add_argument('--qa-output',required=True);a=p.parse_args()
 with resolve(a.input).open(encoding='utf-8-sig',newline='') as h:r=list(csv.DictReader(h))
 with resolve(a.template).open(encoding='utf-8-sig',newline='') as h:t=list(csv.DictReader(h))
 keys=[(x['item_id'],x['dimension']) for x in r]==[(x['item_id'],x['dimension']) for x in t]
 fields=('adjudicator_id','adjudication_date','adjudication_decision','final_present','final_level','adjudication_reason','adjudicator_statement')
 complete=all(all(x[f].strip() for f in fields) for x in r)
 decision=all(x['adjudication_decision'] in {'采纳建议','不采纳建议','另行裁决'} for x in r)
 logic=all((x['final_present']=='否')==(x['final_level']=='未出现') for x in r)
 relation=all((x['adjudication_decision']=='采纳建议')==(x['final_present']==x['recommended_present'] and x['final_level']==x['recommended_level']) for x in r)
 checks=[('记录数',len(r),'4',len(r)==4),('不可变键与模板同序','一致' if keys else '不一致','一致',keys),('工作字段完整','完整' if complete else '有空值','完整',complete),('裁决决定枚举','合法' if decision else '非法','合法',decision),('最终存在性等级逻辑','合法' if logic else '非法','合法',logic),('采纳建议关系','合法' if relation else '非法','合法',relation)]
 with resolve(a.qa_output).open('w',encoding='utf-8-sig',newline='') as h:
  w=csv.DictWriter(h,fieldnames=['check_item','observed','expected','status'],lineterminator='\n');w.writeheader()
  for i,o,e,ok in checks:w.writerow({'check_item':i,'observed':o,'expected':e,'status':'通过' if ok else '不通过'})
 print(f"更正裁决回填检查：{sum(x[-1] for x in checks)}/{len(checks)}通过")
if __name__=='__main__':main()
