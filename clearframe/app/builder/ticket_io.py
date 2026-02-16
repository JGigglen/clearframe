from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List


VALID_STATUSES = {"pending", "processed", "failed"}


@dataclass(frozen=True)
class Ticket:
    ticket_id: str
    title: str
    body: str
    status: str
    source_path: str


# ---------------------------------------------------------
# List Tickets
# ---------------------------------------------------------
def list_ticket_files(inbox_dir: Path) -> List[Path]:
    if not inbox_dir.exists():
        return []

    files = [
        p for p in inbox_dir.iterdir()
        if p.is_file() and p.suffix.lower() == ".json"
    ]

    return sorted(files, key=lambda p: p.name.lower())


# ---------------------------------------------------------
# Load Ticket
# ---------------------------------------------------------
def load_ticket(path: Path) -> Ticket:
    data: Dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))

    ticket_id = str(data.get("id", path.stem)).strip()
    title = str(data.get("title", "")).strip()
    body = str(data.get("body", "")).strip()
    status = str(data.get("status", "pending")).strip().lower()

    if not ticket_id:
        raise ValueError(f"Ticket missing id: {path}")

    if not title:
        raise ValueError(f"Ticket missing title: {path}")

    if not body:
        raise ValueError(f"Ticket missing body: {path}")

    if status not in VALID_STATUSES:
        raise ValueError(f"Invalid ticket status '{status}' in {path}")

    return Ticket(
        ticket_id=ticket_id,
        title=title,
        body=body,
        status=status,
        source_path=str(path)
    )


# ---------------------------------------------------------
# Update Ticket Status
# ---------------------------------------------------------
def update_ticket_status(path: Path, new_status: str) -> None:
    if new_status not in VALID_STATUSES:
        raise ValueError(f"Invalid status: {new_status}")

    data = json.loads(path.read_text(encoding="utf-8"))
    data["status"] = new_status

    path.write_text(
        json.dumps(data, indent=2, sort_keys=True),
        encoding="utf-8"
    )
