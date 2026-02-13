from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, List


class Classification(str, Enum):
    YES = "YES"
    POSSIBLY = "POSSIBLY"
    NO = "NO"


class Intervention(str, Enum):
    YES = "YES"
    SOFT = "SOFT"
    NO = "NO"


class DecisionExtract(BaseModel):
    core_decision: str = Field(..., min_length=1)
    past_investments: List[str] = Field(default_factory=list)
    proposed_next_action: Optional[str] = None


class Detection(BaseModel):
    classification: Classification
    reasoning: str
    counterfactual: Optional[str] = None


from typing import Optional

class EngineOutput(BaseModel):
    extract: Optional[DecisionExtract]
    detection: Detection
    intervention: Intervention
    intervention_text: Optional[str] = None

