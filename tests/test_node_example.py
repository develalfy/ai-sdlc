"""Walk the examples/node/ worked example end-to-end and assert all seven
gates from PROTOCOL.md are satisfied in that example's DONE.md.

Gate 7 (Verify-Reproducible) is verified by re-running the test command
embedded in DONE.md and asserting the exit code + summary line are
structurally similar (not byte-identical — vitest's `Start at HH:MM:SS`
and `Duration Xms` will drift run-to-run, but `Tests N passed (N)` does
not).

Shared structural logic lives in tests/_spec_helpers.py.
"""
from __future__ import annotations

import shutil
import re
import subprocess
from pathlib import Path

import pytest

from _spec_helpers import (  # noqa: E402
    gate_sections,
    has_pass_summary,
    structural_assertions,
    _ANSI_ESCAPE_RE,  # internal but tests use it to strip vitest ANSI noise
)

EXAMPLES_NODE = Path(__file__).resolve().parents[1] / "examples" / "node"
DONE_MD = EXAMPLES_NODE / "DONE.md"

pytestmark = pytest.mark.skipif(
    not DONE_MD.is_file(),
    reason="examples/node/DONE.md not present yet",
)


def test_all_seven_gate_sections_present() -> None:
    text = DONE_MD.read_text(encoding="utf-8")
    sections = gate_sections(text)
    missing = [n for n in range(1, 8) if n not in sections]
    assert not missing, f"DONE.md missing gate section(s): {missing}"


@pytest.mark.parametrize("gate", [1, 2, 3, 4, 5, 6, 7])
def test_each_gate_has_checked_box(gate: int) -> None:
    text = DONE_MD.read_text(encoding="utf-8")
    section = gate_sections(text)[gate]
    assert "- [x]" in section, f"gate {gate} has no [x] checkbox in DONE.md"


def test_gate_3_has_vitest_summary() -> None:
    """vitest prints 'Tests  N passed (N)' on its own line. The shared
    helper accepts both the pytest 'N passed' and the PHP 'N/N assertions
    passed' shapes; vitest's output matches the pytest shape, so
    `has_pass_summary` is the right gate."""
    text = DONE_MD.read_text(encoding="utf-8")
    section = gate_sections(text)[3]
    assert has_pass_summary(section), (
        "gate 3 evidence must contain a 'N passed' summary line"
    )


def test_gate_4_lists_at_least_one_file_read() -> None:
    text = DONE_MD.read_text(encoding="utf-8")
    section = gate_sections(text)[4]
    file_lines = [
        ln for ln in section.splitlines()
        if ln.lstrip().startswith("- ") and ("/" in ln or "\\" in ln)
    ]
    assert file_lines, "gate 4 must list at least one file read"


def test_gate_6_mentions_git_revert() -> None:
    text = DONE_MD.read_text(encoding="utf-8")
    section = gate_sections(text)[6]
    assert "git revert" in section, (
        "gate 6 evidence must mention `git revert` per PROTOCOL.md §3"
    )


def test_gate_7_cites_vitest_command() -> None:
    text = DONE_MD.read_text(encoding="utf-8")
    section = gate_sections(text)[7]
    assert re.search(r"\bnpx\s+vitest\b|\bnpm\s+test\b", section), (
        "gate 7 must cite a vitest-style command (`npx vitest run` or `npm test`)"
    )
    assert has_pass_summary(section), (
        "gate 7 must include an expected summary line with 'N passed'"
    )


def test_gate_7_reproduction_actually_runs() -> None:
    """Run the Node example's vitest, assert exit 0 + 4/4 pass.

    The vitest binary is expected to be installed already
    (`examples/node/node_modules/.bin/vitest`); the .gitignore in that
    example excludes node_modules/, so this test will SKIP in a fresh
    clone — that's the design: the CI job installs first, then runs.

    Also skipped when `node`/`npm`/`npx` aren't on PATH (the
    verify-python CI job has no Node runtime).
    """
    if shutil.which("npx") is None or shutil.which("node") is None:
        pytest.skip("node/npx not installed in this CI job")
    vitest_bin = EXAMPLES_NODE / "node_modules" / ".bin" / "vitest"
    if not vitest_bin.is_file():
        pytest.skip(
            f"vitest not installed at {vitest_bin}; "
            "run `npm install` in examples/node/ first (CI does this)."
        )
    result = subprocess.run(
        ["npx", "vitest", "run"],
        cwd=str(EXAMPLES_NODE),
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert result.returncode == 0, (
        f"gate 7 reproduction failed: rc={result.returncode}\n"
        f"stdout: {result.stdout}\nstderr: {result.stderr}"
    )
    # vitest emits CSI escape sequences (ESC[1m, ESC[36m, etc.) to its
    # stdout when captured by subprocess.run inside CI — strip them
    # before searching. Locally the TTY case suppresses them; CI's
    # captured pipe does not.
    cleaned = _ANSI_ESCAPE_RE.sub("", result.stdout)
    # vitest summary line is "Tests  4 passed (4)" with whitespace.
    assert re.search(r"Tests\s+4\s+passed\s+\(4\)", cleaned), (
        f"gate 7 reproduction: expected 'Tests  4 passed (4)' in vitest output, "
        f"got (ANSI-stripped):\n{cleaned}"
    )


def test_structural_assertions_helper_agrees_on_node_done() -> None:
    """Sanity-check that the shared helper produces the same PASS as the
    example-specific structural tests above. If this fails, the helper and
    the example tests have drifted and one is wrong."""
    structural_assertions(DONE_MD)
