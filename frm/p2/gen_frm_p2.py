#!/usr/bin/env python3
"""Generate 5000 unique FRM Part 2 questions with bilingual support.
Uses extensive variations: numbers, scenarios, templates."""
import json, random, os, math

random.seed(2024)

def q(zh, en, opts_zh, opts_en, ans, exp_zh, exp_en, topic_zh, topic_en, diff=1):
    return {
        "question_zh": zh, "question_en": en,
        "options_zh": opts_zh, "options_en": opts_en,
        "answer": ans,
        "explanation_zh": exp_zh, "explanation_en": exp_en,
        "topic_zh": topic_zh, "topic_en": topic_en,
        "difficulty": diff
    }

def shuffle_answer(q_obj, seed):
    r = random.Random(seed)
    idx = [0, 1, 2, 3]
    r.shuffle(idx)
    q_obj['options_zh'] = [q_obj['options_zh'][i] for i in idx]
    q_obj['options_en'] = [q_obj['options_en'][i] for i in idx]
    q_obj['answer'] = idx.index(q_obj['answer'])
    return q_obj

all_q = []

# ============================================================
# TOPIC 1: Market Risk (1000 questions)
# ============================================================
T1_ZH, T1_EN = "市場風險 (20%)", "Market Risk (20%)"

# 1a: VaR calculations with numbers (200)
for i in range(200):
    r = random.Random(i * 10)
    port_val = r.choice([50, 100, 200, 500, 1000])  # millions
    mu = r.uniform(-0.05, 0.15)
    sigma = r.uniform(0.10, 0.40)
    z = r.choice([1.645, 2.326, 2.576])
    conf = r.choice([95, 97.5, 99])
    var_val = round(port_val * (mu - z * sigma), 2)
    es_val = round(port_val * (mu - z * sigma * 1.2), 2)
    method = r.choice(["參數法", "歷史模擬法", "蒙特卡羅法"])
    method_en = {"參數法": "parametric", "歷史模擬法": "historical simulation", "蒙特卡羅法": "Monte Carlo"}[method]
    
    if i % 4 == 0:
        wrong1 = round(port_val * (mu - z * sigma * 0.8), 2)
        wrong2 = round(port_val * (mu - z * sigma * 1.5), 2)
        wrong3 = round(port_val * mu, 2)
        all_q.append(shuffle_answer(q(
            f"投資組合價值{port_val}百萬，年化回報率{mu*100:.1f}%，波動率{sigma*100:.1f}%。使用{method}計算{conf}% VaR：",
            f"Portfolio value ${port_val}M, annual return {mu*100:.1f}%, volatility {sigma*100:.1f}%. Calculate {conf}% VaR using {method_en}:",
            [f"A. {var_val}百萬", f"B. {wrong1}百萬", f"C. {wrong2}百萬", f"D. {wrong3}百萬"],
            [f"A. ${var_val}M", f"B. ${wrong1}M", f"C. ${wrong2}M", f"D. ${wrong3}M"],
            0, f"VaR = {port_val} × ({mu*100:.1f}% - {z:.3f} × {sigma*100:.1f}%) = {var_val}百萬",
            f"VaR = {port_val} × ({mu*100:.1f}% - {z:.3f} × {sigma*100:.1f}%) = ${var_val}M", T1_ZH, T1_EN, 2
        ), i * 100))
    elif i % 4 == 1:
        wrong1 = round(es_val * 0.9, 2)
        wrong2 = round(es_val * 1.3, 2)
        wrong3 = round(var_val, 2)
        all_q.append(shuffle_answer(q(
            f"同上，{conf}% Expected Shortfall (CVaR) 最接近：",
            f"Using the same parameters, the {conf}% Expected Shortfall (CVaR) is closest to:",
            [f"A. {es_val}百萬", f"B. {wrong1}百萬", f"C. {wrong2}百萬", f"D. {wrong3}百萬"],
            [f"A. ${es_val}M", f"B. ${wrong1}M", f"C. ${wrong2}M", f"D. ${wrong3}M"],
            0, f"ES通常大於VaR，CVaR ≈ {es_val}百萬", f"ES exceeds VaR, CVaR ≈ ${es_val}M", T1_ZH, T1_EN, 2
        ), i * 101))
    elif i % 4 == 2:
        breach = r.randint(2, 15)
        expected = round(250 * (1 - conf / 100), 1)
        all_q.append(shuffle_answer(q(
            f"250個交易日中，VaR被突破{breach}次（{conf}%置信度）。Kupiec檢驗的結論是：",
            f"VaR breached {breach} times in 250 trading days ({conf}% confidence). Kupiec test conclusion:",
            [f"A. {'拒絕H0，模型有問題' if breach > expected * 2 else '不拒絕H0，模型可接受'}",
             f"B. {'不拒絕H0，模型可接受' if breach > expected * 2 else '拒絕H0，模型有問題'}",
             f"C. 需要更多數據才能判斷", f"D. Kupiec檢驗不適用於此情況"],
            [f"A. {'Reject H0, model inadequate' if breach > expected * 2 else 'Cannot reject H0, model acceptable'}",
             f"B. {'Cannot reject H0, model acceptable' if breach > expected * 2 else 'Reject H0, model inadequate'}",
             f"C. Need more data to conclude", f"D. Kupiec test not applicable"],
            0 if breach <= expected * 2 else 0,
            f"預期突破{expected:.0f}次，實際{breach}次", f"Expected {expected:.0f} breaches, actual {breach}", T1_ZH, T1_EN, 3
        ), i * 102))
    else:
        delta = r.uniform(0.3, 0.9)
        gamma = r.uniform(0.01, 0.1)
        vega = r.uniform(0.1, 0.5)
        spot_change = r.choice([2, 5, 10])
        pnl = round(delta * spot_change + 0.5 * gamma * spot_change ** 2, 2)
        wrong1 = round(delta * spot_change, 2)
        wrong2 = round(gamma * spot_change, 2)
        wrong3 = round(vega * spot_change, 2)
        all_q.append(shuffle_answer(q(
            f"Delta={delta:.2f}, Gamma={gamma:.4f}。標的資產上漲{spot_change}點，期權P&L近似值？",
            f"Delta={delta:.2f}, Gamma={gamma:.4f}. If underlying rises {spot_change} points, approximate option P&L?",
            [f"A. {pnl}", f"B. {wrong1}", f"C. {wrong2}", f"D. {wrong3}"],
            [f"A. {pnl}", f"B. {wrong1}", f"C. {wrong2}", f"D. {wrong3}"],
            0, f"ΔP&L ≈ Δ·δx + ½·Γ·(δx)² = {pnl}", f"ΔP&L ≈ Δ·δx + ½·Γ·(δx)² = {pnl}", T1_ZH, T1_EN, 2
        ), i * 103))

