#!/usr/bin/env python3
"""
大B舅父萬題庫 — 自動修復腳本
基於 full_check.py 發現嘅問題，逐一修復。
"""

import json, os, re, sys, shutil
from collections import Counter
from pathlib import Path

BASE = Path(__file__).parent
FIX_LOG = []

def log(msg):
    FIX_LOG.append(msg)
    print(msg)

def backup_and_write(filepath, data):
    bak = filepath.with_suffix('.bak2')
    if not bak.exists():
        shutil.copy2(filepath, bak)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def safe_strip_prefix(opt):
    """Remove A./B./C./D. prefix but ONLY if it's clearly an answer label prefix.
    Don't strip legitimate text like 'J.K. Rowling' or 'A-Team'.
    """
    if not isinstance(opt, str):
        return opt
    # Only strip if: starts with single uppercase letter + period/space, 
    # AND the next char after prefix is NOT uppercase (to avoid J.K. Rowling)
    m = re.match(r'^([A-D])([\.\)])\s+(.+)', opt)
    if m:
        rest = m.group(3)
        # Don't strip if rest starts with uppercase followed by period (like K. Rowling)
        if re.match(r'^[A-Z]\.', rest):
            return opt
        return rest
    # Also handle "A. " without space after
    m = re.match(r'^([A-D])([\.\)])\s*$', opt)
    if m:
        return opt  # just the letter, leave it
    return opt

def fix_option_prefixes(filepath, data):
    """Fix letter prefixes on options (A. B. C. D.) but protect false positives."""
    fixed = 0
    for i, q in enumerate(data):
        if 'options' not in q:
            continue
        for j, opt in enumerate(q['options']):
            if not isinstance(opt, str):
                continue
            new_opt = safe_strip_prefix(opt)
            if new_opt != opt:
                q['options'][j] = new_opt
                fixed += 1
    if fixed > 0:
        log(f"  🔧 OPTION_PREFIX: 修復咗 {fixed} 個選項前綴")
        backup_and_write(filepath, data)
    return fixed

def fix_empty_options(filepath, data):
    """Remove blank options and adjust answer index."""
    fixed = 0
    removed_questions = 0
    new_data = []
    
    for i, q in enumerate(data):
        if 'options' not in q or 'answer' not in q:
            new_data.append(q)
            continue
        
        opts = q['options']
        answer = q['answer']
        
        # Check for blank options
        has_blank = any(not isinstance(o, str) or not o.strip() for o in opts)
        if not has_blank:
            new_data.append(q)
            continue
        
        # Build mapping: old index -> new index (only for non-blank options)
        valid_indices = [j for j, o in enumerate(opts) if isinstance(o, str) and o.strip()]
        
        if len(valid_indices) < 2:
            removed_questions += 1
            continue
        
        # Find new answer index
        if answer in valid_indices:
            new_answer = valid_indices.index(answer)
        else:
            # Answer was pointing to a blank option — can't determine correct answer
            removed_questions += 1
            continue
        
        q['options'] = [opts[j] for j in valid_indices]
        q['answer'] = new_answer
        new_data.append(q)
        fixed += 1
    
    if removed_questions > 0 or fixed > 0:
        log(f"  🔧 EMPTY_OPTIONS: 修復咗 {fixed} 條，移除咗 {removed_questions} 條無法修復嘅")
        data.clear()
        data.extend(new_data)
        backup_and_write(filepath, data)
    return fixed + removed_questions

def fix_duplicates(filepath, data):
    """Remove duplicate questions (keep first occurrence)."""
    seen = set()
    to_keep = []
    dup_count = 0
    
    for i, q in enumerate(data):
        q_text = q.get('question', '').strip()
        if not q_text:
            dup_count += 1
            continue
        # Normalize for comparison
        key = q_text[:300].lower()
        if key in seen:
            dup_count += 1
            continue
        seen.add(key)
        to_keep.append(q)
    
    if dup_count > 0:
        log(f"  🔧 DUPLICATES: 移除咗 {dup_count} 條重複題目")
        data.clear()
        data.extend(to_keep)
        backup_and_write(filepath, data)
    return dup_count

def fix_missing_answers(filepath, data):
    """Remove questions with missing/invalid answer field."""
    to_keep = []
    removed = 0
    
    for q in data:
        answer = q.get('answer')
        if answer is None or not isinstance(answer, int):
            removed += 1
            continue
        opts = q.get('options', [])
        if not isinstance(opts, list) or len(opts) < 2:
            removed += 1
            continue
        if answer < 0 or answer >= len(opts):
            removed += 1
            continue
        to_keep.append(q)
    
    if removed > 0:
        log(f"  🔧 MISSING_ANSWER: 移除咗 {removed} 條答案缺失/越界嘅題目")
        data.clear()
        data.extend(to_keep)
        backup_and_write(filepath, data)
    return removed

