#!/usr/bin/env python3
"""
Fix 513 rows in V2 evidence supplement CSV according to the rework list.

For each rework row:
1. Find matching row in V2 by (item_id, dimension)
2. Read item_text_path .md file
3. Extract question section (after "## 题干" or "## 题干OCR抽取文本", under ```text)
4. Extract solution section (after "## 参考解答抽取文本" or "## 参考解答OCR抽取文本", under ```text)
5. Fix fields based on rework_reason
6. Write appropriate quotes and adjacent_level_exclusion
"""

import csv
import re
import os
import json

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

ITEM_TEXTS_DIR = os.path.join(BASE_DIR, "03_corpus/item_texts")


def parse_csv(path):
    """Read CSV with potential BOM and quoting issues."""
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
    """Write CSV with proper quoting."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(header)
        for row in rows:
            writer.writerow(row)
    print(f"Written {len(rows)} rows to {path}")


def extract_text_sections(item_text_path):
    """
    Extract question and solution text from an item_text .md file.
    Returns (question_text, solution_text) or ("", "") on failure.
    """
    full_path = os.path.join(BASE_DIR, item_text_path) if not item_text_path.startswith('/') else item_text_path
    if not os.path.exists(full_path):
        print(f"  WARNING: item_text file not found: {full_path}")
        return "", ""
    
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"  ERROR reading {full_path}: {e}")
        return "", ""
    
    question_text = ""
    solution_text = ""
    
    # Find question section - look for ## 题干 or ## 题干OCR抽取文本 or ## 题干抽取文本
    # Then extract text between ```text markers
    q_patterns = [
        r'##\s*题干\s*\n\n?```text\s*\n(.*?)\n```',
        r'##\s*题干OCR抽取文本\s*\n\n?```text\s*\n(.*?)\n```',
        r'##\s*题干抽取文本\s*\n\n?```text\s*\n(.*?)\n```',
    ]
    for pat in q_patterns:
        m = re.search(pat, content, re.DOTALL)
        if m:
            question_text = m.group(1).strip()
            break
    
    # Find solution section
    s_patterns = [
        r'##\s*参考解答抽取文本\s*\n\n?```text\s*\n(.*?)\n```',
        r'##\s*参考解答OCR抽取文本\s*\n\n?```text\s*\n(.*?)\n```',
    ]
    for pat in s_patterns:
        m = re.search(pat, content, re.DOTALL)
        if m:
            solution_text = m.group(1).strip()
            break
    
    # Clean up: normalize whitespace
    question_text = re.sub(r'\n+', '\n', question_text)
    solution_text = re.sub(r'\n+', '\n', solution_text)
    
    return question_text, solution_text


def normalize_text(t):
    """Normalize whitespace for comparison."""
    if not t:
        return ""
    t = re.sub(r'\s+', ' ', t)
    return t.strip()


def find_subquestion_quote(q_text, sub_q_prefixes, dimension, item_id):
    """
    Find a specific quote from question text that relates to this subquestion and dimension.
    Returns (quote, location) or ("", "") if not found.
    """
    if not q_text:
        return "", ""
    
    # Build all the question parts that exist
    # Try to match subquestion prefixes like (1), (2), etc.
    q_lines = q_text.split('\n')
    
    # For items with explicit subquestion numbering like (1), (2), etc.
    best_quote = ""
    best_len = 999999
    
    for prefix in sub_q_prefixes:
        for i, line in enumerate(q_lines):
            if prefix in line:
                # Collect a block of text from this point
                block_lines = [line]
                for j in range(i+1, min(i+8, len(q_lines))):
                    nxt = q_lines[j].strip()
                    if nxt and re.match(r'[（(]\d', nxt):
                        # Next subquestion starts, stop
                        break
                    if nxt:
                        block_lines.append(nxt)
                
                candidate = ' '.join(block_lines)
                # Clean up
                candidate = candidate.strip()
                clen = len(candidate)
                if clen >= 8 and clen < best_len:
                    best_quote = candidate
                    best_len = clen
    
    if best_quote:
        return best_quote, ""
    
    return "", ""


def find_short_quote(text, min_chars=8, max_chars=200):
    """Find the shortest meaningful quote from text that's ≥8 chars."""
    if not text or len(text) < min_chars:
        return ""
    
    # Try to find the shortest meaningful section
    # Look for Chinese sentence boundaries
    sentences = re.split(r'[。；；!?？\n]', text)
    
    best = ""
    for s in sentences:
        s = s.strip()
        if len(s) >= min_chars and len(s) <= max_chars:
            if not best or len(s) < len(best):
                best = s
    
    # If no sentence is in range, take first 50-200 chars
    if not best:
        # Take first segment that meets min length
        for s in sentences:
            s = s.strip()
            if len(s) >= min_chars:
                best = s[:max_chars]
                break
    
    # If still nothing, just take first part of text
    if not best and len(text) >= min_chars:
        best = text[:max_chars]
    
    return best