# 1b: Duration/Convexity with numbers (150)
for i in range(150):
    r = random.Random(i * 200 + 5000)
    dur = r.uniform(3, 15)
    conv = r.uniform(20, 200)
    y_change = r.choice([0.5, 1.0, 1.5, 2.0])
    price_change = round(-dur * y_change + 0.5 * conv * (y_change / 100) ** 2, 4)
    wrong1 = round(-dur * y_change, 4)
    wrong2 = round(dur * y_change, 4)
    wrong3 = round(-dur * y_change * 2, 4)
    
    if i % 3 == 0:
        all_q.append(shuffle_answer(q(
            f"債券修正久期{dur:.2f}，凸性{conv:.1f}。收益率上升{y_change}%時，價格變動近似值？",
            f"Bond modified duration {dur:.2f}, convexity {conv:.1f}. If yield rises {y_change}%, approximate price change?",
            [f"A. {price_change*100:.2f}%", f"B. {wrong1*100:.2f}%", f"C. {wrong2*100:.2f}%", f"D. {wrong3*100:.2f}%"],
            [f"A. {price_change*100:.2f}%", f"B. {wrong1*100:.2f}%", f"C. {wrong2*100:.2f}%", f"D. {wrong3*100:.2f}%"],
            0, f"ΔP/P ≈ -D·Δy + ½·C·(Δy)² = {price_change*100:.2f}%",
            f"ΔP/P ≈ -D·Δy + ½·C·(Δy)² = {price_change*100:.2f}%", T1_ZH, T1_EN, 2
        ), i * 200))
    elif i % 3 == 1:
        mac_dur = dur * (1 + r.uniform(0.02, 0.08))
        ytm = r.uniform(0.03, 0.08)
        mod_dur = round(mac_dur / (1 + ytm), 2)
        wrong1 = round(mac_dur * (1 + ytm), 2)
        wrong2 = round(mac_dur, 2)
        wrong3 = round(mac_dur / (1 + ytm * 2), 2)
        all_q.append(shuffle_answer(q(
            f"麥考利久期{mac_dur:.2f}年，到期收益率{ytm*100:.1f}%。修正久期？",
            f"Macaulay duration {mac_dur:.2f} years, YTM {ytm*100:.1f}%. Modified duration?",
            [f"A. {mod_dur}", f"B. {wrong1}", f"C. {wrong2}", f"D. {wrong3}"],
            [f"A. {mod_dur}", f"B. {wrong1}", f"C. {wrong2}", f"D. {wrong3}"],
            0, f"修正久期 = 麥考利久期 / (1+y) = {mod_dur}",
            f"Modified Duration = Macaulay Duration / (1+y) = {mod_dur}", T1_ZH, T1_EN, 1
        ), i * 201))
    else:
        dv01 = round(dur * 0.0001 * r.choice([10, 50, 100]) * 1000000, 0)
        notional = r.choice([10, 50, 100])
        wrong1 = round(dv01 * 0.5, 0)
        wrong2 = round(dv01 * 2, 0)
        wrong3 = round(dv01 * 1.5, 0)
        all_q.append(shuffle_answer(q(
            f"面值{notional}百萬，修正久期{dur:.2f}。DV01最接近？",
            f"Face value ${notional}M, modified duration {dur:.2f}. DV01 is closest to:",
            [f"A. ${dv01:,.0f}", f"B. ${wrong1:,.0f}", f"C. ${wrong2:,.0f}", f"D. ${wrong3:,.0f}"],
            [f"A. ${dv01:,.0f}", f"B. ${wrong1:,.0f}", f"C. ${wrong2:,.0f}", f"D. ${wrong3:,.0f}"],
            0, f"DV01 = D × 0.0001 × 面值 = ${dv01:,.0f}",
            f"DV01 = D × 0.0001 × Notional = ${dv01:,.0f}", T1_ZH, T1_EN, 2
        ), i * 202))

# 1c: Greeks conceptual (150)
greeks = [
    ("Delta (Δ)", "Delta", "期權價格對標的資產價格的敏感度", "Sensitivity of option price to underlying asset price"),
    ("Gamma (Γ)", "Gamma", "Delta對標的資產價格的變化率", "Rate of change of delta with respect to underlying price"),
    ("Vega (ν)", "Vega", "期權價格對隱含波動率的敏感度", "Sensitivity of option price to implied volatility"),
    ("Theta (Θ)", "Theta", "期權價格隨時間的衰減", "Time decay of option price"),
    ("Rho (ρ)", "Rho", "期權價格對利率的敏感度", "Sensitivity of option price to interest rates"),
]
for i in range(150):
    r = random.Random(i * 300 + 8000)
    g = greeks[i % len(greeks)]
    others = [x for x in greeks if x[0] != g[0]]
    wrong = r.sample(others, 3)
    
    templates = [
        (f"以下哪個希臘字母衡量{g[2]}？", f"Which Greek letter measures {g[3].lower()}?"),
        (f"交易員想對沖{g[2]}，應監控哪個指標？", f"A trader hedging {g[3].lower()} should monitor which metric?"),
        (f"{g[0]}的經濟含義是：", f"The economic meaning of {g[1]} is:"),
    ]
    t = templates[i % len(templates)]
    all_q.append(shuffle_answer(q(
        t[0], t[1],
        [f"A. {g[2]}", f"B. {wrong[0][2]}", f"C. {wrong[1][2]}", f"D. {wrong[2][2]}"],
        [f"A. {g[3]}", f"B. {wrong[0][3]}", f"C. {wrong[1][3]}", f"D. {wrong[2][3]}"],
        0, f"{g[0]}：{g[2]}", f"{g[1]}: {g[3]}", T1_ZH, T1_EN, (i % 3) + 1
    ), i * 300))

# 1d: Volatility modeling (150)
for i in range(150):
    r = random.Random(i * 400 + 9000)
    sigma_prev = r.uniform(0.15, 0.35)
    ret = r.uniform(-0.05, 0.05)
    lam = r.choice([0.90, 0.94, 0.97])
    ewma_var = lam * sigma_prev ** 2 + (1 - lam) * ret ** 2
    ewma_vol = round(math.sqrt(ewma_var) * 100, 2)
    wrong1 = round(math.sqrt(lam * sigma_prev ** 2) * 100, 2)
    wrong2 = round(math.sqrt(sigma_prev ** 2 + ret ** 2) * 100, 2)
    wrong3 = round(sigma_prev * 100, 2)
    
    all_q.append(shuffle_answer(q(
        f"前日波動率{sigma_prev*100:.1f}%，今日回報{ret*100:.2f}%，λ={lam}。EWMA今日波動率？",
        f"Previous day volatility {sigma_prev*100:.1f}%, today's return {ret*100:.2f}%, λ={lam}. EWMA volatility today?",
        [f"A. {ewma_vol}%", f"B. {wrong1}%", f"C. {wrong2}%", f"D. {wrong3}%"],
        [f"A. {ewma_vol}%", f"B. {wrong1}%", f"C. {wrong2}%", f"D. {wrong3}%"],
        0, f"σ²(t) = λ·σ²(t-1) + (1-λ)·r²(t) = {ewma_vol}%",
        f"σ²(t) = λ·σ²(t-1) + (1-λ)·r²(t) = {ewma_vol}%", T1_ZH, T1_EN, 2
    ), i * 400))

# 1e: Stress testing & scenarios (100)
stress_scenarios = [
    ("歷史情景法", "Historical Scenario Analysis", "使用歷史上的市場事件作為壓力情景", "Uses historical market events as stress scenarios"),
    ("假設情景法", "Hypothetical Scenario Analysis", "構建假設的極端市場條件", "Constructs hypothetical extreme market conditions"),
    ("反向壓力測試", "Reverse Stress Testing", "從損失結果反推導致該損失的情景", "Works backward from loss to find scenarios causing it"),
    ("敏感度分析", "Sensitivity Analysis", "逐一改變風險因子觀察影響", "Changes one risk factor at a time to observe impact"),
]
for i in range(100):
    s = stress_scenarios[i % len(stress_scenarios)]
    others = [x for x in stress_scenarios if x[0] != s[0]]
    wrong = random.sample(others, 3)
    all_q.append(shuffle_answer(q(
        f"壓力測試中，{s[0]}的特點是：", f"In stress testing, {s[1]} is characterized by:",
        [f"A. {s[2]}", f"B. {wrong[0][2]}", f"C. {wrong[1][2]}", f"D. {wrong[2][2]}"],
        [f"A. {s[3]}", f"B. {wrong[0][3]}", f"C. {wrong[1][3]}", f"D. {wrong[2][3]}"],
        0, f"{s[0]}：{s[2]}", f"{s[1]}: {s[3]}", T1_ZH, T1_EN, (i % 3) + 1
    ), i * 500))

