# Clearframe

Clearframe is a system that detects when human reasoning is distorted under pressure
and reframes decisions before commitment.

## Core Principle
Clearframe does not give advice.
It identifies cognitive patterns and presents counterfactual frames.
The user always decides.

## v0 Scope (Locked)
- Input: user-submitted decision or reasoning
- Detects ONE bias only: Sunk Cost Fallacy
- Explains why the bias may apply
- Presents one counterfactual framing
- No recommendations, no enforcement

## Why This Exists
Humans make predictable reasoning errors under pressure.
Clearframe acts as decision hygiene, not control.

## Status
v0 – manual prompt-driven prototype

---

## Architecture Update — Conditional LLM Consult Layer

Clearframe now supports a gated intelligence layer designed for safe hybrid reasoning.

### Design Principle
LLMs are never used by default.  
They are consulted only when:

- explain=True
- signal confidence is within the ambiguity band

This ensures:
- deterministic outputs remain fast and reliable
- no unnecessary LLM cost
- no hallucination risk during clear cases

### Decision Flow

Input
 ↓
Heuristic Classifier
 ↓
Signal Strength
 ↓
Conservative Gate
 ↓
IF ambiguous AND explain=True
      → consult LLM
ELSE
      → return deterministic result

### Why This Matters

This architecture mirrors production decision systems:

- deterministic logic handles clear cases
- probabilistic models assist only uncertain ones

This provides:
- scalability
- reliability
- explainability
- cost control

### Current Status

✔ Deterministic engine complete  
✔ Explain mode complete  
✔ Ambiguity consult hook implemented  
✔ All tests passing  

LLM integration layer currently stubbed for safe development.
