from __future__ import annotations
from typing import Optional, Dict, Any
from dataclasses import dataclass
from .llm import get_llm, LLMClient

@dataclass(frozen=True)
class EngineOutput:
    """The unified contract for all Clearframe outputs."""
    detection: str
    confidence: float
    intervention_type: str  # YES, POSSIBLY, NO
    analysis: Optional[str] = None
    counterfactual: Optional[str] = None

class ClearframeEngine:
    def __init__(self, llm_client: Optional[LLMClient] = None):
        # Use provided client (for tests) or the global getter
        self.llm = llm_client or get_llm()
        # Constitutional Threshold: Silence below this signal
        self.SILENCE_THRESHOLD = 0.3

    def analyze(self, text: str, bias_type: str, signal_strength: float) -> EngineOutput:
        """
        Processes text through the Constitutional Gate.
        Respects 'Silence-First' by returning early on low signal.
        """
        # 1. The Constitutional Gate
        if signal_strength < self.SILENCE_THRESHOLD:
            return EngineOutput(
                detection=bias_type,
                confidence=signal_strength,
                intervention_type="NO",
                analysis="Signal below threshold. Silence maintained."
            )

        # 2. Intelligence Routing (The Switchboard)
        # Call the unified v0.2 LLM contract
        analysis_text = self.llm.analyze_bias(text, bias_type)
        reframe_data = self.llm.generate_reframe({
            "text": text,
            "bias_context": bias_type
        })

        # 3. Deterministic Intervention Mapping
        # High signal = YES, Mid signal = POSSIBLY
        intervention = "YES" if signal_strength >= 0.6 else "POSSIBLY"

        return EngineOutput(
            detection=bias_type,
            confidence=signal_strength,
            intervention_type=intervention,
            analysis=analysis_text,
            counterfactual=reframe_data.get("counterfactual")
        )