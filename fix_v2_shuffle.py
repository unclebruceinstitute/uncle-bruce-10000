#!/usr/bin/env python3
"""Fix v2-style quiz pages to use shuffleOptions."""
import os, glob

base = '/Users/bruce/.openclaw/workspace/projects/project_03_bruce_institute_10000/uncle-bruce-10000'

# Files with v2-style pattern (getQText, different opts pattern)
v2_files = glob.glob(os.path.join(base, 'v2/*/index.html')) + \
           glob.glob(os.path.join(base, 'v2/*/*/index.html'))

updated = 0
for fpath in sorted(v2_files):
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'function showQuestion' not in content:
        continue
    
    # Check if already fixed (has shuffleOptions call in showQuestion body)
    show_func_start = content.find('function showQuestion(){')
    if show_func_start == -1:
        continue
    show_func_end = content.find('\nfunction ', show_func_start + 10)
    show_func = content[show_func_start:show_func_end] if show_func_end != -1 else content[show_func_start:]
    
    if 'shuffleOptions(q)' in show_func and 'q._opts' in show_func:
        print(f"⏭️  Already done: {os.path.relpath(fpath, base)}")
        continue
    
    # Fix opts line in showQuestion
    old_opts = "const opts=(lang==='en'?q.options_en:q.options_zh)||q.options_zh;"
    new_opts = "shuffleOptions(q);\nconst opts=q._opts[lang==='en'?1:0];"
    if old_opts in content:
        content = content.replace(old_opts, new_opts)
    
    # Fix var version
    old_opts2 = "var opts=(lang==='en'?q.options_en:q.options_zh)||q.options_zh;"
    new_opts2 = "shuffleOptions(q);\nvar opts=q._opts[lang==='en'?1:0];"
    if old_opts2 in content:
        content = content.replace(old_opts2, new_opts2)
    
    # Fix checkAnswer if it uses getAns instead of q._ans
    old_ans = "const q=currentQuiz[currentIndex],ans=getAns(q);"
    new_ans = "const q=currentQuiz[currentIndex];\nshuffleOptions(q);\nconst ans=q._ans;"
    if old_ans in content:
        content = content.replace(old_ans, new_ans)
    
    old_ans2 = "var q=currentQuiz[currentIndex],ans=getAns(q);"
    new_ans2 = "var q=currentQuiz[currentIndex];\nshuffleOptions(q);\nvar ans=q._ans;"
    if old_ans2 in content:
        content = content.replace(old_ans2, new_ans2)
    
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    updated += 1
    print(f"✅ {os.path.relpath(fpath, base)}")

print(f"\n🎉 Updated {updated} files")
