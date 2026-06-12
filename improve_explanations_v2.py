#!/usr/bin/env python3
"""
Generate detailed explanations for all math questions.
Replaces one-line "正確答案是 X" with step-by-step solutions.
"""
import json, re, math

def explain_bodmas(q_zh, q_en, ans, opts, correct_idx):
    """四則混合運算"""
    # Extract the expression
    expr = q_zh.replace('計算 ', '').replace('Calculate ', '')
    steps = []
    
    # Parse the expression for BODMAS explanation
    if '×' in expr and ('+' in expr or '-' in expr):
        steps.append("記住 BODMAS 法則：先乘除，後加減。")
        # Find the multiplication part
        parts = re.findall(r'[-\d]+ × [-\d]+', expr)
        if parts:
            for p in parts:
                nums = p.split(' × ')
                result = int(nums[0]) * int(nums[1])
                steps.append(f"先計 {p} = {result}")
    
    if '(' in expr:
        steps.append("先計括號內嘅運算。")
    
    steps.append(f"計算過程：{expr} = {ans}")
    
    # Add negative number tips if relevant
    if '-' in str(expr) and ('×' in expr or '÷' in expr):
        steps.append("注意負數運算規則：負×正=負，負×負=正。")
    
    zh = f"題目要求計算：{expr}\n" + "\n".join(steps) + f"\n答案是 {ans}。"
    en = f"We need to calculate: {expr}\n" + "\n".join(steps) + f"\nThe answer is {ans}."
    return zh, en

def explain_fractions(q_zh, q_en, ans, opts, correct_idx):
    """分數運算"""
    expr = q_zh.replace('計算 ', '').replace('比較 ', '').replace('嘅大小', '')
    
    if '比較' in q_zh:
        zh = f"將兩個分數通分後比較大小。\n{expr}\n通分後比較分子：答案是 {ans}。"
        en = f"Compare by finding common denominator.\n{expr}\nAnswer: {ans}."
    elif '×' in expr:
        zh = f"分數乘法：分子×分子，分母×分母。\n{expr} = {ans}"
        en = f"Fraction multiplication: numerator×numerator, denominator×denominator.\n{expr} = {ans}"
    elif '÷' in expr:
        zh = f"分數除法：將除數倒轉後相乘。\n{expr}\n倒轉第二個分數後相乘 = {ans}"
        en = f"Fraction division: flip the second fraction and multiply.\n{expr} = {ans}"
    elif '+' in expr:
        zh = f"分數加法：先通分，再將分子相加。\n通分後計算 = {ans}"
        en = f"Fraction addition: find common denominator, then add numerators.\n= {ans}"
    elif '-' in expr:
        zh = f"分數減法：先通分，再將分子相減。\n通分後計算 = {ans}"
        en = f"Fraction subtraction: find common denominator, then subtract numerators.\n= {ans}"
    else:
        zh = f"計算分數運算。\n{expr} = {ans}"
        en = f"Calculate: {expr} = {ans}"
    return zh, en

def explain_hcf_lcm(q_zh, q_en, ans, opts, correct_idx):
    """公因數與公倍數"""
    nums = re.findall(r'\d+', q_zh)
    a, b = int(nums[0]), int(nums[1])
    g = math.gcd(a, b)
    lcm = a * b // g
    
    if '最大公因數' in q_zh or 'GCF' in q_en:
        zh = f"求 {a} 和 {b} 的最大公因數（GCF）。\n{a} 的因數：{sorted([i for i in range(1,a+1) if a%i==0])}\n{b} 的因數：{sorted([i for i in range(1,b+1) if b%i==0])}\n最大公因數 = {g}"
        en = f"Find GCF of {a} and {b}.\nFactors of {a}: {sorted([i for i in range(1,a+1) if a%i==0])}\nFactors of {b}: {sorted([i for i in range(1,b+1) if b%i==0])}\nGCF = {g}"
    else:
        zh = f"求 {a} 和 {b} 的最小公倍數（LCM）。\nLCM = {a}×{b} ÷ GCF({a},{b}) = {a}×{b}÷{g} = {lcm}"
        en = f"Find LCM of {a} and {b}.\nLCM = {a}×{b} ÷ GCF({a},{b}) = {a}×{b}÷{g} = {lcm}"
    return zh, en

def explain_absolute(q_zh, q_en, ans, opts, correct_idx):
    """絕對值"""
    expr = q_zh.replace('計算 ', '')
    zh = f"絕對值係指一個數同 0 嘅距離，必定係非負數。\n{expr}\n計算後取絕對值 = {ans}"
    en = f"Absolute value is the distance from 0, always non-negative.\n{expr}\n= {ans}"
    return zh, en

