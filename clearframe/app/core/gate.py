from .schemas import Classification, Intervention


def conservative_gate(signal: float, base: Classification) -> Classification:
    """
    Final authority gate.
    Conservative bias: silence when weak evidence.
    """

    # very weak evidence → NO
    if signal < 0.35:
        return Classification.NO

    # strong evidence → YES
    if signal >= 0.85:
        return Classification.YES

    # otherwise trust heuristic
    return base


def intervention_for_classification(c: Classification) -> Intervention | None:
    """
    Maps classification → intervention type
    """

    if c == Classification.YES:
        return Intervention.YES

    if c == Classification.POSSIBLY:
        return Intervention.SOFT

    return None
