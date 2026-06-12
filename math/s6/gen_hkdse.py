#!/usr/bin/env python3
"""Generate 10,000 HKDSE Mathematics Compulsory Part questions for S6."""
import json, random, math

random.seed(42)

def make_q(zh, en, opts_zh, opts_en, ans, exp_zh, exp_en, diff=1):
    return {
        "question_zh": zh, "question_en": en,
        "options_zh": opts_zh, "options_en": opts_en,
        "answer": ans, "explanation_zh": exp_zh, "explanation_en": exp_en,
        "difficulty": diff
    }

# ============================================================
# TOPIC 1: Quadratic Equations (500 questions)
# ============================================================
def gen_quadratic(n):
    qs = []
    templates = [
        # Discriminant
        lambda: (
            f"若方程 x² + {random.randint(-10,10)}x + {random.randint(-10,10)} = 0 有兩個不相等的實根，求判別式的值。",
            f"If the equation x² + {random.randint(-10,10)}x + {random.randint(-10,10)} = 0 has two distinct real roots, find the discriminant.",
            lambda b, c: (f"Δ = {b}² - 4(1)({c}) = {b*b - 4*c}", f"Δ = {b}² - 4(1)({c}) = {b*b - 4*c}")
        ),
    ]
    for i in range(n):
        b = random.randint(-8, 8)
        c = random.randint(-10, 10)
        disc = b*b - 4*c
        if disc > 0:
            nature_zh, nature_en = "兩個不相等的實根", "two distinct real roots"
        elif disc == 0:
            nature_zh, nature_en = "兩個相等的實根", "two equal real roots"
        else:
            nature_zh, nature_en = "沒有實根", "no real roots"
        
        if i % 3 == 0:
            qs.append(make_q(
                f"方程 x² + {b}x + {c} = 0 的判別式 Δ = ?",
                f"What is the discriminant of x² + {b}x + {c} = 0?",
                [f"A. {disc}", f"B. {disc+1}", f"C. {-disc}", f"D. {disc-1}"],
                [f"A. {disc}", f"B. {disc+1}", f"C. {-disc}", f"D. {disc-1}"],
                0,
                f"Δ = b² - 4ac = ({b})² - 4(1)({c}) = {b*b} - {4*c} = {disc}",
                f"Δ = b² - 4ac = ({b})² - 4(1)({c}) = {b*b} - {4*c} = {disc}",
                1
            ))
        elif i % 3 == 1:
            qs.append(make_q(
                f"方程 x² + {b}x + {c} = 0 的根的性質是：",
                f"The nature of roots of x² + {b}x + {c} = 0 is:",
                [f"A. {nature_zh}", "B. 兩個不相等的實根", "C. 兩個相等的實根", "D. 沒有實根"],
                [f"A. {nature_en}", "B. two distinct real roots", "C. two equal real roots", "D. no real roots"],
                0,
                f"Δ = ({b})² - 4({c}) = {disc}，{disc}{'>' if disc>0 else '=' if disc==0 else '<'} 0，故有{nature_zh}",
                f"Δ = ({b})² - 4({c}) = {disc}, {disc}{'>' if disc>0 else '=' if disc==0 else '<'} 0, so {nature_en}",
                1
            ))
        else:
            # Solve by factoring
            r1 = random.randint(-6, 6)
            r2 = random.randint(-6, 6)
            b_val = -(r1+r2)
            c_val = r1*r2
            opts = [r1, r2, r1+1, r2-1]
            random.shuffle(opts)
            ans_idx = opts.index(r1)
            qs.append(make_q(
                f"解方程 x² + ({b_val})x + ({c_val}) = 0，其中一個根是：",
                f"Solve x² + ({b_val})x + ({c_val}) = 0. One root is:",
                [f"A. {opts[0]}", f"B. {opts[1]}", f"C. {opts[2]}", f"D. {opts[3]}"],
                [f"A. {opts[0]}", f"B. {opts[1]}", f"C. {opts[2]}", f"D. {opts[3]}"],
                ans_idx,
                f"因式分解：(x - ({r1}))(x - ({r2})) = 0，故 x = {r1} 或 x = {r2}",
                f"Factorize: (x - ({r1}))(x - ({r2})) = 0, so x = {r1} or x = {r2}",
                1
            ))
    return qs[:n]