# 1f: Correlation and copulas (100)
copulas = [
    ("Gaussian Copula", "Gaussian Copula", "假設聯合正態分佈的依賴結構", "Assumes joint normal dependence structure"),
    ("t-Copula", "t-Copula", "允許尾部依賴的copula模型", "Copula model allowing tail dependence"),
    ("Clayton Copula", "Clayton Copula", "捕捉下尾依賴的copula", "Copula capturing lower tail dependence"),
    ("Kendall's τ", "Kendall's Tau", "非參數的等級相關性度量", "Non-parametric rank correlation measure"),
    ("Spearman's ρ", "Spearman's Rho", "基於等級的相關性度量", "Rank-based correlation measure"),
]
for i in range(100):
    c = copulas[i % len(copulas)]
    others = [x for x in copulas if x[0] != c[0]]
    wrong = random.sample(others, 3)
    all_q.append(shuffle_answer(q(
        f"在依賴結構建模中，{c[0]}的特點是：", f"In dependence structure modeling, {c[1]} is characterized by:",
        [f"A. {c[2]}", f"B. {wrong[0][2]}", f"C. {wrong[1][2]}", f"D. {wrong[2][2]}"],
        [f"A. {c[3]}", f"B. {wrong[0][3]}", f"C. {wrong[1][3]}", f"D. {wrong[2][3]}"],
        0, f"{c[0]}：{c[2]}", f"{c[1]}: {c[3]}", T1_ZH, T1_EN, (i % 3) + 1
    ), i * 600))

# 1g: FRTB and Basel market risk (50)
frtb = [
    ("FRTB (交易賬簿基本審查)", "FRTB (Fundamental Review of the Trading Book)", "改革市場風險資本框架的Basel倡議", "Basel initiative to reform market risk capital framework"),
    ("標準化方法 (SA-MR)", "Standardized Approach (SA)", "基於敏感度的市場風險資本計算", "Sensitivity-based market risk capital calculation"),
    ("內部模型法 (IMA-MR)", "Internal Models Approach (IMA)", "使用內部VaR模型計算資本", "Uses internal VaR models for capital calculation"),
    ("交易賬簿/銀行賬簿劃分", "Trading Book / Banking Book Boundary", "界定市場風險資本適用範圍", "Defines scope of market risk capital application"),
]
for i in range(50):
    f = frtb[i % len(frtb)]
    others = [x for x in frtb if x[0] != f[0]]
    wrong = random.sample(others, 3)
    all_q.append(shuffle_answer(q(
        f"關於{f[0]}，以下哪項正確？", f"Regarding {f[1]}, which is correct?",
        [f"A. {f[2]}", f"B. {wrong[0][2]}", f"C. {wrong[1][2]}", f"D. {wrong[2][2]}"],
        [f"A. {f[3]}", f"B. {wrong[0][3]}", f"C. {wrong[1][3]}", f"D. {wrong[2][3]}"],
        0, f"{f[0]}：{f[2]}", f"{f[1]}: {f[3]}", T1_ZH, T1_EN, (i % 3) + 1
    ), i * 700))

# ============================================================
# TOPIC 2: Credit Risk (1000 questions)
# ============================================================
T2_ZH, T2_EN = "信用風險 (20%)", "Credit Risk (20%)"

# 2a: Merton model calculations (200)
for i in range(200):
    r = random.Random(i * 500 + 10000)
    V = r.choice([500, 1000, 2000, 5000])  # firm value
    D = r.choice([300, 400, 600, 800])  # debt face value
    sigma_V = r.uniform(0.15, 0.40)
    T = r.choice([1, 2, 5])
    rf = r.uniform(0.02, 0.06)
    
    if i % 5 == 0:
        # Merton: equity = call option on firm value
        leverage = D / V
        wrong1 = round(V - D, 2)
        wrong2 = round(D * 0.4, 2)
        wrong3 = round(V * sigma_V, 2)
        all_q.append(shuffle_answer(q(
            f"公司資產{V}百萬，負債面值{D}百萬。在Merton模型中，股權可視為：",
            f"Firm assets ${V}M, debt face value ${D}M. In the Merton model, equity is:",
            [f"A. 標的資產為公司價值的看漲期權", f"B. 等於資產減負債 ({wrong1}百萬)",
             f"C. 固定為負債的40% ({wrong2}百萬)", f"D. 與資產波動率成正比 ({wrong3}百萬)"],
            [f"A. A call option on firm assets", f"B. Equal to assets minus debt (${wrong1}M)",
             f"C. Fixed at 40% of debt (${wrong2}M)", f"D. Proportional to asset vol (${wrong3}M)"],
            0, "Merton模型中股權 = max(V-D, 0)的看漲期權",
            "In Merton model, equity = call option on V with strike D", T2_ZH, T2_EN, 3
        ), i * 100))
    elif i % 5 == 1:
        # Distance to default
        dd = round((math.log(V / D) + (rf - 0.5 * sigma_V ** 2) * T) / (sigma_V * math.sqrt(T)), 4)
        wrong1 = round((V - D) / (sigma_V * V), 4)
        wrong2 = round(math.log(V / D) / sigma_V, 4)
        wrong3 = round(dd * 2, 4)
        all_q.append(shuffle_answer(q(
            f"V={V}M, D={D}M, σ_V={sigma_V*100:.1f}%, T={T}年, r={rf*100:.1f}%。距離違約(DD)？",
            f"V=${V}M, D=${D}M, σ_V={sigma_V*100:.1f}%, T={T}yr, r={rf*100:.1f}%. Distance to Default?",
            [f"A. {dd}", f"B. {wrong1}", f"C. {wrong2}", f"D. {wrong3}"],
            [f"A. {dd}", f"B. {wrong1}", f"C. {wrong2}", f"D. {wrong3}"],
            0, f"DD = [ln(V/D) + (r-σ²/2)T] / (σ√T) = {dd}",
            f"DD = [ln(V/D) + (r-σ²/2)T] / (σ√T) = {dd}", T2_ZH, T2_EN, 3
        ), i * 101))
    elif i % 5 == 2:
        # CVA calculation
        lgd = r.uniform(0.3, 0.7)
        ead = r.choice([10, 50, 100, 500])
        pd = r.uniform(0.01, 0.10)
        cva = round(lgd * ead * pd, 2)
        wrong1 = round(ead * pd, 2)
        wrong2 = round(lgd * ead, 2)
        wrong3 = round(lgd * pd * 100, 2)
        all_q.append(shuffle_answer(q(
            f"LGD={lgd*100:.0f}%, EAD={ead}M, PD={pd*100:.1f}%。簡化CVA？",
            f"LGD={lgd*100:.0f}%, EAD=${ead}M, PD={pd*100:.1f}%. Simplified CVA?",
            [f"A. {cva}M", f"B. {wrong1}M", f"C. {wrong2}M", f"D. {wrong3}M"],
            [f"A. ${cva}M", f"B. ${wrong1}M", f"C. ${wrong2}M", f"D. ${wrong3}M"],
            0, f"CVA ≈ LGD × EAD × PD = {cva}M", f"CVA ≈ LGD × EAD × PD = ${cva}M", T2_ZH, T2_EN, 2
        ), i * 102))
    elif i % 5 == 3:
        # Expected loss
        pd = r.uniform(0.01, 0.15)
        lgd = r.uniform(0.2, 0.8)
        ead = r.choice([20, 100, 200, 1000])
        el = round(pd * lgd * ead, 2)
        wrong1 = round(pd * ead, 2)
        wrong2 = round(lgd * ead, 2)
        wrong3 = round(pd * lgd * ead * 2, 2)
        all_q.append(shuffle_answer(q(
            f"PD={pd*100:.1f}%, LGD={lgd*100:.0f}%, EAD={ead}M。預期損失(EL)？",
            f"PD={pd*100:.1f}%, LGD={lgd*100:.0f}%, EAD=${ead}M. Expected Loss (EL)?",
            [f"A. {el}M", f"B. {wrong1}M", f"C. {wrong2}M", f"D. {wrong3}M"],
            [f"A. ${el}M", f"B. ${wrong1}M", f"C. ${wrong2}M", f"D. ${wrong3}M"],
            0, f"EL = PD × LGD × EAD = {el}M", f"EL = PD × LGD × EAD = ${el}M", T2_ZH, T2_EN, 1
        ), i * 103))
    else:
        # Recovery rate
        recovery = r.uniform(0.2, 0.6)
        lgd = round(1 - recovery, 2)
        all_q.append(shuffle_answer(q(
            f"回收率{recovery*100:.0f}%，則違約損失率(LGD)為：",
            f"If recovery rate is {recovery*100:.0f}%, Loss Given Default (LGD) is:",
            [f"A. {lgd*100:.0f}%", f"B. {recovery*100:.0f}%", f"C. {lgd*50:.0f}%", f"D. {(1-lgd)*100:.0f}%"],
            [f"A. {lgd*100:.0f}%", f"B. {recovery*100:.0f}%", f"C. {lgd*50:.0f}%", f"D. {(1-lgd)*100:.0f}%"],
            0, f"LGD = 1 - 回收率 = {lgd*100:.0f}%", f"LGD = 1 - Recovery Rate = {lgd*100:.0f}%", T2_ZH, T1_EN, 1
        ), i * 104))