def explain_powers(q_zh, q_en, ans, opts, correct_idx):
    """冪次"""
    expr = q_zh.replace('計算 ', '')
    zh = f"計算冪次方。\n{expr}\n逐步計算 = {ans}"
    en = f"Calculate powers.\n{expr}\n= {ans}"
    if '√' in expr:
        zh = f"求平方根/立方根。\n{expr} = {ans}\n即係問：邊個數嘅平方/立方等於被開方數？"
        en = f"Find square/cube root.\n{expr} = {ans}"
    return zh, en

def explain_mean(q_zh, q_en, ans, opts, correct_idx):
    """平均數"""
    # Extract actual data numbers (skip context numbers like "5次")
    # Look for comma-separated number lists
    data_match = re.findall(r'(?:(?:\d+),\s*)+(?:\d+)', q_zh)
    if data_match:
        nums = [int(n.strip()) for n in data_match[0].split(',')]
        total = sum(nums)
        count = len(nums)
        zh = f"平均數 = 所有數嘅總和 ÷ 數嘅個數\n數據：{', '.join(map(str, nums))}\n總和 = {total}\n個數 = {count}\n平均數 = {total} ÷ {count} = {ans}"
        en = f"Mean = Sum ÷ Count\nData: {', '.join(map(str, nums))}\nSum = {total}\nCount = {count}\nMean = {total} ÷ {count} = {ans}"
    elif '5個數' in q_zh or '4個' in q_zh:
        zh = f"用平均數公式反推。\n平均數 = 總和 ÷ 個數\n總和 = 平均數 × 個數\n答案 = {ans}"
        en = f"Use mean formula in reverse.\nMean = Sum ÷ Count\nSum = Mean × Count\nAnswer = {ans}"
    elif '三科' in q_zh or '中文' in q_zh:
        scores = re.findall(r'(?:中文|英文|數學) (\d+) 分', q_zh)
        if scores:
            nums = [int(s) for s in scores]
            total = sum(nums)
            zh = f"三科平均分 = ({' + '.join(map(str, nums))}) ÷ 3\n= {total} ÷ 3 = {ans}"
            en = f"Average = ({' + '.join(map(str, nums))}) ÷ 3\n= {total} ÷ 3 = {ans}"
        else:
            zh = f"計算各科分數嘅平均。\n答案 = {ans}"
            en = f"Calculate average of scores.\nAnswer = {ans}"
    elif '考試' in q_zh:
        scores = re.findall(r'攞咗 ([\d, ]+) 分', q_zh)
        if scores:
            nums = [int(s.strip()) for s in scores[0].split(',')]
            total = sum(nums)
            count = len(nums)
            zh = f"平均分 = ({' + '.join(map(str, nums))}) ÷ {count}\n= {total} ÷ {count} = {ans}"
            en = f"Average = ({' + '.join(map(str, nums))}) ÷ {count}\n= {total} ÷ {count} = {ans}"
        else:
            zh = f"計算考試分數嘅平均。\n答案 = {ans}"
            en = f"Calculate average score.\nAnswer = {ans}"
    else:
        zh = f"平均數 = 總和 ÷ 個數。\n答案 = {ans}"
        en = f"Mean = Sum ÷ Count.\nAnswer = {ans}"
    return zh, en

def explain_median(q_zh, q_en, ans, opts, correct_idx):
    """中位數"""
    nums = sorted([int(n) for n in re.findall(r'\d+', q_zh) if 10 <= int(n) <= 99])
    if nums:
        mid = len(nums) // 2
        zh = f"中位數：將數據由細到大排列後，最中間嘅數。\n排列：{', '.join(map(str, nums))}\n共 {len(nums)} 個數，第 {mid+1} 個 = {ans}"
        en = f"Median: the middle value when data is sorted.\nSorted: {', '.join(map(str, nums))}\n{len(nums)} numbers, position {mid+1} = {ans}"
    else:
        zh = f"將數據由細到大排列，搵最中間嘅數。\n答案 = {ans}"
        en = f"Sort data ascending, find the middle value.\nAnswer = {ans}"
    return zh, en

def explain_mode(q_zh, q_en, ans, opts, correct_idx):
    """眾數"""
    zh = f"眾數係出現次數最多嘅數。\n逐一數每個數出現嘅次數，出現最多嘅就係眾數。\n答案 = {ans}"
    en = f"Mode is the most frequently occurring value.\nCount occurrences of each number.\nAnswer = {ans}"
    return zh, en

