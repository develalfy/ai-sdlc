# ai-sdlc — A Collaboration Protocol for AI-Assisted Software Tasks

**Status:** Draft / pre-dogfood · Generated from CEO review on 2026-08-22
**Repo target:** `github.com/<owner>/ai-sdlc` (not yet pushed)
**License:** MIT (proposed)
**Mode:** Open protocol + reference skill, not a SaaS

---

## What this is

A small, opinionated **protocol** that an AI coding agent must follow end-to-end on a software task, plus a reference skill that implements it. It exists because:

1. AI output on non-trivial tasks is **chunked, half-finished, and unverified** (the founder's actual lived pain).
2. Existing agent harnesses (`claude-code`, `opencode`, `aider`, `devin`) lack a **collaboration-grade** contract — anyone can fork, but no shared standard exists for "what done means."
3. A public protocol attracts contributors; a SaaS attracts customers. The founder wants collaborators.

## What this is NOT

- Not a new agent harness.
- Not a replacement for `claude-code` / `opencode` / `aider`.
- Not a SaaS / hosted product.
- Not a research paper.

## Core idea

Define a **5-gate contract** every AI agent must satisfy before declaring a task done, encoded as a reusable skill plus a checklist:

| Gate | Question | Mechanic |
|------|----------|----------|
| **1. Spec gate** | Is the task written down as acceptance criteria, not vibes? | `task.md` template with Given/When/Then |
| **2. Scope gate** | Is the diff bounded — no unrequested additions? | Automated `git diff --stat` review + forbidden-pattern list |
| **3. Verify gate** | Did the agent actually RUN its code and observe pass? | Mandatory `pytest` / `npm test` / `go test` exit code 0 |
| **4. Context gate** | Did the agent check its assumptions about the existing code? | Mandatory file-read evidence in the PR/commit message |
| **5. Done gate** | Is there a checklist proving all 4 passed? | `.ai-sdlc/DONE.md` required in every task |

Fail any gate → "not done." Pass all 5 → ship.

## Repo shape (planned)

```
ai-sdlc/
├── PROTOCOL.md          # The 5-gate spec — human-first, normative
├── SKILL.md             # Hermes/OpenCode/Claude-Code skill (the consumer)
├── templates/
│   ├── task.md          # Acceptance-criteria template
│   ├── DONE.md          # Gate checklist template
│   └── pr-description.md
├── examples/
│   ├── python/          # Worked example: add FastAPI endpoint
│   ├── php/             # Worked example: fix Symfony bug
│   └── node/            # Worked example: refactor React component
├── docs/
│   ├── ceo-plan.md      # This document
│   ├── failure-modes.md # Catalog of "why AI failed" with gate that catches each
│   └── adoption.md      # How to install in your agent harness
├── CONTRIBUTING.md      # How to propose a gate / change a gate
└── LICENSE              # MIT
```

Total surface: ~8 files, ~1500 lines of markdown. No code dependencies.

---

## Why now

- AI agent adoption is in the messy middle: 2026 models are 80-90% first-try-correct, but the last 10-20% requires structural verification, not better prompting.
- The user pain is **not** "AI is bad" — it's "AI is good enough that I stop checking, then it bites me on long tasks."
- A protocol is the wedge: small enough to ship in a week, opinionated enough to be useful, open enough to attract contributors.

## Why a protocol, not a tool

Three shapes were considered; the protocol wins on cost-to-launch and collaborator-friendliness. See `docs/ceo-plan.md` for the full comparison.

---

## Quickstart (planned, after dogfood)

```bash
# In any agent harness that loads SKILL.md:
cp SKILL.md ~/.hermes/skills/ai-sdlc/SKILL.md
# Then on any task:
#   1. Agent reads task.md template, fills it in
#   2. Agent works
#   3. Agent must pass all 5 gates
#   4. Agent produces DONE.md or admits failure
```

## License

MIT — explicit permission to fork, modify, redistribute. See `LICENSE`.

## Contributing

See `CONTRIBUTING.md`. Gate changes require 2 approvals + a worked example.
