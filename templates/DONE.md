# DONE — <task slug>

## Gate 1 — Spec
- [ ] task.md path: ./task.md
- [ ] Acceptance criteria: <count, ≥1>

## Gate 2 — Scope
- [ ] Files changed: <count> (all ≤50 LOC), no new top-level dirs
- [ ] New files: <path> — <one-line justification>

## Gate 3 — Verify
- [ ] Command: <e.g. pytest tests/ -q>
- [ ] Exit code: <0>
- [ ] Summary: <e.g. 12 passed, 0 failed in 1.4s>

## Gate 4 — Context
- [ ] Files read:
  - <path> — confirmed: <assumption held>
  - <path> — WRONG: <assumption that turned out false>

## Gate 5 — Done
- [ ] This file exists and all four boxes above are ticked

## Gate 6 — Recover
- [ ] git revert HEAD succeeded in dry-run; last commit: <sha>