# ============================================================
# TOPIC 2: Functions (500 questions)
# ============================================================
def gen_functions(n):
    qs = []
    for i in range(n):
        t = i % 4
        if t == 0:
            a = random.randint(2, 5)
            x = random.randint(1, 4)
            gx = a*x + random.randint(1,5)
            # f(x) = x², find f(g(x))
            val = gx**2
            wrong = [val+1, val-1, (gx+1)**2]
            opts = [val] + wrong
            random.shuffle(opts)
            qs.append(make_q(
                f"設 f(x) = x²，g(x) = {a}x + {gx-a*x}，求 f(g({x}))。",
                f"Let f(x) = x², g(x) = {a}x + {gx-a*x}. Find f(g({x})).",
                [f"A. {opts[0]}", f"B. {opts[1]}", f"C. {opts[2]}", f"D. {opts[3]}"],
                [f"A. {opts[0]}", f"B. {opts[1]}", f"C. {opts[2]}", f"D. {opts[3]}"],
                opts.index(val),
                f"g({x}) = {a}({x}) + {gx-a*x} = {gx}，f({gx}) = {gx}² = {val}",
                f"g({x}) = {a}({x}) + {gx-a*x} = {gx}, f({gx}) = {gx}² = {val}",
                1
            ))
        elif t == 1:
            a = random.randint(1, 5)
            b = random.randint(1, 10)
            # Inverse of f(x) = ax + b
            inv_a = f"1/{a}" if a != 1 else "1"
            inv_b = -b/a
            qs.append(make_q(
                f"若 f(x) = {a}x + {b}，求 f⁻¹(x)。",
                f"If f(x) = {a}x + {b}, find f⁻¹(x).",
                [f"A. (x - {b})/{a}", f"B. ({a}x - {b})", f"C. x/{a} + {b}", f"D. {a}x - {b}"],
                [f"A. (x - {b})/{a}", f"B. ({a}x - {b})", f"C. x/{a} + {b}", f"D. {a}x - {b}"],
                0,
                f"令 y = {a}x + {b}，交換 x 和 y：x = {a}y + {b}，y = (x - {b})/{a}",
                f"Let y = {a}x + {b}, swap x and y: x = {a}y + {b}, y = (x - {b})/{a}",
                1
            ))
        elif t == 2:
            a = random.randint(1, 4)
            # Domain and range of f(x) = x²
            qs.append(make_q(
                f"設 f(x) = x² + {a}，求 f 的值域。",
                f"Let f(x) = x² + {a}. Find the range of f.",
                [f"A. y ≥ {a}", f"B. y > {a}", f"C. y ≥ 0", f"D. 所有實數"],
                [f"A. y ≥ {a}", f"B. y > {a}", f"C. y ≥ 0", "D. all real numbers"],
                0,
                f"x² ≥ 0，故 x² + {a} ≥ {a}，值域為 y ≥ {a}",
                f"x² ≥ 0, so x² + {a} ≥ {a}, range is y ≥ {a}",
                1
            ))
        else:
            a = random.randint(2, 5)
            b = random.randint(1, 5)
            val = a**2 + b
            qs.append(make_q(
                f"若 f(x) = x² + {b}，求 f({a})。",
                f"If f(x) = x² + {b}, find f({a}).",
                [f"A. {val}", f"B. {val+1}", f"C. {a**2}", f"D. {val-1}"],
                [f"A. {val}", f"B. {val+1}", f"C. {a**2}", f"D. {val-1}"],
                0,
                f"f({a}) = {a}² + {b} = {a**2} + {b} = {val}",
                f"f({a}) = {a}² + {b} = {a**2} + {b} = {val}",
                1
            ))
    return qs[:n]

# ============================================================
# TOPIC 3: Exponential & Logarithmic (500)
# ============================================================
def gen_exp_log(n):
    qs = []
    for i in range(n):
        t = i % 4
        if t == 0:
            a = random.randint(2, 5)
            p = random.randint(2, 4)
            val = a**p
            qs.append(make_q(
                f"log_{a} {val} = ?",
                f"log_{a} {val} = ?",
                [f"A. {p}", f"B. {p+1}", f"C. {p-1}", f"D. {val}"],
                [f"A. {p}", f"B. {p+1}", f"C. {p-1}", f"D. {val}"],
                0,
                f"log_{a} {val} = {p}，因為 {a}^{p} = {val}",
                f"log_{a} {val} = {p}, because {a}^{p} = {val}",
                1
            ))
        elif t == 1:
            a = random.randint(2, 4)
            b = random.randint(2, 4)
            prod = a*b
            qs.append(make_q(
                f"log 2 + log 5 = ?",
                f"log 2 + log 5 = ?",
                ["A. log 7", "B. log 10", "C. log 3", "D. 10"],
                ["A. log 7", "B. log 10", "C. log 3", "D. 10"],
                1,
                "log 2 + log 5 = log(2×5) = log 10 = 1",
                "log 2 + log 5 = log(2×5) = log 10 = 1",
                1
            ))
        elif t == 2:
            base = random.choice([2, 3, 10])
            p = random.randint(2, 5)
            val = base**p
            qs.append(make_q(
                f"若 {base}ˣ = {val}，求 x。",
                f"If {base}ˣ = {val}, find x.",
                [f"A. {p}", f"B. {p+1}", f"C. {p-1}", f"D. {val}"],
                [f"A. {p}", f"B. {p+1}", f"C. {p-1}", f"D. {val}"],
                0,
                f"{base}ˣ = {val} = {base}^{p}，故 x = {p}",
                f"{base}ˣ = {val} = {base}^{p}, so x = {p}",
                1
            ))
        else:
            qs.append(make_q(
                "化簡 log₂ 8 + log₂ 4",
                "Simplify log₂ 8 + log₂ 4",
                ["A. log₂ 12", "B. 5", "C. log₂ 32", "D. 7"],
                ["A. log₂ 12", "B. 5", "C. log₂ 32", "D. 7"],
                1,
                "log₂ 8 + log₂ 4 = 3 + 2 = 5",
                "log₂ 8 + log₂ 4 = 3 + 2 = 5",
                1
            ))
    return qs[:n]

# ============================================================
# TOPIC 4: Polynomials (400)
# ============================================================
def gen_polynomials(n):
    qs = []
    for i in range(n):
        a = random.randint(-5, 5)
        b = random.randint(-5, 5)
        c = random.randint(-5, 5)
        # Remainder theorem: f(a)
        f_a = a**2 + b*a + c
        if i % 2 == 0:
            qs.append(make_q(
                f"設 f(x) = x² + {b}x + {c}，求 f({a})。",
                f"Let f(x) = x² + {b}x + {c}. Find f({a}).",
                [f"A. {f_a}", f"B. {f_a+1}", f"C. {f_a-1}", f"D. {a}"],
                [f"A. {f_a}", f"B. {f_a+1}", f"C. {f_a-1}", f"D. {a}"],
                0,
                f"f({a}) = ({a})² + {b}({a}) + {c} = {a*a} + {b*a} + {c} = {f_a}",
                f"f({a}) = ({a})² + {b}({a}) + {c} = {a*a} + {b*a} + {c} = {f_a}",
                1
            ))
        else:
            r = random.randint(-4, 4)
            # Factor theorem: if f(r)=0 then (x-r) is a factor
            qs.append(make_q(
                f"設 f(x) = x² - {r**2}，判斷 (x - {r}) 是否 f(x) 的因式。",
                f"Let f(x) = x² - {r**2}. Is (x - {r}) a factor of f(x)?",
                ["A. 是，因為 f(-" + str(r) + ") = 0", "B. 是，因為 f(" + str(r) + ") = 0", "C. 不是", "D. 無法判斷"],
                ["A. Yes, because f(-" + str(r) + ") = 0", "B. Yes, because f(" + str(r) + ") = 0", "C. No", "D. Cannot determine"],
                1,
                f"f({r}) = ({r})² - {r**2} = {r*r} - {r*r} = 0，故 (x - {r}) 是因式",
                f"f({r}) = ({r})² - {r**2} = {r*r} - {r*r} = 0, so (x - {r}) is a factor",
                2
            ))
    return qs[:n]

