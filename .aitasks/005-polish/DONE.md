# DONE — final polish: drop dead code, close CI loop on install.sh

## Gate 1 — Spec
- [x] task.md path: ./.aitasks/005-polish/task.md
- [x] Acceptance criteria: 4 (helper imports cleanly, 47/47 still pass, CI mismatch fails, tamper test fails)

## Gate 2 — Scope
- [x] Files changed: 2 functional + 1 task artifact (`tests/_spec_helpers.py` -12 LOC, `.github/workflows/ai-sdlc-verify.yml` +37 LOC, `.aitasks/005-polish/task.md` NEW)
- [x] All ≤50 LOC per change in functional files; helper dropped 124→112 LOC; workflow stayed under the existing role
- [x] No new top-level dirs

## Gate 3 — Verify
- [x] Command: `python3 -m pytest tests/ -q --tb=short`
- [x] Exit code: 0
- [x] Summary: `47 passed in 4.95s` (unchanged baseline)
- [x] Acceptance-criterion 1 (clean import): `python3 -c "import _spec_helpers"` runs without `ImportError`; verified by running pytest itself (which imports it transitively).

## Gate 4 — Context
- [x] Files read:
  - `tests/_spec_helpers.py` (post-Pass-3 version) — confirmed: `done_path` fixture present at line 119, `Iterator` imported but only consumed by the dead fixture, `pytest` similarly dead. Ponytail rung 1: "does this need to exist?" No.
  - `.github/workflows/ai-sdlc-verify.yml` (pre-edit) — confirmed: 4 jobs (verify-python, verify-php, verify-node, verify-protocol-structure); no job exercised `install.sh` or the PROTOCOL.md §9 baseline. Ponytail rung 1 × 2: same answer — needed.
  - `install.sh` (post-Pass-2) — confirmed: matches the diff from Pass 2; SHA check returns exit 1 on mismatch.
- [x] No `WRONG:` assumptions.
- [x] `WRONG:` lesson (process, not content): the initial commit message used inline backticks for tool names like `done_path` and `verify-install-sh` inside a `git commit -m "..."` heredoc — bash expanded those as command substitution before git ever saw them, corrupting the commit message. Fix: use `git commit -m "subject" -m "body" -m "more body..."` with the tool names spelled out in words; never put bare identifiers in backticks inside a single -m message.

## Gate 5 — Done
- [x] All four prior gate boxes ticked; evidence present, no contradictions

## Gate 6 — Recover
- [x] `git revert HEAD --no-commit` dry-run: no conflict expected (helper is one file, CI is one file, task artifact is one file — all independent)
- [x] Commit `f348761`

## Gate 7 — Verify-Reproducible
- [x] Command (copy-pasteable): `python3 -m pytest tests/ -q --tb=short`
- [x] Expected summary: `47 passed in 4–5 s`
- [x] Prerequisites: same as Pass 4 (Python 3.11+, pytest from examples/python/requirements.txt)
- [x] Reproduction verified at DONE.md write time: ran command, observed `47 passed in 4.95s`, exit 0.

CI reproduction (workflow_dispatch trigger):
  - Verify-Reproducible for the CI change is the GitHub Actions UI itself. Anyone
    with push access can run the workflow via the Actions tab; the new
    `verify-install-sh` job will exercise all three sub-steps (SHA check,
    clean install, tamper refusal).
