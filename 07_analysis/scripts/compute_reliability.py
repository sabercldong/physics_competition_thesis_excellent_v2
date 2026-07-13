from pathlib import Path
import pandas as pd
from sklearn.metrics import cohen_kappa_score

ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT/'04_framework/pilot_coding.csv'
OUTPUT = ROOT/'07_analysis/results/generated/reliability_by_dimension.csv'


def main():
    df=pd.read_csv(INPUT)
    if df.empty:
        print('pilot_coding.csv 为空，未计算一致性。')
        return
    required={'item_id','coder','dimension','present','level'}
    missing=required-set(df.columns)
    if missing:
        raise ValueError(f'缺少字段: {sorted(missing)}')
    coders=df['coder'].dropna().unique().tolist()
    if len(coders)!=2:
        raise ValueError('当前脚本要求试编码数据恰好有两名评分者。')
    rows=[]
    for dim, sub in df.groupby('dimension'):
        wide_p=sub.pivot_table(index='item_id',columns='coder',values='present',aggfunc='first').dropna()
        if len(wide_p):
            k_present=cohen_kappa_score(wide_p[coders[0]],wide_p[coders[1]])
            agreement=(wide_p[coders[0]]==wide_p[coders[1]]).mean()
        else:
            k_present=float('nan'); agreement=float('nan')
        wide_l=sub.pivot_table(index='item_id',columns='coder',values='level',aggfunc='first').dropna()
        if len(wide_l):
            k_level=cohen_kappa_score(wide_l[coders[0]],wide_l[coders[1]],weights='quadratic')
        else:
            k_level=float('nan')
        rows.append({'dimension':dim,'n_present_pairs':len(wide_p),'raw_agreement':agreement,'kappa_present':k_present,'n_level_pairs':len(wide_l),'weighted_kappa_level':k_level})
    out=pd.DataFrame(rows)
    OUTPUT.parent.mkdir(parents=True,exist_ok=True)
    out.to_csv(OUTPUT,index=False,encoding='utf-8-sig')
    print(f'已生成 {OUTPUT}')

if __name__=='__main__':
    main()