def explain_probability(q_zh, q_en, ans, opts, correct_idx):
    """概率"""
    zh = f"概率 = 有利結果數 ÷ 總結果數\n計算後約分得到最簡分數。\n答案 = {ans}"
    en = f"Probability = favorable outcomes ÷ total outcomes\nSimplify the fraction.\nAnswer = {ans}"
    return zh, en

def explain_linear_eq(q_zh, q_en, ans, opts, correct_idx):
    """一元一次方程"""
    eq = q_zh.replace('解方程 ', '').replace('Solve ', '')
    if '小明' in q_zh or '買' in q_zh:
        zh = f"將文字題轉化為方程求解。\n設未知數，列方程，解方程。\n答案 = {ans}"
        en = f"Convert word problem to equation.\nSet up and solve.\nAnswer = {ans}"
    else:
        zh = f"解方程：{eq}\n步驟：\n1. 將常數移到等號右邊\n2. 將未知數項合併\n3. 求 x 嘅值\nx = {ans}"
        en = f"Solve: {eq}\nSteps:\n1. Move constants to right side\n2. Combine like terms\n3. Find x\nx = {ans}"
    return zh, en

def explain_simplify(q_zh, q_en, ans, opts, correct_idx):
    """簡化代數式"""
    expr = q_zh.replace('簡化 ', '').replace('Simplify ', '')
    zh = f"合併同類項。\n{expr}\n將 x 嘅係數加減合併。\n答案 = {ans}"
    en = f"Combine like terms.\n{expr}\nCombine coefficients of x.\nAnswer = {ans}"
    return zh, en

def explain_expand(q_zh, q_en, ans, opts, correct_idx):
    """展開"""
    expr = q_zh.replace('展開 ', '').replace('Expand ', '')
    zh = f"用分配律展開括號。\n{expr}\n將括號外嘅數乘入括號內每一項。\n答案 = {ans}"
    en = f"Expand using distributive property.\n{expr}\nMultiply outside term by each inside term.\nAnswer = {ans}"
    return zh, en

def explain_substitution(q_zh, q_en, ans, opts, correct_idx):
    """代入求值"""
    zh = f"將已知數值代入表達式計算。\n逐步代入並計算。\n答案 = {ans}"
    en = f"Substitute the given value and calculate.\nStep by step substitution.\nAnswer = {ans}"
    return zh, en

def explain_inequalities(q_zh, q_en, ans, opts, correct_idx):
    """不等式"""
    eq = q_zh.replace('解不等式 ', '').replace('Solve ', '')
    zh = f"解不等式：{eq}\n步驟同解方程相似，但要注意：\n乘除負數時要反轉不等號方向。\n答案：{ans}"
    en = f"Solve: {eq}\nSimilar to equation solving, but:\nFlip inequality when multiplying/dividing by negative.\nAnswer: {ans}"
    return zh, en

def explain_distance(q_zh, q_en, ans, opts, correct_idx):
    """距離"""
    coords = re.findall(r'\([-?\d,]+\)', q_zh)
    if len(coords) >= 2:
        zh = f"用距離公式：d = √[(x₂-x₁)² + (y₂-y₁)²]\n兩點：{coords[0]} 和 {coords[1]}\n代入公式計算 = {ans}"
        en = f"Distance formula: d = √[(x₂-x₁)² + (y₂-y₁)²]\nPoints: {coords[0]} and {coords[1]}\n= {ans}"
    else:
        zh = f"用距離公式計算兩點之間嘅距離。\n答案 = {ans}"
        en = f"Calculate distance between two points.\nAnswer = {ans}"
    return zh, en

def explain_midpoint(q_zh, q_en, ans, opts, correct_idx):
    """中點"""
    coords = re.findall(r'\([-?\d,]+\)', q_zh)
    if len(coords) >= 2:
        zh = f"用中點公式：M = ((x₁+x₂)/2, (y₁+y₂)/2)\n兩點：{coords[0]} 和 {coords[1]}\n代入公式計算 = {ans}"
        en = f"Midpoint formula: M = ((x₁+x₂)/2, (y₁+y₂)/2)\nPoints: {coords[0]} and {coords[1]}\n= {ans}"
    else:
        zh = f"用中點公式計算。\n答案 = {ans}"
        en = f"Use midpoint formula.\nAnswer = {ans}"
    return zh, en

