from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import List

from .ticket_io import load_ticket
from .planner import build_plan
from .executor import execute_plan


# ---------- Result Schema ----------

@dataclass(frozen=True)
class LoopResult:
    processed: int
    run_dir: str


# ---------- Helpers ----------

def _runs_dir(repo_root: Path) -> Path:
    return repo_root / "clearframe" / "tickets" / "runs"


def _incoming_dir(repo_root: Path) -> Path:
    return repo_root / "clearframe" / "tickets" / "incoming"


def _timestamp() -> str:
    from datetime import datetime
    return datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")


# ---------- Main Loop ----------

def run_local_loop(
    repo_root: Path,
    fail_step_id: int | None = None,
) -> LoopResult:
    """
    Deterministic local ticket loop.
    """
    incoming = _incoming_dir(repo_root)
    runs_root = _runs_dir(repo_root)

    incoming.mkdir(parents=True, exist_ok=True)
    runs_root.mkdir(parents=True, exist_ok=True)

    # New run folder for this execution
    run_dir = runs_root / _timestamp()
    run_dir.mkdir(parents=True, exist_ok=True)

    processed = 0

    # Iterate tickets
    for path in sorted(incoming.glob("*.json")):
        # --- FIX 1: Ignore files that are already 'done' ---
        if ".done" in path.name:
            continue

        ticket = load_ticket(path)
        plan = build_plan(ticket)

        # Unique ID for failure tests to keep index clean
        effective_id = f"{plan.ticket_id}-FAIL" if fail_step_id else plan.ticket_id

        # Execute plan (this will now create the 'workspace' folder)
        result = execute_plan(
            ticket_id=effective_id,
            steps=plan.steps,
            run_dir=run_dir,
            fail_step_id=fail_step_id,
        )

        # --- FIX 2: Use .replace() to avoid Windows "FileExistsError" ---
        archive = path.with_suffix(".done.json")
        path.replace(archive)

        processed += 1

    return LoopResult(
        processed=processed,
        run_dir=str(run_dir),
    )
