from pathlib import Path
import pandas as pd

ROOT=Path(__file__).resolve().parents[2]
INV=ROOT/'03_corpus/paper_inventory.csv'
IDX=ROOT/'03_corpus/item_index.csv'


def main():
    inv=pd.read_csv(INV)
    idx=pd.read_csv(IDX)
    problems=[]
    expected=set(range(35,43))
    observed=set(pd.to_numeric(inv['competition_no'],errors='coerce').dropna().astype(int))
    missing=expected-observed
    if missing:
        problems.append(f'缺少届次: {sorted(missing)}')
    if inv['competition_no'].duplicated().any():
        problems.append('paper_inventory中存在重复届次')
    if not idx.empty:
        if idx['item_id'].duplicated().any():
            problems.append('item_index中item_id重复')
        unverified=idx[idx['source_verified'].astype(str).str.lower().isin(['no','false','0','未核验'])]
        if len(unverified):
            problems.append(f'存在{len(unverified)}条未核验索引记录')
    if problems:
        print('语料库检查发现问题：')
        for p in problems: print('-',p)
        raise SystemExit(1)
    print('语料库结构检查通过。')

if __name__=='__main__':
    main()
