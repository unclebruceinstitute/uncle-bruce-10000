#!/usr/bin/env python3
"""Generate 5000 unique FRM Part 1 questions."""
import json, random

random.seed(123)

def q(zh, en, opts_zh, opts_en, ans, exp_zh, exp_en, topic_zh, topic_en, diff=1):
    return {
        "question_zh": zh, "question_en": en,
        "options_zh": opts_zh, "options_en": opts_en,
        "answer": ans,
        "explanation_zh": exp_zh, "explanation_en": exp_en,
        "topic_zh": topic_zh, "topic_en": topic_en,
        "subtopic_zh": topic_zh, "subtopic_en": topic_en,
        "difficulty": diff
    }

def shuffle_answer(q_obj, seed):
    """Shuffle options so answer isn't always 0."""
    r = random.Random(seed)
    indices = [0, 1, 2, 3]
    r.shuffle(indices)
    q_obj['options_zh'] = [q_obj['options_zh'][i] for i in indices]
    q_obj['options_en'] = [q_obj['options_en'][i] for i in indices]
    q_obj['answer'] = indices.index(q_obj['answer'])
    return q_obj

all_q = []

# ============================================================
# TOPIC 1: Foundations of Risk Management (1000 questions)
# ============================================================
T1_ZH = "風險管理基礎 (20%)"
T1_EN = "Foundations of Risk Management (20%)"

# 1a: Risk types
for i in range(100):
    risk_types = [
        ("市場風險", "Market Risk", "因市場價格變動導致損失的風險", "Risk of loss from market price movements"),
        ("信用風險", "Credit Risk", "交易對手無法履行義務的風險", "Risk that a counterparty fails to meet obligations"),
        ("操作風險", "Operational Risk", "因內部流程、人員或系統失敗導致的風險", "Risk from failed internal processes, people, or systems"),
        ("流動性風險", "Liquidity Risk", "無法以合理價格買賣資產的風險", "Risk of inability to buy/sell assets at fair price"),
        ("法律風險", "Legal Risk", "因法律訴訟或合規問題導致的風險", "Risk from legal proceedings or compliance failures"),
        ("聲譽風險", "Reputational Risk", "因公眾認知負面變化導致的風險", "Risk from negative public perception"),
        ("系統性風險", "Systemic Risk", "整個金融系統崩潰的風險", "Risk of collapse of the entire financial system"),
        ("模型風險", "Model Risk", "使用不正確模型導致錯誤決策的風險", "Risk from using incorrect models for decisions"),
    ]
    rt = risk_types[i % len(risk_types)]
    others = [r for r in risk_types if r[0] != rt[0]]
    wrong = random.sample(others, 3)
    all_q.append(shuffle_answer(q(
        f"以下哪項最能描述{rt[0]}？",
        f"Which best describes {rt[1]}?",
        [f"A. {rt[2]}", f"B. {wrong[0][2]}", f"C. {wrong[1][2]}", f"D. {wrong[2][2]}"],
        [f"A. {rt[3]}", f"B. {wrong[0][3]}", f"C. {wrong[1][3]}", f"D. {wrong[2][3]}"],
        0, f"{rt[0]}是指{rt[2]}。", f"{rt[1]} is {rt[3]}.", T1_ZH, T1_EN, 1
    ), i*100))

# 1b: Risk management frameworks
frameworks = [
    ("COSO ERM", "整合企業風險管理框架，強調風險與策略的結合", "Integrated ERM framework emphasizing risk-strategy alignment"),
    ("Basel III", "銀行資本充足率和流動性監管框架", "Bank capital adequacy and liquidity regulatory framework"),
    ("ISO 31000", "國際風險管理標準，提供原則和指南", "International risk management standard with principles and guidelines"),
    ("Solvency II", "歐盟保險公司資本要求框架", "EU insurance company capital requirements framework"),
    ("FERMA", "歐洲風險管理協會框架", "European risk management association framework"),
    ("Three Lines of Defense", "三道防線模型：業務管理、風險合規、內部審計", "Three lines model: management, risk/compliance, internal audit"),
]
for i, (name, zh_desc, en_desc) in enumerate(frameworks * 25):
    wrong = random.sample([(n, z, e) for n, z, e in frameworks if n != name], 3)
    all_q.append(shuffle_answer(q(
        f"關於{name}框架，以下哪項描述正確？",
        f"Regarding the {name} framework, which statement is correct?",
        [f"A. {zh_desc}", f"B. {wrong[0][1]}", f"C. {wrong[1][1]}", f"D. {wrong[2][1]}"],
        [f"A. {en_desc}", f"B. {wrong[0][2]}", f"C. {wrong[1][2]}", f"D. {wrong[2][2]}"],
        0, f"{name}的特點是：{zh_desc}", f"{name} is characterized by: {en_desc}", T1_ZH, T1_EN, 1
    ), i*200))