def explain_triangles(q_zh, q_en, ans, opts, correct_idx):
    """三角形"""
    if '等邊' in q_zh:
        zh = f"等邊三角形三個角相等。\n三角形內角和 = 180°\n每個角 = 180° ÷ 3 = 60°"
        en = f"Equilateral triangle: all angles equal.\nSum of angles = 180°\nEach angle = 180° ÷ 3 = 60°"
    elif '等腰' in q_zh:
        vertex = re.search(r'頂角 (\d+)°', q_zh)
        if vertex:
            v = int(vertex.group(1))
            base = (180 - v) // 2
            zh = f"等腰三角形兩底角相等。\n三角形內角和 = 180°\n頂角 = {v}°\n底角 = (180° - {v}°) ÷ 2 = {base}°"
            en = f"Isosceles: two base angles equal.\nSum = 180°\nVertex = {v}°\nBase angle = (180° - {v}°) ÷ 2 = {base}°"
        else:
            zh = f"利用等腰三角形性質計算。\n答案 = {ans}"
            en = f"Use isosceles triangle property.\nAnswer = {ans}"
    elif '直角' in q_zh:
        angle = re.search(r'銳角 (\d+)°', q_zh)
        if angle:
            a = int(angle.group(1))
            zh = f"直角三角形有一個 90° 角。\n三角形內角和 = 180°\n另一銳角 = 180° - 90° - {a}° = {ans}°"
            en = f"Right triangle has a 90° angle.\nSum = 180°\nOther acute = 180° - 90° - {a}° = {ans}°"
        else:
            zh = f"利用直角三角形性質計算。\n答案 = {ans}"
            en = f"Use right triangle property.\nAnswer = {ans}"
    else:
        angles = re.findall(r'(\d+)°', q_zh)
        if len(angles) >= 2:
            a, b = int(angles[0]), int(angles[1])
            zh = f"三角形內角和 = 180°\n已知兩角：{a}° 和 {b}°\n第三角 = 180° - {a}° - {b}° = {ans}°"
            en = f"Sum of triangle angles = 180°\nKnown: {a}° and {b}°\nThird = 180° - {a}° - {b}° = {ans}°"
        else:
            zh = f"利用三角形內角和 = 180° 計算。\n答案 = {ans}"
            en = f"Triangle angle sum = 180°.\nAnswer = {ans}"
    return zh, en

def explain_angles(q_zh, q_en, ans, opts, correct_idx):
    """角"""
    if '互補' in q_zh and '180' not in q_zh:
        angle = re.search(r'(\d+)°', q_zh)
        if angle:
            a = int(angle.group(1))
            zh = f"互補兩角之和 = 90°\n已知一角 = {a}°\n另一角 = 90° - {a}° = {ans}°"
            en = f"Complementary angles sum to 90°\nKnown: {a}°\nOther = 90° - {a}° = {ans}°"
        else:
            zh = f"互補兩角之和 = 90°\n答案 = {ans}"
            en = f"Complementary angles sum to 90°\nAnswer = {ans}"
    elif '互補' in q_zh or '互 supplementary' in q_en:
        angle = re.search(r'(\d+)°', q_zh)
        if angle:
            a = int(angle.group(1))
            zh = f"互補（supplementary）兩角之和 = 180°\n已知一角 = {a}°\n另一角 = 180° - {a}° = {ans}°"
            en = f"Supplementary angles sum to 180°\nKnown: {a}°\nOther = 180° - {a}° = {ans}°"
        else:
            zh = f"互補兩角之和 = 180°\n答案 = {ans}"
            en = f"Supplementary angles sum to 180°\nAnswer = {ans}"
    elif '對頂角' in q_zh:
        zh = f"對頂角相等。\n答案 = {ans}°"
        en = f"Vertical angles are equal.\nAnswer = {ans}°"
    else:
        zh = f"利用角度關係計算。\n答案 = {ans}"
        en = f"Use angle relationships.\nAnswer = {ans}"
    return zh, en

def explain_parallel(q_zh, q_en, ans, opts, correct_idx):
    """平行線"""
    angle = re.search(r'(\d+)°', q_zh)
    a = int(angle.group(1)) if angle else 0
    if '同位角' in q_zh:
        zh = f"平行線嘅同位角相等。\n已知角 = {a}°\n同位角 = {a}°"
        en = f"Corresponding angles are equal (parallel lines).\nGiven: {a}°\nCorresponding angle = {a}°"
    elif '內錯角' in q_zh:
        zh = f"平行線嘅內錯角相等。\n已知角 = {a}°\n內錯角 = {a}°"
        en = f"Alternate interior angles are equal.\nGiven: {a}°\nAlternate angle = {a}°"
    elif '同旁內角' in q_zh:
        zh = f"平行線嘅同旁內角互補（和為 180°）。\n已知角 = {a}°\n同旁內角 = 180° - {a}° = {ans}°"
        en = f"Co-interior angles are supplementary (sum to 180°).\nGiven: {a}°\nCo-interior = 180° - {a}° = {ans}°"
    else:
        zh = f"利用平行線性質計算角度。\n答案 = {ans}°"
        en = f"Use parallel line properties.\nAnswer = {ans}°"
    return zh, en

