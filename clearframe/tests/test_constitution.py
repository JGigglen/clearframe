import pytest
from clearframe.app.core.engine import ClearframeEngine
from clearframe.app.core.llm import MockClient

@pytest.fixture
def engine():
    return ClearframeEngine(llm_client=MockClient())

def test_silence_on_low_signal(engine):
    """CONSTITUTION: Must remain silent if signal < 0.3"""
    output = engine.analyze("Normal sentence.", "UNKNOWN", 0.1)
    assert output.intervention_type == "NO"
    assert output.counterfactual is None

def test_no_recommendation_language(engine):
    """CONSTITUTION: Counterfactuals must be questions, never commands."""
    output = engine.analyze("I'm biased!", "SUNK_COST", 0.8)
    # Check that the output ends with a question mark and isn't a command
    assert output.counterfactual.strip().endswith("?")
    assert "should" not in output.counterfactual.lower()
    assert "must" not in output.counterfactual.lower()

def test_single_reframe_only(engine):
    """CONSTITUTION: Exactly one reframing question max."""
    output = engine.analyze("I'm biased!", "CONFIRMATION_BIAS", 0.7)
    # Ensure there isn't more than one question mark (simplistic check)
    assert output.counterfactual.count("?") == 1