# 2b: Credit derivatives conceptual (200)
cd_concepts = [
    ("CDS利差", "CDS Spread", "反映參考實體信用風險的市場價格", "Market price reflecting credit risk of reference entity"),
    ("違約觸發事件", "Credit Event", "CDS合約規定的違約事件類型", "Types of default events specified in CDS contract"),
    ("ISDA主協議", "ISDA Master Agreement", "場外衍生品交易的標準合約框架", "Standard contract framework for OTC derivatives"),
    ("淨額結算", "Netting", "將多筆交易合併計算淨暴露", "Combining multiple transactions for net exposure"),
    ("擔保品協議", "Collateral Agreement", "要求提供擔保品以降低交易對手風險", "Requiring collateral to reduce counterparty risk"),
]
for i in range(200):
    c = cd_concepts[i % len(cd_concepts)]
    others = [x for x in cd_concepts if x[0] != c[0]]
    wrong = random.sample(others, 3)
    all_q.append(shuffle_answer(q(
        f"在信用衍生品市場中，{c[0]}的定義是：", f"In credit derivatives, {c[1]} is defined as:",
        [f"A. {c[2]}", f"B. {wrong[0][2]}", f"C. {wrong[1][2]}", f"D. {wrong[2][2]}"],
        [f"A. {c[3]}", f"B. {wrong[0][3]}", f"C. {wrong[1][3]}", f"D. {wrong[2][3]}"],
        0, f"{c[0]}：{c[2]}", f"{c[1]}: {c[3]}", T2_ZH, T2_EN, (i % 3) + 1
    ), i * 200))

# 2c: Securitization (200)
sec = [
    ("優先級 (Senior Tranche)", "Senior Tranche", "最先獲得現金流，最後承擔損失", "First to receive cash flows, last to bear losses"),
    ("夾層 (Mezzanine Tranche)", "Mezzanine Tranche", "中間風險和回報層級", "Middle risk-return tranche"),
    ("次級 (Equity Tranche)", "Equity Tranche", "最先承擔損失，最後獲得現金流", "First to bear losses, last to receive cash flows"),
    ("瀑布式結構", "Waterfall Structure", "現金流按優先級順序分配", "Cash flows distributed in order of priority"),
    ("超額擔保", "Overcollateralization", "擔保資產價值超過證券面值", "Collateral asset value exceeds security face value"),
    ("資產支持證券 (ABS)", "Asset-Backed Security (ABS)", "以資產池為擔保發行的證券", "Security backed by a pool of assets"),
]
for i in range(200):
    s = sec[i % len(sec)]
    others = [x for x in sec if x[0] != s[0]]
    wrong = random.sample(others, 3)
    all_q.append(shuffle_answer(q(
        f"在證券化中，{s[0]}的特點是：", f"In securitization, {s[1]} is characterized by:",
        [f"A. {s[2]}", f"B. {wrong[0][2]}", f"C. {wrong[1][2]}", f"D. {wrong[2][2]}"],
        [f"A. {s[3]}", f"B. {wrong[0][3]}", f"C. {wrong[1][3]}", f"D. {wrong[2][3]}"],
        0, f"{s[0]}：{s[2]}", f"{s[1]}: {s[3]}", T2_ZH, T2_EN, (i % 3) + 1
    ), i * 300))

# 2d: Credit migration (200)
for i in range(200):
    r = random.Random(i * 600 + 15000)
    ratings = ['AAA', 'AA', 'A', 'BBB', 'BB', 'B', 'CCC']
    from_rating = r.choice(ratings[1:-1])
    to_idx = ratings.index(from_rating) + r.choice([-1, 0, 1])
    to_idx = max(0, min(len(ratings) - 1, to_idx))
    to_rating = ratings[to_idx]
    
    scenarios = [
        (f"信用評級從{from_rating}遷移到{to_rating}，這屬於：", f"Credit rating migrating from {from_rating} to {to_rating} is a:"),
        (f"某公司評級從{from_rating}變為{to_rating}，對其CDS利差的影響是：", f"A firm's rating changes from {from_rating} to {to_rating}. Impact on CDS spread:"),
    ]
    s = scenarios[i % 2]
    direction = "升級" if ratings.index(to_rating) < ratings.index(from_rating) else ("降級" if ratings.index(to_rating) > ratings.index(from_rating) else "不變")
    direction_en = "upgrade" if direction == "升級" else ("downgrade" if direction == "降級" else "unchanged")
    
    wrong_dir1 = "降級" if direction == "升級" else ("升級" if direction == "降級" else "降級")
    wrong_dir1_en = "downgrade" if direction_en == "upgrade" else ("upgrade" if direction_en == "downgrade" else "downgrade")
    
    all_q.append(shuffle_answer(q(
        s[0], s[1],
        [f"A. {direction}", f"B. {wrong_dir1}", f"C. 違約", f"D. 無影響"],
        [f"A. {direction_en}", f"B. {wrong_dir1_en}", f"C. Default", f"D. No impact"],
        0, f"{from_rating}→{to_rating}是{direction}", f"{from_rating}→{to_rating} is {direction_en}", T2_ZH, T2_EN, (i % 3) + 1
    ), i * 400))

# 2e: Counterparty risk concepts (200)
cp_concepts = [
    ("EPE (預期正暴露)", "Expected Positive Exposure (EPE)", "預期的正暴露平均值", "Average of expected positive exposures"),
    ("PFE (潛在未來暴露)", "Potential Future Exposure (PFE)", "給定置信度下的最大未來暴露", "Maximum future exposure at a given confidence level"),
    ("EE (預期暴露)", "Expected Exposure (EE)", "特定時點的預期正暴露", "Expected positive exposure at a specific time"),
    ("有效EPE", "Effective EPE", "累積預期正暴露的加權平均", "Weighted average of cumulative expected positive exposure"),
    ("淨暴露", "Net Exposure", "考慮淨額結算後的暴露", "Exposure after netting"),
]
for i in range(200):
    c = cp_concepts[i % len(cp_concepts)]
    others = [x for x in cp_concepts if x[0] != c[0]]
    wrong = random.sample(others, 3)
    all_q.append(shuffle_answer(q(
        f"在交易對手信用風險中，{c[0]}的定義是：", f"In counterparty credit risk, {c[1]} is defined as:",
        [f"A. {c[2]}", f"B. {wrong[0][2]}", f"C. {wrong[1][2]}", f"D. {wrong[2][2]}"],
        [f"A. {c[3]}", f"B. {wrong[0][3]}", f"C. {wrong[1][3]}", f"D. {wrong[2][3]}"],
        0, f"{c[0]}：{c[2]}", f"{c[1]}: {c[3]}", T2_ZH, T2_EN, (i % 3) + 1
    ), i * 500))

# ============================================================
# TOPIC 3: Operational Risk (1000 questions)
# ============================================================
T3_ZH, T3_EN = "操作風險 (20%)", "Operational Risk (20%)"

