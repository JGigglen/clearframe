from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .ticket_io import Ticket


# ---------- Data Structures ----------

@dataclass(frozen=True)
class Step:
    id: int
    description: str


@dataclass(frozen=True)
class Plan:
    ticket_id: str
    steps: List[Step]


# ---------- Planner ----------

def build_plan(ticket: Ticket) -> Plan:
    """
    Dynamic planner.
    Converts each line of the ticket body into an execution step.
    """
    
    # 1. Get the body text and split it into lines
    body_text = ticket.body or ""
    lines = [line.strip() for line in body_text.splitlines() if line.strip()]

    # 2. Convert lines into Step objects
    steps: List[Step] = []
    for i, line in enumerate(lines, 1):
        steps.append(Step(id=i, description=line))

    # 3. Fallback: If the ticket is empty, give it a default step
    if not steps:
        steps.append(Step(id=1, description="No instructions provided in ticket body"))

    return Plan(
        ticket_id=ticket.ticket_id,
        steps=steps,
    )