def explain_polygons(q_zh, q_en, ans, opts, correct_idx):
    """多邊形"""
    sides = re.search(r'(\d+) 邊形', q_zh)
    n = int(sides.group(1)) if sides else 0
    if '內角和' in q_zh:
        zh = f"n 邊形內角和 = (n-2) × 180°\n{n} 邊形 = ({n}-2) × 180° = {n-2} × 180° = {ans}°"
        en = f"Interior angle sum = (n-2) × 180°\n{n}-gon = ({n}-2) × 180° = {ans}°"
    elif '外角和' in q_zh:
        zh = f"任何凸多邊形嘅外角和都係 360°。\n答案 = 360°"
        en = f"Sum of exterior angles of any convex polygon = 360°.\nAnswer = 360°"
    elif '每個外角' in q_zh:
        zh = f"正 {n} 邊形每個外角 = 360° ÷ {n} = {ans}°"
        en = f"Regular {n}-gon: each exterior angle = 360° ÷ {n} = {ans}°"
    elif '每個內角' in q_zh:
        zh = f"正 {n} 邊形每個內角 = ({n}-2) × 180° ÷ {n} = {ans}°"
        en = f"Regular {n}-gon: each interior angle = ({n}-2) × 180° ÷ {n} = {ans}°"
    elif '對角線' in q_zh:
        zh = f"n 邊形對角線數目 = n(n-3) ÷ 2\n{n} 邊形 = {n}×({n}-3) ÷ 2 = {n*(n-3)} ÷ 2 = {ans}"
        en = f"Diagonals = n(n-3) ÷ 2\n{n}-gon = {n}×({n}-3) ÷ 2 = {ans}"
    else:
        zh = f"利用多邊形性質計算。\n答案 = {ans}"
        en = f"Use polygon properties.\nAnswer = {ans}"
    return zh, en

def explain_area(q_zh, q_en, ans, opts, correct_idx):
    """面積"""
    if '長方形' in q_zh:
        dims = re.findall(r'(\d+)', q_zh)
        zh = f"長方形面積 = 長 × 闊\n= {dims[0]} × {dims[1]} = {ans} cm²"
        en = f"Rectangle area = length × width\n= {dims[0]} × {dims[1]} = {ans} cm²"
    elif '三角形' in q_zh:
        dims = re.findall(r'(\d+)', q_zh)
        zh = f"三角形面積 = 底 × 高 ÷ 2\n= {dims[0]} × {dims[1]} ÷ 2 = {ans} cm²"
        en = f"Triangle area = base × height ÷ 2\n= {dims[0]} × {dims[1]} ÷ 2 = {ans} cm²"
    elif '圓形' in q_zh:
        r = re.search(r'半徑 (\d+)', q_zh)
        r = int(r.group(1)) if r else 0
        zh = f"圓形面積 = πr²\n= 3.14 × {r}² = 3.14 × {r*r} = {ans} cm²"
        en = f"Circle area = πr²\n= 3.14 × {r}² = {ans} cm²"
    elif '正方形' in q_zh:
        s = re.search(r'邊長 (\d+)', q_zh)
        s = int(s.group(1)) if s else 0
        zh = f"正方形面積 = 邊長²\n= {s}² = {ans} cm²"
        en = f"Square area = side²\n= {s}² = {ans} cm²"
    elif '平行四邊形' in q_zh:
        dims = re.findall(r'(\d+)', q_zh)
        zh = f"平行四邊形面積 = 底 × 高\n= {dims[0]} × {dims[1]} = {ans} cm²"
        en = f"Parallelogram area = base × height\n= {dims[0]} × {dims[1]} = {ans} cm²"
    else:
        zh = f"用對應嘅面積公式計算。\n答案 = {ans} cm²"
        en = f"Use the appropriate area formula.\nAnswer = {ans} cm²"
    return zh, en

