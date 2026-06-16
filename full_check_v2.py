#!/usr/bin/env python3
"""
大B舅父萬題庫 — 全面檢查 & 自動修復 v2
正確處理所有數據格式（bilingual options_zh/options_en 等）
"""

import json, os, re, sys, shutil, copy, random
from collections import Counter
from pathlib import Path

BASE = Path(__file__).parent
REPORT = []
FIX_COUNT = 0
CHECK_COUNT = 0

def log(msg):
    REPORT.append(msg)
    print(msg)

def backup_and_write(filepath, data):
    global FIX_COUNT
    bak = filepath.with_suffix('.bak')
    if not bak.exists():
        shutil.copy2(filepath, bak)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    FIX_COUNT += 1

def get_question_text(q):
    """Get question text from any format."""
    for key in ['question', 'question_zh', 'question_en']:
        v = q.get(key, '')
        if v and isinstance(v, str) and v.strip():
            return v.strip()
    return ''

def get_options(q):
    """Get options list from any format (prefer zh, fallback en)."""
    for key in ['options', 'options_zh']:
        v = q.get(key, [])
        if isinstance(v, list) and len(v) > 0:
            return key, v
    return 'options_en', q.get('options_en', [])

def set_options(q, key, new_opts):
    """Set options for the given key."""
    q[key] = new_opts

def safe_strip_prefix(opt):
    """Remove A./B./C./D. prefix but protect false positives like J.K. Rowling."""
    if not isinstance(opt, str):
        return opt
    m = re.match(r'^([A-D])([\.\)])\s+(.+)', opt, re.DOTALL)
    if m:
        rest = m.group(3)
        if re.match(r'^[A-Z]\.', rest):
            return opt  # J.K. Rowling pattern
        return rest
    return opt

def check_and_fix_json(filepath):
    """Check and fix a single JSON file."""
    global CHECK_COUNT
    rel = filepath.relative_to(BASE)
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        log(f"\n📄 {rel}")
        log(f"  ❌ JSON 解析失敗: {e}")
        return
    except Exception as e:
        log(f"\n📄 {rel}")
        log(f"  ❌ 讀取失敗: {e}")
        return
    
    if not isinstance(data, list) or len(data) == 0:
        return
    
    n = len(data)
    CHECK_COUNT += n
    issues = []
    modified = False
    
    # Determine option keys present
    sample = data[0]
    has_opts_zh = 'options_zh' in sample
    has_opts_en = 'options_en' in sample
    has_opts = 'options' in sample
    
    to_remove = set()
    seen_questions = set()
    
    for i, q in enumerate(data):
        pfx = f"  [{i+1}/{n}]"
        
        # ── Check: question not empty ──
        q_text = get_question_text(q)
        if not q_text:
            issues.append(f"{pfx} ❌ question 為空")
            to_remove.add(i)
            continue
        
        # ── Check: duplicate question ──
        q_key = q_text[:300].lower()
        if q_key in seen_questions:
            issues.append(f"{pfx} ❌ 重複題目")
            to_remove.add(i)
            continue
        seen_questions.add(q_key)
        
        # ── Check options (check ALL option fields) ──
        for opt_key in ['options', 'options_zh', 'options_en']:
            if opt_key not in q:
                continue
            opts = q[opt_key]
            if not isinstance(opts, list):
                issues.append(f"{pfx} ❌ {opt_key} 非陣列")
                to_remove.add(i)
                break
            if len(opts) < 2:
                issues.append(f"{pfx} ❌ {opt_key} 不足 2 個選項")
                to_remove.add(i)
                break
            
            # Check blank options
            for j, o in enumerate(opts):
                if not isinstance(o, str) or not o.strip():
                    issues.append(f"{pfx} ❌ {opt_key}[{j}] 空白")
                    to_remove.add(i)
                    break
            
            if i in to_remove:
                break
            
            # Check duplicate options within question
            stripped = [o.strip().lower() for o in opts if isinstance(o, str)]
            if len(stripped) != len(set(stripped)):
                issues.append(f"{pfx} ❌ {opt_key} 有重複選項")
                # Deduplicate
                seen = set()
                new_opts = []
                old_answer = q.get('answer', 0)
                for j, o in enumerate(opts):
                    key = o.strip().lower() if isinstance(o, str) else ''
                    if key and key in seen:
                        continue
                    seen.add(key)
                    new_opts.append(o)
                if len(new_opts) >= 2:
                    q[opt_key] = new_opts
                    modified = True
                else:
                    to_remove.add(i)
                    break
            
            # Check letter prefix (only on first opt_key to avoid double-counting)
            if opt_key in ('options', 'options_zh'):
                prefix_found = False
                for j, o in enumerate(opts):
                    if isinstance(o, str) and re.match(r'^[A-D][\.\)]\s', o):
                        # Check false positive
                        rest = re.sub(r'^[A-D][\.\)]\s+', '', o)
                        if not re.match(r'^[A-Z]\.', rest):
                            prefix_found = True
                            break
                if prefix_found:
                    for opt_k in ['options', 'options_zh', 'options_en']:
                        if opt_k in q:
                            for j, o in enumerate(q[opt_k]):
                                if isinstance(o, str):
                                    new_o = safe_strip_prefix(o)
                                    if new_o != o:
                                        q[opt_k][j] = new_o
                                        modified = True
                    issues.append(f"{pfx} 🔧 移除選項字母前綴")
        
        if i in to_remove:
            continue
        
        # ── Check answer ──
        answer = q.get('answer')
        if not isinstance(answer, int):
            issues.append(f"{pfx} ❌ answer 非整數: {repr(answer)}")
            to_remove.add(i)
            continue
        
        # Get options for answer check
        _, opts = get_options(q)
        if answer < 0 or answer >= len(opts):
            issues.append(f"{pfx} ❌ answer 越界: {answer} (options={len(opts)})")
            to_remove.add(i)
            continue
    
    # ── Remove bad questions ──
    if to_remove:
        keep = [q for i, q in enumerate(data) if i not in to_remove]
        if len(keep) >= 1:
            data[:] = keep
            modified = True
            issues.append(f"  🔧 移除咗 {len(to_remove)} 條問題題目")
        else:
            issues.append(f"  ❌ 全部 {n} 條都有問題，唔改動")
    
    # ── Answer distribution check ──
    if len(data) >= 20:
        _, sample_opts = get_options(data[0])
        n_opts = len(sample_opts)
        answer_counter = Counter(q.get('answer', 0) for q in data)
        total = len(data)
        for idx, count in answer_counter.items():
            pct = count / total * 100
            if pct > 50:
                issues.append(f"  ⚠️ 答案分佈不均：index {idx} 佔 {pct:.1f}%（{count}/{total}）")
    
    # ── Report ──
    if issues:
        log(f"\n📄 {rel} ({n} 題)")
        for iss in issues:
            log(iss)
        if modified:
            backup_and_write(filepath, data)
            log(f"  💾 已保存修復")

