from .schemas import (
    Classification,
    Intervention,
    Detection,
    DecisionExtract,
    EngineOutput,
)
from .extractor import extract_decision
from .detector import heuristic_classification, sunk_cost_signal
from .gate import conservative_gate, intervention_for_classification


def analyze(text: str, explain: bool = False):
    """
    Layer 1 (default): returns Classification only
    Layer 2 (explain=True): returns EngineOutput
    """

    # ---------------- Guard: empty or invalid input ----------------
    if not isinstance(text, str) or not text.strip():
        if not explain:
            return Classification.NO

        det = Detection(
            classification=Classification.NO,
            reasoning="No decision content provided.",
        )

        return EngineOutput(
            extract=None,
            detection=det,
            intervention=None,
            intervention_text=None,
        )

    # ---------------- Core analysis ----------------
    extract = extract_decision(text)

    base_class = heuristic_classification(text)
    signal = sunk_cost_signal(text)

    final_class = conservative_gate(signal, base_class)

    # ---------------- Layer 1: silent mode ----------------
    if not explain:
        return final_class

    # ---------------- Layer 2: explain mode ----------------
    counterfactual = None
    if final_class == Classification.YES:
        counterfactual = (
            "If this were presented today with zero prior investment, "
            "what evidence would justify continuing from this point?"
        )

    reasoning = _reasoning_for(final_class, signal)

    det = Detection(
        classification=final_class,
        reasoning=reasoning,
        counterfactual=counterfactual,
    )

    intervention = intervention_for_classification(final_class)

    intervention_text = _build_intervention_text(final_class, counterfactual)

    return EngineOutput(
        extract=extract,
        detection=det,
        intervention=intervention,
        intervention_text=intervention_text,
    )


def _reasoning_for(c: Classification, signal: float) -> str:
    if c == Classification.NO:
        return f"Signal {signal:.2f}: insufficient evidence of sunk-cost-driven reasoning."
    if c == Classification.POSSIBLY:
        return f"Signal {signal:.2f}: some sunk-cost indicators present, but evidence is ambiguous."
    return f"Signal {signal:.2f}: past investment appears to justify future action."


def _build_intervention_text(
    c: Classification, counterfactual: str | None
) -> str | None:
    if c == Classification.YES:
        return (
            "**Past investment shouldn't drive future decisions.**\n\n"
            "This reasoning relies on unrecoverable costs rather than expected future value.\n\n"
            f"**Reframe:** {counterfactual}"
        )

    if c == Classification.POSSIBLY:
        return (
            "You're already questioning whether past investment is influencing this.\n\n"
            "If none of the past effort could be recovered, would your next step change?"
        )

    return None
def should_consult_llm(signal: float, explain: bool) -> bool:
    """
    Returns True only when:
    - explain mode is on
    - signal is in ambiguity band
    """

    if not explain:
        return False

    return 0.4 <= signal <= 0.6
