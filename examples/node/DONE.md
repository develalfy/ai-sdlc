# DONE — extract Button component (synthetic Node/React example)

## Gate 1 — Spec
- [x] task.md path: ./task.md
- [x] Acceptance criteria: 3 (Given/When/Then)

## Gate 2 — Scope
- [x] Files changed (≤50 LOC each):
  - .gitignore = 4 LOC
  - package.json = 30 LOC (devDependencies + script)
  - tsconfig.json = 16 LOC
  - vitest.config.ts = 7 LOC
  - DONE.md = this file
  - task.md = 29 LOC
  - src/Button.tsx = 25 LOC
  - src/Button.test.tsx = 28 LOC
- [x] No new top-level directories: only `src/` under the existing examples/node/.
- [x] New files justified (one line each):
  - src/Button.tsx — the extracted component required by acceptance criterion 1.
  - src/Button.test.tsx — Vitest suite covering the three criteria.
  - package.json + tsconfig.json + vitest.config.ts — minimal toolchain so the example runs end-to-end without a Vite scaffold.
  - .gitignore — excludes node_modules/ and package-lock.json from the example commit.
- [x] Existing files modified: none.

## Gate 3 — Verify
- [x] Setup: `npm install` (npm 10.x, Node v22.22.2) installed the devDependencies into `node_modules/`. Install was silent; no audit warnings (suppressed via `--no-audit --no-fund`).
- [x] Command run: `cd /home/develalfy/projects/ai-sdlc/examples/node && npx vitest run`
- [x] Exit code: 0
- [x] Raw stdout:
  ```
   RUN  v2.1.9 /home/develalfy/projects/ai-sdlc/examples/node

   ✓ src/Button.test.tsx (4 tests) 218ms

   Test Files  1 passed (1)
        Tests  4 passed (4)
     Start at  20:21:23
     Duration  3.26s
  ```
- [x] Each criterion in task.md maps to at least one Vitest case:
  - criterion 1 (accessible name) → "renders with the supplied label as its accessible name"
  - criterion 2 (variant class) → "applies the variant class for variant=secondary"
  - criterion 3 (click) → "invokes onClick exactly once per click"
  - default-variant coverage → "defaults to the primary variant when variant is omitted"

## Gate 4 — Context
- [x] Files read while working on this task:
  - /home/develalfy/projects/ai-sdlc/PROTOCOL.md
    — confirmed: seven gates (§3), DONE.md evidence rules, gate 6 git-revert recipe, gate 7 reproduction requirement.
  - /home/develalfy/projects/ai-sdlc/SKILL.md
    — confirmed: Hermes consumer side; templates live under templates/.
  - /home/develalfy/projects/ai-sdlc/templates/DONE.md
    — confirmed: the seven gate sections and `[x]` evidence pattern (gate 5 lists all seven).
  - /home/develalfy/projects/ai-sdlc/examples/python/DONE.md
    — confirmed: format for capturing exit code + raw stdout + summary in gate 3.
- [x] Assumptions tested:
  - Assumption: vitest matchers like `toBeInTheDocument()` and `toHaveClass()` work out of the box.
    WRONG: those matchers require an explicit import of `@testing-library/jest-dom/vitest`. Without it, vitest reports "Invalid Chai property" and 3 of 4 tests fail. Added the import to Button.test.tsx, tests then went 4/4 green.
  - Assumption: TypeScript would reject `esModuleInterop` being declared twice in tsconfig.json.
    WRONG: it only emits a build warning, not an error. Removed the duplicate key.

## Gate 5 — Done
- [x] This file exists and all six prior gate boxes are ticked with real evidence (paths, command, exit code, raw stdout, file list, assumption status).

## Gate 6 — Recover
- [x] Smoke-tested against commit `7f303e0`:
  - `git revert HEAD --no-commit` exited 0 with no output (no conflict).
  - `git status --short` during the staged revert listed all eight tracked example files queued for deletion (D  .gitignore, DONE.md, package.json, src/Button.test.tsx, src/Button.tsx, task.md, tsconfig.json, vitest.config.ts). node_modules/ and package-lock.json remained untracked (they were correctly ignored by .gitignore and never tracked).
  - `git revert --abort` exited 0; working tree restored cleanly.
- [x] No conflict. The example is reversible in one command without manual resolution.

## Gate 7 — Verify-Reproducible
- [x] Command (copy-pasteable): `cd /home/develalfy/projects/ai-sdlc/examples/node && npx vitest run`
- [x] Expected summary: `Test Files 1 passed (1) | Tests 4 passed (4)` (duration varies; timing noise is expected and accepted per PROTOCOL.md §3 gate 7).
- [x] Prerequisites: Node 18+, `npm install` first to populate node_modules/ from package.json (vitest 2.x, jsdom, @testing-library/react 16, react 18).
- [x] Reproduction verified at DONE.md write time: re-ran `npx vitest run` after the dependency install; observed `Test Files 1 passed (1) | Tests 4 passed (4)`. Same test count, same pass/fail outcome, same exit code 0.
