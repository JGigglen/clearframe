from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import List


@dataclass(frozen=True)
class RunLog:
    run_id: str
    timestamp_utc: str
    processed: int
    artifacts: List[str]


def write_run_log(run_dir: Path, processed: int, artifacts: List[str]) -> str:
    """
    Writes deterministic log for a loop execution.
    Returns log file path.
    """

    run_id = run_dir.name

    log = RunLog(
        run_id=run_id,
        timestamp_utc=datetime.now(timezone.utc).isoformat(),
        processed=processed,
        artifacts=artifacts,
    )

    path = run_dir / "run_log.json"
    path.write_text(json.dumps(asdict(log), indent=2), encoding="utf-8")

    return str(path)
