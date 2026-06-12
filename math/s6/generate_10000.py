#!/usr/bin/env python3
"""
HKDSE Mathematics Compulsory Part — 10,000 Question Generator
Generates questions at proper HKDSE (S6) level with accurate answers.
"""
import json, random, math, sys, os

random.seed(42)
OUTPUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "questions.json")
Q = []
qid = 0

def add(tid, tz, te, sid, sz, se, qz, qe, oz, oe, ans, ez, ed, diff):
    global qid; qid += 1
    Q.append({"id":qid,"topic_id":tid,"topic_zh":tz,"topic_en":te,"subtopic_id":sid,
              "subtopic_zh":sz,"subtopic_en":se,"question_zh":qz,"question_en":qe,
              "options_zh":oz,"options_en":oe,"answer":ans,"explanation_zh":ez,"explanation_en":ed,"difficulty":diff})

def fe(a, b, c):
    """Format ax²+bx+c=0"""
    p = []
    if a == 1: p.append("x\u00b2")
    elif a == -1: p.append("-x\u00b2")
    else: p.append(f"{a}x\u00b2")
    if b > 0: p.append(f"+{b}x" if b != 1 else "+x")
    elif b < 0: p.append(f"{b}x" if b == -1 else f"-{abs(b)}x")
    if c > 0: p.append(f"+{c}")
    elif c < 0: p.append(f"-{abs(c)}")
    return "".join(p) + " = 0"

# =====================================================================
# PART 1: NUMBER AND ALGEBRA (~3500 questions)
# =====================================================================

# --- 1. QUADRATIC EQUATIONS (500) ---
print("Generating quadratic equations...")
T1,T1Z,T1E = "quadratic_equations","二次方程","Quadratic Equations"

# 1a. Solving by factorization (100)
for _ in range(100):
    a = random.choice([1,1,1,2])
    r1,r2 = random.randint(-6,6), random.randint(-6,6)
    while r1==r2: r2 = random.randint(-6,6)
    ba,ca = -a*(r1+r2), a*r1*r2
    if a>1:
        d = ba*ba-4*a*ca
        if d<0: continue
        sd = int(math.isqrt(d))
        if sd*sd!=d: continue
        x1,x2 = (-ba+sd)/(2*a),(-ba-sd)/(2*a)
        if x1!=int(x1) or x2!=int(x2): continue
        r1,r2 = int(x1),int(x2)
    roots = sorted([r1,r2])
    eq = fe(a,ba,ca)
    rs = f"x = {roots[0]} 或 x = {roots[1]}" if roots[0]!=roots[1] else f"x = {roots[0]}（重根）"
    re = f"x = {roots[0]} or x = {roots[1]}" if roots[0]!=roots[1] else f"x = {roots[0]} (repeated root)"
    w1 = f"x = {-roots[0]} 或 x = {-roots[1]}" if roots[0]!=roots[1] else f"x = {-roots[0]}"
    w1e = f"x = {-roots[0]} or x = {-roots[1]}" if roots[0]!=roots[1] else f"x = {-roots[0]}"
    add(T1,T1Z,T1E,"solving_by_factorization","因式分解法","Solving by Factorization",
        f"解方程 {eq}",f"Solve {eq}",
        [f"A. {rs}",f"B. {w1}",f"C. 無實數解",f"D. x = 0"],
        [f"A. {re}",f"B. {w1e}",f"C. No real roots",f"D. x = 0"],
        0, f"因式分解 {eq}，得 {rs}。", f"Factorizing {eq}, we get {re}.",
        random.choice([1,1,2]))

# 1b. Discriminant (100)
for _ in range(100):
    a = random.choice([1,2,3]); b = random.randint(-10,10); c = random.randint(-10,10)
    d = b*b - 4*a*c
    eq = fe(a,b,c)
    if d>0:
        sq = int(math.isqrt(d))
        if sq*sq==d: nz,ne = "有兩個相異有理實數根","two distinct rational real roots"
        else: nz,ne = "有兩個相異無理實數根","two distinct irrational real roots"
        dt = "\u0394 > 0"
    elif d==0: nz,ne,dt = "有重根","two equal real roots","\u0394 = 0"
    else: nz,ne,dt = "沒有實數根","no real roots","\u0394 < 0"
    add(T1,T1Z,T1E,"discriminant","判別式","Discriminant",
        f"方程 {eq} 的判別式值及根的性質為何？",
        f"Find the discriminant and nature of roots of {eq}.",
        [f"A. \u0394 = {d}，{nz}",f"B. \u0394 = {d+2}，有兩個相異實數根",
         f"C. \u0394 = {-abs(d)}，沒有實數根",f"D. \u0394 = {d-1}，有重根"],
        [f"A. \u0394 = {d}, {ne}",f"B. \u0394 = {d+2}, two distinct real roots",
         f"C. \u0394 = {-abs(d)}, no real roots",f"D. \u0394 = {d-1}, repeated root"],
        0, f"\u0394 = {b}\u00b2 - 4({a})({c}) = {d}。{dt}，故{nz}。",
        f"\u0394 = {b}\u00b2 - 4({a})({c}) = {d}. {dt}, so {ne}.",
        random.choice([1,1,2]))

# 1c. Nature of roots conditions (60)
nrv = [
    ("x\u00b2 + kx + 4 = 0","k\u00b2 - 16 = 0","k = 4 或 k = -4","k = 4 or k = -4",1),
    ("2x\u00b2 + kx + 8 = 0","k\u00b2 - 64 = 0","k = 8 或 k = -8","k = 8 or k = -8",1),
    ("x\u00b2 + 6x + k = 0","36 - 4k = 0","k = 9","k = 9",1),
    ("kx\u00b2 + 12x + 9 = 0","144 - 36k = 0","k = 4","k = 4",2),
    ("3x\u00b2 + kx + 12 = 0","k\u00b2 - 144 = 0","k = 12 或 k = -12","k = 12 or k = -12",2),
    ("x\u00b2 - 2kx + (k+6) = 0","4k\u00b2 - 4k - 24 = 0","k = 3 或 k = -2","k = 3 or k = -2",2),
]
for _ in range(60):
    v = random.choice(nrv)
    w = [f"k = {random.randint(1,10)}", f"k = {random.randint(-10,-1)}", "k = 0"]
    random.shuffle(w)
    add(T1,T1Z,T1E,"nature_of_roots","根的性質","Nature of Roots",
        f"若 {v[0]} 有重根，求 k。", f"If {v[0]} has equal roots, find k.",
        [f"A. {v[2]}",f"B. {w[0]}",f"C. {w[1]}",f"D. {w[2]}"],
        [f"A. {v[3]}",f"B. {w[0]}",f"C. {w[1]}",f"D. {w[2]}"],
        0, f"\u0394 = 0 \u2192 {v[1]} \u2192 {v[2]}。", f"\u0394 = 0 \u2192 {v[1]} \u2192 {v[3]}.", v[4])

# 1d. Sum and product of roots (80)
for _ in range(80):
    a = random.choice([1,1,2])
    r1,r2 = random.randint(-5,5), random.randint(-5,5)
    while r1==r2: r2 = random.randint(-5,5)
    s,p = r1+r2, r1*r2
    ba,ca = -a*s, a*p
    eq = fe(a,ba,ca)
    add(T1,T1Z,T1E,"sum_product_roots","根的和與積","Sum and Product of Roots",
        f"設 \u03b1,\u03b2 為 {eq} 的兩根，求 \u03b1+\u03b2 及 \u03b1\u03b2。",
        f"Let \u03b1,\u03b2 be roots of {eq}. Find \u03b1+\u03b2 and \u03b1\u03b2.",
        [f"A. \u03b1+\u03b2={s}，\u03b1\u03b2={p}",f"B. \u03b1+\u03b2={-s}，\u03b1\u03b2={p}",
         f"C. \u03b1+\u03b2={s}，\u03b1\u03b2={-p}",f"D. \u03b1+\u03b2={ba}，\u03b1\u03b2={ca}"],
        [f"A. \u03b1+\u03b2={s}, \u03b1\u03b2={p}",f"B. \u03b1+\u03b2={-s}, \u03b1\u03b2={p}",
         f"C. \u03b1+\u03b2={s}, \u03b1\u03b2={-p}",f"D. \u03b1+\u03b2={ba}, \u03b1\u03b2={ca}"],
        0, f"\u97cb\u9054\u5b9a\u7406\uff1a\u03b1+\u03b2 = {s}\uff0c\u03b1\u03b2 = {p}\u3002",
        f"Vieta's: \u03b1+\u03b2 = {s}, \u03b1\u03b2 = {p}.", random.choice([1,2,2]))

# 1e. Quadratic graphs / vertex / turning value (80)
for _ in range(80):
    a = random.choice([1,1,2,-1,-2])
    h,k = random.randint(-4,4), random.randint(-5,5)
    if a==1: es="(x"
    elif a==-1: es="-(x"
    else: es=f"{a}(x"
    es += f"-{h})\u00b2" if h>0 else f"+{abs(h)})\u00b2" if h<0 else ")\u00b2"
    if k>0: es += f"+{k}"
    elif k<0: es += f"-{abs(k)}"
    mv = "\u6700\u5c0f\u503c" if a>0 else "\u6700\u5927\u503c"
    mv_en = "minimum" if a>0 else "maximum"
    add(T1,T1Z,T1E,"quadratic_graphs","二次函數圖像","Graphs of Quadratic Functions",
        f"已知 y = {es}，求頂點及最值。", f"Given y = {es}, find vertex and turning value.",
        [f"A. ({h},{k}), {mv}={k}",f"B. ({-h},{k}), {mv}={k}",
         f"C. ({h},{-k}), {mv}={-k}",f"D. (0,{k}), {mv}={k}"],
        [f"A. ({h},{k}), {mv_en}={k}",f"B. ({-h},{k}), {mv_en}={k}",
         f"C. ({h},{-k}), {mv_en}={-k}",f"D. (0,{k}), {mv_en}={k}"],
        0, f"頂點 ({h},{k})，{mv}={k}。", f"Vertex ({h},{k}), {mv_en}={k}.", random.choice([1,2]))

