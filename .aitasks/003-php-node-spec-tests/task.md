# Task — add gate-7 spec-tests for PHP + Node examples (parity with Python)

## Goal

`tests/test_python_example.py` walks the Python example's `DONE.md` and
structurally asserts all seven gates, including a live re-run of the gate-3
test command. PHP and Node examples have no analogous test in `tests/`, so
the spec-test suite does not gate their gate-7 evidence. Bring the test
suite to gate-7 parity for all three worked examples.

## Acceptance criteria

- [ ] Given `tests/test_php_example.py` exists, when
      `python3 -m pytest tests/ -q` runs, then it asserts all seven gates
      of `examples/php/DONE.md` (structural assertions, identical pattern
      to the Python test) and additionally re-runs
      `php tests/Controller/HealthControllerTest.php` from
      `examples/php/`, asserting exit code 0 and a stdout matching
      `4/4 assertions passed`.
- [ ] Given `tests/test_node_example.py` exists, when
      `python3 -m pytest tests/ -q` runs, then it asserts all seven gates
      of `examples/node/DONE.md` (same structural assertions) and
      additionally re-runs `npx vitest run` from `examples/node/`,
      asserting exit code 0 and `4 passed (4)` in the summary.
- [ ] Given both files, when the combined suite runs, then the total
      pass count grows from 13 to 13 + (PHP: ~5) + (Node: ~5) — exact
      count varies by git hash conventions of each test file.
- [ ] Skipping each example's live run via the existing
      `pytest.mark.skipif(not DONE_MD.is_file(), ...)` pattern is
      acceptable: the structural assertions are the primary test; the
      live run is the gate-7 reproduction and MUST run when the DONE.md
      is present (which it is).

## Out of scope

- Refactoring `tests/test_python_example.py` itself (it is the template).
- Changing the JSON shape of any example's DONE.md (the spec-tests must
  tolerate the existing wording).
- Modifying CI workflow — the existing `ai-sdlc-verify.yml` already calls
  the same commands; parity is purely local-spec-test parity.
- Adding a Go or Rust example (out of scope; defer to follow-up task).

## Commit convention

One commit: `test(spec): add gate-7 spec-tests for PHP + Node examples
(parity with Python example)`.
