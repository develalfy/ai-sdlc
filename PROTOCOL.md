# ai-sdlc Protocol v0.1

**Version:** 0.1.0 · **Status:** Stable, public-push ready pending dogfood
**License:** MIT
**Up-to-date spec source:** https://github.com/develalfy/ai-sdlc/blob/main/PROTOCOL.md

---

## 1. Purpose

This protocol defines what an AI coding agent **must** do — and what it
**must not** claim — before declaring a software task done. It exists so that:

- A second human can verify the agent's work from the artifacts alone, without
  re-running the agent.
- The agent's "done" is falsifiable, not rhetorical.
- A team, an open-source community, or a solo founder can apply the same gate
  set across languages and harnesses.

The protocol is normative on **seven gates** (§3). Anything outside §3 is
convention, not requirement.

---

## 2. Definitions

| Term | Definition |
|---|---|
| **Task** | A single unit of work, scoped to one feature, bug, or refactor. |
| **Acceptance criterion** | One Given/When/Then line in `task.md`. |
| **Verify artifact** | The test-run output captured in `DONE.md` as gate-3 evidence. |
| **Implementer** | Any person or agent building against this protocol. |
| **Contributor** | Someone filing a PR to an ai-sdlc repo (subset of implementer). |
| **DONE.md** | The 7-gate checklist the agent fills in at task completion. |
| **Recover** | Gate 6: ability to undo the agent's last change without manual intervention. |
| **Verify-Reproducible** | Gate 7: gate-3 evidence is reproducible from the repo by a reviewer or CI. |

---

## 3. The seven gates (normative)

An agent MUST satisfy **all seven** before declaring a task done. A gate is
satisfied only when its evidence appears in `DONE.md`.

### Gate 1 — Spec

The agent MUST write a `task.md` containing at least one acceptance criterion
in **Given/When/Then** form before writing any code.

Evidence required in DONE.md:
- Path to `task.md`.
- Count of acceptance criteria (≥1).

### Gate 2 — Scope

The agent MUST NOT introduce changes outside what `task.md` specifies.

Concrete bounds (v0.1):

- ≤50 changed lines per existing file.
- No new top-level directories.
- New files only under `src/<new-module>/`, with a one-line justification
  recorded in DONE.md.

If the agent discovers that the task requires work outside these bounds, it
MUST update `task.md` and re-declare scope before proceeding — not silently
expand.

### Gate 3 — Verify

The agent MUST run the project's standard test suite and observe an exit code
of `0`.

- Python: `pytest` (or project-defined runner).
- PHP: `phpunit`.
- Node: `npm test` / `yarn test` / `pnpm test`.
- Go: `go test ./...`.
- Rust: `cargo test`.
- Other: the project's own `make test` or equivalent.

If no test runner is configured, the agent MUST add one. "No tests" is not
an acceptable excuse to skip this gate.

Evidence required in DONE.md:
- Command run.
- Exit code.
- Test summary line (e.g. `12 passed, 0 failed`).

### Gate 4 — Context

The agent MUST list every file it read while working on the task, and the
assumption it confirmed or disproved for each.

Evidence required in DONE.md:
- A "Files read" section listing each path and the assumption tested.
- Any assumption that turned out to be false MUST be highlighted with
  `WRONG:` prefix.

This gate exists to catch the most common AI failure mode: acting on a
plausible-sounding but incorrect mental model of the existing code.

### Gate 5 — Done

DONE.md itself exists, lists all seven gates with their evidence, and every
gate 1–6 has its `[ ]` replaced with `[x]`.

If gate 5's evidence is missing, no other gate counts as passed.

### Gate 6 — Recover

The agent's last change MUST be reversible without manual intervention.

In git-tracked work: `git revert HEAD` succeeds without conflict.

Non-git flows are explicitly v0.2 scope. A protocol-compliant agent MUST
either work in a git-tracked tree or surface the recovery limitation
explicitly in DONE.md before claiming gate 6.

### Gate 7 — Verify-Reproducible

