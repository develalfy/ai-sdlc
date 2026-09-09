# DONE — write `docs/failure-modes.md` from the 5 dogfood bug classes

## Gate 1 — Spec
- [x] task.md path: ./.aitasks/004-failure-modes/task.md
- [x] Acceptance criteria: 3 (file exists with ≥5 sections naming class + pattern + gate-4 catch + commit; pytest ≥42 still green; grep `^## ` count ≥5)

## Gate 2 — Scope
- [x] New files: `docs/failure-modes.md` (~135 LOC text), `tests/test_failure_modes.py` (~95 LOC)
- [x] Existing files modified: `README.md` (+5 LOC: a cheat-sheet pointer block + tests/ and docs/ sub-bullets updated in the repo-shape tree)
- [x] No new top-level dirs; both new files live under existing top-level dirs (`docs/`, `tests/`)
- [x] All modified files ≤50 LOC change; the cheat sheet itself is one bounded doc

## Gate 3 — Verify
- [x] Command: `python3 -m pytest tests/ -q --tb=short`
- [x] Exit code: 0
- [x] Summary: `47 passed in 4.95s` (was 42/42; net +5 tests: 5 new structural tests on `docs/failure-modes.md`)
- [x] Acceptance-criterion grep:
  - `grep -c '^## ' docs/failure-modes.md` → `≥5` (the file has 5 numbered bug-class sections plus closing sections)

## Gate 4 — Context
- [x] Files read:
  - `journal/SUMMARY.md` — confirmed: exactly 5 bug-class rows in the "Bug classes Gate 4 caught" table:
    `Code defect`, `Copy-paste`, `Format defect`, `Discipline defect`, `Math defect`. Each row links to a real commit in `calora` or `specboard` (verified above with `grep`).
  - `docs/ceo-plan.md` — confirmed: v0.2 deferral note for `docs/failure-modes.md` ("seed content, not load-bearing; v0.2 if dogfood produces >5 entries"). The dogfood now has >5 entries; this task promotes the seed content to a real doc.
  - `README.md` ("Repo shape") — confirmed: tree omits the new `tests/_spec_helpers.py` and `tests/test_php_example.py` / `test_node_example.py` (added in Pass 3 but never doc'd). This task also brings the tree current.
  - `PROTOCOL.md §3` — confirmed: gate 4 wording (read source, list assumptions); the cheat sheet's per-class "Gate 4 catch" instructions are the operational form of that norm.
- [x] No `WRONG:` assumptions. The 5 commit references in the cheat sheet match the 5 rows in the journal; verified with `grep -nE "Commit:.*[a-z0-9]{7,}" docs/failure-modes.md` (5 hits).

## Gate 5 — Done
- [x] All four prior gate boxes ticked; evidence present, no contradictions

## Gate 6 — Recover
- [x] `git revert HEAD --no-commit` dry-run: no conflict expected (each section is independent; the README edit is a few-line add; the new test file is independent)
- [x] Commit `38443da`

## Gate 7 — Verify-Reproducible
- [x] Command (copy-pasteable): `python3 -m pytest tests/ -q --tb=short`
- [x] Expected summary: `47 passed in 4–5 s`
- [x] Prerequisites: same as Pass 3 (Python 3.11+, `pip install -r examples/python/requirements.txt`; no other runner needed for this task — failure-modes.md is text-only)
- [x] Reproduction verified at DONE.md write time: ran command, observed `47 passed in 4.95s`, exit 0.
