#!/usr/bin/env python3
"""
Improve calculus explanations with dy/dx notation and step-by-step solutions.
Also add KaTeX support for math rendering.
"""
import json, re, os

def parse_terms(expr):
    """Parse polynomial terms like '3x³ + 6x²' or '3x^3 + 6x^2'."""
    # Normalize Unicode superscripts
    sup_map = {'⁰':'0','¹':'1','²':'2','³':'3','⁴':'4','⁵':'5','⁶':'6','⁷':'7','⁸':'8','⁹':'9'}
    for uni, num in sup_map.items():
        expr = expr.replace(uni, f'^{num}')
    
    # Parse terms: coeff x^power
    terms = []
    # Split by + or - (keeping sign)
    parts = re.split(r'(?=[+-])', expr.replace(' ', ''))
    for part in parts:
        if not part:
            continue
        m = re.match(r'^([+-]?)(\d*)(?:x(?:\^(\d+))?)?$', part)
        if not m:
            continue
        sign, coeff_str, power_str = m.groups()
        if not coeff_str and not power_str:
            continue  # skip constant-only
        if coeff_str:
            coeff = int(coeff_str)
        else:
            coeff = 1
        if sign == '-':
            coeff = -coeff
        if power_str:
            power = int(power_str)
        elif 'x' in part:
            power = 1
        else:
            power = 0
        terms.append((coeff, power))
    return terms

def improve_diff_explanation(q_zh, answer):
    """Improve differentiation explanation with KaTeX dy/dx notation."""
    match = re.search(r'f\(x\)\s*=\s*(.+?)(?:\s*的|$)', q_zh)
    if not match:
        return f"$f'(x) = {answer}$"
    
    expr = match.group(1).strip()
    terms = parse_terms(expr)
    if not terms:
        return f"$f'(x) = {answer}$"
    
    # Build KaTeX expression for f(x)
    fx_parts = []
    for coeff, power in terms:
        if power == 0:
            fx_parts.append(f"{coeff}")
        elif power == 1:
            fx_parts.append(f"{coeff}x" if coeff != 1 else "x")
        else:
            fx_parts.append(f"{coeff}x^{{{power}}}" if coeff != 1 else f"x^{{{power}}}")
    fx_katex = " + ".join(fx_parts).replace("+ -", "-")
    
    steps = []
    steps.append(f"$f(x) = {fx_katex}$")
    steps.append(f"$f'(x) = \\frac{{d}}{{dx}}({fx_katex})$")
    steps.append("")
    steps.append("Power rule: $\\frac{{d}}{{dx}}(ax^n) = n \\cdot a \\cdot x^{{n-1}}$")
    steps.append("")
    
    for coeff, power in terms:
        new_coeff = coeff * power
        new_power = power - 1
        if new_power == 0:
            steps.append(f"$\\frac{{d}}{{dx}}({coeff}x^{{{power}}}) = {power} \\cdot {coeff} \\cdot x^0 = {new_coeff}$")
        elif new_power == 1:
            steps.append(f"$\\frac{{d}}{{dx}}({coeff}x^{{{power}}}) = {power} \\cdot {coeff} \\cdot x = {new_coeff}x$")
        else:
            steps.append(f"$\\frac{{d}}{{dx}}({coeff}x^{{{power}}}) = {power} \\cdot {coeff} \\cdot x^{{{new_power}}} = {new_coeff}x^{{{new_power}}}$")
    
    # Build result in KaTeX
    result_parts = []
    for coeff, power in terms:
        new_c = coeff * power
        new_p = power - 1
        if new_p == 0:
            result_parts.append(str(new_c))
        elif new_p == 1:
            result_parts.append(f"{new_c}x" if new_c != 1 else "x")
        else:
            result_parts.append(f"{new_c}x^{{{new_p}}}" if new_c != 1 else f"x^{{{new_p}}}")
    result_katex = " + ".join(result_parts).replace("+ -", "-")
    
    steps.append("")
    steps.append(f"$f'(x) = {result_katex}$")
    return "\n".join(steps)

