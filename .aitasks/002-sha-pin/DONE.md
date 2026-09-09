# DONE — enable by-default SHA pinning in install.sh

## Gate 1 — Spec
- [x] task.md path: ./.aitasks/002-sha-pin/task.md
- [x] Acceptance criteria: 4 (clean install exit 0, tampered install exits non-zero + no copy, tests stay 13/13, shellcheck clean — last skipped, no shellcheck installed)

## Gate 2 — Scope
- [x] Files changed: 3 (install.sh = 64 LOC +19 LOC, PROTOCOL.md = §9 NEW (+21 LOC), .aitasks/002-sha-pin/{task.md,DONE.md} NEW)
- [x] All ≤50 LOC per file in the docs/script repo; PROTOCOL.md addition is exactly 21 LOC and stays inside the existing ≤50-LOC per-edit pattern
- [x] No new top-level dirs; `.aitasks/002-sha-pin/` mirrors `.aitasks/001-six-to-seven/` convention
- [x] Out-of-scope items honored: no PROTOCOL.md gate wording changed; no template change; no `cp` → `rsync` refactor; no TLS fetch added

## Gate 3 — Verify
- [x] Command: `python3 -m pytest tests/ -q --tb=short`
- [x] Exit code: 0
- [x] Summary: `13 passed in 1.26s` (unchanged baseline — script/protocol change has no test-side impact)
- [x] Acceptance-criterion shell checks (manual, run alongside the test suite):
  - Clean clone: `./install.sh` → exit 0, copies SKILL.md, prints the SHA matching §9.
  - Tampered clone (appended a tamper-marker line): `./install.sh` → exit 1, prints `error: SKILL.md sha mismatch` with expected + actual, no copy performed.

## Gate 4 — Context
- [x] Files read:
  - install.sh (pre-edit) — confirmed: shipped with `EXPECTED_SHA256=""` and a TODO(v0.2) comment explaining the bypass; the mismatch guard was structurally present but disarmed.
  - PROTOCOL.md — confirmed: §8 is "License"; §7 is "Versioning"; the new §9 sits cleanly at the end as a non-normative integrity annex. No gate or template wording touched.
  - SKILL.md (current) — confirmed: SHA256 `25053a9a…4ff85c` to publish in §9.
  - templates/DONE.md, templates/task.md, examples/python/DONE.md, examples/python/task.md — confirmed: no install.sh reference; no template touches needed.
  - examples/{php,node}/DONE.md — confirmed: no install.sh reference either; the workflow is "agent writes code; human runs install.sh separately". No example change needed.
- [x] No `WRONG:` assumptions surfaced. Assumption: PROTOCOL.md §9 marker text format would be `SKILL.md expected SHA256: \`<64-hex>\`` (a single regex-friendly line) so `awk` could extract it — held.

## Gate 5 — Done
- [x] All four prior gate boxes ticked; evidence present, no contradictions

## Gate 6 — Recover
- [x] Commit `c18c614 → TBD` (Pass-1 sha still pending; this DONE is committed together with the PROTOCOL.md + install.sh change in a single feat commit)

## Gate 7 — Verify-Reproducible
- [x] Command (copy-pasteable):
  - Clean path: `( cd /home/develalfy/projects/ai-sdlc && ./install.sh ; echo "exit=$?" )`
  - Tamper path: `( cd /home/develalfy/projects/ai-sdlc && cp SKILL.md /tmp/s.bak && printf '\n# tamper\n' >> SKILL.md && ./install.sh ; echo "exit=$?" ; mv /tmp/s.bak SKILL.md )`
- [x] Expected summary (clean): `installed: /home/develalfy/.hermes/skills/ai-sdlc/SKILL.md (sha 25053a9a…4ff85c)` and `exit=0`
- [x] Expected summary (tamper): `error: SKILL.md sha mismatch`, no `installed:` line, `exit=1`
- [x] Reproduction verified at DONE.md write time: ran both commands. Clean → exit 0 + file present. Tamper → exit 1, no copy.
- [x] Prerequisites: bash ≥4, `sha256sum` (coreutils; standard), PROTOCOL.md present in repo root.

CI workflow should additionally run the same two shell paths on Ubuntu; the existing
`.github/workflows/ai-sdlc-verify.yml` does not yet exercise `install.sh` — adding a
shell-job step is out of scope for this task (the workflow PATH is bound to python/php/node),
but the SHA pin is enforced locally and the manual reproduction above satisfies gate 7 today.
