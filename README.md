# ai-sdlc — A Collaboration Protocol for AI-Assisted Software Tasks

**Status:** Local-only draft, not yet public.
**Repo target:** `github.com/elalfy/ai-sdlc` (planned, not yet pushed)
**License:** MIT

---

## What this is

A small, opinionated **protocol** that an AI coding agent must follow end-to-end on a software task, plus a reference skill that implements it. It exists because:

1. AI output on non-trivial tasks is **chunked, half-finished, and unverified**.
2. Existing agent harnesses (`claude-code`, `opencode`, `aider`, `devin`) lack a **collaboration-grade** contract — anyone can fork, but no shared standard exists for "what done means."
3. A public protocol attracts contributors; a SaaS attracts customers. This is a protocol.

## What this is NOT

- Not a new agent harness.
- Not a replacement for `claude-code` / `opencode` / `aider`.
- Not a SaaS / hosted product.
- Not a research paper.

## The 7 gates

Every AI agent following this protocol must pass all seven gates before declaring a task done:

| # | Gate | Question |
|---|------|----------|
| 1 | **Spec** | Is the task written as Given/When/Then acceptance criteria? |
| 2 | **Scope** | Is the diff bounded — no unrequested additions? |
| 3 | **Verify** | Did the agent actually RUN its code and observe pass? |
| 4 | **Context** | Did the agent check its assumptions about existing code? |
| 5 | **Done** | Is every other gate's evidence present? |
| 6 | **Recover** | Can the agent undo its last change without manual intervention? |
| 7 | **Verify-Reproducible** | Is gate-3 evidence reproducible from the repo? CI or reviewer re-runs and matches. |

Fail any gate → "not done." Pass all 7 → ship.

## Repo shape

```
ai-sdlc/
├── PROTOCOL.md             # The 7-gate spec — human-first, normative
├── SKILL.md                # Hermes skill (v0.1)
├── templates/
│   ├── task.md             # Acceptance-criteria template
│   ├── DONE.md             # 7-gate checklist template
│   └── pr-description.md
├── examples/
│   ├── python/             # Synthetic FastAPI endpoint
│   ├── php/                # Synthetic Symfony controller
│   └── node/               # Synthetic React refactor
├── tests/
│   └── test_python_example.py
├── CONTRIBUTING.md
├── LICENSE                 # MIT
├── install.sh              # SHA-printed cp to ~/.hermes/skills/
└── README.md
```

30 tracked files. ~1.1k protocol LOC, ~2.9k example LOC (incl. node_modules when installed).

## Why a protocol, not a tool

A protocol is forkable, opinionated, and lets anyone participate without adopting a vendor. That matches the goal: a public GitHub repo for collaboration.

## Status

This repo is **pre-dogfood**. See `docs/ceo-plan.md` for the full plan, the 5-task dogfood protocol, and the public-push checklist.

## License

MIT — see `LICENSE`.
