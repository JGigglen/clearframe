from __future__ import annotations

import json
from pathlib import Path
from typing import List, Dict


INDEX_NAME = "index.json"


def _index_path(runs_dir: Path) -> Path:
    return runs_dir / INDEX_NAME


def load_index(runs_dir: Path) -> List[Dict]:
    """
    Loads run index.
    Returns empty list if none exists.
    """
    path = _index_path(runs_dir)

    if not path.exists():
        return []

    return json.loads(path.read_text(encoding="utf-8"))


def append_run(runs_dir: Path, run_dir: Path, processed: int) -> None:
    """
    Adds a run entry to index.json
    """

    runs_dir.mkdir(parents=True, exist_ok=True)

    index = load_index(runs_dir)

    entry = {
        "run_id": run_dir.name,
        "path": str(run_dir),
        "processed": processed,
    }

    index.append(entry)

    _index_path(runs_dir).write_text(
        json.dumps(index, indent=2),
        encoding="utf-8",
    )
