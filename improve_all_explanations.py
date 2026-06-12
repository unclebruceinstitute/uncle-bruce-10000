#!/usr/bin/env python3
"""Improve ALL math explanations with step-by-step KaTeX solutions."""
import json, re, os, math

def parse_poly(expr):
    """Parse polynomial like '3x² - 3x + 1' into [(coeff, power), ...]."""
    sup = {'⁰':'0','¹':'1','²':'2','³':'3','⁴':'4','⁵':'5','⁶':'6','⁷':'7','⁸':'8','⁹':'9'}
    for u, n in sup.items():
        expr = expr.replace(u, f'^{n}')
    expr = expr.replace(' ', '')
    terms = []
    parts = re.split(r'(?=[+-])', expr)
    for p in parts:
        if not p: continue
        m = re.match(r'^([+-]?)(\d*)(?:x(?:\^(\d+))?)?$', p)
        if not m: continue
        sign, cs, ps = m.groups()
        if not cs and not ps: continue
        c = int(cs) if cs else 1
        if sign == '-': c = -c
        pw = int(ps) if ps else (1 if 'x' in p else 0)
        terms.append((c, pw))
    return terms

def poly_to_katex(terms):
    """Convert terms to KaTeX string."""
    parts = []
    for c, pw in terms:
        if pw == 0:
            parts.append(str(c))
        elif pw == 1:
            parts.append(f"{c}x" if c != 1 else "x")
        else:
            parts.append(f"{c}x^{{{pw}}}" if c != 1 else f"x^{{{pw}}}")
    s = " + ".join(parts)
    return s.replace("+ -", "- ")

def eval_poly(terms, x_val):
    """Evaluate polynomial at x_val."""
    return sum(c * x_val**pw for c, pw in terms)

def deriv_terms(terms):
    """Differentiate polynomial terms."""
    result = []
    for c, pw in terms:
        if pw > 0:
            result.append((c * pw, pw - 1))
    return result

def improve_f_eval(q_zh, answer):
    """Improve f(x) evaluation explanation."""
    m = re.search(r'f\(x\)\s*=\s*(.+?)，\s*求\s*f\((\d+)\)', q_zh)
    if not m: return None
    expr, x_str = m.group(1), m.group(2)
    x = int(x_str)
    terms = parse_poly(expr)
    if not terms: return None
    
    fx_katex = poly_to_katex(terms)
    
    steps = []
    steps.append(f"$f(x) = {fx_katex}$")
    steps.append(f"Substitute $x = {x}$:")
    steps.append("")
    
    sub_parts = []
    for c, pw in terms:
        val = c * x**pw
        if pw == 0:
            sub_parts.append(f"{c}")
            steps.append(f"  ${c} = {c}$")
        elif pw == 1:
            sub_parts.append(f"{c} \\times {x}")
            steps.append(f"  ${c}x = {c} \\times {x} = {val}$")
        else:
            sub_parts.append(f"{c} \\times {x}^{{{pw}}}")
            steps.append(f"  ${c}x^{{{pw}}} = {c} \\times {x**pw} = {val}$")
    
    steps.append("")
    result = eval_poly(terms, x)
    sum_str = " + ".join(str(int(c * x**pw)) for c, pw in terms)
    steps.append(f"$f({x}) = {sum_str} = {result}$")
    
    return "\n".join(steps)

