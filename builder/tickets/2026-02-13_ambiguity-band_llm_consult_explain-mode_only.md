# Ambiguity-band LLM consult (explain-mode only)

## Goal
Add optional LLM annotation only when signal is ambiguous and explain=True.

## Acceptance Criteria
- Silent mode unchanged (returns Classification only).
- Explain mode can include optional llm_suggestion metadata.
- No LLM calls unless explain=True and signal is in the ambiguity band.

## Files Likely Affected
- clearframe/app/core/engine.py
- clearframe/app/core/llm.py
- clearframe/app/core/schemas.py

## Tests To Add
- Test that LLM is never called in silent mode.
- Test that LLM is called only in ambiguity band when explain=True.
