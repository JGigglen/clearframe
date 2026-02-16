from __future__ import annotations

import json
import platform
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import List


@dataclass(frozen=True)
class ExecutionResult:
    artifact_path: str
    step_count: int


def execute_plan(ticket_id: str, steps: List, run_dir: Path) -> ExecutionResult:
    """
    Executes a plan in dry-run mode.

    Converts steps into JSON-safe format
    and writes execution artifact with metadata.
    """

    run_dir.mkdir(parents=True, exist_ok=True)

    # Convert steps → serializable
    safe_steps = [asdict(s) for s in steps]

    artifact = {
        "ticket_id": ticket_id,
        "status": "DRY_RUN",
        "steps": safe_steps,

        # -------- metadata --------
        "meta": {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "python_version": sys.version,
            "platform": platform.platform(),
            "clearframe_version": "0.1-dev",
        },
    }

    out_path = run_dir / f"{ticket_id}.execution.json"
    out_path.write_text(json.dumps(artifact, indent=2), encoding="utf-8")

    return ExecutionResult(
        artifact_path=str(out_path),
        step_count=len(steps),
    )


