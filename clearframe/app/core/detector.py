from __future__ import annotations

from typing import List, Dict
from .schemas import Classification


# =========================================================
# Centralized Heuristic Knowledge Base
# =========================================================

HEURISTICS: Dict[str, List[str]] = {
    "past": [
        "already", "spent", "put in", "invested",
        "after all", "so much", "previously"
    ],

    "time_effort": [
        "month", "year", "time", "effort",
        "work", "energy", "money", "capital"
    ],

    "obligation": [
        "so i should", "so i must", "so i have to",
        "therefore i should",
        "can't quit", "can't stop", "committed to"
    ],

    "waste": [
        "waste", "wasted", "for nothing",
        "thrown away", "loss", "losing"
    ]
}


# =========================================================
# Evidence Extraction
# =========================================================

def detect_evidence(text: str) -> List[str]:
    """
    Returns human-readable evidence explaining why a signal fired.
    Used for explain mode only.
    """
    t = text.lower()
    evidence: List[str] = []

    for category, keywords in HEURISTICS.items():
        for word in keywords:
            if word in t:
                evidence.append(f"{category}:{word}")

    return evidence


# =========================================================
# Signal Strength (0.0 → 1.0)
# =========================================================

def sunk_cost_signal(text: str) -> float:
    """
    Conservative normalized signal in [0,1].
    Weighted factors with interaction boost.
    """

    t = text.lower()

    factors = {
        key: any(k in t for k in words)
        for key, words in HEURISTICS.items()
    }

    weights = {
        "past": 0.30,
        "time_effort": 0.20,
        "obligation": 0.35,
        "waste": 0.40
    }

    score = sum(weights[k] for k, v in factors.items() if v)

    # decisive interaction
    if factors["waste"] and factors["obligation"]:
        score = max(score, 0.85)

    return min(score, 1.0)


# =========================================================
# Deterministic Classification
# =========================================================

def heuristic_classification(text: str) -> Classification:
    t = text.lower()

    # ---------- Layer 0: explicit neutralization ----------
    neutralizers = [
        "if i ignore",
        "zero prior",
        "without the time",
        "regardless of"
    ]

    if any(n in t for n in neutralizers):
        return Classification.NO

    # ---------- Layer 1: self-awareness ----------
    if (
        ("am i" in t or "is my desire" in t)
        and "because" in t
        and ("already" in t or "invested" in t)
    ):
        return Classification.POSSIBLY

    # ---------- Layer 2: signal thresholds ----------
    s = sunk_cost_signal(text)

    if s >= 0.85:
        return Classification.YES

    if s >= 0.50:
        return Classification.POSSIBLY

    return Classification.NO


# =========================================================
# Reasoning Generator (Explain Mode Only)
# =========================================================

def reasoning_string(text: str) -> str:
    """
    Produces structured explanation text
    showing exactly what triggered detection.
    """

    evidence = detect_evidence(text)

    if not evidence:
        return "No sunk-cost indicators detected."

    joined = ", ".join(evidence)
    return f"Detected indicators → {joined}"
