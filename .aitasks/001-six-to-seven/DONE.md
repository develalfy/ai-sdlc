# DONE — fix stale "six gates" copy in PHP+Node example DONE.md

## Gate 1 — Spec
- [x] task.md path: ./.aitasks/001-six-to-seven/task.md
- [x] Acceptance criteria: 3 (gates "no `six gates`", "no `six gate sections`", "spec-test suite still 13/13")

## Gate 2 — Scope
- [x] Files changed: 2 (examples/php/DONE.md +1/-1, examples/node/DONE.md +2/-2), all ≤50 LOC; no new top-level dirs
- [x] Out of scope (per task.md) honored: PROTOCOL.md, SKILL.md, README.md, docs/ceo-plan.md, templates/, journal/ untouched
- [x] No new files; no top-level dir additions

## Gate 3 — Verify
- [x] Command: `python3 -m pytest tests/ -q --tb=short`
- [x] Exit code: 0
- [x] Summary: `13 passed in 1.32s` (unchanged from baseline; this task is doc-only so test count is identical)

## Gate 4 — Context
- [x] Files read:
  - examples/php/DONE.md — confirmed: line 39 had `— confirmed: six gates; DONE.md is the source of truth;` — directly contradicts PROTOCOL.md §3 ("seven gates")
  - examples/node/DONE.md — confirmed: line 49 (`six gates, DONE.md evidence rules`) and line 53 (`six gate sections and `[x]` evidence pattern`) both stale
  - PROTOCOL.md §3 — confirmed: spec is normative on seven gates (lines 40, 104)
  - docs/ceo-plan.md — confirmed: still says "6 gates" in §Accepted Scope and §Temporal Interrogation, but this task explicitly excludes that file (historical plan from when the protocol was 6 gates; left intact to preserve reviewer-trace)
  - README.md — confirmed: 7-gates wording is already current, no edits needed
- [x] No `WRONG:` assumptions; only doc-text refresh

## Gate 5 — Done
- [x] All four prior gate boxes ticked, evidence present and non-contradictory

## Gate 6 — Recover
- [x] `git revert HEAD --no-commit` dry-run succeeded; commit `561c754 → 1109b50`

## Gate 7 — Verify-Reproducible
- [x] Command (copy-pasteable): `python3 -m pytest tests/ -q --tb=short`
- [x] Expected summary: `13 passed in 0.0x–2.x s` (structurally invariant; sub-second timing noise)
- [x] Prerequisites: Python 3.11+, `pip install -r examples/python/requirements.txt` (already met in this environment)
- [x] Reproduction verified at DONE.md write time: ran the command above, observed `13 passed in 1.32s`. Exit code 0, count 13/13 — matches baseline.

Reproduction also covers the gate-3 grep assertions: `grep -nE "six gates|six gate sections" examples/php/DONE.md examples/node/DONE.md` exits 1 with no matches.
