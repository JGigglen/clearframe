from __future__ import annotations

from typing import List
from .planner import Step


def build_steps_from_text(body: str) -> List[Step]:
    """
    Deterministic planner.
    Converts ticket text into steps using simple rules.
    """

    steps: List[Step] = []

    lines = [l.strip() for l in body.splitlines() if l.strip()]

    for i, line in enumerate(lines, start=1):
        steps.append(Step(id=i, description=line))

    if not steps:
        steps.append(Step(id=1, description="Review ticket content"))

    return steps
