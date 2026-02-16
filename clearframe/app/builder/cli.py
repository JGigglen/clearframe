from __future__ import annotations
import argparse
import sys
from pathlib import Path

# --- THE MISSING IMPORT ---
from .loop import run_local_loop
from .replay import show_last_run  # <--- Make sure this is here!

def _repo_root_from_here() -> Path:
    return Path(__file__).resolve().parents[3]

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="clearframe-builder")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # run command
    run_p = sub.add_parser("run", help="Run ticket loop")
    run_p.add_argument("--repo-root", default=None)
    run_p.add_argument("--simulate-failure", action="store_true", help="Force a failure at step 2")
    # replay command
    sub.add_parser("replay", help="Show last run summary")

    args = parser.parse_args(argv)

    if args.cmd == "run":
        repo_root = Path(args.repo_root).resolve() if args.repo_root else _repo_root_from_here()
        
        # 1. Capture the flag from the user
        # We turn the True/False flag into "Step 2" or "Nothing"
        fail_id = 2 if args.simulate_failure else None
        
        # 2. Pass it into the loop
        result = run_local_loop(repo_root, fail_step_id=fail_id)
        
        print(f"processed={result.processed}")
        print(f"run_dir={result.run_dir}")
        return 0

    if args.cmd == "replay":
        repo_root = _repo_root_from_here()
        runs_dir = repo_root / "clearframe" / "tickets" / "runs"
        # Now that it's imported, this won't crash!
        show_last_run(runs_dir) 
        return 0

    return 2

if __name__ == "__main__":
    # Note: Using sys.argv[1:] is standard for passing arguments to main
    sys.exit(main(sys.argv[1:]))