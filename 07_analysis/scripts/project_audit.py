from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]

REQUIRED = {
    '03_corpus/paper_inventory.csv': ['competition_no','paper_source','source_grade','source_verified'] if False else ['competition_no','paper_source','source_grade'],
    '03_corpus/item_index.csv': ['item_id','competition_no','question_no','analysis_unit','source_verified'],
    '04_framework/pilot_coding.csv': ['item_id','coder','dimension','present','level','evidence'],
    '09_quality/claim_evidence_matrix.csv': ['claim_id','claim','evidence_level','status'],
}

def main():
    errors=[]
    for rel, cols in REQUIRED.items():
        path=ROOT/rel
        if not path.exists():
            errors.append(f'缺少文件: {rel}')
            continue
        df=pd.read_csv(path)
        missing=[c for c in cols if c not in df.columns]
        if missing:
            errors.append(f'{rel} 缺少字段: {missing}')
    if errors:
        print('\n'.join(errors))
        raise SystemExit(1)
    print('项目结构检查通过；这不代表研究证据已经充分。')

if __name__=='__main__':
    main()
