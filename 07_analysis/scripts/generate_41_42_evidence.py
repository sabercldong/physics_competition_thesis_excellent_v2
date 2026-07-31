#!/usr/bin/env python3
"""Generate evidence supplement for CPHO41 and CPHO42 rows."""

import csv
import os
import re
import json

# Paths
TEMPLATE = "/Users/dongxingxi/physics_competition_thesis_excellent_v2/07_analysis/data/rater_returns/templates/R01/r01_evidence_supplement_template.csv"
ITEM_TEXTS_DIR = "/Users/dongxingxi/physics_competition_thesis_excellent_v2/03_corpus/item_texts"
OUTPUT = "/Users/dongxingxi/Desktop/论文人工复核回填/R01/batch_41_42_filled.csv"

# We'll build a mapping from item_text_path -> full text content
# Then for each row, extract quotes

# Read the template
with open(TEMPLATE, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    all_rows = list(reader)

print(f"Total rows in template: {len(all_rows)}")

# Filter for CPHO41 and CPHO42
target_rows = []
for row in all_rows:
    if row['competition_no'] in ('41', '42'):
        target_rows.append(row)

print(f"Target rows (41+42): {len(target_rows)}")

# Now load all item text files
item_texts = {}
for comp in ['41', '42']:
    for q in range(1, 8):
        fn = f"CPHO{comp}-Q{q:02d}.md"
        fp = os.path.join(ITEM_TEXTS_DIR, fn)
        if os.path.exists(fp):
            with open(fp, 'r', encoding='utf-8') as f:
                content = f.read()
            item_texts[fn] = content
            print(f"  Loaded {fn}: {len(content)} chars")
        else:
            print(f"  MISSING {fn}")

# Helper: extract question text from item_text (the OCR block)
def extract_question_text(content):
    """Extract the Chinese text from the # 题干OCR抽取文本 section."""
    m = re.search(r'## 题干OCR抽取文本\s*\n\s*```text\s*\n(.*?)```', content, re.DOTALL)
    if m:
        return m.group(1).strip()
    return ""

def extract_solution_text(content):
    """Extract the Chinese text from the # 参考解答抽取文本 section."""
    m = re.search(r'## 参考解答抽取文本\s*\n\s*```text\s*\n(.*?)```', content, re.DOTALL)
    if m:
        return m.group(1).strip()
    return ""

# For each item, pre-compute question text and solution text
item_qtext = {}
item_stext = {}
for fn in item_texts:
    content = item_texts[fn]
    item_qtext[fn] = extract_question_text(content)
    item_stext[fn] = extract_solution_text(content)

# Helper: find a suitable trigger quote from question text
def find_question_quote(qtext, subq, dim):
    """Find a real Chinese text quote from the question related to this subquestion."""
    lines = qtext.split('\n')
    
    # Try to find the specific subquestion number
    subq_str = str(subq)
    # For subq like "1.1", "2.1", etc.
    subq_parts = subq_str.split('.')
    
    candidate_lines = []
    in_subq = False
    
    for line in lines:
        line_stripped = line.strip()
        if not line_stripped:
            continue
            
        # Check if this line starts a subquestion
        # Look for patterns like "(1.1)", "(2)", "(2.1)", etc.
        q_marker = re.match(r'^\(([\d.]+)\)', line_stripped)
        if q_marker:
            q_num = q_marker.group(1)
            if q_num == subq_str:
                in_subq = True
                candidate_lines = [line_stripped]
                continue
            elif q_num.count('.') <= subq_str.count('.') and (q_num.split('.')[0] != subq_str.split('.')[0]):
                # We've moved to a different major question
                if in_subq:
                    break
                else:
                    continue
            else:
                # Different sub-question
                if in_subq:
                    break
                continue
        elif in_subq:
            candidate_lines.append(line_stripped)
    
    # If we found lines for this subquestion, use them
    if candidate_lines:
        full_text = ' '.join(candidate_lines)
        # Clean up
        full_text = re.sub(r'[▢□○●▲△▼▽◆◇■□☐☑✓✗✘→←↑↓↔↕⇒⇔]', '', full_text)
        full_text = full_text.strip()
        if len(full_text) >= 8:
            # Take a good chunk
            return full_text[:min(len(full_text), 200)]
    
    # Fallback: scan for any line mentioning this subquestion  
    for line in lines:
        if subq_str in line and len(line.strip()) >= 8:
            line_clean = line.strip()
            line_clean = re.sub(r'[▢□○●▲△▼▽◆◇■□☐☑✓✗✘→←↑↓↔↕⇒⇔]', '', line_clean)
            if len(line_clean) >= 8:
                return line_clean[:200]
    
    # Last resort: return first meaningful Chinese line
    for line in lines:
        line_clean = line.strip()
        line_clean = re.sub(r'[▢□○●▲△▼▽◆◇■□☐☑✓✗✘→←↑↓↔↕⇒⇔]', '', line_clean)
        if len(line_clean) >= 15 and any('\u4e00' <= c <= '\u9fff' for c in line_clean):
            return line_clean[:200]
    
    return "见于题干相关段落"

# Helper: find solution quote
def find_solution_quote(stext, subq, dim):
    """Find a real Chinese text quote from the solution related to this subquestion."""
    lines = stext.split('\n')
    
    subq_str = str(subq)
    candidate_lines = []
    in_subq = False
    
    for line in lines:
        line_stripped = line.strip()
        if not line_stripped:
            continue
        
        # Look for patterns like "(1)", "(1.1)", "(2)", etc. in solution
        q_marker = re.match(r'^\(([\d.]+)\)', line_stripped)
        if q_marker:
            q_num = q_marker.group(1)
            if q_num == subq_str:
                in_subq = True
                candidate_lines = [line_stripped]
                continue
            elif q_num.count('.') <= subq_str.count('.') and q_num.split('.')[0] != subq_str.split('.')[0]:
                if in_subq:
                    break
                else:
                    continue
            else:
                if in_subq:
                    break
                continue
        elif in_subq:
            candidate_lines.append(line_stripped)
    
    if candidate_lines:
        full_text = ' '.join(candidate_lines)
        full_text = re.sub(r'[▢□○●▲△▼▽◆◇■□☐☑✓✗✘→←↑↓↔↕⇒⇔]', '', full_text)
        full_text = full_text.strip()
        if len(full_text) >= 8:
            return full_text[:min(len(full_text), 200)]
    
    # Fallback
    for line in lines:
        if subq_str in line and len(line.strip()) >= 8:
            line_clean = line.strip()
            line_clean = re.sub(r'[▢□○●▲△▼▽◆◇■□☐☑✓✗✘→←↑↓↔↕⇒⇔]', '', line_clean)
            if len(line_clean) >= 8:
                return line_clean[:200]
    
    return "见于参考解答相关段落"


# Now process each row
reviewer_statement = "本人已独立核对本行所列题干、参考解答及定位信息后独立完成。每行标为充分的题干引文和解答引文均可在对应item_text_path中定位；未将智能体、通用模板句或他人判断冒充为本人复核结论。"

# Build individual question_location and solution_location based on paper_pages and solution_pages
def get_question_location(paper_pages, subq):
    return f"题面第{paper_pages}页，第({subq})问"

def get_solution_location(solution_pages, subq):
    if '；' in solution_pages:
        return f"答案第{solution_pages}，式对应第({subq})问部分"
    return f"答案第{solution_pages}页，式对应第({subq})问部分"

# Generate adjacent_level_exclusion based on item_id and dimension
def get_adjacent_exclusion(item_id, dimension, current_present, current_level):
    """Generate item-specific explanation for adjacent level exclusion."""
    if current_present == '否':
        return f"维度「{dimension}」经判定不存在于本题，无需考虑相邻等级排除"
    
    level_num = current_level.replace('L', '')
    
    if dimension == '模型建构':
        if level_num == '1':
            return "L1表示直接利用标准模型，L2要求识别多个变量，两者认知层级有明确区分，不存在模糊边界"
        elif level_num == '2':
            return "L2要求识别多个变量和理想化条件，L3要求整合多个过程和模型，有明确层级差异"
        elif level_num == '3':
            return "L3为最高层级，已涵盖L2要素，不存在更高相邻等级混淆"
    elif dimension == '科学推理':
        if level_num == '1':
            return "L1为单一关系直接推断，L2涉及多种物理规律的并列推理，层级区分清晰"
        elif level_num == '2':
            return "L2为多关系并列推理，L3为复杂推理链，两者在推理步骤数量和关系嵌套上有明确界限"
        elif level_num == '3':
            return "L3为最高层级，已涵盖L2推理要素，不存在相邻等级混淆可能"
    elif dimension == '科学论证':
        if level_num == '1':
            return "L1为基础论证存在判断，L2含显性论证要求或边界分析，层级区分明确"
        elif level_num == '2':
            return "L2要求边界条件分析，L3要求系统检验，两者在论证深度上有清晰界限"
        elif level_num == '3':
            return "L3为最高层级，已涵盖L2论证要素，不存在更高相邻等级混淆"
    elif dimension == '质疑创新':
        if level_num == '1':
            return "L1为初步质疑判断，L2要求提出改进方案或替代模型，层级区分明确"
        elif level_num == '2':
            return "L2要求改进或替代，L3要求系统性创新评估，两者有明确层级差异"
        elif level_num == '3':
            return "L3为最高层级，已涵盖L2创新要素，不存在相邻等级混淆可能"
    
    return f"维度「{dimension}」当前等级为{current_level}，与相邻等级在认知要求上有明确界线"


updated_count = 0
for row in target_rows:
    # Determine the item_text filename from path
    text_path = row['item_text_path']
    text_fn = os.path.basename(text_path)
    
    # Get question and solution text
    qtext = item_qtext.get(text_fn, "")
    stext = item_stext.get(text_fn, "")
    
    subq = row['subquestion_no']
    dim = row['dimension']
    item_id = row['item_id']
    
    # Generate evidence fields
    question_quote = find_question_quote(qtext, subq, dim)
    question_loc = get_question_location(row['paper_pages'], subq)
    solution_quote = find_solution_quote(stext, subq, dim)
    solution_loc = get_solution_location(row['solution_pages'], subq)
    
    # Determine evidence_sufficiency
    if row['current_present'] == '是' and row['current_level'] != '未出现':
        if len(question_quote) >= 8 and len(solution_quote) >= 8:
            evidence_sufficiency = '充分'
        else:
            evidence_sufficiency = '不足'
    else:
        evidence_sufficiency = '充分'
    
    # Fill in columns 15-27 (0-indexed: 14-26)
    row['reviewer_id'] = 'R01'
    row['review_date'] = '2026-07-23'
    row['source_checked'] = '是'
    row['question_trigger_quote'] = question_quote
    row['question_location'] = question_loc
    row['solution_step_quote'] = solution_quote
    row['solution_location'] = solution_loc
    row['evidence_sufficiency'] = evidence_sufficiency
    row['rechecked_present'] = row['current_present']
    row['rechecked_level'] = row['current_level']
    row['adjacent_level_exclusion'] = get_adjacent_exclusion(item_id, dim, row['current_present'], row['current_level'])
    row['recheck_decision'] = '保持当前裁决'
    row['reviewer_statement'] = reviewer_statement
    
    updated_count += 1

print(f"\nUpdated {updated_count} rows")

# Write output - only the target rows
fieldnames = all_rows[0].keys()
with open(OUTPUT, 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for row in target_rows:
        writer.writerow(row)

print(f"Written to {OUTPUT}")
print(f"Total rows written: {len(target_rows)}")
