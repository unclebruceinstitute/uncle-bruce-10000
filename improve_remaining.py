#!/usr/bin/env python3
"""Improve remaining brief explanations across ALL levels."""
import json, re, os, math

def improve_by_question_text(q):
    """Match by question text patterns and generate KaTeX explanation."""
    q_text = q.get('question_zh', '')
    exp = q.get('explanation_zh', '')
    answer_idx = q.get('answer', 0)
    opts = q.get('options_zh', [])
    answer = opts[answer_idx] if answer_idx < len(opts) else ''
    
    # Skip if already improved (has $ or multiple newlines)
    if '$' in exp or exp.count('\n') >= 2:
        return False
    
    new_exp = None
    
    # 1. Inequalities: 解不等式 ax + b > c
    m = re.search(r'解不等式：?\s*(\d+)\s*x\s*\+\s*(\d+)\s*([><≥≤])\s*(\d+)', q_text)
    if m:
        a, b, op, rhs = int(m.group(1)), int(m.group(2)), m.group(3), int(m.group(4))
        x = (rhs - b) / a
        x_str = str(int(x)) if x == int(x) else f"{x:.2f}"
        new_exp = f"${a}x + {b} {op} {rhs}$\n${a}x {op} {rhs} - {b} = {rhs - b}$\n$x {op} \\frac{{{rhs - b}}}{{{a}}} = {x_str}$"
    
    # 2. Distance
    if not new_exp and '距離' in q_text:
        coords = re.findall(r'\((-?\d+),(-?\d+)\)', q_text)
        if len(coords) >= 2:
            x1, y1 = int(coords[0][0]), int(coords[0][1])
            x2, y2 = int(coords[1][0]), int(coords[1][1])
            dx, dy = x2-x1, y2-y1
            dist = (dx**2 + dy**2)**0.5
            dist_str = str(int(dist)) if dist == int(dist) else f"{dist:.2f}"
            new_exp = f"$d = \\sqrt{{(x_2-x_1)^2 + (y_2-y_1)^2}}$\n$d = \\sqrt{{({x2}-{x1})^2 + ({y2}-{y1})^2}} = \\sqrt{{{dx}^2+{dy}^2}} = \\sqrt{{{dx**2+dy**2}}} = {dist_str}$"
    
    # 3. Midpoint
    if not new_exp and '中點' in q_text:
        coords = re.findall(r'\((-?\d+),(-?\d+)\)', q_text)
        if len(coords) >= 2:
            x1, y1 = int(coords[0][0]), int(coords[0][1])
            x2, y2 = int(coords[1][0]), int(coords[1][1])
            mx = (x1+x2)/2; my = (y1+y2)/2
            mx_s = str(int(mx)) if mx == int(mx) else str(my)
            my_s = str(int(my)) if my == int(my) else str(my)
            new_exp = f"$M = \\left(\\frac{{{x1}+{x2}}}{2}, \\frac{{{y1}+{y2}}}{2}\\right) = ({mx_s}, {my_s})$"
    
    # 4. Mean
    if not new_exp and '平均數' in q_text:
        nums_raw = re.findall(r'(\d+)', q_text.split('的平均')[0] if '的平均' in q_text else q_text)
        nums = [int(n) for n in nums_raw if 10 <= int(n) <= 99]
        if len(nums) >= 2:
            total = sum(nums); n = len(nums)
            mean = total / n
            new_exp = f"$\\bar{{x}} = \\frac{{{'+'.join(str(x) for x in nums)}}}{{{n}}} = \\frac{{{total}}}{{{n}}} = {mean:.1f}$"
    
    # 5. Median
    if not new_exp and '中位數' in q_text:
        nums = sorted([int(n) for n in re.findall(r'\d+', q_text) if 10 <= int(n) <= 99])
        if nums:
            mid = nums[len(nums)//2]
            new_exp = f"Sorted: {', '.join(str(n) for n in nums)}\n$n = {len(nums)}$, middle position $= {len(nums)//2+1}$\nMedian $= {mid}$"
    
    # 6. Mode
    if not new_exp and '眾數' in q_text:
        nums = [int(n) for n in re.findall(r'\d+', q_text) if 10 <= int(n) <= 99]
        if nums:
            from collections import Counter
            mode = Counter(nums).most_common(1)[0][0]
            new_exp = f"Count occurrences of each number.\nMost frequent $= {mode}$"
    
    # 7. Triangle angles
    if not new_exp and '三角形' in q_text and '角' in q_text:
        m = re.search(r'(\d+)°\s*和\s*(\d+)°', q_text)
        if m:
            a, b = int(m.group(1)), int(m.group(2))
            c = 180 - a - b
            new_exp = f"Triangle angle sum $= 180°$\n$\\angle_3 = 180° - {a}° - {b}° = {c}°$"
    
    # 8. Simplify ratio
    if not new_exp and '簡化比' in q_text:
        m = re.search(r'(\d+):(\d+)', q_text)
        if m:
            a, b = int(m.group(1)), int(m.group(2))
            g = math.gcd(a, b)
            new_exp = f"$\\text{{GCF}}({a},{b}) = {g}$\n${a}:{b} = {a//g}:{b//g}$"
    
    # 9. Ratio sharing
    if not new_exp and '按' in q_text and '分給' in q_text:
        m = re.search(r'\$(\d+)\s*按\s*(\d+):(\d+)', q_text)
        if m:
            total, a, b = int(m.group(1)), int(m.group(2)), int(m.group(3))
            g = math.gcd(a,b); a2,b2 = a//g, b//g
            share = total*a2//(a2+b2) if '甲得' in q_text else total*b2//(a2+b2)
            who = 'A' if '甲得' in q_text else 'B'
            part = a2 if who=='A' else b2
            new_exp = f"Ratio ${a2}:{b2}$, total $= \\${total}$\nTotal parts $= {a2+b2}$\nEach part $= \\${total//(a2+b2)}$\n{who}'s share $= {total//(a2+b2)} \\times {part} = \\${share}$"
    
    # 10. Percentage of
    if not new_exp and '的' in q_text and '%' in q_text and '多少' in q_text:
        m = re.search(r'(\d+)\s*的\s*(\d+)%', q_text)
        if m:
            base, pct = int(m.group(1)), int(m.group(2))
            result = base * pct / 100
            new_exp = f"${base} \\times {pct}\\% = {base} \\times \\frac{{{pct}}}{{100}} = {result}$"
    
    # 11. Percentage change
    if not new_exp and ('減價' in q_text or '加價' in q_text) and '%' in q_text:
        m = re.search(r'\$(\d+).*?(\d+)%', q_text)
        if m:
            price, pct = int(m.group(1)), int(m.group(2))
            if '減價' in q_text:
                saved = price * pct / 100
                new_price = price - saved
                new_exp = f"$\\text{{Discount}} = \\${price} \\times {pct}\\% = \\${saved}$\n$\\text{{Sale price}} = \\${price} - \\${saved} = \\${new_price}$"
            else:
                add = price * pct / 100
                new_price = price + add
                new_exp = f"$\\text{{Increase}} = \\${price} \\times {pct}\\% = \\${add}$\n$\\text{{New price}} = \\${price} + \\${add} = \\${new_price}$"
    
    # 12. Arithmetic sequence
    if not new_exp and '等差數列' in q_text:
        m = re.search(r'([\d,\s]+),\s*\.\.\.，求第\s*(\d+)\s*項', q_text)
        if m:
            nums = [int(x.strip()) for x in m.group(1).split(',')]
            n = int(m.group(2))
            d = nums[1] - nums[0]
            a1 = nums[0]
            an = a1 + (n-1)*d
            new_exp = f"$d = {nums[1]} - {nums[0]} = {d}$\n$a_n = a_1 + (n-1)d$\n$a_{{{n}}} = {a1} + ({n}-1) \\times {d} = {an}$"
    
    # 13. Shopping/discount
    if not new_exp and '買' in q_text and '%' in q_text:
        m = re.search(r'買\s*(\d+)\s*個.*?\$(\d+).*?(\d+)%', q_text)
        if m:
            qty, price, pct = int(m.group(1)), int(m.group(2)), int(m.group(3))
            sub = qty * price
            disc = sub * pct / 100
            total = sub - disc
            new_exp = f"$\\text{{Subtotal}} = {qty} \\times \\${price} = \\${sub}$\n$\\text{{Discount}} = \\${sub} \\times {pct}\\% = \\${disc}$\n$\\text{{Total}} = \\${sub} - \\${disc} = \\${total}$"
    
    # 14. Volume - cuboid
    if not new_exp and '長方體' in q_text and '體積' in q_text:
        dims = re.findall(r'(\d+)', q_text)
        if len(dims) >= 3:
            a,b,c = int(dims[0]),int(dims[1]),int(dims[2])
            new_exp = f"$V = l \\times w \\times h = {a} \\times {b} \\times {c} = {a*b*c}$ cm³"
    
    # 15. Volume - cylinder
    if not new_exp and '圓柱' in q_text:
        rm = re.search(r'半徑\s*(\d+)', q_text)
        hm = re.search(r'高\s*(\d+)', q_text)
        if rm and hm:
            r,h = int(rm.group(1)),int(hm.group(1))
            vol = 3.14*r**2*h
            new_exp = f"$V = \\pi r^2 h = 3.14 \\times {r}^2 \\times {h} = 3.14 \\times {r**2} \\times {h} = {vol:.1f}$ cm³"
    
    # 16. Area - rectangle
    if not new_exp and '長方形' in q_text and '面積' in q_text:
        dims = re.findall(r'(\d+)', q_text)
        if len(dims) >= 2:
            a,b = int(dims[0]),int(dims[1])
            new_exp = f"$A = l \\times w = {a} \\times {b} = {a*b}$ cm²"
    
    # 17. Area - triangle
    if not new_exp and '三角形' in q_text and '面積' in q_text:
        m = re.search(r'底\s*(\d+).*?高\s*(\d+)', q_text)
        if m:
            b,h = int(m.group(1)),int(m.group(2))
            area = b*h/2
            new_exp = f"$A = \\frac{{1}}{{2}} \\times b \\times h = \\frac{{1}}{{2}} \\times {b} \\times {h} = {area}$ cm²"
    
    # 18. Speed/Distance/Time
    if not new_exp and '時速' in q_text and '行駛' in q_text:
        m = re.search(r'時速\s*(\d+).*?行駛\s*([\d.]+)\s*小時', q_text)
        if m:
            speed, time = float(m.group(1)), float(m.group(2))
            dist = speed * time
            new_exp = f"$d = v \\times t = {speed} \\times {time} = {dist}$ km"
    
    # 19. Age problem
    if not new_exp and '今年' in q_text and '歲' in q_text:
        m = re.search(r'今年\s*(\d+)\s*歲.*?(\d+)\s*年(後|前)', q_text)
        if m:
            age, years, direction = int(m.group(1)), int(m.group(2)), m.group(3)
            result = age + years if direction == '後' else age - years
            op = '+' if direction == '後' else '-'
            new_exp = f"${age} {op} {years} = {result}$ years old"
    
    # 20. Complementary/supplementary angles
    if not new_exp and '互補' in q_text:
        m = re.search(r'(\d+)°', q_text)
        if m:
            a = int(m.group(1))
            if '180' in q_text or 'supplementary' in q_text.lower():
                b = 180 - a
                new_exp = f"Supplementary angles sum to $180°$\n$180° - {a}° = {b}°$"
            else:
                b = 90 - a
                new_exp = f"Complementary angles sum to $90°$\n$90° - {a}° = {b}°$"
    
    # 21. Parallel lines
    if not new_exp and '平行' in q_text and '角' in q_text:
        m = re.search(r'(\d+)°', q_text)
        if m:
            a = int(m.group(1))
            if '同位角' in q_text or '內錯角' in q_text:
                new_exp = f"Corresponding/alternate angles are equal.\nAnswer $= {a}°$"
            elif '同旁內角' in q_text:
                b = 180 - a
                new_exp = f"Co-interior angles sum to $180°$\n$180° - {a}° = {b}°$"
    
    # 22. HCF/LCM
    if not new_exp and ('最大公因數' in q_text or '最小公倍數' in q_text):
        nums = re.findall(r'(\d+)', q_text)
        if len(nums) >= 2:
            a, b = int(nums[0]), int(nums[1])
            g = math.gcd(a, b)
            lcm = a * b // g
            if '最大公因數' in q_text:
                new_exp = f"$\\text{{GCF}}({a},{b}) = {g}$"
            else:
                new_exp = f"$\\text{{LCM}}({a},{b}) = \\frac{{{a} \\times {b}}}{{\\text{{GCF}}({a},{b})}} = \\frac{{{a*b}}}{{{g}}} = {lcm}$"
    
    # 23. Absolute value
    if not new_exp and '|' in q_text and '計算' in q_text:
        m = re.search(r'\|(-?\d+)\|', q_text)
        if m:
            a = int(m.group(1))
            new_exp = f"$|{a}| = {abs(a)}$"
    
    # 24. Fraction operations
    if not new_exp and re.search(r'計算\s+\d+/\d+\s*[+\-×÷]', q_text):
        m = re.search(r'計算\s+(\d+)/(\d+)\s*([+\-×÷])\s*(\d+)/(\d+)', q_text)
        if m:
            n1,d1,op,n2,d2 = int(m.group(1)),int(m.group(2)),m.group(3),int(m.group(4)),int(m.group(5))
            if op == '+':
                num = n1*d2 + n2*d1; den = d1*d2
            elif op == '-':
                num = n1*d2 - n2*d1; den = d1*d2
            elif op == '×':
                num = n1*n2; den = d1*d2
            else:
                num = n1*d2; den = d1*n2
            g = math.gcd(abs(num), abs(den))
            result = f"{num//g}/{den//g}"
            new_exp = f"$\\frac{{{n1}}}{{{d1}}} {op} \\frac{{{n2}}}{{{d2}}} = {result}$"
    
    # 25. Simplify algebraic
    if not new_exp and '簡化' in q_text and 'x' in q_text:
        m = re.search(r'簡化\s*(\d+)x\s*([+\-])\s*(\d+)x', q_text)
        if m:
            a, op, b = int(m.group(1)), m.group(2), int(m.group(3))
            result = a + b if op == '+' else a - b
            new_exp = f"${a}x {op} {b}x = {result}x$"
    
    if new_exp:
        q['explanation_zh'] = new_exp
        q['explanation_en'] = new_exp
        return True
    return False

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    improved = 0
    for q in data:
        if improve_by_question_text(q):
            improved += 1
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    return improved, len(data)

print("Improving remaining brief explanations...")
for level in ['s1','s2','s3','s4','s5','s6']:
    filepath = f'math/{level}/questions.json'
    if os.path.exists(filepath):
        improved, total = process_file(filepath)
        print(f"  {filepath}: {improved} more improved")
        v2 = f'v2/{filepath}'
        if os.path.exists(v2):
            import shutil
            shutil.copy2(filepath, v2)

# Final check
print("\nFinal status:")
for level in ['s1','s2','s3','s4','s5','s6']:
    with open(f'math/{level}/questions.json') as f:
        data = json.load(f)
    brief = sum(1 for q in data if q.get('explanation_zh','').startswith('此題考查') and q.get('explanation_zh','').count('\n') <= 1)
    katex = sum(1 for q in data if '$' in q.get('explanation_zh',''))
    print(f"  {level}: {len(data)} Qs, KaTeX={katex} ({katex*100//len(data)}%), still brief={brief} ({brief*100//len(data)}%)")
