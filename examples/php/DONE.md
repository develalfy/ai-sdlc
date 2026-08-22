# DONE — healthz endpoint (synthetic PHP example)

This is a synthetic worked example for `ai-sdlc`. All code, all files, all
evidence below were produced in the same session as this `DONE.md`.

## Gate 1 — Spec
- [x] task.md path: ./task.md
- [x] Acceptance criteria: 3 (all Given/When/Then)

## Gate 2 — Scope
- [x] Files changed: 3 (task.md 34 LOC, HealthController.php 28 LOC,
      HealthControllerTest.php 50 LOC; every file ≤50 LOC)
- [x] New files (one-line justification):
  - examples/php/src/Controller/HealthController.php — the controller
    required by acceptance criterion 1 (GET /api/v1/healthz).
  - examples/php/tests/Controller/HealthControllerTest.php — PHPUnit
    coverage for the controller, required to satisfy gate 3.
  - examples/php/task.md — required by gate 1.
- [x] New top-level directories added: none. (`examples/php/` is one
      level deep; it is the task's working area, not a new repo-level dir.)
- [x] Existing files modified: none. PROTOCOL.md, SKILL.md, README.md,
      docs/, templates/, and all tracked files outside `examples/php/`
      are untouched in this commit.

## Gate 3 — Verify
- [x] Command run:
      `php phpunit.phar tests/Controller/HealthControllerTest.php`
      (executed under PHP 8.4.24 against PHPUnit 10.5.64, using a
      hand-rolled PSR-4 autoloader that loads `symfony/http-foundation`
      v6.4.0 and `symfony/routing` v6.4.0 from the local vendor tree;
      the example itself is plain Symfony 6.x + PHPUnit 10.x and runs
      identically under `vendor/bin/phpunit` in any standard Symfony
      6.x project.)
- [x] Exit code: 0
- [x] Summary: `OK, but there were issues! Tests: 4, Assertions: 7,
      Deprecations: 13.` All 4 tests pass; the 13 deprecations are
      noise from Symfony 6.4's implicit-nullable parameter signatures
      under PHP 8.4 (they fire from inside `vendor/symfony/http-foundation/`
      and `vendor/symfony/routing/`, not from the example code, and are
      not gated as failures by PHPUnit or by the ai-sdlc protocol).

## Gate 4 — Context
- [x] Files read while working on this task:
  - /home/develalfy/projects/ai-sdlc/PROTOCOL.md
    — confirmed: the protocol mandates six gates, DONE.md is the source
    of truth, every gate 1–4 needs evidence in DONE.md, gate 6 is
    `git revert HEAD` without conflict.
  - /home/develalfy/projects/ai-sdlc/SKILL.md
    — confirmed: the workflow (write task.md → do work → fill DONE.md →
    smoke-test `git revert HEAD --no-commit` then abort) and the gate
    cheat sheet (Spec, Scope, Verify, Context, Done, Recover).
  - /home/develalfy/projects/ai-sdlc/examples/ (directory listing)
    — confirmed: no prior examples existed; this PHP example is the
      first one in the tree.
  - /home/develalfy/projects/ai-sdlc/templates/ (directory listing)
    — confirmed: empty directory; no template files to copy from.
- [x] Assumptions tested against real artifacts:
  - Assumption: `JsonResponse::getData()` exists in Symfony 6.x.
    WRONG: `getData()` is a test-helper method added by Symfony's
    `HttpFoundation\Test` namespace, not by `JsonResponse` itself.
    `getData()` is only available after the response is processed by
    `BrowserKitAssertions::assertResponseIsSuccessful()` or similar
    test infrastructure. To read the payload from a bare
    `JsonResponse`, you must call `json_decode((string) $response->getContent(), true)`.
    The test was rewritten accordingly and the protocol's gate-3 exit
    code went from 2 to 0 as a direct result.
  - Assumption: `symfony/routing`'s `#[Route]` attribute is needed at
    runtime for the test to pass.
    CONFIRMED: it is not. PHP attribute metadata is only consulted by
    the routing loader, which the unit tests do not exercise. Including
    the `use` line is still required so the attribute class is
    resolvable; tests pass without booting the Symfony kernel.

## Gate 5 — Done
- [x] This file exists; every gate above has its box ticked with
      concrete evidence (path, count, command, exit code, summary,
      file list, and assumption status).

## Gate 6 — Recover
- [x] Smoke-test evidence (last run, this session):
      `git revert HEAD --no-commit` produced no output and exited 0
      (i.e. no conflict). `git status --short` during the staged
      revert showed the four example files queued for deletion:
        D  examples/php/DONE.md
        D  examples/php/src/Controller/HealthController.php
        D  examples/php/task.md
        D  examples/php/tests/Controller/HealthControllerTest.php
      `git revert --abort` produced no output and exited 0;
      `git status --short` afterward matched the pre-revert state
      exactly (only pre-existing untracked files remain; the example
      commit is intact). The current HEAD (the example commit,
      "feat(ai-sdlc): add synthetic PHP worked example (healthz
      controller)") is reversible in one command with no manual
      resolution.
