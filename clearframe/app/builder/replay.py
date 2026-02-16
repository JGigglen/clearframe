from __future__ import annotations

import json
from pathlib import Path


def show_last_run(runs_dir: Path) -> None:
    index_path = runs_dir / "index.json"

    if not index_path.exists():
        print("No runs recorded.")
        return

    runs = json.loads(index_path.read_text(encoding="utf-8"))

    if not runs:
        print("Run index empty.")
        return

    last = runs[-1]

    print("Last Run")
    print("--------")
    print(f"id: {last['run_id']}")
    print(f"path: {last['path']}")
    print(f"processed: {last['processed']}")
