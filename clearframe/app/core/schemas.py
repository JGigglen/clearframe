from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict

class Classification(str, Enum):
    YES = "YES"
    POSSIBLY = "POSSIBLY"
    NO = "NO"

class Intervention(str, Enum):
    YES = "YES"
    SOFT = "SOFT"
    NO = "NO"

class LLMSuggestion(BaseModel):
    classification: Classification
    rationale: str

class DecisionExtract(BaseModel):
    core_decision: str = Field(..., min_length=1)
    past_investments: List[str] = Field(default_factory=list)
    proposed_next_action: Optional[str] = None

class Detection(BaseModel):
    classification: Classification
    reasoning: str
    counterfactual: Optional[str] = None
    llm_suggestion: Optional[LLMSuggestion] = None

class EngineOutput(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    extract: Optional[DecisionExtract] = None
    detection: Detection
    intervention: Optional[Intervention] = None
    intervention_text: Optional[str] = None