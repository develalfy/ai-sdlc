# DONE — healthz endpoint (synthetic PHP example)

## Gate 1 — Spec
- [x] task.md path: ./task.md
- [x] Acceptance criteria: 3 (Given/When/Then)

## Gate 2 — Scope
- [x] Files changed (≤50 LOC each):
  - examples/php/.gitignore = 5 LOC
  - examples/php/DONE.md = this file
  - examples/php/src/Controller/HealthController.php = 50 LOC
  - examples/php/task.md = 34 LOC
  - examples/php/tests/Controller/HealthControllerTest.php = 25 LOC
- [x] No new top-level directories: only examples/php/src/ and examples/php/tests/ under the existing examples/php/ root.
- [x] New files justified (one line each):
  - src/Controller/HealthController.php — synthetic controller required by acceptance criterion 1.
  - tests/Controller/HealthControllerTest.php — single-file runnable test using PHP's built-in assert(); no vendor tree required.
  - task.md — required by gate 1.
  - .gitignore — keeps vendor/ and phpunit.phar out of the example directory if a maintainer later adds them.
- [x] Existing files modified: none.

## Gate 3 — Verify
- [x] Command run: `cd /home/develalfy/projects/ai-sdlc/examples/php && php tests/Controller/HealthControllerTest.php`
- [x] PHP version: PHP 8.4.24 (cli)
- [x] Exit code: 0
- [x] Raw stdout:
  ```
  PASS returns 200 status
  PASS returns application/json CT
  PASS body has status=ok
  PASS body has version=0.1.0

  4/4 assertions passed.
  ```

## Gate 4 — Context
- [x] Files read while working on this task:
  - /home/develalfy/projects/ai-sdlc/PROTOCOL.md
    — confirmed: six gates; DONE.md is the source of truth; gate 6 is `git revert HEAD` without conflict.
  - /home/develalfy/projects/ai-sdlc/SKILL.md
    — confirmed: workflow (write task.md → do work → fill DONE.md → smoke-test `git revert HEAD --no-commit` then abort).
  - /home/develalfy/projects/ai-sdlc/examples/python/ (directory listing)
    — confirmed: python example uses pytest with 4 tests, mapping each to one criterion.
- [x] Assumptions tested:
  - Assumption: PHPUnit is required for the test to pass.
    WRONG: PHP 8.4's built-in `assert()` is sufficient for a 4-case smoke test. No composer, no phpunit.phar, no vendor tree. The earlier example required PHPUnit because it was asserting against Symfony's test-helper `getData()`, which is only available inside Symfony's test infrastructure. Dropping that assumption removed the vendor-tree dependency entirely.
  - Assumption: gate 2's 50-LOC ceiling forbids blank lines.
    WRONG: blank lines count, so the controller landed at exactly 50 LOC and the test at 25 LOC after one round of trimming. Confirmed by `wc -l`.

## Gate 5 — Done
- [x] This file exists and all five prior gate boxes are ticked with real evidence (paths, command, exit code, summary, file list, assumption status).

## Gate 6 — Recover
- [x] Smoke-tested against commit `923d7c4`:
  - `git revert HEAD --no-commit` exited 0 with no output (no conflict).
  - `git status --short` during the staged revert listed all five example files queued for deletion (D  .gitignore, D  DONE.md, D  src/Controller/HealthController.php, D  task.md, D  tests/Controller/HealthControllerTest.php).
  - `git revert --abort` exited 0; working tree restored cleanly.
- [x] No conflict. The example is reversible in one command without manual resolution.
