from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List


@dataclass(frozen=True)
class Ticket:
    ticket_id: str
    title: str
    body: str
    source_path: str


def list_ticket_files(inbox_dir: Path) -> List[Path]:
    if not inbox_dir.exists():
        return []
    files = [p for p in inbox_dir.iterdir() if p.is_file() and p.suffix.lower() == ".json"]
    return sorted(files, key=lambda p: p.name.lower())


def load_ticket(path: Path) -> Ticket:
    data: Dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))

    ticket_id = str(data.get("id", path.stem)).strip()
    title = str(data.get("title", "")).strip()
    body = str(data.get("body", "")).strip()

    if not ticket_id:
        raise ValueError(f"Ticket missing id: {path}")
    if not title:
        raise ValueError(f"Ticket missing title: {path}")
    if not body:
        raise ValueError(f"Ticket missing body: {path}")

    return Ticket(ticket_id=ticket_id, title=title, body=body, source_path=str(path))