def explain_volume(q_zh, q_en, ans, opts, correct_idx):
    """體積"""
    if '長方體' in q_zh:
        dims = re.findall(r'(\d+)', q_zh)
        zh = f"長方體體積 = 長 × 闊 × 高\n= {dims[0]} × {dims[1]} × {dims[2]} = {ans} cm³"
        en = f"Cuboid volume = l × w × h\n= {dims[0]} × {dims[1]} × {dims[2]} = {ans} cm³"
    elif '正方體' in q_zh:
        s = re.search(r'邊長 (\d+)', q_zh)
        s = int(s.group(1)) if s else 0
        zh = f"正方體體積 = 邊長³\n= {s}³ = {ans} cm³"
        en = f"Cube volume = side³\n= {s}³ = {ans} cm³"
    elif '圓柱' in q_zh:
        r = re.search(r'半徑 (\d+)', q_zh)
        h = re.search(r'高 (\d+)', q_zh)
        r = int(r.group(1)) if r else 0
        h = int(h.group(1)) if h else 0
        zh = f"圓柱體積 = πr²h\n= 3.14 × {r}² × {h}\n= 3.14 × {r*r} × {h} = {ans} cm³"
        en = f"Cylinder volume = πr²h\n= 3.14 × {r}² × {h} = {ans} cm³"
    elif '三角柱' in q_zh:
        dims = re.findall(r'(\d+)', q_zh)
        zh = f"三角柱體積 = 三角形面積 × 柱長\n= (底×高÷2) × 長\n= ({dims[0]}×{dims[1]}÷2) × {dims[2]} = {ans} cm³"
        en = f"Triangular prism volume = triangle area × length\n= ({dims[0]}×{dims[1]}÷2) × {dims[2]} = {ans} cm³"
    else:
        zh = f"用對應嘅體積公式計算。\n答案 = {ans} cm³"
        en = f"Use the appropriate volume formula.\nAnswer = {ans} cm³"
    return zh, en

def explain_ratio_simplify(q_zh, q_en, ans, opts, correct_idx):
    """簡化比"""
    ratio = re.search(r'(\d+):(\d+)', q_zh)
    if ratio:
        a, b = int(ratio.group(1)), int(ratio.group(2))
        g = math.gcd(a, b)
        zh = f"簡化比 {a}:{b}\n搵最大公因數 GCF({a},{b}) = {g}\n{a}÷{g} : {b}÷{g} = {ans}"
        en = f"Simplify {a}:{b}\nGCF({a},{b}) = {g}\n{a}÷{g} : {b}÷{g} = {ans}"
    else:
        zh = f"搵兩數嘅最大公因數，然後各自除以 GCF。\n答案 = {ans}"
        en = f"Find GCF of both numbers, then divide each by GCF.\nAnswer = {ans}"
    return zh, en

def explain_ratio_sharing(q_zh, q_en, ans, opts, correct_idx):
    """按比分配"""
    total_match = re.search(r'\$(\d+)', q_zh)
    ratio_match = re.search(r'(\d+):(\d+)', q_zh)
    if total_match and ratio_match:
        total = int(total_match.group(1))
        a, b = int(ratio_match.group(1)), int(ratio_match.group(2))
        g = math.gcd(a, b)
        a2, b2 = a // g, b // g
        share_a = total * a2 // (a2 + b2)
        share_b = total * b2 // (a2 + b2)
        if '甲' in q_zh and '乙' in q_zh:
            target = '甲' if '甲得' in q_zh else '乙'
            zh = f"按比 {a2}:{b2} 分配 ${total}。\n總份數 = {a2} + {b2} = {a2+b2}\n每份 = ${total} ÷ {a2+b2} = ${total//(a2+b2)}\n{target}得 = ${total//(a2+b2)} × {a2 if target=='甲' else b2} = ${ans}"
            en = f"Share ${total} in ratio {a2}:{b2}.\nTotal parts = {a2+b2}\nEach part = ${total//(a2+b2)}\nAnswer = ${ans}"
        else:
            zh = f"按比分配。\n答案 = ${ans}"
            en = f"Share in ratio.\nAnswer = ${ans}"
    else:
        zh = f"按比分配計算。\n答案 = {ans}"
        en = f"Ratio sharing calculation.\nAnswer = {ans}"
    return zh, en

def explain_sdt(q_zh, q_en, ans, opts, correct_idx):
    """行程問題"""
    if '速度' in q_zh or 'speed' in q_en.lower():
        zh = f"速度 = 距離 ÷ 時間\n代入數值計算 = {ans} km/h"
        en = f"Speed = Distance ÷ Time\n= {ans} km/h"
    elif '距離' in q_zh or 'distance' in q_en.lower():
        zh = f"距離 = 速度 × 時間\n代入數值計算 = {ans} km"
        en = f"Distance = Speed × Time\n= {ans} km"
    else:
        zh = f"時間 = 距離 ÷ 速度\n代入數值計算 = {ans} h"
        en = f"Time = Distance ÷ Speed\n= {ans} h"
    return zh, en

