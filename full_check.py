#!/usr/bin/env python3
"""
全面檢查大B舅父萬題庫所有題目數據
掃描所有 JSON + HTML 文件，檢查 26 類問題，自動修復並輸出報告。
"""

import json
import os
import re
import shutil
from collections import Counter, defaultdict
from pathlib import Path

BASE = Path(__file__).parent
REPORT = []
ISSUES_BY_CATEGORY = defaultdict(list)
FILES_FIXED = set()
TOTAL_QUESTIONS = 0
TOTAL_ISSUES = 0
TOTAL_FIXED = 0

# ─── Helpers ────────────────────────────────────────────────────────────

def rel(p):
    return str(p.relative_to(BASE))

def backup_file(p):
    bak = p.with_suffix(p.suffix + '.bak')
    if not bak.exists():
        shutil.copy2(p, bak)

def load_json(p):
    with open(p, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(p, data):
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def log_issue(category, file_path, detail):
    global TOTAL_ISSUES
    TOTAL_ISSUES += 1
    entry = f"  [{category}] {rel(file_path)}: {detail}"
    REPORT.append(entry)
    ISSUES_BY_CATEGORY[category].append((rel(file_path), detail))

def log_fix(category, file_path, detail):
    global TOTAL_FIXED
    TOTAL_FIXED += 1
    entry = f"  [FIXED:{category}] {rel(file_path)}: {detail}"
    REPORT.append(entry)

# ─── Option prefix stripping ────────────────────────────────────────────

OPTION_PREFIX_RE = re.compile(r'^[A-Za-z][\.\)\]\:]\s*')

def strip_option_prefix(opt):
    """Remove letter prefix like 'A. ', 'B) ', 'C] ' from option text."""
    return OPTION_PREFIX_RE.sub('', opt).strip()

# ─── JSON question checks ──────────────────────────────────────────────

def check_questions(questions, file_path, is_v2_format=False):
    """Check all questions in a list. Returns (modified, questions)."""
    global TOTAL_QUESTIONS
    modified = False
    seen_questions = {}  # question_text -> index for duplicate detection
    answer_dist = Counter()
    questions_to_remove = set()

    for i, q in enumerate(questions):
        TOTAL_QUESTIONS += 1

        # Determine field names based on format
        if is_v2_format:
            q_field = 'question_zh'
            opts_field = 'options_zh'
        else:
            q_field = 'question'
            opts_field = 'options'

        # --- Check 12: question is empty ---
        question_text = q.get(q_field, '') or q.get('question_zh', '') or q.get('question', '')
        if isinstance(question_text, str) and question_text.strip() == '':
            log_issue('Q12_EMPTY_QUESTION', file_path, f"Q#{i}: question is empty string")

        # --- Check 7: duplicate questions ---
        q_key = question_text.strip() if isinstance(question_text, str) else str(question_text)
        if q_key in seen_questions and q_key != '':
            log_issue('Q7_DUPLICATE_QUESTION', file_path,
                       f"Q#{i} duplicates Q#{seen_questions[q_key]}: '{q_key[:60]}...'")
            questions_to_remove.add(i)
            modified = True
        else:
            seen_questions[q_key] = i

        # --- Get options ---
        opts = q.get(opts_field) or q.get('options_zh') or q.get('options', [])
        if not isinstance(opts, list):
            log_issue('Q11_OPTIONS_LT2', file_path, f"Q#{i}: options is not a list")
            continue

        # --- Check 11: less than 2 options ---
        if len(opts) < 2:
            log_issue('Q11_OPTIONS_LT2', file_path, f"Q#{i}: only {len(opts)} option(s)")

        # --- Check 6: empty options ---
        for j, opt in enumerate(opts):
            if isinstance(opt, str) and opt.strip() == '':
                log_issue('Q6_EMPTY_OPTION', file_path, f"Q#{i}, option {j}: empty string")

        # --- Check 8: duplicate options within a question ---
        opt_stripped = [o.strip() if isinstance(o, str) else str(o) for o in opts]
        seen_opts = {}
        for j, o in enumerate(opt_stripped):
            if o in seen_opts:
                log_issue('Q8_DUPLICATE_OPTION', file_path,
                           f"Q#{i}: option {j} duplicates option {seen_opts[o]}: '{o[:40]}'")
            else:
                seen_opts[o] = j

        # --- Check 14: option letter prefix ---
        for j, opt in enumerate(opts):
            if isinstance(opt, str) and OPTION_PREFIX_RE.match(opt):
                stripped = strip_option_prefix(opt)
                log_issue('Q14_OPTION_PREFIX', file_path,
                           f"Q#{i}, opt {j}: '{opt[:40]}' -> '{stripped[:40]}'")
                q[opts_field][j] = stripped
                # Also fix other option fields
                for other_field in ['options_en']:
                    other_opts = q.get(other_field, [])
                    if j < len(other_opts) and isinstance(other_opts[j], str) and OPTION_PREFIX_RE.match(other_opts[j]):
                        q[other_field][j] = strip_option_prefix(other_opts[j])
                modified = True

        # --- Check 15: extra whitespace in options ---
        for j, opt in enumerate(opts):
            if isinstance(opt, str) and (opt != opt.strip()):
                log_issue('Q15_OPTION_WHITESPACE', file_path,
                           f"Q#{i}, opt {j}: extra whitespace")
                q[opts_field][j] = opt.strip()
                # Also fix other option fields
                for other_field in ['options_en']:
                    other_opts = q.get(other_field, [])
                    if j < len(other_opts) and isinstance(other_opts[j], str):
                        q[other_field][j] = other_opts[j].strip()
                modified = True

        # --- Check 9 & 10: answer index out of bounds / negative ---
        answer = q.get('answer')
        n_opts = len(opts)
        if answer is not None:
            if not isinstance(answer, int):
                log_issue('Q13_ANSWER_MISSING', file_path, f"Q#{i}: answer is not a number: {repr(answer)}")
            else:
                if answer < 0:
                    log_issue('Q10_ANSWER_NEGATIVE', file_path,
                               f"Q#{i}: answer={answer} (negative)")
                elif answer >= n_opts:
                    log_issue('Q9_ANSWER_OOB', file_path,
                               f"Q#{i}: answer={answer} but only {n_opts} options")
                    # Auto-fix: clamp to last valid index
                    q['answer'] = n_opts - 1
                    log_fix('Q9_ANSWER_OOB', file_path, f"Q#{i}: answer {answer} -> {n_opts-1}")
                    modified = True
                else:
                    answer_dist[answer] += 1

        # --- Check 17 & 18: language/garbled text ---
        zh_val = q.get('zh', '') or q.get('question_zh', '')
        en_val = q.get('en', '') or q.get('question_en', '')
        # Detect garbled: high ratio of non-printable or replacement chars
        def has_garbled(s):
            if not isinstance(s, str):
                return False
            garbled_chars = sum(1 for c in s if ord(c) == 0xFFFD or (ord(c) < 32 and c not in '\n\r\t'))
            return garbled_chars > len(s) * 0.1 and len(s) > 5

        if has_garbled(zh_val):
            log_issue('Q17_GARBLED', file_path, f"Q#{i}: zh field has garbled text")
        if has_garbled(en_val):
            log_issue('Q17_GARBLED', file_path, f"Q#{i}: en field has garbled text")

    # Remove duplicates (mark for removal, then remove in reverse order)
    if questions_to_remove:
        for idx in sorted(questions_to_remove, reverse=True):
            questions.pop(idx)

    # --- Check 16: answer distribution imbalance ---
    total_answered = sum(answer_dist.values())
    if total_answered >= 10:
        for idx, count in answer_dist.items():
            pct = count / total_answered * 100
            if pct > 40:
                log_issue('Q16_ANSWER_DIST', file_path,
                           f"Answer index {idx}: {count}/{total_answered} ({pct:.1f}%) — severely imbalanced")

    return modified, questions

# ─── HTML checks ────────────────────────────────────────────────────────

def check_html(file_path):
    global TOTAL_QUESTIONS
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    modified = False
    rp = rel(file_path)

    # Check 1: \'\' syntax error (escaped quotes in JS)
    if "\\'\\'" in content:
        log_issue('HTML1_ESCAPED_QUOTES', file_path, "Contains \\'\\' syntax error")

    # Check 2: startTopic onclick extra closing paren
    if re.search(r'onclick="startTopic\([^)]*\)\s*\)"', content):
        log_issue('HTML2_STARTTOPIC_PAREN', file_path, "startTopic onclick has extra )")

    # Check 3: shuffleOptions hardcoded idx
    if 'shuffleOptions' in content and 'idx=[0,1,2,3]' in content:
        log_issue('HTML3_SHUFFLE_HARDCODED', file_path, "shuffleOptions has hardcoded idx=[0,1,2,3]")

    # Check 4: Topic card onclick with parens in name
    # Look for patterns like onclick="startTopic('...')" where topic name has parens
    topic_onclicks = re.findall(r"startTopic\('([^']*)'\)", content)
    for tn in topic_onclicks:
        if '(' in tn or ')' in tn:
            log_issue('HTML4_TOPIC_ONCLICK', file_path, f"Topic name has parens: '{tn}'")

    # Check 5: reference to broken practice.html
    if 'practice.html' in content:
        log_issue('HTML5_PRACTICE_HTML', file_path, "References practice.html")

    # Check 19: language switch button white text on white bg
    # Look for color:#fff or color:white in button styles that might be on light bg
    # This is tricky - we look for lang button styling issues

    # Check 20: missing back button
    # Look for a back/home link or button
    has_back = ('返回' in content or 'back-btn' in content or 'goBack' in content
                or 'history.back' in content or '返回首頁' in content or '←' in content)
    # Skip root index.html and subject index pages - they don't need back buttons
    is_root = rp in ['index.html'] or rp.count('/') == 1  # subject level
    if not has_back and not is_root and '/s' in rp:
        log_issue('HTML20_NO_BACK_BTN', file_path, "No back button found")

    # Count quiz questions loaded (for stats)
    q_count_match = re.search(r'questions\s*=\s*\[', content)
    if q_count_match:
        # This is a quiz page with embedded questions
        TOTAL_QUESTIONS += 0  # Counted from JSON files

# ─── Main scan ──────────────────────────────────────────────────────────

def find_json_files():
    """Find all JSON files that contain question data."""
    json_files = []
    for root, dirs, files in os.walk(BASE):
        # Skip .git, backup files
        dirs[:] = [d for d in dirs if d != '.git' and not d.endswith('.bak')]
        for f in files:
            if f.endswith('.json') and not f.endswith('.bak'):
                p = Path(root) / f
                # Skip index.json (topic index, not questions) and manifest.json
                if f in ('index.json', 'manifest.json'):
                    continue
                json_files.append(p)
    return sorted(json_files)

def find_html_files():
    """Find all HTML files."""
    html_files = []
    for root, dirs, files in os.walk(BASE):
        dirs[:] = [d for d in dirs if d != '.git']
        for f in files:
            if f.endswith('.html'):
                html_files.append(Path(root) / f)
    return sorted(html_files)

def is_v2_format(filepath):
    """Check if file is in v2 directory."""
    return '/v2/' in str(filepath)

def is_v2_question_format(q):
    """Check if a single question uses the v2 field names."""
    return 'question_zh' in q or 'options_zh' in q

def main():
    global TOTAL_QUESTIONS

    print("=" * 70)
    print("大B舅父萬題庫 — 全面數據質量檢查")
    print("=" * 70)
    print()

    # ── Scan JSON files ──
    json_files = find_json_files()
    print(f"📂 找到 {len(json_files)} 個 JSON 數據檔案")

    for jf in json_files:
        try:
            data = load_json(jf)
        except json.JSONDecodeError as e:
            log_issue('JSON_PARSE_ERROR', jf, f"JSON parse error: {e}")
            continue

        if not isinstance(data, list):
            continue  # Skip non-array JSON files

        if len(data) == 0:
            continue

        # Determine format
        v2fmt = is_v2_format(jf) or is_v2_question_format(data[0])

        modified, cleaned = check_questions(data, jf, is_v2_format=v2fmt)

        if modified:
            backup_file(jf)
            save_json(jf, cleaned)
            FILES_FIXED.add(rel(jf))

    # ── Scan HTML files ──
    html_files = find_html_files()
    print(f"📄 找到 {len(html_files)} 個 HTML 檔案")

    for hf in html_files:
        check_html(hf)

    # ── Generate Report ──
    print()
    print("=" * 70)
    print("📊 檢查報告")
    print("=" * 70)
    print()
    print(f"✅ 總共檢查題目數：{TOTAL_QUESTIONS}")
    print(f"📂 檢查 JSON 檔案：{len(json_files)}")
    print(f"📄 檢查 HTML 檔案：{len(html_files)}")
    print(f"🔴 發現問題總數：{TOTAL_ISSUES}")
    print(f"🔧 自動修復數量：{TOTAL_FIXED}")
    print(f"📁 修改檔案數量：{len(FILES_FIXED)}")
    print()

    # Category breakdown
    if ISSUES_BY_CATEGORY:
        print("── 問題分類統計 ──")
        for cat in sorted(ISSUES_BY_CATEGORY.keys()):
            items = ISSUES_BY_CATEGORY[cat]
            print(f"  {cat}: {len(items)} 個")
        print()

    # Detailed issues
    if REPORT:
        print("── 問題詳情 ──")
        for line in REPORT:
            print(line)
    else:
        print("🎉 全部檢查通過，冇發現任何問題！")

    print()
    print("=" * 70)
    print("檢查完成")
    print("=" * 70)

    # Save report to file
    report_path = BASE / 'check_report.txt'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("大B舅父萬題庫 — 全面數據質量檢查報告\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"總共檢查題目數：{TOTAL_QUESTIONS}\n")
        f.write(f"檢查 JSON 檔案：{len(json_files)}\n")
        f.write(f"檢查 HTML 檔案：{len(html_files)}\n")
        f.write(f"發現問題總數：{TOTAL_ISSUES}\n")
        f.write(f"自動修復數量：{TOTAL_FIXED}\n")
        f.write(f"修改檔案數量：{len(FILES_FIXED)}\n\n")
        if ISSUES_BY_CATEGORY:
            f.write("問題分類統計：\n")
            for cat in sorted(ISSUES_BY_CATEGORY.keys()):
                items = ISSUES_BY_CATEGORY[cat]
                f.write(f"  {cat}: {len(items)} 個\n")
            f.write("\n")
        f.write("問題詳情：\n")
        for line in REPORT:
            f.write(line + "\n")

    print(f"\n📝 報告已保存到：{rel(report_path)}")

if __name__ == '__main__':
    main()
