from .schemas import Classification, Intervention

def intervention_for_classification(c: Classification) -> Intervention:
    if c == Classification.YES:
        return Intervention.YES
    if c == Classification.POSSIBLY:
        return Intervention.SOFT
    return Intervention.NO


def conservative_gate(signal: float, model_class: Classification) -> Classification:
    """
    Gate is the final authority.
    Silence-first, but hedges on disagreement.
    """

    # Weak signal: silence
    if signal < 0.35:
        return Classification.NO

    # Strong heuristic, model says NO → hedge
    if signal >= 0.75 and model_class == Classification.NO:
        return Classification.POSSIBLY

    # Moderate signal cannot support YES
    if signal < 0.65 and model_class == Classification.YES:
        return Classification.POSSIBLY

    # Moderate POSSIBLY still downgraded
    if signal < 0.50 and model_class == Classification.POSSIBLY:
        return Classification.NO

    return model_class
