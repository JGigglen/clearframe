import argparse
import datetime as dt
import re
from pathlib import Path

from ideas import IDEAS  # works when running: python builder/cli.py ...
from ticket_parser import parse_ticket_markdown


REPO_ROOT = Path(__file__).resolve().parents[1]
TICKETS_DIR = REPO_ROOT / "builder" / "tickets"


def slugify(text: str) -> str:
    """
    Lowercase, spaces->underscore, remove unsafe filename chars.
    Keep only a-z, 0-9, underscore, hyphen.
    Collapse repeated underscores.
    """
    s = text.strip().lower()
    s = s.replace(" ", "_")
    s = re.sub(r"[^a-z0-9_\-]+", "", s)
    s = re.sub(r"_+", "_", s)
    s = s.strip("_")
    return s or "untitled"


def brainstorm() -> int:
    for i, idea in enumerate(IDEAS, start=1):
        print(f"{i}. {idea['title']}")
    return 0


def render_ticket_md(idea: dict) -> str:
    title = idea["title"]
    goal = idea.get("goal", "").strip()
    ac = idea.get("acceptance_criteria", [])
    files = idea.get("files_likely_affected", [])
    tests = idea.get("tests_to_add", [])

    def bullets(items):
        return "\n".join([f"- {x}" for x in items]) if items else "- (fill in)"

    return (
        f"# {title}\n\n"
        f"## Goal\n"
        f"{goal or '(fill in)'}\n\n"
        f"## Acceptance Criteria\n"
        f"{bullets(ac)}\n\n"
        f"## Files Likely Affected\n"
        f"{bullets(files)}\n\n"
        f"## Tests To Add\n"
        f"{bullets(tests)}\n"
    )


def pick(index: int) -> int:
    if index < 1 or index > len(IDEAS):
        print(f"Error: pick number must be between 1 and {len(IDEAS)}")
        return 2

    idea = IDEAS[index - 1]
    slug = slugify(idea["title"])
    date_str = dt.date.today().isoformat()
    filename = f"{date_str}_{slug}.md"
    path = TICKETS_DIR / filename

    TICKETS_DIR.mkdir(parents=True, exist_ok=True)

    if path.exists():
        print(f"Ticket already exists: {path}")
        return 1

    content = render_ticket_md(idea)
    path.write_text(content, encoding="utf-8")

    print(f"Created ticket: {path}")
    return 0


def get_latest_ticket() -> Path | None:
    tickets = sorted(TICKETS_DIR.glob("*.md"))
    if not tickets:
        return None
    return tickets[-1]


def work() -> int:
    ticket = get_latest_ticket()
    if not ticket:
        print("No tickets found in builder/tickets/")
        return 1

    print(f"Using ticket: {ticket.name}\n")

    content = ticket.read_text(encoding="utf-8")

    # Parse into structured fields
    ctx = parse_ticket_markdown(content)

    print("----- STRUCTURED TICKET -----")
    print(f"Title: {ctx['title'] or '(missing title)'}\n")

    goal = ctx["goal"] or "(missing goal)"
    print("Goal:")
    print(goal)
    print()

    ac = ctx["acceptance_criteria"]
    print("Acceptance Criteria:")
    if ac:
        for item in ac:
            print(f"- {item}")
    else:
        print("- (none found)")
    print()

    files = ctx["files_likely_affected"]
    print("Files Likely Affected:")
    if files:
        for f in files:
            print(f"- {f}")
    else:
        print("- (none found)")
    print()

    tests = ctx["tests_to_add"]
    print("Tests To Add:")
    if tests:
        for t in tests:
            print(f"- {t}")
    else:
        print("- (none found)")
    print()

    print("Execution Context (what future steps will use):")
    print(ctx)
    print()

    print("Next Actions (still manual in Step 3):")
    print("- Confirm this ticket is the one you want to work on")
    print("- Turn acceptance criteria into concrete implementation tasks")
    print("- Identify the smallest PR-sized change\n")

    return 0



def main() -> int:
    parser = argparse.ArgumentParser(
        prog="builder",
        description="Feature Picker CLI: brainstorm ideas and create a ticket.",
    )

    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("brainstorm", help="Print numbered feature ideas")

    pick_p = sub.add_parser("pick", help="Pick an idea number and create a ticket file")
    pick_p.add_argument("number", type=int, help="Idea number (1-based)")

    sub.add_parser("work", help="Load latest ticket and print execution stub")

    args = parser.parse_args()

    if args.cmd == "brainstorm":
        return brainstorm()

    if args.cmd == "pick":
        return pick(args.number)

    if args.cmd == "work":
        return work()

    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
