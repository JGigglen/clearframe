from typing import Optional
from .schemas import LLMSuggestion

class NoopLLM:
    def consult_sunk_cost(self, text: str) -> Optional[LLMSuggestion]:
        return None

