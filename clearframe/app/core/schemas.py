from dataclasses import dataclass, field
from typing import Optional, Dict, Any

@dataclass(frozen=True)
class Ticket:
    ticket_id: str
    title: str
    body: str
    bias_type: str = "UNKNOWN"
    signal_strength: float = 0.0

@dataclass(frozen=True)
class EngineOutput:
    intervention_type: str  # YES, SOFT, NO
    bias_context: str
    counterfactual: Optional[str] = None
    rationale: Optional[str] = None
    
@dataclass(frozen=True)
class RunResult:
    ticket_id: str
    status: str
    output: EngineOutput
    metadata: Dict[str, Any] = field(default_factory=dict)