def explain_shopping(q_zh, q_en, ans, opts, correct_idx):
    """購物"""
    if '折前' in q_zh:
        zh = f"折前總價 = 單價 × 數量\n答案 = ${ans}"
        en = f"Subtotal = price × quantity\nAnswer = ${ans}"
    elif '折咗幾多' in q_zh or '平咗幾多' in q_zh:
        zh = f"折扣金額 = 折前總價 × 折扣百分比\n答案 = ${ans}"
        en = f"Discount = subtotal × discount rate\nAnswer = ${ans}"
    else:
        zh = f"先計折前總價（單價 × 數量），再乘以折扣率。\n折後價 = 折前總價 × (1 - 折扣%)\n答案 = ${ans}"
        en = f"Calculate subtotal, then apply discount.\nFinal = subtotal × (1 - discount%)\nAnswer = ${ans}"
    return zh, en

def explain_age(q_zh, q_en, ans, opts, correct_idx):
    """年齡問題"""
    if '後' in q_zh:
        zh = f"幾年後嘅年齡 = 而家嘅年齡 + 年數\n答案 = {ans} 歲"
        en = f"Future age = current age + years\nAnswer = {ans}"
    else:
        zh = f"幾年前嘅年齡 = 而家嘅年齡 - 年數\n答案 = {ans} 歲"
        en = f"Past age = current age - years\nAnswer = {ans}"
    return zh, en

def explain_work(q_zh, q_en, ans, opts, correct_idx):
    """工程問題"""
    if '每小時做' in q_zh:
        zh = f"工作量 = 每小時產量 × 小時數\n答案 = {ans}"
        en = f"Output = rate per hour × hours\nAnswer = {ans}"
    elif '平均分做' in q_zh:
        zh = f"每人工作量 = 總工作量 ÷ 人數\n答案 = {ans}"
        en = f"Per person = total ÷ number of workers\nAnswer = {ans}"
    elif '合作' in q_zh and '小時' in q_zh:
        zh = f"合作效率 = 甲效率 + 乙效率\n甲效率 = 1/甲所需時間，乙效率 = 1/乙所需時間\n合作時間 = 1 ÷ 合作效率\n答案 = {ans} 小時"
        en = f"Combined rate = rate_A + rate_B\nTime = 1 ÷ combined rate\nAnswer = {ans} hours"
    else:
        zh = f"利用工作效率公式計算。\n答案 = {ans}"
        en = f"Use work rate formula.\nAnswer = {ans}"
    return zh, en

def explain_pct_basic(q_zh, q_en, ans, opts, correct_idx):
    """百分數計算"""
    if '佔' in q_zh:
        zh = f"百分比 = (部分 ÷ 整體) × 100%\n答案 = {ans}%"
        en = f"Percentage = (part ÷ whole) × 100%\nAnswer = {ans}%"
    elif '幾多人' in q_zh or '幾多' in q_zh:
        zh = f"人數 = 總人數 × 百分比\n答案 = {ans} 人"
        en = f"Count = total × percentage\nAnswer = {ans}"
    else:
        nums = re.findall(r'(\d+)', q_zh)
        if len(nums) >= 2:
            zh = f"計算百分數：{nums[0]} × {nums[1]}%\n= {nums[0]} × {nums[1]}/100\n= {ans}"
            en = f"Calculate: {nums[0]} × {nums[1]}%\n= {nums[0]} × {nums[1]}/100\n= {ans}"
        else:
            zh = f"用百分數公式計算。\n答案 = {ans}"
            en = f"Use percentage formula.\nAnswer = {ans}"
    return zh, en

def explain_pct_change(q_zh, q_en, ans, opts, correct_idx):
    """百分數增減"""
    if '加價' in q_zh:
        zh = f"加價後售價 = 原價 × (1 + 加價百分比)\n答案 = ${ans}"
        en = f"New price = original × (1 + increase%)\nAnswer = ${ans}"
    elif '減價' in q_zh and '平咗' not in q_zh and '原價' not in q_zh:
        zh = f"減價後售價 = 原價 × (1 - 減價百分比)\n答案 = ${ans}"
        en = f"Sale price = original × (1 - discount%)\nAnswer = ${ans}"
    elif '平咗' in q_zh or '平咗' in q_zh:
        zh = f"折扣金額 = 原價 × 折扣百分比\n答案 = ${ans}"
        en = f"Savings = original × discount%\nAnswer = ${ans}"
    elif '原價' in q_zh:
        zh = f"原價 = 折後價 ÷ (1 - 折扣百分比)\n答案 = ${ans}"
        en = f"Original = sale price ÷ (1 - discount%)\nAnswer = ${ans}"
    else:
        zh = f"用百分數增減公式計算。\n答案 = {ans}"
        en = f"Use percentage change formula.\nAnswer = {ans}"
    return zh, en