# 1f. Completing the square (80)
for _ in range(80):
    a = random.choice([1,1,2])
    p,q = random.randint(1,6), random.randint(-5,5)
    ba,ca = 2*a*p, a*p*p+q
    orig = fe(a,ba,ca).replace(" = 0","")
    comp = f"{a}(x+{p})\u00b2" if a>1 else f"(x+{p})\u00b2"
    if q>0: comp += f"+{q}"
    elif q<0: comp += f"-{abs(q)}"
    add(T1,T1Z,T1E,"completing_square","配方法","Completing the Square",
        f"將 y = {orig} 配方。", f"Complete the square: y = {orig}.",
        [f"A. y = {comp}",f"B. y = (x+{p+1})\u00b2+{q}",
         f"C. y = (x-{p})\u00b2+{q+1}",f"D. y = {a}(x+{p})\u00b2+{q+2}"],
        [f"A. y = {comp}",f"B. y = (x+{p+1})\u00b2+{q}",
         f"C. y = (x-{p})\u00b2+{q+1}",f"D. y = {a}(x+{p})\u00b2+{q+2}"],
        0, f"y = {orig} = {comp}。", f"y = {orig} = {comp}.", random.choice([1,2]))

print(f"  Quadratic: {qid} questions so far")

# --- 2. FUNCTIONS AND GRAPHS (500) ---
print("Generating functions and graphs...")
T2,T2Z,T2E = "functions_and_graphs","函數與圖像","Functions and Graphs"

# 2a. Domain and range (100)
drv = [
    ("f(x) = \u221a(x-3)","x \u2265 3, f(x) \u2265 0","x \u2265 3, f(x) \u2265 0","x-3\u22650\u21d2x\u22653","x-3\u22650\u21d2x\u22653",1),
    ("f(x) = \u221a(2x+6)","x \u2265 -3, f(x) \u2265 0","x \u2265 -3, f(x) \u2265 0","2x+6\u22650\u21d2x\u2265-3","2x+6\u22650\u21d2x\u2265-3",1),
    ("f(x) = 1/(x-2)","x \u2260 2, f(x) \u2260 0","x \u2260 2, f(x) \u2260 0","x-2\u22600\u21d2x\u22602","x-2\u22600\u21d2x\u22602",2),
    ("f(x) = \u221a(4-x\u00b2)","\u22122 \u2264 x \u2264 2, 0 \u2264 f(x) \u2264 2","-2 \u2264 x \u2264 2, 0 \u2264 f(x) \u2264 2","4-x\u00b2\u22650\u21d2-2\u2264x\u22642","4-x\u00b2\u22650\u21d2-2\u2264x\u22642",2),
    ("f(x) = |x-5|","所有實數, f(x) \u2265 0","All real numbers, f(x) \u2265 0","絕對值函數定義域為所有實數","Absolute value defined for all reals",1),
    ("f(x) = 1/(x\u00b2-4)","x \u2260 \u00b12","x \u2260 \u00b12","x\u00b2-4\u22600\u21d2x\u2260\u00b12","x\u00b2-4\u22600\u21d2x\u2260\u00b12",2),
    ("f(x) = \u221a(x\u00b2-9)","x \u2264 -3 或 x \u2265 3","x \u2264 -3 or x \u2265 3","x\u00b2-9\u22650\u21d2x\u2264-3或x\u22653","x\u00b2-9\u22650\u21d2x\u2264-3 or x\u22653",2),
]
for _ in range(100):
    v = random.choice(drv)
    add(T2,T2Z,T2E,"domain_range","定義域與值域","Domain and Range",
        f"求 {v[0]} 的定義域和值域。", f"Find the domain and range of {v[0]}.",
        [f"A. {v[1]}",f"B. x>0, f(x)>0",f"C. 所有實數",f"D. x\u22600"],
        [f"A. {v[2]}",f"B. x>0, f(x)>0",f"C. All real numbers",f"D. x\u22600"],
        0, v[3]+".", v[4]+".", v[5])

# 2b. Composite functions (100)
for _ in range(100):
    a1,b1 = random.randint(1,5), random.randint(-5,5)
    a2,b2 = random.randint(1,3), random.randint(-5,5)
    ca,cb = a1*a2, a1*b2+b1
    qtype = random.choice(["fg","gf","f2","g2"])
    if qtype=="fg":
        qz = f"若 f(x) = {a1}x+{b1}, g(x) = {a2}x+{b2}，求 f(g(x))。"
        qe = f"If f(x) = {a1}x+{b1}, g(x) = {a2}x+{b2}, find f(g(x))."
        ans_z = f"{ca}x+{cb}"; ans_e = ans_z
        expl_z = f"f(g(x)) = {a1}({a2}x+{b2})+{b1} = {ca}x+{cb}。"
        expl_e = f"f(g(x)) = {a1}({a2}x+{b2})+{b1} = {ca}x+{cb}."
    elif qtype=="gf":
        ca2,cb2 = a2*a1, a2*b1+b2
        qz = f"若 f(x) = {a1}x+{b1}, g(x) = {a2}x+{b2}，求 g(f(x))。"
        qe = f"If f(x) = {a1}x+{b1}, g(x) = {a2}x+{b2}, find g(f(x))."
        ans_z = f"{ca2}x+{cb2}"; ans_e = ans_z
        expl_z = f"g(f(x)) = {a2}({a1}x+{b1})+{b2} = {ca2}x+{cb2}。"
        expl_e = f"g(f(x)) = {a2}({a1}x+{b1})+{b2} = {ca2}x+{cb2}."
    elif qtype=="f2":
        a1f2 = a1*a1; b1f2 = a1*b1+b1
        qz = f"若 f(x) = {a1}x+{b1}，求 f(f(x))。"
        qe = f"If f(x) = {a1}x+{b1}, find f(f(x))."
        ans_z = f"{a1f2}x+{b1f2}"; ans_e = ans_z
        expl_z = f"f(f(x)) = {a1}({a1}x+{b1})+{b1} = {a1f2}x+{b1f2}。"
        expl_e = f"f(f(x)) = {a1}({a1}x+{b1})+{b1} = {a1f2}x+{b1f2}."
    else:
        a2g2 = a2*a2; b2g2 = a2*b2+b2
        qz = f"若 g(x) = {a2}x+{b2}，求 g(g(x))。"
        qe = f"If g(x) = {a2}x+{b2}, find g(g(x))."
        ans_z = f"{a2g2}x+{b2g2}"; ans_e = ans_z
        expl_z = f"g(g(x)) = {a2}({a2}x+{b2})+{b2} = {a2g2}x+{b2g2}。"
        expl_e = f"g(g(x)) = {a2}({a2}x+{b2})+{b2} = {a2g2}x+{b2g2}."
    w1 = f"{ca+1}x+{cb}"; w2 = f"{ca}x+{cb+1}"; w3 = f"{ca-1}x+{cb+2}"
    add(T2,T2Z,T2E,"composite_functions","複合函數","Composite Functions",qz,qe,
        [f"A. {ans_z}",f"B. {w1}",f"C. {w2}",f"D. {w3}"],
        [f"A. {ans_e}",f"B. {w1}",f"C. {w2}",f"D. {w3}"],
        0, expl_z, expl_e, random.choice([1,2]))

# 2c. Inverse functions (80)
for _ in range(80):
    a = random.choice([2,3,4,5,-2,-3])
    b = random.randint(-8,8)
    inv = f"(x-{b})/{a}" if a>0 else f"(x-{b})/({a})"
    inv_simplified = f"(x-{b})/{a}"
    add(T2,T2Z,T2E,"inverse_functions","反函數","Inverse Functions",
        f"若 f(x) = {a}x+{b}，求 f\u207b\u00b9(x)。", f"If f(x) = {a}x+{b}, find f\u207b\u00b9(x).",
        [f"A. {inv_simplified}",f"B. (x+{b})/{a}",f"C. {a}x-{b}",f"D. x/{a}+{b}"],
        [f"A. {inv_simplified}",f"B. (x+{b})/{a}",f"C. {a}x-{b}",f"D. x/{a}+{b}"],
        0, f"令 y={a}x+{b}, x=(y-{b})/{a}, f\u207b\u00b9(x)={inv_simplified}。",
        f"Let y={a}x+{b}, x=(y-{b})/{a}, f\u207b\u00b9(x)={inv_simplified}.", random.choice([1,2]))