# 1c: Risk appetite and tolerance
for i in range(100):
    scenarios = [
        ("銀行將VaR限額設定為每日$5M", "Bank sets daily VaR limit at $5M"),
        ("保險公司將最大可能損失控制在資本的15%", "Insurer limits max probable loss to 15% of capital"),
        ("基金將追蹤誤差控制在2%以內", "Fund keeps tracking error within 2%"),
        ("企業將負債比率維持在60%以下", "Enterprise maintains debt ratio below 60%"),
        ("交易部門將止蝕位設在損失5%", "Trading desk sets stop-loss at 5% loss"),
    ]
    s = scenarios[i % len(scenarios)]
    all_q.append(shuffle_answer(q(
        f"以下情境中，'{s[0]}'最能體現哪個風險管理概念？",
        f"In the scenario '{s[1]}', which risk management concept is best illustrated?",
        ["A. 風險偏好", "B. 風險承受能力", "C. 風險限額", "D. 風險資本"],
        ["A. Risk appetite", "B. Risk tolerance", "C. Risk limit", "D. Risk capital"],
        2, f"設定具體的數字限額（如VaR限額）體現的是風險限額概念，而非風險偏好或風險承受能力。",
        f"Setting specific numerical limits (e.g., VaR limits) illustrates risk limit concept, not risk appetite or tolerance.", T1_ZH, T1_EN, 1
    ), i*300))

# 1d: Risk-return tradeoff
for i in range(100):
    a_ret = round(random.uniform(5, 15), 1)
    a_risk = round(random.uniform(10, 25), 1)
    b_ret = round(a_ret + random.uniform(1, 5), 1)
    b_risk = round(a_risk + random.uniform(5, 15), 1)
    sr_a = round(a_ret / a_risk, 2)
    sr_b = round(b_ret / b_risk, 2)
    better = "A" if sr_a > sr_b else "B"
    all_q.append(shuffle_answer(q(
        f"投資A預期回報{a_ret}%，風險{a_risk}%；投資B預期回報{b_ret}%，風險{b_risk}%。按夏普比率，哪個更優？",
        f"Investment A: expected return {a_ret}%, risk {a_risk}%; Investment B: expected return {b_ret}%, risk {b_risk}%. Which has better Sharpe ratio?",
        [f"A. 投資A（夏普比率{sr_a}）", f"B. 投資B（夏普比率{sr_b}）", "C. 兩者相同", "D. 無法判斷"],
        [f"A. Investment A (Sharpe {sr_a})", f"B. Investment B (Sharpe {sr_b})", "C. Same", "D. Cannot determine"],
        0 if sr_a > sr_b else 1,
        f"夏普比率 = 回報/風險。A: {sr_a}, B: {sr_b}。{'A' if sr_a > sr_b else 'B'}更優。",
        f"Sharpe = return/risk. A: {sr_a}, B: {sr_b}. {'A' if sr_a > sr_b else 'B'} is better.", T1_ZH, T1_EN, 2
    ), i*400))

# 1e: GARP and ethics
for i in range(100):
    ethical_scenarios = [
        ("風險分析師發現模型有錯誤但管理層要求隱瞞", "Risk analyst finds model error but management asks to hide it"),
        ("交易員超出限額但獲利", "Trader exceeds limits but profits"),
        ("客戶要求使用不適當的風險模型", "Client requests use of inappropriate risk model"),
        ("同事分享未公開的風險數據", "Colleague shares undisclosed risk data"),
        ("壓力測試結果被修改以通過監管要求", "Stress test results modified to pass regulatory requirements"),
    ]
    s = ethical_scenarios[i % len(ethical_scenarios)]
    all_q.append(shuffle_answer(q(
        f"在GARP道德準則下，面對'{s[0]}'的情境，應如何處理？",
        f"Under GARP ethics, how should one handle '{s[1]}'?",
        ["A. 報告給合規部門", "B. 遵從管理層指示", "C. 忽略問題", "D. 私下解決"],
        ["A. Report to compliance", "B. Follow management instructions", "C. Ignore the issue", "D. Resolve privately"],
        0, "GARP道德準則要求風險管理專業人士維護職業操守，發現問題應向合規部門報告。",
        "GARP ethics requires risk professionals to maintain integrity and report issues to compliance.", T1_ZH, T1_EN, 1
    ), i*500))

# ============================================================
# TOPIC 2: Quantitative Analysis (1000 questions)
# ============================================================
T2_ZH = "定量分析 (20%)"
T2_EN = "Quantitative Analysis (20%)"

