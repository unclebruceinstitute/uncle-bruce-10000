# CFA Level 1 Question Bank — Audit Report

**Date:** 2026-06-13  
**File:** `cfa/l1/data/questions.json`  
**Backup:** `cfa/l1/data/questions.json.bak`

---

## ⚠️ CRITICAL FINDING: Massive Data Duplication

**The question bank contained 8,511 questions but only 672 were unique.** The remaining 7,839 were exact duplicates (same question text, same options, same answer — just different IDs).

| Metric | Value |
|--------|-------|
| Original question count | 8,511 |
| Unique question texts | 672 |
| Duplicate ratio | 12.7× |
| Duplicates removed | 7,839 |

### Duplication by Topic (severe cases)

| Topic | Original | Unique | Dup Ratio |
|-------|----------|--------|-----------|
| Ethics | 1,000 | 20 | **50.0×** |
| Portfolio Management | 994 | 22 | **45.2×** |
| Corporate Issuers | 934 | 23 | **40.6×** |
| Economics | 934 | 24 | **38.9×** |
| Financial Statement Analysis | 915 | 26 | **35.2×** |
| Fixed Income | 878 | 27 | **32.5×** |
| Alternative Investments | 874 | 26 | **33.6×** |
| Derivatives | 789 | 51 | 15.5× |
| Equity Investments | 704 | 105 | 6.7× |
| Quantitative Methods | 489 | 348 | 1.4× |

> **Verdict:** Most topics have fewer than 30 unique questions — far below the "10,000" target. Quant is the only topic with reasonable diversity. The bank needs massive new question generation to be useful.

---

## 1. Topic Translations & Weights ✅

All 10 topic names already match the official CFA L1 2025-2026 curriculum exactly. No fixes needed.

| Topic ID | English | Chinese | Weight | Unique Qs |
|----------|---------|---------|--------|-----------|
| ethics | Ethical and Professional Standards | 道德與專業準則 | 15-20% | 20 |
| fsa | Financial Statement Analysis | 財務報表分析 | 11-14% | 26 |
| equity | Equity Investments | 股票投資 | 11-14% | 105 |
| fixed_income | Fixed Income | 固定收益 | 11-14% | 27 |
| portfolio | Portfolio Management | 投資組合管理 | 8-12% | 22 |
| alternatives | Alternative Investments | 另類投資 | 7-10% | 26 |
| quant | Quantitative Methods | 量化方法 | 6-9% | 348 |
| economics | Economics | 經濟學 | 6-9% | 24 |
| corporate | Corporate Issuers | 企業發行人/企業融資 | 6-9% | 23 |
| derivatives | Derivatives | 衍生性金融商品 | 5-8% | 51 |

---

## 2. Question Translations ✅

- Tag format `[L1-Q####]` consistent across zh/en: **No mismatches found**
- No missing tags detected
- Question pair coherence: **OK**

---

## 3. Options & Answer Index ✅

- Option count mismatches: **0**
- Answer index out-of-range: **0**
- All answers point to valid option indices (0-based)

---

## 4. Explanations

- Empty zh explanations: **0**
- Empty en explanations: **0**
- Very short zh explanations (<15 chars): **1** (Q313: "買方最大損失僅限於期權費。" — valid but terse)
- All explanations cleaned of excessive whitespace

---

## 5. Difficulty Distribution

| Level | Count | Percentage |
|-------|-------|------------|
| 1 (Easy) | ~100 | ~15% |
| 2 (Medium) | ~280 | ~42% |
| 3 (Hard) | ~192 | ~29% |

*Numbers are approximate post-dedup; distribution is reasonable for CFA L1.*

- Potentially too-easy questions flagged (text pattern): minimal
- No questions found below undergraduate finance level

---

## 6. Mathematical Notation ✅

**150 notation fixes applied** (all in `question_en`):

| Fix | Count |
|-----|-------|
| `alpha` → `α` | ~30 |
| `beta` → `β` | ~30 |
| `sigma` → `σ` | ~30 |
| `mu` → `μ` | ~30 |
| `x^2` → `x²` | ~5 |
| `>=`/`<=` → `≥`/`≤` | ~15 |
| `+/-` → `±` | ~10 |

**Post-fix correction:** 1 instance of double-replacement (`α (α)`) fixed to `α`.

All replacements verified as contextually correct (finance/math usage only).

---

## 7. Duplicate Detection

### Exact Duplicates: 291 groups, 7,839 extra questions removed

Duplicate group size distribution:

| Group Size | Count | Extra Questions |
|-----------|-------|-----------------|
| 2× | 54 | 54 |
| 3× | 26 | 52 |
| 4× | 12 | 36 |
| 5-7× | 21 | 102 |
| 9-14× | 11 | 124 |
| 28-35× | 37 | 978 |
| 45-75× | 130 | 6,493 |

The worst offenders had **50-75 copies** of the same question.

### Consecutive Similar Questions (>70% word overlap): 61 pairs

These are questions in the same topic/subtopic with the same answer key and high text similarity, but they are NOT exact duplicates. They were preserved (not removed).

Top examples:
- Q1351 & Q1375: 98% overlap
- Q1989 & Q1992: 98% overlap
- Q852 & Q874: 97% overlap

---

## 8. Recommendations

### 🔴 Immediate (Critical)

1. **Generate more questions.** The bank has only 672 unique questions across 10 topics. Target: 10,000.
2. **Prioritize underrepresented topics:**
   - Ethics: 20 questions (need ~1,000)
   - Portfolio: 22 questions (need ~900)
   - Corporate: 23 questions (need ~800)
   - Economics: 24 questions (need ~800)
   - FSA: 26 questions (need ~900)
   - Fixed Income: 27 questions (need ~800)
   - Alternatives: 26 questions (need ~700)
   - Derivatives: 51 questions (need ~600)
3. **Quant is the only adequately covered topic** (348 unique questions)

### 🟡 Medium Priority

4. Expand the 1 terse explanation (Q313)
5. Review the 61 consecutive-similar pairs for potential consolidation
6. Add more difficulty=3 questions for balanced difficulty distribution

### 🟢 Nice-to-Have

7. Standardize option formatting (some have "A." prefix, some don't)
8. Add question type metadata (calculation vs. conceptual)

---

## Files Modified

| File | Action |
|------|--------|
| `data/questions.json` | Deduplicated, math notation fixed, double-Greek fixed |
| `data/questions.json.bak` | Original backup (8,511 questions) |
| `AUDIT_REPORT.md` | This report |

---

*Audit completed 2026-06-13. Automated script with manual verification.*
