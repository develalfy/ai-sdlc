# Task — final polish: drop dead code, close CI loop on install.sh

## Goal

Two cleanups landed mid-session without their own task:

1. `tests/_spec_helpers.py` exports a `done_path` pytest fixture that no
   test uses. Dead code that misleads future contributors.
2. The new SHA-pinning in `install.sh` (Pass 2) had no CI step —
   PROTOCOL.md §9 and SKILL.md could drift apart silently.

## Acceptance criteria

- [ ] Given `_spec_helpers.py` after this task, when `python3 -c "import
      _spec_helpers"` runs, then it imports cleanly without unused
      imports (no `pytest`, no `Iterator`).
- [ ] Given the dead `done_path` fixture is removed, when
      `python3 -m pytest tests/ -q` runs, then it still passes 47/47.
- [ ] Given the new `verify-install-sh` CI job, when someone PRs a SKILL.md
      change without bumping PROTOCOL.md §9, the CI build fails with a
      clear `::error::` annotation.
- [ ] Given a tampered local clone (the CI job's third step), when
      `./install.sh` runs, then CI observes exit 1 and the build fails.

## Out of scope

- Refactoring `tests/test_python_example.py` (already minimal).
- Touching the SHA baseline — current value is the documented one.
- Adding CI step for the failure-modes.md spec-test (already part of the
  existing `verify-protocol-structure` pytest run; same job covers it).

## Commit convention

One commit: `chore(polish): drop dead helper fixture, wire install.sh
SHA pin into CI`.
