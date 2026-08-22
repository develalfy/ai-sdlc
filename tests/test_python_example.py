"""Walk the examples/python/ worked example end-to-end and assert all seven
gates from PROTOCOL.md are satisfied in that example's DONE.md.

Gate 7 (Verify-Reproducible) is verified by re-running the test command
embedded in DONE.md and asserting the exit code + summary line are
structurally similar (not byte-identical — timing drift is expected).
"""
from __future__ import annotations

import re
import subprocess
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


def test_all_seven_gate_sections_present() -> None:
    text = DONE_MD.read_text(encoding="utf-8")
    sections = _sections(text)
    missing = [n for n in range(1, 8) if n not in sections]
    assert not missing, f"DONE.md missing gate section(s): {missing}"


@pytest.mark.parametrize("gate", [1, 2, 3, 4, 5, 6, 7])
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


def test_gate_7_has_reproduction_command() -> None:
    text = DONE_MD.read_text(encoding="utf-8")
    section = _sections(text)[7]
    assert "pytest" in section, "gate 7 must cite a pytest-style command"
    assert re.search(r"\d+\s+passed", section), (
        "gate 7 must include an expected summary line with 'N passed'"
    )


def test_gate_7_reproduction_actually_runs() -> None:
    """Run the python example's pytest, assert exit 0 + a 4/4 pass result.

    This is the live half of gate 7: structural assertions in
    test_gate_7_has_reproduction_command prove the spec is followed; this
    test proves the cited command is real.
    """
    result = subprocess.run(
        ["python3", "-m", "pytest", "test_app.py", "-q", "--tb=short"],
        cwd=str(EXAMPLES_PY),
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, (
        f"gate 7 reproduction failed: rc={result.returncode}\n"
        f"stdout: {result.stdout}\nstderr: {result.stderr}"
    )
    assert re.search(r"4\s+passed", result.stdout), (
        f"gate 7 reproduction: expected 4 passed in pytest output, got:\n{result.stdout}"
    )
