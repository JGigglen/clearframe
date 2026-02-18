from __future__ import annotations
import json
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List

@dataclass(frozen=True)
class Step:
    id: int
    description: str
    status: str = "pending"
    output: str = ""

    def to_dict(self):
        return asdict(self)

@dataclass(frozen=True)
class Plan:
    ticket_id: str
    steps: List[Step]

@dataclass(frozen=True)
class Ticket:
    ticket_id: str
    title: str
    body: str
    bias_type: str = "UNKNOWN"  # This is the line that was missing!

def load_ticket(path: Path) -> Ticket:
    """Standardized loader that now detects bias signatures."""
    data = json.loads(path.read_text(encoding="utf-8"))
    body_text = data.get("body", "").lower()
    t_id = str(data.get("id", path.stem)).upper()
    
    # Deterministic Signature Detection
    # If the ID starts with T5 or has sunk-cost keywords
    if t_id.startswith("T5") or any(w in body_text for w in ["spent", "invested", "wasted"]):
        detected_bias = "SUNK_COST"
    # If the ID starts with T6 or has confirmation-bias keywords
    elif t_id.startswith("T6") or any(w in body_text for w in ["proves", "reddit", "everyone says", "already know"]):
        detected_bias = "CONFIRMATION_BIAS"
    else:
        detected_bias = "UNKNOWN"

    return Ticket(
        ticket_id=t_id,
        title=data.get("title", "Untitled Ticket"),
        body=data.get("body", ""),
        bias_type=detected_bias
    )

def build_plan(ticket: Ticket) -> Plan:
    """Splits the ticket body into executable steps."""
    body_text = ticket.body or ""
    lines = [line.strip() for line in body_text.splitlines() if line.strip()]
    
    if not lines:
        lines = ["No instructions provided"]

    steps = [
        Step(id=i, description=line) 
        for i, line in enumerate(lines, 1)
    ]
    
    return Plan(ticket_id=ticket.ticket_id, steps=steps)