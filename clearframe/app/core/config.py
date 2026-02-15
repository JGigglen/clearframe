from pydantic import BaseModel


class EngineConfig(BaseModel):
    confidence_threshold: float = 0.75
    ambiguity_threshold: float = 0.4

    # whether engine is allowed to consult LLM
    allow_llm: bool = True

    # safety guard — forces silence instead of uncertain output
    conservative_mode: bool = True