def fix_answer_distribution(filepath, data):
    """Redistribute answers for files where answer is always 0.
    Only fix if 90%+ answers are the same index AND there are shuffled versions available.
    """
    if len(data) < 20:
        return 0
    
    answer_counter = Counter(q.get('answer', 0) for q in data)
    total = len(data)
    
    # Find if any single answer index has > 90%
    for idx, count in answer_counter.items():
        pct = count / total * 100
        if pct > 90:
            # This file has severely imbalanced answers
            # We can't "fix" this by redistributing because we don't know the correct answers
            # Just report it
            log(f"  ⚠️ ANSWER_DIST: 答案 index {idx} 佔 {pct:.1f}%（需要人工檢查）")
            return 0
    return 0

def fix_json_parse_errors(filepath):
    """Try to fix JSON parse errors."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Common fixes
        # 1. Remove trailing commas before ] or }
        fixed = re.sub(r',\s*([}\]])', r'\1', content)
        # 2. Fix single quotes to double quotes (cautiously)
        # Only if it looks like the file uses single quotes
        if "'" in fixed and '"' not in fixed[:100]:
            fixed = fixed.replace("'", '"')
        
        try:
            data = json.loads(fixed)
            log(f"  🔧 JSON_PARSE: 修復成功（移除尾隨逗號）")
            backup_and_write(filepath, data)
            return True
        except:
            log(f"  ❌ JSON_PARSE: 無法自動修復")
            return False
    except Exception as e:
        log(f"  ❌ JSON_PARSE: 讀取失敗 - {e}")
        return False

def process_json_file(filepath):
    """Process a single JSON file with all fixes."""
    rel = filepath.relative_to(BASE)
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        log(f"\n📄 {rel}")
        log(f"  ❌ JSON 解析失敗，嘗試修復...")
        fix_json_parse_errors(filepath)
        return
    except Exception as e:
        log(f"\n📄 {rel}")
        log(f"  ❌ 讀取失敗: {e}")
        return
    
    if not isinstance(data, list) or len(data) == 0:
        return
    
    log(f"\n📄 {rel} ({len(data)} 題)")
    changes = 0
    
    # Fix 1: Missing/invalid answers
    c = fix_missing_answers(filepath, data)
    changes += c
    
    # Fix 2: Empty options
    c = fix_empty_options(filepath, data)
    changes += c
    
    # Fix 3: Duplicate questions
    c = fix_duplicates(filepath, data)
    changes += c
    
    # Fix 4: Option letter prefixes
    c = fix_option_prefixes(filepath, data)
    changes += c
    
    # Fix 5: Answer distribution (report only)
    fix_answer_distribution(filepath, data)
    
    if changes == 0:
        log(f"  ✅ 冇問題")

def fix_html_shuffle(filepath):
    """Fix hardcoded shuffleOptions in HTML files."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return False
    
    # Pattern: var idx=[0,1,2,3]; -> use clean.length dynamically
    # The correct shuffle should use: idx = Array.from({length: clean.length}, (_, i) => i)
    old_patterns = [
        'var idx=[0,1,2,3];',
        'var idx=[0, 1, 2, 3];',
        'idx=[0,1,2,3];',
        'idx=[0, 1, 2, 3];',
    ]
    
    modified = False
    for old in old_patterns:
        if old in content:
            new = 'var idx=Array.from({length:clean.length},(_,i)=>i);'
            content = content.replace(old, new)
            modified = True
    
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        log(f"  🔧 SHUFFLE: 修復硬編碼 idx=[0,1,2,3]")
        return True
    return False

def process_html_file(filepath):
    """Process HTML files for fixes."""
    rel = filepath.relative_to(BASE)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return
    
    has_issue = False
    if 'idx=[0,1,2,3]' in content or 'idx=[0, 1, 2, 3]' in content:
        has_issue = True
    
    if not has_issue:
        return
    
    log(f"\n📄 {rel}")
    fix_html_shuffle(filepath)

def main():
    log("=" * 60)
    log("大B舅父萬題庫 — 自動修復")
    log("=" * 60)
    
    # Process all JSON files
    json_files = []
    for root, dirs, fnames in os.walk(BASE):
        rel = os.path.relpath(root, BASE)
        if rel.startswith(('.git', 'katex')):
            continue
        for f in fnames:
            if f.endswith('.json') and f not in ('index.json', 'manifest.json'):
                json_files.append(Path(root) / f)
    
    json_files.sort()
    log(f"\n📂 處理 {len(json_files)} 個 JSON 檔案...")
    
    for fp in json_files:
        process_json_file(fp)
    
    # Process HTML files
    html_files = []
    for root, dirs, fnames in os.walk(BASE):
        rel = os.path.relpath(root, BASE)
        if rel.startswith(('.git', 'katex')):
            continue
        for f in fnames:
            if f.endswith('.html'):
                html_files.append(Path(root) / f)
    
    html_files.sort()
    log(f"\n📂 處理 {len(html_files)} 個 HTML 檔案...")
    
    for fp in html_files:
        process_html_file(fp)
    
    # Summary
    log("\n" + "=" * 60)
    log("修復完成！")
    log("=" * 60)
    
    # Save fix log
    log_path = BASE / "fix_report.txt"
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(FIX_LOG))
    log(f"\n📝 修復報告已保存到: {log_path}")

if __name__ == '__main__':
    main()
