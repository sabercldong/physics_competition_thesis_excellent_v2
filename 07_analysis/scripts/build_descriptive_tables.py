from pathlib import Path
import pandas as pd

ROOT=Path(__file__).resolve().parents[2]
INPUT=ROOT/'07_analysis/data/final_coding.csv'
OUT=ROOT/'07_analysis/results/generated'


def main():
    if not INPUT.exists():
        print('尚无 final_coding.csv，未生成正式结果。')
        return
    df=pd.read_csv(INPUT)
    if df.empty:
        print('final_coding.csv 为空。')
        return
    OUT.mkdir(parents=True,exist_ok=True)
    # 每一行应为 item_id × dimension 的裁决后记录。
    presence=(df[df['present']==1].groupby('dimension')['item_id'].nunique().reset_index(name='items_present'))
    total=df['item_id'].nunique()
    presence['total_items']=total
    presence['proportion']=presence['items_present']/total if total else 0
    presence.to_csv(OUT/'dimension_presence.csv',index=False,encoding='utf-8-sig')
    levels=(df[df['present']==1].groupby(['dimension','level']).size().reset_index(name='count'))
    levels.to_csv(OUT/'dimension_levels.csv',index=False,encoding='utf-8-sig')
    print('已生成基础描述表。')

if __name__=='__main__':
    main()
