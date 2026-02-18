import json
from pathlib import Path
from typing import List, Optional
from dataclasses import dataclass
from ..core.schemas import Ticket

@dataclass(frozen=True)
class Step:
    id: int
    description: str
    status: str = "pending"
    output: Optional[str] = None

@dataclass(frozen=True)
class Plan:
    steps: List[Step]

def load_ticket(path: Path) -> Ticket:
    raw_text = path.read_text(encoding="utf-8").strip()
    try:
        data = json.loads(raw_text)
        if not isinstance(data, dict): data = {"body": str(data)}
    except json.JSONDecodeError:
        data = {"body": raw_text}

    body_text = data.get("body", "").lower()
    t_id = str(data.get("id", path.stem)).upper()
    
    signatures = {
        "SUNK_COST": ["spent", "invested", "wasted", "already", "months"],
        "CONFIRMATION_BIAS": ["proves", "reddit", "everyone says", "already know", "tweets"],
        "RECENCY_BIAS": ["latest", "just announced", "breaking news", "today", "saw a post"],
        "AUTHORITY_BIAS": ["boss", "ceo", "vp", "director", "manager", "says so", "directive"]
    }
    
    results = []
    for bias_name, keywords in signatures.items():
        matches = sum(1 for word in keywords if word in body_text)
        strength = matches / len(keywords)
        results.append((bias_name, strength))
    
    bias, strength = max(results, key=lambda x: x[1])
    if strength == 0: bias = "UNKNOWN"

    return Ticket(
        ticket_id=t_id,
        title=data.get("title", "Untitled Ticket"),
        body=data.get("body", ""),
        bias_type=bias,
        signal_strength=round(strength, 2)
    )

def build_plan(ticket: Ticket) -> Plan:
    return Plan(steps=[Step(id=1, description="Standard execution pathway")])