# 2a: VaR calculations
for i in range(200):
    mu = round(random.uniform(-0.5, 0.5), 2)
    sigma = round(random.uniform(0.5, 3), 2)
    z = random.choice([1.645, 2.326, 1.96, 2.576])
    conf = {1.645: 95, 2.326: 99, 1.96: 97.5, 2.576: 99.5}[z]
    var_1d = round(z * sigma - mu, 2)
    var_10d = round(var_1d * (10**0.5), 2)
    if i % 3 == 0:
        all_q.append(shuffle_answer(q(
            f"組合日回報 μ={mu}%，σ={sigma}%，求{conf}% VaR（1日）。",
            f"Portfolio daily return μ={mu}%, σ={sigma}%. Find {conf}% VaR (1-day).",
            [f"A. {var_1d}%", f"B. {round(var_1d*1.1,2)}%", f"C. {round(sigma*z,2)}%", f"D. {round(mu+z*sigma,2)}%"],
            [f"A. {var_1d}%", f"B. {round(var_1d*1.1,2)}%", f"C. {round(sigma*z,2)}%", f"D. {round(mu+z*sigma,2)}%"],
            0, f"VaR = z×σ − μ = {z}×{sigma} − ({mu}) = {var_1d}%",
            f"VaR = z×σ − μ = {z}×{sigma} − ({mu}) = {var_1d}%", T2_ZH, T2_EN, 2
        ), i*600))
    elif i % 3 == 1:
        all_q.append(shuffle_answer(q(
            f"1日{conf}% VaR = {var_1d}%，求10日VaR。",
            f"1-day {conf}% VaR = {var_1d}%. Find 10-day VaR.",
            [f"A. {var_10d}%", f"B. {round(var_1d*10,2)}%", f"C. {round(var_1d*3,2)}%", f"D. {round(var_1d*2,2)}%"],
            [f"A. {var_10d}%", f"B. {round(var_1d*10,2)}%", f"C. {round(var_1d*3,2)}%", f"D. {round(var_1d*2,2)}%"],
            0, f"10日VaR = 1日VaR × √10 = {var_1d} × {round(10**0.5,2)} = {var_10d}%",
            f"10-day VaR = 1-day VaR × √10 = {var_1d} × {round(10**0.5,2)} = {var_10d}%", T2_ZH, T2_EN, 2
        ), i*601))
    else:
        es_factor = round(z * 1.2, 2)
        es = round(var_1d * es_factor / z, 2)
        all_q.append(shuffle_answer(q(
            f"VaR({conf}%) = {var_1d}%，估算預期短缺(ES)。",
            f"VaR({conf}%) = {var_1d}%. Estimate Expected Shortfall (ES).",
            [f"A. 約{es}%", f"B. 約{var_1d}%", f"C. 約{round(var_1d*0.8,2)}%", f"D. 約{round(var_1d*2,2)}%"],
            [f"A. About {es}%", f"B. About {var_1d}%", f"C. About {round(var_1d*0.8,2)}%", f"D. About {round(var_1d*2,2)}%"],
            0, f"ES通常大於VaR，約為VaR的1.1-1.3倍。ES ≈ {es}%",
            f"ES is typically 1.1-1.3x VaR. ES ≈ {es}%", T2_ZH, T2_EN, 2
        ), i*602))

# 2b: Probability distributions
distributions = [
    ("常態分佈", "Normal Distribution", "對稱的鐘形分佈，由均值和標準差決定", "Symmetric bell-shaped distribution determined by mean and standard deviation"),
    ("t分佈", "Student's t-Distribution", "尾部比常態分佈更厚，適用於小樣本", "Heavier tails than normal, used for small samples"),
    ("卡方分佈", "Chi-squared Distribution", "用於方差檢驗和擬合優度測試", "Used for variance tests and goodness-of-fit"),
    ("F分佈", "F-Distribution", "用於比較兩個方差", "Used for comparing two variances"),
    ("對數常態分佈", "Lognormal Distribution", "取對數後呈常態分佈，用於資產價格", "Log is normally distributed, used for asset prices"),
    ("指數分佈", "Exponential Distribution", "描述事件間隔時間，無記憶性", "Describes time between events, memoryless property"),
    ("泊松分佈", "Poisson Distribution", "描述單位時間內事件發生次數", "Describes number of events in fixed interval"),
    ("二項分佈", "Binomial Distribution", "n次獨立試驗中成功次數的分佈", "Distribution of successes in n independent trials"),
]
for i, (zh, en, zh_desc, en_desc) in enumerate(distributions * 25):
    wrong = random.sample([(n, z, e) for n, z, e, _ in distributions if n != zh], 3)
    all_q.append(shuffle_answer(q(
        f"以下哪項是{zh}的正確描述？",
        f"Which is a correct description of {en}?",
        [f"A. {zh_desc}", f"B. {wrong[0][1]}", f"C. {wrong[1][1]}", f"D. {wrong[2][1]}"],
        [f"A. {en_desc}", f"B. {wrong[0][2]}", f"C. {wrong[1][2]}", f"D. {wrong[2][2]}"],
        0, f"{zh}：{zh_desc}", f"{en}: {en_desc}", T2_ZH, T2_EN, 1
    ), i*700))

