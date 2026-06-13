# FRM Part 2 Question Bank — Audit Report

**Date:** 2026-06-13
**File:** `frm/p2/data/questions.json`
**Total Questions:** 5,000

---

## Summary

| Check | Status | Notes |
|-------|--------|-------|
| Topic weights | ✅ FIXED | Rebalanced to official exam weights |
| Answer distribution | ✅ FIXED | Was 98.3% option 0 → now ~25% each |
| Question uniqueness | 🔴 CRITICAL | Only 60 unique question texts (see §4) |
| Required fields | ✅ Pass | All 11 fields present in all questions |
| Duplicate IDs | ✅ Pass | All 5,000 IDs unique |
| Options count | ✅ Pass | All questions have exactly 4 options |
| Answer range | ✅ Pass | All answers ∈ {0, 1, 2, 3} |
| Chinese content | ✅ Pass | All zh fields populated |
| Explanation quality | ✅ Pass | All explanations ≥ 20 chars |
| Difficulty range | ✅ Pass | Values: 1, 2, 3 (evenly distributed ~33%) |

---

## 1. Topic Distribution — FIXED ✅

**Exam weights applied:**

| Topic | Before | After | Target |
|-------|--------|-------|--------|
| Market Risk | 835 (16.7%) | 1,000 (20.0%) | 20% |
| Credit Risk | 833 (16.7%) | 1,000 (20.0%) | 20% |
| Operational Risk | 833 (16.7%) | 1,000 (20.0%) | 20% |
| Liquidity and Treasury Risk | 833 (16.7%) | 750 (15.0%) | 15% |
| Risk Management and Investment Management | 833 (16.7%) | 750 (15.0%) | 15% |
| Current Issues | 833 (16.7%) | 500 (10.0%) | 10% |

**Method:** Downsampled topics above target, upsampled (duplicated with new IDs) topics below target.

---

## 2. Answer Distribution — FIXED ✅

### Before (CRITICAL skew)
| Option | Count | % |
|--------|-------|---|
| 0 | 4,917 | 98.3% |
| 1 | 0 | 0.0% |
| 2 | 0 | 0.0% |
| 3 | 83 | 1.7% |

### After (balanced)
| Option | Count | % |
|--------|-------|---|
| 0 | 1,251 | 25.0% |
| 1 | 1,267 | 25.3% |
| 2 | 1,237 | 24.7% |
| 3 | 1,245 | 24.9% |

**Method:** For each question, swapped option text so the correct answer is repositioned to the target slot, preserving semantic correctness.

**Per-topic balance (after):**
- Credit Risk: 0:248 | 1:261 | 2:244 | 3:247
- Current Issues: 0:120 | 1:134 | 2:117 | 3:129
- Liquidity and Treasury Risk: 0:187 | 1:189 | 2:182 | 3:192
- Market Risk: 0:245 | 1:255 | 2:250 | 3:250
- Operational Risk: 0:261 | 1:241 | 2:257 | 3:241
- Risk Management and Investment Management: 0:190 | 1:187 | 2:187 | 3:186

---

## 3. Standard Quality Checks — All Pass ✅

- **Required fields:** All 11 fields (`id`, `topic_en`, `topic_zh`, `question_en`, `question_zh`, `options_en`, `options_zh`, `answer`, `explanation_en`, `explanation_zh`, `difficulty`) present in every question.
- **Duplicate IDs:** None — all 5,000 IDs unique and sequential (1–5000).
- **Options:** All questions have exactly 4 options in both EN and ZH.
- **Answer validity:** All answers are integers in [0, 3].
- **Chinese content:** Zero missing ZH questions, explanations, or options.
- **Explanation quality:** All ≥ 20 characters.
- **Duplicate option text within a question:** None found.

---

## 4. 🔴 CRITICAL: Question Uniqueness

**Only 60 unique question texts exist across 5,000 entries.**

Each unique question is duplicated approximately 80–107 times with different IDs.

Top duplicated questions:
| Count | Question (truncated) |
|-------|---------------------|
| 107× | "Operational risk under Basel is defined as the risk of loss from:" |
| 104× | "Risk-weighted assets (RWAs) for market risk under the standardized approach..." |
| 104× | "In the CreditMetrics framework, credit migration refers to:" |
| 104× | "The maximum loss on a long call option position is:" |
| 103× | "Business continuity planning (BCP) aims to:" |
| 103× | "A credit spread represents:" |
| 103× | "A recovery rate of 40% means:" |

**Impact:** This makes the question bank nearly useless for exam preparation — users will see the same ~60 questions repeated dozens of times.

**Root cause:** The original generation appears to have created only 60 questions and then duplicated them with different IDs to reach 5,000.

**Recommendation:** This question bank needs to be regenerated with 5,000 genuinely unique questions. The current 60 questions can serve as seed templates but are insufficient.

---

## 5. Topic–Language Mapping

| English | Chinese |
|---------|---------|
| Credit Risk | 信用風險 |
| Current Issues | 最新議題 |
| Liquidity and Treasury Risk | 流動性與財務風險 |
| Market Risk | 市場風險 |
| Operational Risk | 操作風險 |
| Risk Management and Investment Management | 風險管理與投資管理 |

All mappings are consistent across all questions.

---

## 6. Difficulty Distribution

| Difficulty | Count | % |
|-----------|-------|---|
| 1 (Easy) | 1,661 | 33.2% |
| 2 (Medium) | 1,680 | 33.6% |
| 3 (Hard) | 1,659 | 33.2% |

Evenly distributed across all topics.

---

## Changes Made

1. **Answer distribution rebalanced** — Swapped option positions so correct answers are evenly distributed across options 0–3 (was 98.3% on option 0).
2. **Topic counts rebalanced** — Adjusted to match FRM Part 2 official exam weights (Market/Credit/OpRisk at 20%, Liquidity/RiskMgmt at 15%, Current Issues at 10%).
3. **IDs reassigned** — Sequential 1–5000 after rebalancing.

## Outstanding Issue (Requires Regeneration)

⚠️ **The question bank has only 60 unique questions.** This cannot be fixed by data manipulation — the questions need to be regenerated from scratch to provide meaningful exam prep value.