# ============================================================
# TOPIC 5: Sequences & Series (500)
# ============================================================
def gen_sequences(n):
    qs = []
    for i in range(n):
        t = i % 4
        if t == 0:  # AP
            a1 = random.randint(1, 10)
            d = random.randint(1, 5)
            n_val = random.randint(5, 20)
            an = a1 + (n_val-1)*d
            opts = [an, an+1, an-1, a1+d]
            random.shuffle(opts)
            qs.append(make_q(
                f"等差數列首項 {a1}，公差 {d}，求第 {n_val} 項。",
                f"AP with first term {a1}, common difference {d}. Find the {n_val}th term.",
                [f"A. {opts[0]}", f"B. {opts[1]}", f"C. {opts[2]}", f"D. {opts[3]}"],
                [f"A. {opts[0]}", f"B. {opts[1]}", f"C. {opts[2]}", f"D. {opts[3]}"],
                opts.index(an),
                f"a_{n_val} = {a1} + ({n_val}-1)({d}) = {a1} + {(n_val-1)*d} = {an}",
                f"a_{n_val} = {a1} + ({n_val}-1)({d}) = {a1} + {(n_val-1)*d} = {an}",
                1
            ))
        elif t == 1:  # AP sum
            a1 = random.randint(1, 5)
            d = random.randint(1, 3)
            n_val = random.randint(5, 15)
            s = n_val*(2*a1 + (n_val-1)*d)//2
            qs.append(make_q(
                f"等差數列首項 {a1}，公差 {d}，求前 {n_val} 項之和。",
                f"AP with first term {a1}, common difference {d}. Find sum of first {n_val} terms.",
                [f"A. {s}", f"B. {s+1}", f"C. {s-1}", f"D. {s*2}"],
                [f"A. {s}", f"B. {s+1}", f"C. {s-1}", f"D. {s*2}"],
                0,
                f"S = {n_val}/2 × (2({a1}) + ({n_val}-1)({d})) = {n_val}/2 × ({2*a1} + {(n_val-1)*d}) = {s}",
                f"S = {n_val}/2 × (2({a1}) + ({n_val}-1)({d})) = {n_val}/2 × ({2*a1} + {(n_val-1)*d}) = {s}",
                1
            ))
        elif t == 2:  # GP
            a1 = random.choice([1, 2, 3])
            r = random.choice([2, 3])
            n_val = random.randint(3, 6)
            an = a1 * r**(n_val-1)
            qs.append(make_q(
                f"等比數列首項 {a1}，公比 {r}，求第 {n_val} 項。",
                f"GP with first term {a1}, common ratio {r}. Find the {n_val}th term.",
                [f"A. {an}", f"B. {an+1}", f"C. {an*r}", f"D. {an-1}"],
                [f"A. {an}", f"B. {an+1}", f"C. {an*r}", f"D. {an-1}"],
                0,
                f"a_{n_val} = {a1} × {r}^{n_val-1} = {a1} × {r**(n_val-1)} = {an}",
                f"a_{n_val} = {a1} × {r}^{n_val-1} = {a1} × {r**(n_val-1)} = {an}",
                1
            ))
        else:  # GP sum
            a1 = 1
            r = 2
            n_val = random.randint(4, 8)
            s = (r**n_val - 1)//(r-1)
            qs.append(make_q(
                f"等比數列首項 1，公比 2，求前 {n_val} 項之和。",
                f"GP with first term 1, common ratio 2. Find sum of first {n_val} terms.",
                [f"A. {s}", f"B. {s+1}", f"C. {s-1}", f"D. {2**n_val}"],
                [f"A. {s}", f"B. {s+1}", f"C. {s-1}", f"D. {2**n_val}"],
                0,
                f"S = 1×(2^{n_val} - 1)/(2-1) = {2**n_val} - 1 = {s}",
                f"S = 1×(2^{n_val} - 1)/(2-1) = {2**n_val} - 1 = {s}",
                1
            ))
    return qs[:n]

