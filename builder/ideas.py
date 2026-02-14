# Hardcoded feature ideas for Step 1 (no LLM calls).

IDEAS = [
    {
        "title": "Ambiguity-band LLM consult (explain-mode only)",
        "goal": "Add optional LLM annotation only when signal is ambiguous and explain=True.",
        "acceptance_criteria": [
            "Silent mode unchanged (returns Classification only).",
            "Explain mode can include optional llm_suggestion metadata.",
            "No LLM calls unless explain=True and signal is in the ambiguity band.",
        ],
        "files_likely_affected": [
            "clearframe/app/core/engine.py",
            "clearframe/app/core/llm.py",
            "clearframe/app/core/schemas.py",
        ],
        "tests_to_add": [
            "Test that LLM is never called in silent mode.",
            "Test that LLM is called only in ambiguity band when explain=True.",
        ],
    },
    {
        "title": "Decision extractor upgrade (real decision sentence parsing)",
        "goal": "Improve extract_decision to identify core decision + optional next action from text.",
        "acceptance_criteria": [
            "Extract core decision sentence reliably for multi-sentence inputs.",
            "Populate DecisionExtract fields (core_decision, proposed_next_action).",
            "No behavior regression in existing engine outputs.",
        ],
        "files_likely_affected": [
            "clearframe/app/core/extractor.py",
            "clearframe/app/core/schemas.py",
        ],
        "tests_to_add": [
            "Extractor unit tests for single sentence and multi-sentence inputs.",
            "Regression tests for existing manual cases.",
        ],
    },
    {
        "title": "CLI flags: --silent / --explain / --json for run_clearframe.py",
        "goal": "Make Clearframe runner usable as a tool with structured outputs.",
        "acceptance_criteria": [
            "Default is silent classification output.",
            "--explain prints explanation + counterfactual when present.",
            "--json prints machine-readable output.",
        ],
        "files_likely_affected": [
            "run_clearframe.py",
        ],
        "tests_to_add": [
            "CLI smoke tests (optional) or minimal integration checks.",
        ],
    },
    {
        "title": "Add 'waste' and stronger obligation patterns to heuristic signal",
        "goal": "Reduce false negatives for textbook sunk-cost language while staying conservative.",
        "acceptance_criteria": [
            "Waste language increases signal strongly.",
            "YES requires stronger evidence (avoid YES on time-only language).",
            "Manual cases updated/added for new patterns.",
        ],
        "files_likely_affected": [
            "clearframe/app/core/detector.py",
            "clearframe/app/core/gate.py",
            "clearframe/tests/test_manual_cases.py",
        ],
        "tests_to_add": [
            "New manual cases for waste/obligation combos.",
            "Threshold regression tests.",
        ],
    },
    {
        "title": "Add second bias detector module scaffold",
        "goal": "Create a consistent module pattern to support more biases later (without implementing one yet).",
        "acceptance_criteria": [
            "New module scaffold mirrors sunk-cost layout (extract/detect/gate).",
            "No changes to existing behavior.",
            "Clear place to plug in new detectors later.",
        ],
        "files_likely_affected": [
            "clearframe/app/core/",
            "clearframe/app/core/schemas.py",
        ],
        "tests_to_add": [
            "Minimal scaffold test ensuring imports load.",
        ],
    },
    {
        "title": "Policy tuning: gate thresholds as config",
        "goal": "Move gate thresholds into a small config object to make calibration explicit.",
        "acceptance_criteria": [
            "Thresholds defined in one place.",
            "Behavior unchanged with default config.",
            "Easy to test alternate configs.",
        ],
        "files_likely_affected": [
            "clearframe/app/core/gate.py",
            "clearframe/app/core/engine.py",
        ],
        "tests_to_add": [
            "Test default config matches current behavior.",
            "Test alternate config changes downgrade behavior.",
        ],
    },
]
