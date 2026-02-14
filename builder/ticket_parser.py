from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


SECTION_TITLES = {
    "goal": "Goal",
    "acceptance_criteria": "Acceptance Criteria",
    "files_likely_affected": "Files Likely Affected",
    "tests_to_add": "Tests To Add",
}


def _is_heading(line: str) -> bool:
    return line.startswith("## ")


def _heading_name(line: str) -> str:
    return line[3:].strip()


def _is_bullet(line: str) -> bool:
    s = line.strip()
    return s.startswith("- ")


def _bullet_text(line: str) -> str:
    return line.strip()[2:].strip()


def parse_ticket_markdown(md: str) -> Dict[str, object]:
    """
    Parse a ticket markdown created by builder/cli.py into structured fields.

    Returns a dict with keys:
      - title: str
      - goal: str
      - acceptance_criteria: list[str]
      - files_likely_affected: list[str]
      - tests_to_add: list[str]
    """
    lines = md.splitlines()

    # Title = first "# " heading
    title = ""
    for line in lines:
        if line.startswith("# "):
            title = line[2:].strip()
            break

    # Capture sections by "## " headings
    sections: Dict[str, List[str]] = {}
    current = None

    for line in lines:
        if _is_heading(line):
            current = _heading_name(line)
            sections[current] = []
            continue

        if current is not None:
            sections[current].append(line)

    def get_section_text(section_title: str) -> str:
        raw = sections.get(section_title, [])
        # Keep non-empty lines, join as paragraph
        kept = [l.rstrip() for l in raw if l.strip()]
        return "\n".join(kept).strip()

    def get_section_bullets(section_title: str) -> List[str]:
        raw = sections.get(section_title, [])
        bullets: List[str] = []
        for l in raw:
            if _is_bullet(l):
                item = _bullet_text(l)
                if item and item != "(fill in)":
                    bullets.append(item)
        return bullets

    goal = get_section_text(SECTION_TITLES["goal"])
    acceptance = get_section_bullets(SECTION_TITLES["acceptance_criteria"])
    files = get_section_bullets(SECTION_TITLES["files_likely_affected"])
    tests = get_section_bullets(SECTION_TITLES["tests_to_add"])

    return {
        "title": title,
        "goal": goal,
        "acceptance_criteria": acceptance,
        "files_likely_affected": files,
        "tests_to_add": tests,
    }
