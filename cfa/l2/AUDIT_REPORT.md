# CFA Level 2 Question Bank — Audit Report

**Date:** 2026-06-13  
**File:** `cfa/l2/data/questions.json`  
**Total Questions:** 8,497  
**Topics:** 10 | **Subtopics:** 89

---

## Executive Summary

The CFA L2 question bank has **critical structural issues** that must be fixed before use:

1. **Answer distribution is catastrophically skewed** — 90–100% of correct answers are option A across all topics
2. **1,076 questions have mismatched numbers** between English and Chinese versions
3. **164 duplicate question texts** generate 611 repeated questions
4. **766 consecutive same-topic-same-answer pairs** make patterns predictable
5. **Topic weights deviate** from official CFA L2 curriculum in 4 of 10 topics
6. **~1,116 questions lack [L2-xxx] tags**
7. **~96 questions are L1-style definition recall**, inappropriate for L2

---

## 1. Topic Translations & Official Weights

### Current Topic Names

| topic_id | topic_zh | topic_en (current) | topic_en (official CFA L2) | Status |
|---|---|---|---|---|
| ethics | 道德與專業標準 | Ethical and Professional Standards | Ethical & Professional Standards | ⚠️ Minor naming |
| quant | 量化方法 | Quantitative Methods | Quantitative Methods | ✅ |
| economics | 經濟學 | Economics | Economics | ✅ |
| fsa | 財務報表分析 | Financial Statement Analysis | Financial Statement Analysis | ✅ |
| corporate | 企業發行人 | Corporate Issuers | Corporate Issuers | ✅ |
| equity | 股票投資 | Equity Investments | Equity Valuation | ❌ Should be "Equity Valuation" |
| fixed_income | 固定收益 | Fixed Income | Fixed Income | ✅ |
| derivatives | 衍生工具 | Derivatives | Derivatives | ✅ |
| alternatives | 另類投資 | Alternative Investments | Alternative Investments | ✅ |
| portfolio | 投資組合管理 | Portfolio Management | Portfolio Management | ✅ |

### Official CFA L2 Exam Weight Compliance

| Topic | Count | Actual % | Official Weight | Status |
|---|---|---|---|---|
| Ethical & Professional Standards | 1,000 | 11.8% | 10–15% | ✅ |
| Quantitative Methods | 497 | 5.8% | 5–10% | ✅ |
| Economics | 933 | 11.0% | 5–10% | ⚠️ Over target |
| Financial Statement Analysis | 912 | 10.7% | 10–15% | ✅ |
| Corporate Issuers | 933 | 11.0% | 5–10% | ⚠️ Over target |
| Equity Valuation | 689 | 8.1% | 10–15% | ⚠️ Under target |
| Fixed Income | 876 | 10.3% | 10–15% | ✅ |
| Derivatives | 790 | 9.3% | 5–10% | ✅ |
| Alternative Investments | 873 | 10.3% | 5–10% | ⚠️ Over target |
| Portfolio Management | 994 | 11.7% | 10–15% | ✅ |

**Recommended rebalancing:**
- **Reduce:** Economics (933→~600), Corporate (933→~600), Alternatives (873→~550)
- **Increase:** Equity Valuation (689→~900)
- Net: redistribute ~800 questions

### Required Changes

1. **Rename `equity.topic_en`** from "Equity Investments" → "Equity Valuation" (L2 official name)
2. **Add exam weight percentages** to `topic_zh` and `topic_en` fields, e.g.:
   - `topic_en`: `"Ethical & Professional Standards (10-15%)"`
   - `topic_zh`: `"道德與專業標準 (10-15%)"`
3. **Rebalance question counts** to match official weights

---

## 2. Answer Distribution — CRITICAL

**This is the most severe issue in the bank.**

| Topic | A (%) | B (%) | C (%) | D (%) |
|---|---|---|---|---|
| ethics | 90% | 10% | 0% | 0% |
| quant | 100% | 0% | 0% | 0% |
| economics | 90% | 0% | 5% | 4% |
| fsa | 94% | 5% | 0% | 0% |
| corporate | 100% | 0% | 0% | 0% |
| equity | 100% | 0% | 0% | 0% |
| fixed_income | 100% | 0% | 0% | 0% |
| derivatives | 100% | 0% | 0% | 0% |
| alternatives | 100% | 0% | 0% | 0% |
| portfolio | 100% | 0% | 0% | 0% |

