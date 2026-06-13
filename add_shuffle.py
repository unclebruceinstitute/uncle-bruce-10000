#!/usr/bin/env python3
"""Add runtime option shuffling to all quiz HTML pages."""
import os, re, glob

base = '/Users/bruce/.openclaw/workspace/projects/project_03_bruce_institute_10000/uncle-bruce-10000'

SHUFFLE_FUNC = """
function shuffleOptions(q){
  if(q._shuffled)return;
  var opts=getOpts(q),ans=getAns(q);
  var idx=[0,1,2,3];
  for(var i=3;i>0;i--){var j=Math.floor(Math.random()*(i+1));var t=idx[i];idx[i]=idx[j];idx[j]=t;}
  q._opts=[idx.map(function(i){return opts[i]}), idx.map(function(i){return opts[i]})];
  q._ans=idx.indexOf(ans);
  q._shuffled=true;
}
"""

files = glob.glob(os.path.join(base, '**/index.html'), recursive=True)
updated = 0

for fpath in sorted(files):
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'function showQuestion' not in content:
        continue
    if 'shuffleOptions' in content:
        print(f"⏭️  Already done: {os.path.relpath(fpath, base)}")
        continue
    
    # 1. Insert shuffleOptions function before showQuestion
    content = content.replace(
        'function showQuestion(){',
        SHUFFLE_FUNC + 'function showQuestion(){'
    )
    
    # 2. In showQuestion, replace the opts rendering with shuffled version
    # Old pattern: const opts=getOpts(q); or var opts=getOpts(q);
    # followed by opts.map(...)
    # We need to add shuffleOptions(q) call and change opts source
    
    # Replace the options rendering block
    old_opts_pattern = re.compile(
        r"(document\.getElementById\('qText'\)\.textContent=getQ\(q\);\s*\n)"
        r"(\s*)(const|var)\s+opts=getOpts\(q\);\s*\n"
        r"(\s*)document\.getElementById\('qOptions'\)\.innerHTML=opts\.map\(\(o,i\)=>",
        re.MULTILINE
    )
    
    new_opts = (
        r"\1"
        r"\2shuffleOptions(q);\n"
        r"\2\3 opts=q._opts[lang==='en'?1:0];\n"
        r"\4document.getElementById('qOptions').innerHTML=opts.map((o,i)=>"
    )
    
    content_new = re.sub(old_opts_pattern, new_opts, content)
    if content_new == content:
        # Try alternative pattern (some files might use slightly different formatting)
        # Try simpler replacement
        if "const opts=getOpts(q);" in content:
            content = content.replace(
                "document.getElementById('qText').textContent=getQ(q);\n  const opts=getOpts(q);",
                "document.getElementById('qText').textContent=getQ(q);\n  shuffleOptions(q);\n  const opts=q._opts[lang==='en'?1:0];"
            )
        elif "var opts=getOpts(q);" in content:
            content = content.replace(
                "document.getElementById('qText').textContent=getQ(q);\n  var opts=getOpts(q);",
                "document.getElementById('qText').textContent=getQ(q);\n  shuffleOptions(q);\n  var opts=q._opts[lang==='en'?1:0];"
            )
    else:
        content = content_new
    
    # 3. In checkAnswer, replace ans lookup
    old_ans = "const q=currentQuiz[currentIndex],ans=getAns(q);"
    new_ans = "const q=currentQuiz[currentIndex];\n  shuffleOptions(q);\n  const ans=q._ans;"
    content = content.replace(old_ans, new_ans)
    
    # Also try var version
    old_ans2 = "var q=currentQuiz[currentIndex],ans=getAns(q);"
    new_ans2 = "var q=currentQuiz[currentIndex];\n  shuffleOptions(q);\n  var ans=q._ans;"
    content = content.replace(old_ans2, new_ans2)
    
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    updated += 1
    print(f"✅ {os.path.relpath(fpath, base)}")

print(f"\n🎉 Updated {updated} files")
