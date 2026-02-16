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

def load_ticket(path: Path) -> Ticket:
    """Standardized loader to ensure tickets are read deterministically."""
    data = json.loads(path.read_text(encoding="utf-8"))
    return Ticket(
        ticket_id=str(data.get("id", path.stem)),
        title=data.get("title", "Untitled Ticket"),
        body=data.get("body", "")
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