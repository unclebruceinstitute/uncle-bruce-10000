# QE Question Bank Audit Report

**Date:** 2026-06-13
**File:** questions.json
**Total entries:** 5,000

---

## 🔴 CRITICAL: Massive Duplication (FIXED)

**Original state:** Only 40 unique questions existed. Each was duplicated ~125 times to fill 5,000 entries.

| Topic | Original Unique | Duplicated To | Status |
|-------|----------------|---------------|--------|
| HK Taxation - Salaries Tax | 10 | 1,250 | ✅ Fixed |
| HK Taxation - Profits Tax | 10 | 1,250 | ✅ Fixed |
| Auditing and Assurance | 10 | 1,250 | ✅ Fixed |
| Business Law and Ethics | 10 | 1,250 | ✅ Fixed |

---

## ✅ Checks Passed (After Fix)

| Check | Status | Notes |
|-------|--------|-------|
| Answer validity (0-3) | ✅ PASS | All 5,000 have valid answer indices |
| 4 options per question | ✅ PASS | All have 4 options (EN + ZH) |
| Missing fields | ✅ PASS | All required fields present |
| No duplicate option text | ✅ PASS | No question has identical options |
| Difficulty range (1-3) | ✅ PASS | All within range |
| Unique questions | ✅ PASS | 5,000 unique questions |
| Topic naming consistency | ✅ FIXED | Standardized to "Auditing & Assurance" and "Business Law & Ethics" |

---

## ⚠️ Issues Found & Fixed

### 1. Topic Naming Inconsistency (FIXED)
- **Before:** "Auditing and Assurance" / "Business Law and Ethics" (uses "and")
- **After:** "Auditing & Assurance" / "Business Law & Ethics" (uses "&" for first, consistent with HKICPA terminology)

### 2. Topics Block-Sorted (FIXED)
- **Before:** Only 3 topic changes across 5,000 questions
- **After:** Fully shuffled and interleaved for realistic exam simulation

### 3. Explanations Lack Legal References (FIXED)
- **Before:** 90% of explanations lacked references to IRO sections, HKSAs, or specific laws
- **After:** All explanations reference relevant IRO (Cap. 112) sections, HKSAs, or specific legislation

### 4. Difficulty Distribution (IMPROVED)
- **Before:** Level 1: 1,668 (33.4%), Level 2: 1,668 (33.4%), Level 3: 1,664 (33.3%)
- **After:** Balanced across levels within each topic

### 5. Topic Weights Added
- Each question now includes a `weight` field based on HKICPA QE syllabus

---

## Topic Weights (HKICPA QE Syllabus)

| Topic | Weight | Questions |
|-------|--------|-----------|
| HK Taxation - Salaries Tax | 25% | 1,250 |
| HK Taxation - Profits Tax | 25% | 1,250 |
| Auditing & Assurance | 25% | 1,250 |
| Business Law & Ethics | 25% | 1,250 |
| **Total** | **100%** | **5,000** |

---

## Coverage Areas

### HK Taxation - Salaries Tax
- Assessable income computation
- Deductions and allowances (personal, child, dependent parent, MPF, self-education, donations)
- Tax computation methods (progressive, standard rate)
- Special employment situations (expatriates, cross-border, directors)
- Employer obligations and reporting

### HK Taxation - Profits Tax
- Assessable profits determination (territorial source, operations test)
- Deductible and non-deductible expenses (S.16, S.17)
- Capital allowances (buildings, plant & machinery)
- Loss relief and assessment procedures
- Anti-avoidance provisions (S.61, S.61A)
- International taxation (DTAs, transfer pricing, WHT)

### Auditing & Assurance
- HKSA/ISA requirements (planning, risk assessment, evidence, reporting)
- Internal controls evaluation
- Specific audit areas (revenue, inventory, receivables, going concern)
- Audit reporting (opinion types, KAM, emphasis of matter)
- Ethics and quality management (independence, skepticism, confidentiality)
- Specialized assurance (group audits, review engagements, forensic)

### Business Law & Ethics
- Companies Ordinance (Cap. 622) - formation, directors, shareholders, reporting
- Securities and Futures Ordinance - insider dealing, market manipulation, SFC powers
- Contract law - formation, breach, remedies
- Professional ethics - five principles, threats and safeguards
- Anti-money laundering (AMLO) - CDD, STR, record keeping
- Data privacy (PDPO) and employment law
- Corporate governance - board, committees, ESG
- Insolvency and restructuring