**Impact:** Students can score 90%+ by always choosing A. The bank is unusable in current form.

**Fix:** Redistribute answers so each option (A/B/C/D) is the correct answer ~25% of the time per topic. Minimum target: no option >35% or <15%.

---

## 3. EN/ZH Number Mismatches — CRITICAL

**1,076 questions** have different numbers between English and Chinese versions.

### Examples

| ID | English | Chinese |
|---|---|---|
| 15 | Annuity pays **$544**/year for **9** years at **7%** | 年金每年支付**$496**，持續**9**年，折現率**8%** |
| 17 | **10**-year zero-coupon bond, YTM **5%** | **11**年期零息債券，YTM **3%** |
| 41 | Mean **50**, SD **10.0**, at least **75%** | 均值**43**，標準差**11**，至少**70%** |
| 61 | Strike **$47**, underlying **$55** | 執行價**$56**，標的價**$58** |
| 64 | Strike **$49**, underlying **$45** | 執行價**$54**，標的價**$41** |

**Impact:** Students working in different languages get different questions with different answers. Explains wrong answers will also mismatch.

**Fix:** Align all numbers between EN and ZH versions. Run automated extraction of all numeric values and reconcile.

---

## 4. Question Translation Accuracy

### Assessment
- **Structure:** Most questions follow consistent format with `[L2-Qxxx]` tags
- **Tagging:** 7,381 of 8,497 questions have `[L2-xxx]` tags (87%); 1,116 are untagged
- **Translation quality:** Generally good for non-numeric content; translations are natural and accurate
- **Terminology:** Financial terms correctly translated (e.g., 權益乘數 for equity multiplier, 追蹤誤差 for tracking error)

### Issues Found
- **1,076 number mismatches** (see §3 above)
- **1,116 questions missing [L2-xxx] tags** — inconsistent formatting
- Some ZH questions have slightly different phrasing that changes meaning

---

## 5. Answer Translation Accuracy

### Assessment
- Answer options generally translate correctly
- Options maintain the same meaning across languages
- Some answer options in ZH are more verbose than EN equivalents

### Issues
- The answer distribution skew (§2) affects both languages equally
- Some ZH options use different numerical values than EN (tied to §3)

---

## 6. Explanation Clarity & Completeness

### Assessment
- **193 questions** have explanations under 30 characters (very terse)
- Most explanations correctly show the calculation or reasoning
- Explanations are bilingual and generally well-translated

### Sample Terse Explanations

| ID | Explanation |
|---|---|
| 449 | "E(X) = np = 20 × 0.3 = 7" |
| 1856 | "SE = σ/√n = 11/√39 = 12/7 = 2" |
| 1540 | "P/E = $40/$2 = 20" |

**Issues:**
- Some explanations only show the formula result without reasoning
- Mathematical errors in some explanations (e.g., ID 1856: 11/√39 ≠ 12/7)
- Explanations for mismatched questions (§3) will reference wrong numbers

**Fix:** Expand terse explanations to include reasoning steps. Verify mathematical correctness.

---

## 7. Difficulty Level

### Current Distribution

| Level | Count | % |
|---|---|---|
| 1 (Easy) | 1,255 | 14% |
| 2 (Medium) | 3,607 | 42% |
| 3 (Hard) | 3,635 | 42% |

**Assessment:** L2 should emphasize analysis and application (Level 2+3). Current 86% at Level 2+3 is reasonable, but:

### Concerns
- **96 questions are L1-style definition recall** (e.g., "What is the definition of VaR?", "2 and 20 fee structure?")
- **1,255 Level 1 questions** — many may be too simple for L2 exam standard
- CFA L2 is entirely item-set based (vignettes), but only **98 questions** reference case/scenario context

**Sample L1-difficulty questions inappropriate for L2:**

| ID | Question | Issue |
|---|---|---|
| 1624 | "Coupon 4%, market rates rise to 7%. Bond price will:" | Basic L1 concept |
| 347 | "Real estate Cap Rate calculation?" | Simple recall |
| 3940 | "Definition of VaR?" | Pure definition |
| 3205 | "'2 and 20' fee structure?" | Simple recall |

**Fix:** Re-evaluate difficulty levels. Convert L1-style questions to L2 application format (scenario-based). Consider removing or upgrading the 96 definition-recall questions.

---

## 8. Mathematical Notation

**893 questions** use plain-text math notation instead of proper symbols.

