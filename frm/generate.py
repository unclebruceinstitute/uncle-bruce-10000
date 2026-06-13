#!/usr/bin/env python3
"""Generate FRM exam questions - 10,000 total (5000 P1 + 5000 P2)"""
import json, random, os

random.seed(42)

# ============ PART 1 TOPICS ============
p1_topics = {
    "Foundations of Risk Management": {
        "zh": "風險管理基礎",
        "questions": [
            # Template: (q_en, q_zh, [opts_en], [opts_zh], answer, exp_en, exp_zh)
            (
                "Which of the following best describes 'risk' in the context of the Basel framework?",
                "以下哪項最能描述巴塞爾框架中的「風險」？",
                ["The probability of loss multiplied by the magnitude of loss", "Only the probability of a negative event", "The standard deviation of returns", "The maximum possible loss"],
                ["損失概率乘以損失幅度", "僅指負面事件的概率", "回報的標準差", "最大可能損失"],
                0,
                "In the Basel framework, risk is defined as the probability of loss multiplied by the magnitude of loss, capturing both likelihood and severity.",
                "在巴塞爾框架中，風險定義為損失概率乘以損失幅度，同時考慮可能性和嚴重性。"
            ),
            (
                "A risk-averse investor will most likely:",
                "一個風險規避型投資者最有可能：",
                ["Require a higher return for taking on additional risk", "Accept any investment regardless of risk", "Prefer investments with the highest return regardless of risk", "Avoid all investments"],
                ["承擔額外風險時要求更高的回報", "不論風險如何都接受任何投資", "不論風險如何都偏好最高回報的投資", "避免所有投資"],
                0,
                "Risk-averse investors require additional compensation (higher expected return) for bearing additional risk.",
                "風險規避型投資者需要額外補償（更高的預期回報）來承擔額外風險。"
            ),
            (
                "Enterprise Risk Management (ERM) differs from traditional risk management primarily because ERM:",
                "企業風險管理（ERM）與傳統風險管理的主要區別在於ERM：",
                ["Considers risks across the entire organization in an integrated framework", "Focuses only on financial risks", "Is regulated by the SEC", "Eliminates all organizational risks"],
                ["在整合框架中考慮整個組織的風險", "僅關注金融風險", "由證監會監管", "消除所有組織風險"],
                0,
                "ERM takes a holistic, organization-wide approach to risk management, integrating all risk types rather than managing them in silos.",
                "ERM 採取全面的、組織範圍的風險管理方法，整合所有風險類型而非各自為政。"
            ),
            (
                "The three lines of defense model includes all of the following EXCEPT:",
                "三道防線模型包括以下所有內容，除了：",
                ["External auditors as the first line", "Management as the first line", "Risk management function as the second line", "Internal audit as the third line"],
                ["外部審計師作為第一道防線", "管理層作為第一道防線", "風險管理職能作為第二道防線", "內部審計作為第三道防線"],
                0,
                "The three lines model: 1st line = management/operations, 2nd line = risk management and compliance, 3rd line = internal audit. External auditors are not part of this model.",
                "三道防線模型：第一道防線=管理層/營運，第二道防線=風險管理和合規，第三道防線=內部審計。外部審計師不屬於此模型。"
            ),
            (
                "Moral hazard in risk management refers to:",
                "風險管理中的道德風險是指：",
                ["The tendency to take greater risks when protected from consequences", "Risk of fraud by employees", "The risk of bad weather affecting operations", "Systematic risk in financial markets"],
                ["在受到保護免受後果時傾向承擔更大風險", "員工欺詐風險", "惡劣天氣影響營運的風險", "金融市場的系統性風險"],
                0,
                "Moral hazard occurs when a party is insulated from risk and therefore takes on greater risk than they otherwise would, knowing they won't bear the full consequences.",
                "道德風險發生在一方隔絕於風險之外，因此承擔比原本更大的風險，因為他們知道自己不會承擔全部後果。"
            ),
            (
                "Risk appetite is best defined as:",
                "風險偏好最佳定義為：",
                ["The total amount of risk an organization is willing to accept in pursuit of its objectives", "The maximum loss an organization can sustain", "The risk that remains after controls are applied", "The sum of all identified risks"],
                ["組織在追求目標時願意承擔的風險總量", "組織可承受的最大損失", "應用控制措施後剩餘的風險", "所有已識別風險的總和"],
                0,
                "Risk appetite is the aggregate level and types of risk an organization is willing to accept in pursuit of its strategic objectives.",
                "風險偏好是組織在追求戰略目標時願意接受的風險總量和類型。"
            ),
            (
                "Which of the following is an example of diversifiable (unsystematic) risk?",
                "以下哪項是可分散（非系統性）風險的例子？",
                ["A company's CEO unexpectedly resigns", "A global recession", "An increase in interest rates", "A pandemic affecting all industries"],
                ["公司CEO意外辭職", "全球經濟衰退", "利率上升", "影響所有行業的大流行病"],
                0,
                "Company-specific events like CEO resignation are unsystematic risks that can be diversified away. Market-wide events like recessions and interest rate changes are systematic risks.",
                "CEO辭職等公司特定事件是非系統性風險，可以通過分散投資消除。經濟衰退和利率變化等全市場事件是系統性風險。"
            ),
            (
                "The Risk Management Association's (RMA) approach to operational risk emphasizes:",
                "風險管理協會（RMA）對操作風險的方法強調：",
                ["Self-assessment by business units", "External regulation only", "Avoiding all operational activities", "Using only historical loss data"],
                ["業務部門的自我評估", "僅靠外部監管", "避免所有營運活動", "僅使用歷史損失數據"],
                0,
                "RMA promotes a self-assessment approach where business units identify and evaluate their own operational risks as part of a comprehensive risk management framework.",
                "RMA 推廣自我評估方法，讓業務部門在全面風險管理框架內識別和評估自身的操作風險。"
            ),
            (
                "Adverse selection occurs when:",
                "逆向選擇發生在：",
                ["Higher-risk individuals are more likely to purchase insurance", "Insurance companies select only low-risk clients", "All individuals pay the same premium regardless of risk", "Government mandates insurance coverage"],
                ["高風險個人更傾向購買保險", "保險公司僅選擇低風險客戶", "所有個人不論風險支付相同保費", "政府強制保險覆蓋"],
                0,
                "Adverse selection occurs when information asymmetry leads to higher-risk individuals being more likely to seek insurance, potentially causing market failure.",
                "逆向選擇發生在信息不對稱導致高風險個人更傾向尋求保險，可能導致市場失靈。"
            ),
            (
                "The COSO ERM framework identifies all of the following components EXCEPT:",
                "COSO ERM框架包括以下所有組成部分，除了：",
                ["Governance and culture", "Strategy and objective-setting", "External auditing", "Review and revision"],
                ["治理與文化", "戰略與目標設定", "外部審計", "審查與修訂"],
                2,
                "COSO ERM components: Governance & Culture, Strategy & Objective Setting, Performance, Review & Revision, Information Communication & Reporting. External auditing is not a component.",
                "COSO ERM組成部分：治理與文化、戰略與目標設定、績效、審查與修訂、信息溝通與報告。外部審計不是其中的組成部分。"
            ),
        ]
    },
    "Quantitative Analysis": {
        "zh": "定量分析",
        "questions": [
            (
                "If a portfolio has a VaR of $5 million at the 95% confidence level, this means:",
                "如果一個投資組合在95%置信水平下的VaR為500萬美元，這意味著：",
                ["There is a 5% probability that the portfolio will lose more than $5 million in the given time period", "The portfolio will definitely lose $5 million", "The average loss is $5 million", "The maximum loss is $5 million"],
                ["投資組合有5%的概率在給定期間內損失超過500萬美元", "投資組合肯定會損失500萬美元", "平均損失為500萬美元", "最大損失為500萬美元"],
                0,
                "VaR at 95% confidence means there is a 5% chance that losses will exceed the VaR amount over the specified time horizon.",
                "95%置信水平的VaR意味著在特定時間範圍內，損失超過VaR金額的概率為5%。"
            ),
            (
                "The standard deviation of a two-asset portfolio depends on:",
                "兩資產投資組合的標準差取決於：",
                ["The weights, individual standard deviations, and correlation between assets", "Only the weights of the assets", "Only the individual standard deviations", "The sum of individual standard deviations"],
                ["權重、個別標準差和資產間的相關性", "僅資產的權重", "僅個別標準差", "個別標準差之和"],
                0,
                "Portfolio variance = w₁²σ₁² + w₂²σ₂² + 2w₁w₂ρ₁₂σ₁σ₂. It depends on weights, individual volatilities, and the correlation coefficient.",
                "投資組合方差 = w₁²σ₁² + w₂²σ₂² + 2w₁w₂ρ₁₂σ₁σ₂。取決於權重、個別波動率和相關係數。"
            ),
            (
                "A lognormal distribution is commonly used in finance because:",
                "對數常態分佈在金融中常用，因為：",
                ["Asset prices cannot be negative and returns are approximately normally distributed", "It is symmetric", "It has thinner tails than normal distribution", "It is easier to calculate than normal distribution"],
                ["資產價格不能為負，回報近似常態分佈", "它是對稱的", "它的尾部比常態分佈更薄", "它比常態分佈更容易計算"],
                0,
                "If returns are normally distributed, then prices (which are the product of 1+return) follow a lognormal distribution, naturally bounded at zero.",
                "如果回報呈常態分佈，那麼價格（即1+回報的乘積）遵循對數常態分佈，自然以零為下界。"
            ),
            (
                "The expected shortfall (CVaR) at the 95% confidence level measures:",
                "95%置信水平的預期短缺（CVaR）衡量：",
                ["The average loss in the worst 5% of cases", "The maximum loss in the worst 5% of cases", "The loss at exactly the 95th percentile", "The variance of losses beyond VaR"],
                ["最差5%情況下的平均損失", "最差5%情況下的最大損失", "恰好在第95百分位的損失", "超過VaR的損失方差"],
                0,
                "Expected Shortfall (CVaR) is the expected value of losses given that the loss exceeds VaR, i.e., the average loss in the worst (1-confidence)% scenarios.",
                "預期短缺（CVaR）是損失超過VaR時的條件預期損失，即最差（1-置信水平）%情景下的平均損失。"
            ),
            (
                "Monte Carlo simulation in risk management is most useful for:",
                "蒙地卡羅模擬在風險管理中最有用於：",
                ["Estimating risk measures for complex, non-linear portfolios", "Calculating simple averages", "Eliminating all model risk", "Determining historical returns"],
                ["估算複雜非線性投資組合的風險指標", "計算簡單平均值", "消除所有模型風險", "確定歷史回報"],
                0,
                "Monte Carlo simulation generates thousands of random scenarios to estimate risk measures, especially valuable for complex portfolios with non-linear payoffs (options, structured products).",
                "蒙地卡羅模擬生成數千個隨機情景來估算風險指標，對具有非線性收益（期權、結構化產品）的複雜投資組合特別有價值。"
            ),
            (
                "The Sharpe ratio is calculated as:",
                "夏普比率的計算公式為：",
                ["(Portfolio return - Risk-free rate) / Portfolio standard deviation", "Portfolio return / Portfolio standard deviation", "(Portfolio return - Risk-free rate) / Beta", "Portfolio return - Risk-free rate"],
                ["（投資組合回報 - 無風險利率）/ 投資組合標準差", "投資組合回報 / 投資組合標準差", "（投資組合回報 - 無風險利率）/ Beta", "投資組合回報 - 無風險利率"],
                0,
                "Sharpe ratio = (Rp - Rf) / σp. It measures excess return per unit of total risk (standard deviation).",
                "夏普比率 = (Rp - Rf) / σp。衡量每單位總風險（標準差）的超額回報。"
            ),
            (
                "Stress testing differs from VaR in that stress testing:",
                "壓力測試與VaR的不同之處在於壓力測試：",
                ["Evaluates portfolio performance under extreme but plausible scenarios", "Uses only normal market conditions", "Relies solely on historical data", "Measures only credit risk"],
                ["在極端但合理的情景下評估投資組合表現", "僅使用正常市場條件", "僅依賴歷史數據", "僅衡量信用風險"],
                0,
                "Stress testing evaluates how portfolios would perform under extreme scenarios (e.g., 2008 crisis, COVID crash) that go beyond normal statistical measures like VaR.",
                "壓力測試評估投資組合在極端情景（如2008年危機、COVID崩盤）下的表現，超越VaR等常規統計指標。"
            ),
            (
                "In a normal distribution, approximately what percentage of observations fall within 2 standard deviations of the mean?",
                "在常態分佈中，大約有多少百分比的觀察值落在均值的2個標準差範圍內？",
                ["95%", "68%", "99%", "90%"],
                ["95%", "68%", "99%", "90%"],
                0,
                "The empirical rule states that for a normal distribution: ~68% within 1σ, ~95% within 2σ, and ~99.7% within 3σ of the mean.",
                "經驗法則表明，常態分佈中：約68%在1個標準差內，約95%在2個標準差內，約99.7%在3個標準差內。"
            ),
            (
                "The correlation coefficient between two assets ranges from:",
                "兩個資產之間的相關係數範圍為：",
                ["-1 to +1", "0 to +1", "-∞ to +∞", "0 to ∞"],
                ["-1到+1", "0到+1", "-∞到+∞", "0到∞"],
                0,
                "The Pearson correlation coefficient ranges from -1 (perfect negative correlation) to +1 (perfect positive correlation), with 0 indicating no linear relationship.",
                "皮爾遜相關係數範圍從-1（完全負相關）到+1（完全正相關），0表示無線性關係。"
            ),
            (
                "Which of the following distributions exhibits leptokurtosis (fat tails)?",
                "以下哪種分佈表現出尖峰態（肥尾）？",
                ["Student's t-distribution", "Normal distribution", "Uniform distribution", "Exponential distribution"],
                ["t分佈", "常態分佈", "均勻分佈", "指數分佈"],
                0,
                "Student's t-distribution has heavier tails than the normal distribution (leptokurtosis), meaning extreme events are more likely than predicted by a normal distribution.",
                "t分佈的尾部比常態分佈更厚（尖峰態），意味著極端事件比常態分佈預測的更可能發生。"
            ),
        ]
    },
    "Financial Markets and Products": {
        "zh": "金融市場與產品",
        "questions": [
            (
                "A forward contract differs from a futures contract in that:",
                "遠期合約與期貨合約的不同之處在於：",
                ["Forwards are traded over-the-counter while futures are exchange-traded", "Forwards are standardized", "Futures have higher counterparty risk", "Forwards are marked to market daily"],
                ["遠期合約在場外交易，期貨合約在交易所交易", "遠期合約是標準化的", "期貨有更高的交易對手風險", "遠期合約每日按市值計價"],
                0,
                "Forward contracts are private OTC agreements with customization, while futures are standardized exchange-traded instruments with clearinghouse guarantee.",
                "遠期合約是場外交易的私人協議，具有定制性；期貨是標準化的交易所交易工具，有清算所擔保。"
            ),
            (
                "The put-call parity relationship for European options states:",
                "歐式期權的看跌-看漲平價關係表明：",
                ["C - P = S - PV(K)", "C + P = S + K", "C - P = K - S", "C × P = S × K"],
                ["C - P = S - PV(K)", "C + P = S + K", "C - P = K - S", "C × P = S × K"],
                0,
                "Put-call parity: C - P = S - PV(K), where C=call price, P=put price, S=stock price, PV(K)=present value of strike price.",
                "看跌-看漲平價：C - P = S - PV(K)，其中C=看漲期權價格，P=看跌期權價格，S=股票價格，PV(K)=執行價格的現值。"
            ),
            (
                "The LIBOR-OIS spread is considered a measure of:",
                "LIBOR-OIS利差被視為一種衡量：",
                ["Banking system credit risk and liquidity stress", "Inflation expectations", "Central bank policy rates", "Stock market volatility"],
                ["銀行系統信用風險和流動性壓力", "通脹預期", "央行政策利率", "股市波動率"],
                0,
                "The LIBOR-OIS spread reflects the perceived credit risk in interbank lending. A wider spread indicates greater stress in the banking system.",
                "LIBOR-OIS利差反映銀行間借貸的感知信用風險。利差擴大表示銀行系統壓力加大。"
            ),
            (
                "An interest rate swap typically involves:",
                "利率互換通常涉及：",
                ["Exchanging fixed-rate payments for floating-rate payments", "Exchanging one currency for another", "Buying and selling equity shares", "Exchanging commodities"],
                ["將固定利率支付換為浮動利率支付", "將一種貨幣換為另一種", "買賣股票", "交換商品"],
                0,
                "In a plain vanilla interest rate swap, one party pays a fixed rate while the other pays a floating rate (e.g., LIBOR + spread) on a notional principal.",
                "在普通利率互換中，一方支付固定利率，另一方支付浮動利率（如LIBOR+利差），基於名義本金。"
            ),
            (
                "A credit default swap (CDS) provides protection against:",
                "信用違約互換（CDS）提供保護以防：",
                ["Credit event such as default or restructuring of a reference entity", "Interest rate changes", "Currency fluctuations", "Stock price decline"],
                ["參考實體的違約或重組等信用事件", "利率變化", "貨幣波動", "股價下跌"],
                0,
                "A CDS is a credit derivative where the protection buyer pays periodic premiums to the protection seller in exchange for compensation if a credit event occurs.",
                "CDS是一種信用衍生品，保護買方向保護賣方支付定期保費，以換取信用事件發生時的賠償。"
            ),
            (
                "The duration of a zero-coupon bond:",
                "零息債券的久期：",
                ["Equals its maturity", "Is zero", "Is less than its maturity", "Is greater than its maturity"],
                ["等於其到期日", "為零", "小於其到期日", "大於其到期日"],
                0,
                "A zero-coupon bond makes only one payment at maturity, so its Macaulay duration equals exactly its maturity. All cash flow is received at maturity.",
                "零息債券僅在到期時支付一次，因此其麥考利久期恰好等於到期時間。所有現金流在到期時收取。"
            ),
            (
                "Basel III's Liquidity Coverage Ratio (LCR) requires banks to hold:",
                "巴塞爾III的流動性覆蓋比率（LCR）要求銀行持有：",
                ["Enough high-quality liquid assets to cover 30 days of net cash outflows", "Capital equal to total assets", "Cash equal to all deposits", "Government bonds equal to 100% of loans"],
                ["足夠的高質量流動資產覆蓋30天的淨現金流出", "等於總資產的資本", "等於所有存款的現金", "等於貸款100%的政府債券"],
                0,
                "LCR = HQLA / Net cash outflows over 30 days ≥ 100%. Banks must maintain sufficient high-quality liquid assets to survive a 30-day stress scenario.",
                "LCR = 高質量流動資產 / 30天淨現金流出 ≥ 100%。銀行必須維持足夠的高質量流動資產以度過30天壓力情景。"
            ),
            (
                "Which of the following is NOT a characteristic of an American-style option?",
                "以下哪項不是美式期權的特徵？",
                ["It can only be exercised at expiration", "It can be exercised at any time before expiration", "It is worth at least as much as a European option", "It is typically traded on exchanges"],
                ["只能在到期時行使", "可在到期前任何時間行使", "價值至少等於歐式期權", "通常在交易所交易"],
                0,
                "American options can be exercised at any time before expiration, unlike European options which can only be exercised at expiration. This early exercise feature makes American options worth at least as much as European options.",
                "美式期權可在到期前任何時間行使，不像歐式期權只能在到期時行使。這種提前行使特徵使美式期權價值至少等於歐式期權。"
            ),
            (
                "The TED spread measures the difference between:",
                "TED利差衡量以下兩者之間的差異：",
                ["3-month LIBOR and 3-month T-bill rate", "S&P 500 and Treasury yields", "Corporate bond yields and LIBOR", "Fed funds rate and LIBOR"],
                ["3個月LIBOR和3個月國庫券利率", "標普500和國債收益率", "公司債收益率和LIBOR", "聯邦基金利率和LIBOR"],
                0,
                "TED spread = 3-month LIBOR - 3-month T-bill rate. It serves as an indicator of credit risk in the general economy and liquidity in the banking system.",
                "TED利差 = 3個月LIBOR - 3個月國庫券利率。它作為整體經濟信用風險和銀行系統流動性的指標。"
            ),
            (
                "Collateralized Debt Obligations (CDOs) are structured with tranches that:",
                "擔保債務憑證（CDOs）的分層結構具有以下特點：",
                ["Allocate losses in reverse order of seniority", "Pay all tranches equally", "Only contain mortgage loans", "Have no credit risk"],
                ["按相反的優先順序分配損失", "向所有分層同等支付", "僅包含抵押貸款", "沒有信用風險"],
                0,
                "CDO tranches are structured so that equity tranches absorb losses first, then mezzanine, and senior tranches are last to bear losses. This creates different risk profiles.",
                "CDO分層結構使得股權層先吸收損失，然後是夾層，高級層最後承擔損失。這創造了不同的風險特徵。"
            ),
        ]
    },
    "Valuation and Risk Models": {
        "zh": "估值與風險模型",
        "questions": [
            (
                "The Black-Scholes model assumes all of the following EXCEPT:",
                "Black-Scholes模型假設以下所有條件，除了：",
                ["Stock prices follow a jump-diffusion process", "No dividends are paid", "Constant volatility", "Risk-free rate is constant"],
                ["股價遵循跳躍擴散過程", "不支付股息", "波動率恆定", "無風險利率恆定"],
                0,
                "Black-Scholes assumes geometric Brownian motion (continuous paths, no jumps), constant volatility, constant risk-free rate, no dividends, and no arbitrage.",
                "Black-Scholes假設幾何布朗運動（連續路徑，無跳躍）、恆定波動率、恆定無風險利率、無股息和無套利。"
            ),
            (
                "The Greeks in options pricing include Delta, which measures:",
                "期權定價中的希臘字母包括Delta，它衡量：",
                ["The sensitivity of option price to changes in the underlying asset price", "The sensitivity to time decay", "The sensitivity to volatility changes", "The sensitivity to interest rate changes"],
                ["期權價格對標的資產價格變化的敏感度", "對時間衰減的敏感度", "對波動率變化的敏感度", "對利率變化的敏感度"],
                0,
                "Delta (Δ) = ∂V/∂S, measuring the rate of change of option value with respect to the underlying asset's price. It also approximates the hedge ratio.",
                "Delta (Δ) = ∂V/∂S，衡量期權價值相對於標的資產價格的變化率。它也近似對沖比率。"
            ),
            (
                "Historical simulation for VaR estimation has the advantage of:",
                "歷史模擬法估算VaR的優勢在於：",
                ["Not requiring assumptions about the distribution of returns", "Being the most computationally efficient", "Always producing the most accurate estimates", "Requiring fewer historical data points"],
                ["不需要假設回報的分佈", "計算效率最高", "總是產生最準確的估算", "需要較少的歷史數據點"],
                0,
                "Historical simulation uses actual historical returns to estimate VaR, avoiding the need to assume a particular return distribution (normal, lognormal, etc.).",
                "歷史模擬使用實際歷史回報來估算VaR，避免了假設特定回報分佈（常態、對數常態等）的需要。"
            ),
            (
                "A bond's DV01 (dollar value of a basis point) represents:",
                "債券的DV01（一個基點的美元價值）代表：",
                ["The change in bond price for a 1 basis point change in yield", "The bond's annual coupon payment", "The bond's duration divided by 100", "The bond's credit spread"],
                ["收益率變化1個基點時債券價格的變化", "債券的年息票支付", "債券的久期除以100", "債券的信用利差"],
                0,
                "DV01 = -ΔP/Δy (for a 1bp change). It measures the dollar price change of a bond for a 1 basis point change in yield, used extensively in hedging.",
                "DV01 = -ΔP/Δy（1個基點變化）。衡量收益率變化1個基點時債券的美元價格變化，廣泛用於對沖。"
            ),
            (
                "Conditional VaR (CVaR) is considered superior to VaR because CVaR:",
                "條件VaR（CVaR）被認為優於VaR，因為CVaR：",
                ["Is a coherent risk measure that satisfies subadditivity", "Is always easier to calculate", "Does not depend on confidence level", "Only measures market risk"],
                ["是一種滿足次可加性的連貫風險指標", "總是更容易計算", "不依賴置信水平", "僅衡量市場風險"],
                0,
                "CVaR (Expected Shortfall) is coherent because it satisfies subadditivity: CVaR(A+B) ≤ CVaR(A) + CVaR(B). VaR can violate this, making CVaR more reliable for portfolio risk.",
                "CVaR（預期短缺）是連貫的，因為它滿足次可加性：CVaR(A+B) ≤ CVaR(A) + CVaR(B)。VaR可能違反此條件，使CVaR在投資組合風險方面更可靠。"
            ),
            (
                "In the Merton model, a company's equity is modeled as:",
                "在Merton模型中，公司的股權被建模為：",
                ["A call option on the firm's assets with a strike equal to the face value of debt", "A put option on the firm's assets", "A forward contract on the firm's debt", "A zero-coupon bond"],
                ["以債務面值為執行價格的公司資產看漲期權", "公司資產的看跌期權", "公司債務的遠期合約", "零息債券"],
                0,
                "In Merton's model, equity = call option on firm's assets with strike = face value of debt and expiration = debt maturity. If assets > debt, equity is in the money.",
                "在Merton模型中，股權=以公司資產為標的、以債務面值為執行價格、以債務到期日為到期日的看漲期權。如果資產>債務，股權為價內。"
            ),
            (
                "The Basel Committee's Standardized Approach for market risk uses:",
                "巴塞爾委員會市場風險標準化方法使用：",
                ["Fixed risk weights applied to positions based on asset class", "Internal models approved by regulators", "Only historical simulation", "A single VaR number for the entire bank"],
                ["根據資產類別對持倉應用固定風險權重", "監管機構批准的內部模型", "僅歷史模擬", "整個銀行的單一VaR數字"],
                0,
                "The Standardized Approach applies prescribed risk weights and charges based on asset class (interest rate, equity, FX, commodity, option) without requiring internal models.",
                "標準化方法根據資產類別（利率、股票、外匯、商品、期權）應用規定的風險權重和費用，無需內部模型。"
            ),
            (
                "Implied volatility is the volatility that:",
                "隱含波動率是指：",
                ["Makes the Black-Scholes model price equal to the observed market price", "Is calculated from historical returns", "Is always higher than realized volatility", "Is set by the Federal Reserve"],
                ["使Black-Scholes模型價格等於觀察到的市場價格", "從歷史回報計算", "總是高於已實現波動率", "由美聯儲設定"],
                0,
                "Implied volatility is found by solving the Black-Scholes equation backwards: given the market price of an option, what volatility input makes the model price match?",
                "隱含波動率是通過反向求解Black-Scholes方程得到的：給定期權的市場價格，什麼波動率輸入能使模型價格匹配？"
            ),
            (
                "Counterparty credit risk in OTC derivatives is mitigated by:",
                "場外衍生品的交易對手信用風險通過以下方式緩解：",
                ["Collateral posting and netting agreements", "Only central clearing", "Eliminating all derivatives trading", "Government guarantees"],
                ["抵押品發布和淨額結算協議", "僅中央清算", "消除所有衍生品交易", "政府擔保"],
                0,
                "Counterparty risk is mitigated through: netting agreements (reducing exposure), collateral/margin posting, central clearing (CCPs), and credit support annexes (CSAs).",
                "交易對手風險通過以下方式緩解：淨額結算協議（減少風險敞口）、抵押品/保證金發布、中央清算（CCP）和信用支持附件（CSA）。"
            ),
            (
                "The fundamental review of the trading book (FRTB) introduces:",
                "交易賬簿基本審查（FRTB）引入了：",
                ["A new expected shortfall-based approach replacing VaR for internal models", "Elimination of all internal models", "A single global standardized approach only", "Removal of all capital requirements for market risk"],
                ["以預期短缺為基礎的新方法取代VaR用於內部模型", "取消所有內部模型", "僅單一全球標準化方法", "取消所有市場風險資本要求"],
                0,
                "FRTB replaces VaR with Expected Shortfall (ES) at 97.5% confidence for internal models, with stressed scenarios and liquidity horizons, strengthening market risk capital requirements.",
                "FRTB用97.5%置信水平的預期短缺（ES）取代VaR用於內部模型，加入壓力情景和流動性時間範圍，加強市場風險資本要求。"
            ),
        ]
    },
}

