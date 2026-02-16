from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import List

from .ticket_io import Ticket, list_ticket_files, load_ticket
from .planner import build_plan
from .executor import execute_plan
from .planner_rules import build_steps_from_text


@dataclass(frozen=True)
class LoopResult:
    processed: int
    run_dir: str
    artifacts: List[str]


def run_local_loop(repo_root: Path) -> LoopResult:
    """
    Deterministic local agent loop.

    Reads tickets from:
        clearframe/tickets/inbox/*.json

    Produces execution artifacts in:
        clearframe/tickets/runs/<timestamp>/
    """

    tickets_dir = repo_root / "clearframe" / "tickets"
    inbox_dir = tickets_dir / "inbox"
    runs_dir = tickets_dir / "runs"

    # collect ticket files
    files = list_ticket_files(inbox_dir)

    # create run folder
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir = runs_dir / ts
    run_dir.mkdir(parents=True, exist_ok=True)

    artifacts: List[str] = []

    # process tickets deterministically
    for path in files:
        ticket: Ticket = load_ticket(path)

        # PLAN
        plan = build_plan(ticket)

        # EXECUTE
        result = execute_plan(
            ticket_id=ticket.ticket_id,
            steps=build_steps_from_text(ticket.body),
            run_dir=run_dir,
        )

        artifacts.append(result.artifact_path)
    
    from .logger import write_run_log
    write_run_log(run_dir, len(artifacts), artifacts)

    from .run_index import append_run
    append_run(runs_dir, run_dir, len(artifacts))


    return LoopResult(
        processed=len(files),
        run_dir=str(run_dir),
        artifacts=artifacts,
    )