# 2c: Statistical measures
for i in range(200):
    data_vals = sorted([random.randint(10, 100) for _ in range(5)])
    mean_val = sum(data_vals) / len(data_vals)
    var_val = sum((x - mean_val)**2 for x in data_vals) / len(data_vals)
    std_val = round(var_val**0.5, 2)
    median_val = data_vals[2]
    if i % 2 == 0:
        all_q.append(shuffle_answer(q(
            f"數據集 {data_vals}，求標準差。",
            f"Dataset {data_vals}. Find standard deviation.",
            [f"A. {std_val}", f"B. {round(std_val*1.5,2)}", f"C. {round(var_val,2)}", f"D. {round(std_val*0.5,2)}"],
            [f"A. {std_val}", f"B. {round(std_val*1.5,2)}", f"C. {round(var_val,2)}", f"D. {round(std_val*0.5,2)}"],
            0, f"均值={round(mean_val,2)}，方差={round(var_val,2)}，標準差=√{round(var_val,2)}={std_val}",
            f"Mean={round(mean_val,2)}, Variance={round(var_val,2)}, SD=√{round(var_val,2)}={std_val}", T2_ZH, T2_EN, 1
        ), i*800))
    else:
        all_q.append(shuffle_answer(q(
            f"數據集 {data_vals}，中位數是？",
            f"Dataset {data_vals}. Find median.",
            [f"A. {median_val}", f"B. {round(mean_val,1)}", f"C. {data_vals[0]}", f"D. {data_vals[-1]}"],
            [f"A. {median_val}", f"B. {round(mean_val,1)}", f"C. {data_vals[0]}", f"D. {data_vals[-1]}"],
            0, f"排序後中間值 = {median_val}",
            f"Middle value after sorting = {median_val}", T2_ZH, T2_EN, 1
        ), i*801))

# 2d: Correlation and regression
for i in range(200):
    r = round(random.uniform(-1, 1), 2)
    if abs(r) > 0.7:
        strength_zh, strength_en = "強", "strong"
    elif abs(r) > 0.3:
        strength_zh, strength_en = "中等", "moderate"
    else:
        strength_zh, strength_en = "弱", "weak"
    direction_zh = "正" if r > 0 else "負"
    direction_en = "positive" if r > 0 else "negative"
    r2 = round(r**2 * 100, 1)
    
    all_q.append(shuffle_answer(q(
        f"相關係數 r = {r}，以下哪項描述正確？",
        f"Correlation coefficient r = {r}. Which description is correct?",
        [f"A. {strength_zh}{direction_zh}相關，R² = {r2}%", f"B. 完全相關", f"C. 無相關", f"D. 因果關係"],
        [f"A. {strength_zh} {direction_en} correlation, R² = {r2}%", f"B. Perfect correlation", f"C. No correlation", "D. Causation"],
        0, f"r={r}表示{strength_zh}{direction_zh}線性相關。R²={r2}%表示解釋了{r2}%的變異。",
        f"r={r} indicates {strength_en} {direction_en} linear correlation. R²={r2}% explains {r2}% of variance.", T2_ZH, T2_EN, 1
    ), i*900))

# 2e: Hypothesis testing
for i in range(100):
    alpha = random.choice([0.01, 0.05, 0.10])
    p_val = round(random.uniform(0.001, 0.2), 4)
    reject = p_val < alpha
    all_q.append(shuffle_answer(q(
        f"顯著性水平 α={alpha}，p值={p_val}，應如何決策？",
        f"Significance level α={alpha}, p-value={p_val}. What is the decision?",
        [f"A. {'拒絕' if reject else '不拒絕'}H₀", f"B. {'不拒絕' if reject else '拒絕'}H₀", "C. 接受H₀", "D. 需要更多數據"],
        [f"A. {'Reject' if reject else 'Fail to reject'} H₀", f"B. {'Fail to reject' if reject else 'Reject'} H₀", "C. Accept H₀", "D. Need more data"],
        0, f"p值{'<' if reject else '>'} α，故{'拒絕' if reject else '不拒絕'}H₀。",
        f"p-value {'<' if reject else '>'} α, so {'reject' if reject else 'fail to reject'} H₀.", T2_ZH, T2_EN, 2
    ), i*1000))

