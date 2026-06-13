#!/usr/bin/env python3
"""Fix answer mismatches - improved version."""
import json, re, glob, os

base = '/Users/bruce/.openclaw/workspace/projects/project_03_bruce_institute_10000/uncle-bruce-10000'

def clean_opt(t):
    return re.sub(r'^[A-Da-d][.]\s*', '', t).strip()

def extract_expected(exp_zh, exp_en):
    for exp in [exp_zh, exp_en]:
        if not exp:
            continue
        m = re.search(r'(?:The correct answer is|correct answer is)\s*"?(.+?)"?\s*[.]?\s*$', exp)
        if m:
            return m.group(1).strip()
        m = re.search(r'(?:Answer)\s*:\s*(.+?)[.]?\s*$', exp)
        if m:
            return m.group(1).strip()
    return None

def normalize_answer(answer, opts):
    if isinstance(answer, int):
        return answer
    if isinstance(answer, str):
        if len(answer) == 1 and answer.upper() in 'ABCD':
            return ord(answer.upper()) - ord('A')
        for i, opt in enumerate(opts):
            if answer.strip().lower() in opt.lower():
                return i
    return 0

total_fixed = 0

for fpath in sorted(glob.glob(os.path.join(base, '**/questions.json'), recursive=True)):
    rel = os.path.relpath(fpath, base)
    with open(fpath, 'r', encoding='utf-8') as f:
        d = json.load(f)
    qs = d if isinstance(d, list) else d.get('questions', [])
    if not isinstance(qs, list):
        continue
    
    fixed = 0
    for q in qs:
        ans = normalize_answer(q.get('answer', 0), q.get('options_en', []) or q.get('options_zh', []))
        opts = q.get('options_en', []) or q.get('options_zh', [])
        exp = extract_expected(q.get('explanation_zh', ''), q.get('explanation_en', ''))
        if not opts or ans >= len(opts) or not exp:
            continue
        
        current = clean_opt(opts[ans]).lower()
        expected = clean_opt(exp).lower()
        
        if current == expected or expected in current or current in expected:
            continue
        
        found = -1
        for i, opt in enumerate(opts):
            oc = clean_opt(opt).lower()
            if oc == expected or expected in oc:
                found = i
                break
        
        if found >= 0 and found != ans:
            raw = q.get('answer', 0)
            if isinstance(raw, str) and len(raw) == 1 and raw.upper() in 'ABCD':
                q['answer'] = chr(ord('A') + found)
            else:
                q['answer'] = found
            fixed += 1
    
    if fixed > 0:
        with open(fpath, 'w', encoding='utf-8') as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
        total_fixed += fixed
        print(f"Fixed {fixed} in {rel}")

print(f"\nTotal fixed: {total_fixed}")
