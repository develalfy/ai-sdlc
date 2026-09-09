# Task — fix stale "six gates" copy in PHP+Node example DONE.md

## Goal

Bring `examples/php/DONE.md` and `examples/node/DONE.md` into sync with
PROTOCOL.md §3, which is normative on **seven** gates.

## Acceptance criteria

- [ ] Given `examples/php/DONE.md` Gate 4 lists PROTOCOL.md as a file read,
      when I grep for `six gates`, then no instance appears anywhere in the
      file.
- [ ] Given `examples/node/DONE.md` Gate 4 lists PROTOCOL.md as a file read,
      when I grep for `six gates` or `six gate sections`, then no instance
      appears anywhere in the file.
- [ ] Given the changes above, when the spec-test suite
      (`python3 -m pytest tests/ -q`) runs, then it still passes with no
      regression.

## Out of scope

- PROTOCOL.md, SKILL.md, README.md wording changes.
- Updating the "v0.1 (6-gate)" references in `docs/ceo-plan.md` (historical
  plan from when the protocol was 6 gates; explicitly out of scope for this
  task).
- Any other example, template, or journal edit.

## Commit convention

One commit: `fix(examples): update stale "six gates" copy to "seven" in
PHP+Node DONE.md`.
