# Task — write `docs/failure-modes.md` from the 5 dogfood bug classes

## Goal

The 5-task dogfood kill-switch surfaced 5 distinct bug classes that no test
suite caught. The raw findings live in `journal/SUMMARY.md`; this task
promotes them to a top-level cheat sheet (`docs/failure-modes.md`) so
contributors and downstream agents have a fast lookup when a `DONE.md`
_gate-3_ "passed" looks suspiciously green.

## Acceptance criteria

- [ ] Given `docs/failure-modes.md` exists with one section per bug class,
      when an agent reads the file, then each section names the class,
      shows a minimal code-snippet pattern that exemplifies the bug,
      names a one-line "how the agent should have caught this in gate 4
      (Context)" lesson, and links back to the dogfood commit.
- [ ] Given the file exists, when `python3 -m pytest tests/ -q` runs,
      then it still passes with no regression (≥42 passing).
- [ ] Given the file exists, when
      `grep -c '^## ' docs/failure-modes.md` runs, then the count is ≥5
      (one section per dogfood bug class).

## Out of scope

- Adding new bug classes beyond the 5 in `journal/SUMMARY.md`. (Future
  tasks can append.)
- Rewriting `journal/SUMMARY.md` itself — its narrative form is fine; the
  cheat sheet is a derivative, not a replacement.
- Wiring `docs/failure-modes.md` into the live spec-tests. The class names
  serve as a rubric; programmatic enforcement is a v0.2 follow-up.

## Commit convention

One commit: `docs(failure-modes): capture the 5 dogfood bug classes as a
cheat sheet, plus a README link`.