The test evidence in gate 3 MUST be reproducible from the artifacts in this
repository. A reviewer (or CI) MUST be able to re-run the cited command from
a clean clone and observe a matching exit code and a structurally similar
summary line.

Evidence required in DONE.md (in addition to gate 3):
- The exact command string, copy-pasteable.
- The expected summary line (e.g. `4 passed in 0.82s`), including the trailing
  timestamp if the runner prints one.
- Any environment prerequisites (Python version, Node version, PHP version,
  system packages, env vars) needed to reproduce.

If a CI workflow exists (`.github/workflows/ai-sdlc-verify.yml`), a green run
on the PR satisfies gate 7 automatically. If no CI exists, the reviewer is
expected to re-run the command locally before approving.

The protocol does NOT require byte-identical reproduction — it requires
"structurally similar" output: same exit code, same test count, same pass/fail
counts. Timing drift is normal and expected. A diff in test count or a
mismatched exit code is a gate-7 failure.

This gate exists to close the anti-fabrication gap: gate 3 says "paste
evidence"; gate 7 says "evidence must be reproducible." Without gate 7, an
agent can paste plausible-looking output without it being true.

---

## 4. The DONE.md contract

`DONE.md` is the source of truth. Any harness (or human) reviewing the work
MUST be able to read DONE.md and verify each gate from its evidence alone.

Required sections:

```markdown
# DONE — <task slug>

## Gate 1 — Spec
- [x] task.md path: ./task.md
- [x] Acceptance criteria: 4

## Gate 2 — Scope
- [x] Files changed: 3 (all ≤50 LOC), no new top-level dirs
- [x] New files: src/ai_sdlc/checker.py — needed because protocol checker doesn't exist yet

## Gate 3 — Verify
- [x] Command: pytest tests/ -q
- [x] Exit code: 0
- [x] Summary: 12 passed, 0 failed in 1.4s

## Gate 4 — Context
- [x] Files read:
  - src/api/routes.py — confirmed: existing /healthz endpoint returns JSON
  - src/db/conn.py — WRONG: assumed asyncpg, actual is psycopg2 sync

## Gate 5 — Done
- [x] This file exists and all six prior gate boxes are ticked

## Gate 6 — Recover
- [x] git revert HEAD succeeded in dry-run; last commit: 7a3f1c2

## Gate 7 — Verify-Reproducible
- [x] Command (copy-pasteable): `pytest tests/ -q`
- [x] Expected summary: `12 passed, 0 failed in 1.4s`
- [x] Prerequisites: Python 3.11+, `pip install -r requirements.txt`
- [x] CI run (if applicable): `.github/workflows/ai-sdlc-verify.yml` — green on PR #N
```

A gate is **failed** if its checkbox is `[ ]` or if the evidence is missing,
illegible, or contradicted by other evidence in the same file.

---

## 5. The STATUS signal (optional, supplementary)

For harnesses that want a fast pre-DONE.md screening, an agent MAY emit a
status line to stdout:

```
STATUS: PASS
```

or

```
STATUS: FAIL gate-N
```

Where `N` is `1`–`7`.

**This is a screening shortcut, NOT a substitute for DONE.md evidence.**
Gate 5's whole point is that DONE.md is the final arbiter. A stdout `STATUS:
PASS` with a missing DONE.md fails gate 5.

---

## 6. What this protocol does NOT mandate

- The **language** of the implementation.
- The **agent harness** (Hermes, OpenCode, Claude-Code, aider, etc.).
- The **task management system** (linear, kanban, todo.txt, no system).
- The **commit convention** (we recommend a single commit per task; the
  protocol does not require it).
- The **test framework**, beyond "the project's standard."

If a tooling choice makes a gate impossible, the implementer SHOULD raise an
issue in the ai-sdlc repo rather than silently skip the gate.

---

## 7. Versioning

- **v0.1 (this document):** initial public-facing spec.
- **v0.2 (planned):** non-git recovery, harness adapter matrix, failure-modes
  catalog seed.

Gate changes require 2 approvals from the contributor set + a worked example.
See `CONTRIBUTING.md`.

---

## 8. License

MIT — see `LICENSE`.
