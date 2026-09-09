# Task — fix cross-toolchain CI regressions in ai-sdlc spec-tests

## Goal

Ashraf reported "pipelines failing." Root cause: my Pass-3 added
`tests/test_php_example.py::test_gate_7_reproduction_actually_runs` (which
shells out to `php`) and `tests/test_node_example.py::test_gate_7_reproduction_actually_runs`
(which shells out to `npx vitest`). The `verify-python` and
`verify-protocol-structure` jobs are Python-only — no `php`/`npx` on PATH.
The Node test already had a skipif for missing vitest binary; nothing
guarded the case where `npx` itself is absent.

## Acceptance criteria

- [ ] Given `tests/test_php_example.py::test_gate_7_reproduction_actually_runs`,
      when it runs in a job where `php` is not on PATH, then pytest SKIPS
      the test (current behavior: ERROR with `FileNotFoundError: [Errno 2]
      No such file or directory: 'php'`).
- [ ] Given `tests/test_node_example.py::test_gate_7_reproduction_actually_runs`,
      when it runs in a job where `npx`/`node` are not on PATH, then pytest
      SKIPS the test (current behavior: ERROR with `FileNotFoundError: [Errno 2]
      No such file or directory: 'npx'`).
- [ ] Given the `verify-php` and `verify-node` CI jobs, when they each install
      Python+pytest and run the example's spec-test, then the live
      reproduction inside that spec-test runs successfully in each job's
      own toolchain.
- [ ] Given all the above, when the full local pytest run executes from repo
      root, then it reports `47 passed, 0 failed`.

## Out of scope

- Adding `--strict-markers` or other pytest-config changes.
- Splitting verify-python into per-tool sub-jobs (the skipif is enough for
  current matrix; restructure is overkill).
- Adding a Makefile or task runner.
- Touching examples/*/source (only test + workflow files).

## Commit convention

One commit: `fix(ci): guard live-run spec-tests against missing PHP/Node
toolchains, add per-lang spec-test CI steps`.
