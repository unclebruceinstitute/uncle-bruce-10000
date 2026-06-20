#!/usr/bin/env python3
"""Check HTML pages for broken links and references."""
import os, re
from pathlib import Path

BASE = Path('.')
issues = []
checked = 0

for fp in sorted(BASE.rglob('*.html')):
    if '.git' in str(fp):
        continue
    rel = str(fp)
    checked += 1
    try:
        with open(fp) as f:
            content = f.read()
    except:
        continue

    # Check fetch() JSON references
    json_refs = re.findall(r"fetch\(['\"]([^'\"]+\.json)['\"]", content)
    for ref in json_refs:
        if ref.startswith('http'):
            continue
        target = fp.parent / ref
        if not target.exists():
            issues.append(f'MISSING_JSON: {rel} -> {ref}')

    # Check relative links
    href_matches = re.findall(r'href=["\']((?!http|#|mailto|javascript)[^"\']+)["\']', content)
    for href in href_matches:
        target = fp.parent / href
        if not target.exists():
            if not (target / 'index.html').exists():
                issues.append(f'BROKEN_LINK: {rel} -> {href}')

    # Check script src
    src_matches = re.findall(r'<script[^>]+src=["\']((?!http)[^"\']+)["\']', content)
    for src in src_matches:
        target = fp.parent / src
        if not target.exists():
            issues.append(f'MISSING_SCRIPT: {rel} -> {src}')

    # Check CSS href
    css_matches = re.findall(r'<link[^>]+href=["\']((?!http)[^"\']+\.css)["\']', content)
    for css in css_matches:
        target = fp.parent / css
        if not target.exists():
            issues.append(f'MISSING_CSS: {rel} -> {css}')

print(f'Checked {checked} HTML files')
print(f'Found {len(issues)} issues:')
for iss in issues[:30]:
    print(f'  - {iss}')
if len(issues) > 30:
    print(f'  ... and {len(issues)-30} more')
