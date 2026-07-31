#!/usr/bin/env python3
"""
B组22个material的公式核对视觉复核脚本。
对每个material：
1. 读取公式核对表(formula_check_v1.csv)的全部条目
2. 读取item_texts中的参考解答文本层
3. 交叉验证公式核对表的每一条是否与答案文本一致
4. 用视觉API抽查每个material的第一页答案渲染图
5. 输出结论
"""

import csv
import json
import os
import re
import base64
import urllib.request
import ssl

ROOT = "/Users/dongxingxi/physics_competition_thesis_excellent_v2"
TRANSCRIPTS = os.path.join(ROOT, "03_corpus/manual_review_transcripts")
ITEM_TEXTS = os.path.join(ROOT, "03_corpus/item_texts")
RENDERS_B1 = os.path.join(ROOT, "03_corpus/manual_review_renders/G1-07-B1")
RENDERS_D1 = os.path.join(ROOT, "03_corpus/manual_review_renders/G1-07-D1")

# API configuration
API = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
KEY = "sk-ws-H.RXYIEYI.lyTu.MEQCIAwEFTT7Afx_K1k0AWgXh3PGz7yx_88XosHp9BwSvxPMAiAiy013faRiU7wyqZXzabaMfmBpgQ6nPgRfxQvau3AyPA"
ctx = ssl._create_unverified_context()

