# Clearframe

Clearframe is a deterministic reasoning analysis engine that detects when human decisions are influenced by cognitive bias and reframes them before commitment.

It does **not** give advice.  
It detects patterns and presents counterfactual frames.  
The human always decides.

---

## Core Principle

Clearframe is decision hygiene, not decision control.

It exists because humans make predictable reasoning errors under pressure.  
Clearframe identifies those patterns before action is taken.

---

## v0 Scope (Locked)

Current supported capability:

- Input: natural-language reasoning
- Detects one bias: **Sunk Cost Fallacy**
- Explains why bias may apply
- Provides one counterfactual frame
- Returns structured output
- Silent mode available
- No recommendations
- No enforcement
- Deterministic by default

---

## Architecture

Clearframe is intentionally built **logic-first, not model-first**.

Input
↓
Feature Extraction
↓
Heuristic Classifier
↓
Signal Strength
↓
Conservative Gate
↓
Optional LLM Consult
↓
Structured Output

---

## Conditional Intelligence Layer

LLMs are never used automatically.

They are consulted only when:

- explain=True
- confidence falls inside ambiguity band

This guarantees:

- deterministic speed
- zero hallucination risk in clear cases
- reduced cost
- explainability
- predictable behavior

LLMs act as advisors — never decision makers.

---

## Execution Loop System

Clearframe now includes a deterministic execution loop.

Ticket → Loop Runner → Engine → Artifact


The loop:

- reads ticket files
- analyzes reasoning
- writes structured results
- preserves run history
- produces reproducible outputs

This is the foundation for autonomous reasoning agents.

---

## Current Status

**v0.1 — Engine Stable**

Completed:

- deterministic engine
- signal scoring
- conservative gate
- schema-validated outputs
- LLM adapter interface
- explain mode
- full test suite
- execution loop
- artifact system

All tests passing.

---

## Design Philosophy

Clearframe is built under strict engineering rules:

- deterministic first
- tests before intelligence
- scaffolding before automation
- minimal abstraction
- modular boundaries
- conservative outputs

Intelligence is added only after correctness is proven.

---

## Long-Term Direction

Clearframe is being developed as a general reasoning-quality analysis engine capable of:

- detecting cognitive bias
- auditing reasoning chains
- evaluating decisions
- assisting human judgment safely

---

## Author

JGigglen


