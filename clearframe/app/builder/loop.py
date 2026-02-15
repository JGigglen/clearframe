from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import List

from .ticket_io import Ticket, list_ticket_files, load_ticket


@dataclass(frozen=True)
class LoopResult:
    processed: int
    run_dir: str
    artifacts: List[str]


def run_local_loop(repo_root: Path) -> LoopResult:
    tickets_dir = repo_root / "clearframe" / "tickets"
    inbox_dir = tickets_dir / "inbox"
    runs_dir = tickets_dir / "runs"

    files = list_ticket_files(inbox_dir)

    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir = runs_dir / ts
    run_dir.mkdir(parents=True, exist_ok=True)

    artifacts: List[str] = []
    for p in files:
        t: Ticket = load_ticket(p)

        artifact = {
            "id": t.ticket_id,
            "title": t.title,
            "body": t.body,
            "source_path": t.source_path,
            "status": "DRY_RUN",
        }

        out_path = run_dir / f"{t.ticket_id}.artifact.json"
        out_path.write_text(json.dumps(artifact, indent=2, sort_keys=True), encoding="utf-8")
        artifacts.append(str(out_path))

    return LoopResult(processed=len(files), run_dir=str(run_dir), artifacts=artifacts)
