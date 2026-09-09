# ai-sdlc — A Collaboration Protocol for AI-Assisted Software Tasks

**Status:** v0.1 public at [github.com/develalfy/ai-sdlc](https://github.com/develalfy/ai-sdlc) — dogfood phase (4-week kill-switch running).
**License:** MIT
**Audience:** Anyone using an AI coding agent (Claude Code, OpenCode, Aider, Devin, Hermes, etc.) and tired of chunked, half-finished output.

---

## The problem

AI coding agents ship code that:
- Misses the real requirement (invented it instead of asking)
- Touches files you didn't ask for (scope creep)
- Claims success without ever running it
- Breaks something that already worked (didn't read existing code)
- Can't be reverted cleanly (no git discipline)
- "Works on my machine" — can't be reproduced from the repo

These are not model-quality problems. They're **process problems** the agent doesn't enforce because no one defined "done."

## What ai-sdlc is

A small protocol that defines what "done" means for an AI coding task: **7 gates** every agent must pass before claiming success. Plus a reference skill (`SKILL.md`) that implements the protocol for Hermes, and install paths for other agents.

It is not a new agent. It is not a SaaS. It is a **collaboration contract** — forkable, opinionated, vendor-neutral — that any agent can implement and any project can require.

## The 7 gates

| # | Gate | What it forces |
|---|------|-----------------|
| 1 | **Spec** | Acceptance criteria written before code (Given/When/Then or equivalent) |
| 2 | **Scope** | Diff bounded — no "while I was here" additions |
| 3 | **Verify** | Agent actually ran the code and observed it pass |
| 4 | **Context** | Agent read existing code and confirmed its assumptions |
| 5 | **Done** | Every gate's evidence is present in DONE.md |
| 6 | **Recover** | `git revert HEAD` succeeds without manual fixup |
| 7 | **Verify-Reproducible** | CI or reviewer re-runs gate-3 evidence from the repo and matches |

Fail any one → **not done.** Pass all 7 → **ship.**

The full rules live in [`PROTOCOL.md`](./PROTOCOL.md). The cheat-sheet summary lives in [`SKILL.md`](./SKILL.md).

---

## Quick start

### 1. Install the skill (60 seconds)

**Hermes:**
```bash
git clone https://github.com/develalfy/ai-sdlc.git ~/projects/ai-sdlc
cd ~/projects/ai-sdlc
./install.sh
```
Computes the SHA of `SKILL.md`, prints it for your records, and copies the file to `~/.hermes/skills/ai-sdlc/`. **v0.1 caveat:** SHA verification is not yet enforced — the script doesn't refuse on mismatch. SHA-pinning ships in v0.2. For now, eyeball the printed hash against the GitHub release tag.

**Claude Code:**
```bash
git clone https://github.com/develalfy/ai-sdlc.git ~/projects/ai-sdlc
cp ~/projects/ai-sdlc/SKILL.md ~/.claude/skills/ai-sdlc/SKILL.md
```

**OpenCode:**
```bash
git clone https://github.com/develalfy/ai-sdlc.git ~/projects/ai-sdlc
cp ~/projects/ai-sdlc/SKILL.md ~/.config/opencode/skills/ai-sdlc/SKILL.md
```

**Other agents:** any harness that loads a SKILL.md from a known directory works the same way. PRs welcome to add more install paths.

**Uninstall:**
```bash
rm -rf ~/.hermes/skills/ai-sdlc     # or ~/.claude/skills/ai-sdlc, etc.
```

### 2. Use it on a task

Give your agent any non-trivial coding task. The skill is **auto-loaded** by your harness when relevant (Hermes: any task; Claude Code: when the agent detects the trigger phrase "use ai-sdlc" or sees a `task.md`/`DONE.md` in the workspace).

Give your agent any non-trivial coding task. The agent will:

1. **Load the `ai-sdlc` skill** from its installed location.
2. **Apply the 7 gates** — write `task.md` (Spec), check diff size (Scope), run tests (Verify), read source (Context), fill `DONE.md` (Done), `git revert HEAD` (Recover), ensure CI/reviewer can re-run (Verify-Reproducible).
3. **Report when all 7 pass.**

Templates are in `templates/`:
- [`templates/task.md`](./templates/task.md) — acceptance criteria
- [`templates/DONE.md`](./templates/DONE.md) — 7-gate evidence checklist
- [`templates/pr-description.md`](./templates/pr-description.md) — PR body

### 3. Verify it caught a real bug

3 worked examples prove the protocol works on real code:

- [`examples/python/`](./examples/python/) — synthetic FastAPI endpoint
- [`examples/php/`](./examples/php/) — synthetic Symfony controller
- [`examples/node/`](./examples/node/) — synthetic React refactor

Each one has a filled `task.md`, working code, tests, and a `DONE.md` showing all 7 gates PASS.

The 5-task **dogfood journal** (real bugs caught in Calora and Specboard during testing) lives in `journal/`. See [`journal/SUMMARY.md`](./journal/SUMMARY.md) for the meta-pattern: every bug caught was found by Gate 4 (Context).

A condensed cheat sheet of those 5 bug classes — for fast lookup when reviewing a `DONE.md` — lives at [`docs/failure-modes.md`](./docs/failure-modes.md). Names: *Code defect / Copy-paste defect / Format defect / Discipline defect / Math defect*. Walk your diff against them before trusting a green test.

### 4. Skip it when not needed

The protocol is **only** for non-trivial work. Skip it for:
- One-line typo fixes
- Pure formatting changes
- Pure research / no code change
- Trivially small tasks (<30 LOC, <30 min)
- Tasks that are already done by your existing review process

If you can review the diff in under 60 seconds, you don't need ai-sdlc.

---

## Repo shape

```
ai-sdlc/
├── README.md               # This file
├── PROTOCOL.md             # Full 7-gate spec (normative)
├── SKILL.md                # Hermes skill implementation
├── templates/
│   ├── task.md             # Acceptance criteria template
│   ├── DONE.md             # 7-gate evidence checklist
│   └── pr-description.md
├── examples/
│   ├── python/             # FastAPI endpoint, tests pass
│   ├── php/                # Symfony controller, tests pass
│   └── node/               # React refactor, tests pass
├── tests/
│   ├── _spec_helpers.py        # Shared structural assertions for all examples
│   ├── test_python_example.py  # Python worked example — 7-gate spec-test
│   ├── test_php_example.py     # PHP worked example — 7-gate spec-test
│   └── test_node_example.py    # Node worked example — 7-gate spec-test
├── docs/
│   ├── ceo-plan.md             # Why this exists, dogfood protocol, kill-switch
│   └── failure-modes.md        # 5 dogfood bug classes as a cheat sheet
├── journal/                # Real-world dogfood evidence
│   ├── SUMMARY.md          # 5-task dogfood kill-switch PASS
│   └── 00N-*.md            # Per-task journal entries (in dogfood repos)
├── CONTRIBUTING.md         # How to propose gate changes (2-approval rule)
├── LICENSE                 # MIT
└── install.sh              # SHA-verified skill installer
```

## FAQ

**Q: How is this different from gstack / Superpowers / other agent frameworks?**
A: ai-sdlc is **stack-agnostic**. It doesn't ship an agent harness, doesn't pick a model, doesn't dictate an IDE. It defines a contract any agent can implement. Install it as a skill in whatever harness you already use.

**Q: Do I run install.sh once or per-task?**
A: Once per machine. After install, the skill stays in `~/.hermes/skills/ai-sdlc/` (or your agent's equivalent). Update with `git pull` in the cloned repo + re-run install.sh if `SKILL.md` SHA changes.

**Q: Does this work with Codex / Cursor / Windsurf / [any agent]?**
A: Yes, if your agent loads SKILL.md files from a known directory. The protocol is plain markdown — no SDK, no API. PRs welcome for new install paths.

**Q: Does it slow down small tasks?**
A: Yes, if you run it on tiny tasks. Don't. Use it on tasks where "did the agent actually run it?" is a question worth asking.

**Q: What's the kill-switch?**
A: The 4-week clock from 2026-08-23 to 2026-09-20. If the protocol doesn't actually catch real bugs or starts blocking trivial work, it gets killed. See [`docs/ceo-plan.md`](./docs/ceo-plan.md) and [`journal/SUMMARY.md`](./journal/SUMMARY.md) for the dogfood evidence that triggered the clock.

**Q: Can I change the gates?**
A: Yes — see [`CONTRIBUTING.md`](./CONTRIBUTING.md). Gate changes require 2 approvals and a working dogfood entry showing the new gate catches a real bug.

**Q: Is this an opinionated stack?**
A: No. The protocol is plain text. The 3 worked examples use Python/FastAPI, PHP/Symfony, Node/React — chosen to show the protocol is language-agnostic. Adapt to your stack.

**Q: Does the agent have to follow all 7 gates?**
A: Yes — that's the protocol. The exception is gate-6 (Recover), which only applies to git-tracked work. Non-git tasks skip gate-6 with a documented reason in DONE.md.

---

## What ai-sdlc is NOT

- **Not a new agent harness.** Use your existing Claude Code / OpenCode / Aider / Devin / Hermes. This loads as a skill.
- **Not a SaaS.** No hosted service, no API, no auth. It's a markdown protocol.
- **Not a model spec.** The protocol works with any LLM. No vendor lock-in.
- **Not a research paper.** It's a working protocol with working examples and working dogfood.

---

## License

MIT — see [`LICENSE`](./LICENSE).

## Contributing

See [`CONTRIBUTING.md`](./CONTRIBUTING.md). Gate changes require 2 approvals and a dogfood entry showing the new gate catches a real bug.
