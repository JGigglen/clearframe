from .schemas import EngineOutput, Detection, Classification
from .extractor import extract_decision
from .detector import heuristic_classification, sunk_cost_signal
from .gate import conservative_gate, intervention_for_classification

def build_intervention_text(c: Classification, counterfactual: str | None) -> str | None:
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


def analyze(text: str) -> EngineOutput:
    if not isinstance(text, str) or not text.strip():
        extract = extract_decision("")
        det = Detection(
            classification=Classification.NO,
            reasoning="No decision content provided."
        )
        return EngineOutput(
            extract=extract,
            detection=det,
            intervention=intervention_for_classification(Classification.NO),
            intervention_text=None
        )

    extract = extract_decision(text)

    base_class = heuristic_classification(text)
    signal = sunk_cost_signal(text)

    final_class = conservative_gate(signal, base_class)

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
        counterfactual=counterfactual
    )

    intervention = intervention_for_classification(final_class)
    intervention_text = build_intervention_text(final_class, counterfactual)

    return EngineOutput(
        extract=extract,
        detection=det,
        intervention=intervention,
        intervention_text=intervention_text
    )


def _reasoning_for(c: Classification, signal: float) -> str:
    if c == Classification.NO:
        return f"Signal {signal:.2f}: insufficient evidence of sunk-cost-driven reasoning."
    if c == Classification.POSSIBLY:
        return f"Signal {signal:.2f}: some sunk-cost indicators present, but evidence is ambiguous."
    return f"Signal {signal:.2f}: past investment appears to justify future action."
