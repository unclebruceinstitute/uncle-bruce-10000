#!/usr/bin/env python3
"""Part 1A: Quadratic Equations & Functions, Functions & Graphs (~1000 questions)"""

import random, math

def fmt_coeff(a, b, c):
    """Format ax² + bx + c = 0"""
    parts = []
    if a == 1: parts.append("x²")
    elif a == -1: parts.append("-x²")
    else: parts.append(f"{a}x²")
    if b > 0:
        parts.append(f"+ {b}x" if b != 1 else "+ x")
    elif b < 0:
        parts.append(f"- {abs(b)}x" if b != -1 else "- x")
    if c > 0: parts.append(f"+ {c}")
    elif c < 0: parts.append(f"- {abs(c)}")
    return "".join(parts) + " = 0"

def fmt_coeff_en(a, b, c):
    return fmt_coeff(a, b, c)  # Same for equations

def gen_quadratic(Q, start_id):
    """Generate ~500 quadratic equation questions"""
    TID = "quadratic_equations"
    TZH = "二次方程"; TEN = "Quadratic Equations"
    qid = start_id

    # --- 1. Solving by factorization (80) ---
    for _ in range(80):
        a = random.choice([1, 1, 1, 2])
        r1 = random.randint(-6, 6)
        r2 = random.randint(-6, 6)
        while r1 == r2: r2 = random.randint(-6, 6)
        ba = -a*(r1+r2); ca = a*r1*r2
        if a > 1:
            disc = ba*ba - 4*a*ca
            if disc < 0: continue
            sd = int(math.isqrt(disc))
            if sd*sd != disc: continue
            x1 = (-ba+sd)/(2*a); x2 = (-ba-sd)/(2*a)
            if x1 != int(x1) or x2 != int(x2): continue
            r1, r2 = int(x1), int(x2)
        roots = sorted([r1, r2])
        eq = fmt_coeff(a, ba, ca)
        rs = f"x = {roots[0]} 或 x = {roots[1]}" if roots[0]!=roots[1] else f"x = {roots[0]}（重根）"
        rs_en = f"x = {roots[0]} or x = {roots[1]}" if roots[0]!=roots[1] else f"x = {roots[0]} (repeated root)"
        wrong1 = f"x = {-roots[0]} 或 x = {-roots[1]}" if roots[0]!=roots[1] else f"x = {-roots[0]}"
        wrong1e = f"x = {-roots[0]} or x = {-roots[1]}" if roots[0]!=roots[1] else f"x = {-roots[0]}"
        qid += 1
        Q.append({"id":qid,"topic_id":TID,"topic_zh":TZH,"topic_en":TEN,
            "subtopic_id":"solving_by_factorization","subtopic_zh":"因式分解法","subtopic_en":"Solving by Factorization",
            "question_zh":f"解方程 {eq}","question_en":f"Solve {eq}",
            "options_zh":[f"A. {rs}",f"B. {wrong1}",f"C. 無實數解",f"D. x = 0 或 x = 1"],
            "options_en":[f"A. {rs_en}",f"B. {wrong1e}",f"C. No real roots",f"D. x = 0 or x = 1"],
            "answer":0,
            "explanation_zh":f"因式分解得 a(x-{roots[0]})(x-{roots[1]})=0，解得 {rs}。" if a==1 else f"因式分解得 {a}(x-{roots[0]})(x-{roots[1]})=0，解得 {rs}。",
            "explanation_en":f"Factorizing gives roots {rs_en}." if a==1 else f"Factorizing gives {a}(x-{roots[0]})(x-{roots[1]})=0, so {rs_en}.",
            "difficulty":random.choice([1,1,1,2])})

    # --- 2. Discriminant (80) ---
    for _ in range(80):
        a = random.choice([1,2]); b = random.randint(-10,10); c = random.randint(-10,10)
        d = b*b - 4*a*c
        eq = fmt_coeff(a, b, c)
        if d > 0:
            sq = int(math.isqrt(d))
            if sq*sq == d:
                nz = "有兩個相異有理實數根"; ne = "two distinct rational real roots"
            else:
                nz = "有兩個相異無理實數根"; ne = "two distinct irrational real roots"
            dt = "Δ > 0"
        elif d == 0:
            nz = "有重根（兩個相等實數根）"; ne = "two equal real roots (repeated root)"; dt = "Δ = 0"
        else:
            nz = "沒有實數根"; ne = "no real roots"; dt = "Δ < 0"
        qid += 1
        Q.append({"id":qid,"topic_id":TID,"topic_zh":TZH,"topic_en":TEN,
            "subtopic_id":"discriminant","subtopic_zh":"判別式","subtopic_en":"Discriminant",
            "question_zh":f"方程 {eq} 的判別式 Δ 的值及根的性質為何？",
            "question_en":f"What is the discriminant Δ and nature of roots of {eq}?",
            "options_zh":[f"A. Δ = {d}，{nz}",f"B. Δ = {d+2}，有兩個相異實數根",f"C. Δ = {-d}，沒有實數根",f"D. Δ = {d-1}，有重根"],
            "options_en":[f"A. Δ = {d}, {ne}",f"B. Δ = {d+2}, two distinct real roots",f"C. Δ = {-d}, no real roots",f"D. Δ = {d-1}, repeated root"],
            "answer":0,
            "explanation_zh":f"Δ = ({b})² - 4({a})({c}) = {b*b} - {4*a*c} = {d}。{dt}，故{nz}。",
            "explanation_en":f"Δ = ({b})² - 4({a})({c}) = {b*b} - {4*a*c} = {d}. {dt}, so {ne}.",
            "difficulty":random.choice([1,1,2])})

    # --- 3. Nature of roots conditions (60) ---
    variants = [
        ("x² + kx + 4 = 0", "k² - 16 = 0", "k = ±4", "k = 4 或 k = -4", "k = 4 or k = -4", 1),
        ("2x² + kx + 8 = 0", "k² - 64 = 0", "k = ±8", "k = 8 或 k = -8", "k = 8 or k = -8", 1),
        ("x² + 6x + k = 0", "36 - 4k = 0", "k = 9", "k = 9", "k = 9", 1),
        ("kx² + 12x + 9 = 0", "144 - 36k = 0", "k = 4", "k = 4", "k = 4", 2),
        ("x² + kx + (k+2) = 0", "k² - 4k - 8 = 0", "k = 2±2√3", "k = 2+2√3 或 k = 2-2√3", "k = 2+2√3 or k = 2-2√3", 3),
        ("3x² + kx + 12 = 0", "k² - 144 = 0", "k = ±12", "k = 12 或 k = -12", "k = 12 or k = -12", 2),
        ("x² - 2kx + (k+6) = 0", "4k² - 4k - 24 = 0", "k = 3 或 k = -2", "k = 3 或 k = -2", "k = 3 or k = -2", 2),
    ]
    for _ in range(60):
        v = random.choice(variants)
        qid += 1
        Q.append({"id":qid,"topic_id":TID,"topic_zh":TZH,"topic_en":TEN,
            "subtopic_id":"nature_of_roots","subtopic_zh":"根的性質","subtopic_en":"Nature of Roots",
            "question_zh":f"若方程 {v[0]} 有重根，求 k 的值。",
            "question_en":f"If {v[0]} has equal roots, find the value(s) of k.",
            "options_zh":[f"A. {v[3]}",f"B. k = {random.randint(1,8)}",f"C. k = {random.randint(-8,-1)}",f"D. k = 0"],
            "options_en":[f"A. {v[4]}",f"B. k = {random.randint(1,8)}",f"C. k = {random.randint(-8,-1)}",f"D. k = 0"],
            "answer":0,
            "explanation_zh":f"令 Δ = 0，即 {v[1]}，解得 {v[3]}。",
            "explanation_en":f"Setting Δ = 0, i.e. {v[1]}, we get {v[4]}.",
            "difficulty":v[5]})

    # --- 4. Sum and product of roots (60) ---
    for _ in range(60):
        a = random.choice([1,1,2])
        r1 = random.randint(-5,5); r2 = random.randint(-5,5)
        while r1==r2: r2=random.randint(-5,5)
        s = r1+r2; p = r1*r2
        ba = -a*s; ca = a*p
        eq = fmt_coeff(a, ba, ca)
        qid += 1
        Q.append({"id":qid,"topic_id":TID,"topic_zh":TZH,"topic_en":TEN,
            "subtopic_id":"sum_product_roots","subtopic_zh":"根的和與積","subtopic_en":"Sum and Product of Roots",
            "question_zh":f"設 α 和 β 為方程 {eq} 的兩根，求 α + β 及 αβ。",
            "question_en":f"Let α and β be roots of {eq}. Find α + β and αβ.",
            "options_zh":[f"A. α+β={s}，αβ={p}",f"B. α+β={-s}，αβ={p}",f"C. α+β={s}，αβ={-p}",f"D. α+β={ba}，αβ={ca}"],
            "options_en":[f"A. α+β={s}, αβ={p}",f"B. α+β={-s}, αβ={p}",f"C. α+β={s}, αβ={-p}",f"D. α+β={ba}, αβ={ca}"],
            "answer":0,
            "explanation_zh":f"韋達定理：α+β = -b/a = {s}，αβ = c/a = {p}。",
            "explanation_en":f"Vieta's formulas: α+β = -b/a = {s}, αβ = c/a = {p}.",
            "difficulty":random.choice([1,2,2])})

    # --- 5. Quadratic graphs / vertex (60) ---
    for _ in range(60):
        a = random.choice([1,1,2,-1,-2])
        h = random.randint(-4,4); k = random.randint(-5,5)
        # y = a(x-h)² + k
        if a == 1: eq_s = "(x"
        elif a == -1: eq_s = "-(x"
        else: eq_s = f"{a}(x"
        eq_s += f" - {h})²" if h > 0 else f" + {abs(h)})²" if h < 0 else ")²"
        if k > 0: eq_s += f" + {k}"
        elif k < 0: eq_s += f" - {abs(k)}"
        mv = "最小值" if a > 0 else "最大值"
        mv_en = "minimum" if a > 0 else "maximum"
        qid += 1
        Q.append({"id":qid,"topic_id":TID,"topic_zh":TZH,"topic_en":TEN,
            "subtopic_id":"quadratic_graphs","subtopic_zh":"二次函數圖像","subtopic_en":"Graphs of Quadratic Functions",
            "question_zh":f"已知 y = {eq_s}，求頂點坐標及最值。",
            "question_en":f"Given y = {eq_s}, find the vertex and turning value.",
            "options_zh":[f"A. 頂點({h},{k})，{mv}={k}",f"B. 頂點({-h},{k})，{mv}={k}",f"C. 頂點({h},{-k})，{mv}={-k}",f"D. 頂點({0},{k})，{mv}={k}"],
            "options_en":[f"A. Vertex({h},{k}), {mv_en}={k}",f"B. Vertex({-h},{k}), {mv_en}={k}",f"C. Vertex({h},{-k}), {mv_en}={-k}",f"D. Vertex({0},{k}), {mv_en}={k}"],
            "answer":0,
            "explanation_zh":f"由 y = {eq_s} 可知頂點為 ({h}, {k})，{mv} = {k}。",
            "explanation_en":f"From y = {eq_s}, vertex is ({h}, {k}), {mv_en} = {k}.",
            "difficulty":random.choice([1,1,2])})

    # --- 6. Completing the square (60) ---
    for _ in range(60):
        a = random.choice([1,1,2])
        p = random.randint(1,6); q = random.randint(-5,5)
        ba = 2*a*p; ca = a*p*p+q
        orig = fmt_coeff(a, ba, ca)
        comp = f"{a}(x+{p})²" if a>1 else f"(x+{p})²" if p>0 else f"(x-{abs(p)})²"
        if q > 0: comp += f" + {q}"
        elif q < 0: comp += f" - {abs(q)}"
        qid += 1
        Q.append({"id":qid,"topic_id":TID,"topic_zh":TZH,"topic_en":TEN,
            "subtopic_id":"completing_square","subtopic_zh":"配方法","subtopic_en":"Completing the Square",
            "question_zh":f"將 y = {orig[:-3]} 配方為 y = a(x-h)² + k 的形式。",
            "question_en":f"Express y = {orig[:-3]} in the form y = a(x-h)² + k.",
            "options_zh":[f"A. y = {comp}",f"B. y = (x+{p+1})² + {q}",f"C. y = (x-{p})² + {q+1}",f"D. y = {a}(x+{p})² + {q+2}"],
            "options_en":[f"A. y = {comp}",f"B. y = (x+{p+1})² + {q}",f"C. y = (x-{p})² + {q+1}",f"D. y = {a}(x+{p})² + {q+2}"],
            "answer":0,
            "explanation_zh":f"配方：y = {orig[:-3]} = {comp}。",
            "explanation_en":f"Completing the square: y = {orig[:-3]} = {comp}.",
            "difficulty":random.choice([1,2,2])})

    # --- 7. Applications / word problems (100) ---
    for i in range(100):
        if i % 4 == 0:  # Projectile max height
            a_val = random.randint(1,3); v0 = random.randint(10,30); h0 = random.randint(0,10)
            t_max = v0/(2*a_val); h_max = h0 + v0*v0/(4*a_val)
            t_max_r = round(t_max,2); h_max_r = round(h_max,2)
            qid += 1
            Q.append({"id":qid,"topic_id":TID,"topic_zh":TZH,"topic_en":TEN,
                "subtopic_id":"quadratic_applications","subtopic_zh":"二次函數應用","subtopic_en":"Applications",
                "question_zh":f"一個球的高度 h（米）與時間 t（秒）的關係為 h = -{a_val}t² + {v0}t + {h0}。求最高高度。",
                "question_en":f"Height h(m) of a ball: h = -{a_val}t² + {v0}t + {h0}. Find maximum height.",
                "options_zh":[f"A. {h_max_r}米",f"B. {round(h_max_r+3,2)}米",f"C. {round(h_max_r-5,2)}米",f"D. {v0}米"],
                "options_en":[f"A. {h_max_r}m",f"B. {round(h_max_r+3,2)}m",f"C. {round(h_max_r-5,2)}m",f"D. {v0}m"],
                "answer":0,
                "explanation_zh":f"t = {v0}/{2×{a_val}} = {t_max_r}秒，h = {h_max_r}米。",
                "explanation_en":f"t = {v0}/(2×{a_val}) = {t_max_r}s, h = {h_max_r}m.",
                "difficulty":2})
        elif i % 4 == 1:  # Projectile ground time
            a_val = random.randint(1,3); v0 = random.randint(10,25); h0 = random.randint(2,8)
            disc = v0*v0 + 4*a_val*h0
            t_hit = round((v0 + math.sqrt(disc))/(2*a_val), 2)
            qid += 1
            Q.append({"id":qid,"topic_id":TID,"topic_zh":TZH,"topic_en":TEN,
                "subtopic_id":"quadratic_applications","subtopic_zh":"二次函數應用","subtopic_en":"Applications",
                "question_zh":f"一個球的高度 h（米）= -{a_val}t² + {v0}t + {h0}。何時著地？（取正數）",
                "question_en":f"Ball height h(m) = -{a_val}t² + {v0}t + {h0}. When does it hit the ground? (positive value)",
                "options_zh":[f"A. t = {t_hit}秒",f"B. t = {round(t_hit+1.5,2)}秒",f"C. t = {round(t_hit/2,2)}秒",f"D. t = {round(t_hit*1.5,2)}秒"],
                "options_en":[f"A. t = {t_hit}s",f"B. t = {round(t_hit+1.5,2)}s",f"C. t = {round(t_hit/2,2)}s",f"D. t = {round(t_hit*1.5,2)}s"],
                "answer":0,
                "explanation_zh":f"令 h=0，解二次方程取正根 t = {t_hit}秒。",
                "explanation_en":f"Setting h=0, positive root t = {t_hit}s.",
                "difficulty":2})
        elif i % 4 == 2:  # Rectangular area
            perim = random.choice([20,24,28,32,36,40])
            hp = perim // 2
            x = random.randint(3, hp-3)
            area = x * (hp - x)
            qid += 1
            Q.append({"id":qid,"topic_id":TID,"topic_zh":TZH,"topic_en":TEN,
                "subtopic_id":"quadratic_applications","subtopic_zh":"二次函數應用","subtopic_en":"Applications",
                "question_zh":f"長方形周界 {perim} 米，長為 x 米。面積 A 用 x 表示為何？",
                "question_en":f"Rectangle perimeter {perim}m, length x m. Express area A in terms of x.",
                "options_zh":[f"A. A = x({hp}-x)",f"B. A = x({perim}-x)",f"C. A = x({hp}-2x)",f"D. A = {hp}x - x²"],
                "options_en":[f"A. A = x({hp}-x)",f"B. A = x({perim}-x)",f"C. A = x({hp}-2x)",f"D. A = {hp}x - x²"],
                "answer":0,
                "explanation_zh":f"周界 = 2(長+寬) = {perim}，長+寬 = {hp}，寬 = {hp}-x，A = x({hp}-x)。",
                "explanation_en":f"Perimeter = 2(l+w) = {perim}, l+w = {hp}, w = {hp}-x, A = x({hp}-x).",
                "difficulty":2})
        else:  # Max area problem
            perim = random.choice([24,36,40,48])
            hp = perim // 2
            max_a = (hp//2)**2
            qid += 1
            Q.append({"id":qid,"topic_id":TID,"topic_zh":TZH,"topic_en":TEN,
                "subtopic_id":"quadratic_applications","subtopic_zh":"二次函數應用","subtopic_en":"Applications",
                "question_zh":f"長方形周界 {perim} 米，長闊均為正數。最大面積為多少？",
                "question_en":f"Rectangle perimeter {perim}m, positive sides. What is the maximum area?",
                "options_zh":[f"A. {max_a}平方米",f"B. {max_a+10}平方米",f"C. {hp}平方米",f.D. {perim}平方米"],
                "options_en":[f"A. {max_a} sq m",f"B. {max_a+10} sq m",f"C. {hp} sq m",f"D. {perim} sq m"],
                "answer":0,
                "explanation_zh":f"正方形時面積最大，邊長 = {hp}/2 = {hp//2}，面積 = {max_a}。",
                "explanation_en":f"Maximum when square, side = {hp}/2 = {hp//2}, area = {max_a}.",
                "difficulty":2})

    return qid

def gen_functions_graphs(Q, start_id):
    """Generate ~500 function & graph questions"""
    TID = "functions_and_graphs"
    TZH = "函數與圖像"; TEN = "Functions and Graphs"
    qid = start_id

    # --- 1. Domain and range (80) ---
    domain_variants = [
        ("f(x) = √(x - 3)", "x ≥ 3", "f(x) ≥ 0", "x ≥ 3, f(x) ≥ 0", "x ≥ 3, f(x) ≥ 0", "根號內須 ≥ 0，x - 3 ≥ 0 → x ≥ 3", "x - 3 ≥ 0 → x ≥ 3, range ≥ 0", 1),
        ("f(x) = √(2x + 6)", "x ≥ -3", "f(x) ≥ 0", "x ≥ -3, f(x) ≥ 0", "x ≥ -3, f(x) ≥ 0", "2x+6 ≥ 0 → x ≥ -3", "2x+6 ≥ 0 → x ≥ -3", 1),
        ("f(x) = 1/(x - 2)", "x ≠ 2", "f(x) ≠ 0", "x ≠ 2, f(x) ≠ 0", "x ≠ 2, f(x) ≠ 0", "分母 ≠ 0，x ≠ 2；分子為常數故 f(x) ≠ 0", "Denominator ≠ 0, x ≠ 2; numerator constant so f(x) ≠ 0", 2),
        ("f(x) = 1/(x² - 4)", "x ≠ ±2", "f(x) ≠ 0 且 f(x) ≥ 1/4 或 f(x) < 0", "x ≠ 2 且 x ≠ -2", "x ≠ 2 and x ≠ -2", "x²-4 ≠ 0 → x ≠ ±2", "x²-4 ≠ 0 → x ≠ ±2", 2),
        ("f(x) = √(4 - x²)", "-2 ≤ x ≤ 2", "0 ≤ f(x) ≤ 2", "-2 ≤ x ≤ 2, 0 ≤ f(x) ≤ 2", "-2 ≤ x ≤ 2, 0 ≤ f(x) ≤ 2", "4-x² ≥ 0 → -2 ≤ x ≤ 2", "4-x² ≥ 0 → -2 ≤ x ≤ 2", 2),
        ("f(x) = |x - 5|", "所有實數", "f(x) ≥ 0", "所有實數, f(x) ≥ 0", "All real numbers, f(x) ≥ 0", "絕對值函數定義域為所有實數，值域 ≥ 0", "Absolute value defined for all reals, range ≥ 0", 1),
    ]
    for _ in range(80):
        v = random.choice(domain_variants)
        qid += 1
        Q.append({"id":qid,"topic_id":TID,"topic_zh":TZH,"topic_en":TEN,
            "subtopic_id":"domain_range","subtopic_zh":"定義域與值域","subtopic_en":"Domain and Range",
            "question_zh":f"求函數 {v[0]} 的定義域和值域。",
            "question_en":f"Find the domain and range of {v[0]}.",
            "options_zh":[f"A. {v[3]}",f"B. x > 0, f(x) > 0",f.C. 所有實數",f.D. x ≠ 0"],
            "options_en":[f"A. {v[4]}",f"B. x > 0, f(x) > 0",f"C. All real numbers",f"D. x ≠ 0"],
            "answer":0,
            "explanation_zh":v[5],"explanation_en":v[6],"difficulty":v[7]})

    # --- 2. Composite functions (80) ---
    for _ in range(80):
        a1 = random.randint(1,5); b1 = random.randint(-5,5)
        a2 = random.randint(1,3); b2 = random.randint(-5,5)
        # f(x) = a1*x + b1, g(x) = a2*x + b2
        # f(g(x)) = a1*(a2*x+b2)+b1 = a1*a2*x + a1*b2 + b1
        ca = a1*a2; cb = a1*b2+b1
        qid += 1
        Q.append({"id":qid,"topic_id":TID,"topic_zh":TZH,"topic_en":TEN,
            "subtopic_id":"composite_functions","subtopic_zh":"複合函數","subtopic_en":"Composite Functions",
            "question_zh":f"若 f(x) = {a1}x + {b1} 及 g(x) = {a2}x + {b2}，求 f(g(x))。",
            "question_en":f"If f(x) = {a1}x + {b1} and g(x) = {a2}x + {b2}, find f(g(x)).",
            "options_zh":[f"A. {ca}x + {cb}",f"B. {a1*a2}x + {b1+b2}",f"C. {a1+a2}x + {b1*b2}",f.D. {a2*a1}x + {a2*b1+b2}"],
            "options_en":[f"A. {ca}x + {cb}",f"B. {a1*a2}x + {b1+b2}",f"C. {a1+a2}x + {b1*b2}",f"D. {a2*a1}x + {a2*b1+b2}"],
            "answer":0,
            "explanation_zh":f"f(g(x)) = {a1}({a2}x+{b2}) + {b1} = {ca}x + {cb}。",
            "explanation_en":f"f(g(x)) = {a1}({a2}x+{b2}) + {b1} = {ca}x + {cb}.",
            "difficulty":random.choice([1,2])})

    # --- 3. Inverse functions (80) ---
    for _ in range(80):
        a = random.choice([2,3,4,5,-2,-3])
        b = random.randint(-10,10)
        # f(x) = ax + b → f⁻¹(x) = (x-b)/a
        qid += 1
        Q.append({"id":qid,"topic_id":TID,"topic_zh":TZH,"topic_en":TEN,
            "subtopic_id":"inverse_functions","subtopic_zh":"反函數","subtopic_en":"Inverse Functions",
            "question_zh":f"若 f(x) = {a}x + {b}，求 f⁻¹(x)。",
            "question_en":f"If f(x) = {a}x + {b}, find f⁻¹(x).",
            "options_zh":[f"A. f⁻¹(x) = (x - {b})/{a}" if a>0 else f"A. f⁻¹(x) = (x - {b})/({a})",
                         f"B. f⁻¹(x) = (x + {b})/{a}",
                         f"C. f⁻¹(x) = {a}x - {b}",
                         f"D. f⁻¹(x) = x/{a} + {b}"],
            "options_en":[f"A. f⁻¹(x) = (x - {b})/{a}" if a>0 else f"A. f⁻¹(x) = (x - {b})/({a})",
                         f"B. f⁻¹(x) = (x + {b})/{a}",
                         f"C. f⁻¹(x) = {a}x - {b}",
                         f"D. f⁻¹(x) = x/{a} + {b}"],
            "answer":0,
            "explanation_zh":f"令 y = {a}x + {b}，解 x = (y-{b})/{a}，故 f⁻¹(x) = (x-{b})/{a}。",
            "explanation_en":f"Let y = {a}x + {b}, solve x = (y-{b})/{a}, so f⁻¹(x) = (x-{b})/{a}.",
            "difficulty":random.choice([1,2])})

    # --- 4. Polynomial functions (80) ---
    for _ in range(80):
        deg = random.choice([2,3])
        if deg == 2:
            a = random.choice([1,2,-1,-2])
            r1 = random.randint(-3,3); r2 = random.randint(-3,3)
            while r1==r2: r2=random.randint(-3,3)
            ba = -a*(r1+r2); ca = a*r1*r2
            eq_s = fmt_coeff(a, ba, ca).replace(" = 0","")
            qid += 1
            Q.append({"id":qid,"topic_id":TID,"topic_zh":TZH,"topic_en":TEN,
                "subtopic_id":"polynomial_functions","subtopic_zh":"多項式函數","subtopic_en":"Polynomial Functions",
                "question_zh":f"函數 y = {eq_s} 的圖像與 x 軸的交點為何？",
                "question_en":f"What are the x-intercepts of y = {eq_s}?",
                "options_zh":[f"A. ({r1}, 0) 和 ({r2}, 0)",f"B. ({-r1}, 0) 和 ({-r2}, 0)",f"C. (0, {ca})",f"D. 無交點 / No intercepts"],
                "options_en":[f"A. ({r1}, 0) and ({r2}, 0)",f"B. ({-r1}, 0) and ({-r2}, 0)",f"C. (0, {ca})",f"D. No intercepts"],
                "answer":0,
                "explanation_zh":f"令 y=0，解得 x={r1} 或 x={r2}。",
                "explanation_en":f"Setting y=0, x={r1} or x={r2}.",
                "difficulty":random.choice([1,2])})
        else:
            r1 = random.randint(-3,3); r2 = random.randint(-3,3); r3 = random.randint(-3,3)
            # (x-r1)(x-r2)(x-r3) = x³ - (r1+r2+r3)x² + (r1r2+r1r3+r2r3)x - r1r2r3
            s1 = r1+r2+r3; s2 = r1*r2+r1*r3+r2*r3; s3 = r1*r2*r3
            qid += 1
            Q.append({"id":qid,"topic_id":TID,"topic_zh":TZH,"topic_en":TEN,
                "subtopic_id":"polynomial_functions","subtopic_zh":"多項式函數","subtopic_en":"Polynomial Functions",
                "question_zh":f"已知 x³ + {-s1}x² + {s2}x + {-s3} = 0 的一個根為 x = {r1}，因式分解此方程。",
                "question_en":f"Given x³ + {-s1}x² + {s2}x + {-s3} = 0 has root x = {r1}, factorize.",
                "options_zh":[f"A. (x-{r1})(x-{r2})(x-{r3}) = 0",f"B. (x+{r1})(x-{r2})(x-{r3}) = 0",f"C. (x-{r1})(x²+{r2}x+{r3}) = 0",f.D. 無法因式分解"],
                "options_en":[f"A. (x-{r1})(x-{r2})(x-{r3}) = 0",f"B. (x+{r1})(x-{r2})(x-{r3}) = 0",f"C. (x-{r1})(x²+{r2}x+{r3}) = 0",f"D. Cannot be factorized"],
                "answer":0,
                "explanation_zh":f"因式分解得 (x-{r1})(x-{r2})(x-{r3}) = 0。",
                "explanation_en":f"Factorization gives (x-{r1})(x-{r2})(x-{r3}) = 0.",
                "difficulty":random.choice([2,2,3])})

    # --- 5. Transformations of graphs (80) ---
    for _ in range(80):
        transform_types = [
            ("y = f(x) + k", "向上平移 k 個單位", "Shift upwards by k units"),
            ("y = f(x) - k", "向下平移 k 個單位", "Shift downwards by k units"),
            ("y = f(x - h)", "向右平移 h 個單位", "Shift right by h units"),
            ("y = f(x + h)", "向左平移 h 個單位", "Shift left by h units"),
            ("y = -f(x)", "關於 x 軸對稱翻轉", "Reflection about x-axis"),
            ("y = f(-x)", "關於 y 軸對稱翻轉", "Reflection about y-axis"),
            ("y = af(x)，a > 1", "垂直方向拉伸 a 倍", "Vertical stretch by factor a"),
            ("y = f(2x)", "水平方向壓縮 1/2", "Horizontal compression by 1/2"),
        ]
        t = random.choice(transform_types)
        qid += 1
        Q.append({"id":qid,"topic_id":TID,"topic_zh":TZH,"topic_en":TEN,
            "subtopic_id":"graph_transformations","subtopic_zh":"圖像變換","subtopic_en":"Graph Transformations",
            "question_zh":f"由 y = f(x) 變換到 {t[0]}，圖像如何改變？",
            "question_en":f"How does the graph change from y = f(x) to {t[0]}?",
            "options_zh":[f"A. {t[1]}",f"B. 向下平移",f.C. 旋轉90度",f.D. 沒有改變"],
            "options_en":[f"A. {t[2]}",f"B. Shift downwards",f"C. Rotate 90°",f"D. No change"],
            "answer":0,
            "explanation_zh":f"{t[0]} 表示{t[1]}。",
            "explanation_en":f"{t[0]} means {t[2]}.",
            "difficulty":random.choice([1,1,2])})

    # --- 6. Even/odd functions (50) ---
    for _ in range(50):
        funcs = [
            ("f(x) = x²", "偶函數", "Even function", "f(-x) = (-x)² = x² = f(x)", "f(-x) = (-x)² = x² = f(x)"),
            ("f(x) = x⁴ + 1", "偶函數", "Even function", "f(-x) = x⁴ + 1 = f(x)", "f(-x) = x⁴ + 1 = f(x)"),
            ("f(x) = x³", "奇函數", "Odd function", "f(-x) = -x³ = -f(x)", "f(-x) = -x³ = -f(x)"),
            ("f(x) = x³ - x", "奇函數", "Odd function", "f(-x) = -x³ + x = -(x³-x) = -f(x)", "f(-x) = -x³ + x = -f(x)"),
            ("f(x) = |x|", "偶函數", "Even function", "f(-x) = |-x| = |x| = f(x)", "f(-x) = |-x| = |x| = f(x)"),
            ("f(x) = x² + x", "非奇非偶", "Neither even nor odd", "f(-x) = x² - x ≠ f(x) 且 ≠ -f(x)", "f(-x) = x² - x ≠ f(x) and ≠ -f(x)"),
        ]
        fn = random.choice(funcs)
        qid += 1
        Q.append({"id":qid,"topic_id":TID,"topic_zh":TZH,"topic_en":TEN,
            "subtopic_id":"even_odd_functions","subtopic_zh":"奇偶函數","subtopic_en":"Even and Odd Functions",
            "question_zh":f"判斷 {fn[0]} 是奇函數、偶函數還是兩者皆非。",
            "question_en":f"Determine if {fn[0]} is even, odd, or neither.",
            "options_zh":[f"A. {fn[1]}",f"B. {'偶函數' if fn[1]!='偶函數' else '奇函數'}",f.C. {'兩者皆是' if fn[1]!='非奇非偶' else '奇函數'}",f.D. 無法判斷"],
            "options_en":[f"A. {fn[2]}",f"B. {'Even function' if fn[2]!='Even function' else 'Odd function'}",f"C. {'Both' if fn[2]!='Neither even nor odd' else 'Odd function'}",f"D. Cannot determine"],
            "answer":0,
            "explanation_zh":f"驗證：{fn[3]}，故為{fn[1]}。",
            "explanation_en":f"Check: {fn[4]}, so it is a {fn[2]}.",
            "difficulty":random.choice([1,2])})

    # --- 7. Piecewise functions (50) ---
    for _ in range(50):
        a = random.randint(1,5); b = random.randint(-5,5); x0 = random.randint(0,5)
        qid += 1
        Q.append({"id":qid,"topic_id":TID,"topic_zh":TZH,"topic_en":TEN,
            "subtopic_id":"piecewise_functions","subtopic_zh":"分段函數","subtopic_en":"Piecewise Functions",
            "question_zh":f"設 f(x) = {{ x², x < {x0}; {a}x + {b}, x ≥ {x0} }}。求 f({x0})。",
            "question_en":f"Let f(x) = {{ x², x < {x0}; {a}x + {b}, x ≥ {x0} }}. Find f({x0}).",
            "options_zh":[f"A. {a*x0+b}",f"B. {x0*x0}",f.C. {a*(x0+1)+b}",f.D. 未定義"],
            "options_en":[f"A. {a*x0+b}",f.B. {x0*x0}",f"C. {a*(x0+1)+b}",f"D. Undefined"],
            "answer":0,
            "explanation_zh":f"因 {x0} ≥ {x0}，用第二段：f({x0}) = {a}×{x0} + {b} = {a*x0+b}。",
            "explanation_en":f"Since {x0} ≥ {x0}, use second piece: f({x0}) = {a}×{x0} + {b} = {a*x0+b}.",
            "difficulty":random.choice([1,2])})

    return qid

def generate_part1a(Q):
    qid = gen_quadratic_equations(Q, 0)
    print(f"  Quadratic equations: {qid} questions")
    qid2 = gen_functions_graphs(Q, qid)
    print(f"  Functions & graphs: {qid2 - qid} questions")
    return qid2
