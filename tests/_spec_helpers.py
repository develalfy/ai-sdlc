"""Shared structural assertions for ai-sdlc example spec-tests.

Each worked-example spec-test (python, php, node) walks a DONE.md file and
asserts that all seven gates from PROTOCOL.md §3 are satisfied:

    1. Spec — `## Gate 1` section present + contains a `[x]` checkbox
    2. Scope — `## Gate 2` section present + contains a `[x]` checkbox
    3. Verify — `## Gate 3` section present + contains a `[x]` checkbox
                AND the section text includes a pytest/phpunit/npm-test-
                style "N passed" or "N/N assertions passed" summary line
    4. Context — `## Gate 4` section present + contains a `[x]` checkbox
                AND lists at least one file read
    5. Done — `## Gate 5` section present + contains a `[x]` checkbox
    6. Recover — `## Gate 6` section present + contains a `[x]` checkbox
                 AND mentions `git revert`
    7. Verify-Reproducible — `## Gate 7` section present + contains a
                             `[x]` checkbox AND cites the runnable
                             command for this example's runner

This module is the canonical helper used by tests/test_<lang>_example.py.
It exists as a shared module (not a fixture or a base class) because pytest
discovers helpers by import; no setup, no conftest, no test framework.

For non-trivial structural rules (e.g. "summary line must include at least
one passing test, not '0 passed'"), see Pass-4 of the 2026-09-09 dogfood
session for the tightening that applied to this helper.
"""
from __future__ import annotations

import re
from pathlib import Path


def gate_sections(done_text: str) -> dict[int, str]:
    """Return the body of each `## Gate N — ...` section in DONE.md,
    keyed by the gate number N. Sections not present are omitted."""
    sections: dict[int, str] = {}
    current = 0
    for line in done_text.splitlines():
        m = re.match(r"^##\s*Gate\s+(\d+)\b", line)
        if m:
            current = int(m.group(1))
            sections[current] = ""
        elif current:
            sections[current] += line + "\n"
    return sections


def file_read_lines(section_text: str) -> list[str]:
    """Extract bullet lines that look like a "file path — assumption"
    pair. Lines that lack a path separator are filtered out so a stray
    "- [x] Assumptions tested" header doesn't pollute the list."""
    out: list[str] = []
    for ln in section_text.splitlines():
        s = ln.lstrip()
        if not s.startswith("- "):
            continue
        if "/" in ln or "\\" in ln:
            out.append(ln)
    return out


def has_pass_summary(section_text: str) -> bool:
    """True iff the section text contains a summary line with N >= 1
    passing tests/assertions across the three supported runners.

    The first summary line with N >= 1 wins. Rejects the pathological
    "0 passed" pattern (gates §3 "exit code 0 + N passed" — N=0 is
    structural but NOT evidence that anything was tested).
    """
    for line in section_text.splitlines():
        # Accept line-start, whitespace, or backtick before the digit.
        # The Python example wraps "4 passed in 0.55s" inside backticks on a
        # single line, so the leading `\d+` is preceded by a backtick, not space.
        m = re.search(r"(?:^|[\s`])(\d+)\s+passed", line)
        if m and int(m.group(1)) >= 1:
            return True
        if re.search(r"\d+/\d+\s+assertions\s+passed", line):
            return True
    return False


def structural_assertions(done_path: Path) -> None:
    """Run the gate-1..6 structural assertions on a single DONE.md.

    Gate 7 is checked separately by each example's test file because it
    is the gate that needs a runner-specific live re-run, not a static
    structural check.
    """
    text = done_path.read_text(encoding="utf-8")
    sections = gate_sections(text)

    missing = [n for n in range(1, 7) if n not in sections]
    assert not missing, f"{done_path}: missing gate section(s): {missing}"

    for gate in range(1, 7):
        body = sections[gate]
        assert "- [x]" in body, (
            f"{done_path}: gate {gate} has no [x] checkbox"
        )

    # Gate 4 specifically: must list at least one file read with a path.
    gate4 = sections[4]
    read_files = file_read_lines(gate4)
    assert read_files, (
        f"{done_path}: gate 4 must list at least one file read (with a path)"
    )

    # Gate 6 specifically: must mention `git revert`.
    assert "git revert" in sections[6], (
        f"{done_path}: gate 6 evidence must mention `git revert` per PROTOCOL.md §3"
    )