# 2d. Even/odd functions (60)
eov = [
    ("f(x) = x\u00b2","偶函數","Even function","f(-x) = x\u00b2 = f(x)","f(-x) = x\u00b2 = f(x)",1),
    ("f(x) = x\u2074 + 1","偶函數","Even function","f(-x) = x\u2074+1 = f(x)","f(-x) = x\u2074+1 = f(x)",1),
    ("f(x) = x\u00b3","奇函數","Odd function","f(-x) = -x\u00b3 = -f(x)","f(-x) = -x\u00b3 = -f(x)",1),
    ("f(x) = x\u00b3 - x","奇函數","Odd function","f(-x) = -x\u00b3+x = -f(x)","f(-x) = -x\u00b3+x = -f(x)",2),
    ("f(x) = |x|","偶函數","Even function","f(-x) = |-x| = |x| = f(x)","f(-x) = |-x| = |x| = f(x)",1),
    ("f(x) = x\u00b2 + x","非奇非偶","Neither","f(-x) = x\u00b2-x \u2260 f(x), \u2260 -f(x)","f(-x)=x\u00b2-x\u2260f(x),\u2260-f(x)",2),
    ("f(x) = \u221ax\u00b2","偶函數","Even function","f(-x)=|x|=f(x)","f(-x)=|x|=f(x)",1),
    ("f(x) = 1/x","奇函數","Odd function","f(-x)=-1/x=-f(x)","f(-x)=-1/x=-f(x)",2),
]
for _ in range(60):
    v = random.choice(eov)
    opts_z = [f"A. {v[1]}", f"B. {'偶函數' if v[1]!='偶函數' else '奇函數'}",
              f"C. {'兩者皆是' if v[1]=='非奇非偶' else '非奇非偶'}", f"D. 無法判斷"]
    opts_e = [f"A. {v[2]}", f"B. {'Even' if v[2]!='Even function' else 'Odd function'}",
              f"C. {'Both' if v[2]=='Neither' else 'Neither'}", f"D. Cannot determine"]
    add(T2,T2Z,T2E,"even_odd","奇偶函數","Even/Odd Functions",
        f"判斷 {v[0]} 的奇偶性。", f"Determine if {v[0]} is even, odd, or neither.",
        opts_z, opts_e, 0, f"{v[3]}，故為{v[1]}。", f"{v[4]}, so {v[2]}.", v[5])

# 2e. Graph transformations (80)
gtv = [
    ("y = f(x) + 3","向上平移3個單位","Shift up by 3",1),
    ("y = f(x) - 2","向下平移2個單位","Shift down by 2",1),
    ("y = f(x - 4)","向右平移4個單位","Shift right by 4",1),
    ("y = f(x + 1)","向左平移1個單位","Shift left by 1",1),
    ("y = -f(x)","關於x軸翻轉","Reflection about x-axis",2),
    ("y = f(-x)","關於y軸翻轉","Reflection about y-axis",2),
    ("y = 2f(x)","垂直拉伸2倍","Vertical stretch by 2",2),
    ("y = f(2x)","水平壓縮為1/2","Horizontal compression by 1/2",2),
    ("y = f(x)+k, k>0","向上平移k個單位","Shift up by k units",1),
    ("y = f(x-h), h>0","向右平移h個單位","Shift right by h units",2),
]
for _ in range(80):
    v = random.choice(gtv)
    add(T2,T2Z,T2E,"graph_transformations","圖像變換","Graph Transformations",
        f"由 y = f(x) 變換到 {v[0]}，圖像有何改變？", f"How does y=f(x) change to {v[0]}?",
        [f"A. {v[1]}",f"B. 向下平移",f"C. 旋轉90\u00b0",f"D. 沒有改變"],
        [f"A. {v[2]}",f"B. Shift down",f"C. Rotate 90\u00b0",f"D. No change"],
        0, f"{v[0]} \u21d2 {v[1]}。", f"{v[0]} \u21d2 {v[2]}.", v[3])

# 2f. Polynomial functions (80)
for _ in range(80):
    deg = random.choice([2,3])
    if deg == 2:
        r1,r2 = random.randint(-4,4), random.randint(-4,4)
        while r1==r2: r2=random.randint(-4,4)
        roots = sorted([r1,r2])
        add(T2,T2Z,T2E,"polynomial_functions","多項式函數","Polynomial Functions",
            f"函數 y = (x-{r1})(x-{r2}) 的x軸截距為何？",
            f"Find x-intercepts of y = (x-{r1})(x-{r2}).",
            [f"A. x={roots[0]} 和 x={roots[1]}",f"B. x={-roots[0]} 和 x={-roots[1]}",
             f"C. x=0",f"D. 無截距"],
            [f"A. x={roots[0]} and x={roots[1]}",f"B. x={-roots[0]} and x={-roots[1]}",
             f"C. x=0",f"D. No intercepts"],
            0, f"令y=0，得x={roots[0]}或x={roots[1]}。", f"y=0 gives x={roots[0]} or x={roots[1]}.", 1)
    else:
        r1,r2,r3 = random.randint(-3,3),random.randint(-3,3),random.randint(-3,3)
        s1 = r1+r2+r3; s2 = r1*r2+r1*r3+r2*r3; s3 = r1*r2*r3
        c0 = -s3; c1 = s2; c2 = -s1
        eq = f"x\u00b3"
        if c2!=0: eq += f"{'+' if c2>0 else ''}{c2}x\u00b2"
        if c1!=0: eq += f"{'+' if c1>0 else ''}{c1}x"
        if c0!=0: eq += f"{'+' if c0>0 else ''}{c0}"
        add(T2,T2Z,T2E,"polynomial_functions","多項式函數","Polynomial Functions",
            f"已知 {eq} = 0 有根 x={r1}，求其餘兩根。",
            f"Given {eq} = 0 has root x={r1}, find the other roots.",
            [f"A. x={r2}, x={r3}",f"B. x={-r2}, x={-r3}",
             f"C. x={r1+1}, x={r2+1}",f"D. 無實數根"],
            [f"A. x={r2}, x={r3}",f"B. x={-r2}, x={-r3}",
             f"C. x={r1+1}, x={r2+1}",f"D. No real roots"],
            0, f"因式分解得(x-{r1})(x-{r2})(x-{r3})=0，其餘根為x={r2}, x={r3}。",
            f"Factorizing: (x-{r1})(x-{r2})(x-{r3})=0, other roots x={r2}, x={r3}.", 3)

print(f"  Functions & graphs: {qid} questions so far")

# --- 3. EXPONENTIAL AND LOGARITHMIC FUNCTIONS (400) ---
print("Generating exponential & log...")
T3,T3Z,T3E = "exponential_log","指數與對數函數","Exponential and Logarithmic Functions"

# 3a. Laws of indices (60)
for _ in range(60):
    a = random.randint(2,5)
    m = random.randint(2,4); n = random.randint(2,4)
    problems = [
        (f"{a}\u1d50 \u00d7 {a}\u207f", f"{a}\u02e3\u02e0\u207a\u02e1\u1d58", f"{a}^({m}+{n}) = {a}^{m+n}", f"{a}^{m+n}", m+n,
         f"{a}\u1d50 \u00d7 {a}\u207f = {a}\u02e3\u02e0\u207a\u02e1\u1d58 = {a}^{m+n}", f"{a}\u1d50\u00d7{a}\u207f = {a}^{m+n}", 1),
        (f"{a}\u1d50 \u00f7 {a}\u207f", f"{a}\u02e3\u02e0\u207b\u02e1\u1d58", f"{a}^({m}-{n}) = {a}^{m-n}", f"{a}^{m-n}", m-n,
         f"{a}\u1d50 \u00f7 {a}\u207f = {a}^{m-n}", f"{a}\u1d50\u00f7{a}\u207f = {a}^{m-n}", 1),
        (f"({a}\u1d50)\u207f", f"{a}\u1d50\u1d58", f"{a}^({m}\u00d7{n}) = {a}^{m*n}", f"{a}^{m*n}", m*n,
         f"({a}\u1d50)\u207f = {a}^{m*n}", f"({a}\u1d50)\u207f = {a}^{m*n}", 2),
    ]
    p = random.choice(problems)
    # Replace unicode superscripts with actual values for display
    qz = p[0].replace("\u1d50", f"^{{{m}}}").replace("\u207f", f"^{{{n}}}")
    qe = qz
    ans_val = p[4]
    opt_a = f"{a}^{ans_val} = {a**ans_val}" if ans_val>=0 else f"{a}^({ans_val}) = {1/a**abs(ans_val):.4g}"
    add(T3,T3Z,T3E,"laws_of_indices","指數定律","Laws of Indices",
        f"化簡 {qz}。", f"Simplify {qz}.",
        [f"A. {opt_a}",f"B. {a}^{ans_val+1}",f"C. {a}^{ans_val-1}",f"D. {a*2}^{ans_val}"],
        [f"A. {opt_a}",f"B. {a}^{ans_val+1}",f"C. {a}^{ans_val-1}",f"D. {a*2}^{ans_val}"],
        0, f"指數定律：{qz} = {opt_a}。", f"Law of indices: {qz} = {opt_a}.", p[7])

