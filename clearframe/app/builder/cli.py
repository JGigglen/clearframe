from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .loop import run_local_loop


def _repo_root_from_here() -> Path:
    return Path(__file__).resolve().parents[3]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="clearframe-builder")
    sub = parser.add_subparsers(dest="cmd", required=True)

    run_p = sub.add_parser("run")
    run_p.add_argument("--repo-root", default=None)

    args = parser.parse_args(argv)

    if args.cmd == "run":
        repo_root = Path(args.repo_root).resolve() if args.repo_root else _repo_root_from_here()
        result = run_local_loop(repo_root)
        print(f"processed={result.processed}")
        print(f"run_dir={result.run_dir}")
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
