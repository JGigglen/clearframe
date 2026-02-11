# Clearframe Manual Tests — Sunk Cost Bias

Purpose:
Verify that Clearframe intervenes correctly and conservatively.

---

## Test 001 — Explicit Sunk Cost

Input:
"I’ve already spent six months here, so I should keep going."

Expected Classification:
YES

Expected Intervention:
YES

---

## Test 002 — Bias Awareness

Input:
"Am I continuing this just because I’ve already put time into it?"

Expected Classification:
POSSIBLY

Expected Intervention:
SOFT

---

## Test 003 — Counterfactual Reasoning

Input:
"If I ignore the time I’ve already invested, does this still make sense?"

Expected Classification:
NO

Expected Intervention:
NO