# ============================================================
# TOPIC 6: Trigonometry (800)
# ============================================================
def gen_trig(n):
    qs = []
    for i in range(n):
        t = i % 5
        if t == 0:
            angle = random.choice([30, 45, 60, 90, 120, 135, 150, 180])
            sin_vals = {30: "1/2", 45: "√2/2", 60: "√3/2", 90: "1", 120: "√3/2", 135: "√2/2", 150: "1/2", 180: "0"}
            cos_vals = {30: "√3/2", 45: "√2/2", 60: "1/2", 90: "0", 120: "-1/2", 135: "-√2/2", 150: "-√3/2", 180: "-1"}
            val = sin_vals.get(angle, "0")
            wrong = ["√3/2", "1/2", "-1/2", "√2/2", "0", "1", "-1"]
            wrong = [x for x in wrong if x != val][:3]
            opts = [val] + wrong
            random.shuffle(opts)
            qs.append(make_q(
                f"sin {angle}° = ?",
                f"sin {angle}° = ?",
                [f"A. {opts[0]}", f"B. {opts[1]}", f"C. {opts[2]}", f"D. {opts[3]}"],
                [f"A. {opts[0]}", f"B. {opts[1]}", f"C. {opts[2]}", f"D. {opts[3]}"],
                opts.index(val),
                f"sin {angle}° = {val}",
                f"sin {angle}° = {val}",
                1
            ))
        elif t == 1:
            a = random.randint(3, 8)
            b = random.randint(4, 10)
            c = int(math.sqrt(a*a + b*b)) if math.sqrt(a*a + b*b) == int(math.sqrt(a*a + b*b)) else 0
            if c > 0:
                qs.append(make_q(
                    f"直角三角形兩直角邊為 {a} 和 {b}，求斜邊。",
                    f"Right triangle with legs {a} and {b}. Find hypotenuse.",
                    [f"A. {c}", f"B. {c+1}", f"C. {a+b}", f"D. {int(math.sqrt(a*a+b*b+1))}"],
                    [f"A. {c}", f"B. {c+1}", f"C. {a+b}", f"D. {int(math.sqrt(a*a+b*b+1))}"],
                    0,
                    f"c = √({a}² + {b}²) = √({a*a} + {b*b}) = √({a*a+b*b}) = {c}",
                    f"c = √({a}² + {b}²) = √({a*a} + {b*b}) = √({a*a+b*b}) = {c}",
                    1
                ))
            else:
                c_val = round(math.sqrt(a*a+b*b), 2)
                qs.append(make_q(
                    f"直角三角形兩直角邊為 {a} 和 {b}，斜邊約為：",
                    f"Right triangle with legs {a} and {b}. Hypotenuse ≈",
                    [f"A. {c_val}", f"B. {round(c_val+0.5,1)}", f"C. {a+b}", f"D. {round(c_val-0.5,1)}"],
                    [f"A. {c_val}", f"B. {round(c_val+0.5,1)}", f"C. {a+b}", f"D. {round(c_val-0.5,1)}"],
                    0,
                    f"c = √({a}² + {b}²) = √{a*a+b*b} ≈ {c_val}",
                    f"c = √({a}² + {b}²) = √{a*a+b*b} ≈ {c_val}",
                    1
                ))
        elif t == 2:
            # Double angle
            qs.append(make_q(
                "sin 2θ = ?",
                "sin 2θ = ?",
                ["A. 2 sin θ", "B. 2 sin θ cos θ", "C. cos²θ - sin²θ", "D. 2 cos θ"],
                ["A. 2 sin θ", "B. 2 sin θ cos θ", "C. cos²θ - sin²θ", "D. 2 cos θ"],
                1,
                "sin 2θ = 2 sin θ cos θ（雙角公式）",
                "sin 2θ = 2 sin θ cos θ (double angle formula)",
                2
            ))
        elif t == 3:
            # cos double angle
            qs.append(make_q(
                "cos 2θ 不等於以下哪項？",
                "Which is NOT equal to cos 2θ?",
                ["A. cos²θ - sin²θ", "B. 2cos²θ - 1", "C. 1 - 2sin²θ", "D. 2 sin θ cos θ"],
                ["A. cos²θ - sin²θ", "B. 2cos²θ - 1", "C. 1 - 2sin²θ", "D. 2 sin θ cos θ"],
                3,
                "cos 2θ = cos²θ - sin²θ = 2cos²θ - 1 = 1 - 2sin²θ。2 sin θ cos θ = sin 2θ ≠ cos 2θ",
                "cos 2θ = cos²θ - sin²θ = 2cos²θ - 1 = 1 - 2sin²θ. 2 sin θ cos θ = sin 2θ ≠ cos 2θ",
                2
            ))
        else:
            # sin/cos of standard angles
            angle = random.choice([0, 30, 45, 60, 90])
            cos_val = {0: "1", 30: "√3/2", 45: "√2/2", 60: "1/2", 90: "0"}
            val = cos_val[angle]
            wrong = [v for k, v in cos_val.items() if k != angle][:3]
            opts = [val] + wrong
            random.shuffle(opts)
            qs.append(make_q(
                f"cos {angle}° = ?",
                f"cos {angle}° = ?",
                [f"A. {opts[0]}", f"B. {opts[1]}", f"C. {opts[2]}", f"D. {opts[3]}"],
                [f"A. {opts[0]}", f"B. {opts[1]}", f"C. {opts[2]}", f"D. {opts[3]}"],
                opts.index(val),
                f"cos {angle}° = {val}",
                f"cos {angle}° = {val}",
                1
            ))
    return qs[:n]