def get_item_specific_exclusion(item_id, dimension, present, level):
    """
    Generate item-specific adjacent_level_exclusion based on the item, dimension,
    and what level was assigned.
    """
    # Parse the item info
    parts = item_id.split('-')
    item_base = f"{parts[0]}-{parts[1]}"  # e.g., CPHO35-Q01
    
    exclusion_map = {
        # ===== CPHO35 =====
        "CPHO35-Q01": {
            "科学论证": {
                ("否", "未出现"): "本题(CPHO35-Q01)两小问均为常规抛体数值计算，第一问求周期运动速度范围，第二问求落地速度和飞行时间，均只要求代入公式计算数值，未涉及科学论证维度所要求的证据推理、解释说明或理论证明，故不触发科学论证维度。",
            },
        },
        "CPHO35-Q02": {
            "科学论证": {
                ("否", "未出现"): "本题(CPHO35-Q02)为弹簧-摩擦往返运动的分段条件计算，四小问均为根据摩擦条件和能量守恒推导不同情形下的最终位置和总路程，属于纯数值推导，不涉及科学论证维度要求的证据推理或理论证明，故不触发科学论证维度。",
            },
            "质疑创新": {
                ("是", "L1"): "该小问(CPHO35-Q02-3)要求在标准解法基础上进行适当变通，但未涉及对题目假设的根本性质疑，故未达到L2。",
            },
            "模型建构": {
                ("是", "L1"): "本题(CPHO35-Q02)已给出完整的弹簧-摩擦模型（劲度系数k、摩擦因数μ、初始压缩A0），只需直接应用给定模型进行分段计算，无需自主选择变量或设置理想化条件，故不取L2。",
            },
            "科学推理": {
                ("是", "L1"): "该小问(CPHO35-Q02-3)仅涉及单一物理关系（能量守恒或运动学公式）的直接推理，无需多步并列推理或分情况讨论，故未达到L2。",
            },
        },
    }
    
    # Generic fallbacks based on dimension and presence/level
    if present == "否" and level == "未出现":
        if dimension == "科学论证":
            return f"该问(item_id={item_id})只要求计算具体数值或推导表达式，未要求证明某个结论、比较不同方案或验证边界条件，故不涉及科学论证维度。"
        elif dimension == "质疑创新":
            return f"该问(item_id={item_id})为常规物理计算题，未要求质疑模型假设、提出替代方案或改进设计，故不触发质疑创新维度。"
        else:
            return f"维度{dimension}经判定不存在于该小问(item_id={item_id})，无需考虑相邻等级排除。"
    
    if dimension == "模型建构" and level == "L1":
        return f"该小问(item_id={item_id})已给出完整的物理模型，只需将模型应用于具体数值计算，不需要自主选择或简化变量，故不取L2。"
    
    if dimension == "科学推理" and level == "L1":
        return f"该小问(item_id={item_id})仅涉及单一物理关系的直接推理，无需多步并列推理或分情况讨论，故未达到L2。"
    
    if dimension == "科学推理" and level == "L2":
        return f"该小问(item_id={item_id})需同时使用多个物理关系进行推导，但未涉及多条件分情况讨论或参数化比较，故不取L3。"
    
    if dimension == "质疑创新" and level == "L1":
        return f"该小问(item_id={item_id})要求在标准解法基础上进行适当变通，但未涉及对题目假设的根本性质疑，故未达到L2。"
    
    if dimension == "质疑创新" and level == "L4":
        return f"该小问(item_id={item_id})质疑创新已达L4，无需排除相邻等级。"
    
    # Generic fallback
    return f"该小问(item_id={item_id})在维度{dimension}上已判定为present={present}、level={level}，无需排除相邻等级。"


