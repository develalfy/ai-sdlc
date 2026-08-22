"""Walk the examples/python/ worked example end-to-end and assert all six
gates from PROTOCOL.md are satisfied in that example's DONE.md.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

EXAMPLES_PY = Path(__file__).resolve().parents[1] / "examples" / "python"
DONE_MD = EXAMPLES_PY / "DONE.md"

pytestmark = pytest.mark.skipif(
    not DONE_MD.is_file(),
    reason="examples/python/DONE.md not present yet (subagent still drafting)",
)


def _sections(done_text: str) -> dict[int, str]:
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


def test_all_six_gate_sections_present() -> None:
    text = DONE_MD.read_text(encoding="utf-8")
    sections = _sections(text)
    missing = [n for n in range(1, 7) if n not in sections]
    assert not missing, f"DONE.md missing gate section(s): {missing}"


@pytest.mark.parametrize("gate", [1, 2, 3, 4, 5, 6])
def test_each_gate_has_checked_box(gate: int) -> None:
    text = DONE_MD.read_text(encoding="utf-8")
    section = _sections(text)[gate]
    assert "- [x]" in section, f"gate {gate} has no [x] checkbox in DONE.md"


def test_gate_3_has_pytest_summary() -> None:
    text = DONE_MD.read_text(encoding="utf-8")
    section = _sections(text)[3]
    assert re.search(r"\d+\s+passed", section), (
        "gate 3 evidence must contain a pytest summary line like 'N passed'"
    )


def test_gate_4_lists_at_least_one_file_read() -> None:
    text = DONE_MD.read_text(encoding="utf-8")
    section = _sections(text)[4]
    file_lines = [
        ln for ln in section.splitlines()
        if ln.lstrip().startswith("- ") and ("/" in ln or "\\" in ln)
    ]
    assert file_lines, "gate 4 must list at least one file read"


def test_gate_6_mentions_git_revert() -> None:
    text = DONE_MD.read_text(encoding="utf-8")
    section = _sections(text)[6]
    assert "git revert" in section, (
        "gate 6 evidence must mention `git revert` per PROTOCOL.md §3"
    )
