#!/usr/bin/env python3
"""Find and fix answer index mismatches across all question banks.
Checks: answer points to the option that matches the explanation."""
import json, os, re, glob

base = '/Users/bruce/.openclaw/workspace/projects/project_03_bruce_institute_10000/uncle-bruce-10000'

def normalize_answer(answer, opts):
    """Convert answer to numeric index."""
    if isinstance(answer, int):
        return answer
    if isinstance(answer, str):
        if len(answer) == 1 and answer.upper() in 'ABCD':
            return ord(answer.upper()) - ord('A')
        # Try to match against options
        for i, opt in enumerate(opts):
            if answer.strip().lower() in opt.lower():
                return i
    return 0

def extract_answer_from_explanation(exp_zh, exp_en):
    """Try to extract the correct answer text from explanation."""
    for exp in [exp_zh, exp_en]:
        if not exp:
            continue
        # Pattern: "正確答案是「XXX」" or 'The correct answer is "XXX"'
        m = re.search(r'(?:正確答案是|正确答案是|The correct answer is)\s*[「"\'"]?(.+?)[」"\'"]?[。.]?\s*$', exp)
        if m:
            return m.group(1).strip()
        # Pattern: "答案：XXX" or "Answer: XXX"
        m = re.search(r'(?:答案|Answer)\s*[:：]\s*(.+?)[。.]?\s*$', exp)
        if m:
            return m.group(1).strip()
    return None

def check_and_fix_bank(filepath):
    """Check a question bank for answer mismatches and fix them."""
    with open(filepath, 'r', encoding='utf-8') as f:
        d = json.load(f)
    
    qs = d.get('questions', d) if isinstance(d, dict) else d
    if not isinstance(qs, list):
        return 0, 0, []
    
    fixed = 0
    issues = []
    
    for q in qs:
        qid = q.get('id', '?')
        answer_raw = q.get('answer', 0)
        opts_zh = q.get('options_zh', [])
        opts_en = q.get('options_en', [])
        exp_zh = q.get('explanation_zh', '')
        exp_en = q.get('explanation_en', '')
        
        # Get the option that the answer currently points to
        opts = opts_en if opts_en else opts_zh
        answer = normalize_answer(answer_raw, opts)
        if not opts or answer >= len(opts):
            continue
        
        current_answer_text = opts[answer]
        
        # Extract what the explanation says the answer should be
        expected = extract_answer_from_explanation(exp_zh, exp_en)
        if not expected:
            continue
        
        # Check if the current answer matches the explanation
        # Clean up option text (remove "A. " prefix)
        def clean_opt(t):
            return re.sub(r'^[A-Da-d][.．、]\s*', '', t).strip()
        
        current_clean = clean_opt(current_answer_text)
        expected_clean = clean_opt(expected)
        
        # Check match (case insensitive, partial match)
        if current_clean.lower() == expected_clean.lower():
            continue
        if expected_clean.lower() in current_clean.lower() or current_clean.lower() in expected_clean.lower():
            continue
        
        # Try to find the correct option
        correct_idx = None
        for i, opt in enumerate(opts):
            opt_clean = clean_opt(opt)
            if opt_clean.lower() == expected_clean.lower() or expected_clean.lower() in opt_clean.lower():
                correct_idx = i
                break
        
        if correct_idx is not None and correct_idx != answer:
            # Fix the answer - preserve original format
            if isinstance(answer_raw, str) and len(answer_raw) == 1 and answer_raw.upper() in 'ABCD':
                q['answer'] = chr(ord('A') + correct_idx)
            else:
                q['answer'] = correct_idx
            fixed += 1
            issues.append({
                'id': qid,
                'old_answer': answer,
                'new_answer': correct_idx,
                'old_text': current_answer_text,
                'correct_text': opts[correct_idx],
                'expected': expected
            })
    
    return len(qs), fixed, issues

# Process all question banks
json_files = glob.glob(os.path.join(base, '**/questions.json'), recursive=True)
total_fixed = 0
total_questions = 0
all_issues = {}

for fpath in sorted(json_files):
    rel = os.path.relpath(fpath, base)
    try:
        count, fixed, issues = check_and_fix_bank(fpath)
        if fixed > 0:
            # Save the fixed file
            with open(fpath, 'r', encoding='utf-8') as f:
                d = json.load(f)
            with open(fpath, 'w', encoding='utf-8') as f:
                json.dump(d, f, ensure_ascii=False, indent=2)
            
            total_fixed += fixed
            total_questions += count
            all_issues[rel] = issues
            print(f"🔧 {rel}: {fixed}/{count} fixed")
            for iss in issues[:5]:  # Show first 5
                print(f"   #{iss['id']}: answer {iss['old_answer']}→{iss['new_answer']} | '{iss['correct_text'][:50]}'")
            if len(issues) > 5:
                print(f"   ... and {len(issues)-5} more")
        else:
            total_questions += count
    except Exception as e:
        print(f"❌ {rel}: {e}")

print(f"\n{'='*60}")
print(f"Total: {total_fixed}/{total_questions} questions fixed")
if all_issues:
    print(f"\nBanks with fixes:")
    for bank, issues in all_issues.items():
        print(f"  {bank}: {len(issues)} fixes")