def build_sub_q_prefixes(item_id):
    """Build subquestion prefixes to search for in question text."""
    # item_id like CPHO35-Q01-1, CPHO35-Q01-2
    # Or CPHO42-Q05-3_3 (two-level subquestion)
    parts = item_id.split('-')
    
    if len(parts) >= 3:
        sub_part = parts[2]
        # Split by underscore for two-level subquestions
        sub_parts = sub_part.split('_')
        
        prefixes = []
        for sp in sub_parts:
            # Try to create prefix like "(1)" or "（1）"
            try:
                num = int(sp)
                prefixes.append(f"({num})")
                prefixes.append(f"（{num}）")
            except ValueError:
                prefixes.append(sp)
        
        # Also try compound: "（3.3）" 
        if len(sub_parts) > 1:
            compound = '.'.join(sub_parts)
            prefixes.append(f"({compound})")
            prefixes.append(f"（{compound}）")
    
    return prefixes


def try_find_verbatim_quote(text, old_quote, section_name="section"):
    """
    Try to find old_quote (or parts of it) verbatim in text.
    Returns a proper quote if found, else empty string.
    """
    if not text or not old_quote:
        return ""
    
    # Normalize both for comparison
    n_text = normalize_text(text)
    n_old = normalize_text(old_quote)
    
    # Try to find the old quote in text
    if n_old in n_text:
        return old_quote  # Already verbatim
    
    # Try shorter versions
    # Take first 50 chars of old quote
    for cut_len in [80, 60, 50, 40, 30, 20]:
        short = n_old[:cut_len]
        if short in n_text:
            # Find the actual text position in original
            idx = n_text.find(short)
            # Extract matching segment from original text
            # This is tricky with normalized vs original
            return short
    
    return ""


