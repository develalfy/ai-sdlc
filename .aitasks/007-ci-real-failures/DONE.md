# DONE — fix two real CI failures caught in run 34312364273

## Gate 1 — Spec
- [x] task.md path: ./.aitasks/007-ci-real-failures/task.md
- [x] Acceptance criteria: 4 (ANSI-strip regex match, set -e capture rc, 47/47 local green, manual bash -e repro)

## Gate 2 — Scope
- [x] Files changed: 3 functional + 1 task artifact
  - `tests/_spec_helpers.py` (+12 LOC: `_ANSI_ESCAPE_RE` constant + `_strip_ansi` helper)
  - `tests/test_node_example.py` (+9/-3 LOC: import `_ANSI_ESCAPE_RE`; strip before regex)
  - `.github/workflows/ai-sdlc-verify.yml` (+5/-1 LOC: `./install.sh; rc=$?` → `./install.sh || rc=$?`)
  - `.aitasks/007-ci-real-failures/task.md` (NEW, ≤50 LOC)
- [x] All ≤50 LOC per file change in functional code.

## Gate 3 — Verify
- [x] Command: `python3 -m pytest tests/ -q --tb=short`
- [x] Exit code: 0
- [x] Summary: `47 passed in 5.57s` (unchanged baseline; ANSI strip is a no-op locally because vitest suppresses colors on TTY)
- [x] CI confirmation (run `34477069784`, sha `c8bd3da`): all 5 jobs succeeded —
  `verify-python`, `verify-php`, `verify-node`, `verify-protocol-structure` (a.k.a. spec-test), `verify-install-sh`.

## Gate 4 — Context
- [x] Files read:
  - `/tmp/job-102341467125.txt` (verify-node, run 34312364273) — confirmed: vitest's captured stdout contained ESC[36m, ESC[1m, ESC[7m codes around keywords like `Tests`. My regex `Tests\s+4\s+passed\s+\(4\)` only matched literal whitespace.
  - `/tmp/job-102341467180.txt` (verify-install-sh, same run) — confirmed: the tamper step got `##[error]Process completed with exit code 1` because `./install.sh` returned 1 and `set -e` aborted before the `rc=$?` assignment.
  - `tests/_spec_helpers.py` (pre-edit) — confirmed: no ANSI-strip helper. Added minimum-viable one.
  - GitHub Actions shell behavior — confirmed: `run:` blocks execute under `bash -e {0}` per Actions docs (https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#using-other-shells-with-the-shell-keyword — the default shell).

- [x] `WRONG:` assumptions:
  - WRONG: assumed `subprocess.run(capture_output=True)` would always yield ANSI-free text. Actual: vitest 2.1.x uses ANSI when the controlling TTY is ambiguous (often inside GitHub Actions runners because the PTY-detection differs from local).
  - WRONG: assumed `./install.sh; rc=$?` would capture the exit code under `set -e`. Actual: bash treats `cmd; assign` as two list elements; `set -e` aborts on `cmd`'s failure before the assignment runs. The right idiom is `cmd || assign` (OR short-circuits around `set -e`).
  - WRONG: assumed the previous "pipelines failing" message referred to remaining issues from Pass-3 fix. Actual: Ashraf was reporting the *current* CI red, which had two distinct new failures — vitest ANSI in the verify-node test, and set -e in the verify-install-sh tamper step. Both my own faults in the prior pass.

## Gate 5 — Done
- [x] All four prior gate boxes ticked; evidence (CI run + local pytest + manual repro) present and non-contradictory

## Gate 6 — Recover
- [x] `git revert HEAD --no-commit` dry-run: no conflict (each change is independent)
- [x] Commit `c8bd3da`

## Gate 7 — Verify-Reproducible
- [x] Commands (copy-pasteable):
  - Local pytest: `python3 -m pytest tests/ -q --tb=short`
  - Bash set -e repro: `bash -ec './install.sh || rc=$?; echo "rc=$rc"'` after `printf '\n# tamper\n' >> SKILL.md` — should print `rc=1` and exit 0 from bash.
  - CI re-run: push to main; `verify-node` and `verify-install-sh` should both succeed.
- [x] Expected summary (pytest): `47 passed in 4–6 s`
- [x] Expected summary (CI): all 5 jobs green on the next push.
- [x] Reproduction verified at DONE.md write time:
  - Local pytest: `47 passed in 5.57s` (exit 0)
  - Bash repro with tampered SKILL.md: `rc=1`, bash exit 0
  - CI run 34477069784 (post-push): 5/5 jobs success

## Cross-link

`/home/develalfy/projects/ai-sdlc/journal/SESSION-2026-09-09.md` should be amended
to mention the post-push discovery + these two fixes (out of scope for this commit;
it's a doc-only follow-up).
