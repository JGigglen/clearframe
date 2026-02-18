from typing import Optional
from .schemas import EngineOutput

class ClearframeEngine:
    SILENCE_THRESHOLD = 0.3
    DETERMINISTIC_MAX = 0.8

    def __init__(self, llm_client):
        self.llm = llm_client

    def analyze(self, text: str, bias_type: str, strength: float) -> EngineOutput:
        # 1. Deterministic Gate: Absolute Silence
        if strength < self.SILENCE_THRESHOLD or bias_type == "UNKNOWN":
            return EngineOutput(intervention_type="NO", bias_context=bias_type)

        # 2. Strategic Intervention Logic
        if strength >= self.DETERMINISTIC_MAX:
            i_type = "YES"
        else:
            i_type = "SOFT"

        # 3. LLM Consult (The Reframe)
        reframe_data = self.llm.generate_reframe({"bias_context": bias_type})

        # 4. Discipline Enforcement
        question = reframe_data.get("counterfactual", "")
        if "should" in question.lower() or "recommend" in question.lower():
            question = f"How would you view this {bias_type} if you started from scratch?"

        return EngineOutput(
            intervention_type=i_type,
            bias_context=bias_type,
            counterfactual=question,
            rationale=reframe_data.get("rationale")
        )
