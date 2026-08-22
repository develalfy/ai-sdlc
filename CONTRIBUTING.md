# Contributing to ai-sdlc

Thanks for caring about how AI coding agents get measured. The protocol is
small on purpose; contributions should be too.

## Adding a worked example

A worked example is a real coding task demonstrated end-to-end, with all six
gates satisfied in its `DONE.md`. Examples are how contributors teach each
other — and how we vet gate changes before merging them.

- [ ] Pick a language the repo does not already cover, or a fresh scenario in
      one it does.
- [ ] Create `examples/<lang>/<slug>/` with `task.md`, source files, and
      `DONE.md` filled in against `PROTOCOL.md` §3.
- [ ] Run the project's standard test suite; capture the exit code and
      summary line in `DONE.md` (gate 3 evidence).
- [ ] List every file the agent read while doing the task (gate 4 evidence);
      mark any wrong assumption with `WRONG:`.
- [ ] Run `git revert HEAD --no-commit && git revert --abort` from the example
      directory; paste the commit hash into `DONE.md` (gate 6 evidence).

If `examples/<lang>/<slug>/tests/` exists, `tests/test_<lang>_example.py` in
this repo will pick it up.

## Proposing a gate change

Gate changes are the highest-impact edit you can make. Per PROTOCOL.md §7, a
gate change requires:

1. **Two approvals** from the contributor set (two distinct maintainers or
   recognized contributors approving the PR).
2. **A worked example** that exercises the proposed change end-to-end. The
   example MUST pass all six gates with the new wording, and its `DONE.md`
   MUST be the strongest evidence in the PR thread.

Without both, the PR is closed regardless of diff quality. Gate changes
without an example are rejected outright — proposals, not patches.

## Filing an issue

Use the templates under `.github/ISSUE_TEMPLATE/` when present. Labels:

- `bug` — protocol wording or template that contradicts itself.
- `enhancement` — wording improvement, new failure-mode catalog entry, new
  example.
- `gate-N-needed` — a real task that the current six gates cannot cleanly
  cover (e.g. non-git recovery for v0.2). Include the scenario.
- `good first issue` — small, well-scoped, no gate-change implications.

If none of these fit, open an issue with `[discussion]` in the title.

## Code of conduct

Be technical, be direct, be kind. Critique the protocol, the example, or the
wording — not the person. Assume good faith on typos and small gaps; demand
precision on gate definitions. Harassment, slurs, and personal attacks get
you removed; substantive disagreement gets you a thread.

## License

This repo is MIT. By submitting a contribution, you agree it is released
under the same MIT terms. See `LICENSE`.
