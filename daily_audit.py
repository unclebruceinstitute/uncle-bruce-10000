#!/usr/bin/env python3
"""Daily audit script for Uncle Bruce 10000 question bank."""
import json, os, re, sys
from pathlib import Path
from collections import Counter

BASE = Path(__file__).parent
issues = []
stats = {"total_files": 0, "total_questions": 0, "empty_options": 0, "dup_questions": 0, "answer_mismatch": 0, "bad_prefix": 0, "missing_explanation": 0, "empty_question": 0, "answer_skew": 0}

def get_question_text(q):
    """Get question text from various field names."""
    for key in ['question', 'question_zh', 'question_en', 'questionText']:
        t = q.get(key, '').strip()
        if t:
            return t
    return ''

def check_json(filepath):
    rel = str(filepath.relative_to(BASE))
    try:
        with open(filepath) as f:
            data = json.load(f)
    except Exception as e:
        issues.append(f"JSON_ERROR: {rel}: {e}")
        return

    questions = data if isinstance(data, list) else data.get("questions", [])
    if not isinstance(questions, list):
        issues.append(f"NOT_LIST: {rel}")
        return

    stats["total_files"] += 1
    stats["total_questions"] += len(questions)

    seen_texts = set()
    answer_dist = Counter()
    empty_q_count = 0
    no_answer_count = 0
    no_explanation_count = 0

    for i, q in enumerate(questions):
        qid = f"{rel}#{i}"

        # Empty question text
        qt = get_question_text(q)
        if not qt:
            empty_q_count += 1
            continue

        # Duplicate question text
        norm = re.sub(r'\s+', ' ', qt.lower().strip())[:100]
        if norm in seen_texts:
            stats["dup_questions"] += 1
            if stats["dup_questions"] <= 20:
                issues.append(f"DUP_Q: {qid}: {qt[:60]}")
        seen_texts.add(norm)

        # Check options - try multiple field names
        options = q.get("options", q.get("options_zh", q.get("options_en", [])))
        if not options:
            stats["empty_options"] += 1
            if stats["empty_options"] <= 10:
                issues.append(f"NO_OPTIONS: {qid}")
            continue

        for j, opt in enumerate(options):
            if not opt or not str(opt).strip():
                stats["empty_options"] += 1
                if stats["empty_options"] <= 10:
                    issues.append(f"EMPTY_OPT: {qid} opt[{j}]")

        # Check answer validity
        answer = q.get("answer", "")
        if answer == "" or answer is None:
            no_answer_count += 1
        else:
            answer_dist[str(answer)] += 1

        # Missing explanation
        expl = q.get("explanation", q.get("explanation_zh", q.get("explanation_en", "")))
        if not str(expl).strip():
            no_explanation_count += 1

    stats["empty_question"] += empty_q_count
    stats["missing_explanation"] += no_explanation_count

    if empty_q_count > 0:
        issues.append(f"EMPTY_Q_BATCH: {rel}: {empty_q_count} questions have no text")
    if no_answer_count > len(questions) * 0.5 and len(questions) > 0:
        issues.append(f"MANY_NO_ANSWER: {rel}: {no_answer_count}/{len(questions)}")

    # Answer distribution check
    if answer_dist and len(questions) > 20:
        total = sum(answer_dist.values())
        for ans, cnt in sorted(answer_dist.items()):
            pct = cnt / total * 100
            if pct > 45 and total > 10:
                stats["answer_skew"] += 1
                if stats["answer_skew"] <= 10:
                    issues.append(f"SKEWED_ANS: {rel}: answer '{ans}' = {pct:.0f}% ({cnt}/{total})")

def check_html(filepath):
    rel = str(filepath.relative_to(BASE))
    try:
        with open(filepath) as f:
            content = f.read()
    except:
        return

    # Check back button links
    back_matches = re.findall(r'href=["\']([^"\']+)["\'][^>]*class=["\'][^"\']*back', content)
    for href in back_matches:
        if href.startswith('http') or href.startswith('#'):
            continue
        target = filepath.parent / href
        if not target.exists() and not (filepath.parent / href.lstrip('./')).exists():
            # Try resolving relative to base
            alt = BASE / href.lstrip('./')
            if not alt.exists():
                issues.append(f"BROKEN_BACK: {rel} -> {href}")

    # Check script src references
    src_matches = re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', content)
    for src in src_matches:
        if src.startswith('http'):
            continue
        target = filepath.parent / src
        if not target.exists():
            issues.append(f"BROKEN_SCRIPT: {rel} -> {src}")

    # Check CSS href references
    css_matches = re.findall(r'<link[^>]+href=["\']([^"\']+\.css)["\']', content)
    for css in css_matches:
        if css.startswith('http'):
            continue
        target = filepath.parent / css
        if not target.exists():
            issues.append(f"BROKEN_CSS: {rel} -> {css}")

# Scan all JSON files
for fp in sorted(BASE.rglob("questions.json")):
    if '.git' in str(fp):
        continue
    check_json(fp)

# Scan all HTML files
for fp in sorted(BASE.rglob("*.html")):
    if '.git' in str(fp):
        continue
    check_html(fp)

# Report
print("=" * 60)
print("📊 大B舅父萬題庫 — 每日審計報告")
print("=" * 60)
print(f"\n📁 JSON 檔案數: {stats['total_files']}")
print(f"📝 總題目數: {stats['total_questions']:,}")
print(f"\n⚠️ 問題統計:")
print(f"  空題目 (冇 question text): {stats['empty_question']}")
print(f"  重複題目: {stats['dup_questions']}")
print(f"  空選項: {stats['empty_options']}")
print(f"  缺 explanation: {stats['missing_explanation']}")
print(f"  答案分佈偏斜: {stats['answer_skew']}")

# Find low-count categories
print(f"\n📊 分類題目數量 (少於50題):")
low_count = []
for fp in sorted(BASE.rglob("questions.json")):
    if '.git' in str(fp):
        continue
    try:
        with open(fp) as f:
            data = json.load(f)
        questions = data if isinstance(data, list) else data.get("questions", [])
        if len(questions) < 50:
            rel = str(fp.relative_to(BASE))
            low_count.append((len(questions), rel))
    except:
        pass

for cnt, path in sorted(low_count):
    print(f"  {cnt:>5} 題: {path}")

print(f"\n📊 題目數量統計 (各主要分類):")
category_counts = Counter()
for fp in sorted(BASE.rglob("questions.json")):
    if '.git' in str(fp):
        continue
    try:
        with open(fp) as f:
            data = json.load(f)
        questions = data if isinstance(data, list) else data.get("questions", [])
        rel = str(fp.relative_to(BASE))
        # Get top-level category
        parts = rel.split('/')
        cat = parts[0] if len(parts) > 1 else 'root'
        category_counts[cat] += len(questions)
    except:
        pass

for cat, cnt in category_counts.most_common():
    print(f"  {cnt:>8,} 題: {cat}")

if issues:
    print(f"\n🔴 發現 {len(issues)} 個問題:")
    for iss in issues[:60]:
        print(f"  - {iss}")
    if len(issues) > 60:
        print(f"  ... 及另外 {len(issues)-60} 個問題")
else:
    print(f"\n✅ 冇發現問題！")

# Save report
with open(BASE / "audit_report.txt", "w") as f:
    f.write(f"Audit: {os.popen('date').read().strip()}\n")
    f.write(f"Files: {stats['total_files']}, Questions: {stats['total_questions']}\n")
    f.write(f"Issues: {len(issues)}\n")
    for iss in issues:
        f.write(iss + "\n")