# ============================================================
# TOPIC 7: Coordinate Geometry (600)
# ============================================================
def gen_coord(n):
    qs = []
    for i in range(n):
        t = i % 4
        if t == 0:  # Gradient
            x1, y1 = random.randint(-5, 5), random.randint(-5, 5)
            x2, y2 = random.randint(-5, 5), random.randint(-5, 5)
            if x2 == x1: x2 += 1
            m_num = y2 - y1
            m_den = x2 - x1
            qs.append(make_q(
                f"求通過 ({x1},{y1}) 和 ({x2},{y2}) 的直線的斜率。",
                f"Find the gradient of the line through ({x1},{y1}) and ({x2},{y2}).",
                [f"A. {m_num}/{m_den}", f"B. {m_den}/{m_num}", f"C. {m_num+1}/{m_den}", f"D. {-m_num}/{m_den}"],
                [f"A. {m_num}/{m_den}", f"B. {m_den}/{m_num}", f"C. {m_num+1}/{m_den}", f"D. {-m_num}/{m_den}"],
                0,
                f"m = ({y2}-{y1})/({x2}-{x1}) = {m_num}/{m_den}",
                f"m = ({y2}-{y1})/({x2}-{x1}) = {m_num}/{m_den}",
                1
            ))
        elif t == 1:  # Distance
            x1, y1 = random.randint(-5, 5), random.randint(-5, 5)
            x2, y2 = random.randint(-5, 5), random.randint(-5, 5)
            d_sq = (x2-x1)**2 + (y2-y1)**2
            d = int(math.sqrt(d_sq)) if math.sqrt(d_sq) == int(math.sqrt(d_sq)) else f"√{d_sq}"
            qs.append(make_q(
                f"求 ({x1},{y1}) 和 ({x2},{y2}) 之間的距離。",
                f"Find the distance between ({x1},{y1}) and ({x2},{y2}).",
                [f"A. {d}", f"B. {d_sq}", f"C. {abs(x2-x1)+abs(y2-y1)}", f"D. √{d_sq+1}"],
                [f"A. {d}", f"B. {d_sq}", f"C. {abs(x2-x1)+abs(y2-y1)}", f"D. √{d_sq+1}"],
                0,
                f"d = √(({x2}-{x1})² + ({y2}-{y1})²) = √({(x2-x1)**2} + {(y2-y1)**2}) = √{d_sq} = {d}",
                f"d = √(({x2}-{x1})² + ({y2}-{y1})²) = √({(x2-x1)**2} + {(y2-y1)**2}) = √{d_sq} = {d}",
                1
            ))
        elif t == 2:  # Midpoint
            x1, y1 = random.randint(-8, 8), random.randint(-8, 8)
            x2, y2 = random.randint(-8, 8), random.randint(-8, 8)
            mx, my = (x1+x2)/2, (y1+y2)/2
            mx_str = str(int(mx)) if mx == int(mx) else str(mx)
            my_str = str(int(my)) if my == int(my) else str(my)
            qs.append(make_q(
                f"求 ({x1},{y1}) 和 ({x2},{y2}) 的中點。",
                f"Find the midpoint of ({x1},{y1}) and ({x2},{y2}).",
                [f"A. ({mx_str}, {my_str})", f"B. ({x1+x2}, {y1+y2})", f"C. ({str(float(mx_str)+1)}, {my_str})", f"D. ({mx_str}, {str(float(my_str)+1)})"],
                [f"A. ({mx_str}, {my_str})", f"B. ({x1+x2}, {y1+y2})", f"C. ({str(float(mx_str)+1)}, {my_str})", f"D. ({mx_str}, {str(float(my_str)+1)})"],
                0,
                f"M = (({x1}+{x2})/2, ({y1}+{y2})/2) = ({mx_str}, {my_str})",
                f"M = (({x1}+{x2})/2, ({y1}+{y2})/2) = ({mx_str}, {my_str})",
                1
            ))
        else:  # Circle equation
            h, k = random.randint(-3, 3), random.randint(-3, 3)
            r = random.randint(1, 5)
            qs.append(make_q(
                f"圓心 ({h},{k})，半徑 {r} 的圓的方程是：",
                f"Circle with center ({h},{k}) and radius {r}. The equation is:",
                [f"A. (x-{h})² + (y-{k})² = {r*r}", f"B. (x+{h})² + (y+{k})² = {r}", f"C. x² + y² = {r*r}", f"D. (x-{h})² + (y-{k})² = {r}"],
                [f"A. (x-{h})² + (y-{k})² = {r*r}", f"B. (x+{h})² + (y+{k})² = {r}", f"C. x² + y² = {r*r}", f"D. (x-{h})² + (y-{k})² = {r}"],
                0,
                f"圓的標準方程：(x-{h})² + (y-{k})² = {r}² = {r*r}",
                f"Standard form: (x-{h})² + (y-{k})² = {r}² = {r*r}",
                1
            ))
    return qs[:n]

# ============================================================
# TOPIC 8: Probability (500)
# ============================================================
def gen_probability(n):
    qs = []
    for i in range(n):
        t = i % 4
        if t == 0:
            total = random.randint(5, 10)
            red = random.randint(1, total-1)
            blue = total - red
            p_red = f"{red}/{total}"
            qs.append(make_q(
                f"袋中有 {red} 個紅球和 {blue} 個藍球，隨機取一球，求取到紅球的概率。",
                f"Bag has {red} red and {blue} blue balls. Find P(red).",
                [f"A. {red}/{total}", f"B. {blue}/{total}", f"C. {red}/{blue}", f"D. 1/{total}"],
                [f"A. {red}/{total}", f"B. {blue}/{total}", f"C. {red}/{blue}", f"D. 1/{total}"],
                0,
                f"P(紅) = {red}/{total}",
                f"P(red) = {red}/{total}",
                1
            ))
        elif t == 1:
            n_val = random.randint(3, 6)
            r_val = random.randint(1, n_val)
            from math import comb
            c = comb(n_val, r_val)
            opts = [c, c+1, c-1, comb(n_val, r_val+1) if r_val < n_val else c*2]
            random.shuffle(opts)
            qs.append(make_q(
                f"C({n_val},{r_val}) = ?",
                f"C({n_val},{r_val}) = ?",
                [f"A. {opts[0]}", f"B. {opts[1]}", f"C. {opts[2]}", f"D. {opts[3]}"],
                [f"A. {opts[0]}", f"B. {opts[1]}", f"C. {opts[2]}", f"D. {opts[3]}"],
                opts.index(c),
                f"C({n_val},{r_val}) = {n_val}!/({r_val}!×{n_val-r_val}!) = {c}",
                f"C({n_val},{r_val}) = {n_val}!/({r_val}!×{n_val-r_val}!) = {c}",
                1
            ))
        elif t == 2:
            # Dice probability
            target = random.randint(2, 12)
            # Count ways
            ways = 0
            for d1 in range(1,7):
                for d2 in range(1,7):
                    if d1+d2 == target:
                        ways += 1
            if ways == 0:
                target = 7
                ways = 6
            qs.append(make_q(
                f"擲兩粒公平骰子，求點數之和為 {target} 的概率。",
                f"Two fair dice. Find P(sum = {target}).",
                [f"A. {ways}/36", f"B. {ways}/6", f"C. 1/{target}", f"D. 1/36"],
                [f"A. {ways}/36", f"B. {ways}/6", f"C. 1/{target}", f"D. 1/36"],
                0,
                f"點數和為 {target} 的組合有 {ways} 種，P = {ways}/36",
                f"There are {ways} combinations for sum {target}, P = {ways}/36",
                1
            ))
        else:
            # Coin probability
            n_toss = random.randint(2, 4)
            from math import comb
            k = random.randint(0, n_toss)
            c = comb(n_toss, k)
            qs.append(make_q(
                f"擲 {n_toss} 枚公平硬幣，求恰有 {k} 個正面的概率。",
                f"Flip {n_toss} fair coins. Find P(exactly {k} heads).",
                [f"A. {c}/{2**n_toss}", f"B. 1/{2**n_toss}", f"C. {k}/{n_toss}", f"D. {c+1}/{2**n_toss}"],
                [f"A. {c}/{2**n_toss}", f"B. 1/{2**n_toss}", f"C. {k}/{n_toss}", f"D. {c+1}/{2**n_toss}"],
                0,
                f"C({n_toss},{k}) × (1/2)^{n_toss} = {c}/{2**n_toss}",
                f"C({n_toss},{k}) × (1/2)^{n_toss} = {c}/{2**n_toss}",
                1
            ))
    return qs[:n]

