from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import List

from clearframe.app.builder.ticket_io import Ticket, list_ticket_files, load_ticket
from clearframe.app.core.engine import analyze


@dataclass(frozen=True)
class LoopResult:
    processed: int
    run_dir: str
    artifacts: List[str]


def run_local_loop(repo_root: Path) -> LoopResult:
    """
    Deterministic execution loop.

    Reads tickets → runs engine → writes artifacts
    """

    tickets_dir = repo_root / "clearframe" / "tickets"
    inbox_dir = tickets_dir / "inbox"
    runs_dir = tickets_dir / "runs"

    files = list_ticket_files(inbox_dir)

    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir = runs_dir / ts
    run_dir.mkdir(parents=True, exist_ok=True)

    artifacts: List[str] = []

    for path in files:
        ticket: Ticket = load_ticket(path)

        # -------------------------
        # ENGINE EXECUTION
        # -------------------------
        result = analyze(ticket.body, explain=True)

        # -------------------------
        # SERIALIZE RESULT
        # -------------------------
        artifact = {
            "ticket_id": ticket.ticket_id,
            "title": ticket.title,
            "classification": result.detection.classification.value,
            "reasoning": result.detection.reasoning,
            "counterfactual": result.detection.counterfactual,
            "llm_used": result.detection.llm_suggestion is not None,
        }

        out_path = run_dir / f"{ticket.ticket_id}.artifact.json"
        out_path.write_text(
            json.dumps(artifact, indent=2, sort_keys=True),
            encoding="utf-8"
        )

        artifacts.append(str(out_path))

    return LoopResult(
        processed=len(files),
        run_dir=str(run_dir),
        artifacts=artifacts
    )
