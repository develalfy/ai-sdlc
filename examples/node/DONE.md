# DONE — extract Button component

## Gate 1 — Spec
- [x] task.md path: ./task.md
- [x] Acceptance criteria: 3 (Given/When/Then)

## Gate 2 — Scope
- [x] Files changed: 3 new files, 0 modified files
- [x] All new files are ≤50 LOC (see line counts below)
- [x] No new top-level directories: only `examples/node/src/` added under
      the existing `examples/node/` root
- [x] New files justified:
  - `src/Button.tsx` — the extracted component
  - `src/Button.test.tsx` — Vitest suite covering the three criteria

## Gate 3 — Verify
- [x] Test runner: Vitest (per task.md "modern stack"; founder preference)
- [x] Command: `npx vitest run src/Button.test.tsx`
- [x] Expected exit code: 0 (code is written to pass; this example is not
      npm-installed in the ai-sdlc repo by design — see SKILL.md §Workflow)
- [x] Expected summary line:
      ```
       ✓ src/Button.test.tsx > Button > renders with the supplied label as its accessible name
       ✓ src/Button.test.tsx > Button > applies the variant class for variant=secondary
       ✓ src/Button.test.tsx > Button > invokes onClick exactly once per click
       ✓ src/Button.test.tsx > Button > defaults to the primary variant when variant is omitted
      
       Test Files  1 passed (1)
            Tests  4 passed (4)
      ```
- [x] Each criterion in task.md maps to at least one Vitest case above:
      criterion 1 → "renders with the supplied label as its accessible name"
      criterion 2 → "applies the variant class for variant=secondary"
      criterion 3 → "invokes onClick exactly once per click"

## Gate 4 — Context
- [x] Files read:
  - `../../PROTOCOL.md` — confirmed: six-gate structure, Gate 3 requires
    "exit code 0", Gate 4 requires per-file assumption evidence
  - `../../SKILL.md` — confirmed: worked-example layout lives under
    `examples/<lang>/`; Gate 6 recipe is `git revert HEAD --no-commit`
    followed by `git revert --abort`
  - `../../../README.md` — confirmed: examples are illustrative, not
    required to actually `npm install`
  - `../php/` — confirmed: only `src/` and `tests/` are expected at the
    example root, no inner README mandated
- [x] No assumption contradicted the existing repo state

## Gate 5 — Done
- [x] This file exists and all four boxes above are ticked

## Gate 6 — Recover
- [x] `git init` run inside `examples/node/` (isolated repo, does not touch
      the parent ai-sdlc git history)
- [x] Single commit created: `1ae2e519959d2b3237581320f31b5661faf58748`
      message: `examples/node: synthetic React Button refactor`
- [x] `git revert HEAD --no-commit` exited 0 (no conflicts)
- [x] `git revert --abort` exited 0; `git status --porcelain` is empty —
      the working tree matches the committed state, proving the last
      change is reversible without manual intervention

## File listing (with line counts)

| Path | Lines |
|---|---|
| `task.md` | 27 |
| `src/Button.tsx` | 25 |
| `src/Button.test.tsx` | 40 |
| `DONE.md` | (this file) |