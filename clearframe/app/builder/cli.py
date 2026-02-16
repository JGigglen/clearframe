from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .loop import run_local_loop
from .replay import show_last_run


def _repo_root_from_here() -> Path:
    return Path(__file__).resolve().parents[3]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="clearframe-builder")
    sub = parser.add_subparsers(dest="cmd", required=True)

    run_p = sub.add_parser("run")
    run_p.add_argument("--repo-root", default=None)

    # 1. Add subcommand (from screenshot)
    sub.add_parser("replay", help="Show last run summary.")

    args = parser.parse_args(argv)

    if args.cmd == "run":
        repo_root = Path(args.repo_root).resolve() if args.repo_root else _repo_root_from_here()
        result = run_local_loop(repo_root)
        print(f"processed={result.processed}")
        print(f"run_dir={result.run_dir}")
        return 0

    # 2. Inside command handler (from screenshot)
    elif args.cmd == "replay":
        repo_root = _repo_root_from_here()
        runs_dir = repo_root / "clearframe" / "tickets" / "runs"
        show_last_run(runs_dir)
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