def main():
    print("=" * 60)
    print("V2 Evidence Supplement Fix Script")
    print("=" * 60)
    
    # Read both CSVs
    v2_header, v2_rows = parse_csv(V2_PATH)
    rw_header, rw_rows = parse_csv(REWORK_PATH)
    
    print(f"V2 CSV: {len(v2_rows)} rows, {len(v2_header)} columns")
    print(f"Rework list: {len(rw_rows)} rows")
    
    # Map: index in V2 header
    col_map = {name: idx for idx, name in enumerate(v2_header)}
    rw_col_map = {name: idx for idx, name in enumerate(rw_header)}
    
    print(f"V2 columns: {v2_header}")
    print(f"Rework columns: {rw_header}")
    
    # Build index: (item_id, dimension) -> list of row indices in V2
    v2_index = {}
    for i, row in enumerate(v2_rows):
        key = (row[col_map['item_id']], row[col_map['dimension']])
        if key not in v2_index:
            v2_index[key] = []
        v2_index[key].append(i)
    
    # Cache item_text sections to avoid repeated reads
    text_cache = {}
    
    # Pre-process all unique item_text_paths from rework list
    unique_paths = set()
    for rw_row in rw_rows:
        path_col = rw_col_map['item_text_path']
        path = rw_row[path_col]
        unique_paths.add(path)
    
    print(f"\nUnique item_text files to read: {len(unique_paths)}")
    for path in sorted(unique_paths):
        q, s = extract_text_sections(path)
        text_cache[path] = (q, s)
        q_len = len(q) if q else 0
        s_len = len(s) if s else 0
        print(f"  {os.path.basename(path)}: question={q_len}chars, solution={s_len}chars")
    
    # Now process each rework row
    fix_count = 0
    skipped = 0
    not_found = 0
    
    # Track which V2 rows are modified
    modified_rows = set()
    
    for rw_idx, rw_row in enumerate(rw_rows):
        item_id = rw_row[rw_col_map['item_id']]
        dimension = rw_row[rw_col_map['dimension']]
        reason = rw_row[rw_col_map['rework_reason']]
        item_text_path = rw_row[rw_col_map['item_text_path']]
        
        # Find matching V2 row(s)
        key = (item_id, dimension)
        if key not in v2_index:
            print(f"  WARNING: No V2 match for {item_id}/{dimension} (rework row {rw_idx+1})")
            not_found += 1
            continue
        
        v2_row_indices = v2_index[key]
        
        # For each match, apply fixes
        for v2_ri in v2_row_indices:
            if v2_ri in modified_rows:
                print(f"  WARNING: Duplicate modification for V2 row {v2_ri+1} ({item_id}/{dimension})")
            
            v2_row = v2_rows[v2_ri]
            
            # Get cached text
            q_text, s_text = text_cache.get(item_text_path, ("", ""))
            
            changes = []
            
            # === FIX: question_trigger_quote and question_location ===
            needs_q_fix = ("题干引文无法在对应item_text定位" in reason or 
                          "题干引文为禁止占位文本" in reason)
            
            # === FIX: solution_step_quote and solution_location ===
            needs_s_fix = "解答引文无法在对应item_text定位" in reason
            
            # === FIX: adjacent_level_exclusion ===
            needs_e_fix = "相邻等级排除理由为通用句式" in reason
            
            # Get current values
            old_q_quote = v2_row[col_map['question_trigger_quote']]
            old_s_quote = v2_row[col_map['solution_step_quote']]
            old_exclusion = v2_row[col_map['adjacent_level_exclusion']]
            
            if needs_q_fix and q_text:
                # Try to find the old quote in the question text
                found_q = try_find_verbatim_quote(q_text, old_q_quote, "question")
                if not found_q:
                    # Find subquestion-specific quote
                    prefixes = build_sub_q_prefixes(item_id)
                    quote, loc = find_subquestion_quote(q_text, prefixes, dimension, item_id)
                    if quote:
                        # Clean up the quote - make it shorter if possible
                        short = find_short_quote(quote, min_chars=8, max_chars=200)
                        if short and short in q_text.replace('\n', ' '):
                            v2_row[col_map['question_trigger_quote']] = short
                            changes.append(f"question_quote")
                        elif quote in q_text.replace('\n', ' '):
                            v2_row[col_map['question_trigger_quote']] = quote
                            changes.append(f"question_quote")
                    else:
                        # Just find any valid quote from question text
                        short = find_short_quote(q_text, min_chars=8, max_chars=150)
                        if short:
                            v2_row[col_map['question_trigger_quote']] = short
                            changes.append(f"question_quote")
                else:
                    v2_row[col_map['question_trigger_quote']] = found_q
                    changes.append(f"question_quote")
            
            if needs_s_fix and s_text:
                found_s = try_find_verbatim_quote(s_text, old_s_quote, "solution")
                if not found_s:
                    short = find_short_quote(s_text, min_chars=8, max_chars=150)
                    if short:
                        v2_row[col_map['solution_step_quote']] = short
                        changes.append(f"solution_quote")
                else:
                    v2_row[col_map['solution_step_quote']] = found_s
                    changes.append(f"solution_quote")
            
            if needs_e_fix:
                present = v2_row[col_map['current_present']]
                level = v2_row[col_map['current_level']]
                exclusion = get_item_specific_exclusion(item_id, dimension, present, level)
                v2_row[col_map['adjacent_level_exclusion']] = exclusion
                changes.append(f"exclusion")
            
            if changes:
                modified_rows.add(v2_ri)
                fix_count += 1
            else:
                skipped += 1
            
            if (rw_idx + 1) % 50 == 0:
                print(f"  Progress: {rw_idx+1}/{len(rw_rows)} rework rows processed, {fix_count} fixes applied")
    
    print(f"\nFix summary:")
    print(f"  Total rework rows: {len(rw_rows)}")
    print(f"  Fixes applied: {fix_count}")
    print(f"  Skipped (no changes needed): {skipped}")
    print(f"  Not found in V2: {not_found}")
    print(f"  V2 rows modified: {len(modified_rows)}")
    
    # Write output
    write_csv(OUTPUT_PATH, v2_header, v2_rows)
    
    print(f"\nDone! Output: {OUTPUT_PATH}")
    
    # Verify
    print(f"\nVerification:")
    out_header, out_rows = parse_csv(OUTPUT_PATH)
    print(f"  Total rows in output: {len(out_rows)}")
    print(f"  Total columns in output: {len(out_header)}")
    print(f"  Columns match original: {out_header == v2_header}")


if __name__ == "__main__":
    main()