def improve_tangent(q_zh, answer):
    """Improve tangent slope explanation with dy/dx."""
    m = re.search(r'y\s*=\s*(.+?)\s*在\s*x\s*=\s*(\d+)\s*處', q_zh)
    if not m: return None
    expr, x_str = m.group(1), m.group(2)
    x = int(x_str)
    terms = parse_poly(expr)
    if not terms: return None
    
    fx_katex = poly_to_katex(terms)
    deriv = deriv_terms(terms)
    dy_katex = poly_to_katex(deriv)
    
    steps = []
    steps.append(f"$y = {fx_katex}$")
    steps.append("")
    steps.append(f"$\\frac{{dy}}{{dx}} = {dy_katex}$")
    steps.append("")
    steps.append(f"At $x = {x}$:")
    
    sub_parts = []
    for c, pw in deriv:
        val = c * x**pw
        if pw == 0:
            sub_parts.append(str(c))
        elif pw == 1:
            sub_parts.append(f"{c} \\times {x}")
            steps.append(f"  ${c}x = {c} \\times {x} = {val}$")
        else:
            sub_parts.append(f"{c} \\times {x}^{{{pw}}}")
            steps.append(f"  ${c}x^{{{pw}}} = {c} \\times {x**pw} = {val}$")
    
    result = eval_poly(deriv, x)
    steps.append("")
    steps.append(f"$\\frac{{dy}}{{dx}}\\Big|_{{x={x}}} = {result}$")
    steps.append(f"Tangent slope $= {result}$")
    
    return "\n".join(steps)

def improve_std_dev(q_zh, answer):
    """Improve standard deviation explanation."""
    nums = re.findall(r'[\d.]+', q_zh.split('的')[0])
    nums = [float(n) for n in nums if '.' not in n or n.count('.') == 1]
    if len(nums) < 2: return None
    
    n = len(nums)
    mean = sum(nums) / n
    var = sum((x - mean)**2 for x in nums) / n
    sd = var ** 0.5
    
    steps = []
    steps.append(f"Data: {', '.join(str(int(x)) for x in nums)}")
    steps.append(f"$n = {n}$")
    steps.append(f"$\\bar{{x}} = \\frac{{{'+'.join(str(int(x)) for x in nums)}}}{{{n}}} = {mean:.2f}$")
    steps.append("")
    steps.append("$\\sigma = \\sqrt{\\frac{\\sum(x_i - \\bar{x})^2}{n}}$")
    steps.append("")
    
    sq_parts = []
    for x in nums:
        d = x - mean
        sq_parts.append(f"({int(x)} - {mean:.2f})^2 = {d**2:.2f}")
    steps.append("Squared deviations: " + ", ".join(sq_parts))
    steps.append(f"$\\sum(x_i - \\bar{{x}})^2 = {sum((x-mean)**2 for x in nums):.2f}$")
    steps.append(f"$\\sigma = \\sqrt{{{var:.2f}}} = {sd:.2f}$")
    
    return "\n".join(steps)

def improve_mean(q_zh, answer):
    """Improve mean explanation."""
    # Extract numbers from "求 X, Y, Z, ... 的平均數"
    m = re.search(r'求\s+([\d,\s]+)\s*的平均', q_zh)
    if not m: return None
    nums = [int(x.strip()) for x in m.group(1).split(',')]
    total = sum(nums)
    n = len(nums)
    mean = total / n
    
    steps = []
    steps.append(f"Data: {', '.join(str(x) for x in nums)}")
    steps.append(f"$\\bar{{x}} = \\frac{{{'+'.join(str(x) for x in nums)}}}{{{n}}}$")
    steps.append(f"$\\bar{{x}} = \\frac{{{total}}}{{{n}}} = {mean:.1f}$")
    
    return "\n".join(steps)

def improve_triangle(q_zh, answer):
    """Improve triangle angle explanation."""
    m = re.search(r'三角形兩角為\s*(\d+)°\s*和\s*(\d+)°', q_zh)
    if not m: return None
    a, b = int(m.group(1)), int(m.group(2))
    c = 180 - a - b
    
    steps = []
    steps.append("Sum of angles in a triangle $= 180°$")
    steps.append(f"$\\angle_3 = 180° - {a}° - {b}° = {c}°$")
    
    return "\n".join(steps)

def improve_equation(q_zh, answer):
    """Improve equation solving explanation."""
    m = re.search(r'解方程\s*(\d*)x\s*\+\s*(\d+)\s*=\s*(\d+)', q_zh)
    if not m: return None
    a_str, b_str, rhs_str = m.group(1), m.group(2), m.group(3)
    a = int(a_str) if a_str else 1
    b = int(b_str)
    rhs = int(rhs_str)
    x = (rhs - b) / a
    
    steps = []
    steps.append(f"${a}x + {b} = {rhs}$")
    steps.append(f"${a}x = {rhs} - {b} = {rhs - b}$")
    steps.append(f"$x = \\frac{{{rhs - b}}}{{{a}}} = {int(x) if x == int(x) else x}$")
    
    return "\n".join(steps)

