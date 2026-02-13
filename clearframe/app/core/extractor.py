from .schemas import DecisionExtract
import re

def extract_decision(text: str) -> DecisionExtract:
    """
    Minimal but real extraction:
    - Pull first decision-like sentence
    - Do not infer intent
    """

    clean = " ".join(text.strip().split())

    # Sentence split (very conservative)
    sentences = re.split(r"[.!?]", clean)
    candidate = sentences[0].strip() if sentences else clean

    core = candidate if len(candidate) <= 140 else candidate[:137] + "..."

    past = []
    lowered = clean.lower()
    if any(k in lowered for k in ["already", "spent", "invested", "put in", "years", "months"]):
        past.append("User references past investment.")

    return DecisionExtract(
        core_decision=core or clean[:140],
        past_investments=past,
        proposed_next_action=None
    )