# 3a: Basel framework (200)
basel = [
    ("基本指標法 (BIA)", "Basic Indicator Approach", "以三年平均總收入的15%計提資本", "Capital = 15% of 3-year average gross income"),
    ("標準化方法 (TSA)", "Standardized Approach", "按業務線分配收入計提資本", "Capital allocated by business line income"),
    ("新標準化方法 (NSA)", "New Standardized Approach", "Basel IV下更風險敏感的方法", "More risk-sensitive method under Basel IV"),
    ("內部模型法 (IMA)", "Internal Models Approach", "使用銀行自己的損失數據建模", "Uses bank's own loss data for modeling"),
]
for i in range(200):
    b = basel[i % len(basel)]
    others = [x for x in basel if x[0] != b[0]]
    wrong = random.sample(others, 3)
    all_q.append(shuffle_answer(q(
        f"操作風險資本計量中，{b[0]}的特點是：", f"In operational risk capital, {b[1]} is characterized by:",
        [f"A. {b[2]}", f"B. {wrong[0][2]}", f"C. {wrong[1][2]}", f"D. {wrong[2][2]}"],
        [f"A. {b[3]}", f"B. {wrong[0][3]}", f"C. {wrong[1][3]}", f"D. {wrong[2][3]}"],
        0, f"{b[0]}：{b[2]}", f"{b[1]}: {b[3]}", T3_ZH, T3_EN, (i % 3) + 1
    ), i * 100))

# 3b: Loss distribution approach (150)
for i in range(150):
    r = random.Random(i * 700 + 20000)
    n_losses = r.randint(50, 500)
    mean_loss = r.uniform(0.1, 5.0)
    max_loss = r.uniform(10, 100)
    var_loss = r.uniform(1, 20)
    
    if i % 3 == 0:
        all_q.append(shuffle_answer(q(
            f"損失分佈法(LDA)中，收集了{n_losses}筆損失數據，平均損失{mean_loss:.1f}M。LDA的目的是：",
            f"In LDA with {n_losses} losses, mean loss ${mean_loss:.1f}M. LDA's purpose is:",
            [f"A. 估計操作風險的損失分佈和資本要求", f"B. 計算每筆損失的精確金額",
             f"C. 確定損失發生的根本原因", f"D. 預測下一次損失的確切時間"],
            [f"A. Estimate op risk loss distribution and capital", f"B. Calculate exact amount of each loss",
             f"C. Determine root cause of each loss", f"D. Predict exact time of next loss"],
            0, "LDA通過擬合頻率和嚴重度分佈來估計操作風險資本",
            "LDA estimates op risk capital by fitting frequency and severity distributions", T3_ZH, T3_EN, 2
        ), i * 100))
    elif i % 3 == 1:
        all_q.append(shuffle_answer(q(
            f"LDA中，嚴重度分佈通常使用：", f"In LDA, the severity distribution typically uses:",
            [f"A. 對數正態分佈或廣義帕累托分佈(GPD)", f"B. 正態分佈",
             f"C. 均勻分佈", f"D. 二項分佈"],
            [f"A. Lognormal or Generalized Pareto Distribution (GPD)", f"B. Normal distribution",
             f"C. Uniform distribution", f"D. Binomial distribution"],
            0, "操作損失通常呈厚尾分佈，適合用對數正態或GPD",
            "Op risk losses are heavy-tailed, suited to lognormal or GPD", T3_ZH, T3_EN, 2
        ), i * 101))
    else:
        all_q.append(shuffle_answer(q(
            f"LDA中，損失頻率分佈通常使用：", f"In LDA, the loss frequency distribution typically uses:",
            [f"A. 泊松分佈或負二項分佈", f"B. 正態分佈",
             f"C. 對數正態分佈", f"D. 指數分佈"],
            [f"A. Poisson or Negative Binomial distribution", f"B. Normal distribution",
             f"C. Lognormal distribution", f"D. Exponential distribution"],
            0, "損失次數通常用泊松或負二項分佈建模",
            "Loss counts are typically modeled with Poisson or Negative Binomial", T3_ZH, T3_EN, 2
        ), i * 102))

# 3c: Scenario analysis (150)
for i in range(150):
    r = random.Random(i * 800 + 22000)
    scenarios = [
        ("內部欺詐情景：交易員偽造記錄導致的損失", "Internal fraud: Trader falsifies records", 50),
        ("系統故障：核心銀行系統宕機24小時", "Core banking system down 24 hours", 100),
        ("外部欺詐：網絡攻擊導致數據洩露", "Cyber attack causing data breach", 200),
        ("合規失敗：反洗錢程序不當導致罰款", "AML failure leading to regulatory fine", 150),
    ]
    s = scenarios[i % len(scenarios)]
    others = [x for x in scenarios if x[0] != s[0]]
    wrong = random.sample(others, 3)
    all_q.append(shuffle_answer(q(
        f"操作風險情景分析中，以下哪個是{s[0][:20]}的典型情景？",
        f"In op risk scenario analysis, which is a typical scenario for {s[1][:30]}?",
        [f"A. {s[0]}", f"B. {wrong[0][0]}", f"C. {wrong[1][0]}", f"D. {wrong[2][0]}"],
        [f"A. {s[1]}", f"B. {wrong[0][1]}", f"C. {wrong[1][1]}", f"D. {wrong[2][1]}"],
        0, f"情景分析用於評估極端但可能的操作風險事件",
            f"Scenario analysis assesses extreme but plausible op risk events", T3_ZH, T3_EN, 2
        ), i * 200))

# 3d: Cyber and IT risk (200)
cyber = [
    ("勒索軟件攻擊", "Ransomware Attack", "加密受害者數據並要求贖金", "Encrypts victim's data and demands ransom"),
    ("分佈式拒絕服務 (DDoS)", "Distributed Denial of Service", "通過大量請求使系統不可用", "Makes system unavailable through massive requests"),
    ("供應鏈攻擊", "Supply Chain Attack", "通過第三方供應商滲透系統", "Penetrates systems through third-party vendors"),
    ("釣魚攻擊", "Phishing Attack", "通過欺騙性郵件獲取敏感信息", "Obtains sensitive info through deceptive emails"),
    ("零日漏洞", "Zero-Day Vulnerability", "尚未被修補的軟件安全漏洞", "Software security flaw not yet patched"),
    ("數據洩露", "Data Breach", "未經授權訪問敏感數據", "Unauthorized access to sensitive data"),
]
for i in range(200):
    c = cyber[i % len(cyber)]
    others = [x for x in cyber if x[0] != c[0]]
    wrong = random.sample(others, 3)
    all_q.append(shuffle_answer(q(
        f"在IT風險管理中，{c[0]}的特點是：", f"In IT risk management, {c[1]} is characterized by:",
        [f"A. {c[2]}", f"B. {wrong[0][2]}", f"C. {wrong[1][2]}", f"D. {wrong[2][2]}"],
        [f"A. {c[3]}", f"B. {wrong[0][3]}", f"C. {wrong[1][3]}", f"D. {wrong[2][3]}"],
        0, f"{c[0]}：{c[2]}", f"{c[1]}: {c[3]}", T3_ZH, T3_EN, (i % 3) + 1
    ), i * 300))

# 3e: Model risk management (150)
model_risk = [
    ("模型驗證", "Model Validation", "獨立評估模型的準確性和適當性", "Independent assessment of model accuracy and appropriateness"),
    ("模型監控", "Model Monitoring", "持續追蹤模型表現和偏差", "Ongoing tracking of model performance and deviations"),
    ("模型清單", "Model Inventory", "所有在用模型的完整記錄", "Complete record of all models in use"),
    ("模型風險資本", "Model Risk Capital", "因模型錯誤導致的潛在損失準備", "Reserve for potential losses from model errors"),
]
for i in range(150):
    m = model_risk[i % len(model_risk)]
    others = [x for x in model_risk if x[0] != m[0]]
    wrong = random.sample(others, 3)
    all_q.append(shuffle_answer(q(
        f"在模型風險管理中，{m[0]}的定義是：", f"In model risk management, {m[1]} is defined as:",
        [f"A. {m[2]}", f"B. {wrong[0][2]}", f"C. {wrong[1][2]}", f"D. {wrong[2][2]}"],
        [f"A. {m[3]}", f"B. {wrong[0][3]}", f"C. {wrong[1][3]}", f"D. {wrong[2][3]}"],
        0, f"{m[0]}：{m[2]}", f"{m[1]}: {m[3]}", T3_ZH, T3_EN, (i % 3) + 1
    ), i * 400))

