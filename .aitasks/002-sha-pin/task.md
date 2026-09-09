# Task — enable SHA pinning in install.sh

## Goal

`install.sh` currently computes a SHA256 of `SKILL.md` and prints it, but
refuses to verify against a pinned baseline (the `EXPECTED_SHA256=""`
short-circuits the mismatch check). Anyone who can swap a local clone's
`SKILL.md` can install a doctored copy into `~/.hermes/skills/ai-sdlc/`
without detection. Enable by-default pinning against a baseline published
in `PROTOCOL.md` §9 (new section), so the install fails closed when local
bytes diverge from the published bytes.

## Acceptance criteria

- [ ] Given PROTOCOL.md §9 contains a published SKILL.md SHA256 baseline,
      when a user runs `./install.sh` against an unmodified clone,
      then the script exits 0 and copies SKILL.md to `~/.hermes/skills/ai-sdlc/SKILL.md`.
- [ ] Given PROTOCOL.md §9 contains the SHA baseline,
      when a user edits SKILL.md locally so its SHA differs from the baseline
      and runs `./install.sh`,
      then the script exits non-zero with a clear "sha mismatch" message and
      does NOT copy SKILL.md to the destination.
- [ ] Given both, when the spec-test suite (`python3 -m pytest tests/ -q`) runs,
      then it still passes with no regression (≥13 passed).
- [ ] Given the install.sh change, when shellcheck is available and run against
      install.sh, then it reports no new errors. (Skipped if shellcheck not
      installed.)

## Out of scope

- TLS-pinned network fetch of the canonical SHA (v0.1 ships local-only).
- A signature (GPG / Sigstore) on top of the SHA — that is v0.2+.
- Any change to PROTOCOL.md gate definitions (§3) or DONE.md templates.
- Refactoring the install path itself (`cp` → `rsync`, `install -D`, etc.).
- Cross-harness installers (Claude Code, OpenCode, etc.) — only the Hermes
  install.sh is in scope.

## Commit convention

One commit: `feat(install): enable by-default SHA256 pinning against
PROTOCOL.md §9 baseline` (+ a docs commit for the PROTOCOL.md §9 section).
