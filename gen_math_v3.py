#!/usr/bin/env python3
"""
Math Question Generator v3
- Much more template diversity per subtopic
- Round-robin shuffling (no consecutive same topic)
- Real-world HK contexts
- Proper deduplication
"""
import json, random, os, math

random.seed(42)

# ============================================================
# TEMPLATE DEFINITIONS - Many more per subtopic
# ============================================================

def gen_directed_number_bodmas(n):
    """四則混合運算 - many diverse templates"""
    qs = []
    templates = [
        # Basic arithmetic with signs
        lambda: (f"計算 {a} × {b} + {c}", f"Calculate {a} × {b} + {c}", a*b+c,
                 [a*b+c+1, a*b+c-1, a*b-c, -(a*b+c)])
        for a in [random.randint(-12,12) or 1 for _ in range(1)]
        for b in [random.randint(-12,12) or 1 for _ in range(1)]
        for c in [random.randint(-20,20) for _ in range(1)]
    ]
    # Generate with actual random values each time
    for _ in range(n):
        t = random.randint(0, 7)
        if t == 0:
            a, b, c = random.randint(-15,15) or 1, random.randint(-15,15) or 1, random.randint(-30,30)
            ans = a*b+c
            q_zh, q_en = f"計算 {a} × {b} + {c}", f"Calculate {a} × {b} + {c}"
            opts = [ans, ans+1, ans-1, a*b-c]
        elif t == 1:
            a, b, c = random.randint(-15,15) or 1, random.randint(-15,15) or 1, random.randint(-30,30)
            ans = a+b*c
            q_zh, q_en = f"計算 {a} + {b} × {c}", f"Calculate {a} + {b} × {c}"
            opts = [ans, ans+1, ans-1, (a+b)*c]
        elif t == 2:
            a, b = random.randint(-20,20) or 1, random.randint(-20,20) or 1
            ans = a*b
            q_zh, q_en = f"計算 ({a}) × ({b})", f"Calculate ({a}) × ({b})"
            opts = [ans, ans+1, -ans, ans+random.choice([2,3,5])]
        elif t == 3:
            # Division with clean result
            b = random.randint(2,8)
            ans_val = random.randint(-10,10)
            a = ans_val * b
            c = random.randint(-15,15)
            ans = ans_val + c
            q_zh, q_en = f"計算 {a} ÷ {b} + {c}", f"Calculate {a} ÷ {b} + {c}"
            opts = [ans, ans+1, ans-1, ans_val-c]
        elif t == 4:
            # Mixed with parentheses
            a, b, c = random.randint(-10,10) or 1, random.randint(-10,10) or 1, random.randint(-10,10) or 1
            ans = (a+b)*c
            q_zh, q_en = f"計算 ({a} + {b}) × {c}", f"Calculate ({a} + {b}) × {c}"
            opts = [ans, ans+1, ans-1, a+b*c]
        elif t == 5:
            # Word problem style
            a, b = random.randint(-20,-1), random.randint(2,10)
            ans = a * b
            q_zh = f"溫度每小時下降 {abs(a)} 度，{b} 小時後溫度變化了多少？"
            q_en = f"Temperature drops {abs(a)}°/h. Change after {b}h?"
            opts = [ans, -ans, ans+1, ans-1]
        elif t == 6:
            # Multi-step
            a, b, c, d = [random.randint(-8,8) or 1 for _ in range(4)]
            ans = a*b + c*d
            q_zh, q_en = f"計算 {a}×{b} + {c}×{d}", f"Calculate {a}×{b} + {c}×{d}"
            opts = [ans, ans+1, ans-1, a*b-c*d]
        else:
            # Nested parentheses
            a, b, c = random.randint(-8,8) or 1, random.randint(-8,8) or 1, random.randint(-8,8) or 1
            ans = (a + b*c)
            q_zh, q_en = f"計算 {a} + ({b} × {c})", f"Calculate {a} + ({b} × {c})"
            opts = [ans, ans+1, ans-1, (a+b)*c]
        qs.append((q_zh, q_en, ans, opts))
    return qs

def gen_directed_number_fractions(n):
    """分數運算"""
    qs = []
    for _ in range(n):
        t = random.randint(0, 5)
        if t == 0:  # Addition
            a,b = random.randint(1,10), random.randint(2,12)
            c,d = random.randint(1,10), random.randint(2,12)
            num, den = a*d+b*c, b*d
            g = math.gcd(abs(num),abs(den))
            ans = f"{num//g}/{den//g}"
            q_zh = f"計算 {a}/{b} + {c}/{d}"
            q_en = f"Calculate {a}/{b} + {c}/{d}"
            opts = [ans, f"{num+1}/{den}", f"{a+c}/{b+d}", f"{num-1}/{den}"]
        elif t == 1:  # Subtraction
            a,b = random.randint(1,10), random.randint(2,12)
            c,d = random.randint(1,10), random.randint(2,12)
            num, den = a*d-b*c, b*d
            g = math.gcd(abs(num),abs(den))
            ans = f"{num//g}/{den//g}"
            q_zh = f"計算 {a}/{b} - {c}/{d}"
            q_en = f"Calculate {a}/{b} - {c}/{d}"
            opts = [ans, f"{abs(num)+1}/{den}", f"{a-c}/{b}", f"{num//g+1}/{den//g}"]
        elif t == 2:  # Multiplication
            a,b = random.randint(1,10), random.randint(2,10)
            c,d = random.randint(1,10), random.randint(2,10)
            num, den = a*c, b*d
            g = math.gcd(abs(num),abs(den))
            ans = f"{num//g}/{den//g}"
            q_zh = f"計算 {a}/{b} × {c}/{d}"
            q_en = f"Calculate {a}/{b} × {c}/{d}"
            opts = [ans, f"{a+b}/{c+d}", f"{num+1}/{den}", f"{a*d}/{b*c}"]
        elif t == 3:  # Division
            a,b = random.randint(1,10), random.randint(2,10)
            c,d = random.randint(1,10), random.randint(2,10)
            num, den = a*d, b*c
            g = math.gcd(abs(num),abs(den))
            ans = f"{num//g}/{den//g}"
            q_zh = f"計算 {a}/{b} ÷ {c}/{d}"
            q_en = f"Calculate {a}/{b} ÷ {c}/{d}"
            opts = [ans, f"{a*c}/{b*d}", f"{num+1}/{den}", f"{a}/{b}"]
        elif t == 4:  # Compare
            a,b = random.randint(1,10), random.randint(2,12)
            c,d = random.randint(1,10), random.randint(2,12)
            left, right = a*d, b*c
            if left > right:
                ans_str = f"{a}/{b} > {c}/{d}"
            elif left < right:
                ans_str = f"{a}/{b} < {c}/{d}"
            else:
                ans_str = f"{a}/{b} = {c}/{d}"
            q_zh = f"比較 {a}/{b} 和 {c}/{d} 的大小"
            q_en = f"Compare {a}/{b} and {c}/{d}"
            opts = [ans_str, f"{a}/{b} > {c}/{d}" if left <= right else f"{a}/{b} < {c}/{d}",
                    f"{a}/{b} = {c}/{d}" if left != right else f"{a}/{b} > {c}/{d}", "無法比較"]
            ans = 0
        else:  # Mixed number word problem
            a,b = random.randint(1,5), random.randint(2,8)
            c = random.randint(1,3)
            whole = a * b + c
            q_zh = f"一個蛋糕分成 {b} 份，小明食咗 {a} 個蛋糕加 {c} 份，佢食咗幾多份？"
            q_en = f"A cake is cut into {b} pieces. Ming ate {a} cakes and {c} pieces. How many pieces total?"
            ans = whole
            opts = [whole, whole+1, whole-1, a+c]
        if t != 4:
            q_zh = q_zh
        qs.append((q_zh, q_en, ans, opts))
    return qs

