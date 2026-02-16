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
    Deterministic planner.

    Converts a ticket into a fixed execution plan.
    No intelligence.
    No randomness.
    """

    steps = [
        Step(1, "Validate ticket structure"),
        Step(2, "Analyze request"),
        Step(3, "Select execution strategy"),
        Step(4, "Prepare output artifact"),
    ]

    return Plan(
        ticket_id=ticket.ticket_id,
        steps=steps,
    )
