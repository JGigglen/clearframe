from app.core.engine import analyze
from app.core.schemas import Classification, Intervention

def test_explicit_sunk_cost_yes():
    text = "I should keep going because I’ve already spent a year on this, and quitting now would mean all that effort was wasted."
    out = analyze(text)
    assert out.detection.classification in (Classification.YES, Classification.POSSIBLY)
    assert out.intervention in (Intervention.YES, Intervention.SOFT)

def test_bias_awareness_possibly():
    text = "Am I continuing just because I’ve already invested time?"
    out = analyze(text)
    assert out.detection.classification == Classification.POSSIBLY
    assert out.intervention == Intervention.SOFT

def test_counterfactual_no():
    text = "If I ignore the time I’ve already spent, does this still make sense?"
    out = analyze(text)
    assert out.detection.classification == Classification.NO
    assert out.intervention == Intervention.NO

def test_empty_input_silent():
    out = analyze("")
    assert out.detection.classification == Classification.NO