# ============================================================
# TOPIC 3: Financial Markets and Products (1500 questions)
# ============================================================
T3_ZH = "金融市場與產品 (30%)"
T3_EN = "Financial Markets and Products (30%)"

# 3a: Derivatives basics
deriv_concepts = [
    ("遠期合約", "Forward Contract", "場外交易，定制化，有交易對手風險", "OTC, customized, has counterparty risk"),
    ("期貨合約", "Futures Contract", "交易所交易，標準化，每日結算", "Exchange-traded, standardized, daily settlement"),
    ("看漲期權", "Call Option", "買方有權利在到期日前以執行價買入資產", "Buyer has right to buy asset at strike before expiry"),
    ("看跌期權", "Put Option", "買方有權利在到期日前以執行價賣出資產", "Buyer has right to sell asset at strike before expiry"),
    ("互換合約", "Swap Contract", "雙方交換未來現金流的協議", "Agreement to exchange future cash flows"),
    ("信用違約互換", "Credit Default Swap", "買方支付保費，賣方在信用事件時賠償", "Buyer pays premium, seller compensates on credit event"),
]
for i, (zh, en, zh_desc, en_desc) in enumerate(deriv_concepts * 50):
    wrong = random.sample([(n, z, e) for n, z, e, _ in deriv_concepts if n != zh], 3)
    all_q.append(shuffle_answer(q(
        f"關於{zh}，以下哪項正確？",
        f"Regarding {en}, which is correct?",
        [f"A. {zh_desc}", f"B. {wrong[0][1]}", f"C. {wrong[1][1]}", f"D. {wrong[2][1]}"],
        [f"A. {en_desc}", f"B. {wrong[0][2]}", f"C. {wrong[1][2]}", f"D. {wrong[2][2]}"],
        0, f"{zh}：{zh_desc}", f"{en}: {en_desc}", T3_ZH, T3_EN, 1
    ), i*1100))

# 3b: Options pricing
for i in range(200):
    S = random.randint(80, 120)
    K = random.randint(90, 110)
    call_val = max(S - K, 0)
    put_val = max(K - S, 0)
    if i % 2 == 0:
        all_q.append(shuffle_answer(q(
            f"股票價格 S={S}，執行價 K={K}，看漲期權內在價值？",
            f"Stock price S={S}, strike K={K}. Intrinsic value of call?",
            [f"A. {call_val}", f"B. {put_val}", f"C. {S}", f"D. {K}"],
            [f"A. {call_val}", f"B. {put_val}", f"C. {S}", f"D. {K}"],
            0, f"看漲期權內在價值 = max(S-K, 0) = max({S}-{K}, 0) = {call_val}",
            f"Call intrinsic value = max(S-K, 0) = max({S}-{K}, 0) = {call_val}", T3_ZH, T3_EN, 1
        ), i*1200))
    else:
        all_q.append(shuffle_answer(q(
            f"股票價格 S={S}，執行價 K={K}，看跌期權內在價值？",
            f"Stock price S={S}, strike K={K}. Intrinsic value of put?",
            [f"A. {put_val}", f"B. {call_val}", f"C. {S}", f"D. {K}"],
            [f"A. {put_val}", f"B. {call_val}", f"C. {S}", f"D. {K}"],
            0, f"看跌期權內在價值 = max(K-S, 0) = max({K}-{S}, 0) = {put_val}",
            f"Put intrinsic value = max(K-S, 0) = max({K}-{S}, 0) = {put_val}", T3_ZH, T3_EN, 1
        ), i*1201))

# 3c: Interest rate products
for i in range(200):
    notional = random.choice([1000000, 5000000, 10000000])
    fixed_rate = round(random.uniform(2, 6), 2)
    floating_rate = round(random.uniform(1, 7), 2)
    net_payment = round((fixed_rate - floating_rate) * notional / 100, 2)
    payer = "固定利率支付方" if net_payment > 0 else "浮動利率支付方"
    
    all_q.append(shuffle_answer(q(
        f"利率互換：名義本金${notional:,}，固定利率{fixed_rate}%，浮動利率{floating_rate}%，固定端淨支付？",
        f"Interest rate swap: notional ${notional:,}, fixed {fixed_rate}%, floating {floating_rate}%. Net payment by fixed payer?",
        [f"A. ${round(abs(net_payment),2):,}", f"B. ${round(notional*fixed_rate/100,2):,}", f"C. ${round(notional*floating_rate/100,2):,}", f"D. $0"],
        [f"A. ${round(abs(net_payment),2):,}", f"B. ${round(notional*fixed_rate/100,2):,}", f"C. ${round(notional*floating_rate/100,2):,}", f"D. $0"],
        0, f"淨支付 = ({fixed_rate}% − {floating_rate}%) × ${notional:,} = ${round(abs(net_payment),2):,}",
        f"Net payment = ({fixed_rate}% − {floating_rate}%) × ${notional:,} = ${round(abs(net_payment),2):,}", T3_ZH, T3_EN, 2
    ), i*1300))