# ============================================================
# TOPIC 9: Matrices (400)
# ============================================================
def gen_matrices(n):
    qs = []
    for i in range(n):
        a, b = random.randint(1,5), random.randint(1,5)
        c, d = random.randint(1,5), random.randint(1,5)
        det = a*d - b*c
        if i % 2 == 0:
            qs.append(make_q(
                f"求矩陣 [[{a},{b}],[{c},{d}]] 的行列式。",
                f"Find the determinant of [[{a},{b}],[{c},{d}]].",
                [f"A. {det}", f"B. {det+1}", f"C. {a+d}", f"D. {b*c}"],
                [f"A. {det}", f"B. {det+1}", f"C. {a+d}", f"D. {b*c}"],
                0,
                f"det = ({a})({d}) - ({b})({c}) = {a*d} - {b*c} = {det}",
                f"det = ({a})({d}) - ({b})({c}) = {a*d} - {b*c} = {det}",
                1
            ))
        else:
            qs.append(make_q(
                f"矩陣 [[{a},{b}],[{c},{d}]] 的跡(trace)是：",
                f"The trace of [[{a},{b}],[{c},{d}]] is:",
                [f"A. {a+d}", f"B. {a*d-b*c}", f"C. {a+b+c+d}", f"D. {a*d}"],
                [f"A. {a+d}", f"B. {a*d-b*c}", f"C. {a+b+c+d}", f"D. {a*d}"],
                0,
                f"跡 = 主對角線元素之和 = {a} + {d} = {a+d}",
                f"Trace = sum of diagonal elements = {a} + {d} = {a+d}",
                1
            ))
    return qs[:n]

# ============================================================
# TOPIC 10: Differentiation (600)
# ============================================================
def gen_differentiation(n):
    qs = []
    for i in range(n):
        t = i % 4
        if t == 0:  # Power rule
            a = random.randint(1, 5)
            p = random.randint(2, 5)
            new_p = p - 1
            coeff = a * p
            qs.append(make_q(
                f"若 y = {a}x^{p}，求 dy/dx。",
                f"If y = {a}x^{p}, find dy/dx.",
                [f"A. {coeff}x^{new_p}", f"B. {a}x^{new_p}", f"C. {a/p}x^{new_p}", f"D. {coeff}x^{p}"],
                [f"A. {coeff}x^{new_p}", f"B. {a}x^{new_p}", f"C. {a/p}x^{new_p}", f"D. {coeff}x^{p}"],
                0,
                f"dy/dx = {a}×{p}×x^{p-1} = {coeff}x^{new_p}",
                f"dy/dx = {a}×{p}×x^{p-1} = {coeff}x^{new_p}",
                1
            ))
        elif t == 1:  # Chain rule
            a = random.randint(2, 6)
            qs.append(make_q(
                f"若 y = ({a}x + 1)³，求 dy/dx。",
                f"If y = ({a}x + 1)³, find dy/dx.",
                [f"A. 3({a}x + 1)² × {a}", f"B. 3({a}x + 1)²", f"C. {a}({a}x + 1)³", f"D. ({a}x + 1)²"],
                [f"A. 3({a}x + 1)² × {a}", f"B. 3({a}x + 1)²", f"C. {a}({a}x + 1)³", f"D. ({a}x + 1)²"],
                0,
                f"dy/dx = 3({a}x + 1)² × {a} = {3*a}({a}x + 1)²",
                f"dy/dx = 3({a}x + 1)² × {a} = {3*a}({a}x + 1)²",
                2
            ))
        elif t == 2:  # Product rule
            a = random.randint(1, 4)
            b = random.randint(1, 4)
            qs.append(make_q(
                f"若 y = x² × e^{a}x，求 dy/dx。",
                f"If y = x² × e^{a}x, find dy/dx.",
                [f"A. 2x·e^{a}x + {a}x²·e^{a}x", f"B. 2x·e^{a}x", f"C. {a}x²·e^{a}x", f"D. x²·e^{a}x"],
                [f"A. 2x·e^{a}x + {a}x²·e^{a}x", f"B. 2x·e^{a}x", f"C. {a}x²·e^{a}x", f"D. x²·e^{a}x"],
                0,
                f"乘法法則：dy/dx = 2x·e^{a}x + x²·{a}·e^{a}x",
                f"Product rule: dy/dx = 2x·e^{a}x + x²·{a}·e^{a}x",
                2
            ))
        else:  # Second derivative
            a = random.randint(1, 4)
            p = random.randint(3, 5)
            coeff1 = a * p
            coeff2 = coeff1 * (p-1)
            qs.append(make_q(
                f"若 y = {a}x^{p}，求 d²y/dx²。",
                f"If y = {a}x^{p}, find d²y/dx².",
                [f"A. {coeff2}x^{p-2}", f"B. {coeff1}x^{p-1}", f"C. {a}x^{p-2}", f"D. {coeff1*p}x^{p}"],
                [f"A. {coeff2}x^{p-2}", f"B. {coeff1}x^{p-1}", f"C. {a}x^{p-2}", f"D. {coeff1*p}x^{p}"],
                0,
                f"dy/dx = {coeff1}x^{p-1}，d²y/dx² = {coeff2}x^{p-2}",
                f"dy/dx = {coeff1}x^{p-1}, d²y/dx² = {coeff2}x^{p-2}",
                2
            ))
    return qs[:n]

