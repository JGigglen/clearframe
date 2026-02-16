from __future__ import annotations

from typing import Optional

from .config import EngineConfig
from .extractor import extract_decision
from .detector import heuristic_classification, sunk_cost_signal
from .gate import conservative_gate, intervention_for_classification
from .schemas import Classification, Detection, EngineOutput
from .llm import LLMClient, MockLLMClient


# ---------------------------------------------------------
# LLM Consult Policy
# ---------------------------------------------------------
def should_consult_llm(signal: float, explain: bool, config: EngineConfig) -> bool:
    if not explain:
        return False

    if not config.allow_llm:
        return False

    return True


# ---------------------------------------------------------
# Reasoning helper
# ---------------------------------------------------------
def _reasoning_for(c: Classification, signal: float) -> str:
    if c == Classification.YES:
        return "Past investment is influencing the decision."
    if c == Classification.POSSIBLY:
        return "Some sunk cost indicators detected but not decisive."
    return "No sunk cost reasoning detected."


# ---------------------------------------------------------
# Main Engine
# ---------------------------------------------------------
def analyze(
    text: str,
    explain: bool = False,
    llm: Optional[LLMClient] = None,
    config: Optional[EngineConfig] = None,
):
    """
    Layer 1 → returns Classification
    Layer 2 → returns EngineOutput
    """

    # -------------------------
    # Defaults
    # -------------------------
    if config is None:
        config = EngineConfig()

    from .llm import get_llm

    if llm is None:
        llm = get_llm()


    # -------------------------
    # Guard: empty input
    # -------------------------
    if not isinstance(text, str) or not text.strip():

        if not explain:
            return Classification.NO

        det = Detection(
            classification=Classification.NO,
            reasoning="No decision content provided.",
            counterfactual=None,
            llm_suggestion=None,
        )

        return EngineOutput(
            extract=None,
            detection=det,
            intervention=None,
            intervention_text=None,
        )

    # -------------------------
    # Deterministic analysis
    # -------------------------
    extract = extract_decision(text)

    base_class = heuristic_classification(text)
    signal = sunk_cost_signal(text)

    final_class = conservative_gate(signal, base_class)

    # -------------------------
    # Silent mode contract
    # -------------------------
    if not explain:
        return final_class

    # -------------------------
    # Counterfactual
    # -------------------------
    counterfactual = None
    if final_class == Classification.YES:
        counterfactual = "If you ignored prior investment, would you still choose this?"

    reasoning = _reasoning_for(final_class, signal)

    # -------------------------
    # Optional LLM consult
    # -------------------------
    llm_note = None

    if should_consult_llm(signal, explain, config):

        raw = llm.consult_sunk_cost(text)

        from .schemas import LLMSuggestion

        if isinstance(raw, LLMSuggestion):
            llm_note = raw
        else:
            llm_note = LLMSuggestion(
                classification=final_class,
                rationale=str(raw),
            )

    # -------------------------
    # Detection object
    # -------------------------
    det = Detection(
        classification=final_class,
        reasoning=reasoning,
        counterfactual=counterfactual,
        llm_suggestion=llm_note,
    )

    intervention = intervention_for_classification(final_class)

    return EngineOutput(
        extract=extract,
        detection=det,
        intervention=intervention,
        intervention_text=None,
    )