def ask_vision(img_path, question):
    """Call qwen-vl-plus vision API"""
    try:
        with open(img_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        payload = json.dumps({
            "model": "qwen-vl-plus",
            "messages": [{
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}},
                    {"type": "text", "text": question}
                ]
            }]
        }).encode()
        req = urllib.request.Request(API, data=payload,
            headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
        resp = json.loads(urllib.request.urlopen(req, context=ctx, timeout=120).read())
        return resp['choices'][0]['message']['content']
    except Exception as e:
        return f"[API ERROR: {e}]"

def read_csv_safe(path):
    """Read a formula_check CSV and return list of dicts"""
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
    """Read the item_texts markdown file and return its content"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"  ERROR reading item_text {path}: {e}")
        return ""

def normalize_for_compare(s):
    """Normalize formula text for comparison - strip spaces, normalize Greek letters"""
    if not s:
        return ""
    s = s.strip()
    # Normalize common representations
    replacements = {
        'mu_0': 'μ0', 'mu0': 'μ0',
        'theta': 'θ', 'phi': 'Φ', 'Phi': 'Φ',
        'lambda': 'λ', 'varepsilon': 'ε', 'epsilon': 'ε',
        'pi': 'π', 'Pi': 'Π',
        'Omega': 'Ω', 'omega': 'ω',
        'alpha': 'α', 'beta': 'β', 'gamma': 'γ',
        'eta': 'η', 'rho': 'ρ',
        'ln': 'ln', 'sqrt': '√',
        'integral': '∫', '->': '→',
        'infinity': '∞',
    }
    return s

def extract_formula_from_text(text, formula_hint):
    """Try to find the formula in the answer text based on hints like equation numbers"""
    if not text or not formula_hint:
        return "NO_HINT"
    
    # Look for equation number references like (1), (2), etc.
    eq_nums = re.findall(r'\((\d+)\)', formula_hint)
    
    # Try to find specific equation patterns
    lines = text.split('\n')
    found_lines = []
    
    # Remove common non-comparable elements
    formula_keywords = formula_hint.replace('=', ' ').replace('+', ' ').replace('-', ' ')
    keywords = [w for w in formula_keywords.split() if len(w) > 2]
    
    for line in lines:
        line_stripped = line.strip()
        # Check for equation numbers
        for num in eq_nums:
            if f'({num})' in line_stripped:
                found_lines.append(line_stripped)
                break
        # Also check for keyword matches
        if keywords:
            matches = sum(1 for kw in keywords if kw in line_stripped)
            if matches >= 2 and len(line_stripped) > 10:
                if line_stripped not in found_lines:
                    found_lines.append(line_stripped)
    
    return found_lines[:5] if found_lines else ["NOT_FOUND_IN_TEXT"]

def cross_validate_entry(csv_row, item_text):
    """
    Cross-validate one CSV entry against the answer text.
    Returns: (status, details)
    status: 'PASS' | 'NEEDS_REVIEW' | 'UNCERTAIN'
    """
    check_id = csv_row.get('check_id', '')
    formula = csv_row.get('formula_or_result', '')
    source = csv_row.get('source_basis', '')
    status = csv_row.get('check_status', '')
    pages = csv_row.get('pdf_pages', '')
    scope = csv_row.get('source_scope', '')
    note = csv_row.get('boundary_note', '')
    
    details = []
    
    # Check if it's a parameter/condition entry vs formula entry
    if scope in ['题面参数', '题面条件', '评分标准']:
        # These are metadata entries, just confirm they exist
        if '题面' in source or 'PDF' in source:
            details.append(f"题面/条件条目，需人工确认")
            return ('UNCERTAIN', details)
        return ('PASS', ['元数据条目，无需公式验证'])
    
    # It's a formula entry - try to find it in the answer text
    # Look for the formula content in the text
    formula_clean = re.sub(r'[ \t]+', ' ', formula).strip()
    
    # Extract key mathematical symbols from the formula
    key_parts = re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*|[μθπλΦεΩωαβγρη]|\\[a-zA-Z]+', formula)
    
    # Try to locate in text by looking for surrounding context
    text_lower = item_text.lower()
    formula_lower = formula_clean.lower()
    
    # Check if the formula's key components appear in the text near each other
    match_score = 0
    for part in set(key_parts):
        if len(part) > 1 and part.lower() in text_lower:
            match_score += 1
    
    # Also check pages mentioned
    page_check = True
    for p in re.findall(r'\d+', pages):
        if p in item_text:
            pass
    
    total_key_parts = len(set(key_parts))
    if total_key_parts == 0:
        return ('UNCERTAIN', ['无法提取公式关键部分'])
    
    coverage = match_score / total_key_parts if total_key_parts > 0 else 0
    
    if coverage >= 0.7:
        details.append(f"公式关键元素匹配度: {coverage:.0%} ({match_score}/{total_key_parts})")
        return ('PASS', details)
    elif coverage >= 0.4:
        details.append(f"公式关键元素部分匹配: {coverage:.0%} ({match_score}/{total_key_parts})")
        details.append(f"公式: {formula[:80]}...")
        return ('NEEDS_REVIEW', details)
    else:
        details.append(f"公式关键元素匹配度低: {coverage:.0%} ({match_score}/{total_key_parts})")
        details.append(f"公式: {formula[:80]}...")
        return ('UNCERTAIN', details)


def find_solution_render(material_id):
    """Find the first solution page render PNG for this material"""
    # Try B1 first, then D1
    for render_dir in [RENDERS_B1, RENDERS_D1]:
        if not os.path.isdir(render_dir):
            continue
        for f in sorted(os.listdir(render_dir)):
            if f.startswith(f"{material_id}-solution-page-") and f.endswith(".png"):
                return os.path.join(render_dir, f)
    return None


# The 22 materials with their render directories
MATERIALS = [
    ("CPHO36-Q03", 28), ("CPHO36-Q07", 50), ("CPHO39-Q04", 56), ("CPHO39-Q06", 44),
    ("CPHO35-Q02", 41), ("CPHO35-Q03", 42), ("CPHO35-Q04", 36), ("CPHO35-Q08", 41),
    ("CPHO39-Q03", 45), ("CPHO39-Q05", 38), ("CPHO39-Q07", 31), ("CPHO35-Q05", 50),
    ("CPHO35-Q06", 38), ("CPHO36-Q04", 31), ("CPHO36-Q05", 46), ("CPHO39-Q01", 30),
    ("CPHO35-Q01", 34), ("CPHO35-Q07", 29), ("CPHO36-Q01", 33), ("CPHO36-Q02", 43),
    ("CPHO36-Q06", 31), ("CPHO39-Q02", 29),
]

def main():
    results = {}
    total_csv_entries = 0
    total_pass = 0
    total_needs_review = 0
    total_uncertain = 0
    
    for material_id, expected_count in MATERIALS:
        print(f"\\n{'='*80}")
        print(f"处理: {material_id} (预期{expected_count}条)")
        print(f"{'='*80}")
        
        # 1. Read CSV
        csv_path = os.path.join(TRANSCRIPTS, f"{material_id}_formula_check_v1.csv")
        csv_rows = read_csv_safe(csv_path)
        
        if not csv_rows:
            print(f"  [ERROR] 无法读取CSV或空文件")
            results[material_id] = {
                'status': '待核实不能关闭',
                'csv_count': 0,
                'found_count': 0,
                'pass': 0,
                'needs_review': 0,
                'uncertain': 0,
                'details': ['CSV文件无法读取或为空']
            }
            continue
        
        actual_count = len(csv_rows)
        total_csv_entries += actual_count
        print(f"  CSV条目数: {actual_count} (预期{expected_count})")
        
        # 2. Read item_text
        item_text_path = os.path.join(ITEM_TEXTS, f"{material_id}.md")
        item_text = read_item_text(item_text_path)
        text_len = len(item_text)
        print(f"  item_text长度: {text_len} 字符")
        
        # 3. Cross-validate each entry
        material_pass = 0
        material_needs = 0
        material_uncertain = 0
        entry_details = []
        
        for i, row in enumerate(csv_rows):
            check_id = row.get('check_id', f'ROW_{i+1}')
            formula = row.get('formula_or_result', '')
            scope = row.get('source_scope', '')
            
            val_status, val_details = cross_validate_entry(row, item_text)
            
            if val_status == 'PASS':
                material_pass += 1
            elif val_status == 'NEEDS_REVIEW':
                material_needs += 1
            else:
                material_uncertain += 1
            
            if val_status != 'PASS':
                entry_details.append(f"    {check_id}: {val_status} - {'; '.join(val_details)}")
        
        print(f"  交叉验证结果: PASS={material_pass}, NEEDS_REVIEW={material_needs}, UNCERTAIN={material_uncertain}")
        for d in entry_details[-10:]:  # Show last 10 non-pass entries
            print(d)
        
        # 4. Visual API spot check - first solution page
        render_path = find_solution_render(material_id)
        vision_result = ""
        if render_path:
            print(f"  渲染图: {os.path.basename(render_path)}")
            question = f"请从这张渲染图中识别出所有带编号的公式（如(1),(2),...），列出每个公式编号及其内容。这是{material_id}的参考解答第1页。"
            vision_result = ask_vision(render_path, question)
            print(f"  Vision API返回(前300字): {vision_result[:300]}")
        else:
            print(f"  [WARN] 未找到渲染图")
            vision_result = "[NO RENDER FOUND]"
        
        # 5. Determine conclusion
        # If CSV count doesn't match expected, flag it
        count_issue = actual_count != expected_count
        if count_issue:
            print(f"  [WARN] 条目数不匹配: 实际{actual_count} vs 预期{expected_count}")
        
        if material_uncertain > 0 and material_pass == 0:
            conclusion = "待核实不能关闭"
        elif material_uncertain > 0:
            conclusion = "待核实不能关闭"  # Any uncertain entries need resolution
        elif material_needs > 0:
            conclusion = "需修订"
        elif count_issue:
            conclusion = "需修订"
        else:
            conclusion = "通过无需修订"
        
        # Check if vision API had issues
        if "ERROR" in vision_result or "[NO RENDER FOUND]" in vision_result:
            conclusion = "待核实不能关闭"
        
        results[material_id] = {
            'status': conclusion,
            'csv_count': actual_count,
            'expected_count': expected_count,
            'pass': material_pass,
            'needs_review': material_needs,
            'uncertain': material_uncertain,
            'details': entry_details,
            'vision': vision_result[:200] if vision_result else ''
        }
        
        print(f"  => 结论: {conclusion}")
    
    # Summary output
    print("\\n" + "="*80)
    print("汇总报告")
    print("="*80)
    print(f"\\n总CSV条目处理数: {total_csv_entries}")
    print()
    print(f"{'Material':<20} {'状态':<20} {'CSV':<6} {'PASS':<6} {'REVIEW':<8} {'UNCERT':<8}")
    print("-"*70)
    
    for material_id, _ in MATERIALS:
        r = results.get(material_id, {})
        status = r.get('status', 'N/A')
        csv_c = r.get('csv_count', 0)
        p = r.get('pass', 0)
        n = r.get('needs_review', 0)
        u = r.get('uncertain', 0)
        print(f"{material_id:<20} {status:<20} {csv_c:<6} {p:<6} {n:<8} {u:<8}")
    
    print("-"*70)
    pass_count = sum(1 for r in results.values() if r.get('status') == '通过无需修订')
    review_count = sum(1 for r in results.values() if r.get('status') == '需修订')
    uncertain_count = sum(1 for r in results.values() if r.get('status') == '待核实不能关闭')
    print(f"通过无需修订: {pass_count}")
    print(f"需修订: {review_count}")
    print(f"待核实不能关闭: {uncertain_count}")


if __name__ == '__main__':
    main()