def improve_distance(q_zh, answer):
    """Improve distance explanation."""
    coords = re.findall(r'\((-?\d+),(-?\d+)\)', q_zh)
    if len(coords) < 2: return None
    x1, y1 = int(coords[0][0]), int(coords[0][1])
    x2, y2 = int(coords[1][0]), int(coords[1][1])
    
    dx = x2 - x1
    dy = y2 - y1
    dist = (dx**2 + dy**2) ** 0.5
    
    steps = []
    steps.append(f"$d = \\sqrt{{(x_2 - x_1)^2 + (y_2 - y_1)^2}}$")
    steps.append(f"$d = \\sqrt{{({x2} - {x1})^2 + ({y2} - {y1})^2}}$")
    steps.append(f"$d = \\sqrt{{{dx}^2 + {dy}^2}} = \\sqrt{{{dx**2} + {dy**2}}} = \\sqrt{{{dx**2 + dy**2}}}$")
    if dist == int(dist):
        steps.append(f"$d = {int(dist)}$")
    
    return "\n".join(steps)

def improve_midpoint(q_zh, answer):
    """Improve midpoint explanation."""
    coords = re.findall(r'\((-?\d+),(-?\d+)\)', q_zh)
    if len(coords) < 2: return None
    x1, y1 = int(coords[0][0]), int(coords[0][1])
    x2, y2 = int(coords[1][0]), int(coords[1][1])
    mx = (x1 + x2) / 2
    my = (y1 + y2) / 2
    
    steps = []
    steps.append(f"$M = \\left(\\frac{{x_1 + x_2}}{{2}}, \\frac{{y_1 + y_2}}{{2}}\\right)$")
    steps.append(f"$M = \\left(\\frac{{{x1} + {x2}}}{{2}}, \\frac{{{y1} + {y2}}}{{2}}\\right)$")
    mx_str = str(int(mx)) if mx == int(mx) else str(mx)
    my_str = str(int(my)) if my == int(my) else str(my)
    steps.append(f"$M = ({mx_str}, {my_str})$")
    
    return "\n".join(steps)

def improve_volume(q_zh, answer):
    """Improve volume explanation."""
    if '長方體' in q_zh:
        dims = re.findall(r'(\d+)', q_zh)
        if len(dims) >= 3:
            a, b, c = int(dims[0]), int(dims[1]), int(dims[2])
            steps = [
                f"$V = l \\times w \\times h$",
                f"$V = {a} \\times {b} \\times {c} = {a*b*c}$ cm³"
            ]
            return "\n".join(steps)
    elif '圓柱' in q_zh:
        r_m = re.search(r'半徑\s*(\d+)', q_zh)
        h_m = re.search(r'高\s*(\d+)', q_zh)
        if r_m and h_m:
            r, h = int(r_m.group(1)), int(h_m.group(1))
            vol = 3.14 * r**2 * h
            steps = [
                f"$V = \\pi r^2 h$",
                f"$V = 3.14 \\times {r}^2 \\times {h}$",
                f"$V = 3.14 \\times {r**2} \\times {h} = {vol:.1f}$ cm³"
            ]
            return "\n".join(steps)
    return None

def improve_ratio(q_zh, answer):
    """Improve ratio simplification."""
    m = re.search(r'簡化比\s*(\d+):(\d+)', q_zh)
    if not m: return None
    a, b = int(m.group(1)), int(m.group(2))
    g = math.gcd(a, b)
    steps = [
        f"$\\text{{GCF}}({a}, {b}) = {g}$",
        f"${a}:{b} = {a//g}:{b//g}$"
    ]
    return "\n".join(steps)

