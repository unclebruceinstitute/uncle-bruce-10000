#!/usr/bin/env python3
"""Daily maintenance audit for 大B舅父萬題庫"""
import json, os, re, sys
from pathlib import Path
from collections import Counter

BASE = Path(".")
issues = []
stats = {"total_questions": 0, "total_json_files": 0, "total_html_files": 0}

# ── 1. JSON quality checks ──
print("=" * 60)
print("1. JSON QUALITY AUDIT")
print("=" * 60)

json_files = sorted(BASE.rglob("questions.json"))
low_count_categories = []

for jf in json_files:
    rel = str(jf.relative_to(BASE))
    try:
        with open(jf) as f:
            data = json.load(f)
    except Exception as e:
        issues.append(f"JSON PARSE ERROR: {rel}: {e}")
        continue

    # Handle both list and dict-with-questions format
    if isinstance(data, dict) and 'questions' in data:
        data = data['questions']
    if not isinstance(data, list):
        issues.append(f"NOT A LIST: {rel}")
        continue

    count = len(data)
    stats["total_json_files"] += 1
    stats["total_questions"] += count

    # Skip very small test files
    if count <= 1:
        continue

    # Check low count categories (< 40 questions)
    if count < 40:
        low_count_categories.append((rel, count))

    # Check for duplicates (by question text, support both formats)
    q_texts = []
    for q in data:
        qt = (q.get("question_zh") or q.get("question_en") or q.get("question", "")).strip()
        if qt:
            q_texts.append(qt)

    dup_count = len(q_texts) - len(set(q_texts))
    if dup_count > 0:
        issues.append(f"DUPLICATES ({dup_count}): {rel}")

    # Check answer distribution (answer is 0-3 int, not letter)
    answers = [q.get("answer") for q in data if q.get("answer") is not None]
    if answers:
        dist = Counter(answers)
        total_a = len(answers)
        for ans_val, cnt in dist.items():
            pct = cnt / total_a * 100
            if pct > 50 or pct < 10:
                issues.append(f"ANSWER IMBALANCE ({ans_val}={pct:.0f}%): {rel}")

    # Check empty options and placeholder options
    empty_opts = 0
    placeholder_opts = 0
    missing_explanation = 0
    placeholder_patterns = ['错误选项', '正確選項', '正确选项', '錯誤選項', 'Placeholder']
    for q in data:
        opts = q.get("options_zh") or q.get("options_en") or q.get("options", [])
        if isinstance(opts, list):
            for o in opts:
                if not o or not str(o).strip():
                    empty_opts += 1
                    break
            # Check for placeholder options (wrong answers with template text)
            ans = q.get("answer", -1)
            for i, o in enumerate(opts):
                if isinstance(o, str) and any(p in o for p in placeholder_patterns):
                    if i != ans:  # only count wrong-answer placeholders
                        placeholder_opts += 1
                        break

        exp = q.get("explanation_zh") or q.get("explanation_en") or q.get("explanation")
        if not exp or not str(exp).strip():
            missing_explanation += 1

    if empty_opts > 0:
        issues.append(f"EMPTY OPTIONS ({empty_opts}): {rel}")
    if placeholder_opts > 5:
        issues.append(f"PLACEHOLDER OPTIONS ({placeholder_opts}/{count}): {rel}")
    if missing_explanation > count * 0.5:
        issues.append(f"MISSING EXPLANATIONS ({missing_explanation}/{count}): {rel}")

# Report low count
if low_count_categories:
    print("\n⚠️ LOW QUESTION COUNT (< 40):")
    for path, cnt in sorted(low_count_categories, key=lambda x: x[1]):
        print(f"  {cnt:4d} questions: {path}")

# ── 2. HTML checks ──
print("\n" + "=" * 60)
print("2. HTML QUALITY AUDIT")
print("=" * 60)

html_files = sorted(BASE.rglob("index.html"))
stats["total_html_files"] = len(html_files)

html_issues = []
for hf in html_files:
    rel = str(hf.relative_to(BASE))
    try:
        content = hf.read_text(encoding="utf-8")
    except Exception as e:
        html_issues.append(f"READ ERROR: {rel}: {e}")
        continue

    # Check for common JS errors
    if "undefined is not" in content.lower():
        html_issues.append(f"JS ERROR PATTERN: {rel}")
    if "SyntaxError" in content:
        html_issues.append(f"SYNTAX ERROR: {rel}")

    # Check back button links
    back_matches = re.findall(r'href="([^"]*)"[^>]*>.*?(?:返回|back|←)', content, re.I | re.S)
    for href in back_matches:
        if href.startswith("http"):
            continue
        # Check relative path exists
        target = (hf.parent / href).resolve()
        if not target.exists():
            html_issues.append(f"BROKEN BACK LINK ({href}): {rel}")

    # Check questions.json reference exists
    json_refs = re.findall(r'(?:fetch|load)\s*\(\s*["\']([^"\']*questions\.json)["\']', content)
    for ref in json_refs:
        target = (hf.parent / ref).resolve()
        if not target.exists():
            html_issues.append(f"BROKEN JSON REF ({ref}): {rel}")

    # Check for duplicate HTML in music (classic + duplicate folder)
    if "sazaesan" in rel or ("classic" in rel and "sazae_san" in rel):
        # Check for duplicate sazae-san folders
        pass

for hi in html_issues:
    print(f"  ❌ {hi}")

# ── 3. Duplicate HTML pages (same content) ──
print("\n" + "=" * 60)
print("3. DUPLICATE / REDUNDANT PAGES")
print("=" * 60)

# Check for sazae_san vs sazaesan duplication
sazae_paths = [p for p in html_files if "sazae" in str(p).lower()]
if len(sazae_paths) > 1:
    print(f"  ⚠️ Multiple Sazae-san pages: {[str(p.relative_to(BASE)) for p in sazae_paths]}")

# ── 4. Summary ──
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"  Total JSON files scanned: {stats['total_json_files']}")
print(f"  Total questions: {stats['total_questions']}")
print(f"  Total HTML pages: {stats['total_html_files']}")
print(f"  Issues found: {len(issues)}")

if issues:
    print("\n🔴 ALL ISSUES:")
    for i in issues:
        print(f"  {i}")
else:
    print("\n✅ No issues found!")
