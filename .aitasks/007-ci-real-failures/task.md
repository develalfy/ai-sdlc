# Task — fix two CI failures Ashraf reported (verified via GitHub API)

## Goal

After pushing `fb05f73`, Ashraf's "pipelines failing" report was
confirmed: the latest GHA workflow run shows two red jobs:
  1. `verify-node` — fails on `test_gate_7_reproduction_actually_runs`
     regex that doesn't account for ANSI escape sequences vitest emits
     when its stdout is captured by `subprocess.run` inside CI.
  2. `verify-install-sh` — the tamper-test step uses
     `./install.sh; rc=$?` which is NOT `set -e`-safe; CI's `run:` shell
     is `bash -e {0}` so the script aborts on `./install.sh`'s non-zero
     exit instead of capturing its rc.

## Acceptance criteria

- [ ] Given vitest emits ANSI escape sequences on captured stdout in CI,
      when `test_gate_7_reproduction_actually_runs` runs in
      `verify-node`, then it strips ANSI before regex-searching and
      asserts `Tests  4 passed (4)` (post-strip).
- [ ] Given `./install.sh` exits 1 on tamper, when the CI
      `verify-install-sh` step runs the tamper test, then the step
      captures the rc without `set -e` aborting, then exits 0 (because
      install.sh correctly refused the tampered file — the JOB is
      green).
- [ ] Local pytest: 47 passed, 0 failed.
- [ ] Manual repro of the bash -e issue:
      `bash -ec './install.sh || rc=$?; echo "rc=$rc"'` with a tampered
      SKILL.md prints `rc=1` and exits 0 from bash.

## Out of scope

- Pinning Node 24 (the deprecation warning is informational; the
  test still works on Node 24 as we just verified).
- Restructuring the workflow.
- Touching the install.sh source — only the workflow step.

## Commit convention

One commit: `fix(ci): strip vitest ANSI in node spec-test, fix
set -e in install.sh tamper step`.