def explain_arithmetic(q_zh, q_en, ans, opts, correct_idx):
    """等差數列"""
    seq_match = re.findall(r'(\d+)', q_zh)
    if len(seq_match) >= 5:
        nums = [int(x) for x in seq_match[:4]]
        diff = nums[1] - nums[0]
        term = int(seq_match[-1]) if '第' in q_zh else 0
        first = nums[0]
        zh = f"等差數列公差 d = {diff}\n通項公式：aₙ = a₁ + (n-1)d\n第 {term} 項 = {first} + ({term}-1) × {diff}\n= {first} + {(term-1)*diff} = {ans}"
        en = f"Common difference d = {diff}\nFormula: aₙ = a₁ + (n-1)d\nTerm {term} = {first} + ({term}-1) × {diff}\n= {ans}"
    else:
        zh = f"搵公差，用通項公式計算。\n答案 = {ans}"
        en = f"Find common difference, use formula.\nAnswer = {ans}"
    return zh, en

def explain_patterns(q_zh, q_en, ans, opts, correct_idx):
    """規律"""
    zh = f"觀察數列嘅規律（等差、等比、平方數等），推算下一個數。\n答案 = {ans}"
    en = f"Observe the pattern (arithmetic, geometric, squares, etc.), find the next number.\nAnswer = {ans}"
    return zh, en


# Map topic_id/subtopic_id to explanation functions
EXPLAINERS = {
    ('directed_number', 'bodmas'): explain_bodmas,
    ('directed_number', 'fractions'): explain_fractions,
    ('directed_number', 'hcf_lcm'): explain_hcf_lcm,
    ('directed_number', 'absolute'): explain_absolute,
    ('directed_number', 'powers'): explain_powers,
    ('statistics', 'mean'): explain_mean,
    ('statistics', 'median'): explain_median,
    ('statistics', 'mode'): explain_mode,
    ('statistics', 'probability'): explain_probability,
    ('basic_algebra', 'linear_eq'): explain_linear_eq,
    ('basic_algebra', 'simplify'): explain_simplify,
    ('basic_algebra', 'expand'): explain_expand,
    ('basic_algebra', 'substitution'): explain_substitution,
    ('basic_algebra', 'inequalities'): explain_inequalities,
    ('coordinates', 'distance'): explain_distance,
    ('coordinates', 'midpoint'): explain_midpoint,
    ('basic_geometry', 'triangles'): explain_triangles,
    ('basic_geometry', 'angles'): explain_angles,
    ('basic_geometry', 'parallel'): explain_parallel,
    ('basic_geometry', 'polygons'): explain_polygons,
    ('area_volume', 'area'): explain_area,
    ('area_volume', 'volume'): explain_volume,
    ('ratio_rate', 'simplify'): explain_ratio_simplify,
    ('ratio_rate', 'sharing'): explain_ratio_sharing,
    ('ratio_rate', 'sdt'): explain_sdt,
    ('mixed', 'shopping'): explain_shopping,
    ('mixed', 'age'): explain_age,
    ('mixed', 'work'): explain_work,
    ('percentages', 'basic'): explain_pct_basic,
    ('percentages', 'change'): explain_pct_change,
    ('sequences', 'arithmetic'): explain_arithmetic,
    ('sequences', 'patterns'): explain_patterns,
}


def improve_explanations(filepath):
    """Improve all explanations in a question file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    improved = 0
    for q in data:
        key = (q.get('topic_id', ''), q.get('subtopic_id', ''))
        explainer = EXPLAINERS.get(key)
        
        if explainer:
            ans_val = q['options_zh'][q['answer']] if q['answer'] < len(q['options_zh']) else '?'
            try:
                zh, en = explainer(
                    q.get('question_zh', ''),
                    q.get('question_en', ''),
                    ans_val,
                    q.get('options_zh', []),
                    q['answer']
                )
                q['explanation_zh'] = zh
                q['explanation_en'] = en
                improved += 1
            except Exception as e:
                # Keep existing explanation
                pass
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    
    return improved, len(data)


if __name__ == '__main__':
    files = [
        'math/s1/questions.json',
        'v2/math/s1/questions.json',
    ]
    
    for f in files:
        print(f'Improving explanations in {f}...')
        improved, total = improve_explanations(f)
        print(f'  Improved {improved}/{total} explanations')
    
    # Show sample
    with open('math/s1/questions.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print('\n=== Sample improved explanations ===')
    for q in data[:5]:
        print(f'Q: {q["question_zh"][:50]}')
        print(f'  ZH: {q["explanation_zh"][:80]}...')
        print(f'  EN: {q["explanation_en"][:80]}...')
        print()
    
    print('Done!')