def check_html(filepath):
    """Check HTML files for known issues."""
    rel = filepath.relative_to(BASE)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return
    
    issues = []
    
    # Check escaped quotes
    if "\\'\\'" in content:
        issues.append("  ❌ JS 語法錯誤：\\'\\'")
    
    # Check hardcoded shuffle
    if 'idx=[0,1,2,3]' in content or 'idx=[0, 1, 2, 3]' in content:
        issues.append("  ❌ shuffleOptions 硬編碼 idx=[0,1,2,3]")
        # Fix
        content = content.replace('idx=[0,1,2,3]', 'idx=Array.from({length:clean.length},(_,i)=>i)')
        content = content.replace('idx=[0, 1, 2, 3]', 'idx=Array.from({length:clean.length},(_,i)=>i)')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        issues.append("  🔧 已修復 shuffleOptions")
    
    if issues:
        log(f"\n📄 {rel}")
        for iss in issues:
            log(iss)

def main():
    log("=" * 60)
    log("大B舅父萬題庫 — 全面檢查 & 修復 v2")
    log("=" * 60)
    
    # Collect all JSON files
    json_files = []
    html_files = []
    for root, dirs, fnames in os.walk(BASE):
        rel = os.path.relpath(root, BASE)
        if rel.startswith(('.git', 'katex')):
            continue
        for f in fnames:
            fp = Path(root) / f
            if f.endswith('.json') and 'index.json' not in f and 'manifest.json' not in f and '.bak' not in f:
                json_files.append(fp)
            elif f.endswith('.html'):
                html_files.append(fp)
    
    json_files.sort()
    html_files.sort()
    
    log(f"\n📂 {len(json_files)} 個 JSON 檔案")
    for fp in json_files:
        check_and_fix_json(fp)
    
    log(f"\n📂 {len(html_files)} 個 HTML 檔案")
    for fp in html_files:
        check_html(fp)
    
    # Summary
    log("\n" + "=" * 60)
    log("📊 總結")
    log("=" * 60)
    log(f"  檢查題目：{CHECK_COUNT}")
    log(f"  修復計數：{FIX_COUNT}")
    log("=" * 60)
    
    report_path = BASE / "check_report_v2.txt"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(REPORT))
    log(f"\n📝 報告: {report_path}")

if __name__ == '__main__':
    main()
