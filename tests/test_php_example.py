"""Walk the examples/php/ worked example end-to-end and assert all seven
gates from PROTOCOL.md are satisfied in that example's DONE.md.

Gate 7 (Verify-Reproducible) is verified by re-running the test command
embedded in DONE.md and asserting the exit code + summary line are
structurally similar (not byte-identical).

Shared structural logic lives in tests/_spec_helpers.py.
"""
from __future__ import annotations

import shutil
import re
import subprocess
from pathlib import Path

import pytest

from _spec_helpers import structural_assertions, has_pass_summary  # noqa: E402

EXAMPLES_PHP = Path(__file__).resolve().parents[1] / "examples" / "php"
DONE_MD = EXAMPLES_PHP / "DONE.md"

pytestmark = pytest.mark.skipif(
    not DONE_MD.is_file(),
    reason="examples/php/DONE.md not present yet",
)


def test_all_seven_gate_sections_present() -> None:
    text = DONE_MD.read_text(encoding="utf-8")
    from _spec_helpers import gate_sections
    sections = gate_sections(text)
    missing = [n for n in range(1, 8) if n not in sections]
    assert not missing, f"DONE.md missing gate section(s): {missing}"


@pytest.mark.parametrize("gate", [1, 2, 3, 4, 5, 6, 7])
def test_each_gate_has_checked_box(gate: int) -> None:
    from _spec_helpers import gate_sections
    text = DONE_MD.read_text(encoding="utf-8")
    section = gate_sections(text)[gate]
    assert "- [x]" in section, f"gate {gate} has no [x] checkbox in DONE.md"


def test_gate_3_has_php_summary() -> None:
    """PHP runner prints 'N/N assertions passed' rather than pytest's
    'N passed'. Match either so a future port to PHPUnit (with the pytest
    line shape) is also accepted."""
    from _spec_helpers import gate_sections
    text = DONE_MD.read_text(encoding="utf-8")
    section = gate_sections(text)[3]
    assert has_pass_summary(section), (
        "gate 3 evidence must contain a passing-test summary line "
        "(e.g. '4/4 assertions passed' or '4 passed')"
    )


def test_gate_4_lists_at_least_one_file_read() -> None:
    from _spec_helpers import gate_sections
    text = DONE_MD.read_text(encoding="utf-8")
    section = gate_sections(text)[4]
    file_lines = [
        ln for ln in section.splitlines()
        if ln.lstrip().startswith("- ") and ("/" in ln or "\\" in ln)
    ]
    assert file_lines, "gate 4 must list at least one file read"


def test_gate_6_mentions_git_revert() -> None:
    from _spec_helpers import gate_sections
    text = DONE_MD.read_text(encoding="utf-8")
    section = gate_sections(text)[6]
    assert "git revert" in section, (
        "gate 6 evidence must mention `git revert` per PROTOCOL.md §3"
    )


def test_gate_7_cites_php_test_command() -> None:
    from _spec_helpers import gate_sections
    text = DONE_MD.read_text(encoding="utf-8")
    section = gate_sections(text)[7]
    # PHP example uses `php tests/...` (single-file runner, no phpunit).
    assert "php " in section, "gate 7 must cite a `php <test-file>` command"
    assert has_pass_summary(section), (
        "gate 7 must include an expected summary line with 'N passed' "
        "or 'N/N assertions passed'"
    )


@pytest.mark.skipif(
    shutil.which("php") is None,
    reason="php CLI not installed in this CI job — install via shivammathur/setup-php or apt",
)
def test_gate_7_reproduction_actually_runs() -> None:
    """Run the PHP example's test file, assert exit 0 + 4/4 pass.

    This is the live half of gate 7: structural assertions in
    test_gate_7_cites_php_test_command prove the spec is followed; this
    test proves the cited command is real.

    Skipped when `php` is not on PATH — the verify-python job has no
    PHP runtime; only verify-php does.
    """
    test_file = EXAMPLES_PHP / "tests" / "Controller" / "HealthControllerTest.php"
    assert test_file.is_file(), f"PHP test file missing: {test_file}"
    result = subprocess.run(
        ["php", str(test_file)],
        cwd=str(EXAMPLES_PHP),
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, (
        f"gate 7 reproduction failed: rc={result.returncode}\n"
        f"stdout: {result.stdout}\nstderr: {result.stderr}"
    )
    assert re.search(r"4/4\s+assertions\s+passed", result.stdout), (
        f"gate 7 reproduction: expected '4/4 assertions passed' in stdout, "
        f"got:\n{result.stdout}"
    )


def test_structural_assertions_helper_agrees_on_php_done() -> None:
    """Sanity-check that the shared helper produces the same PASS as the
    example-specific structural tests above. If this fails, the helper and
    the example tests have drifted and one is wrong."""
    structural_assertions(DONE_MD)
