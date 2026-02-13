from .schemas import Classification

def sunk_cost_signal(text: str) -> float:
    """
    Conservative normalized signal in [0,1].
    Uses weighted factors instead of naive addition.
    """
    t = text.lower()

    factors = {
        "past": any(k in t for k in ["already", "spent", "put in", "invested", "after all", "so much"]),
        "time_effort": any(k in t for k in ["month", "year", "time", "effort", "work", "energy", "money"]),
        "obligation": any(k in t for k in [
            "so i should", "so i must", "so i have to",
            "therefore i should", "can't quit", "can't stop"
        ]),
        "waste": any(k in t for k in ["waste", "wasted", "for nothing", "thrown away"])
    }

    # Weighted presence (not additive explosion)
    weights = {
        "past": 0.30,
        "time_effort": 0.20,
        "obligation": 0.35,
        "waste": 0.40
    }

    score = sum(weights[k] for k, v in factors.items() if v)

    # Waste + obligation is a decisive interaction
    if factors["waste"] and factors["obligation"]:
        score = max(score, 0.85)

    return min(score, 1.0)


def heuristic_classification(text: str) -> Classification:
    t = text.lower()

    # Explicit neutralization wins
    if "if i ignore" in t or "zero prior" in t or "without the time" in t:
        return Classification.NO

    # Bias self-awareness
    if ("am i" in t or "is my desire" in t) and ("just because" in t or "because" in t) and ("already" in t or "invested" in t):
        return Classification.POSSIBLY

    s = sunk_cost_signal(text)

    if s >= 0.85:
        return Classification.YES
    if s >= 0.50:
        return Classification.POSSIBLY
    return Classification.NO