def improve_sharing(q_zh, answer):
    """Improve ratio sharing explanation."""
    m = re.search(r'\$(\d+)\s*按\s*(\d+):(\d+)', q_zh)
    if not m: return None
    total, a, b = int(m.group(1)), int(m.group(2)), int(m.group(3))
    g = math.gcd(a, b)
    a2, b2 = a//g, b//g
    share = total * a2 // (a2 + b2) if '甲得' in q_zh else total * b2 // (a2 + b2)
    who = 'A' if '甲得' in q_zh else 'B'
    part = a2 if who == 'A' else b2
    
    steps = [
        f"Ratio ${a2}:{b2}$, total $= \\${total}$",
        f"Total parts $= {a2} + {b2} = {a2 + b2}$",
        f"Each part $= \\frac{{{total}}}{{{a2+b2}}} = {total//(a2+b2)}$",
        f"{who}'s share $= {total//(a2+b2)} \\times {part} = \\${share}$"
    ]
    return "\n".join(steps)

def improve_pct(q_zh, answer):
    """Improve percentage explanation."""
    if '減價' in q_zh or '加價' in q_zh:
        m = re.search(r'\$(\d+).*?(\d+)%', q_zh)
        if not m: return None
        price, pct = int(m.group(1)), int(m.group(2))
        if '減價' in q_zh:
            new_price = price * (1 - pct/100)
            steps = [
                f"Original $= \\${price}$, discount $= {pct}\\%$",
                f"$\\text{{Discount}} = {price} \\times \\frac{{{pct}}}{{100}} = {price * pct / 100}$",
                f"$\\text{{Sale price}} = {price} - {price * pct / 100} = \\${new_price}$"
            ]
        else:
            new_price = price * (1 + pct/100)
            steps = [
                f"Original $= \\${price}$, increase $= {pct}\\%$",
                f"$\\text{{Increase}} = {price} \\times \\frac{{{pct}}}{{100}} = {price * pct / 100}$",
                f"$\\text{{New price}} = {price} + {price * pct / 100} = \\${new_price}$"
            ]
        return "\n".join(steps)
    elif '的' in q_zh and '%' in q_zh:
        m = re.search(r'(\d+)\s*的\s*(\d+)%', q_zh)
        if not m: return None
        base, pct = int(m.group(1)), int(m.group(2))
        result = base * pct / 100
        steps = [
            f"${base} \\times {pct}\\% = {base} \\times \\frac{{{pct}}}{{100}} = {result}$"
        ]
        return "\n".join(steps)
    return None

def improve_arithmetic_seq(q_zh, answer):
    """Improve arithmetic sequence explanation."""
    m = re.search(r'等差數列\s*([\d,\s]+),\s*\.\.\.，求第\s*(\d+)\s*項', q_zh)
    if not m: return None
    nums = [int(x.strip()) for x in m.group(1).split(',')]
    n = int(m.group(2))
    d = nums[1] - nums[0]
    a1 = nums[0]
    an = a1 + (n-1) * d
    
    steps = [
        f"First terms: {', '.join(str(x) for x in nums)}",
        f"Common difference $d = {nums[1]} - {nums[0]} = {d}$",
        f"$a_n = a_1 + (n-1)d$",
        f"$a_{{{n}}} = {a1} + ({n}-1) \\times {d} = {a1} + {(n-1)*d} = {an}$"
    ]
    return "\n".join(steps)

def improve_shopping(q_zh, answer):
    """Improve shopping/discount explanation."""
    m = re.search(r'買\s*(\d+)\s*個.*?\$(\d+).*?(\d+)%', q_zh)
    if not m: return None
    qty, price, pct = int(m.group(1)), int(m.group(2)), int(m.group(3))
    subtotal = qty * price
    discount = subtotal * pct / 100
    total = subtotal - discount
    
    steps = [
        f"$\\text{{Subtotal}} = {qty} \\times \\${price} = \\${subtotal}$",
        f"$\\text{{Discount}} = \\${subtotal} \\times {pct}\\% = \\${discount}$",
        f"$\\text{{Total}} = \\${subtotal} - \\${discount} = \\${total}$"
    ]
    return "\n".join(steps)