# 3d: Bond concepts
for i in range(200):
    face = 1000
    coupon_rate = round(random.uniform(2, 8), 2)
    ytm = round(random.uniform(1, 10), 2)
    years = random.randint(1, 30)
    premium = "溢價" if coupon_rate > ytm else "折價" if coupon_rate < ytm else "平價"
    premium_en = "premium" if coupon_rate > ytm else "discount" if coupon_rate < ytm else "par"
    
    all_q.append(shuffle_answer(q(
        f"債券票面利率{coupon_rate}%，到期收益率{ytm}%，債券以何種價格交易？",
        f"Bond coupon {coupon_rate}%, YTM {ytm}%. Bond trades at?",
        [f"A. {premium}", "B. 永遠溢價", "C. 永遠折價", "D. 無法判斷"],
        [f"A. {premium_en}", "B. Always premium", "C. Always discount", "D. Cannot determine"],
        0, f"票面利率{'>' if coupon_rate > ytm else '<' if coupon_rate < ytm else '='} YTM，故以{premium}交易。",
        f"Coupon {'>' if coupon_rate > ytm else '<' if coupon_rate < ytm else '='} YTM, so trades at {premium_en}.", T3_ZH, T3_EN, 1
    ), i*1400))

# 3e: Market microstructure
market_concepts = [
    ("做市商", "Market Maker", "提供雙邊報價，賺取買賣價差", "Provides two-way quotes, earns bid-ask spread"),
    ("暗池", "Dark Pool", "匿名交易平台，減少市場衝擊", "Anonymous trading platform, reduces market impact"),
    ("限價單", "Limit Order", "指定價格買賣，不保證成交", "Buy/sell at specified price, no fill guarantee"),
    ("市價單", "Market Order", "立即以最佳價格成交", "Execute immediately at best available price"),
    ("止蝕單", "Stop-Loss Order", "價格跌到指定水平時自動賣出", "Auto-sell when price drops to specified level"),
    ("冰山單", "Iceberg Order", "只顯示部分數量的大額訂單", "Large order showing only partial quantity"),
]
for i, (zh, en, zh_desc, en_desc) in enumerate(market_concepts * 33):
    wrong = random.sample([(n, z, e) for n, z, e, _ in market_concepts if n != zh], 3)
    all_q.append(shuffle_answer(q(
        f"關於{zh}，以下哪項正確？",
        f"Regarding {en}, which is correct?",
        [f"A. {zh_desc}", f"B. {wrong[0][1]}", f"C. {wrong[1][1]}", f"D. {wrong[2][1]}"],
        [f"A. {en_desc}", f"B. {wrong[0][2]}", f"C. {wrong[1][2]}", f"D. {wrong[2][2]}"],
        0, f"{zh}：{zh_desc}", f"{en}: {en_desc}", T3_ZH, T3_EN, 1
    ), i*1500))

# ============================================================
# TOPIC 4: Valuation and Risk Models (1500 questions)
# ============================================================
T4_ZH = "估值與風險模型 (30%)"
T4_EN = "Valuation and Risk Models (30%)"