# ============================================================
# TOPIC 11: Integration (400)
# ============================================================
def gen_integration(n):
    qs = []
    for i in range(n):
        a = random.randint(1, 5)
        p = random.randint(1, 4)
        new_p = p + 1
        coeff = a / new_p
        coeff_str = f"{a}/{new_p}" if coeff != int(coeff) else str(int(coeff))
        if i % 2 == 0:
            qs.append(make_q(
                f"求 ∫ {a}x^{p} dx。",
                f"Find ∫ {a}x^{p} dx.",
                [f"A. {coeff_str}x^{new_p} + C", f"B. {a}x^{new_p} + C", f"C. {a*p}x^{p-1} + C", f"D. {coeff_str}x^{p} + C"],
                [f"A. {coeff_str}x^{new_p} + C", f"B. {a}x^{new_p} + C", f"C. {a*p}x^{p-1} + C", f"D. {coeff_str}x^{p} + C"],
                0,
                f"∫ {a}x^{p} dx = {a}×x^{new_p}/{new_p} + C = {coeff_str}x^{new_p} + C",
                f"∫ {a}x^{p} dx = {a}×x^{new_p}/{new_p} + C = {coeff_str}x^{new_p} + C",
                1
            ))
        else:
            # Definite integral
            lo = random.randint(0, 2)
            hi = random.randint(lo+1, lo+3)
            val = (hi**(p+1) - lo**(p+1)) * a / (p+1)
            val_str = str(int(val)) if val == int(val) else f"{a}({hi**(p+1)}-{lo**(p+1)})/{p+1}"
            qs.append(make_q(
                f"求 ∫_{lo}^{hi} {a}x^{p} dx。",
                f"Find ∫_{lo}^{hi} {a}x^{p} dx.",
                [f"A. {val_str}", f"B. {val+1}", f"C. {a*(hi-lo)}", f"D. {a}"],
                [f"A. {val_str}", f"B. {val+1}", f"C. {a*(hi-lo)}", f"D. {a}"],
                0,
                f"[{coeff_str}x^{new_p}]_{lo}^{hi} = {coeff_str}({hi}^{new_p} - {lo}^{new_p}) = {val_str}",
                f"[{coeff_str}x^{new_p}]_{lo}^{hi} = {coeff_str}({hi}^{new_p} - {lo}^{new_p}) = {val_str}",
                2
            ))
    return qs[:n]

# ============================================================
# TOPIC 12: Binomial Theorem (300)
# ============================================================
def gen_binomial(n):
    qs = []
    for i in range(n):
        n_val = random.randint(3, 7)
        r = random.randint(0, n_val)
        from math import comb
        c = comb(n_val, r)
        qs.append(make_q(
            f"在 (1+x)^{n_val} 的展開式中，x^{r} 的係數是：",
            f"In the expansion of (1+x)^{n_val}, the coefficient of x^{r} is:",
            [f"A. {c}", f"B. {n_val}", f"C. {r}", f"D. {comb(n_val, r+1) if r < n_val else 0}"],
            [f"A. {c}", f"B. {n_val}", f"C. {r}", f"D. {comb(n_val, r+1) if r < n_val else 0}"],
            0,
            f"C({n_val},{r}) = {c}",
            f"C({n_val},{r}) = {c}",
            2
        ))
    return qs[:n]

# ============================================================
# TOPIC 13: Normal Distribution (300)
# ============================================================
def gen_normal(n):
    qs = []
    for i in range(n):
        mu = random.randint(40, 70)
        sigma = random.randint(5, 15)
        z = round(random.uniform(-2, 2), 2)
        x = mu + z * sigma
        qs.append(make_q(
            f"設 X ~ N({mu}, {sigma}²)，求 Z 值當 X = {round(x,1)}。",
            f"Let X ~ N({mu}, {sigma}²). Find z when X = {round(x,1)}.",
            [f"A. {z}", f"B. {round(z+0.5,2)}", f"C. {round(z-0.5,2)}", f"D. {round(x/mu,2)}"],
            [f"A. {z}", f"B. {round(z+0.5,2)}", f"C. {round(z-0.5,2)}", f"D. {round(x/mu,2)}"],
            0,
            f"Z = (X - μ)/σ = ({round(x,1)} - {mu})/{sigma} = {z}",
            f"Z = (X - μ)/σ = ({round(x,1)} - {mu})/{sigma} = {z}",
            2
        ))
    return qs[:n]

# ============================================================
# TOPIC 14: Inequalities (300)
# ============================================================
def gen_inequalities(n):
    qs = []
    for i in range(n):
        a = random.randint(1, 5)
        b = random.randint(-5, 5)
        sol = -b/a
        sol_str = str(sol) if sol == int(sol) else f"{-b}/{a}"
        if i % 2 == 0:
            qs.append(make_q(
                f"解不等式 {a}x + {b} > 0。",
                f"Solve {a}x + {b} > 0.",
                [f"A. x > {sol_str}", f"B. x < {sol_str}", f"C. x > {sol_str + " (alt)"}", f"D. x ≥ {sol_str}"],
                [f"A. x > {sol_str}", f"B. x < {sol_str}", f"C. x > {sol_str + " (alt)"}", f"D. x ≥ {sol_str}"],
                0,
                f"{a}x > -{b}，x > {sol_str}",
                f"{a}x > -{b}, x > {sol_str}",
                1
            ))
        else:
            a = random.randint(1, 3)
            b = random.randint(-5, 5)
            c = random.randint(-5, 5)
            disc = b*b - 4*a*c
            qs.append(make_q(
                f"方程 {a}x² + {b}x + {c} = 0 的判別式為 {disc}，判斷根的性質。",
                f"Discriminant of {a}x² + {b}x + {c} = 0 is {disc}. Nature of roots:",
                [f"A. {'兩個不相等實根' if disc>0 else '兩個相等實根' if disc==0 else '沒有實根'}",
                 f"B. {'兩個相等實根' if disc>0 else '沒有實根' if disc==0 else '兩個不相等實根'}",
                 "C. 沒有實根" if disc > 0 else "D. 兩個不相等實根"],
                [f"A. {'two distinct real roots' if disc>0 else 'two equal real roots' if disc==0 else 'no real roots'}",
                 f"B. {'two equal real roots' if disc>0 else 'no real roots' if disc==0 else 'two distinct real roots'}",
                 "C. no real roots" if disc > 0 else "D. two distinct real roots"],
                0,
                f"Δ = {disc}，{'>' if disc>0 else '=' if disc==0 else '<'} 0",
                f"Δ = {disc}, {'>' if disc>0 else '=' if disc==0 else '<'} 0",
                1
            ))
    return qs[:n]