def gen_directed_number_hcf_lcm(n):
    """公因數與公倍數"""
    qs = []
    for _ in range(n):
        a, b = random.randint(2,60), random.randint(2,60)
        g = math.gcd(a,b)
        lcm = a*b//g
        t = random.randint(0,1)
        if t == 0:
            q_zh = f"求 {a} 和 {b} 的最大公因數"
            q_en = f"Find the GCF of {a} and {b}"
            ans = g
            opts = [g, lcm, a, b]
        else:
            q_zh = f"求 {a} 和 {b} 的最小公倍數"
            q_en = f"Find the LCM of {a} and {b}"
            ans = lcm
            opts = [lcm, g, a*b, max(a,b)]
        qs.append((q_zh, q_en, ans, opts))
    return qs

def gen_directed_number_absolute(n):
    """絕對值"""
    qs = []
    for _ in range(n):
        t = random.randint(0,2)
        if t == 0:
            a = random.randint(-50,50)
            ans = abs(a)
            q_zh = f"計算 |{a}|"
            q_en = f"Calculate |{a}|"
            opts = [ans, -ans, ans+1, a]
        elif t == 1:
            a, b = random.randint(-20,20), random.randint(-20,20)
            ans = abs(a) + abs(b)
            q_zh = f"計算 |{a}| + |{b}|"
            q_en = f"Calculate |{a}| + |{b}|"
            opts = [ans, abs(a+b), abs(a-b), ans+1]
        else:
            a, b = random.randint(-15,15), random.randint(-15,15)
            ans = abs(a - b)
            q_zh = f"計算 |{a} - {b}|"
            q_en = f"Calculate |{a} - {b}|"
            opts = [ans, abs(a)+abs(b), abs(a*b), ans+1]
        qs.append((q_zh, q_en, ans, opts))
    return qs

def gen_directed_number_powers(n):
    """冪次"""
    qs = []
    for _ in range(n):
        t = random.randint(0,5)
        if t == 0:
            a = random.randint(2,10)
            p = random.choice([2,3])
            ans = a**p
            q_zh = f"計算 {a}{'²' if p==2 else '³'}"
            q_en = f"Calculate {a}{'²' if p==2 else '³'}"
            opts = [ans, a*p, ans+a, ans-a]
        elif t == 1:
            a = random.randint(2,5)
            p, q_val = random.randint(2,4), random.randint(2,4)
            ans = a**(p+q_val)
            q_zh = f"計算 {a}^{p} × {a}^{q_val}"
            q_en = f"Calculate {a}^{p} × {a}^{q_val}"
            opts = [ans, a**(p*q_val), a**p+a**q_val, ans+1]
        elif t == 2:
            base = random.choice([2,3,5,10])
            exp = random.randint(2,5)
            ans = base**exp
            q_zh = f"計算 {base}^{exp}"
            q_en = f"Calculate {base}^{exp}"
            opts = [ans, base*exp, base**(exp-1), base**(exp+1)]
        elif t == 3:
            # Square roots
            base = random.randint(2,15)
            ans = base**2
            q_zh = f"計算 √{ans}"
            q_en = f"Calculate √{ans}"
            opts = [base, base+1, base-1, base*2]
        elif t == 4:
            # Cube roots
            base = random.randint(2,8)
            ans = base**3
            q_zh = f"計算 ³√{ans}"
            q_en = f"Calculate ³√{ans}"
            opts = [base, base+1, base-1, base*3]
        else:
            # a^n / a^m
            a = random.randint(2,5)
            n_val = random.randint(3,6)
            m_val = random.randint(1, n_val-1)
            ans = a**(n_val-m_val)
            q_zh = f"計算 {a}^{n_val} ÷ {a}^{m_val}"
            q_en = f"Calculate {a}^{n_val} ÷ {a}^{m_val}"
            opts = [ans, a**(n_val+m_val), a**n_val-a**m_val, ans+1]
        qs.append((q_zh, q_en, ans, opts))
    return qs

def gen_statistics_mean(n):
    """平均數"""
    qs = []
    for _ in range(n):
        t = random.randint(0,3)
        if t == 0:
            nums = [random.randint(10,99) for _ in range(random.randint(4,8))]
            avg = round(sum(nums)/len(nums),1)
            q_zh = f"求 {', '.join(map(str,nums))} 的平均數"
            q_en = f"Find the mean of {', '.join(map(str,nums))}"
            opts = [avg, sum(nums), min(nums), max(nums)]
        elif t == 1:
            # Word problem
            scores = [random.randint(40,100) for _ in range(5)]
            avg = round(sum(scores)/len(scores),1)
            q_zh = f"小明5次考試分別攞咗 {', '.join(map(str,scores))} 分，求平均分"
            q_en = f"Ming scored {', '.join(map(str,scores))} in 5 tests. Find the mean."
            opts = [avg, max(scores), min(scores), sum(scores)]
        elif t == 2:
            # With missing value
            nums = [random.randint(10,90) for _ in range(4)]
            target_avg = random.randint(40,70)
            missing = target_avg * 5 - sum(nums)
            q_zh = f"5個數嘅平均數係 {target_avg}，其中4個係 {', '.join(map(str,nums))}，求第5個數"
            q_en = f"Mean of 5 numbers is {target_avg}. Four are {', '.join(map(str,nums))}. Find the 5th."
            ans = missing
            opts = [missing, missing+1, missing-1, target_avg]
        else:
            # Weighted context
            a, b, c = random.randint(50,100), random.randint(50,100), random.randint(50,100)
            avg = round((a+b+c)/3,1)
            q_zh = f"中文 {a} 分、英文 {b} 分、數學 {c} 分，求三科平均分"
            q_en = f"Chinese {a}, English {b}, Math {c}. Find the average."
            opts = [avg, a+b+c, max(a,b,c), min(a,b,c)]
        qs.append((q_zh, q_en, avg if t!=2 else ans, opts))
    return qs