# 3b. Laws of logarithms (80)
for _ in range(80):
    base = random.choice([2,3,5,10])
    a = random.randint(1,4); b = random.randint(1,4)
    prob_type = random.choice(["product","quotient","power","change_base"])
    if prob_type == "product":
        qz = f"log\u208{str(base)[-1]}({base**a} \u00d7 {base**b})"
        qe = f"log_{base}({base**a} \u00d7 {base**b})"
        ans = a + b
        ez = f"log({base**a}\u00d7{base**b}) = log{base**a} + log{base**b} = {a} + {b} = {ans}"
        ee = ez
    elif prob_type == "quotient":
        qz = f"log\u208{str(base)[-1]}({base**a} \u00f7 {base**b})"
        qe = f"log_{base}({base**a} / {base**b})"
        ans = a - b
        ez = f"log({base**a}/{base**b}) = log{base**a} - log{base**b} = {a} - {b} = {ans}"
        ee = ez
    elif prob_type == "power":
        qz = f"log\u208{str(base)[-1]}({base}^{a})"
        qe = f"log_{base}({base}^{a})"
        ans = a
        ez = f"log({base}^{a}) = {a}\u00d7log{base} = {a}\u00d71 = {a}"
        ee = ez
    else:
        qz = f"log\u2082{base**a}"
        qe = f"log_2({base**a})"
        ans = round(a * math.log(base)/math.log(2), 4)
        if ans == int(ans): ans = int(ans)
        ez = f"log\u2082({base**a}) = {a}\u00d7log\u2082{base} = {ans}"
        ee = ez
    add(T3,T3Z,T3E,"laws_of_logarithms","對數定律","Laws of Logarithms",
        f"計算 {qz}。", f"Evaluate {qe}.",
        [f"A. {ans}",f"B. {ans+1}",f"C. {ans-1}",f"D. {ans*2}"],
        [f"A. {ans}",f"B. {ans+1}",f"C. {ans-1}",f"D. {ans*2}"],
        0, ez, ee, random.choice([1,2]))

# 3c. Solving exponential equations (80)
for _ in range(80):
    base = random.choice([2,3,5])
    x_val = random.randint(-3,5)
    rhs = base**x_val
    add(T3,T3Z,T3E,"exponential_equations","指數方程","Exponential Equations",
        f"解方程 {base}\u02e3 = {rhs}。", f"Solve {base}^x = {rhs}.",
        [f"A. x = {x_val}",f"B. x = {x_val+1}",f"C. x = {-x_val}",f"D. x = {x_val*2}"],
        [f"A. x = {x_val}",f"B. x = {x_val+1}",f"C. x = {-x_val}",f"D. x = {x_val*2}"],
        0, f"{base}^x = {base}^{x_val}，故 x = {x_val}。", f"{base}^x = {base}^{x_val}, so x = {x_val}.", 1)

