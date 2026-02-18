import pytest
from clearframe.app.core.engine import ClearframeEngine
from clearframe.app.core.llm import MockClient

@pytest.fixture
def engine():
    # We use the MockClient to test logic without spending Gemini credits
    return ClearframeEngine(llm_client=MockClient())

def test_silence_on_low_signal(engine):
    """CONSTITUTION: Must remain silent if signal < 0.3"""
    output = engine.analyze("This is a normal sentence.", "UNKNOWN", 0.1)
    assert output.intervention_type == "NO"
    assert output.counterfactual is None

def test_no_recommendation_language(engine):
    """CONSTITUTION: Counterfactuals must be questions, never commands."""
    output = engine.analyze("I'm biased!", "SUNK_COST", 0.8)
    # Counterfactuals must end with a question mark
    assert output.counterfactual.strip().endswith("?")
    # They should not use 'pushy' advice words
    text = output.counterfactual.lower()
    assert "should" not in text
    assert "must" not in text

def test_single_reframe_only(engine):
    """CONSTITUTION: Exactly one reframing question max."""
    output = engine.analyze("I'm biased!", "CONFIRMATION_BIAS", 0.7)
    # Verify exactly one question mark to prevent rambling
    assert output.counterfactual.count("?") == 1