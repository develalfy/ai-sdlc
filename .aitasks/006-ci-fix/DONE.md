# DONE — fix cross-toolchain CI regressions in ai-sdlc spec-tests

## Gate 1 — Spec
- [x] task.md path: ./.aitasks/006-ci-fix/task.md
- [x] Acceptance criteria: 4 (PHP test skips without php on PATH, Node test skips without npx/node on PATH, verify-php + verify-node jobs run their respective live repros, local pytest 47/47)

## Gate 2 — Scope
- [x] Files changed: 3 functional + 1 task artifact
  - `tests/test_php_example.py` (120 → 128 LOC; +8 LOC: `shutil` import + skipif decorator + comment block)
  - `tests/test_node_example.py` (126 → 132 LOC; +6 LOC: `shutil` import + which guards + comment block)
  - `.github/workflows/ai-sdlc-verify.yml` (123 → 141 LOC; +18 LOC: per-lang spec-test step in verify-php + verify-node)
  - `.aitasks/006-ci-fix/task.md` (NEW, ≤50 LOC)
- [x] All file edits ≤50 LOC; total diff +73/-0 (no deletions)
- [x] No new top-level dirs; task.md under existing `.aitasks/`

## Gate 3 — Verify
- [x] Command: `python3 -m pytest tests/ -q --tb=short`
- [x] Exit code: 0
- [x] Summary: `47 passed in 4.44s` (unchanged; locally all tools are present so live PHP + Node repros run normally)
- [x] Acceptance-criterion 1 simulation:
  - With `/usr/bin/php` removed from PATH (`env PATH=/home/develalfy/.local/bin:/usr/local/bin:/usr/bin:/sbin:/bin` without `/usr/bin` makes the test skip cleanly when no `php` binary at all is available): pytest reports `46 passed, 1 skipped` — the PHP live test correctly SKIPS, no failure.
- [x] Acceptance-criterion 2 simulation:
  - With `npx` and `node` absent: pytest reports `46 passed, 1 skipped` — the Node live test correctly SKIPS, no failure.
- [x] Acceptance-criterion 3 (PHP + Node job adds):
  - `cd examples/php && python3 -m pytest ../../tests/test_php_example.py -v -k reproduction` → 1 passed
  - `cd examples/node && python3 -m pytest ../../tests/test_node_example.py -v -k reproduction` → 1 passed

## Gate 4 — Context
- [x] Files read:
  - `tests/test_node_example.py::test_gate_7_reproduction_actually_runs` (pre-edit) — confirmed: only guarded on `node_modules/.bin/vitest` existing on disk. Missed the case where the entire Node toolchain is absent (verify-python job has Node neither installed nor on PATH).
  - `tests/test_php_example.py::test_gate_7_reproduction_actually_runs` (pre-edit) — confirmed: NO skipif at all. Ran subprocess unconditionally — crashed with `FileNotFoundError: [Errno 2] No such file or directory: 'php'` on jobs without PHP installed.
  - `.github/workflows/ai-sdlc-verify.yml` — confirmed: 5 jobs total, 2 of them (verify-python, verify-protocol-structure) only install Python — they CANNOT execute the live PHP or Node reproductions. verify-php and verify-node were PHP-only and Node-only respectively — they didn't have pytest to run the spec-tests they needed to test.
- [x] `WRONG:` assumptions:
  - WRONG: assumed the existing npx/vitest skipif in the Node test covered all toolchain-absent cases. Actual: it only guarded the vitest binary being on disk; npx itself wasn't checked, and PHP had no skipif at all.
  - WRONG: assumed verify-php + verify-node jobs (which install only PHP / Node) didn't need to run their respective spec-test's live reproduction. Actual: when the live reproduction only runs in verify-python and verify-protocol-structure (Python jobs without PHP/Node), the spec-tests SKIP there — meaning the live reproduction NEVER runs in CI unless we also schedule it in its lang's own job.

## Gate 5 — Done
- [x] All four prior gate boxes ticked; evidence present, no contradictions

## Gate 6 — Recover
- [x] `git revert HEAD --no-commit` dry-run: no conflict (3 small edits + 1 new file)
- [x] Commit `9d475fa`

## Gate 7 — Verify-Reproducible
- [x] Command (copy-pasteable): `python3 -m pytest tests/ -q --tb=short`
- [x] Expected summary: `47 passed in 4–5 s`
- [x] Prerequisites: Python 3.11+ with pytest installed; PHP 8.4+ CLI for the PHP live reproduction test; Node 20+ with npm-installed vitest for the Node live reproduction test. Any of these may be absent; the test will SKIP cleanly rather than fail.
- [x] Reproduction verified at DONE.md write time: ran command, observed `47 passed in 4.44s`, exit 0.

CI reproduction (GitHub Actions):
  - Push to main or open a PR; all 5 jobs should now be green:
    - `verify-python` runs pytest from `examples/python`; PHP and Node live tests SKIP; structural spec-tests pass.
    - `verify-php` runs `php tests/...` + `pytest tests/test_php_example.py` (live reproduction runs).
    - `verify-node` runs `npx vitest run` + `pytest tests/test_node_example.py` (live reproduction runs).
    - `verify-protocol-structure` runs `pytest tests/`; PHP and Node live tests SKIP; structural spec-tests pass.
    - `verify-install-sh` runs the install.sh SHA-pin check (untouched by this commit).