# 3d. Solving log equations (80)
for _ in range(80):
    base = random.choice([2,3,10])
    x_val = random.randint(1,5)
    rhs = base**x_val
    add(T3,T3Z,T3E,"log_equations","對數方程","Logarithmic Equations",
        f"解方程 log\u208{str(base)[-1]}(x) = {x_val}。" if base<10 else f"解方程 log\u2081\u2080(x) = {x_val}。",
        f"Solve log_{base}(x) = {x_val}.",
        [f"A. x = {rhs}",f"B. x = {base}",f"C. x = {x_val}",f.D. x = {rhs+1}"],
        [f"A. x = {rhs}",f"B. x = {base}",f"C. x = {x_val}",f"D. x = {rhs+1}"],
        0, f"log_{base}(x) = {x_val} \u21d2 x = {base}^{x_val} = {rhs}。",
        f"log_{base}(x) = {x_val} \u21d2 x = {base}^{x_val} = {rhs}.", 1)

# 3e. Exponential growth/decay (100)
for _ in range(100):
    P0 = random.choice([100,200,500,1000])
    r = random.choice([0.05,0.1,0.15,0.2,0.02])
    t = random.randint(1,10)
    P = round(P0 * (1+r)**t, 2)
    P_dec = round(P0 * (1-r)**t, 2)
    if random.random() < 0.5:
        # Growth
        add(T3,T3Z,T3E,"exponential_growth","指數增長","Exponential Growth",
            f"某投資初值 ${P0}，年增率 {r*100}%。{t}年後價值為何？（四捨五入至小數點後兩位）",
            f"An investment starts at ${P0}, annual growth rate {r*100}%. Value after {t} years? (2 d.p.)",
            [f"A. ${P}",f"B. ${round(P*1.1,2)}",f"C. ${round(P*0.9,2)}",f"D. ${P0+t*int(P0*r)}"],
            [f"A. ${P}",f"B. ${round(P*1.1,2)}",f"C. ${round(P*0.9,2)}",f"D. ${P0+t*int(P0*r)}"],
            0, f"P = {P0}(1+{r})^{t} = {P}。", f"P = {P0}(1+{r})^{t} = {P}.", 2)
    else:
        # Decay
        add(T3,T3Z,T3E,"exponential_decay","指數衰減","Exponential Decay",
            f"某物質初量 {P0}g，年衰減率 {r*100}%。{t}年後剩餘多少？",
            f"Substance initial {P0}g, annual decay rate {r*100}%. Amount after {t} years?",
            [f"A. {P_dec}g",f"B. {round(P_dec*1.1,2)}g",f"C. {round(P_dec*0.9,2)}g",f"D. {P0-t*int(P0*r)}g"],
            [f"A. {P_dec}g",f"B. {round(P_dec*1.1,2)}g",f"C. {round(P_dec*0.9,2)}g",f"D. {P0-t*int(P0*r)}g"],
            0, f"P = {P0}(1-{r})^{t} = {P_dec}g。", f"P = {P0}(1-{r})^{t} = {P_dec}g.", 2)

print(f"  Exponential & log: {qid} questions so far")

# --- 4. MORE ABOUT POLYNOMIALS (300) ---
print("Generating polynomials...")
T4,T4Z,T4E = "more_polynomials","多項式進階","More About Polynomials"

# 4a. Remainder theorem (80)
for _ in range(80):
    a3 = random.choice([1,2]); a2 = random.randint(-5,5); a1 = random.randint(-5,5); a0 = random.randint(-5,5)
    c = random.randint(-3,3)
    rem = a3*c**3 + a2*c**2 + a1*c + a0
    px = f"{a3}x\u00b3" if a3!=1 else "x\u00b3"
    if a2>0: px += f"+{a2}x\u00b2" if a2!=1 else "+x\u00b2"
    elif a2<0: px += f"{a2}x\u00b2" if a2!=-1 else "-x\u00b2"
    if a1>0: px += f"+{a1}x" if a1!=1 else "+x"
    elif a1<0: px += f"{a1}x" if a1!=-1 else "-x"
    if a0>0: px += f"+{a0}"
    elif a0<0: px += f"{a0}"
    add(T4,T4Z,T4E,"remainder_theorem","餘式定理","Remainder Theorem",
        f"求 {px} 除以 (x-({c})) 的餘數。",
        f"Find the remainder when {px} is divided by (x-({c})).",
        [f"A. {rem}",f"B. {rem+1}",f"C. {rem-1}",f"D. {c}"],
        [f"A. {rem}",f"B. {rem+1}",f"C. {rem-1}",f"D. {c}"],
        0, f"餘式定理：f({c}) = {rem}。", f"Remainder theorem: f({c}) = {rem}.", 1)

# 4b. Factor theorem (80)
for _ in range(80):
    r = random.randint(-4,4)
    a2 = random.choice([1,2]); a1 = random.randint(-5,5); a0 = random.randint(-10,10)
    val = a2*r*r + a1*r + a0
    is_factor = (val == 0)
    px = f"{a2}x\u00b2" if a2!=1 else "x\u00b2"
    if a1>0: px += f"+{a1}x" if a1!=1 else "+x"
    elif a1<0: px += f"{a1}x" if a1!=-1 else "-x"
    if a0>0: px += f"+{a0}"
    elif a0<0: px += f"{a0}"
    ans_str = "是" if is_factor else "不是"
    ans_en = "Yes" if is_factor else "No"
    add(T4,T4Z,T4E,"factor_theorem","因式定理","Factor Theorem",
        f"(x-{r}) 是否為 {px} 的因式？", f"Is (x-{r}) a factor of {px}?",
        [f"A. {ans_str}，f({r})={val}",f"B. {'不是' if is_factor else '是'}",
         f"C. 無法判斷",f"D. 部分是"],
        [f"A. {ans_en}, f({r})={val}",f"B. {'No' if is_factor else 'Yes'}",
         f"C. Cannot determine",f"D. Partially"],
        0, f"f({r}) = {val}，故(x-{r}){'是' if is_factor else '不是'}因式。" ,
        f"f({r}) = {val}, so (x-{r}) is {'a' if is_factor else 'not a'} factor.", 2)

# 4c. Polynomial division (80)
for _ in range(80):
    r1 = random.randint(-4,4); r2 = random.randint(-4,4)
    while r1==r2: r2=random.randint(-4,4)
    # (x-r1)(x-r2)(x+a) divided by (x-r1)
    a = random.randint(-3,3)
    # quotient: (x-r2)(x+a) = x² + (a-r2)x - a*r2
    q_a = 1; q_b = a-r2; q_c = -a*r2
    # dividend: (x-r1)(x² + q_b*x + q_c) = x³ + (q_b-r1)x² + (q_c-r1*q_b)x - r1*q_c
    d_c = -r1*q_c; d_b = q_c - r1*q_b; d_a_coeff = q_b - r1
    def fmt_poly3(a3,a2,a1,a0):
        s = f"x\u00b3"
        if a2>0: s += f"+{a2}x\u00b2" if a2!=1 else "+x\u00b2"
        elif a2<0: s += f"{a2}x\u00b2" if a2!=-1 else "-x\u00b2"
        if a1>0: s += f"+{a1}x" if a1!=1 else "+x"
        elif a1<0: s += f"{a1}x" if a1!=-1 else "-x"
        if a0>0: s += f"+{a0}"
        elif a0<0: s += f"{a0}"
        return s
    def fmt_poly2(a2,a1,a0):
        s = f"x\u00b2" if a2==1 else f"{a2}x\u00b2"
        if a1>0: s += f"+{a1}x" if a1!=1 else "+x"
        elif a1<0: s += f"{a1}x" if a1!=-1 else "-x"
        if a0>0: s += f"+{a0}"
        elif a0<0: s += f"{a0}"
        return s
    dvd = fmt_poly3(1, d_a_coeff, d_b, d_c)
    qot = fmt_poly2(q_a, q_b, q_c)
    add(T4,T4Z,T4E,"polynomial_division","多項式除法","Polynomial Division",
        f"以 (x-({r1})) 除 {dvd}，求商式。",
        f"Divide {dvd} by (x-({r1})), find quotient.",
        [f"A. {qot}",f"B. {fmt_poly2(1,q_b+1,q_c)}",f"C. {fmt_poly2(1,q_b,q_c+1)}",f"D. {fmt_poly2(2,q_b,q_c)}"],
        [f"A. {qot}",f"B. {fmt_poly2(1,q_b+1,q_c)}",f"C. {fmt_poly2(1,q_b,q_c+1)}",f"D. {fmt_poly2(2,q_b,q_c)}"],
        0, f"多項式除法：{dvd} \u00f7 (x-{r1}) = {qot}。",
        f"Polynomial division: {dvd} / (x-{r1}) = {qot}.", 2)

# 4d. Solving higher-degree equations (60)
for _ in range(60):
    r1,r2,r3 = random.randint(-3,3),random.randint(-3,3),random.randint(-3,3)
    s1=r1+r2+r3; s2=r1*r2+r1*r3+r2*r3; s3=r1*r2*r3
    c2=-s1; c1=s2; c0=-s3
    eq = "x\u00b3"
    if c2>0: eq += f"+{c2}x\u00b2" if c2!=1 else "+x\u00b2"
    elif c2<0: eq += f"{c2}x\u00b2" if c2!=-1 else "-x\u00b2"
    if c1>0: eq += f"+{c1}x" if c1!=1 else "+x"
    elif c1<0: eq += f"{c1}x" if c1!=-1 else "-x"
    if c0>0: eq += f"+{c0}"
    elif c0<0: eq += f"{c0}"
    eq += " = 0"
    add(T4,T4Z,T4E,"higher_degree_equations","高次方程","Higher-Degree Equations",
        f"解方程 {eq}。", f"Solve {eq}.",
        [f"A. x={r1}, x={r2}, x={r3}",f"B. x={-r1}, x={-r2}, x={-r3}",
         f"C. x=0, x={r1}, x={r2}",f.D. 無實數根"],
        [f"A. x={r1}, x={r2}, x={r3}",f"B. x={-r1}, x={-r2}, x={-r3}",
         f"C. x=0, x={r1}, x={r2}",f"D. No real roots"],
        0, f"因式分解得 (x-{r1})(x-{r2})(x-{r3})=0，x={r1},{r2},{r3}。",
        f"Factorizing: (x-{r1})(x-{r2})(x-{r3})=0, x={r1},{r2},{r3}.", 3)

print(f"  Polynomials: {qid} questions so far")

# --- 5. PARTIAL FRACTIONS (200) ---
print("Generating partial fractions...")
T5,T5Z,T5E = "partial_fractions","部分分式","Partial Fractions"

for _ in range(200):
    a = random.randint(1,5); b = random.randint(1,5)
    while a==b: b = random.randint(1,5)
    num = random.randint(1,10)
    # Decompose num/((x+a)(x+b)) = A/(x+a) + B/(x+b)
    A = num / (b - a)  # substituting x = -a
    B = -A  # since A + B = 0 for constant numerator
    # Actually: num = A(x+b) + B(x+a), at x=-a: num = A(b-a), A = num/(b-a)
    # at x=-b: num = B(a-b), B = num/(a-b) = -num/(b-a)
    A_val = round(num/(b-a), 4)
    B_val = round(num/(a-b), 4)
    if A_val == int(A_val): A_val = int(A_val)
    if B_val == int(B_val): B_val = int(B_val)
    add(T5,T5Z,T5E,"partial_fractions","部分分式","Partial Fractions",
        f"將 {num}/((x+{a})(x+{b})) 分解為部分分式。",
        f"Decompose {num}/((x+{a})(x+{b})) into partial fractions.",
        [f"A. {A_val}/(x+{a}) + {B_val}/(x+{b})",
         f"B. {A_val+1}/(x+{a}) + {B_val}/(x+{b})",
         f"C. {A_val}/(x+{a}) + {B_val+1}/(x+{b})",
         f"D. {num}/(x+{a}) - {num}/(x+{b})"],
        [f"A. {A_val}/(x+{a}) + {B_val}/(x+{b})",
         f"B. {A_val+1}/(x+{a}) + {B_val}/(x+{b})",
         f"C. {A_val}/(x+{a}) + {B_val+1}/(x+{b})",
         f"D. {num}/(x+{a}) - {num}/(x+{b})"],
        0,
        f"令 {num}/((x+{a})(x+{b})) = A/(x+{a}) + B/(x+{b})，代入 x=-{a} 得 A={A_val}，代入 x=-{{b}} 得 B={B_val}。",
        f"Let {num}/((x+{a})(x+{b})) = A/(x+{a}) + B/(x+{b}). x=-{a}: A={A_val}, x=-{b}: B={B_val}.",
        2)

print(f"  Partial fractions: {qid} questions so far")

# --- 6. INEQUALITIES AND LINEAR PROGRAMMING (300) ---
print("Generating inequalities...")
T6,T6Z,T6E = "inequalities","不等式","Inequalities"

# 6a. Linear inequalities (80)
for _ in range(80):
    a = random.choice([2,3,4,5])
    b = random.randint(-10,10)
    c = random.randint(-10,10)
    # ax + b > c or ax + b < c
    op = random.choice([">","<","\u2265","\u2264"])
    x_bound = (c - b) / a
    if op in [">", "\u2265"]:
        sol_z = f"x {'>' if op=='>' else '\u2265'} {x_bound}"
        sol_e = sol_z
    else:
        sol_z = f"x {'<' if op=='<' else '\u2264'} {x_bound}"
        sol_e = sol_z
    add(T6,T6Z,T6E,"linear_inequalities","線性不等式","Linear Inequalities",
        f"解不等式 {a}x + {b} {op} {c}。", f"Solve {a}x + {b} {op} {c}.",
        [f"A. {sol_z}",f"B. x {'<' if op in ['>','\u2265'] else '>'} {x_bound}",
         f"C. x = {x_bound}",f.D. 無解"],
        [f"A. {sol_e}",f"B. x {'<' if op in ['>','\u2265'] else '>'} {x_bound}",
         f"C. x = {x_bound}",f"D. No solution"],
        0, f"{a}x {op} {c-b}\u21d2{sol_z}。", f"{a}x {op} {c-b}\u21d2{sol_e}.", 1)

# 6b. Quadratic inequalities (100)
for _ in range(100):
    r1 = random.randint(-4,4); r2 = random.randint(-4,4)
    while r1==r2: r2=random.randint(-4,4)
    roots = sorted([r1,r2])
    op = random.choice(["< 0", "\u2264 0", "> 0", "\u2265 0"])
    if "<" in op or "\u2264" in op:
        if "\u2264" in op:
            sol_z = f"{roots[0]} \u2264 x \u2264 {roots[1]}"
            sol_e = f"{roots[0]} \u2264 x \u2264 {roots[1]}"
        else:
            sol_z = f"{roots[0]} < x < {roots[1]}"
            sol_e = f"{roots[0]} < x < {roots[1]}"
    else:
        if "\u2265" in op:
            sol_z = f"x \u2264 {roots[0]} 或 x \u2265 {roots[1]}"
            sol_e = f"x \u2264 {roots[0]} or x \u2265 {roots[1]}"
        else:
            sol_z = f"x < {roots[0]} 或 x > {roots[1]}"
            sol_e = f"x < {roots[0]} or x > {roots[1]}"
    eq = f"(x-{r1})(x-{r2})"
    add(T6,T6Z,T6E,"quadratic_inequalities","二次不等式","Quadratic Inequalities",
        f"解不等式 {eq} {op}。", f"Solve {eq} {op}.",
        [f"A. {sol_z}",f"B. x > {roots[1]}",f"C. x < {roots[0]}",f.D. 所有實數"],
        [f"A. {sol_e}",f"B. x > {roots[1]}",f"C. x < {roots[0]}",f"D. All real numbers"],
        0, f"解 {eq} {op}，得 {sol_z}。", f"Solving {eq} {op}: {sol_e}.", 2)

# 6c. Absolute value inequalities (60)
for _ in range(60):
    a = random.randint(1,5); b = random.randint(1,10)
    op = random.choice(["<", "\u2264"])
    if op == "<":
        sol_z = f"{-b} < x-{a} < {b}，即 {a-b} < x < {a+b}"
        sol_e = f"{-b} < x-{a} < {b}, i.e. {a-b} < x < {a+b}"
    else:
        sol_z = f"{-b} \u2264 x-{a} \u2264 {b}，即 {a-b} \u2264 x \u2264 {a+b}"
        sol_e = f"{-b} \u2264 x-{a} \u2264 {b}, i.e. {a-b} \u2264 x \u2264 {a+b}"
    add(T6,T6Z,T6E,"absolute_value_inequalities","絕對值不等式","Absolute Value Inequalities",
        f"解 |x - {a}| {op} {b}。", f"Solve |x - {a}| {op} {b}.",
        [f"A. {sol_z}",f"B. x > {a+b}",f"C. x < {a-b}",f.D. 無解"],
        [f"A. {sol_e}",f"B. x > {a+b}",f"C. x < {a-b}",f"D. No solution"],
        0, f"|x-{a}|{op}{b}\u21d2{sol_z}。", f"|x-{a}|{op}{b}\u21d2{sol_e}.", 2)

# 6d. Systems of inequalities / linear programming (60)
for _ in range(60):
    x_bound = random.randint(2,8); y_bound = random.randint(2,8)
    add(T6,T6Z,T6E,"linear_programming","線性規劃","Linear Programming",
        f"在約束條件 x \u2265 0, y \u2265 0, x \u2264 {x_bound}, y \u2264 {y_bound} 下，求 P = 3x + 2y 的最大值。",
        f"Under constraints x\u22650, y\u22650, x\u2264{x_bound}, y\u2264{y_bound}, find max P = 3x + 2y.",
        [f"A. {3*x_bound+2*y_bound}",f"B. {3*x_bound+2*(y_bound-1)}",
         f"C. {3*(x_bound-1)+2*y_bound}",f"D. {3*x_bound}"],
        [f"A. {3*x_bound+2*y_bound}",f"B. {3*x_bound+2*(y_bound-1)}",
         f"C. {3*(x_bound-1)+2*y_bound}",f"D. {3*x_bound}"],
        0, f"在角點 ({x_bound},{y_bound}) 處，P = 3({x_bound})+2({y_bound}) = {3*x_bound+2*y_bound}。",
        f"At corner ({x_bound},{y_bound}), P = 3({x_bound})+2({y_bound}) = {3*x_bound+2*y_bound}.", 3)

print(f"  Inequalities: {qid} questions so far")

# --- 7. SEQUENCES AND SERIES (350) ---
print("Generating sequences and series...")
T7,T7Z,T7E = "sequences_series","數列與級數","Sequences and Series"

# 7a. Arithmetic sequences (100)
for _ in range(100):
    a1 = random.randint(1,20); d = random.randint(-5,10)
    while d==0: d = random.randint(-5,10)
    n = random.randint(5,20)
    an = a1 + (n-1)*d
    sn = n*(2*a1+(n-1)*d)//2
    qtype = random.choice(["nth","sum","find_d","find_n"])
    if qtype == "nth":
        add(T7,T7Z,T7E,"arithmetic_sequences","等差數列","Arithmetic Sequences",
            f"等差數列首項 {a1}，公差 {d}，求第 {n} 項。",
            f"AP: first term {a1}, common difference {d}. Find the {n}th term.",
            [f"A. {an}",f"B. {an+d}",f"C. {an-d}",f"D. {a1+n*d}"],
            [f"A. {an}",f"B. {an+d}",f"C. {an-d}",f"D. {a1+n*d}"],
            0, f"a\u2099 = {a1} + ({n}-1)({d}) = {an}。", f"a\u2099 = {a1} + ({n}-1)({d}) = {an}.", 1)
    elif qtype == "sum":
        add(T7,T7Z,T7E,"arithmetic_series","等差級數","Arithmetic Series",
            f"等差數列首項 {a1}，公差 {d}，求前 {n} 項和。",
            f"AP: first term {a1}, d = {d}. Find sum of first {n} terms.",
            [f"A. {sn}",f"B. {sn+10}",f"C. {sn-5}",f"D. {n*an}"],
            [f"A. {sn}",f"B. {sn+10}",f"C. {sn-5}",f"D. {n*an}"],
            0, f"S\u2099 = {n}/2 \u00d7 (2\u00d7{a1} + ({n}-1)\u00d7{d}) = {sn}。",
            f"S\u2099 = {n}/2 \u00d7 (2\u00d7{a1} + ({n}-1)\u00d7{d}) = {sn}.", 1)
    elif qtype == "find_d":
        add(T7,T7Z,T7E,"arithmetic_sequences","等差數列","Arithmetic Sequences",
            f"等差數列第3項 = {a1+2*d}，第7項 = {a1+6*d}，求公差。",
            f"AP: 3rd term = {a1+2*d}, 7th term = {a1+6*d}. Find common difference.",
            [f"A. d = {d}",f"B. d = {d+1}",f"C. d = {d-1}",f"D. d = {2*d}"],
            [f"A. d = {d}",f"B. d = {d+1}",f"C. d = {d-1}",f"D. d = {2*d}"],
            0, f"d = (a\u2087-a\u2083)/(7-3) = ({a1+6*d}-{a1+2*d})/4 = {d}。",
            f"d = (a\u2087-a\u2083)/(7-3) = ({a1+6*d}-{a1+2*d})/4 = {d}.", 2)
    else:
        target = a1 + (n-1)*d
        add(T7,T7Z,T7E,"arithmetic_sequences","等差數列","Arithmetic Sequences",
            f"等差數列首項 {a1}，公差 {d}，第幾項為 {target}？",
            f"AP: first term {a1}, d = {d}. Which term equals {target}?",
            [f"A. 第 {n} 項",f"B. 第 {n+1} 項",f"C. 第 {n-1} 項",f.D. 不存在],
            [f"A. Term {n}",f"B. Term {n+1}",f"C. Term {n-1}",f"D. Does not exist"],
            0, f"{target} = {a1} + (n-1)({d})，n = {n}。", f"{target} = {a1} + (n-1)({d}), n = {n}.", 2)

# 7b. Geometric sequences (100)
for _ in range(100):
    a1 = random.choice([1,2,3,4,5])
    r = random.choice([2,3,-2,0.5,-0.5])
    n = random.randint(3,8)
    an = round(a1 * r**(n-1), 4)
    if abs(an) > 10000: an = int(an)
    qtype = random.choice(["nth","sum","find_r"])
    if qtype == "nth":
        add(T7,T7Z,T7E,"geometric_sequences","等比數列","Geometric Sequences",
            f"等比數列首項 {a1}，公比 {r}，求第 {n} 項。",
            f"GP: first term {a1}, ratio {r}. Find {n}th term.",
            [f"A. {an}",f"B. {round(an*r,4)}",f"C. {round(an/r,4)}",f"D. {a1*r**n}"],
            [f"A. {an}",f"B. {round(an*r,4)}",f"C. {round(an/r,4)}",f"D. {a1*r**n}"],
            0, f"a\u2099 = {a1} \u00d7 {r}^{n-1} = {an}。", f"a\u2099 = {a1} \u00d7 {r}^{n-1} = {an}.", 1)
    elif qtype == "sum":
        if r == 1: sn = a1 * n
        else: sn = round(a1 * (r**n - 1) / (r - 1), 4)
        add(T7,T7Z,T7E,"geometric_series","等比級數","Geometric Series",
            f"等比數列首項 {a1}，公比 {r}，求前 {n} 項和。",
            f"GP: first term {a1}, ratio {r}. Sum of first {n} terms.",
            [f"A. {sn}",f"B. {round(sn*1.1,4)}",f"C. {round(sn*0.9,4)}",f"D. {a1*n}"],
            [f"A. {sn}",f"B. {round(sn*1.1,4)}",f"C. {round(sn*0.9,4)}",f"D. {a1*n}"],
            0, f"S = {a1}\u00d7({r}^{n}-1)/({r}-1) = {sn}。", f"S = {a1}\u00d7({r}^{n}-1)/({r}-1) = {sn}.", 2)
    else:
        a2 = a1*r; a3 = a1*r*r
        add(T7,T7Z,T7E,"geometric_sequences","等比數列","Geometric Sequences",
            f"等比數列前3項為 {a1}, {int(a2)}, {int(a3)}，求公比。",
            f"GP: first 3 terms {a1}, {int(a2)}, {int(a3)}. Find common ratio.",
            [f"A. r = {r}",f"B. r = {r+1}",f"C. r = {r-1}",f"D. r = {-r}"],
            [f"A. r = {r}",f"B. r = {r+1}",f"C. r = {r-1}",f"D. r = {-r}"],
            0, f"r = {int(a2)}/{a1} = {r}。", f"r = {int(a2)}/{a1} = {r}.", 1)

# 7c. Infinite GP (80)
for _ in range(80):
    a1 = random.choice([1,2,3,4,5])
    r = random.choice([0.5, 0.25, 1/3, -0.5, 0.1, 0.2])
    if abs(r) >= 1: r = 0.5
    s = round(a1 / (1 - r), 4)
    add(T7,T7Z,T7E,"infinite_gp","無限等比級數","Infinite GP",
        f"無限等比級數首項 {a1}，公比 {r}，求其和。",
        f"Infinite GP: first term {a1}, ratio {r}. Find sum to infinity.",
        [f"A. {s}",f"B. {round(s*2,4)}",f"C. {round(s/2,4)}",f.D. 不存在],
        [f"A. {s}",f"B. {round(s*2,4)}",f"C. {round(s/2,4)}",f"D. Does not exist"],
        0, f"S\u221e = {a1}/(1-({r})) = {a1}/{round(1-r,4)} = {s}。",
        f"S\u221e = {a1}/(1-({r})) = {a1}/{round(1-r,4)} = {s}.", 2)

# 7d. Applications (70)
for _ in range(70):
    p0 = random.choice([10000,50000,100000])
    rate = random.choice([0.03,0.05,0.06,0.08])
    years = random.choice([5,10,15,20])
    fv = round(p0 * (1 + rate)**years, 2)
    add(T7,T7Z,T7E,"sequences_applications","數列應用","Applications of Sequences",
        f"本金 ${p0}，年利率 {rate*100}%，複利計算。{years}年後金額為何？",
        f"Principal ${p0}, annual rate {rate*100}%, compound interest. Amount after {years} years?",
        [f"A. ${fv}",f"B. ${round(fv*0.9,2)}",f"C. ${p0+years*int(p0*rate)}",f.D. ${round(fv*1.1,2)}"],
        [f"A. ${fv}",f"B. ${round(fv*0.9,2)}",f"C. ${p0+years*int(p0*rate)}",f"D. ${round(fv*1.1,2)}"],
        0, f"A = {p0}(1+{rate})^{years} = ${fv}。", f"A = {p0}(1+{rate})^{years} = ${fv}.", 2)

print(f"  Sequences & series: {qid} questions so far")

# --- 8. MATHEMATICAL INDUCTION (200) ---
print("Generating mathematical induction...")
T8,T8Z,T8E = "mathematical_induction","數學歸納法","Mathematical Induction"

induction_problems = [
    ("1+2+3+...+n = n(n+1)/2","1+2+3+...+n = n(n+1)/2",
     "假設 n=k 時成立，即 1+2+...+k = k(k+1)/2","Assume true for n=k: 1+2+...+k = k(k+1)/2",
     "則 n=k+1 時，1+2+...+k+(k+1) = k(k+1)/2 + (k+1) = (k+1)(k+2)/2","For n=k+1: k(k+1)/2+(k+1)=(k+1)(k+2)/2"),
    ("1\u00b2+2\u00b2+...+n\u00b2 = n(n+1)(2n+1)/6","1\u00b2+2\u00b2+...+n\u00b2 = n(n+1)(2n+1)/6",
     "假設 n=k 時成立","Assume true for n=k",
     "則 n=k+1 時利用歸納假設可證","For n=k+1, using induction hypothesis"),
    ("2\u02b0 > n for n \u2265 1","2\u02b0 > n for n \u2265 1",
     "假設 2\u1d42 > k","Assume 2\u1d42 > k",
     "則 2\u1d42\u207a\u00b9 = 2\u00b72\u1d42 > 2k > k+1 for k\u22651","2\u1d42\u207a\u00b9=2\u00b72\u1d42>2k>k+1 for k\u22651"),
    ("3\u02b0 - 1 is divisible by 2","3\u02b0 - 1 is divisible by 2",
     "假設 3\u1d42 - 1 = 2m for some integer m","Assume 3\u1d42 - 1 = 2m",
     "3\u1d42\u207a\u00b9 - 1 = 3(3\u1d42) - 1 = 3(2m+1) - 1 = 6m+2 = 2(3m+1)","3\u1d42\u207a\u00b9-1 = 3(2m+1)-1 = 6m+2 = 2(3m+1)"),
    ("5\u02b0 - 1 is divisible by 4","5\u02b0 - 1 is divisible by 4",
     "假設 5\u1d42 - 1 = 4m","Assume 5\u1d42 - 1 = 4m",
     "5\u1d42\u207a\u00b9 - 1 = 5(4m+1)-1 = 20m+4 = 4(5m+1)","5\u1d42\u207a\u00b9-1 = 5(4m+1)-1 = 20m+4 = 4(5m+1)"),
    ("n(n+1) is always even","n(n+1) is always even",
     "假設 k(k+1) 為偶數","Assume k(k+1) is even",
     "(k+1)(k+2) = k(k+1) + 2(k+1) 亦為偶數","(k+1)(k+2)=k(k+1)+2(k+1) is also even"),
]
for _ in range(200):
    p = random.choice(induction_problems)
    qtype = random.choice(["base","inductive_step","conclusion"])
    if qtype == "base":
        add(T8,T8Z,T8E,"induction_base","歸納法基礎步","Base Case",
            f"用數學歸納法證明 {p[0]}，基礎步為何？",
            f"Prove {p[1]} by induction. What is the base case?",
            [f"A. 驗證 n=1 成立",f"B. 假設 n=k 成立",f"C. 驗證 n=2 成立",f.D. 直接得出結論"],
            [f"A. Verify n=1 is true",f"B. Assume n=k is true",f"C. Verify n=2",f"D. Conclude directly"],
            0, "基礎步：驗證 n=1 時命題成立。", "Base case: verify the proposition holds for n=1.", 1)
    elif qtype == "inductive_step":
        add(T8,T8Z,T8E,"inductive_step","歸納步驟","Inductive Step",
            f"用數學歸納法證明 {p[0]}，歸納假設為何？",
            f"Prove {p[1]} by induction. What is the inductive hypothesis?",
            [f"A. {p[2]}",f"B. 假設所有 n 成立",f.C. 驗證 n=1",f.D. 直接計算"],
            [f"A. {p[3]}",f"B. Assume all n true",f"C. Verify n=1",f"D. Direct calculation"],
            0, f"歸納假設：{p[2]}。", f"Inductive hypothesis: {p[3]}.", 2)
    else:
        add(T8,T8Z,T8E,"induction_conclusion","歸納法結論","Conclusion",
            f"用數學歸納法證明 {p[0]}，歸納步的結論為何？",
            f"Prove {p[1]} by induction. Conclusion of inductive step?",
            [f"A. {p[4]}",f.B. 回到基礎步",f.C. 不成立",f.D. 需要更多驗證"],
            [f"A. {p[5]}",f"B. Return to base case",f"C. Not valid",f"D. Need more verification"],
            0, f"歸納步：{p[4]}。", f"Inductive step: {p[5]}.", 2)

print(f"  Mathematical induction: {qid} questions so far")

# --- 9. BINOMIAL THEOREM (250) ---
print("Generating binomial theorem...")
T9,T9Z,T9E = "binomial_theorem","二項式定理","Binomial Theorem"

# 9a. Binomial expansion (100)
for _ in range(100):
    n = random.randint(2,6)
    r = random.randint(0,n)
    coeff = math.comb(n,r)
    add(T9,T9Z,T9E,"binomial_expansion","二項式展開","Binomial Expansion",
        f"求 (1+x)^{n} 展開式中 x^{r} 的係數。",
        f"Find the coefficient of x^{r} in the expansion of (1+x)^{n}.",
        [f"A. {coeff}",f"B. {coeff+1}",f"C. {coeff-1}",f"D. {n}"],
        [f"A. {coeff}",f"B. {coeff+1}",f"C. {coeff-1}",f"D. {n}"],
        0, f"C({n},{r}) = {coeff}。", f"C({n},{r}) = {coeff}.", 1)

# 9b. General term (80)
for _ in range(80):
    n = random.randint(3,7)
    r = random.randint(1,n)
    coeff = math.comb(n,r)
    add(T9,T9Z,T9E,"general_term","通項","General Term",
        f"(a+b)^{n} 展開式的第 {r+1} 項為何？",
        f"Find the (r+1)th term in expansion of (a+b)^{n}, r={r}.",
        [f"A. C({n},{r})a^{n-r}b^{r}",f"B. C({n},{r-1})a^{n-r+1}b^{r-1}",
         f"C. C({n},{r+1})a^{n-r-1}b^{r+1}",f"D. C({n},{r})a^{r}b^{n-r}"],
        [f"A. C({n},{r})a^{n-r}b^{r}",f"B. C({n},{r-1})a^{n-r+1}b^{r-1}",
         f"C. C({n},{r+1})a^{n-r-1}b^{r+1}",f"D. C({n},{r})a^{r}b^{n-r}"],
        0, f"第{r+1}項 = C({n},{r})a^{n-r}b^{r}。", f"({r+1})th term = C({n},{r})a^{n-r}b^{r}.", 2)

# 9c. Specific coefficient problems (70)
for _ in range(70):
    n = random.choice([3,4,5,6])
    a_val = random.choice([1,2])
    # (1+ax)^n expansion
    for r in range(n+1):
        coeff = math.comb(n,r) * a_val**r
        if r >= 1:
            break
    r_use = random.randint(1,n)
    coeff_use = math.comb(n,r_use) * a_val**r_use
    add(T9,T9Z,T9E,"specific_coefficient","特定係數","Specific Coefficient",
        f"求 (1+{a_val}x)^{n} 展開式中 x^{r_use} 的係數。",
        f"Find coefficient of x^{r_use} in (1+{a_val}x)^{n}.",
        [f"A. {coeff_use}",f"B. {coeff_use+1}",f"C. {math.comb(n,r_use)}",f"D. {a_val**r_use}"],
        [f"A. {coeff_use}",f"B. {coeff_use+1}",f"C. {math.comb(n,r_use)}",f"D. {a_val**r_use}"],
        0, f"C({n},{r_use})\u00d7{a_val}^{r_use} = {coeff_use}。",
        f"C({n},{r_use})\u00d7{a_val}^{r_use} = {coeff_use}.", 2)

print(f"  Binomial theorem: {qid} questions so far")

# --- 10. MATRICES AND DETERMINANTS (300) ---
print("Generating matrices...")
T10,T10Z,T10E = "matrices","矩陣與行列式","Matrices and Determinants"

# 10a. Matrix operations (80)
for _ in range(80):
    a,b,c,d = [random.randint(-5,5) for _ in range(4)]
    e,f_,g,h = [random.randint(-5,5) for _ in range(4)]
    op = random.choice(["add","multiply"])
    if op == "add":
        rz, re = f"[{a+e} {b+f_}; {c+g} {d+h}]", f"[{a+e} {b+f_}; {c+g} {d+h}]"
        qz = f"求 [{a} {b}; {c} {d}] + [{e} {f_}; {g} {h}]"
        qe = f"Find [{a} {b}; {c} {d}] + [{e} {f_}; {g} {h}]"
        ez = f"對應元素相加得 {rz}。"
        ee = f"Element-wise addition gives {re}."
    else:
        # 2x2 multiplication
        r00 = a*e + b*g; r01 = a*f_ + b*h; r10 = c*e + d*g; r11 = c*f_ + d*h
        rz = f"[{r00} {r01}; {r10} {r11}]"
        qz = f"求 [{a} {b}; {c} {d}] \u00d7 [{e} {f_}; {g} {h}]"
        qe = qz
        ez = f"矩陣乘法得 {rz}。"
        ee = f"Matrix multiplication gives {rz}."
    add(T10,T10Z,T10E,"matrix_operations","矩陣運算","Matrix Operations",qz,qe,
        [f"A. {rz}",f"B. [{a+1} {b}; {c} {d}]",f"C. [{a} {b+1}; {c} {d}]",f"D. 單位矩陣"],
        [f"A. {rz}",f"B. [{a+1} {b}; {c} {d}]",f"C. [{a} {b+1}; {c} {d}]",f"D. Identity matrix"],
        0, ez, ee, random.choice([1,2]))

# 10b. 2x2 determinants (80)
for _ in range(80):
    a,b,c,d = [random.randint(-5,5) for _ in range(4)]
    det = a*d - b*c
    add(T10,T10Z,T10E,"determinant_2x2","2\u00d72行列式","2\u00d72 Determinant",
        f"求行列式 |{a} {b}; {c} {d}| 的值。",
        f"Find det |{a} {b}; {c} {d}|.",
        [f"A. {det}",f"B. {det+1}",f"C. {det-1}",f"D. {a*d+b*c}"],
        [f"A. {det}",f"B. {det+1}",f"C. {det-1}",f"D. {a*d+b*c}"],
        0, f"det = ({a})({d}) - ({b})({c}) = {a*d} - {b*c} = {det}。",
        f"det = ({a})({d}) - ({b})({c}) = {a*d} - {b*c} = {det}.", 1)

# 10c. Inverse matrices (70)
for _ in range(70):
    a,b,c,d = [random.randint(-3,3) for _ in range(4)]
    det = a*d - b*c
    while det == 0:
        a,b,c,d = [random.randint(-3,3) for _ in range(4)]
        det = a*d - b*c
    inv = f"(1/{det})[{d} {-b}; {-c} {a}]"
    add(T10,T10Z,T10E,"inverse_matrix","逆矩陣","Inverse Matrix",
        f"求 [{a} {b}; {c} {d}] 的逆矩陣。",
        f"Find inverse of [{a} {b}; {c} {d}].",
        [f"A. {inv}",f"B. (1/{det})[{a} {b}; {c} {d}]",f"C. [{d} {-b}; {-c} {a}]",f.D. 不存在],
        [f"A. {inv}",f"B. (1/{det})[{a} {b}; {c} {d}]",f"C. [{d} {-b}; {-c} {a}]",f"D. Does not exist"],
        0, f"det = {det}，逆矩陣 = (1/{det})[{d} {-b}; {-c} {a}]。",
        f"det = {det}, inverse = (1/{det})[{d} {-b}; {-c} {a}].", 2)

# 10d. Systems of linear equations (70)
for _ in range(70):
    a1,b1,c1 = random.randint(1,5), random.randint(-5,5), random.randint(-10,10)
    a2,b2,c2 = random.randint(1,5), random.randint(-5,5), random.randint(-10,10)
    D = a1*b2 - a2*b1
    while D == 0:
        a2,b2 = random.randint(1,5), random.randint(-5,5)
        D = a1*b2 - a2*b1
    Dx = c1*b2 - c2*b1; Dy = a1*c2 - a2*c1
    x = round(Dx/D, 4); y = round(Dy/D, 4)
    if x == int(x): x = int(x)
    if y == int(y): y = int(y)
    add(T10,T10Z,T10E,"linear_systems","聯立方程","Systems of Linear Equations",
        f"用行列式解：{a1}x + {b1}y = {c1}，{a2}x + {b2}y = {c2}。",
        f"Solve by determinants: {a1}x + {b1}y = {c1}, {a2}x + {b2}y = {c2}.",
        [f"A. x={x}, y={y}",f"B. x={x+1}, y={y}",f"C. x={x}, y={y+1}",f.D. 無解"],
        [f"A. x={x}, y={y}",f"B. x={x+1}, y={y}",f"C. x={x}, y={y+1}",f"D. No solution"],
        0, f"D={D}, D_x={Dx}, D_y={Dy}, x={x}, y={y}。", f"D={D}, Dx={Dx}, Dy={Dy}, x={x}, y={y}.", 2)

print(f"  Matrices: {qid} questions so far")

# --- 11. VARIATIONS (100) ---
print("Generating variations...")
T11,T11Z,T11E = "variations","變數關係","Variations"

for _ in range(100):
    vtype = random.choice(["direct","inverse","joint","partial"])
    k = random.choice([2,3,4,5,6])
    x1 = random.randint(2,10)
    if vtype == "direct":
        y1 = k * x1
        x2 = random.randint(2,10)
        y2 = k * x2
        add(T11,T11Z,T11E,"direct_variation","正變","Direct Variation",
            f"若 y \u221d x，且當 x={x1} 時 y={y1}，求當 x={x2} 時 y 的值。",
            f"If y \u221d x, and y={y1} when x={x1}, find y when x={x2}.",
            [f"A. y = {y2}",f"B. y = {y2+1}",f"C. y = {y2-1}",f.D. y = {y2*2}"],
            [f"A. y = {y2}",f"B. y = {y2+1}",f"C. y = {y2-1}",f"D. y = {y2*2}"],
            0, f"y = kx, k = {y1}/{x1} = {k}, y = {k}\u00d7{x2} = {y2}。",
            f"y = kx, k = {y1}/{x1} = {k}, y = {k}\u00d7{x2} = {y2}.", 1)
    elif vtype == "inverse":
        y1 = k * 100 // x1  # make it clean
        k_actual = y1 * x1
        x2 = random.randint(2,10)
        y2 = k_actual // x2 if k_actual % x2 == 0 else round(k_actual / x2, 2)
        add(T11,T11Z,T11E,"inverse_variation","反變","Inverse Variation",
            f"若 y \u221d 1/x，且當 x={x1} 時 y={y1}，求當 x={x2} 時 y 的值。",
            f"If y \u221d 1/x, y={y1} when x={x1}, find y when x={x2}.",
            [f"A. y = {y2}",f"B. y = {y2+1}",f"C. y = {round(y1*x1/x2+1,2)}",f.D. y = {y1}"],
            [f"A. y = {y2}",f"B. y = {y2+1}",f"C. y = {round(y1*x1/x2+1,2)}",f"D. y = {y1}"],
            0, f"y = k/x, k = {y1}\u00d7{x1} = {k_actual}, y = {k_actual}/{x2} = {y2}。",
            f"y = k/x, k = {y1}\u00d7{x1} = {k_actual}, y = {k_actual}/{x2} = {y2}.", 2)
    elif vtype == "joint":
        z1 = k * x1 * random.randint(2,5)
        y1_val = random.randint(2,5)
        z1 = k * x1 * y1_val
        x2 = random.randint(2,10); y2_val = random.randint(2,5)
        z2 = k * x2 * y2_val
        add(T11,T11Z,T11E,"joint_variation","聯變","Joint Variation",
            f"若 z \u221d xy，且當 x={x1}, y={y1_val} 時 z={z1}，求當 x={x2}, y={y2_val} 時 z 的值。",
            f"If z \u221d xy, z={z1} when x={x1}, y={y1_val}, find z when x={x2}, y={y2_val}.",
            [f"A. z = {z2}",f"B. z = {z2+1}",f"C. z = {z2-1}",f.D. z = {z2*2}"],
            [f"A. z = {z2}",f"B. z = {z2+1}",f"C. z = {z2-1}",f"D. z = {z2*2}"],
            0, f"z = kxy, k = {z1}/({x1}\u00d7{y1_val}) = {k}, z = {k}\u00d7{x2}\u00d7{y2_val} = {z2}。",
            f"z = kxy, k = {z1}/({x1}\u00d7{y1_val}) = {k}, z = {k}\u00d7{x2}\u00d7{y2_val} = {z2}.", 2)
    else:  # partial
        c = random.randint(1,5)
        y1 = k*x1 + c
        x2 = random.randint(2,10)
        y2 = k*x2 + c
        add(T11,T11Z,T11E,"partial_variation","部分變","Partial Variation",
            f"若 y = kx + c，且當 x={x1} 時 y={y1}，x=0 時 y={c}，求當 x={x2} 時 y 的值。",
            f"If y = kx + c, y={y1} when x={x1}, y={c} when x=0, find y when x={x2}.",
            [f"A. y = {y2}",f"B. y = {y2+1}",f"C. y = {y2-1}",f.D. y = {k*x2}"],
            [f"A. y = {y2}",f"B. y = {y2+1}",f"C. y = {y2-1}",f"D. y = {k*x2}"],
            0, f"k = ({y1}-{c})/{x1} = {k}, y = {k}\u00d7{x2}+{c} = {y2}。",
            f"k = ({y1}-{c})/{x1} = {k}, y = {k}\u00d7{x2}+{c} = {y2}.", 2)

print(f"  Variations: {qid} questions so far")
print(f"=== PART 1 TOTAL: {qid} ===")

# Save checkpoint
part1_count = qid