### Examples
- "alpha" → should be "α"
- "beta" → should be "β"  
- "sigma" → should be "σ"
- "mu" → should be "μ"

**Impact:** Minor readability issue. Not blocking but should be standardized.

**Fix:** Run find-and-replace for common math terms → Unicode symbols.

---

## 9. Duplicate Detection

### Exact Duplicates
- **164 unique duplicate question texts**
- **611 questions affected** (7.2% of bank)

### Top Duplicates

| Count | Question Pattern |
|---|---|
| 31× | "Call option strike $50, underlying $55.0 Option status?" |
| 24× | "Put option strike $50, underlying $45.0 Intrinsic value?" |
| 21× | "What is the 'high water mark' in hedge fund fees?" |
| 17× | "EPS=$2, price=$40.0 P/E ratio?" |
| 13× | "SD = 13, sample size = 36.0 Standard error?" |
| 12× | "Mean 50, SD 10.0 Chebyshev: at least 75% of data falls within what range?" |

**Impact:** Reduces effective question pool. Students see identical questions in practice.

**Fix:** Remove duplicates, keeping one instance per unique question text. For template-based questions (e.g., option pricing), parameterize and vary the inputs.

---

## 10. Consecutive Similar Questions

**766 consecutive pairs** share the same topic AND same correct answer.

### Distribution by Topic

| Topic | Consecutive pairs |
|---|---|
| portfolio | 107 |
| corporate | 91 |
| economics | 88 |
| alternatives | 82 |
| ethics | 81 |
| fixed_income | 78 |
| fsa | 74 |
| derivatives | 64 |
| equity | 62 |
| quant | 39 |

### Longest Streaks

| Length | Topic | Answer | Starting ID |
|---|---|---|---|
| 5 | economics | A | 7441 |
| 5 | alternatives | A | 8009 |
| 4 | portfolio | A | 7392 |
| 4 | fixed_income | A | 4698 |
| 4 | economics | A | 7758 |
| 4 | corporate | A | 3412 |

**Impact:** Students can detect patterns (especially since all answers are A). Combined with §2, this makes the bank trivially gameable.

**Fix:** Shuffle questions so no two consecutive questions share the same topic. Ensure answer rotation within topic blocks.

---

## Priority Action Items

### P0 — Critical (Blocks use)

| # | Issue | Action | Effort |
|---|---|---|---|
| 1 | Answer skew (90-100% are A) | Redistribute all correct answers to ~25% per option | High |
| 2 | 1,076 EN/ZH number mismatches | Reconcile numbers in both language versions | High |

### P1 — High (Significant quality impact)

| # | Issue | Action | Effort |
|---|---|---|---|
| 3 | 611 duplicate questions | Deduplicate, keeping one instance | Medium |
| 4 | 766 consecutive same-answer pairs | Reshuffle question order | Low |
| 5 | Topic weight deviations | Rebalance counts: ↓Econ/Corp/Alts, ↑Equity | Medium |
| 6 | `equity.topic_en` naming | Rename "Equity Investments" → "Equity Valuation" | Low |

### P2 — Medium (Quality improvements)

| # | Issue | Action | Effort |
|---|---|---|---|
| 7 | 1,116 untagged questions | Add [L2-xxx] tags to all questions | Medium |
| 8 | 96 L1-style definition questions | Convert to L2 application format or remove | Medium |
| 9 | 193 terse explanations | Expand with reasoning steps | Low |
| 10 | Add exam weight % to topic fields | Update topic_zh and topic_en | Low |

### P3 — Low (Polish)

| # | Issue | Action | Effort |
|---|---|---|---|
| 11 | 893 plain-text math symbols | Replace with Unicode (α, β, σ, μ, √) | Low |
| 12 | Mathematical errors in explanations | Verify and correct calculations | Low |

---

## Summary Statistics

| Metric | Value |
|---|---|
| Total questions | 8,497 |
| Topics | 10 |
| Subtopics | 89 |
| Questions with [L2-xxx] tag | 7,381 (87%) |
| EN/ZH number mismatches | 1,076 (12.7%) |
| Duplicate question texts | 164 (611 questions) |
| Consecutive same-topic-same-answer pairs | 766 |
| Questions with answer = A | ~8,200 (~96%) |
| L1-style definition questions | 96 |
| Questions with terse explanations (<30 chars) | 193 |
| Questions with plain-text math | 893 |

---

*Report generated automatically. Manual review recommended before implementing fixes.*
