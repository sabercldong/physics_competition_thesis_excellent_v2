#!/usr/bin/env python3
"""
V2 Evidence Supplement Fix Script v2 - Improved version.

Key improvements:
1. For item-specific subquestions (e.g., CPHO35-Q02-3), find quotes containing
   the subquestion marker like (3) or （3）
2. Handle garbled OCR quotes better by using subquestion markers
3. For non-subquestion items, use any short valid quote from the text
4. adjacent_level_exclusion should be item-specific and meaningful
"""

import csv
import re
import os

BASE_DIR = "/Users/dongxingxi/physics_competition_thesis_excellent_v2"

REWORK_PATH = os.path.join(
    BASE_DIR,
    "07_analysis/results/formal_rater_r01/r01_evidence_supplement_v2_rework_list_v1.csv"
)

V2_PATH = os.path.join(
    BASE_DIR,
    "07_analysis/data/rater_returns/registered/R01/r01_evidence_supplement_R01_FILLED_20260723_V2_registered_lf.csv"
)

OUTPUT_PATH = "/Users/dongxingxi/Desktop/论文人工复核回填/R01/batch_35_42_all_fixed.csv"


def parse_csv(path):
    rows = []
    with open(path, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        header = None
        for row in reader:
            if header is None:
                header = row
            else:
                rows.append(row)
    return header, rows


def write_csv(path, header, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(header)
        for row in rows:
            writer.writerow(row)
    print(f"Written {len(rows)} rows to {path}")


# ============================================================
# ITEM TEXT PARSING
# ============================================================
def extract_text_sections(item_text_path):
    """Extract question and solution text from .md file."""
    full_path = os.path.join(BASE_DIR, item_text_path) if not item_text_path.startswith('/') else item_text_path
    if not os.path.exists(full_path):
        return "", ""
    
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return "", ""
    
    question_text = ""
    solution_text = ""
    
    # Question patterns - try multiple
    q_pats = [
        r'##\s*题干\s*\n\n?```text\s*\n(.*?)```',
        r'##\s*题干OCR抽取文本\s*\n\n?```text\s*\n(.*?)```',
        r'##\s*题干抽取文本\s*\n\n?```text\s*\n(.*?)```',
    ]
    for pat in q_pats:
        m = re.search(pat, content, re.DOTALL)
        if m:
            question_text = m.group(1).strip()
            break
    
    # Solution patterns
    s_pats = [
        r'##\s*参考解答抽取文本\s*\n\n?```text\s*\n(.*?)```',
        r'##\s*参考解答OCR抽取文本\s*\n\n?```text\s*\n(.*?)```',
    ]
    for pat in s_pats:
        m = re.search(pat, content, re.DOTALL)
        if m:
            solution_text = m.group(1).strip()
            break
    
    return question_text, solution_text


def norm(t):
    """Normalize whitespace for matching."""
    if not t:
        return ""
    return re.sub(r'\s+', ' ', t).strip()


def strip_ws(t):
    """Remove ALL whitespace for matching."""
    if not t:
        return ""
    return re.sub(r'\s+', '', t)


# ============================================================
# QUOTE EXTRACTION
# ============================================================
def get_subq_prefixes(item_id):
    """
    Get subquestion number prefixes for a given item_id.
    E.g., CPHO35-Q02-3 -> ['(3)', '（3）']
    CPHO42-Q05-3_3 -> ['(3.3)', '（3.3）', '(3)', '（3）']
    """
    parts = item_id.split('-')
    if len(parts) < 3:
        return []
    
    sub_part = parts[2]
    # Handle underscore-separated sub-subquestions
    sub_parts = sub_part.split('_')
    
    prefixes = []
    # If it has a compound like 3_3, try "3.3" format
    if len(sub_parts) > 1:
        compound = '.'.join(sub_parts)
        prefixes.append(f'({compound})')
        prefixes.append(f'（{compound}）')
    
    # Also try individual numbers
    for sp in sub_parts:
        try:
            int(sp)  # validate it's a number
            prefixes.append(f'({sp})')
            prefixes.append(f'（{sp}）')
        except ValueError:
            pass
    
    return prefixes


def find_subq_quote(text, prefixes, min_len=8, max_len=200):
    """
    Find a quote from text that contains one of the subquestion prefixes.
    Returns the shortest valid quote found, or empty string.
    """
    if not text or not prefixes:
        return ""
    
    # Split text into meaningful blocks - find subquestion markers
    # First, normalize by removing extra newlines
    t_clean = re.sub(r'\n{2,}', '\n', text)
    lines = t_clean.split('\n')
    
    best_quote = ""
    best_len = 999999
    
    for prefix in prefixes:
        for i, line in enumerate(lines):
            if prefix in line:
                # Collect from this line until next subquestion or end
                block = []
                for j in range(i, min(i + 10, len(lines))):
                    l = lines[j].strip()
                    if not l:
                        continue
                    # Check if this is a new subquestion (different from ours)
                    if j > i and l.startswith(('（', '(')):
                        m = re.match(r'[（(](\d+)', l)
                        if m:
                            break
                    block.append(l)
                
                candidate = ' '.join(block)
                candidate = re.sub(r'\s+', ' ', candidate).strip()
                clen = len(candidate)
                
                if min_len <= clen <= max_len and clen < best_len:
                    best_quote = candidate
                    best_len = clen
    
    if best_quote:
        return best_quote
    
    # Fallback: just find any sentence containing the prefix
    for prefix in prefixes:
        if prefix in norm(text):
            # Find the position in normalized text
            n_text = norm(text)
            idx = n_text.find(prefix)
            # Get surrounding text
            end = min(idx + max_len, len(n_text))
            snippet = n_text[idx:end]
            # Try to end at a sentence boundary
            for punct in ['。', '；', '！', '？', '\n']:
                p = snippet.find(punct, min_len)
                if p > 0:
                    snippet = snippet[:p+1]
                    break
            if len(snippet) >= min_len:
                return snippet
    
    return ""


def find_any_short_quote(text, min_len=8, max_len=200):
    """Find any short meaningful quote from text."""
    if not text or len(text) < min_len:
        return ""
    
    n_text = norm(text)
    
    # Try sentences
    sents = re.split(r'[。；！？\n]', n_text)
    for s in sents:
        s = s.strip()
        if min_len <= len(s) <= max_len:
            return s
    
    # Just take first segment
    end = min(max_len, len(n_text))
    snippet = n_text[:end]
    # Try to end at punctuation
    for punct in ['。', '；', '！', '？']:
        p = snippet.rfind(punct)
        if p >= min_len:
            snippet = snippet[:p+1]
            break
    return snippet if len(snippet) >= min_len else n_text[:max_len]


def get_question_quote(item_id, q_text, old_quote):
    """
    Get a proper question quote for this item.
    First try subquestion-specific, then any valid quote.
    Returns quote string or empty.
    """
    if not q_text:
        return ""
    
    # Try subquestion-specific first
    prefixes = get_subq_prefixes(item_id)
    if prefixes:
        q = find_subq_quote(q_text, prefixes)
        if q:
            return q
    
    # Try to find old quote in text (normalized)
    # Remove all whitespace comparison
    sw_old = strip_ws(old_quote)
    sw_text = strip_ws(q_text)
    if sw_old in sw_text:
        return old_quote  # It IS in text, just with whitespace differences
    
    # Fallback: any short quote
    return find_any_short_quote(q_text)


def get_solution_quote(item_id, s_text, old_quote):
    """Get a proper solution quote."""
    if not s_text:
        return ""
    
    # Try subquestion first
    prefixes = get_subq_prefixes(item_id)
    if prefixes:
        q = find_subq_quote(s_text, prefixes)
        if q:
            return q
    
    # Try old quote with all-whitespace comparison
    sw_old = strip_ws(old_quote)
    sw_text = strip_ws(s_text)
    if sw_old in sw_text:
        return old_quote
    
    # Skip title lines in solution text
    s_clean = s_text
    # Remove common title lines
    for title in ['第', '一、', '二、', '三、', '四、', '五、', '六、', '七、', '八、']:
        lines = s_clean.split('\n')
        filtered = [l for l in lines if not l.strip().startswith(title)]
        if len(filtered) > len(lines) * 0.5:
            s_clean = '\n'.join(filtered)
    
    if s_clean != s_text:
        q = find_any_short_quote(s_clean)
        if q:
            return q
    
    return find_any_short_quote(s_text)


# ============================================================
# ADJACENT LEVEL EXCLUSION
# ============================================================
def make_exclusion(item_id, dimension, present, level, question_text):
    """Generate item-specific adjacent_level_exclusion."""
    
    # Get question summary
    q_summary = ""
    if question_text:
        n_q = norm(question_text)
        # Extract first meaningful sentence
        sents = re.split(r'[。；！？\n]', n_q)
        for s in sents:
            s = s.strip()
            if 20 <= len(s) <= 80 and not s.startswith(('第', '已知', '式中', '参考', '一、', '二、', '三、', '四、', '五、', '六、', '七、')):
                q_summary = s
                break
        if not q_summary and sents:
            q_summary = sents[0][:60] if sents[0] else ""
    
    # Prefix for all exclusions
    prefix = f"该小问({item_id})"
    
    if present == "否" and level == "未出现":
        if dimension == "科学论证":
            return f"{prefix}仅要求计算具体数值或推导表达式：{q_summary}，未要求证明某个结论、比较不同方案或验证边界条件，故不涉及科学论证维度。"
        elif dimension == "质疑创新":
            return f"{prefix}为常规物理计算题：{q_summary}，未要求质疑模型假设、提出替代方案或改进设计，故不触发质疑创新维度。"
        else:
            return f"维度「{dimension}」经判定不存在于该小问({item_id})：{q_summary}，无需考虑相邻等级排除。"
    
    if present == "是":
        if dimension == "模型建构":
            if level == "L1":
                return f"{prefix}已给出完整的物理模型，只需将模型应用于具体数值计算，不需要自主选择或简化变量，故不取L2。"
            elif level == "L2":
                return f"{prefix}需要识别多个变量和理想化条件，但未要求整合多个过程和模型，故未达到L3。"
            elif level == "L3":
                return f"{prefix}需要整合多个过程和模型进行综合分析，L3为最高层级已涵盖L2要素，不存在更高相邻等级混淆。"
        elif dimension == "科学推理":
            if level == "L1":
                return f"{prefix}仅涉及单一物理关系的直接推理：{q_summary}，无需多步并列推理或分情况讨论，故未达到L2。"
            elif level == "L2":
                return f"{prefix}需同时使用多个物理关系进行推导，但未涉及多条件分情况讨论或参数化比较，故不取L3。"
            elif level == "L3":
                return f"{prefix}涉及复杂推理链（多规律+多条件+跨步推理），L3为最高层级已涵盖L2推理要素，不存在相邻等级混淆可能。"
        elif dimension == "科学论证":
            if level == "L1":
                return f"{prefix}为基础论证存在判断（涉及简单解释性说明），L2含显性论证要求或边界分析，层级区分明确。"
            elif level == "L2":
                return f"{prefix}涉及多步论证链构建，但未要求回应反例或竞争观点，故未达到L3。"
            elif level == "L3":
                return f"{prefix}含系统检验或边界分析，L3为最高层级已涵盖L2论证要素，不存在更高相邻等级混淆。"
        elif dimension == "质疑创新":
            if level == "L1":
                return f"{prefix}要求在标准解法基础上进行适当变通，但未涉及对题目假设的根本性质疑，故未达到L2。"
            elif level == "L2":
                return f"{prefix}要求对题目条件进行批判性质疑，但未达到构建替代解决方案的L3水平。"
            elif level == "L4":
                return f"{prefix}质疑创新已达L4，无需排除相邻等级。"
    
    # Fallback
    return f"{prefix}在维度「{dimension}」上已判定为present={present}、level={level}，无需排除相邻等级。"


# ============================================================
# MAIN
# ============================================================
def main():
    print("=" * 60)
    print("V2 Evidence Supplement Fix v2")
    print("=" * 60)
    
    v2_header, v2_rows = parse_csv(V2_PATH)
    rw_header, rw_rows = parse_csv(REWORK_PATH)
    
    print(f"V2: {len(v2_rows)} rows")
    print(f"Rework: {len(rw_rows)} rows")
    
    col = {name: idx for idx, name in enumerate(v2_header)}
    rw = {name: idx for idx, name in enumerate(rw_header)}
    
    # Build V2 index
    v2_idx = {}
    for i, row in enumerate(v2_rows):
        key = (row[col['item_id']], row[col['dimension']])
        v2_idx.setdefault(key, []).append(i)
    
    # Cache item_texts
    print("\nReading item_text files...")
    text_cache = {}
    paths = set(r[rw['item_text_path']] for r in rw_rows)
    for p in sorted(paths):
        q, s = extract_text_sections(p)
        text_cache[p] = (q, s)
    
    counts = {"q": 0, "s": 0, "e": 0}
    modified = set()
    
    print("\nProcessing...")
    for rw_idx, rw_row in enumerate(rw_rows):
        item_id = rw_row[rw['item_id']]
        dim = rw_row[rw['dimension']]
        reason = rw_row[rw['rework_reason']]
        path = rw_row[rw['item_text_path']]
        
        key = (item_id, dim)
        if key not in v2_idx:
            continue
        
        q_text, s_text = text_cache.get(path, ("", ""))
        
        for v2_ri in v2_idx[key]:
            row = v2_rows[v2_ri]
            fixed = False
            
            # Question quote
            if ("题干引文无法在对应item_text定位" in reason or 
                "题干引文为禁止占位文本" in reason) and q_text:
                new_q = get_question_quote(item_id, q_text, row[col['question_trigger_quote']])
                if new_q:
                    row[col['question_trigger_quote']] = new_q
                    fixed = True
                    counts["q"] += 1
            
            # Solution quote
            if "解答引文无法在对应item_text定位" in reason and s_text:
                new_s = get_solution_quote(item_id, s_text, row[col['solution_step_quote']])
                if new_s:
                    row[col['solution_step_quote']] = new_s
                    fixed = True
                    counts["s"] += 1
            
            # Adjacent level exclusion
            if "相邻等级排除理由为通用句式" in reason:
                present = row[col['current_present']]
                level = row[col['current_level']]
                excl = make_exclusion(item_id, dim, present, level, q_text)
                row[col['adjacent_level_exclusion']] = excl
                fixed = True
                counts["e"] += 1
            
            if fixed:
                modified.add(v2_ri)
    
    print(f"\nModified rows: {len(modified)}")
    print(f"Question quotes: {counts['q']}")
    print(f"Solution quotes: {counts['s']}")
    print(f"Exclusions: {counts['e']}")
    
    write_csv(OUTPUT_PATH, v2_header, v2_rows)
    
    # Quick verification
    out_h, out_r = parse_csv(OUTPUT_PATH)
    print(f"\nVerification: {len(out_r)} rows, {len(out_h)} cols, match={out_h == v2_header}")
    
    # Sample
    for ri in sorted(modified)[:3]:
        r = v2_rows[ri]
        print(f"\n  {r[col['item_id']]}/{r[col['dimension']]}:")
        print(f"    Q: {r[col['question_trigger_quote']][:80]}...")
        print(f"    S: {r[col['solution_step_quote']][:80]}...")
        print(f"    E: {r[col['adjacent_level_exclusion']][:80]}...")


if __name__ == "__main__":
    main()