def gen_statistics_median(n):
    """中位數"""
    qs = []
    for _ in range(n):
        size = random.choice([5,7,9])
        nums = sorted(random.sample(range(10,100), size))
        median = nums[size//2]
        q_zh = f"求 {', '.join(map(str,nums))} 的中位數"
        q_en = f"Find the median of {', '.join(map(str,nums))}"
        avg = round(sum(nums)/len(nums),1)
        opts = [median, avg, nums[0], nums[-1]]
        qs.append((q_zh, q_en, median, opts))
    return qs

def gen_statistics_mode(n):
    """眾數"""
    qs = []
    for _ in range(n):
        mode_val = random.randint(10,90)
        others = [random.randint(10,90) for _ in range(random.randint(3,6))]
        nums = others + [mode_val]*random.randint(2,4)
        random.shuffle(nums)
        from collections import Counter
        actual_mode = Counter(nums).most_common(1)[0][0]
        q_zh = f"求 {', '.join(map(str,nums))} 的眾數"
        q_en = f"Find the mode of {', '.join(map(str,nums))}"
        avg = round(sum(nums)/len(nums),1)
        opts = [actual_mode, avg, min(nums), max(nums)]
        qs.append((q_zh, q_en, actual_mode, opts))
    return qs

def gen_statistics_probability(n):
    """概率"""
    qs = []
    for _ in range(n):
        t = random.randint(0,2)
        if t == 0:
            total = random.randint(5,20)
            red = random.randint(1, total-1)
            g = math.gcd(red, total)
            ans = f"{red//g}/{total//g}"
            q_zh = f"袋中有 {total} 個球，其中 {red} 個紅色，求抽到紅球的概率"
            q_en = f"Bag has {total} balls, {red} red. Find P(red)."
            opts = [ans, f"{total-red}/{total}", f"1/{total}", f"{red}/{total+1}"]
        elif t == 1:
            total = random.randint(10,30)
            blue = random.randint(2, total-2)
            red = total - blue
            g = math.gcd(blue, total)
            ans = f"{blue//g}/{total//g}"
            q_zh = f"袋中有 {total} 個球，{red} 紅 {blue} 藍，求抽到藍球的概率"
            q_en = f"Bag: {total} balls ({red} red, {blue} blue). P(blue)?"
            opts = [ans, f"{red}/{total}", f"1/{blue}", f"{blue}/{total+1}"]
        else:
            die = random.randint(1,6)
            q_zh = f"擲一粒公正骰子，求擲到 {die} 的概率"
            q_en = f"Fair die. P(rolling {die})?"
            ans = "1/6"
            opts = ["1/6", f"{die}/6", "1/3", "1/2"]
        qs.append((q_zh, q_en, ans, opts))
    return qs

def gen_basic_algebra_linear_eq(n):
    """一元一次方程"""
    qs = []
    for _ in range(n):
        t = random.randint(0,3)
        if t == 0:
            a = random.randint(2,10)
            x = random.randint(1,15)
            b = random.randint(1,30)
            rhs = a*x + b
            q_zh = f"解方程 {a}x + {b} = {rhs}"
            q_en = f"Solve {a}x + {b} = {rhs}"
            ans = x
            opts = [x, x+1, x-1, (rhs+b)//a]
        elif t == 1:
            a = random.randint(2,8)
            x = random.randint(1,12)
            b = random.randint(1,20)
            rhs = a*x - b
            q_zh = f"解方程 {a}x - {b} = {rhs}"
            q_en = f"Solve {a}x - {b} = {rhs}"
            ans = x
            opts = [x, x+1, x-1, (rhs-b)//a]
        elif t == 2:
            # Word problem
            a = random.randint(3,8)
            x = random.randint(2,10)
            total = a * x
            q_zh = f"小明買咗 {a} 個蘋果，一共使咗 ${total}，每個蘋果幾錢？"
            q_en = f"Ming bought {a} apples for ${total}. Price per apple?"
            ans = x
            opts = [x, x+1, x-1, total+a]
        else:
            # Two-step equation
            a = random.randint(2,6)
            b = random.randint(1,15)
            x = random.randint(1,10)
            rhs = a*(x+b)
            q_zh = f"解方程 {a}(x + {b}) = {rhs}"
            q_en = f"Solve {a}(x + {b}) = {rhs}"
            ans = x
            opts = [x, x+1, x-1, rhs//a]
        qs.append((q_zh, q_en, ans, opts))
    return qs

def gen_basic_algebra_simplify(n):
    """簡化代數式"""
    qs = []
    for _ in range(n):
        t = random.randint(0,2)
        if t == 0:
            a, b = random.randint(2,20), random.randint(2,20)
            ans = f"{a+b}x"
            q_zh = f"簡化 {a}x + {b}x"
            q_en = f"Simplify {a}x + {b}x"
            opts = [ans, f"{a-b}x", f"{a*b}x", f"{a+b}x²"]
        elif t == 1:
            a = random.randint(5,25)
            b = random.randint(2, max(2, a-1))
            ans = f"{a-b}x"
            q_zh = f"簡化 {a}x - {b}x"
            q_en = f"Simplify {a}x - {b}x"
            opts = [ans, f"{a+b}x", f"{a*b}x", f"{b-a}x"]
        else:
            a, b, c = random.randint(2,10), random.randint(2,10), random.randint(2,10)
            ans = f"{a+b-c}x"
            q_zh = f"簡化 {a}x + {b}x - {c}x"
            q_en = f"Simplify {a}x + {b}x - {c}x"
            opts = [ans, f"{a+b+c}x", f"{a-b+c}x", f"{a+b-c}x²"]
        qs.append((q_zh, q_en, ans, opts))
    return qs

def gen_basic_algebra_expand(n):
    """展開"""
    qs = []
    for _ in range(n):
        t = random.randint(0,3)
        if t == 0:
            a = random.randint(2,12)
            b = random.randint(-12,12)
            sign = "+" if b >= 0 else "-"
            ans = f"{a}x + {a*b}" if b >= 0 else f"{a}x - {abs(a*b)}"
            q_zh = f"展開 {a}(x {sign} {abs(b)})"
            q_en = f"Expand {a}(x {sign} {abs(b)})"
            opts = [ans, f"{a}x + {b}", f"x + {a*b}", f"{a}x {sign} {abs(b)}"]
        elif t == 1:
            # (x+a)(x+b)
            a, b = random.randint(1,10), random.randint(1,10)
            coeff = a+b
            const = a*b
            ans = f"x² + {coeff}x + {const}"
            q_zh = f"展開 (x + {a})(x + {b})"
            q_en = f"Expand (x + {a})(x + {b})"
            opts = [ans, f"x² + {const}x + {coeff}", f"x² + {coeff}x - {const}", f"x² - {coeff}x + {const}"]
        elif t == 2:
            # (x-a)(x+b)
            a, b = random.randint(1,8), random.randint(1,8)
            coeff = b - a
            const = -a*b
            sign_coeff = "+" if coeff >= 0 else "-"
            sign_const = "+" if const >= 0 else "-"
            ans = f"x² {sign_coeff} {abs(coeff)}x {sign_const} {abs(const)}"
            q_zh = f"展開 (x - {a})(x + {b})"
            q_en = f"Expand (x - {a})(x + {b})"
            opts = [ans, f"x² + {a+b}x + {a*b}", f"x² + {a+b}x - {a*b}", f"x² - {abs(coeff)}x - {abs(const)}"]
        else:
            # a(bx + c)
            a = random.randint(2,8)
            b = random.randint(2,6)
            c = random.randint(-10,10)
            ans_coeff = a*b
            ans_const = a*c
            sign = "+" if ans_const >= 0 else "-"
            ans = f"{ans_coeff}x {sign} {abs(ans_const)}"
            q_zh = f"展開 {a}({b}x {'+' if c>=0 else '-'} {abs(c)})"
            q_en = f"Expand {a}({b}x {'+' if c>=0 else '-'} {abs(c)})"
            opts = [ans, f"{a}x + {c}", f"{a*b}x + {c}", f"{a+b}x + {a*c}"]
        qs.append((q_zh, q_en, ans, opts))
    return qs

def gen_basic_algebra_substitution(n):
    """代入求值"""
    qs = []
    for _ in range(n):
        t = random.randint(0,2)
        x = random.randint(1,10)
        if t == 0:
            a, b = random.randint(2,8), random.randint(1,20)
            ans = a*x + b
            q_zh = f"若 x = {x}，求 {a}x + {b} 的值"
            q_en = f"If x = {x}, find {a}x + {b}"
            opts = [ans, ans+1, ans-1, a+b]
        elif t == 1:
            a = random.randint(2,5)
            ans = a*x**2
            q_zh = f"若 x = {x}，求 {a}x² 的值"
            q_en = f"If x = {x}, find {a}x²"
            opts = [ans, a*x, ans+a, ans-1]
        else:
            a, b, c = random.randint(1,5), random.randint(1,10), random.randint(1,20)
            ans = a*x**2 + b*x + c
            q_zh = f"若 x = {x}，求 {a}x² + {b}x + {c} 的值"
            q_en = f"If x = {x}, find {a}x² + {b}x + {c}"
            opts = [ans, ans+1, ans-1, a+b+c]
        qs.append((q_zh, q_en, ans, opts))
    return qs

def gen_basic_algebra_inequalities(n):
    """不等式"""
    qs = []
    for _ in range(n):
        a = random.randint(2,8)
        b = random.randint(1,20)
        x = random.randint(1,10)
        rhs = a*x + b
        op = random.choice([">", "<"])
        if op == ">":
            ans_str = f"x > {x}" if a > 0 else f"x < {x}"
            q_zh = f"解不等式 {a}x + {b} > {rhs}"
            q_en = f"Solve {a}x + {b} > {rhs}"
        else:
            ans_str = f"x < {x}" if a > 0 else f"x > {x}"
            q_zh = f"解不等式 {a}x + {b} < {rhs}"
            q_en = f"Solve {a}x + {b} < {rhs}"
        opts = [ans_str, f"x > {x+1}", f"x < {x-1}", f"x ≥ {x}"]
        qs.append((q_zh, q_en, ans_str, opts))
    return qs

def gen_coordinates_distance(n):
    """距離"""
    qs = []
    for _ in range(n):
        t = random.randint(0,1)
        if t == 0:
            # Same x or y
            if random.random() < 0.5:
                x = random.randint(-10,10)
                y1, y2 = sorted(random.sample(range(-10,11), 2))
                dist = abs(y2-y1)
                p1, p2 = f"({x},{y1})", f"({x},{y2})"
            else:
                y = random.randint(-10,10)
                x1, x2 = sorted(random.sample(range(-10,11), 2))
                dist = abs(x2-x1)
                p1, p2 = f"({x1},{y})", f"({x2},{y})"
            q_zh = f"求 {p1} 和 {p2} 的距離"
            q_en = f"Distance between {p1} and {p2}"
            opts = [dist, dist+1, dist-1, dist*2]
        else:
            # Pythagorean triple
            triples = [(3,4,5),(5,12,13),(6,8,10),(8,15,17),(7,24,25),(9,12,15)]
            dx, dy, hyp = random.choice(triples)
            if random.random() < 0.5: dx = -dx
            if random.random() < 0.5: dy = -dy
            x1, y1 = random.randint(-8,8), random.randint(-8,8)
            x2, y2 = x1+dx, y1+dy
            q_zh = f"求 ({x1},{y1}) 和 ({x2},{y2}) 的距離"
            q_en = f"Distance between ({x1},{y1}) and ({x2},{y2})"
            opts = [hyp, hyp+1, hyp-1, abs(dx)+abs(dy)]
        qs.append((q_zh, q_en, hyp if t==1 else dist, opts))
    return qs

def gen_coordinates_midpoint(n):
    """中點"""
    qs = []
    for _ in range(n):
        x1, y1 = random.randint(-15,15), random.randint(-15,15)
        x2, y2 = random.randint(-15,15), random.randint(-15,15)
        mx, my = (x1+x2)//2 if (x1+x2)%2==0 else (x1+x2)/2, (y1+y2)//2 if (y1+y2)%2==0 else (y1+y2)/2
        ans = f"({mx},{my})"
        q_zh = f"求 ({x1},{y1}) 和 ({x2},{y2}) 的中點"
        q_en = f"Midpoint of ({x1},{y1}) and ({x2},{y2})"
        opts = [ans, f"({x1+x2},{y1+y2})", f"({x1},{y2})", f"({x2},{y1})"]
        qs.append((q_zh, q_en, ans, opts))
    return qs

def gen_basic_geometry_triangles(n):
    """三角形"""
    qs = []
    for _ in range(n):
        t = random.randint(0,3)
        if t == 0:
            a, b = random.randint(20,80), random.randint(20,80)
            c = 180 - a - b
            if c <= 0: c, b = 60, 180-a-60
            q_zh = f"三角形兩角為 {a}° 和 {b}°，求第三角"
            q_en = f"Triangle: angles {a}° and {b}°. Find the third."
            ans = c
            opts = [c, 360-a-b, a+b, c+1]
        elif t == 1:
            # Isosceles
            base = random.randint(30,80)
            other = (180-base)//2
            q_zh = f"等腰三角形頂角 {base}°，求底角"
            q_en = f"Isosceles triangle: vertex angle {base}°. Find base angle."
            ans = other
            opts = [other, base, 180-base, other+1]
        elif t == 2:
            # Equilateral angle
            q_zh = "等邊三角形的每個角是多少度？"
            q_en = "What is each angle in an equilateral triangle?"
            ans = 60
            opts = [60, 90, 45, 120]
        else:
            # Right triangle
            a = random.randint(20,70)
            b = 90 - a
            q_zh = f"直角三角形一個銳角 {a}°，求另一個銳角"
            q_en = f"Right triangle: one acute angle {a}°. Find the other."
            ans = b
            opts = [b, 180-a, a, 90+a]
        qs.append((q_zh, q_en, ans, opts))
    return qs

def gen_basic_geometry_angles(n):
    """角"""
    qs = []
    for _ in range(n):
        t = random.randint(0,2)
        if t == 0:  # Complementary
            a = random.randint(10,80)
            b = 90-a
            q_zh = f"兩角互補，一角為 {a}°，求另一角"
            q_en = f"Complementary: one angle {a}°. Find the other."
            ans = b
            opts = [b, 180-a, a, 90+a]
        elif t == 1:  # Supplementary
            a = random.randint(10,170)
            b = 180-a
            q_zh = f"兩角互補，一角為 {a}°，求另一角"
            q_en = f"Supplementary: one angle {a}°. Find the other."
            ans = b
            opts = [b, 360-a, a, 90-a]
        else:
            # Vertical angles
            a = random.randint(20,80)
            q_zh = f"對頂角其中一角 {a}°，另一角是多少？"
            q_en = f"Vertical angle: one is {a}°. Find the other."
            ans = a
            opts = [a, 180-a, 90-a, 360-a]
        qs.append((q_zh, q_en, ans, opts))
    return qs

def gen_basic_geometry_parallel(n):
    """平行線"""
    qs = []
    for _ in range(n):
        a = random.choice([x for x in range(20,160) if x != 90])
        t = random.randint(0,2)
        if t == 0:
            q_zh = f"兩直線平行，一角 {a}°，求同位角"
            q_en = f"Parallel lines, angle {a}°. Find corresponding angle."
            ans = a
            opts = [a, 180-a, 360-a, 90]
        elif t == 1:
            q_zh = f"兩直線平行，一角 {a}°，求內錯角"
            q_en = f"Parallel lines, angle {a}°. Find alternate interior angle."
            ans = a
            opts = [a, 180-a, 360-a, 90]
        else:
            q_zh = f"兩直線平行，一角 {a}°，求同旁內角"
            q_en = f"Parallel lines, angle {a}°. Find co-interior angle."
            ans = 180-a
            opts = [180-a, a, 360-a, 90-a]
        qs.append((q_zh, q_en, ans, opts))
    return qs

def gen_basic_geometry_polygons(n):
    """多邊形"""
    qs = []
    for _ in range(n):
        t = random.randint(0,4)
        if t == 0:
            sides = random.randint(3,12)
            interior = (sides-2)*180
            q_zh = f"{sides} 邊形的內角和是多少？"
            q_en = f"Sum of interior angles of a {sides}-gon?"
            ans = interior
            opts = [interior, sides*180, (sides-1)*180, interior+180]
        elif t == 1:
            sides = random.randint(3,10)
            q_zh = f"任意 {sides} 邊形的外角和是多少？"
            q_en = f"Sum of exterior angles of any {sides}-gon?"
            ans = 360
            opts = [360, (sides-2)*180, sides*180, 180]
        elif t == 2:
            sides = random.randint(3,10)
            each = 360 / sides
            q_zh = f"正 {sides} 邊形每個外角是多少度？"
            q_en = f"Each exterior angle of a regular {sides}-gon?"
            ans = round(each, 2)
            opts = [ans, round((sides-2)*180/sides, 2), 180-each, each*2]
        elif t == 3:
            sides = random.randint(3,10)
            each = (sides-2)*180/sides
            q_zh = f"正 {sides} 邊形每個內角是多少度？"
            q_en = f"Each interior angle of a regular {sides}-gon?"
            ans = round(each, 2)
            opts = [ans, round(360/sides, 2), 180-each, each+1]
        else:
            sides = random.randint(5,12)
            diagonals = sides*(sides-3)//2
            q_zh = f"{sides} 邊形有多少條對角線？"
            q_en = f"How many diagonals in a {sides}-gon?"
            ans = diagonals
            opts = [diagonals, sides*(sides-1)//2, sides*2, diagonals+1]
        qs.append((q_zh, q_en, ans, opts))
    return qs

def gen_area_volume_area(n):
    """面積"""
    qs = []
    for _ in range(n):
        t = random.randint(0,4)
        if t == 0:  # Rectangle
            a, b = random.randint(3,25), random.randint(3,25)
            ans = a*b
            q_zh = f"長方形闊 {a} cm，長 {b} cm，求面積"
            q_en = f"Rectangle: {a}cm × {b}cm. Find area."
            opts = [ans, 2*(a+b), a+b, ans+1]
        elif t == 1:  # Triangle
            base, height = random.randint(4,20), random.randint(3,20)
            ans = round(base*height/2, 1)
            q_zh = f"三角形底 {base} cm，高 {height} cm，求面積"
            q_en = f"Triangle: base {base}cm, height {height}cm. Find area."
            opts = [ans, base*height, ans+1, base+height]
        elif t == 2:  # Circle
            r = random.choice([3,4,5,6,7,8,10])
            ans = round(3.14*r**2, 2)
            q_zh = f"圓形半徑 {r} cm，求面積（取 π = 3.14）"
            q_en = f"Circle radius {r}cm. Find area (π=3.14)."
            opts = [ans, round(2*3.14*r,2), round(3.14*r,2), round(3.14*r**3,2)]
        elif t == 3:  # Square
            s = random.randint(3,20)
            ans = s**2
            q_zh = f"正方形邊長 {s} cm，求面積"
            q_en = f"Square side {s}cm. Find area."
            opts = [ans, 4*s, 2*s, ans+1]
        else:  # Parallelogram
            base, height = random.randint(5,20), random.randint(3,15)
            ans = base*height
            q_zh = f"平行四邊形底 {base} cm，高 {height} cm，求面積"
            q_en = f"Parallelogram: base {base}cm, height {height}cm. Find area."
            opts = [ans, 2*(base+height), base+height, ans+1]
        qs.append((q_zh, q_en, ans, opts))
    return qs

def gen_area_volume_volume(n):
    """體積"""
    qs = []
    for _ in range(n):
        t = random.randint(0,3)
        if t == 0:  # Cuboid
            a, b, c = random.randint(2,12), random.randint(2,12), random.randint(2,12)
            ans = a*b*c
            q_zh = f"長方體 {a}×{b}×{c} cm，求體積"
            q_en = f"Cuboid {a}×{b}×{c}cm. Find volume."
            opts = [ans, 2*(a*b+b*c+a*c), a+b+c, ans+1]
        elif t == 1:  # Cube
            s = random.randint(2,8)
            ans = s**3
            q_zh = f"正方體邊長 {s} cm，求體積"
            q_en = f"Cube side {s}cm. Find volume."
            opts = [ans, 6*s**2, 3*s, ans+1]
        elif t == 2:  # Cylinder
            r = random.choice([3,4,5,6,7])
            h = random.randint(5,15)
            ans = round(3.14*r**2*h, 1)
            q_zh = f"圓柱體半徑 {r} cm，高 {h} cm，求體積（π ≈ 3.14）"
            q_en = f"Cylinder: r={r}cm, h={h}cm. Find volume (π≈3.14)."
            opts = [ans, round(2*3.14*r*h,1), round(3.14*r*h,1), round(3.14*r**2,1)]
        else:  # Prism (triangular)
            base, tri_h, length = random.randint(3,10), random.randint(3,10), random.randint(5,15)
            ans = round(0.5*base*tri_h*length, 1)
            q_zh = f"三角柱底邊 {base} cm，三角形高 {tri_h} cm，柱長 {length} cm，求體積"
            q_en = f"Triangular prism: base {base}cm, tri-height {tri_h}cm, length {length}cm. Volume?"
            opts = [ans, base*tri_h*length, round(0.5*base*length,1), ans+1]
        qs.append((q_zh, q_en, ans, opts))
    return qs

def gen_ratio_rate_simplify(n):
    """簡化比"""
    qs = []
    for _ in range(n):
        g = random.randint(2,6)
        a, b = g*random.randint(1,8), g*random.randint(1,8)
        g2 = math.gcd(a,b)
        ans = f"{a//g2}:{b//g2}"
        q_zh = f"簡化比 {a}:{b}"
        q_en = f"Simplify {a}:{b}"
        opts = [ans, f"{a}:{b}", f"{a+1}:{b}", f"{a}:{b+1}"]
        qs.append((q_zh, q_en, ans, opts))
    return qs

def gen_ratio_rate_sharing(n):
    """按比分配"""
    qs = []
    for _ in range(n):
        total = random.choice([100,120,150,200,240,300,360,500,600,1000])
        a, b = random.randint(1,6), random.randint(1,6)
        g = math.gcd(a,b)
        a, b = a//g, b//g
        share_a = total*a//(a+b)
        share_b = total*b//(a+b)
        t = random.randint(0,1)
        if t == 0:
            q_zh = f"${total} 按 {a}:{b} 分給甲乙，甲得多少？"
            q_en = f"${total} shared in ratio {a}:{b}. How much does A get?"
            ans = share_a
            opts = [share_a, share_b, total//(a+b), share_a+share_b]
        else:
            q_zh = f"${total} 按 {a}:{b} 分給甲乙，乙得多少？"
            q_en = f"${total} shared in ratio {a}:{b}. How much does B get?"
            ans = share_b
            opts = [share_b, share_a, total//(a+b), share_b+1]
        qs.append((q_zh, q_en, ans, opts))
    return qs

def gen_ratio_rate_sdt(n):
    """行程問題"""
    qs = []
    for _ in range(n):
        t = random.randint(0,2)
        if t == 0:  # Find distance
            speed = random.choice([20,30,40,50,60,80,100])
            time = random.choice([0.5,1,1.5,2,2.5,3])
            dist = speed * time
            q_zh = f"時速 {speed} 公里，行駛 {time} 小時，求距離"
            q_en = f"Speed {speed}km/h, time {time}h. Find distance."
            ans = dist
            opts = [dist, speed+time, speed-time, dist+1]
        elif t == 1:  # Find speed
            dist = random.choice([50,60,80,100,120,150,200])
            time = random.choice([1,2,3,4,5])
            speed = dist/time
            q_zh = f"距離 {dist} 公里，用 {time} 小時，求速度"
            q_en = f"Distance {dist}km, time {time}h. Find speed."
            ans = speed
            opts = [speed, dist+time, dist-time, speed+1]
        else:  # Word problem
            speed = random.choice([30,40,50,60])
            time = random.choice([1,2,3])
            dist = speed * time
            q_zh = f"巴士以時速 {speed} 公里行駛，{time} 小時行咗幾多公里？"
            q_en = f"Bus travels at {speed}km/h. How far in {time}h?"
            ans = dist
            opts = [dist, speed+time, speed-time, dist+1]
        qs.append((q_zh, q_en, ans, opts))
    return qs

def gen_mixed_shopping(n):
    """購物"""
    qs = []
    stores = ["惠康", "屈臣氏", "萬寧", "7-Eleven", "OK便利店", "百佳"]
    items = [("口罩",38),("零食",25),("飲品",12),("蘋果",8),("麵包",15),("雞蛋",30),("牛奶",22),("筆",5)]
    for _ in range(n):
        store = random.choice(stores)
        item, price = random.choice(items)
        qty = random.randint(2,10)
        discount = random.choice([10,15,20,25,30])
        subtotal = price * qty
        saved = round(subtotal * discount/100, 1)
        total = subtotal - saved
        t = random.randint(0,2)
        if t == 0:
            q_zh = f"在{store}買 {qty} 個{item}，每個 ${price}，{discount}% 折扣後總價？"
            q_en = f"Buy {qty} {item} at ${price} each, {discount}% off. Total?"
            ans = total
            opts = [total, subtotal, saved, total+1]
        elif t == 1:
            q_zh = f"在{store}買 {qty} 個{item}，每個 ${price}，折咗幾多錢？"
            q_en = f"Buy {qty} {item} at ${price} each. How much saved with {discount}% off?"
            ans = saved
            opts = [saved, total, subtotal, saved+1]
        else:
            q_zh = f"在{store}買 {qty} 個{item}，每個 ${price}，折前總價？"
            q_en = f"Buy {qty} {item} at ${price} each. Subtotal before {discount}% discount?"
            ans = subtotal
            opts = [subtotal, total, saved, subtotal+1]
        qs.append((q_zh, q_en, ans, opts))
    return qs

def gen_mixed_age(n):
    """年齡問題"""
    qs = []
    names = ["小明", "小紅", "小華", "小強", "小美", "大寶", "阿珍", "阿強"]
    for _ in range(n):
        name = random.choice(names)
        age = random.randint(6,15)
        years = random.randint(1,20)
        t = random.randint(0,1)
        if t == 0:
            q_zh = f"{name}今年 {age} 歲，{years} 年後幾歲？"
            q_en = f"{name} is {age} now. How old in {years} years?"
            ans = age + years
            opts = [ans, age-years, age*years, ans+1]
        else:
            if years > age: years = random.randint(1, age-1)
            q_zh = f"{name}今年 {age} 歲，{years} 年前幾歲？"
            q_en = f"{name} is {age} now. How old {years} years ago?"
            ans = age - years
            opts = [ans, age+years, age*years, ans+1]
        qs.append((q_zh, q_en, ans, opts))
    return qs

def gen_mixed_work(n):
    """工程問題"""
    qs = []
    for _ in range(n):
        t = random.randint(0,3)
        if t == 0:
            a = random.randint(2,8)
            b = random.randint(2,8)
            while b == a:
                b = random.randint(2,8)
            num, den = a*b, a+b
            g = math.gcd(num, den)
            ans = f"{num//g}/{den//g}"
            q_zh = f"甲需 {a} 小時完成工作，乙需 {b} 小時，合作需幾多小時？"
            q_en = f"A takes {a}h, B takes {b}h. Time working together?"
            opts = [ans, f"{a+b}", f"{a*b}", f"{(a+b)//2}"]
        elif t == 1:
            a = random.randint(3,10)
            total = random.randint(50,200)
            rate = total / a
            q_zh = f"甲每小時做 {rate:.0f} 件產品，{a} 小時共做幾多件？"
            q_en = f"A makes {rate:.0f} items/hour. Total in {a}h?"
            ans = total
            opts = [total, total+1, int(rate), total+a]
        elif t == 2:
            total = random.randint(100,500)
            a = random.randint(2,8)
            per = total / a
            q_zh = f"{total} 件產品由 {a} 人平均分做，每人做幾多件？"
            q_en = f"{total} items shared equally among {a} workers. Each?"
            ans = per
            opts = [per, per+1, total-a, a]
        else:
            a, b = random.randint(2,6), random.randint(2,6)
            while b == a:
                b = random.randint(2,6)
            # A does 1/a per hour, B does 1/b per hour
            # Fraction done in 1 hour = 1/a + 1/b = (a+b)/(ab)
            num, den = a+b, a*b
            g = math.gcd(num, den)
            ans = f"{num//g}/{den//g}"
            q_zh = f"甲需 {a} 小時，乙需 {b} 小時，合作 1 小時完成幾多？"
            q_en = f"A: {a}h, B: {b}h. Fraction done in 1h together?"
            opts = [ans, f"1/{a+b}", f"{a+b}/{a*b}", f"1/{max(a,b)}"]
        qs.append((q_zh, q_en, ans, opts))
    return qs

def gen_percentages_basic(n):
    """百分數計算"""
    qs = []
    bases = list(range(20, 1001, 7))  # Many more base values
    pcts = list(range(3, 91, 3))  # Many more percentage values
    for _ in range(n):
        t = random.randint(0,3)
        if t == 0:
            base = random.choice(bases)
            pct = random.choice(pcts)
            ans = base * pct / 100
            q_zh = f"計算 {base} 的 {pct}% 是多少？"
            q_en = f"What is {pct}% of {base}?"
            opts = [ans, ans*10, base-ans, base+ans]
        elif t == 1:
            base = random.choice(bases)
            pct = random.choice(pcts)
            ans = base * pct / 100
            q_zh = f"{base} 嘅 {pct}% 等於幾多？"
            q_en = f"{pct}% of {base} equals?"
            opts = [ans, base-pct, base+pct, ans*2]
        elif t == 2:
            # Reverse: find the percentage
            base = random.choice([50,100,200,250,500,1000])
            pct = random.choice([10,20,25,40,50])
            part = base * pct / 100
            q_zh = f"{part:.0f} 佔 {base} 嘅百分之幾？"
            q_en = f"{part:.0f} is what percent of {base}?"
            ans = pct
            opts = [pct, pct*10, 100-pct, pct*2]
        else:
            # Word problem
            total = random.randint(40, 200)
            pct = random.choice([10,15,20,25,30,40,50,60,75,80,90])
            ans = total * pct / 100
            q_zh = f"全班 {total} 人，{pct}% 係男生，男生有幾多人？"
            q_en = f"{total} students, {pct}% are boys. How many boys?"
            opts = [ans, total-ans, ans+1, total]
        qs.append((q_zh, q_en, ans, opts))
    return qs

def gen_percentages_change(n):
    """百分數增減"""
    qs = []
    prices = list(range(50, 2001, 13))  # Many price values
    pcts = list(range(3, 51, 3))  # Many percentage values
    for _ in range(n):
        price = random.choice(prices)
        pct = random.choice(pcts)
        t = random.randint(0,3)
        if t == 0:  # Increase
            new_price = price * (1 + pct/100)
            q_zh = f"一件貨品原價 ${price}，加價 {pct}% 後售價是多少？"
            q_en = f"Item costs ${price}. After {pct}% increase, new price?"
            ans = new_price
            opts = [new_price, price*pct/100, price*(1-pct/100), new_price+price]
        elif t == 1:  # Decrease
            new_price = price * (1 - pct/100)
            q_zh = f"一件貨品原價 ${price}，減價 {pct}% 後售價是多少？"
            q_en = f"Item costs ${price}. After {pct}% decrease, new price?"
            ans = new_price
            opts = [new_price, price*pct/100, price*(1+pct/100), new_price-1]
        elif t == 2:  # Find discount amount
            new_price = price * (1 - pct/100)
            saved = price - new_price
            q_zh = f"一件貨品原價 ${price}，減價 {pct}%，平咗幾多？"
            q_en = f"Item costs ${price}, {pct}% off. How much saved?"
            ans = saved
            opts = [saved, new_price, price*pct, saved+1]
        else:  # Find original price
            pct_used = random.choice([10,20,25,30,40,50])
            original = random.choice([100,200,250,400,500,800,1000])
            new_price = original * (1 - pct_used/100)
            q_zh = f"減價 {pct_used}% 後售 ${new_price:.0f}，原價幾多？"
            q_en = f"After {pct_used}% off, price is ${new_price:.0f}. Original?"
            ans = original
            opts = [original, new_price, original+pct_used, new_price*2]
        qs.append((q_zh, q_en, ans, opts))
    return qs

def gen_sequences_arithmetic(n):
    """等差數列"""
    qs = []
    for _ in range(n):
        start = random.randint(1,20)
        diff = random.randint(2,10)
        term = random.randint(5,20)
        ans = start + (term-1)*diff
        seq = [start + i*diff for i in range(4)]
        seq_str = ", ".join(map(str, seq))
        q_zh = f"等差數列 {seq_str}, ...，求第 {term} 項"
        q_en = f"AP: {seq_str}, ..., find term {term}"
        opts = [ans, ans+diff, ans-diff, start+term*diff]
        qs.append((q_zh, q_en, ans, opts))
    return qs

def gen_sequences_patterns(n):
    """規律"""
    qs = []
    for _ in range(n):
        t = random.randint(0,7)
        if t == 0:
            nums = [i**2 for i in range(1,6)]
            next_val = 6**2
            q_zh = f"數列 {', '.join(map(str,nums))}, ...，下一個數是？"
            q_en = f"Sequence: {', '.join(map(str,nums))}, ... Next?"
            ans = next_val
            opts = [next_val, next_val+1, 31, 30]
        elif t == 1:
            a, b = 1, 1
            seq = [a, b]
            for _ in range(4):
                a, b = b, a+b
                seq.append(b)
            next_val = seq[-1] + seq[-2]
            q_zh = f"數列 {', '.join(map(str,seq))}, ...，下一個數是？"
            q_en = f"Sequence: {', '.join(map(str,seq))}, ... Next?"
            ans = next_val
            opts = [next_val, next_val+1, seq[-1]*2, seq[-1]+1]
        elif t == 2:
            start = random.randint(2,5)
            ratio = random.randint(2,3)
            nums = [start * ratio**i for i in range(4)]
            next_val = start * ratio**4
            q_zh = f"等比數列 {', '.join(map(str,nums))}, ...，下一個數是？"
            q_en = f"GP: {', '.join(map(str,nums))}, ... Next?"
            ans = next_val
            opts = [next_val, nums[-1]+ratio, nums[-1]*2, next_val+1]
        elif t == 3:
            # Triangular numbers
            tri = [i*(i+1)//2 for i in range(1,7)]
            next_val = 7*8//2
            q_zh = f"三角數列 {', '.join(map(str,tri))}, ...，下一個是？"
            q_en = f"Triangular: {', '.join(map(str,tri))}, ... Next?"
            ans = next_val
            opts = [next_val, next_val+1, 48, 49]
        elif t == 4:
            # Cube numbers
            nums = [i**3 for i in range(1,5)]
            next_val = 5**3
            q_zh = f"立方數列 {', '.join(map(str,nums))}, ...，下一個是？"
            q_en = f"Cubes: {', '.join(map(str,nums))}, ... Next?"
            ans = next_val
            opts = [next_val, 64, 80, 100]
        elif t == 5:
            # Powers of 2
            base = random.choice([2, 3])
            nums = [base**i for i in range(5)]
            next_val = base**5
            q_zh = f"{base}嘅冪次方數列 {', '.join(map(str,nums))}, ...，下一個是？"
            q_en = f"Powers of {base}: {', '.join(map(str,nums))}, ... Next?"
            ans = next_val
            opts = [next_val, next_val+1, nums[-1]*base, nums[-1]+base]
        elif t == 6:
            # Prime numbers
            primes = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47]
            start = random.randint(0,8)
            seq = primes[start:start+5]
            next_val = primes[start+5]
            q_zh = f"質數列 {', '.join(map(str,seq))}, ...，下一個是？"
            q_en = f"Primes: {', '.join(map(str,seq))}, ... Next?"
            ans = next_val
            opts = [next_val, next_val+2, next_val+1, next_val-2]
        else:
            # Odd numbers pattern
            start = random.randint(1,10)
            step = random.choice([2,3,5])
            nums = [start + i*step for i in range(5)]
            next_val = start + 5*step
            q_zh = f"數列 {', '.join(map(str,nums))}, ...，下一個是？"
            q_en = f"Sequence: {', '.join(map(str,nums))}, ... Next?"
            ans = next_val
            opts = [next_val, next_val+1, next_val-step, next_val+step]
        qs.append((q_zh, q_en, ans, opts))
    return qs


# ============================================================
# MAIN GENERATION + SHUFFLING
# ============================================================

def generate_all():
    """Generate all 10,000 questions with proper distribution."""
    # Target distribution
    distribution = {
        "directed_number": {"bodmas": 400, "fractions": 400, "hcf_lcm": 200, "absolute": 150, "powers": 100},
        "statistics": {"mean": 350, "median": 300, "mode": 250, "probability": 150},
        "basic_algebra": {"linear_eq": 350, "simplify": 250, "expand": 200, "substitution": 200, "inequalities": 150},
        "coordinates": {"distance": 580, "midpoint": 580},
        "basic_geometry": {"triangles": 350, "angles": 300, "parallel": 300, "polygons": 150},
        "area_volume": {"area": 550, "volume": 550},
        "ratio_rate": {"simplify": 400, "sharing": 400, "sdt": 300},
        "mixed": {"shopping": 400, "age": 300, "work": 400},
        "percentages": {"basic": 650, "change": 550},
        "sequences": {"arithmetic": 650, "patterns": 100},
    }

    # Generator functions
    generators = {
        ("directed_number", "bodmas"): gen_directed_number_bodmas,
        ("directed_number", "fractions"): gen_directed_number_fractions,
        ("directed_number", "hcf_lcm"): gen_directed_number_hcf_lcm,
        ("directed_number", "absolute"): gen_directed_number_absolute,
        ("directed_number", "powers"): gen_directed_number_powers,
        ("statistics", "mean"): gen_statistics_mean,
        ("statistics", "median"): gen_statistics_median,
        ("statistics", "mode"): gen_statistics_mode,
        ("statistics", "probability"): gen_statistics_probability,
        ("basic_algebra", "linear_eq"): gen_basic_algebra_linear_eq,
        ("basic_algebra", "simplify"): gen_basic_algebra_simplify,
        ("basic_algebra", "expand"): gen_basic_algebra_expand,
        ("basic_algebra", "substitution"): gen_basic_algebra_substitution,
        ("basic_algebra", "inequalities"): gen_basic_algebra_inequalities,
        ("coordinates", "distance"): gen_coordinates_distance,
        ("coordinates", "midpoint"): gen_coordinates_midpoint,
        ("basic_geometry", "triangles"): gen_basic_geometry_triangles,
        ("basic_geometry", "angles"): gen_basic_geometry_angles,
        ("basic_geometry", "parallel"): gen_basic_geometry_parallel,
        ("basic_geometry", "polygons"): gen_basic_geometry_polygons,
        ("area_volume", "area"): gen_area_volume_area,
        ("area_volume", "volume"): gen_area_volume_volume,
        ("ratio_rate", "simplify"): gen_ratio_rate_simplify,
        ("ratio_rate", "sharing"): gen_ratio_rate_sharing,
        ("ratio_rate", "sdt"): gen_ratio_rate_sdt,
        ("mixed", "shopping"): gen_mixed_shopping,
        ("mixed", "age"): gen_mixed_age,
        ("mixed", "work"): gen_mixed_work,
        ("percentages", "basic"): gen_percentages_basic,
        ("percentages", "change"): gen_percentages_change,
        ("sequences", "arithmetic"): gen_sequences_arithmetic,
        ("sequences", "patterns"): gen_sequences_patterns,
    }

    # Display names
    topic_names = {
        "directed_number": ("正負數", "Directed Number"),
        "statistics": ("統計圖表", "Statistics"),
        "basic_algebra": ("基本代數", "Basic Algebra"),
        "coordinates": ("坐標", "Coordinates"),
        "basic_geometry": ("基本幾何", "Basic Geometry"),
        "area_volume": ("面積與體積", "Area & Volume"),
        "ratio_rate": ("比與比率", "Ratio & Rate"),
        "mixed": ("綜合應用", "Mixed Applications"),
        "percentages": ("百分數", "Percentages"),
        "sequences": ("規律與數列", "Sequences"),
    }
    subtopic_names = {
        "bodmas": ("四則混合運算", "Mixed Operations"),
        "fractions": ("分數運算", "Fraction Operations"),
        "hcf_lcm": ("公因數與公倍數", "HCF & LCM"),
        "absolute": ("絕對值", "Absolute Value"),
        "powers": ("冪次", "Powers"),
        "mean": ("平均數", "Mean"),
        "median": ("中位數", "Median"),
        "mode": ("眾數", "Mode"),
        "probability": ("概率", "Probability"),
        "linear_eq": ("一元一次方程", "Linear Equations"),
        "simplify": ("簡化代數式", "Simplify"),
        "expand": ("展開", "Expand"),
        "substitution": ("代入求值", "Substitution"),
        "inequalities": ("不等式", "Inequalities"),
        "distance": ("距離", "Distance"),
        "midpoint": ("中點", "Midpoint"),
        "triangles": ("三角形", "Triangles"),
        "angles": ("角", "Angles"),
        "parallel": ("平行線", "Parallel Lines"),
        "polygons": ("多邊形", "Polygons"),
        "area": ("面積", "Area"),
        "volume": ("體積", "Volume"),
        "simplify_ratio": ("簡化比", "Simplify Ratio"),
        "sharing": ("按比分配", "Ratio Sharing"),
        "sdt": ("行程問題", "Speed/Distance/Time"),
        "shopping": ("購物", "Shopping"),
        "age": ("年齡", "Age Problems"),
        "work": ("工程", "Work Problems"),
        "basic_pct": ("百分數計算", "Basic Percentage"),
        "pct_change": ("百分數增減", "Percentage Change"),
        "arithmetic": ("等差數列", "Arithmetic Sequences"),
        "patterns": ("規律", "Patterns"),
    }

    # Generate questions grouped by topic+subtopic
    all_by_topic = {}  # topic_id -> list of question dicts
    seen_q = set()

    # Actually generate
    for (topic_id, subtopic_id), gen_func in generators.items():
        target = distribution[topic_id][subtopic_id]
        raw = gen_func(target * 2)  # Generate extra for dedup

        topic_zh, topic_en = topic_names[topic_id]
        sub_zh, sub_en = subtopic_names.get(subtopic_id, (subtopic_id.replace("_"," ").title(), subtopic_id.replace("_"," ").title()))

        questions = []
        for q_zh, q_en, ans, opts in raw:
            # Deduplicate
            if q_zh in seen_q:
                continue
            seen_q.add(q_zh)

            # Format answer and options
            if isinstance(ans, float):
                ans_str = str(round(ans, 2))
            else:
                ans_str = str(ans)
            opts_str = []
            for o in opts:
                if isinstance(o, float):
                    opts_str.append(str(round(o, 2)))
                else:
                    opts_str.append(str(o))

            # Ensure answer is in options
            if ans_str not in opts_str:
                opts_str[0] = ans_str

            # Shuffle options and find correct index
            combined = list(enumerate(opts_str))
            random.shuffle(combined)
            correct_idx = next(i for i,(orig,_) in enumerate(combined) if orig==0)
            shuffled_opts = [o for _,o in combined]

            # Difficulty
            diff = random.choices([1,2,3], weights=[40,40,20])[0]

            questions.append({
                "topic_id": topic_id,
                "topic_zh": topic_zh,
                "topic_en": topic_en,
                "subtopic_id": subtopic_id,
                "subtopic_zh": sub_zh,
                "subtopic_en": sub_en,
                "question_zh": q_zh,
                "question_en": q_en,
                "options_zh": shuffled_opts,
                "options_en": shuffled_opts,
                "answer": correct_idx,
                "explanation_zh": f"正確答案是 {ans_str}。",
                "explanation_en": f"The correct answer is {ans_str}.",
                "difficulty": diff,
            })

            if len(questions) >= target:
                break

        all_by_topic[topic_id] = all_by_topic.get(topic_id, []) + questions
        print(f"  {topic_id}/{subtopic_id}: {len(questions)} questions")

    return all_by_topic


def round_robin_shuffle(all_by_topic):
    """Round-robin shuffle: guarantee NO two consecutive same topic."""
    topic_items = []
    for tid, qs in all_by_topic.items():
        random.shuffle(qs)
        topic_items.append((tid, qs))

    # Use min count for strict round-robin, rest go into extras
    min_count = min(len(qs) for _, qs in topic_items)
    print(f'  Round-robin base: {min_count} per topic × {len(topic_items)} topics = {min_count * len(topic_items)}')

    # Phase 1: strict round-robin
    result = []
    for r in range(min_count):
        round_qs = [qs[r] for tid, qs in topic_items]
        random.shuffle(round_qs)
        result.extend(round_qs)

    # Phase 2: insert extras at non-clashing positions
    extras = []
    for tid, qs in topic_items:
        extras.extend(qs[min_count:])
    random.shuffle(extras)
    
    for q in extras:
        q_tid = q['topic_id']
        inserted = False
        step = max(1, len(result) // (len(extras) + 1))
        start = random.randint(0, min(step, len(result)))
        for pos in range(start, len(result) + 1, step):
            prev_ok = pos == 0 or result[pos - 1]['topic_id'] != q_tid
            next_ok = pos >= len(result) or result[pos]['topic_id'] != q_tid
            if prev_ok and next_ok:
                result.insert(pos, q)
                inserted = True
                break
        if not inserted:
            # Try every position
            for pos in range(len(result) + 1):
                prev_ok = pos == 0 or result[pos - 1]['topic_id'] != q_tid
                next_ok = pos >= len(result) or result[pos]['topic_id'] != q_tid
                if prev_ok and next_ok:
                    result.insert(pos, q)
                    inserted = True
                    break
        if not inserted:
            result.append(q)

    # Phase 3: swap away any remaining consecutive same-topic pairs
    for _ in range(500):
        fixed_all = True
        for i in range(1, len(result)):
            if result[i]['topic_id'] == result[i-1]['topic_id']:
                fixed_all = False
                for j in range(i+1, min(i+500, len(result))):
                    jt = result[j]['topic_id']
                    if jt == result[i-1]['topic_id']:
                        continue
                    if j+1 < len(result) and jt == result[j+1]['topic_id']:
                        continue
                    if j-1 >= 0 and result[j-1]['topic_id'] == result[i]['topic_id']:
                        continue
                    result[i], result[j] = result[j], result[i]
                    break
                break
        if fixed_all:
            break

    # Trim to 10000
    result = result[:10000]

    # Re-assign IDs
    for i, q in enumerate(result):
        q['id'] = i + 1

    return result


def verify(data):
    """Print verification summary."""
    print(f"\n{'='*60}")
    print(f"VERIFICATION SUMMARY")
    print(f"{'='*60}")
    print(f"Total questions: {len(data)}")

    # Topic distribution
    from collections import Counter
    topics = Counter(q['topic_id'] for q in data)
    print(f"\nTopic distribution:")
    for t, c in topics.most_common():
        print(f"  {t}: {c}")

    # Consecutive same-topic check
    max_run = 0
    current_topic = None
    current_len = 0
    for q in data:
        t = q['topic_id']
        if t == current_topic:
            current_len += 1
        else:
            max_run = max(max_run, current_len)
            current_topic = t
            current_len = 1
    max_run = max(max_run, current_len)
    print(f"\nMax consecutive same-topic run: {max_run}")

    # Duplicate check
    q_texts = [q['question_zh'] for q in data]
    dupes = len(q_texts) - len(set(q_texts))
    print(f"Duplicate question texts: {dupes}")

    # Sample
    print(f"\nSample 15 consecutive questions:")
    for i in range(min(15, len(data))):
        q = data[i]
        print(f"  Q{q['id']}: [{q['topic_id']}] {q['question_zh'][:55]}")


if __name__ == "__main__":
    print("Generating 10,000 math questions (v3)...")
    all_by_topic = generate_all()

    total = sum(len(v) for v in all_by_topic.values())
    print(f"\nGenerated {total} questions total")
    print("Round-robin shuffling...")

    data = round_robin_shuffle(all_by_topic)
    verify(data)

    # Save to both locations
    for path in ['math/s1/questions.json', 'v2/math/s1/questions.json']:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=1)
        print(f"\nSaved to {path}")

    print("\nDone! ✅")