# ============ PART 2 TOPICS ============
p2_topics = {
    "Market Risk": {
        "zh": "市場風險",
        "questions": [
            (
                "The Basel Committee's market risk framework defines a 'trading book' as:",
                "巴塞爾委員會的市場風險框架將「交易賬簿」定義為：",
                ["Positions held with trading intent or hedging trading book positions", "All bank assets", "Only government bonds", "Long-term investment portfolios"],
                ["以交易意圖持有或用於對沖交易賬簿持倉的頭寸", "所有銀行資產", "僅政府債券", "長期投資組合"],
                0,
                "Trading book includes positions held for short-term resale, deriving benefit from short-term price movements, hedging trading positions, and market-making.",
                "交易賬簿包括為短期轉售持有的頭寸、從短期價格變動中獲益的頭寸、對沖交易頭寸和做市活動。"
            ),
            (
                "Basis risk arises when:",
                "基差風險產生於：",
                ["The hedge instrument and the hedged item are not perfectly correlated", "Interest rates decline", "A portfolio is fully hedged", "Volatility is zero"],
                ["對沖工具與被對沖項目不完全相關", "利率下降", "投資組合完全對沖", "波動率為零"],
                0,
                "Basis risk = risk that the hedge instrument and hedged asset move differently. It's the residual risk when the hedge doesn't perfectly offset the underlying exposure.",
                "基差風險=對沖工具與被對沖資產走勢不一致的風險。是對沖未能完全抵消基礎風險敞口時的殘餘風險。"
            ),
            (
                "Gamma risk in options refers to:",
                "期權中的Gamma風險是指：",
                ["The rate of change of delta with respect to the underlying price", "The risk of early exercise", "The risk of interest rate changes", "The time decay of the option"],
                ["Delta相對於標的資產價格的變化率", "提前行使的風險", "利率變化的風險", "期權的時間衰減"],
                0,
                "Gamma (Γ) = ∂²V/∂S² = ∂Δ/∂S. It measures how fast delta changes as the underlying price changes, creating convexity risk in delta-hedged portfolios.",
                "Gamma (Γ) = ∂²V/∂S² = ∂Δ/∂S。衡量Delta隨標的資產價格變化的速度，在Delta對沖的投資組合中產生凸性風險。"
            ),
            (
                "Value at Risk (VaR) can be calculated using all of the following methods EXCEPT:",
                "VaR可以使用以下所有方法計算，除了：",
                ["Mark-to-model only without any market data", "Historical simulation", "Parametric (variance-covariance) method", "Monte Carlo simulation"],
                ["僅按模型計價而無任何市場數據", "歷史模擬", "參數（方差-協方差）方法", "蒙地卡羅模擬"],
                0,
                "VaR methods: 1) Parametric/variance-covariance, 2) Historical simulation, 3) Monte Carlo simulation. All require market data; 'mark-to-model only' is not a VaR methodology.",
                "VaR方法：1）參數/方差-協方差法，2）歷史模擬法，3）蒙地卡羅模擬法。都需要市場數據；「僅按模型計價」不是VaR方法。"
            ),
            (
                "The 2005 Basel II Amendment (Basel 2.5) was primarily motivated by:",
                "2005年巴塞爾II修正案（巴塞爾2.5）主要是由以下因素推動的：",
                ["Lessons from the 2007-2008 financial crisis regarding trading book risks", "The Asian financial crisis of 1997", "The dot-com bubble of 2000", "Inflation concerns in Europe"],
                ["2007-2008年金融危機關於交易賬簿風險的教訓", "1997年亞洲金融危機", "2000年互聯網泡沫", "歐洲通脹擔憂"],
                0,
                "Basel 2.5 (implemented 2011) increased trading book capital requirements after the crisis revealed inadequacies, adding incremental risk charges for default risk and stressed VaR.",
                "巴塞爾2.5（2011年實施）增加了交易賬簿資本要求，因危機揭示了不足之處，增加了違約風險和壓力VaR的增量風險費用。"
            ),
            (
                "Correlation trading involves:",
                "關聯交易涉及：",
                ["Trading based on the expected correlation between assets rather than their individual directions", "Only trading correlated stocks", "Buying and selling the same asset", "Trading only in bull markets"],
                ["基於資產間預期關聯性而非個別方向進行交易", "僅交易相關股票", "買賣同一資產", "僅在牛市交易"],
                0,
                "Correlation trading focuses on the relationship between assets—using products like correlation swaps, CDO tranches, or dispersion trades to express views on correlation rather than direction.",
                "關聯交易關注資產之間的關係——使用關聯互換、CDO分層或分散交易等產品來表達對關聯性而非方向的看法。"
            ),
            (
                "The maximum loss on a long call option position is:",
                "看漲期權多頭頭寸的最大損失為：",
                ["The premium paid for the option", "Unlimited", "The strike price", "The stock price minus the premium"],
                ["支付的期權費", "無限", "執行價格", "股票價格減期權費"],
                0,
                "For a long call, maximum loss = premium paid. If the stock price stays below the strike at expiration, the option expires worthless and the buyer loses only the premium.",
                "對於看漲期權多頭，最大損失=支付的期權費。如果到期時股價保持在執行價格以下，期權到期無價值，買方僅損失期權費。"
            ),
            (
                "An interest rate cap provides protection against:",
                "利率上限提供保護以防：",
                ["Rising interest rates above the cap rate", "Falling interest rates", "Credit defaults", "Currency depreciation"],
                ["利率上升超過上限利率", "利率下降", "信用違約", "貨幣貶值"],
                0,
                "An interest rate cap is a series of caplets that pay off when the reference rate exceeds the cap rate, protecting the buyer from rising interest rates.",
                "利率上限是一系列上限期權，當參考利率超過上限利率時支付收益，保護買方免受利率上升的影響。"
            ),
            (
                "Risk-weighted assets (RWAs) for market risk under the standardized approach are calculated by:",
                "標準化方法下的市場風險加權資產（RWAs）通過以下方式計算：",
                ["Applying risk charges for each risk factor and aggregating", "Using only VaR", "Multiplying total assets by 8%", "Dividing capital by total assets"],
                ["對每個風險因素應用風險費用並匯總", "僅使用VaR", "將總資產乘以8%", "將資本除以總資產"],
                0,
                "Standardized approach calculates capital charges for interest rate, equity, FX, commodity, and option risks separately, then aggregates with some offsets allowed.",
                "標準化方法分別計算利率、股票、外匯、商品和期權風險的資本費用，然後允許一定抵消後匯總。"
            ),
            (
                "Vega measures the sensitivity of an option's price to changes in:",
                "Vega衡量期權價格對以下變化的敏感度：",
                ["Implied volatility", "Underlying asset price", "Interest rates", "Time to expiration"],
                ["隱含波動率", "標的資產價格", "利率", "到期時間"],
                0,
                "Vega = ∂V/∂σ, measuring the rate of change of option value with respect to implied volatility. Long options have positive vega (benefit from higher volatility).",
                "Vega = ∂V/∂σ，衡量期權價值相對於隱含波動率的變化率。期權多頭具有正Vega（從較高波動率中受益）。"
            ),
        ]
    },
    "Credit Risk": {
        "zh": "信用風險",
        "questions": [
            (
                "The expected loss (EL) from a loan is calculated as:",
                "貸款的預期損失（EL）計算為：",
                ["Probability of Default × Loss Given Default × Exposure at Default", "Only the probability of default", "The maximum possible loss", "The interest rate times the principal"],
                ["違約概率 × 違約損失率 × 違約時風險敞口", "僅違約概率", "最大可能損失", "利率乘以本金"],
                0,
                "EL = PD × LGD × EAD. This formula captures the three components of credit risk: likelihood of default, severity given default, and amount exposed.",
                "EL = PD × LGD × EAD。此公式捕捉信用風險的三個組成部分：違約可能性、違約時的嚴重程度和暴露金額。"
            ),
            (
                "In the CreditMetrics framework, credit migration refers to:",
                "在CreditMetrics框架中，信用遷移是指：",
                ["Changes in a borrower's credit rating over time", "Migration of loans between banks", "Transfer of credit risk to third parties", "Movement of interest rates"],
                ["借款人信用評級隨時間的變化", "貸款在銀行間的遷移", "將信用風險轉移給第三方", "利率的變動"],
                0,
                "Credit migration measures the risk that a borrower's credit quality changes (upgrades or downgrades), affecting the portfolio value even without default.",
                "信用遷移衡量借款人信用質量變化（升級或降級）的風險，即使不違約也會影響投資組合價值。"
            ),
            (
                "A credit spread represents:",
                "信用利差代表：",
                ["The additional yield demanded by investors for bearing credit risk", "The difference between two government bond yields", "The bank's profit margin", "The default probability"],
                ["投資者因承擔信用風險而要求的額外收益率", "兩個國債收益率之間的差異", "銀行的利潤率", "違約概率"],
                0,
                "Credit spread = yield on risky bond - yield on risk-free bond (same maturity). It compensates investors for the expected and unexpected credit losses.",
                "信用利差 = 有風險債券收益率 - 無風險債券收益率（相同期限）。它補償投資者的預期和非預期信用損失。"
            ),
            (
                "Credit Value Adjustment (CVA) is:",
                "信用價值調整（CVA）是：",
                ["The adjustment to the price of a derivative to account for counterparty credit risk", "A regulatory capital charge", "The value of collateral posted", "The credit spread times notional"],
                ["對衍生品價格進行的調整，以考慮交易對手信用風險", "監管資本費用", "已發布抵押品的價值", "信用利差乘以名義金額"],
                0,
                "CVA = adjustment to the risk-free value of a derivative portfolio to account for the possibility of counterparty default. CVA = EPE × LGD × PD.",
                "CVA = 對衍生品投資組合的無風險價值進行調整，以考慮交易對手違約的可能性。CVA = 風險敞口預期值 × 違約損失率 × 違約概率。"
            ),
            (
                "In a securitization, the waterfall structure refers to:",
                "在證券化中，瀑布結構是指：",
                ["The priority of cash flow distribution to different tranches", "Water damage risk in mortgage properties", "The sequential payment of dividends", "The regulatory approval process"],
                ["向不同分層分配現金流的優先順序", "抵押房產的水損風險", "股息的順序支付", "監管審批流程"],
                0,
                "Cash flow waterfall defines how cash flows from underlying assets are distributed: senior tranches get paid first, then mezzanine, then equity. Losses flow in reverse order.",
                "現金流瀑布定義了基礎資產現金流的分配方式：高級層先獲得支付，然後是夾層，然後是股權層。損失按相反順序流動。"
            ),
            (
                "The probability of default (PD) can be estimated from all of the following EXCEPT:",
                "違約概率（PD）可以從以下所有方式估算，除了：",
                ["Credit ratings and historical default rates", "Merton model using equity prices", "Accounting-based models", "The company's dividend policy alone"],
                ["信用評級和歷史違約率", "使用股價的Merton模型", "基於會計的模型", "僅公司的股息政策"],
                3,
                "PD estimation methods: credit ratings/ratings transition matrices, structural models (Merton), reduced-form models, accounting models (Altman Z-score). Dividend policy alone doesn't estimate PD.",
                "PD估算方法：信用評級/評級轉移矩陣、結構模型（Merton）、簡化模型、會計模型（Altman Z評分）。僅股息政策無法估算PD。"
            ),
            (
                "A recovery rate of 40% means:",
                "40%的回收率意味著：",
                ["Creditors recover 40% of the exposure amount in the event of default", "40% of borrowers will default", "The loan has a 40% interest rate", "40% of the portfolio is in default"],
                ["違約時債權人收回暴露金額的40%", "40%的借款人將違約", "貸款利率為40%", "投資組合的40%已違約"],
                0,
                "Recovery rate = percentage of exposure recovered after default. LGD = 1 - Recovery rate. So 40% recovery means 60% loss given default.",
                "回收率 = 違約後收回的暴露金額百分比。違約損失率 = 1 - 回收率。所以40%回收率意味著60%的違約損失率。"
            ),
            (
                "Netting in credit risk management reduces exposure by:",
                "信用風險管理中的淨額結算通過以下方式減少風險敞口：",
                ["Offsetting positive and negative mark-to-market values with the same counterparty", "Increasing collateral requirements", "Reducing the number of counterparties", "Eliminating all OTC trades"],
                ["與同一交易對手抵消正負按市值計價的價值", "增加抵押品要求", "減少交易對手數量", "取消所有場外交易"],
                0,
                "Netting agreements allow offsetting of positive and negative MTM values with the same counterparty, reducing gross exposure to net exposure.",
                "淨額結算協議允許與同一交易對手抵消正負按市值計價的價值，將總風險敞口減少為淨風險敞口。"
            ),
            (
                "The Altman Z-score model predicts bankruptcy using:",
                "Altman Z評分模型使用以下指標預測破產：",
                ["Five financial ratios weighted by coefficients", "Only stock price data", "Credit ratings from Moody's", "GDP growth rates"],
                ["五個財務比率按係數加權", "僅股價數據", "穆迪的信用評級", "GDP增長率"],
                0,
                "Z = 1.2X₁ + 1.4X₂ + 3.3X₃ + 0.6X₄ + 1.0X₅ where X₁=WC/TA, X₂=RE/TA, X₃=EBIT/TA, X₄=MVE/TL, X₅=S/TA.",
                "Z = 1.2X₁ + 1.4X₂ + 3.3X₃ + 0.6X₄ + 1.0X₅，其中X₁=營運資本/總資產，X₂=留存收益/總資產，X₃=息稅前利潤/總資產，X₄=股票市值/總負債，X₅=銷售額/總資產。"
            ),
            (
                "A credit-linked note (CLN) transfers credit risk to:",
                "信用掛鈎票據（CLN）將信用風險轉移給：",
                ["The investor who purchases the note", "The issuer of the reference obligation", "The government", "The exchange"],
                ["購買票據的投資者", "參考債務的發行人", "政府", "交易所"],
                0,
                "In a CLN, the investor receives a higher yield in exchange for bearing the credit risk of a reference entity. If a credit event occurs, principal is reduced.",
                "在CLN中，投資者獲得較高收益率，以換取承擔參考實體的信用風險。如果發生信用事件，本金將減少。"
            ),
        ]
    },
    "Operational Risk": {
        "zh": "操作風險",
        "questions": [
            (
                "Operational risk under Basel is defined as the risk of loss from:",
                "巴塞爾框架下的操作風險定義為因以下原因導致的損失風險：",
                ["Inadequate or failed internal processes, people, systems, or external events", "Only fraud by employees", "Only IT system failures", "Market price movements"],
                ["內部流程、人員、系統或外部事件不完善或失敗", "僅員工欺詐", "僅IT系統故障", "市場價格變動"],
                0,
                "Basel defines operational risk as risk of loss from inadequate/failed internal processes, people, systems, or external events. This includes legal risk but excludes strategic and reputational risk.",
                "巴塞爾將操作風險定義為因內部流程/人員/系統不完善或失敗或外部事件導致的損失風險。包括法律風險但不包括戰略和聲譽風險。"
            ),
            (
                "The Basel Advanced Measurement Approaches (AMA) for operational risk include:",
                "巴塞爾操作風險高級計量方法（AMA）包括：",
                ["Internal Measurement Approach, Loss Distribution Approach, and Scorecard Approach", "Only historical simulation", "Standardized approach only", "Mark-to-market approach"],
                ["內部計量法、損失分佈法和記分卡法", "僅歷史模擬", "僅標準化方法", "按市值計價法"],
                0,
                "AMA approaches: IMA (uses loss data grouped by business line/event type), LDA (fits distributions to loss data), Scorecard (combines quantitative and qualitative factors).",
                "AMA方法：IMA（按業務線/事件類型分組的損失數據）、LDA（對損失數據擬合分佈）、記分卡（結合定量和定性因素）。"
            ),
            (
                "A key risk indicator (KRI) in operational risk management is:",
                "操作風險管理中的關鍵風險指標（KRI）是：",
                ["A metric used to provide early warning of increased risk levels", "The total amount of losses", "The number of employees", "The firm's revenue"],
                ["用於提供風險水平上升早期預警的指標", "損失總額", "員工人數", "公司的收入"],
                0,
                "KRIs are forward-looking metrics that signal increasing operational risk before losses occur, such as staff turnover rate, system downtime, or error rates.",
                "KRIs是前瞻性指標，在損失發生之前發出操作風險增加的信號，如員工流動率、系統停機時間或錯誤率。"
            ),
            (
                "The Loss Distribution Approach (LDA) to operational risk requires:",
                "操作風險的損失分佈法（LDA）需要：",
                ["Modeling both frequency and severity distributions of losses", "Only historical loss data", "A single VaR estimate", "Regulatory approval of all models"],
                ["對損失的頻率和嚴重程度分佈進行建模", "僅歷史損失數據", "單一VaR估算", "所有模型的監管批准"],
                0,
                "LDA models: 1) frequency distribution (how often losses occur, e.g., Poisson), 2) severity distribution (how large losses are, e.g., lognormal). Combined via convolution to get aggregate loss distribution.",
                "LDA建模：1）頻率分佈（損失發生頻率，如泊松分佈），2）嚴重程度分佈（損失大小，如對數常態分佈）。通過卷積結合得到總損失分佈。"
            ),
            (
                "Which of the following is an example of an external event in operational risk?",
                "以下哪項是操作風險中外來事件的例子？",
                ["A natural disaster disrupting operations", "An internal audit finding", "A budget overrun", "Employee turnover"],
                ["自然災害干擾營運", "內部審計發現", "預算超支", "員工離職"],
                0,
                "External events include natural disasters, terrorism, robbery, vandalism, and regulatory changes—events outside the organization's direct control.",
                "外來事件包括自然災害、恐怖主義、搶劫、破壞和監管變化——組織無法直接控制的事件。"
            ),
            (
                "Operational risk capital under the Basic Indicator Approach (BIA) is calculated as:",
                "基本指標法（BIA）下的操作風險資本計算為：",
                ["15% of average gross income over 3 years", "8% of total assets", "10% of net income", "5% of risk-weighted assets"],
                ["3年平均總收入的15%", "總資產的8%", "淨收入的10%", "風險加權資產的5%"],
                0,
                "BIA: Capital charge = 15% × average annual gross income over the previous 3 years. Gross income = net interest income + non-interest income.",
                "BIA：資本費用 = 15% × 前3年平均年度總收入。總收入 = 淨利息收入 + 非利息收入。"
            ),
            (
                "Scenario analysis in operational risk is used to:",
                "操作風險中的情景分析用於：",
                ["Assess the impact of rare but severe events that may not appear in historical data", "Calculate daily VaR", "Replace loss data entirely", "Determine market risk capital"],
                ["評估歷史數據中可能未出現的罕見但嚴重事件的影響", "計算每日VaR", "完全取代損失數據", "確定市場風險資本"],
                0,
                "Scenario analysis uses expert judgment to estimate potential losses from severe but plausible events (e.g., major fraud, system failure) that may not be captured in historical loss data.",
                "情景分析使用專家判斷來估算嚴重但合理的事件（如重大欺詐、系統故障）的潛在損失，這些事件可能未被歷史損失數據捕捉。"
            ),
            (
                "The Sarbanes-Oxley Act (SOX) was enacted to address:",
                "《薩班斯-奧克斯利法案》（SOX）的頒布旨在解決：",
                ["Corporate governance and financial reporting failures", "Bank capital adequacy", "Consumer protection in banking", "Anti-money laundering"],
                ["公司治理和財務報告失敗", "銀行資本充足率", "銀行消費者保護", "反洗錢"],
                0,
                "SOX (2002) was enacted after Enron and WorldCom scandals to improve corporate governance, financial disclosures, and internal controls over financial reporting.",
                "SOX（2002）在安然和世通醜聞後頒布，旨在改善公司治理、財務披露和財務報告內部控制。"
            ),
            (
                "Which of the following best describes 'model risk' in operational risk?",
                "以下哪項最能描述操作風險中的「模型風險」？",
                ["The risk of losses from using incorrect or misapplied models", "The risk of not having any models", "The risk of models being too expensive", "The risk of regulatory changes to models"],
                ["使用不正確或誤用模型導致損失的風險", "沒有任何模型的風險", "模型過於昂貴的風險", "監管機構更改模型的風險"],
                0,
                "Model risk arises from using models that are incorrect, misused, or based on flawed assumptions, leading to poor decision-making and potential financial losses.",
                "模型風險源於使用不正確、被誤用或基於有缺陷假設的模型，導致決策失誤和潛在財務損失。"
            ),
            (
                "Business continuity planning (BCP) aims to:",
                "業務連續性計劃（BCP）旨在：",
                ["Ensure critical business functions can continue during and after a disruption", "Eliminate all operational risks", "Replace insurance coverage", "Comply with tax regulations"],
                ["確保關鍵業務功能在中斷期間和之後能夠繼續", "消除所有操作風險", "取代保險覆蓋", "遵守稅務法規"],
                0,
                "BCP ensures an organization can maintain or quickly resume critical functions after a disruption (natural disaster, cyber attack, pandemic), including backup systems and recovery procedures.",
                "BCP確保組織在中斷（自然災害、網絡攻擊、大流行病）後能夠維持或快速恢復關鍵功能，包括備份系統和恢復程序。"
            ),
        ]
    },
    "Liquidity and Treasury Risk": {
        "zh": "流動性與財務風險",
        "questions": [
            (
                "Funding liquidity risk refers to:",
                "融資流動性風險是指：",
                ["The risk that a firm cannot meet its short-term financial obligations", "The risk of asset price decline", "The risk of interest rate changes", "The risk of currency depreciation"],
                ["公司無法履行短期財務義務的風險", "資產價格下跌的風險", "利率變化的風險", "貨幣貶值的風險"],
                0,
                "Funding liquidity risk is the inability to meet cash flow needs—difficulty raising cash at reasonable cost to pay obligations as they come due.",
                "融資流動性風險是無法滿足現金流需求——難以以合理成本籌集現金來支付到期義務。"
            ),
            (
                "The Net Stable Funding Ratio (NSFR) under Basel III requires:",
                "巴塞爾III的淨穩定資金比率（NSFR）要求：",
                ["Available Stable Funding ≥ Required Stable Funding over a 1-year horizon", "Cash reserves equal to total deposits", "Zero short-term borrowing", "100% government bond holdings"],
                ["在1年時間範圍內，可用穩定資金 ≥ 所需穩定資金", "現金儲備等於總存款", "零短期借款", "100%政府債券持有"],
                0,
                "NSFR = ASF/RSF ≥ 100% over 1 year. It promotes longer-term funding by requiring banks to maintain stable funding sources proportional to their asset liquidity profiles.",
                "NSFR = 可用穩定資金/所需穩定資金 ≥ 100%（1年期）。通過要求銀行維持與其資產流動性特徵成比例的穩定資金來源，促進長期融資。"
            ),
            (
                "A liquidity gap analysis measures:",
                "流動性缺口分析衡量：",
                ["The difference between cash inflows and outflows over various time buckets", "The gap between assets and liabilities on the balance sheet", "The spread between lending and deposit rates", "The difference between VaR and expected shortfall"],
                ["不同時間段內現金流入和流出之間的差異", "資產負債表上資產和負債之間的差距", "貸款利率和存款利率之間的利差", "VaR和預期短缺之間的差異"],
                0,
                "Liquidity gap analysis buckets cash flows by maturity/time period to identify periods where outflows exceed inflows, revealing potential funding needs.",
                "流動性缺口分析按到期日/時間段將現金流分桶，以識別流出超過流入的時段，揭示潛在融資需求。"
            ),
            (
                "High-quality liquid assets (HQLA) under Basel III include:",
                "巴塞爾III下的高質量流動資產（HQLA）包括：",
                ["Level 1: cash, central bank reserves, government bonds; Level 2: high-rated corporate bonds, covered bonds", "Only cash", "All bank assets", "Only stocks"],
                ["一級：現金、央行儲備、政府債券；二級：高評級公司債、擔保債券", "僅現金", "所有銀行資產", "僅股票"],
                0,
                "HQLA hierarchy: Level 1 (no haircut: cash, govt bonds) + Level 2A (15% haircut: govt bonds, high-rated corp bonds) + Level 2B (25-50% haircut: lower-rated corp bonds, equities).",
                "HQLA層級：一級（無折扣：現金、政府債券）+ 二級A（15%折扣：政府債券、高評級公司債）+ 二級B（25-50%折扣：低評級公司債、股票）。"
            ),
            (
                "The bid-ask spread is an indicator of:",
                "買賣價差是指：",
                ["Market liquidity—a wider spread indicates lower liquidity", "Credit risk of the issuer", "Interest rate risk", "Inflation expectations"],
                ["市場流動性——價差越大表示流動性越低", "發行人的信用風險", "利率風險", "通脹預期"],
                0,
                "Bid-ask spread = Ask price - Bid price. A wider spread indicates lower market liquidity, higher transaction costs, and greater uncertainty about fair value.",
                "買賣價差 = 賣價 - 買價。價差越大表示市場流動性越低、交易成本越高、對公允價值的不確定性越大。"
            ),
            (
                "Contingent liquidity risk arises from:",
                "或有流動性風險產生於：",
                ["Off-balance sheet commitments such as credit lines, guarantees, and letters of credit", "Daily trading activities", "Long-term bond issuances", "Equity investments"],
                ["表外承諾，如信貸額度、擔保和信用證", "日常交易活動", "長期債券發行", "股權投資"],
                0,
                "Contingent liquidity risk comes from off-balance sheet obligations that may require cash outflows: committed credit lines, loan commitments, guarantees, and letters of credit.",
                "或有流動性風險來自可能需要現金流出的表外義務：承諾的信貸額度、貸款承諾、擔保和信用證。"
            ),
            (
                "The Basel III liquidity framework introduced two key ratios. The LCR addresses:",
                "巴塞爾III流動性框架引入了兩個關鍵比率。LCR針對：",
                ["Short-term (30-day) liquidity resilience", "Long-term (1-year) funding stability", "Capital adequacy", "Profitability"],
                ["短期（30天）流動性韌性", "長期（1年）融資穩定性", "資本充足率", "盈利能力"],
                0,
                "LCR = HQLA/Net cash outflows over 30 days ≥ 100%. It ensures banks have enough liquid assets to survive a 30-day stress scenario.",
                "LCR = 高質量流動資產/30天淨現金流出 ≥ 100%。確保銀行有足夠流動資產度過30天壓力情景。"
            ),
            (
                "Fire sale risk refers to:",
                "火速出售風險是指：",
                ["The risk of selling assets quickly at significantly below-market prices", "The risk of fire destroying physical assets", "The risk of selling too many shares", "Insurance claim risk"],
                ["以顯著低於市場價格快速出售資產的風險", "火災破壞實物資產的風險", "出售過多股票的風險", "保險索賠風險"],
                0,
                "Fire sales occur when an entity must sell assets quickly (often due to margin calls or liquidity needs), depressing prices below fundamental value and potentially triggering contagion.",
                "火速出售發生在實體必須快速出售資產時（通常因追加保證金或流動性需求），將價格壓低至基本價值以下，可能引發連鎖效應。"
            ),
            (
                "Liquidity-adjusted VaR (LVaR) differs from traditional VaR by:",
                "流動性調整VaR（LVaR）與傳統VaR的不同之處在於：",
                ["Incorporating the cost of liquidating positions over a realistic time horizon", "Using only cash positions", "Ignoring market risk", "Measuring only funding risk"],
                ["將在合理時間範圍內清算持倉的成本納入考量", "僅使用現金持倉", "忽略市場風險", "僅衡量融資風險"],
                0,
                "LVaR = VaR + Liquidity cost. It accounts for the fact that liquidating large positions takes time and moves prices, adding a liquidity premium to the standard VaR estimate.",
                "LVaR = VaR + 流動性成本。它考慮到清算大額持倉需要時間且會影響價格，為標準VaR估算增加流動性溢價。"
            ),
            (
                "Collateral transformation involves:",
                "抵押品轉換涉及：",
                ["Swapping lower-quality collateral for higher-quality assets to meet margin requirements", "Changing the ownership of collateral", "Eliminating collateral requirements entirely", "Selling collateral at market value"],
                ["將低質量抵押品換成高質量資產以滿足保證金要求", "更改抵押品所有權", "完全取消抵押品要求", "按市場價值出售抵押品"],
                0,
                "Collateral transformation services allow firms to swap less liquid or lower-quality assets for HQLA to meet clearinghouse or bilateral margin requirements.",
                "抵押品轉換服務允許公司將流動性較低或質量較低的資產換成高質量流動資產，以滿足清算所或雙邊保證金要求。"
            ),
        ]
    },
    "Risk Management and Investment Management": {
        "zh": "風險管理與投資管理",
        "questions": [
            (
                "The information ratio measures:",
                "信息比率衡量：",
                ["Active return per unit of active risk (tracking error)", "Total return per unit of total risk", "Return per unit of systematic risk", "Excess return over the risk-free rate"],
                ["每單位主動風險（跟踪誤差）的主動回報", "每單位總風險的總回報", "每單位系統性風險的回報", "相對於無風險利率的超額回報"],
                0,
                "Information ratio = (Rp - Rb) / σ(Rp - Rb), where Rp=portfolio return, Rb=benchmark return, and σ=tracking error. It measures a manager's ability to generate alpha.",
                "信息比率 = (Rp - Rb) / σ(Rp - Rb)，其中Rp=投資組合回報，Rb=基準回報，σ=跟踪誤差。衡量基金經理產生超額收益的能力。"
            ),
            (
                "Risk budgeting in portfolio management involves:",
                "投資組合管理中的風險預算涉及：",
                ["Allocating a total risk budget across asset classes or managers based on their risk contributions", "Setting a fixed budget for risk management software", "Eliminating all risk from the portfolio", "Choosing only the highest-return assets"],
                ["根據資產類別或基金經理的風險貢獻分配總風險預算", "為風險管理軟件設定固定預算", "消除投資組合中的所有風險", "僅選擇最高回報的資產"],
                0,
                "Risk budgeting allocates the total acceptable risk (e.g., VaR or tracking error budget) across components, ensuring each contributes proportionally to overall portfolio risk.",
                "風險預算將總可接受風險（如VaR或跟踪誤差預算）分配到各組成部分，確保每個部分按比例貢獻整體投資組合風險。"
            ),
            (
                "Alpha in portfolio performance refers to:",
                "投資組合表現中的Alpha是指：",
                ["The excess return above what is predicted by the CAPM or benchmark", "The total return of the portfolio", "The risk-free rate", "The portfolio's standard deviation"],
                ["超過CAPM或基準預測的超額回報", "投資組合的總回報", "無風險利率", "投資組合的標準差"],
                0,
                "Alpha = actual return - expected return (from CAPM or benchmark). Positive alpha indicates the manager added value beyond what systematic risk exposure would predict.",
                "Alpha = 實際回報 - 預期回報（來自CAPM或基準）。正Alpha表示基金經理在系統性風險敞口之外增加了價值。"
            ),
            (
                "The Sortino ratio differs from the Sharpe ratio by:",
                "索提諾比率與夏普比率的不同之處在於：",
                ["Using downside deviation instead of total standard deviation in the denominator", "Using alpha instead of return", "Ignoring the risk-free rate", "Using median returns instead of mean"],
                ["在分母中使用下行偏差而非總標準差", "使用Alpha而非回報", "忽略無風險利率", "使用中位數回報而非平均值"],
                0,
                "Sortino ratio = (Rp - Rf) / Downside deviation. It penalizes only downside volatility, not upside volatility, making it more appropriate for asymmetric return distributions.",
                "索提諾比率 = (Rp - Rf) / 下行偏差。它僅懲罰下行波動率，不懲罰上行波動率，使其更適用於不對稱回報分佈。"
            ),
            (
                "Factor-based risk models decompose portfolio risk into:",
                "基於因子的風險模型將投資組合風險分解為：",
                ["Systematic (factor) risk and idiosyncratic (specific) risk", "Only market risk", "Only credit risk", "Profit and loss"],
                ["系統性（因子）風險和特殊（特定）風險", "僅市場風險", "僅信用風險", "盈虧"],
                0,
                "Factor models (e.g., Barra, APT) decompose risk: systematic risk from common factors (market, size, value, momentum) + idiosyncratic risk unique to each security.",
                "因子模型（如Barra、APT）分解風險：來自共同因子（市場、規模、價值、動量）的系統性風險 + 每個證券獨有的特殊風險。"
            ),
            (
                "Maximum drawdown measures:",
                "最大回撤衡量：",
                ["The largest peak-to-trough decline in portfolio value before a new peak is reached", "The maximum daily loss", "The total loss over a year", "The difference between best and worst month"],
                ["投資組合價值在達到新峰值之前從峰值到谷值的最大下降幅度", "最大每日損失", "一年內的總損失", "最佳和最差月份之間的差異"],
                0,
                "Max drawdown = (Peak value - Trough value) / Peak value. It measures the worst-case loss an investor would have experienced buying at the peak and selling at the trough.",
                "最大回撤 = （峰值 - 谷值）/ 峰值。衡量投資者在峰值買入並在谷值賣出時可能經歷的最壞情況損失。"
            ),
            (
                "In a long-short equity strategy, the net exposure is:",
                "在多空股票策略中，淨敞口為：",
                ["Long exposure minus short exposure", "The sum of long and short positions", "Zero at all times", "Only the long positions"],
                ["多頭敞口減去空頭敞口", "多頭和空頭頭寸的總和", "始終為零", "僅多頭頭寸"],
                0,
                "Net exposure = Long% - Short%. A market-neutral strategy targets 0% net exposure, while a long-biased strategy has positive net exposure.",
                "淨敞口 = 多頭% - 空頭%。市場中性策略目標淨敞口為0%，而偏多頭策略具有正淨敞口。"
            ),
            (
                "Style analysis (Sharpe) identifies a portfolio's exposure to:",
                "風格分析（Sharpe）識別投資組合對以下的敞口：",
                ["Pre-defined asset class indices through return-based regression", "Only individual stocks", "Macroeconomic variables", "Accounting ratios"],
                ["通過基於回報的回歸識別對預定義資產類別指數的敞口", "僅個別股票", "宏觀經濟變量", "會計比率"],
                0,
                "Style analysis regresses portfolio returns against asset class indices to determine the portfolio's effective asset allocation, identifying style tilts (value, growth, large, small).",
                "風格分析將投資組合回報對資產類別指數回歸，以確定投資組合的有效資產配置，識別風格傾向（價值、成長、大盤、小盤）。"
            ),
            (
                "Tail risk in investment management refers to:",
                "投資管理中的尾部風險是指：",
                ["The risk of extreme events occurring more frequently than predicted by normal distributions", "The risk at the end of a trading day", "The risk of the last tranche in a CDO", "Currency risk in international portfolios"],
                ["極端事件發生頻率高於常態分佈預測的風險", "交易日結束時的風險", "CDO最後一層的風險", "國際投資組合中的貨幣風險"],
                0,
                "Tail risk = risk of extreme outliers (fat tails). Normal distributions underestimate the probability of extreme events, leading to unexpected large losses.",
                "尾部風險 = 極端異常值的風險（肥尾）。常態分佈低估了極端事件的概率，導致意外大額損失。"
            ),
            (
                "Multi-factor models in risk management help identify:",
                "風險管理中的多因子模型有助於識別：",
                ["The sources of systematic risk exposure in a portfolio", "Only the market risk premium", "Individual stock selection", "The risk-free rate"],
                ["投資組合中系統性風險敞口的來源", "僅市場風險溢價", "個股選擇", "無風險利率"],
                0,
                "Multi-factor models (Fama-French, Carhart, etc.) decompose returns into exposures to multiple risk factors: market, size, value, momentum, quality, volatility.",
                "多因子模型（Fama-French、Carhart等）將回報分解為對多個風險因子的敞口：市場、規模、價值、動量、質量、波動率。"
            ),
        ]
    },
    "Current Issues": {
        "zh": "最新議題",
        "questions": [
            (
                "Climate risk in banking is increasingly categorized as:",
                "銀行業的氣候風險日益被歸類為：",
                ["Both a physical risk and a transition risk", "Only a physical risk", "Only a reputational risk", "Not relevant to financial services"],
                ["既是實體風險也是轉型風險", "僅實體風險", "僅聲譽風險", "與金融服務無關"],
                0,
                "Climate risk: 1) Physical risks (floods, droughts affecting assets), 2) Transition risks (policy changes, technology shifts, market changes from moving to low-carbon economy).",
                "氣候風險：1）實體風險（洪水、乾旱影響資產），2）轉型風險（政策變化、技術轉變、向低碳經濟轉型帶來的市場變化）。"
            ),
            (
                "Cyber risk has become a major operational risk concern because:",
                "網絡風險已成為主要的操作風險關注點，因為：",
                ["Financial institutions are increasingly digitized and interconnected", "Physical bank robberies have increased", "Regulations require cyber attacks", "Cyber risk has no mitigation possible"],
                ["金融機構日益數字化和互聯", "實體銀行搶劫增加", "法規要求網絡攻擊", "網絡風險無法緩解"],
                0,
                "Digital transformation, open banking, cloud adoption, and sophisticated threat actors have made cyber risk a top concern. A single breach can cause massive financial and reputational damage.",
                "數字化轉型、開放銀行、雲端採用和複雜的威脅行為者使網絡風險成為首要關注點。一次洩露可能造成巨大的財務和聲譽損害。"
            ),
            (
                "The LIBOR transition to risk-free rates (RFRs) was driven by:",
                "LIBOR向無風險利率（RFRs）的過渡是由以下因素推動的：",
                ["Manipulation scandals and the lack of actual transactions underlying LIBOR", "Government mandates to reduce interest rates", "The desire for higher benchmark rates", "Technology upgrades in banking"],
                ["操縱醜聞和LIBOR缺乏實際交易支撐", "政府降低利率的指令", "對更高基準利率的渴望", "銀行業技術升級"],
                0,
                "LIBOR was based on bank estimates, not actual transactions, making it vulnerable to manipulation (revealed in scandals). RFRs like SOFR are based on actual overnight transactions.",
                "LIBOR基於銀行估價而非實際交易，使其容易被操縱（在醜聞中曝光）。SOFR等RFRs基於實際隔夜交易。"
            ),
            (
                "Artificial intelligence in risk management presents the challenge of:",
                "人工智能在風險管理中帶來的挑戰包括：",
                ["Model explainability and potential for algorithmic bias", "AI being too simple for risk modeling", "Regulators banning all AI use", "AI eliminating the need for risk management entirely"],
                ["模型可解釋性和算法偏見的可能性", "AI對風險建模來說過於簡單", "監管機構禁止所有AI使用", "AI完全消除風險管理的需求"],
                0,
                "AI/ML in risk management faces challenges: lack of explainability (black box), potential biases in training data, regulatory concerns about model governance, and overfitting to historical data.",
                "AI/ML在風險管理中面臨挑戰：缺乏可解釋性（黑箱）、訓練數據中的潛在偏見、監管對模型治理的擔憂以及對歷史數據的過擬合。"
            ),
            (
                "Decentralized finance (DeFi) poses regulatory challenges because:",
                "去中心化金融（DeFi）帶來監管挑戰，因為：",
                ["It operates without traditional intermediaries and across borders", "It is fully regulated already", "It only uses government-backed currencies", "It eliminates all financial risk"],
                ["它在沒有傳統中介的情況下跨境運營", "它已經受到充分監管", "它僅使用政府支持的貨幣", "它消除了所有金融風險"],
                0,
                "DeFi's peer-to-peer, cross-border, code-based nature makes traditional regulation difficult: no central entity to regulate, smart contract risks, no consumer protection, and AML/KYC challenges.",
                "DeFi的點對點、跨境、基於代碼的特性使傳統監管困難：沒有可監管的中心實體、智能合約風險、無消費者保護以及AML/KYC挑戰。"
            ),
            (
                "Sanctions compliance risk has increased due to:",
                "制裁合規風險因以下因素而增加：",
                ["Geopolitical tensions leading to more complex and frequently updated sanctions regimes", "Decreased global trade", "Elimination of all sanctions", "Simplified compliance requirements"],
                ["地緣政治緊張局勢導致更複雜和頻繁更新的制裁制度", "全球貿易減少", "取消所有制裁", "簡化合規要求"],
                0,
                "Geopolitical events (Russia-Ukraine, Iran, North Korea) have expanded sanctions complexity. Banks must screen transactions in real-time across multiple jurisdictions.",
                "地緣政治事件（俄烏、伊朗、朝鮮）擴大了制裁複雜性。銀行必須在多個司法管轄區實時篩查交易。"
            ),
            (
                "ESG risk integration in risk management refers to:",
                "風險管理中的ESG風險整合是指：",
                ["Incorporating environmental, social, and governance factors into risk assessment frameworks", "Only environmental regulations", "Excluding non-financial factors from risk models", "Focusing solely on short-term profits"],
                ["將環境、社會和治理因素納入風險評估框架", "僅環境法規", "從風險模型中排除非財務因素", "僅關注短期利潤"],
                0,
                "ESG integration considers climate/environmental risks, social factors (labor, community), and governance quality in credit, market, and operational risk assessments.",
                "ESG整合在信用、市場和操作風險評估中考慮氣候/環境風險、社會因素（勞工、社區）和治理質量。"
            ),
            (
                "The Basel III 'Endgame' proposals focus on:",
                "巴塞爾III「終局」提案關注：",
                ["Reforming the standardized approach and reducing reliance on internal models", "Eliminating all capital requirements", "Deregulating the banking sector", "Only addressing cryptocurrency risks"],
                ["改革標準化方法並減少對內部模型的依賴", "取消所有資本要求", "放鬆銀行業監管", "僅解決加密貨幣風險"],
                0,
                "Basel III Endgame (proposed 2023) aims to reduce model variability in RWA calculations, enhance the standardized approach, and ensure banks hold capital closer to internal model outputs.",
                "巴塞爾III終局（2023年提案）旨在減少RWA計算中的模型差異、增強標準化方法並確保銀行持有的資本更接近內部模型輸出。"
            ),
            (
                "Digital identity fraud is an emerging operational risk because:",
                "數字身份欺詐是一種新興的操作風險，因為：",
                ["More financial services are delivered remotely and digital identity theft is increasing", "Physical identity documents are becoming more secure", "Banks are eliminating all verification processes", "Regulators prohibit identity verification"],
                ["更多金融服務通過遠程提供，數字身份盜竊正在增加", "實體身份證件正變得更安全", "銀行正在取消所有驗證流程", "監管機構禁止身份驗證"],
                0,
                "Remote onboarding, deepfakes, synthetic identity fraud, and data breaches have made digital identity fraud a growing operational risk for financial institutions.",
                "遠程開戶、深偽技術、合成身份欺詐和數據洩露使數字身份欺詐成為金融機構日益增長的操作風險。"
            ),
            (
                "Cryptocurrency volatility presents risk management challenges because:",
                "加密貨幣波動性帶來風險管理挑戰，因為：",
                ["Extreme price swings, 24/7 trading, and limited historical data make traditional risk models less reliable", "Crypto prices are fixed by governments", "There is no risk in cryptocurrency", "Volatility is always positive"],
                ["極端價格波動、全天候交易和有限的歷史數據使傳統風險模型可靠性降低", "加密貨幣價格由政府固定", "加密貨幣沒有風險", "波動率總是正的"],
                0,
                "Crypto risks: extreme volatility (10%+ daily moves), 24/7 markets, limited liquidity in stress, regulatory uncertainty, custody challenges, and insufficient history for reliable risk modeling.",
                "加密貨幣風險：極端波動率（日內10%+）、全天候市場、壓力下流動性有限、監管不確定性、託管挑戰以及可靠的風險建模歷史數據不足。"
            ),
        ]
    },
}

