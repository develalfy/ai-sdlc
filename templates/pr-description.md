# <task slug>

## ai-sdlc gates

- [ ] Gate 1 — Spec: `./task.md` with <N> acceptance criteria
- [ ] Gate 2 — Scope: <N> files changed, all ≤50 LOC, no new top-level dirs
- [ ] Gate 3 — Verify: `<command>` → exit 0, `<summary>`
- [ ] Gate 4 — Context: <N> files read, assumptions recorded (incl. any `WRONG:`)
- [ ] Gate 5 — Done: `./DONE.md` complete
- [ ] Gate 6 — Recover: `git revert HEAD` clean (commit `<sha>`)
- [ ] Gate 7 — Verify-Reproducible: gate-3 command re-runs and matches expected summary

## Linked artifacts

- task: `./task.md`
- evidence: `./DONE.md`

## Manual-test notes

<Steps a reviewer must run by hand that the automated suite does not cover.
Delete this section if nothing manual is required.>

## Reviewer checklist

- [ ] Acceptance criteria in `task.md` are met by the diff
- [ ] `DONE.md` Gate 3 evidence matches the latest test run on this branch
- [ ] Gate 7 verified: re-run gate-3 command from a clean clone and confirm structurally similar output
- [ ] No files exceed the 50-LOC scope cap
- [ ] No `WRONG:` assumptions in Gate 4 are unresolved
- [ ] `git revert HEAD --no-commit && git revert --abort` completes without conflict