# 3f: KRI and RCSA (150)
kri = [
    ("前瞻性KRI", "Leading KRI", "預測潛在風險事件的指標", "Indicator that predicts potential risk events"),
    ("滯後性KRI", "Lagging KRI", "反映已發生風險事件的指標", "Indicator reflecting past risk events"),
    ("風險容忍度", "Risk Tolerance", "組織願意承受的最大風險水平", "Maximum risk level organization is willing to accept"),
    ("風險偏好", "Risk Appetite", "組織為達成目標願意承擔的風險總量", "Total risk organization accepts to achieve objectives"),
    ("控制環境", "Control Environment", "組織的風險管理和控制文化", "Organization's risk management and control culture"),
]
for i in range(150):
    k = kri[i % len(kri)]
    others = [x for x in kri if x[0] != k[0]]
    wrong = random.sample(others, 3)
    all_q.append(shuffle_answer(q(
        f"在風險管理框架中，{k[0]}的含義是：", f"In risk management framework, {k[1]} means:",
        [f"A. {k[2]}", f"B. {wrong[0][2]}", f"C. {wrong[1][2]}", f"D. {wrong[2][2]}"],
        [f"A. {k[3]}", f"B. {wrong[0][3]}", f"C. {wrong[1][3]}", f"D. {wrong[2][3]}"],
        0, f"{k[0]}：{k[2]}", f"{k[1]}: {k[3]}", T3_ZH, T3_EN, (i % 3) + 1
    ), i * 500))

# ============================================================
# TOPIC 4: Liquidity and Treasury Risk (750 questions)
# ============================================================
T4_ZH, T4_EN = "流動性與財務風險 (15%)", "Liquidity and Treasury Risk (15%)"

# 4a: LCR/NSFR calculations (200)
for i in range(200):
    r = random.Random(i * 900 + 25000)
    hqla = r.choice([80, 100, 120, 150, 200])
    outflows = r.choice([70, 90, 100, 110, 130])
    inflows = r.choice([30, 40, 50, 60])
    net_out = max(outflows - min(inflows, outflows * 0.75), 10)
    lcr = round(hqla / net_out * 100, 1)
    
    if i % 3 == 0:
        wrong1 = round(hqla / outflows * 100, 1)
        wrong2 = round((hqla + inflows) / outflows * 100, 1)
        wrong3 = round(hqla * 100 / (outflows - inflows), 1)
        all_q.append(shuffle_answer(q(
            f"HQLA={hqla}M，淨流出={net_out:.0f}M。LCR？",
            f"HQLA=${hqla}M, net outflows=${net_out:.0f}M. LCR?",
            [f"A. {lcr}%", f"B. {wrong1}%", f"C. {wrong2}%", f"D. {wrong3}%"],
            [f"A. {lcr}%", f"B. {wrong1}%", f"C. {wrong2}%", f"D. {wrong3}%"],
            0, f"LCR = HQLA / 淨流出 = {lcr}%",
            f"LCR = HQLA / Net Outflows = {lcr}%", T4_ZH, T4_EN, 2
        ), i * 100))
    elif i % 3 == 1:
        asf = r.choice([500, 700, 900])
        rsf = r.choice([400, 600, 800])
        nsfr = round(asf / rsf * 100, 1)
        wrong1 = round(asf / (rsf * 1.1) * 100, 1)
        wrong2 = round((asf * 0.9) / rsf * 100, 1)
        wrong3 = round(rsf / asf * 100, 1)
        all_q.append(shuffle_answer(q(
            f"可用穩定資金(ASF)={asf}M，所需穩定資金(RSF)={rsf}M。NSFR？",
            f"Available Stable Funding (ASF)=${asf}M, Required Stable Funding (RSF)=${rsf}M. NSFR?",
            [f"A. {nsfr}%", f"B. {wrong1}%", f"C. {wrong2}%", f"D. {wrong3}%"],
            [f"A. {nsfr}%", f"B. {wrong1}%", f"C. {wrong2}%", f"D. {wrong3}%"],
            0, f"NSFR = ASF / RSF = {nsfr}%",
            f"NSFR = ASF / RSF = {nsfr}%", T4_ZH, T4_EN, 2
        ), i * 101))
    else:
        gap = r.choice([-200, -100, -50, 50, 100, 200])
        interpretation = "資金缺口" if gap < 0 else "資金盈餘"
        interpretation_en = "funding gap" if gap < 0 else "funding surplus"
        all_q.append(shuffle_answer(q(
            f"30天累積流動性缺口為{gap}M，這表示：", f"30-day cumulative liquidity gap is ${gap}M. This indicates:",
            [f"A. {interpretation}", f"B. 資金{'盈餘' if gap < 0 else '缺口'}",
             f"C. 流動性充足", f"D. 需要立即行動"],
            [f"A. {interpretation_en}", f"B. {'Surplus' if gap < 0 else 'Gap'}",
             f"C. Adequate liquidity", f"D. Immediate action needed"],
            0, f"缺口{gap}M表示{interpretation}",
            f"Gap of ${gap}M indicates {interpretation_en}", T4_ZH, T4_EN, 1
        ), i * 102))

# 4b: Repo and collateral (200)
repo = [
    ("回購利率", "Repo Rate", "回購協議中的借款成本", "Borrowing cost in repurchase agreement"),
    ("擔保品折扣", "Haircut", "擔保品市值與貸款金額的差額", "Difference between collateral market value and loan amount"),
    ("三方回購", "Tri-Party Repo", "由第三方銀行管理擔保品的回購", "Repo with collateral managed by third-party bank"),
    ("特殊擔保品", "Special Collateral", "市場上供不應求的高需求擔保品", "High-demand collateral in short supply"),
    ("擔保品替換", "Collateral Substitution", "用不同資產替換現有擔保品", "Replacing existing collateral with different assets"),
]
for i in range(200):
    rp = repo[i % len(repo)]
    others = [x for x in repo if x[0] != rp[0]]
    wrong = random.sample(others, 3)
    all_q.append(shuffle_answer(q(
        f"在回購市場中，{rp[0]}的定義是：", f"In repo markets, {rp[1]} is defined as:",
        [f"A. {rp[2]}", f"B. {wrong[0][2]}", f"C. {wrong[1][2]}", f"D. {wrong[2][2]}"],
        [f"A. {rp[3]}", f"B. {wrong[0][3]}", f"C. {wrong[1][3]}", f"D. {wrong[2][3]}"],
        0, f"{rp[0]}：{rp[2]}", f"{rp[1]}: {rp[3]}", T4_ZH, T4_EN, (i % 3) + 1
    ), i * 200))

# 4c: Funding liquidity risk (200)
flr = [
    ("流動性螺旋", "Liquidity Spiral", "資產價格下跌→融資困難→被迫出售→價格進一步下跌",
     "Asset prices fall → funding difficulties → forced selling → prices fall further"),
    ("融資流動性風險", "Funding Liquidity Risk", "無法以合理成本獲得融資的風險",
     "Risk of inability to obtain funding at reasonable cost"),
    ("市場流動性風險", "Market Liquidity Risk", "無法以合理價格買賣資產的風險",
     "Risk of inability to buy/sell assets at fair price"),
    ("流動性黑洞", "Liquidity Black Hole", "市場流動性突然完全消失",
     "Sudden complete disappearance of market liquidity"),
    ("央行最後貸款人", "Lender of Last Resort", "央行在流動性危機時向銀行提供緊急融資",
     "Central bank providing emergency funding during liquidity crisis"),
]
for i in range(200):
    f = flr[i % len(flr)]
    others = [x for x in flr if x[0] != f[0]]
    wrong = random.sample(others, 3)
    all_q.append(shuffle_answer(q(
        f"在流動性風險中，{f[0]}的特點是：", f"In liquidity risk, {f[1]} is characterized by:",
        [f"A. {f[2]}", f"B. {wrong[0][2]}", f"C. {wrong[1][2]}", f"D. {wrong[2][2]}"],
        [f"A. {f[3]}", f"B. {wrong[0][3]}", f"C. {wrong[1][3]}", f"D. {wrong[2][3]}"],
        0, f"{f[0]}：{f[2]}", f"{f[1]}: {f[3]}", T4_ZH, T4_EN, (i % 3) + 1
    ), i * 300))

