from typing import Protocol, Dict, Any

class LLM(Protocol):
    def complete_json(self, prompt: str) -> Dict[str, Any]:
        ...


class NoopLLM:
    """
    Placeholder. Returns empty, forcing heuristic behavior.
    """
    def complete_json(self, prompt: str) -> Dict[str, Any]:
        return {}
