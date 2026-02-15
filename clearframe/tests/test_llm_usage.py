from clearframe.app.core.engine import analyze
from clearframe.app.core.llm import LLMClient
from clearframe.app.core.schemas import Classification, LLMSuggestion


class SpyLLM(LLMClient):
    def __init__(self):
        self.called = False

    def consult_sunk_cost(self, text: str) -> LLMSuggestion:
        self.called = True
        return LLMSuggestion(
            classification=Classification.NO,
            rationale="spy"
        )


def test_llm_called_only_when_allowed():
    spy = SpyLLM()

    analyze(
        "I already spent time on this",
        explain=True,
        llm=spy
    )

    assert spy.called is True


def test_llm_not_called_in_silent_mode():
    spy = SpyLLM()

    analyze(
        "I already spent time on this",
        explain=False,
        llm=spy
    )

    assert spy.called is False
