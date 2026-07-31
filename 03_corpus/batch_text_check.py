#!/usr/bin/env python3
"""
B组22个material的公式核对 - 文本交叉验证部分 (无API调用)
先做所有文本交叉验证，再单独做视觉抽查
"""

import csv
import os
import re

ROOT = "/Users/dongxingxi/physics_competition_thesis_excellent_v2"
TRANSCRIPTS = os.path.join(ROOT, "03_corpus/manual_review_transcripts")
ITEM_TEXTS = os.path.join(ROOT, "03_corpus/item_texts")

MATERIALS = [
    ("CPHO36-Q03", 28), ("CPHO36-Q07", 50), ("CPHO39-Q04", 56), ("CPHO39-Q06", 44),
    ("CPHO35-Q02", 41), ("CPHO35-Q03", 42), ("CPHO35-Q04", 36), ("CPHO35-Q08", 41),
    ("CPHO39-Q03", 45), ("CPHO39-Q05", 38), ("CPHO39-Q07", 31), ("CPHO35-Q05", 50),
    ("CPHO35-Q06", 38), ("CPHO36-Q04", 31), ("CPHO36-Q05", 46), ("CPHO39-Q01", 30),
    ("CPHO35-Q01", 34), ("CPHO35-Q07", 29), ("CPHO36-Q01", 33), ("CPHO36-Q02", 43),
    ("CPHO36-Q06", 31), ("CPHO39-Q02", 29),
]

def read_csv_safe(path):
    results = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                results.append(row)
    except Exception as e:
        print(f"  ERROR reading CSV {path}: {e}")
    return results