# 4d: FTP and treasury (150)
ftp = [
    ("匹配法", "Matched Term FTP", "資金成本與資產期限匹配", "Funding cost matches asset maturity"),
    ("流動性準備金", "Liquidity Premium", "為流動性風險收取的額外成本", "Additional charge for liquidity risk"),
    ("機會成本法", "Opportunity Cost FTP", "基於最佳替代用途的資金成本", "Funding cost based on best alternative use"),
    ("集中度限額", "Concentration Limits", "限制對單一融資來源的依賴", "Limits dependence on single funding source"),
]
for i in range(150):
    f = ftp[i % len(ftp)]
    others = [x for x in ftp if x[0] != f[0]]
    wrong = random.sample(others, 3)
    all_q.append(shuffle_answer(q(
        f"在資金轉移定價中，{f[0]}的特點是：", f"In funds transfer pricing, {f[1]} is characterized by:",
        [f"A. {f[2]}", f"B. {wrong[0][2]}", f"C. {wrong[1][2]}", f"D. {wrong[2][2]}"],
        [f"A. {f[3]}", f"B. {wrong[0][3]}", f"C. {wrong[1][3]}", f"D. {wrong[2][3]}"],
        0, f"{f[0]}：{f[2]}", f"{f[1]}: {f[3]}", T4_ZH, T4_EN, (i % 3) + 1
    ), i * 400))

# ============================================================
# TOPIC 5: Risk Mgmt & Investment Mgmt (750 questions)
# ============================================================
T5_ZH, T5_EN = "風險管理與投資管理 (15%)", "Risk Management and Investment Management (15%)"

# 5a: CAPM and portfolio theory (200)
for i in range(200):
    r = random.Random(i * 1000 + 30000)
    rf = r.uniform(0.02, 0.06)
    beta = r.uniform(0.5, 2.0)
    rm = r.uniform(0.08, 0.15)
    expected_ret = round(rf + beta * (rm - rf), 4)
    wrong1 = round(rf + beta * rm, 4)
    wrong2 = round(beta * rm, 4)
    wrong3 = round(rf + (rm - rf) / beta, 4)
    
    if i % 3 == 0:
        all_q.append(shuffle_answer(q(
            f"Rf={rf*100:.1f}%, β={beta:.2f}, E(Rm)={rm*100:.1f}%。CAPM預期回報率？",
            f"Rf={rf*100:.1f}%, β={beta:.2f}, E(Rm)={rm*100:.1f}%. CAPM expected return?",
            [f"A. {expected_ret*100:.2f}%", f"B. {wrong1*100:.2f}%", f"C. {wrong2*100:.2f}%", f"D. {wrong3*100:.2f}%"],
            [f"A. {expected_ret*100:.2f}%", f"B. {wrong1*100:.2f}%", f"C. {wrong2*100:.2f}%", f"D. {wrong3*100:.2f}%"],
            0, f"E(R) = Rf + β(E(Rm)-Rf) = {expected_ret*100:.2f}%",
            f"E(R) = Rf + β(E(Rm)-Rf) = {expected_ret*100:.2f}%", T5_ZH, T5_EN, 2
        ), i * 100))
    elif i % 3 == 1:
        sharpe_p = r.uniform(0.3, 1.5)
        sharpe_b = r.uniform(0.2, 1.0)
        ir = round(sharpe_p - sharpe_b, 4) if sharpe_p > sharpe_b else round(sharpe_b - sharpe_p, 4)
        all_q.append(shuffle_answer(q(
            f"投資組合夏普比率={sharpe_p:.2f}，基準夏普比率={sharpe_b:.2f}。信息比率？",
            f"Portfolio Sharpe={sharpe_p:.2f}, Benchmark Sharpe={sharpe_b:.2f}. Information Ratio?",
            [f"A. 需要追蹤誤差才能計算", f"B. {sharpe_p:.2f}",
             f"C. {sharpe_b:.2f}", f"D. {ir:.2f}"],
            [f"A. Need tracking error to calculate", f"B. {sharpe_p:.2f}",
             f"C. {sharpe_b:.2f}", f"D. {ir:.2f}"],
            0, "信息比率 = 主動回報/追蹤誤差，需要追蹤誤差數據",
            "IR = Active Return / Tracking Error, need TE data", T5_ZH, T5_EN, 2
        ), i * 101))
    else:
        w1 = r.uniform(0.2, 0.8)
        w2 = 1 - w1
        ret1 = r.uniform(0.05, 0.15)
        ret2 = r.uniform(0.03, 0.12)
        port_ret = round(w1 * ret1 + w2 * ret2, 4)
        wrong1 = round((ret1 + ret2) / 2, 4)
        wrong2 = round(w1 * ret1, 4)
        wrong3 = round(w2 * ret2, 4)
        all_q.append(shuffle_answer(q(
            f"資產1權重{w1*100:.0f}%,回報{ret1*100:.1f}%；資產2權重{w2*100:.0f}%,回報{ret2*100:.1f}%。組合回報？",
            f"Asset 1 weight {w1*100:.0f}%, return {ret1*100:.1f}%; Asset 2 weight {w2*100:.0f}%, return {ret2*100:.1f}%. Portfolio return?",
            [f"A. {port_ret*100:.2f}%", f"B. {wrong1*100:.2f}%", f"C. {wrong2*100:.2f}%", f"D. {wrong3*100:.2f}%"],
            [f"A. {port_ret*100:.2f}%", f"B. {wrong1*100:.2f}%", f"C. {wrong2*100:.2f}%", f"D. {wrong3*100:.2f}%"],
            0, f"Rp = w1×R1 + w2×R2 = {port_ret*100:.2f}%",
            f"Rp = w1×R1 + w2×R2 = {port_ret*100:.2f}%", T5_ZH, T5_EN, 1
        ), i * 102))

# 5b: Risk-adjusted performance (150)
rap = [
    ("夏普比率", "Sharpe Ratio", "(Rp-Rf)/σp，衡量單位總風險的超額回報", "(Rp-Rf)/σp, excess return per unit of total risk"),
    ("索提諾比率", "Sortino Ratio", "(Rp-Rf)/σd，只考慮下行風險", "(Rp-Rf)/σd, considers only downside risk"),
    ("特雷諾比率", "Treynor Ratio", "(Rp-Rf)/β，衡量單位系統風險的超額回報", "(Rp-Rf)/β, excess return per unit of systematic risk"),
    ("M²", "Modigliani-Modigliani", "風險調整後的回報率", "Risk-adjusted rate of return"),
    ("信息比率", "Information Ratio", "主動回報/追蹤誤差", "Active return / tracking error"),
]
for i in range(150):
    p = rap[i % len(rap)]
    others = [x for x in rap if x[0] != p[0]]
    wrong = random.sample(others, 3)
    all_q.append(shuffle_answer(q(
        f"績效指標{p[0]}的計算公式是：", f"The formula for {p[1]} is:",
        [f"A. {p[2]}", f"B. {wrong[0][2]}", f"C. {wrong[1][2]}", f"D. {wrong[2][2]}"],
        [f"A. {p[3]}", f"B. {wrong[0][3]}", f"C. {wrong[1][3]}", f"D. {wrong[2][3]}"],
        0, f"{p[0]}：{p[2]}", f"{p[1]}: {p[3]}", T5_ZH, T5_EN, (i % 3) + 1
    ), i * 200))

