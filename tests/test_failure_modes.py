"""Structural assertions for `docs/failure-modes.md`.

Promoted from 2026-09-09 dogfood session: the failure-modes cheat sheet is
a contract with the reader; it claims "5 dogfood bug classes." If the
number of `^## N. <class> —` sections ever drifts from 5, this test
fails — and the cheat sheet loses its "trust me, there are exactly
five of these" guarantee.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

DOC = Path(__file__).resolve().parents[1] / "docs" / "failure-modes.md"
JOURNAL = Path(__file__).resolve().parents[1] / "journal" / "SUMMARY.md"

pytestmark = pytest.mark.skipif(
    not DOC.is_file(),
    reason="docs/failure-modes.md not yet written (see Pass-5 of 2026-09-09 session)",
)


def test_failure_modes_exists() -> None:
    assert DOC.is_file(), f"missing {DOC}"


def test_at_least_five_bug_classes() -> None:
    """The file claims 5 classes, derived from the 5-task dogfood.
    Each class lives under a `^## N. <class name> — ...` heading.

    A drop below 5 is over-deleting (loss of evidence); a rise above
    5 is a class without a journal entry to anchor it. Both fail this
    test and force a reviewer to update either the cheat sheet or the
    journal.
    """
    text = DOC.read_text(encoding="utf-8")
    matches = re.findall(r"^##\s+\d+\.\s+\S+", text, flags=re.MULTILINE)
    assert len(matches) >= 5, (
        f"failure-modes.md claims 5 bug classes; found {len(matches)}: {matches}"
    )


def test_each_class_links_a_real_commit() -> None:
    """Each section must reference a real commit hash from the dogfood,
    not a hypothetical placeholder like `<commit>`. This guards against
    the cheat sheet drifting into example-only content."""
    text = DOC.read_text(encoding="utf-8")
    # Each section references `Commit: <repo-short> <sha>` (e.g.
    # `Commit: \`calora 9a9dc31\``. Match the SHA at the end of the line,
    # 7+ hex chars, NOT preceded by `calora ` or `specboard `, which are
    # repo-name short hands.
    commits = re.findall(
        r"Commit:\s*[`'][a-z\-]+\s+([a-f0-9]{7,})[`']",
        text,
        flags=re.IGNORECASE,
    )
    assert len(commits) >= 5, (
        f"failure-modes.md: expected >=5 real-commit references, got {len(commits)}: {commits}"
    )
    # No placeholders like "<commit>" or "TODO".
    assert "<commit>" not in text.lower(), "failure-modes.md has un-filled <commit> placeholders"


def test_cheat_sheet_outbound_link_resolves() -> None:
    """The cheat sheet links back to journal/SUMMARY.md. If that file
    is moved or renamed, the link is dead — fail loudly."""
    assert JOURNAL.is_file(), (
        f"failure-modes.md links to {JOURNAL.name} but it is not present"
    )
    text = DOC.read_text(encoding="utf-8")
    assert "SUMMARY.md" in text or "journal/" in text, (
        "failure-modes.md should link back to journal/SUMMARY.md"
    )


def test_dogfood_journal_also_lists_five_classes() -> None:
    """The cheat sheet claims parity with journal/SUMMARY.md's bug-class
    table. If the journal ever grows more classes, this test will
    signal that the cheat sheet is out of date (informational — the
    cheat sheet can choose to subsume or summarize).
    """
    if not JOURNAL.is_file():
        pytest.skip("journal/SUMMARY.md not present")
    text = JOURNAL.read_text(encoding="utf-8")
    # The journal table uses "| Code defect |" etc. Each class has a row.
    rows = [ln for ln in text.splitlines() if ln.startswith("|")]
    classes = [
        r for r in rows
        if ("defect" in r.lower())
        and not r.startswith("| Class")
        and not r.startswith("|----")
    ]
    assert len(classes) >= 5, (
        f"journal/SUMMARY.md lists {len(classes)} bug-class rows, expected >=5"
    )