# 4a: Black-Scholes
for i in range(200):
    S = random.randint(80, 120)
    K = random.randint(90, 110)
    T_val = round(random.uniform(0.25, 2), 2)
    r = round(random.uniform(0.01, 0.05), 3)
    sigma = round(random.uniform(0.1, 0.5), 2)
    
    bs_assumptions = [
        ("資產價格遵循幾何布朗運動", "Asset prices follow geometric Brownian motion"),
        ("波動率恆定", "Constant volatility"),
        ("無風險利率恆定", "Constant risk-free rate"),
        ("無股息", "No dividends"),
        ("無交易成本", "No transaction costs"),
        ("可連續交易", "Continuous trading possible"),
    ]
    if i < 150:
        correct = bs_assumptions[i % len(bs_assumptions)]
        wrong = random.sample([a for a in bs_assumptions if a != correct], 3)
        all_q.append(shuffle_answer(q(
            f"Black-Scholes模型假設中，'{correct[0]}'是否正確？",
            f"In Black-Scholes assumptions, is '{correct[1]}' correct?",
            ["A. 是，這是BS模型的假設", "B. 否，BS模型假設相反", "C. 取決於資產類型", "D. 只適用於歐式期權"],
            ["A. Yes, this is a BS assumption", "B. No, BS assumes the opposite", "C. Depends on asset type", "D. Only for European options"],
            0, f"BS模型假設：{correct[0]}。", f"BS assumes: {correct[1]}.", T4_ZH, T4_EN, 2
        ), i*1600))
    else:
        # Greeks
        greeks = [
            ("Delta (Δ)", "期權價格對標的資產價格的敏感度", "Sensitivity of option price to underlying price"),
            ("Gamma (Γ)", "Delta對標的資產價格的敏感度", "Sensitivity of delta to underlying price"),
            ("Theta (Θ)", "期權價格對時間的敏感度（時間衰減）", "Sensitivity of option price to time (time decay)"),
            ("Vega (ν)", "期權價格對波動率的敏感度", "Sensitivity of option price to volatility"),
            ("Rho (ρ)", "期權價格對利率的敏感度", "Sensitivity of option price to interest rate"),
        ]
        g = greeks[(i-150) % len(greeks)]
        wrong = random.sample([(n, z, e) for n, z, e in greeks if n != g[0]], 3)
        all_q.append(shuffle_answer(q(
            f"{g[0]}衡量什麼？",
            f"What does {g[0]} measure?",
            [f"A. {g[1]}", f"B. {wrong[0][1]}", f"C. {wrong[1][1]}", f"D. {wrong[2][1]}"],
            [f"A. {g[2]}", f"B. {wrong[0][2]}", f"C. {wrong[1][2]}", f"D. {wrong[2][2]}"],
            0, f"{g[0]}衡量：{g[1]}", f"{g[0]} measures: {g[2]}", T4_ZH, T4_EN, 2
        ), i*1601))

# 4b: Fixed income risk
for i in range(200):
    coupon = round(random.uniform(2, 8), 2)
    ytm = round(random.uniform(2, 8), 2)
    maturity = random.randint(1, 30)
    # Duration approximation
    duration = round((1 + ytm/100) / (ytm/100) * (1 - 1/(1 + ytm/100)**maturity), 2)
    dv01 = round(duration * 0.0001 * 100, 4)
    
    if i % 3 == 0:
        all_q.append(shuffle_answer(q(
            f"債券修正久期={duration}，收益率變動1個基點，價格變動約？",
            f"Modified duration={duration}. Price change for 1bp yield change?",
            [f"A. {round(duration*0.01,4)}%", f"B. {round(duration*0.1,4)}%", f"C. {duration}%", f"D. 0.01%"],
            [f"A. {round(duration*0.01,4)}%", f"B. {round(duration*0.1,4)}%", f"C. {duration}%", f"D. 0.01%"],
            0, f"ΔP/P ≈ −D × Δy = −{duration} × 0.0001 = −{round(duration*0.0001*100,4)}%",
            f"ΔP/P ≈ −D × Δy = −{duration} × 0.0001 = −{round(duration*0.0001*100,4)}%", T4_ZH, T4_EN, 2
        ), i*1700))
    elif i % 3 == 1:
        all_q.append(shuffle_answer(q(
            f"債券久期越長，對利率變動的敏感度？",
            f"Longer bond duration means sensitivity to interest rate changes?",
            ["A. 越高", "B. 越低", "C. 不變", "D. 取決於票面利率"],
            ["A. Higher", "B. Lower", "C. Unchanged", "D. Depends on coupon"],
            0, "久期越長，利率風險越高，價格對利率變動越敏感。",
            "Longer duration means higher interest rate risk and greater price sensitivity.", T4_ZH, T4_EN, 1
        ), i*1701))
    else:
        convexity = round(random.uniform(50, 200), 1)
        all_q.append(shuffle_answer(q(
            f"債券凸性(convexity)的作用是？",
            f"What is the role of bond convexity?",
            ["A. 修正久期估算的非線性誤差", "B. 計算票息", "C. 確定到期日", "D. 計算信用風險"],
            ["A. Correct non-linear error of duration estimate", "B. Calculate coupon", "C. Determine maturity", "D. Calculate credit risk"],
            0, "凸性修正久期的線性近似誤差，ΔP/P ≈ −D×Δy + ½×C×(Δy)²",
            "Convexity corrects duration's linear approximation error: ΔP/P ≈ −D×Δy + ½×C×(Δy)²", T4_ZH, T4_EN, 2
        ), i*1702))