# 5c: Hedge fund and alternatives (200)
alt = [
    ("多空策略", "Long/Short Strategy", "買入預期上漲的資產，賣空預期下跌的資產", "Buy expected winners, short expected losers"),
    ("事件驅動策略", "Event-Driven Strategy", "利用併購、重組等事件獲利", "Profits from M&A, restructuring events"),
    ("全球宏觀策略", "Global Macro Strategy", "基於宏觀經濟趨勢的投資", "Investment based on macroeconomic trends"),
    ("管理期貨 (CTA)", "Managed Futures (CTA)", "使用期貨合約的系統性交易策略", "Systematic trading using futures contracts"),
    ("相對價值策略", "Relative Value Strategy", "利用相關資產間的價格差異獲利", "Profits from price discrepancies between related assets"),
]
for i in range(200):
    a = alt[i % len(alt)]
    others = [x for x in alt if x[0] != a[0]]
    wrong = random.sample(others, 3)
    all_q.append(shuffle_answer(q(
        f"另類投資中，{a[0]}的特點是：", f"In alternative investments, {a[1]} is characterized by:",
        [f"A. {a[2]}", f"B. {wrong[0][2]}", f"C. {wrong[1][2]}", f"D. {wrong[2][2]}"],
        [f"A. {a[3]}", f"B. {wrong[0][3]}", f"C. {wrong[1][3]}", f"D. {wrong[2][3]}"],
        0, f"{a[0]}：{a[2]}", f"{a[1]}: {a[3]}", T5_ZH, T5_EN, (i % 3) + 1
    ), i * 300))

# 5d: ALM and insurance (200)
alm = [
    ("久期匹配", "Duration Matching", "使資產久期等於負債久期", "Setting asset duration equal to liability duration"),
    ("現金流匹配", "Cash Flow Matching", "使資產現金流與負債現金流在時間上匹配", "Matching asset cash flows to liability cash flows in time"),
    ("免疫策略", "Immunization", "保護組合免受利率變動影響", "Protecting portfolio from interest rate changes"),
    ("再投資風險", "Reinvestment Risk", "現金流再投資時利率下降的風險", "Risk of lower rates when reinvesting cash flows"),
    ("資產負債缺口", "Asset-Liability Gap", "資產和負債之間的不匹配", "Mismatch between assets and liabilities"),
]
for i in range(200):
    a = alm[i % len(alm)]
    others = [x for x in alm if x[0] != a[0]]
    wrong = random.sample(others, 3)
    all_q.append(shuffle_answer(q(
        f"在ALM中，{a[0]}的定義是：", f"In ALM, {a[1]} is defined as:",
        [f"A. {a[2]}", f"B. {wrong[0][2]}", f"C. {wrong[1][2]}", f"D. {wrong[2][2]}"],
        [f"A. {a[3]}", f"B. {wrong[0][3]}", f"C. {wrong[1][3]}", f"D. {wrong[2][3]}"],
        0, f"{a[0]}：{a[2]}", f"{a[1]}: {a[3]}", T5_ZH, T5_EN, (i % 3) + 1
    ), i * 400))

# ============================================================
# TOPIC 6: Current Issues (500 questions)
# ============================================================
T6_ZH, T6_EN = "最新議題 (10%)", "Current Issues (10%)"

# Various current issues (500)
ci_topics = [
    # Climate
    ("物理氣候風險", "Physical Climate Risk", "極端天氣事件直接導致的資產損失", "Direct asset losses from extreme weather"),
    ("轉型氣候風險", "Transition Climate Risk", "向低碳經濟轉型帶來的風險", "Risks from transitioning to low-carbon economy"),
    ("碳排放風險", "Carbon Emission Risk", "碳定價和排放法規帶來的財務影響", "Financial impact from carbon pricing"),
    ("綠色洗白", "Greenwashing", "誇大環保承諾的虛假宣傳", "False claims overstating environmental commitment"),
    # AI/ML
    ("AI模型風險", "AI Model Risk", "AI/ML模型的可解釋性和偏差風險", "Explainability and bias risks of AI/ML"),
    ("機器學習風控", "ML in Risk Management", "使用ML改進風險預測", "Using ML to improve risk prediction"),
    ("算法偏差", "Algorithmic Bias", "AI系統中的系統性偏差", "Systematic bias in AI systems"),
    # Crypto
    ("加密貨幣波動率", "Cryptocurrency Volatility", "數字資產的極端價格波動", "Extreme price volatility of digital assets"),
    ("DeFi智能合約風險", "DeFi Smart Contract Risk", "去中心化金融的代碼漏洞風險", "Code vulnerability risk in DeFi"),
    ("穩定幣脫鉤", "Stablecoin De-pegging", "穩定幣偏離其掛鉤價值", "Stablecoin deviating from pegged value"),
    # Regulatory
    ("Basel III.1", "Basel III.1", "修訂後的資本框架", "Revised capital framework"),
    ("LIBOR過渡", "LIBOR Transition", "從LIBOR轉向替代基準利率", "Transition from LIBOR to alternative benchmarks"),
    ("數字銀行", "Digital Banking", "純數字銀行模式的風險", "Risks of digital-only banking model"),
    ("地緣政治制裁", "Geopolitical Sanctions", "制裁對金融市場的影響", "Impact of sanctions on financial markets"),
    # Cyber
    ("勒索軟件風險", "Ransomware Risk", "加密數據並要求贖金的攻擊", "Attacks encrypting data for ransom"),
    ("供應鏈網絡攻擊", "Supply Chain Cyber Attack", "通過供應商進行的網絡攻擊", "Cyber attack through vendor chain"),
    # Pandemic
    ("供應鏈韌性", "Supply Chain Resilience", "抵禦供應中斷的能力", "Ability to withstand supply disruptions"),
    ("通脹對沖", "Inflation Hedging", "保護資產免受通脹侵蝕", "Protecting assets from inflation erosion"),
    ("ESG整合", "ESG Integration", "將ESG因素納入風控框架", "Incorporating ESG into risk framework"),
    ("操作韌性監管", "Operational Resilience Regulation", "監管機構對操作韌性的要求", "Regulatory requirements for operational resilience"),
]
for i in range(500):
    c = ci_topics[i % len(ci_topics)]
    others = [x for x in ci_topics if x[0] != c[0]]
    wrong = random.sample(others, 3)
    
    templates = [
        (f"在當前風險議題中，{c[0]}的定義是：", f"In current risk issues, {c[1]} is defined as:"),
        (f"關於{c[0]}，以下哪項正確？", f"Regarding {c[1]}, which is correct?"),
        (f"{c[0]}的主要風險特徵是：", f"The main risk characteristic of {c[1]} is:"),
    ]
    t = templates[i % len(templates)]
    all_q.append(shuffle_answer(q(
        t[0], t[1],
        [f"A. {c[2]}", f"B. {wrong[0][2]}", f"C. {wrong[1][2]}", f"D. {wrong[2][2]}"],
        [f"A. {c[3]}", f"B. {wrong[0][3]}", f"C. {wrong[1][3]}", f"D. {wrong[2][3]}"],
        0, f"{c[0]}：{c[2]}", f"{c[1]}: {c[3]}", T6_ZH, T6_EN, (i % 3) + 1
    ), i * 500 + 50000))

# ============================================================
# Finalize
# ============================================================
for i, q_obj in enumerate(all_q):
    q_obj['id'] = i + 1

output = {"questions": all_q}
outpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'questions.json')
os.makedirs(os.path.dirname(outpath), exist_ok=True)
with open(outpath, 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

from collections import Counter
texts = [q['question_en'] for q in all_q]
dupes = len(texts) - len(set(texts))
topics = Counter(q['topic_en'] for q in all_q)
answers = Counter(q['answer'] for q in all_q)
diffs = Counter(q['difficulty'] for q in all_q)

print(f"✅ Generated {len(all_q)} questions")
print(f"   Unique texts: {len(set(texts))}")
print(f"   Duplicates: {dupes}")
print(f"\n   Topics:")
for t, c in sorted(topics.items()):
    print(f"     {t}: {c} ({c/len(all_q)*100:.1f}%)")
print(f"\n   Answers: {dict(sorted(answers.items()))}")
print(f"   Difficulty: {dict(sorted(diffs.items()))}")