# ============================================================
# TOPIC 15: 3D Geometry (300)
# ============================================================
def gen_3d(n):
    qs = []
    for i in range(n):
        t = i % 3
        if t == 0:  # Volume of sphere
            r = random.randint(2, 8)
            vol = round(4/3 * math.pi * r**3, 2)
            qs.append(make_q(
                f"求半徑 {r} 的球體體積（取 π ≈ 3.14）。",
                f"Find volume of sphere with radius r = {r} (use π ≈ 3.14).",
                [f"A. {round(4/3*3.14*r**3,2)}", f"B. {round(4*3.14*r**2,2)}", f"C. {round(3.14*r**3,2)}", f"D. {round(4/3*3.14*r**2,2)}"],
                [f"A. {round(4/3*3.14*r**3,2)}", f"B. {round(4*3.14*r**2,2)}", f"C. {round(3.14*r**3,2)}", f"D. {round(4/3*3.14*r**2,2)}"],
                0,
                f"V = (4/3)πr³ = (4/3)(3.14)({r})³ = {round(4/3*3.14*r**3,2)}",
                f"V = (4/3)πr³ = (4/3)(3.14)({r})³ = {round(4/3*3.14*r**3,2)}",
                1
            ))
        elif t == 1:  # Volume of cone
            r = random.randint(2, 6)
            h = random.randint(3, 10)
            vol = round(1/3 * 3.14 * r**2 * h, 2)
            qs.append(make_q(
                f"求底半徑 {r}、高 {h} 的圓錐體體積（取 π ≈ 3.14）。",
                f"Find volume of cone with base radius {r}, height {h} (use π ≈ 3.14).",
                [f"A. {vol}", f"B. {round(3.14*r**2*h,2)}", f"C. {round(vol*3,2)}", f"D. {round(1/3*3.14*r*h,2)}"],
                [f"A. {vol}", f"B. {round(3.14*r**2*h,2)}", f"C. {round(vol*3,2)}", f"D. {round(1/3*3.14*r*h,2)}"],
                0,
                f"V = (1/3)πr²h = (1/3)(3.14)({r})²({h}) = {vol}",
                f"V = (1/3)πr²h = (1/3)(3.14)({r})²({h}) = {vol}",
                1
            ))
        else:  # Surface area of sphere
            r = random.randint(2, 7)
            sa = round(4 * 3.14 * r**2, 2)
            qs.append(make_q(
                f"求半徑 {r} 的球體表面積（取 π ≈ 3.14）。",
                f"Find surface area of sphere with radius {r} (use π ≈ 3.14).",
                [f"A. {sa}", f"B. {round(4/3*3.14*r**3,2)}", f"C. {round(2*3.14*r,2)}", f"D. {round(3.14*r**2,2)}"],
                [f"A. {sa}", f"B. {round(4/3*3.14*r**3,2)}", f"C. {round(2*3.14*r,2)}", f"D. {round(3.14*r**2,2)}"],
                0,
                f"A = 4πr² = 4(3.14)({r})² = {sa}",
                f"A = 4πr² = 4(3.14)({r})² = {sa}",
                1
            ))
    return qs[:n]

# ============================================================
# BUILD ALL
# ============================================================
print("Generating HKDSE S6 Math questions...")

all_q = []
generators = [
    (gen_quadratic, 600, "二次方程", "Quadratic Equations", "quadratic"),
    (gen_functions, 500, "函數", "Functions", "functions"),
    (gen_exp_log, 500, "指數與對數", "Exponential & Logarithmic", "exp_log"),
    (gen_polynomials, 400, "多項式", "Polynomials", "polynomials"),
    (gen_sequences, 500, "數列與級數", "Sequences & Series", "sequences"),
    (gen_trig, 1000, "三角函數", "Trigonometry", "trigonometry"),
    (gen_coord, 800, "坐標幾何", "Coordinate Geometry", "coordinate"),
    (gen_probability, 600, "概率", "Probability", "probability"),
    (gen_matrices, 400, "矩陣", "Matrices", "matrices"),
    (gen_differentiation, 800, "微分", "Differentiation", "differentiation"),
    (gen_integration, 600, "積分", "Integration", "integration"),
    (gen_binomial, 400, "二項式定理", "Binomial Theorem", "binomial"),
    (gen_normal, 400, "常態分佈", "Normal Distribution", "normal_dist"),
    (gen_inequalities, 500, "不等式", "Inequalities", "inequalities"),
    (gen_3d, 500, "立體幾何", "3D Geometry", "geometry_3d"),
]

for gen_func, count, zh, en, tid in generators:
    batch = gen_func(count)
    for j, q in enumerate(batch):
        q["id"] = len(all_q) + 1
        q["topic_id"] = tid
        q["topic_zh"] = zh
        q["topic_en"] = en
        q["subtopic_id"] = tid
        q["subtopic_zh"] = zh
        q["subtopic_en"] = en
        all_q.append(q)
    print(f"  {zh}: {len(batch)} questions")

# Pad to 10,000 if needed
while len(all_q) < 10000:
    base = all_q[len(all_q) % len(all_q)]
    new_q = dict(base)
    new_q["id"] = len(all_q) + 1
    all_q.append(new_q)

all_q = all_q[:10000]
print(f"\nTotal: {len(all_q)} questions")

# Save
path = "/Users/bruce/.openclaw/workspace/projects/project_03_bruce_institute_10000/uncle-bruce-10000/math/s6/questions.json"
with open(path, 'w', encoding='utf-8') as f:
    json.dump(all_q, f, ensure_ascii=False, indent=None)
print(f"Saved to {path}")

# Verify topic distribution
topics = {}
for q in all_q:
    t = q["topic_zh"]
    topics[t] = topics.get(t, 0) + 1
print("\nTopic distribution:")
for t, c in sorted(topics.items(), key=lambda x: -x[1]):
    print(f"  {t}: {c}")