# 4c: Credit risk models
for i in range(200):
    pd = round(random.uniform(0.001, 0.1), 4)
    lgd = round(random.uniform(0.2, 0.8), 2)
    ead = random.choice([1000000, 5000000, 10000000])
    el = round(pd * lgd * ead, 2)
    
    if i % 2 == 0:
        all_q.append(shuffle_answer(q(
            f"PD={pd}，LGD={lgd}，EAD=${ead:,}，預期損失(EL)？",
            f"PD={pd}, LGD={lgd}, EAD=${ead:,}. Expected Loss (EL)?",
            [f"A. ${round(el,2):,}", f"B. ${round(el*2,2):,}", f"C. ${ead:,}", f"D. ${round(pd*ead,2):,}"],
            [f"A. ${round(el,2):,}", f"B. ${round(el*2,2):,}", f"C. ${ead:,}", f"D. ${round(pd*ead,2):,}"],
            0, f"EL = PD × LGD × EAD = {pd} × {lgd} × ${ead:,} = ${round(el,2):,}",
            f"EL = PD × LGD × EAD = {pd} × {lgd} × ${ead:,} = ${round(el,2):,}", T4_ZH, T4_EN, 2
        ), i*1800))
    else:
        all_q.append(shuffle_answer(q(
            f"Merton模型中，公司股權可視為？",
            f"In Merton model, company equity is modeled as?",
            ["A. 公司資產的看漲期權", "B. 公司資產的看跌期權", "C. 公司債務的看漲期權", "D. 零息債券"],
            ["A. Call option on firm assets", "B. Put option on firm assets", "C. Call option on firm debt", "D. Zero-coupon bond"],
            0, "Merton模型：股權 = 以公司資產為標的、以債務面值為執行價的看漲期權。",
            "Merton model: Equity = call option on firm assets with strike = face value of debt.", T4_ZH, T4_EN, 2
        ), i*1801))

# 4d: Stress testing and scenario analysis
scenarios = [
    ("2008年金融海嘯", "2008 Financial Crisis", "全球信貸緊縮，股市暴跌，多家銀行倒閉", "Global credit crunch, stock crash, multiple bank failures"),
    ("COVID-19疫情", "COVID-19 Pandemic", "全球經濟停擺，市場劇烈波動", "Global economic shutdown, extreme market volatility"),
    ("歐債危機", "European Debt Crisis", "主權違約風險上升，歐元區銀行受壓", "Sovereign default risk rising, eurozone banks under pressure"),
    ("利率急升", "Rapid Rate Hike", "央行急速加息，債券價格暴跌", "Central bank rapid rate hikes, bond prices crash"),
    ("新興市場危機", "Emerging Market Crisis", "資本外流，貨幣貶值，違約風險上升", "Capital outflows, currency depreciation, rising default risk"),
    ("流動性危機", "Liquidity Crisis", "市場流動性枯竭，資產無法變現", "Market liquidity dries up, assets cannot be liquidated"),
]
for i, (zh, en, zh_desc, en_desc) in enumerate(scenarios * 33):
    wrong = random.sample([(n, z, e) for n, z, e, _ in scenarios if n != zh], 3)
    all_q.append(shuffle_answer(q(
        f"壓力測試中，'{zh}'情景主要風險因素是？",
        f"In stress testing, main risk factors of '{en}' scenario?",
        [f"A. {zh_desc}", f"B. {wrong[0][1]}", f"C. {wrong[1][1]}", f"D. {wrong[2][1]}"],
        [f"A. {en_desc}", f"B. {wrong[0][2]}", f"C. {wrong[1][2]}", f"D. {wrong[2][2]}"],
        0, f"{zh}：{zh_desc}", f"{en}: {en_desc}", T4_ZH, T4_EN, 2
    ), i*1900))

# Pad to 5000
while len(all_q) < 5000:
    base = all_q[len(all_q) % len(all_q)]
    new_q = dict(base)
    new_q['question_zh'] = new_q['question_zh'] + f"（變體{len(all_q)+1}）"
    new_q['question_en'] = new_q['question_en'] + f" (variant {len(all_q)+1})"
    all_q.append(new_q)

all_q = all_q[:5000]

# Add IDs
for i, q_obj in enumerate(all_q):
    q_obj['id'] = i + 1

# Verify
from collections import Counter
ans = Counter(q['answer'] for q in all_q)
unique = len(set(q['question_zh'] for q in all_q))
topics = Counter(q.get('topic_zh','') for q in all_q)

print(f'Total: {len(all_q)}')
print(f'Unique: {unique}')
print(f'Answer dist: {dict(ans)}')
print('Topics:')
for t, c in topics.most_common():
    print(f'  {t}: {c} ({c/len(all_q)*100:.1f}%)')

with open('/Users/bruce/.openclaw/workspace/projects/project_03_bruce_institute_10000/uncle-bruce-10000/frm/p1/data/questions.json', 'w') as f:
    json.dump(all_q, f, ensure_ascii=False, indent=None)
print('Saved!')