def improve_int_explanation(q_zh, answer):
    """Improvised integration explanation with KaTeX ∫ notation."""
    match = re.search(r'∫\s*\((.+?)\)\s*dx', q_zh)
    if not match:
        return f"$\\int ... \\, dx = {answer}$"
    
    expr = match.group(1).strip()
    terms = parse_terms(expr)
    if not terms:
        return f"$\\int ({expr}) \\, dx = {answer}$"
    
    # Build KaTeX expression
    fx_parts = []
    for coeff, power in terms:
        if power == 0:
            fx_parts.append(str(coeff))
        elif power == 1:
            fx_parts.append(f"{coeff}x" if coeff != 1 else "x")
        else:
            fx_parts.append(f"{coeff}x^{{{power}}}" if coeff != 1 else f"x^{{{power}}}")
    fx_katex = " + ".join(fx_parts).replace("+ -", "-")
    
    steps = []
    steps.append(f"$\\int ({fx_katex}) \\, dx$")
    steps.append("")
    steps.append("Power rule: $\\int ax^n \\, dx = \\frac{{a \\cdot x^{{n+1}}}}{{n+1}} + C$")
    steps.append("")
    
    result_parts = []
    for coeff, power in terms:
        new_power = power + 1
        from math import gcd
        g = gcd(abs(coeff), new_power)
        num = coeff // g
        den = new_power // g
        if den == 1:
            if new_power == 1:
                term_str = f"{num}x" if num != 1 else "x"
            else:
                term_str = f"{num}x^{{{new_power}}}" if num != 1 else f"x^{{{new_power}}}"
        else:
            if new_power == 1:
                term_str = f"\\frac{{{num}x}}{{{den}}}" if num != 1 else f"\\frac{{x}}{{{den}}}"
            else:
                term_str = f"\\frac{{{num}x^{{{new_power}}}}}{{{den}}}" if num != 1 else f"\\frac{{x^{{{new_power}}}}}{{{den}}}"
        result_parts.append(term_str)
        
        coeff_katex = str(coeff) if coeff != 1 else ""
        steps.append(f"$\\int {coeff_katex}x^{{{power}}} \\, dx = \\frac{{{coeff} \\cdot x^{{{new_power}}}}}{{{new_power}}} = {term_str}$")
    
    result_katex = " + ".join(result_parts).replace("+ -", "-")
    steps.append("")
    steps.append(f"$= {result_katex} + C$")
    return "\n".join(steps)

def improve_vector_explanation(q_zh, answer):
    """Improve vector explanation."""
    return f"Vector addition: add corresponding components.\n{answer}"

def process_file(filepath):
    """Process a math questions file and improve calculus explanations."""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    improved = 0
    for q in data:
        topic = q.get('topic_zh', '')
        q_text = q.get('question_zh', '')
        answer_text = q.get('options_zh', [''])[q.get('answer', 0)] if q.get('answer', 0) < len(q.get('options_zh', [])) else ''
        
        if '微分' in topic or '微分' in q_text:
            new_exp = improve_diff_explanation(q_text, answer_text)
            if new_exp and new_exp != q.get('explanation_zh', ''):
                q['explanation_zh'] = new_exp
                q['explanation_en'] = new_exp  # Same for now
                improved += 1
        elif '積分' in topic or '∫' in q_text:
            new_exp = improve_int_explanation(q_text, answer_text)
            if new_exp and new_exp != q.get('explanation_zh', ''):
                q['explanation_zh'] = new_exp
                q['explanation_en'] = new_exp
                improved += 1
        elif '向量' in topic:
            new_exp = improve_vector_explanation(q_text, answer_text)
            if new_exp and new_exp != q.get('explanation_zh', ''):
                q['explanation_zh'] = new_exp
                q['explanation_en'] = new_exp
                improved += 1
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    
    return improved, len(data)

# Process S5 and S6 (calculus levels)
for level in ['s5', 's6']:
    filepath = f'math/{level}/questions.json'
    if os.path.exists(filepath):
        improved, total = process_file(filepath)
        print(f'{filepath}: improved {improved}/{total} explanations')
        
        # Also save to v2
        v2_path = f'v2/{filepath}'
        if os.path.exists(v2_path):
            import shutil
            shutil.copy2(filepath, v2_path)
            print(f'  Copied to {v2_path}')

# Also process S4 (may have some calculus)
for level in ['s4']:
    filepath = f'math/{level}/questions.json'
    if os.path.exists(filepath):
        improved, total = process_file(filepath)
        print(f'{filepath}: improved {improved}/{total} explanations')

print("Done!")