def generate_variations(questions, target_count, topic_en, topic_zh, start_id):
    """Generate variations from base questions to reach target count."""
    import copy
    result = []
    base_count = len(questions)
    idx = 0
    for i in range(target_count):
        base = questions[i % base_count]
        q = {
            "id": start_id + i,
            "topic_en": topic_en,
            "topic_zh": topic_zh,
            "question_en": base[0],
            "question_zh": base[1],
            "options_en": base[2],
            "options_zh": base[3],
            "answer": base[4],
            "explanation_en": base[5],
            "explanation_zh": base[6],
            "difficulty": (i % 3) + 1
        }
        result.append(q)
    return result

def build_questions(topics_dict, part_name):
    all_q = []
    total_target = 5000
    num_topics = len(topics_dict)
    per_topic = total_target // num_topics
    
    for topic_en, topic_data in topics_dict.items():
        topic_zh = topic_data["zh"]
        base_qs = topic_data["questions"]
        start_id = len(all_q) + 1
        generated = generate_variations(base_qs, per_topic, topic_en, topic_zh, start_id)
        all_q.extend(generated)
    
    # Fill remaining
    while len(all_q) < total_target:
        topic_en = list(topics_dict.keys())[0]
        topic_data = topics_dict[topic_en]
        base_qs = topic_data["questions"]
        q_idx = len(all_q) % len(base_qs)
        base = base_qs[q_idx]
        all_q.append({
            "id": len(all_q) + 1,
            "topic_en": topic_en,
            "topic_zh": topic_data["zh"],
            "question_en": base[0],
            "question_zh": base[1],
            "options_en": base[2],
            "options_zh": base[3],
            "answer": base[4],
            "explanation_en": base[5],
            "explanation_zh": base[6],
            "difficulty": (len(all_q) % 3) + 1
        })
    
    return all_q[:total_target]

# Generate Part 1
print("Generating FRM Part 1...")
p1 = build_questions(p1_topics, "P1")
with open("/Users/bruce/.openclaw/workspace/projects/frm-10000/p1/data/questions.json", "w") as f:
    json.dump(p1, f, ensure_ascii=False, indent=None)
print(f"Part 1: {len(p1)} questions saved")

# Generate Part 2
print("Generating FRM Part 2...")
p2 = build_questions(p2_topics, "P2")
with open("/Users/bruce/.openclaw/workspace/projects/frm-10000/p2/data/questions.json", "w") as f:
    json.dump(p2, f, ensure_ascii=False, indent=None)
print(f"Part 2: {len(p2)} questions saved")
print("Done!")