def read_item_text(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return ""

def extract_reference_section(text):
    """Extract the 参考解答 section (after '参考解答' marker)"""
    # Find the reference solution section
    idx = text.find('参考解答:')
    if idx == -1:
        idx = text.find('参考解答')
    if idx != -1:
        return text[idx:]
    return text

def extract_equation(text, eq_num):
    """
    Try to find equation with given number in the answer text.
    Returns the line containing the equation.
    """
    lines = text.split('\n')
    for i, line in enumerate(lines):
        # Match patterns like "(1)", "(1)4分", "(1)2分" etc.
        if re.search(rf'\({eq_num}\)', line):
            # Return this line and surrounding context
            start = max(0, i-1)
            end = min(len(lines), i+3)
            return '\n'.join(lines[start:end])
    return None

def find_key_formulas_in_text(text):
    """
    Find all equations with their numbers in the answer text.
    Returns dict of {eq_num: equation_text}
    """
    equations = {}
    lines = text.split('\n')
    
    current_eq = None
    current_text = []
    
    for i, line in enumerate(lines):
        # Look for equation numbers
        eq_match = re.search(r'\((\d+)\)', line)
        if eq_match:
            num = int(eq_match.group(1))
            # Check if there's a score annotation like "4分" after the number
            score_match = re.search(rf'\({num}\)(\d*分?)', line)
            
            # Collect the equation text (up to 3 lines before for multi-line formulas)
            context_start = max(0, i-3)
            eq_text_lines = []
            for j in range(context_start, i+1):
                eq_text_lines.append(lines[j].strip())
            
            # Also include the next line if it's part of the formula
            if i+1 < len(lines) and lines[i+1].strip() and not re.search(r'\((\d+)\)', lines[i+1]):
                eq_text_lines.append(lines[i+1].strip())
            if i+2 < len(lines) and lines[i+2].strip() and not re.search(r'\((\d+)\)', lines[i+2]):
                eq_text_lines.append(lines[i+2].strip())
                
            equations[num] = ' '.join(eq_text_lines)
            current_eq = num
            current_text = [line.strip()]
        elif current_eq is not None and line.strip():
            # Check if this continuation line has its own equation number
            if re.search(r'\(\d+\)', line):
                current_eq = None
                current_text = []
            else:
                current_text.append(line.strip())
    
    return equations

def cross_validate_entry(csv_row, item_text, eq_dict):
    """Cross-validate one CSV entry against the answer text with equation lookup"""
    check_id = csv_row.get('check_id', '')
    formula = csv_row.get('formula_or_result', '').strip()
    source = csv_row.get('source_basis', '')
    scope = csv_row.get('source_scope', '')
    pages = csv_row.get('pdf_pages', '')
    note = csv_row.get('boundary_note', '')
    
    details = []
    
    # Try to extract equation number from source_basis
    eq_nums = re.findall(r'\((\d+)\)', source)
    
    # For metadata entries (parameter/condition/scoring)
    if scope in ['题面参数', '题面条件', '评分标准']:
        return ('PASS', ['元数据/题面条目'])
    
    # For formula entries - try to find matching equation(s)
    if eq_nums:
        found_any = False
        for eq_num in eq_nums:
            eq_num = int(eq_num)
            if eq_num in eq_dict:
                eq_text = eq_dict[eq_num]
                # Check if the formula key parts appear in the equation text
                formula_clean = re.sub(r'[\s]+', '', formula)
                eq_clean = re.sub(r'[\s]+', '', eq_text)
                
                # Extract key tokens from formula
                formula_tokens = set(re.findall(r'[a-zA-ZµθπλΦεΩωαβγρη0-9\\]+', formula))
                eq_tokens = set(re.findall(r'[a-zA-ZµθπλΦεΩωαβγρη0-9\\]+', eq_text))
                
                if formula_tokens:
                    overlap = formula_tokens & eq_tokens
                    ratio = len(overlap) / len(formula_tokens)
                    if ratio >= 0.5:
                        found_any = True
                        details.append(f"式({eq_num})匹配度: {ratio:.0%}")
                    else:
                        details.append(f"式({eq_num})部分匹配: {ratio:.0%} (公式关键元素: {formula_tokens - eq_tokens})")
                else:
                    details.append(f"式({eq_num})存在但无法解析token")
            else:
                details.append(f"式({eq_num})在文本中未找到")
        
        if found_any:
            return ('PASS', details)
        elif any('部分匹配' in d for d in details):
            return ('NEEDS_REVIEW', details)
        else:
            return ('UNCERTAIN', details)
    
    # If no equation numbers in source, try generic formula matching
    # Extract key symbols
    key_symbols = set(re.findall(r'[a-zA-ZµθπλΦεΩωαβγρη_{}]+', formula))
    if len(key_symbols) < 2:
        return ('UNCERTAIN', ['公式符号太少，无法可靠匹配'])
    
    # Check how many symbols appear in the answer text
    text_upper = item_text.upper()
    found_symbols = sum(1 for s in key_symbols if s.upper() in text_upper)
    ratio = found_symbols / len(key_symbols) if key_symbols else 0
    
    if ratio >= 0.7:
        return ('PASS', [f"符号匹配度: {ratio:.0%} ({found_symbols}/{len(key_symbols)})"])
    elif ratio >= 0.4:
        return ('NEEDS_REVIEW', [f"符号部分匹配: {ratio:.0%} ({found_symbols}/{len(key_symbols)})"])
    else:
        return ('UNCERTAIN', [f"符号低匹配: {ratio:.0%} ({found_symbols}/{len(key_symbols)})"])

def main():
    total_csv = 0
    total_pass = 0
    total_needs = 0
    total_uncertain = 0
    all_results = {}
    
    for material_id, expected_count in MATERIALS:
        print(f"\n{'='*70}")
        print(f"【{material_id}】 (预期{expected_count}条)")
        print('='*70)
        
        # Read CSV
        csv_path = os.path.join(TRANSCRIPTS, f"{material_id}_formula_check_v1.csv")
        csv_rows = read_csv_safe(csv_path)
        
        if not csv_rows:
            print(f"  [ERROR] 无法读取CSV")
            all_results[material_id] = {'status': '待核实不能关闭', 'detail': 'CSV读取失败'}
            continue
        
        actual_count = len(csv_rows)
        total_csv += actual_count
        print(f"  CSV条目: {actual_count}")
        
        # Read item_text and extract equations
        item_text_path = os.path.join(ITEM_TEXTS, f"{material_id}.md")
        item_text = read_item_text(item_text_path)
        ref_text = extract_reference_section(item_text)
        eq_dict = find_key_formulas_in_text(ref_text)
        
        print(f"  文中发现编号公式: {sorted(eq_dict.keys())}")
        print(f"  参考解答文本长度: {len(ref_text)} chars")
        
        # Cross-validate
        mat_pass = 0
        mat_needs = 0
        mat_uncertain = 0
        issues = []
        
        for i, row in enumerate(csv_rows):
            check_id = row.get('check_id', f'ROW_{i+1}')
            formula = row.get('formula_or_result', '')
            scope = row.get('source_scope', '')
            
            val_status, val_details = cross_validate_entry(row, ref_text, eq_dict)
            
            if val_status == 'PASS':
                mat_pass += 1
            elif val_status == 'NEEDS_REVIEW':
                mat_needs += 1
                issues.append(f"    {check_id} [{scope}]: {'; '.join(val_details)}")
            else:
                mat_uncertain += 1
                issues.append(f"    {check_id} [{scope}]: {'; '.join(val_details)}")
        
        total_pass += mat_pass
        total_needs += mat_needs
        total_uncertain += mat_uncertain
        
        print(f"  结果: PASS={mat_pass}, NEEDS_REVIEW={mat_needs}, UNCERTAIN={mat_uncertain}")
        
        if issues:
            print(f"  需关注条目 ({len(issues)}):")
            for iss in issues[:8]:
                print(iss)
            if len(issues) > 8:
                print(f"    ... 还有 {len(issues)-8} 条")
        
        # Determine conclusion
        if mat_uncertain > 0:
            conclusion = "待核实不能关闭"
        elif mat_needs > 0:
            conclusion = "需修订"
        elif actual_count != expected_count:
            conclusion = "需修订"
        else:
            conclusion = "通过无需修订"
        
        # Check for specific issues from note field
        has_special_issues = False
        for row in csv_rows:
            note = row.get('boundary_note', '')
            if '待最终复核' in note or '待人工确认' in note:
                pass  # This is the default status, not a reason to flag
            if '疑似' in note or '需以原PDF' in note or '编号' in note:
                has_special_issues = True
        
        if has_special_issues and conclusion == '通过无需修订':
            conclusion = "需修订"
        
        all_results[material_id] = {
            'status': conclusion,
            'count': actual_count,
            'expected': expected_count,
            'pass': mat_pass,
            'needs': mat_needs,
            'uncertain': mat_uncertain,
            'issues': issues[:5],
            'eq_nums': sorted(eq_dict.keys())
        }
        
        # Show first few equations found
        first_eqs = list(eq_dict.items())[:3]
        for num, text in first_eqs:
            print(f"    式({num}): {text[:100]}...")
        
        print(f"  => 结论: {conclusion}")
    
    # Summary
    print('\n' + '='*70)
    print('汇总报告')
    print('='*70)
    print(f'总CSV条目: {total_csv}')
    print(f'总PASS: {total_pass}')
    print(f'总NEEDS_REVIEW: {total_needs}')
    print(f'总UNCERTAIN: {total_uncertain}')
    print()
    print(f'{"Material":<20} {"状态":<20} {"CSV":<6} {"PASS":<6} {"REV":<6} {"UNC":<6}')
    print('-'*65)
    
    final_pass = 0
    final_review = 0
    final_uncertain = 0
    
    for mid, _ in MATERIALS:
        r = all_results.get(mid, {})
        s = r.get('status', 'N/A')
        print(f'{mid:<20} {s:<20} {r.get("count",0):<6} {r.get("pass",0):<6} {r.get("needs",0):<6} {r.get("uncertain",0):<6}')
        if s == '通过无需修订':
            final_pass += 1
        elif s == '需修订':
            final_review += 1
        else:
            final_uncertain += 1
    
    print('-'*65)
    print(f'通过无需修订: {final_pass}')
    print(f'需修订: {final_review}')
    print(f'待核实不能关闭: {final_uncertain}')
    
    return all_results

if __name__ == '__main__':
    results = main()
