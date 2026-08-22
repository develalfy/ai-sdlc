---
name: ai-sdlc
description: Six-gate protocol for AI coding agents — Spec, Scope, Verify, Context, Done, Recover. Use when starting any non-trivial coding task with an AI agent (claude-code, opencode, Hermes, aider, devin). Forces the agent to write acceptance criteria first, run tests, check assumptions, fill in DONE.md, and ensure the last change is reversible. Prevents "I have to check every time" by making the agent's work falsifiable from artifacts alone.
---

# ai-sdlc — Six-Gate Protocol for AI Coding Agents

**Read `PROTOCOL.md` first.** This skill is the executable consumer; the
protocol is the spec.

## When to load this skill

Load this skill whenever you are about to start a non-trivial coding task with
an AI agent. "Non-trivial" means: more than one file, touches existing logic,
or has a real chance of breaking something.

Skip it only for one-line typo fixes, formatting-only changes, or pure
research.

## The six gates (cheat sheet)

| # | Gate | Single-line rule |
|---|------|------------------|
| 1 | Spec | Write `task.md` with Given/When/Then criteria before any code. |
| 2 | Scope | ≤50 LOC per file, no new top-level dirs; update task.md if scope grows. |
| 3 | Verify | Run the project's test suite; capture exit code + summary in DONE.md. |
| 4 | Context | List every file you read and the assumption you confirmed/disproved. |
| 5 | Done | DONE.md exists, all four above boxes ticked. |
| 6 | Recover | `git revert HEAD` succeeds without conflict. |

A gate is **failed** if its evidence is missing or contradicted. The task is
**not done** until all six pass.

## Workflow

### Step 1 — Write `task.md`

Copy `templates/task.md` to the project root (or your task tracker of choice)
and fill in:

- A one-line goal.
- At least one Given/When/Then acceptance criterion.
- An "Out of scope" section listing what you do NOT want changed.

### Step 2 — Do the work

Read before writing. Run tests as you go. Do not claim done yet.

### Step 3 — Fill in `DONE.md`

Copy `templates/DONE.md` and tick each gate's box only when its evidence is
real. The template forces you to be specific — paste the test summary, list
the files you read, paste the commit hash.

### Step 4 — Verify gate 6

```bash
git revert HEAD --no-commit
git revert --abort   # always abort; this is a smoke test
```

If `git revert` reports a conflict, gate 6 fails. Resolve the conflict before
claiming done.

### Step 5 — Optional: emit `STATUS:` line

For harnesses that grep stdout:

```bash
echo "STATUS: PASS"            # all six gates ticked
echo "STATUS: FAIL gate-3"     # gate 3 (Verify) failed
```

Status line is a shortcut, not a substitute. DONE.md is the source of truth.

## Templates

- `templates/task.md` — acceptance-criteria template
- `templates/DONE.md` — 6-gate checklist template
- `templates/pr-description.md` — PR body template

Copy from the ai-sdlc repo:

```bash
curl -fsSL https://raw.githubusercontent.com/elalfy/ai-sdlc/main/templates/DONE.md > DONE.md
```

(Pinned SHA verification is on the roadmap; see PROTOCOL.md §7.)

## Worked examples

See `examples/` for end-to-end runs in:

- `examples/python/` — synthetic FastAPI endpoint
- `examples/php/` — synthetic Symfony controller
- `examples/node/` — synthetic React refactor

Each example includes a filled-in `task.md` and `DONE.md`.

## Common failure modes

These are the patterns the gates catch. When a gate fails, this is the most
likely reason.

| Gate that catches it | Failure mode |
|---|---|
| 1 (Spec) | Agent invented requirements that weren't in the task. |
| 2 (Scope) | Agent added "while I was here" changes that weren't requested. |
| 3 (Verify) | Agent emitted plausible-looking code without running tests. |
| 4 (Context) | Agent assumed an API/version/library that didn't exist. |
| 6 (Recover) | Agent left the repo in a state where its last change can't be cleanly undone. |

## Anti-patterns

- **"Looks good to me" without test output.** That is not gate 3. Paste the
  pytest/phpunit/npm test command's exit code and summary.
- **Ticking all boxes "to ship faster."** That defeats the protocol. Every box
  requires real evidence in the same file.
- **Skipping gate 6 on non-git work.** Surface the limitation explicitly in
  DONE.md, or work in a git tree.

## See also

- `PROTOCOL.md` — the normative spec
- `CONTRIBUTING.md` — how to propose gate changes
- `examples/` — worked examples in three languages
