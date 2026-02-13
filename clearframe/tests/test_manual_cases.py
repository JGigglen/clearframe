from clearframe.app.core.engine import analyze
from clearframe.app.core.schemas import Classification, EngineOutput


def test_explicit_sunk_cost_yes_silent():
    text = (
        "I should keep going because I've already spent a year on this, "
        "and quitting now would mean all that effort was wasted."
    )

    result = analyze(text)

    assert isinstance(result, Classification)
    assert result in (Classification.YES, Classification.POSSIBLY)


def test_explicit_sunk_cost_yes_explain():
    text = (
        "I should keep going because I've already spent a year on this, "
        "and quitting now would mean all that effort was wasted."
    )

    result = analyze(text, explain=True)

    assert isinstance(result, EngineOutput)
    assert result.detection.classification in (
        Classification.YES,
        Classification.POSSIBLY,
    )
    assert isinstance(result.detection.reasoning, str)
    assert result.intervention is not None


def test_bias_awareness_possibly_explain():
    text = "Am I continuing just because I've already invested time?"

    result = analyze(text, explain=True)

    assert result.detection.classification == Classification.POSSIBLY


def test_counterfactual_no_silent():
    text = "If I ignore the time I've already spent, does this still make sense?"

    result = analyze(text)

    assert result == Classification.NO


def test_empty_input_silent_is_no():
    result = analyze("   ")

    assert result == Classification.NO


def test_empty_input_explain_has_reasoning_and_no_intervention():
    result = analyze("   ", explain=True)

    assert result.detection.classification == Classification.NO
    assert "No decision content" in result.detection.reasoning
    assert result.intervention is None