# Map topic_id/subtopic_id to improvement function
IMPROVERS = {
    ('directed_number', 'bodmas'): None,
    ('directed_number', 'fractions'): None,
    ('directed_number', 'hcf_lcm'): None,
    ('directed_number', 'absolute'): None,
    ('directed_number', 'powers'): None,
    ('statistics', 'mean'): improve_mean,
    ('statistics', 'median'): None,
    ('statistics', 'mode'): None,
    ('statistics', 'probability'): None,
    ('basic_algebra', 'linear_eq'): improve_equation,
    ('basic_algebra', 'simplify'): None,
    ('basic_algebra', 'expand'): None,
    ('basic_algebra', 'substitution'): None,
    ('basic_algebra', 'inequalities'): None,
    ('coordinates', 'distance'): improve_distance,
    ('coordinates', 'midpoint'): improve_midpoint,
    ('basic_geometry', 'triangles'): improve_triangle,
    ('basic_geometry', 'angles'): None,
    ('basic_geometry', 'parallel'): None,
    ('basic_geometry', 'polygons'): None,
    ('area_volume', 'area'): None,
    ('area_volume', 'volume'): improve_volume,
    ('ratio_rate', 'simplify'): improve_ratio,
    ('ratio_rate', 'sharing'): improve_sharing,
    ('ratio_rate', 'sdt'): None,
    ('mixed', 'shopping'): improve_shopping,
    ('mixed', 'age'): None,
    ('mixed', 'work'): None,
    ('percentages', 'basic'): improve_pct,
    ('percentages', 'change'): improve_pct,
    ('sequences', 'arithmetic'): improve_arithmetic_seq,
    ('sequences', 'patterns'): None,
    # S5/S6 specific
    ('DSE 模擬 - 代數', ''): improve_f_eval,
    ('DSE 模擬 - 微積分', ''): improve_tangent,
    ('DSE 模擬 - 統計與概率', ''): improve_std_dev,
}

def improve_question(q):
    """Try to improve a single question's explanation."""
    topic = q.get('topic_id', '')
    subtopic = q.get('subtopic_id', '')
    q_text = q.get('question_zh', '')
    answer_text = q.get('options_zh', [''])[q.get('answer', 0)] if q.get('answer', 0) < len(q.get('options_zh', [])) else ''
    
    # Try specific matchers for S5/S6 topics
    if 'f(x)' in q_text and '求 f(' in q_text:
        new_exp = improve_f_eval(q_text, answer_text)
        if new_exp:
            q['explanation_zh'] = new_exp
            q['explanation_en'] = new_exp
            return True
    
    if '切線斜率' in q_text or 'y=' in q_text:
        new_exp = improve_tangent(q_text, answer_text)
        if new_exp:
            q['explanation_zh'] = new_exp
            q['explanation_en'] = new_exp
            return True
    
    if '標準差' in q_text:
        new_exp = improve_std_dev(q_text, answer_text)
        if new_exp:
            q['explanation_zh'] = new_exp
            q['explanation_en'] = new_exp
            return True
    
    # Try by topic_id/subtopic_id
    key = (topic, subtopic)
    improver = IMPROVERS.get(key)
    if not improver:
        # Try topic_id only
        for k, v in IMPROVERS.items():
            if k[0] == topic:
                improver = v
                break
    
    if improver:
        new_exp = improver(q_text, answer_text)
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
        if improve_question(q):
            improved += 1
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    
    return improved, len(data)

print("Improving ALL math explanations with KaTeX...")
for level in ['s1','s2','s3','s4','s5','s6']:
    filepath = f'math/{level}/questions.json'
    if os.path.exists(filepath):
        improved, total = process_file(filepath)
        print(f"  {filepath}: {improved}/{total} improved")
        # Copy to v2
        v2 = f'v2/{filepath}'
        if os.path.exists(os.path.dirname(v2)):
            import shutil
            shutil.copy2(filepath, v2)

print("\nDone!")
