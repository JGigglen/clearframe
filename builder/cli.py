from __future__ import annotations
import argparse
import sys
import os
from pathlib import Path

# We use relative imports (the dot) to stay inside the local folder
try:
    from .executor import execute_plan
    from .loop import run_local_loop
except ImportError:
    # Manual path injection if running as a direct script
    sys.path.append(os.path.dirname(__file__))
    from executor import execute_plan
    from loop import run_local_loop

# Optional replay
show_last_run = None
try:
    from .replay import show_last_run
except Exception:
    pass

def _get_repo_root() -> Path:
    """Finds the root by looking for the 'app' folder."""
    current_path = Path(__file__).resolve()
    for parent in current_path.parents:
        if (parent / "app").exists():
            return parent
    return Path.cwd()

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="clearframe-builder")
    sub = parser.add_subparsers(dest="cmd", required=True)

    run_p = sub.add_parser("run", help="Run the local builder loop.")
    run_p.add_argument("--repo-root", default=None, help="Path to repo root (optional).")

    if show_last_run is not None:
        sub.add_parser("replay", help="Show last run summary.")

    args = parser.parse_args(argv)
    repo_root = Path(args.repo_root).resolve() if args.repo_root else _get_repo_root()

    if args.cmd == "run":
        print(f"\n[SUCCESS] CLI Loaded. Root: {repo_root}")
        # result = run_local_loop(repo_root) # Commented for pure CLI test
        # print(f"processed={result.processed}")
        return 0

    return 2

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))