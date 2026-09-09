# ai-sdlc failure modes

A working cheat sheet of the bug classes that the ai-sdlc dogfood surfaced
in real code, even when the project's own test suite passed.

Every class here was caught during **Gate 4 (Context)** of the protocol.
Raw narrative: [`journal/SUMMARY.md`](../journal/SUMMARY.md).

The protocol does not auto-detect these classes; agents and reviewers
**must** look for them by name when a `DONE.md` looks suspiciously green.

---

## 1. Code defect — passing test on the wrong branch

**Symptom.** Test runs, returns expected status, gate-3 captures it. The
function is structurally present but the test only exercised one branch.

**Dogfood.** Calora `/api/health` always returned 200, even when the AI
provider was down. Tests checked the happy path; the bug was in the
failure path. Commit: `calora 9a9dc31`.

**Pattern (illustrative, simplified):**

```text
// Bug: returns 200 unconditionally regardless of dependency state.
//       Tests only ever hit the happy path.
function health() { return { status: 200, body: { status: "ok" } }; }
```

**Gate 4 catch.** Read the function under test. List every return
statement. For each, find a matching test. A return statement with no
matching test = untested surface area = the bug.

---

## 2. Copy-paste defect — duplicated source files drift apart

**Symptom.** A helper is copy-pasted between `lib/x.ts` and `test/x.test.ts`.
One copy gets updated; the other doesn't. The test passes against the
wrong copy.

**Dogfood.** Calora's image-validator helper was duplicated into the test
file; the test copy got validation rules first, the source copy lagged.
Commit: `calora c0ad547`.

**Pattern.**

```text
// lib/validate.ts        ← source, gets one set of rules
// test/validate.test.ts  ← test, copy-pasted; gets the SAME rules initially,
//                          then a refactor adds rules to ONE copy only.
```

**Gate 4 catch.** `git grep -n "<symbol>"` in the changed callers. Two
matches with different bodies = drift.

---

## 3. Format defect — header emitted per iteration

**Symptom.** A metric header or log banner that should appear once is
emitted inside a loop. Tests check "the line is present"; rarely do they
check cardinality.

**Dogfood.** Calora's `/api/metrics` Prometheus endpoint emitted `# HELP`
and `# TYPE` once per scraped series iteration, polluting scrapes.
Commit: `calora 4da7c18`.

**Pattern.**

```text
for each ref:
    emit "# HELP <name>"   ← these are loop-invariant
    emit "# TYPE <name>"
    emit "<name> <value>"
```

**Gate 4 catch.** Read every `for` loop that pushes to a list or string.
Hoist any line that doesn't depend on the loop variable out of the loop.
If you can't, leave a `ponytail:` comment naming the ceiling and the
upgrade path.

---

## 4. Discipline defect — version format allowed to drift

**Symptom.** A version-string regex (`v\d+`) accepts anything that starts
with `v`. Deploys ship `v1` and never bump it; freshness is not enforced.

**Dogfood.** Calora's service worker `CACHE_VERSION` was `v\d+`, so `v1`
shipped unchanged for months. Commit: `calora 60266dc`.

**Pattern.**

```text
// Too permissive:  "v" + process.env.VERSION  → could be "v" or "v0"
// Test only checks: /^v\d+$/                    → accepts both
```

**Gate 4 catch.** Read the format regex. Tighten it to your real
freshness rule (`vYYYYMMDD-NN`) and add a test that fails on the
unconstrained form.

---

## 5. Math defect — modulo bias

**Symptom.** `bytes[i] % N` to pick from `N` alphabet buckets produces
uneven distribution when `N` does not divide 256. Short codes or
random IDs end up clumped.

**Dogfood.** Specboard's `generateSlug` used `bytes[i] % 56`; 4 buckets
got 2x probability. Commit: `specboard 52059cf`.

**Pattern.**

```text
// Bias:  when N does not divide 256, low (N, 256%N) buckets over-represent.
//        E.g. for N=56:  256 mod 56 = 32  →  32 buckets get extra draws.
```

**Gate 4 catch.** When you see `% alphabet-size` on bytes, ask "does
256 mod N == 0?" If not, bias is real. Reject-and-resample or restrict
the input range to a multiple of N.

**Test improvement.** "All chars used at least once" does NOT catch this.
Use count-tolerance on N ≥ 10000 draws; assert max-bucket deviation
within ±25% of expected mean. See journal/SUMMARY.md §"Process changes
observed" for the empirical ranges that worked.

---

## How to use this file

When you review a `DONE.md` (yours or someone else's):

1. Read gate 3 evidence — does the test count match what `task.md`
   promised?
2. Read gate 4 — is each acceptance criterion traceable to a file +
   line?
3. Walk the five classes above against the diff. If any class "fits,"
   look at the actual code; don't trust the green test.

A passing test suite is not proof of correctness if the tests don't
cover the right shape of the contract. Each of the 5 classes above had
a test suite that "passed" while a real bug shipped silently.

---

## Adding a new failure mode

Edit this file. Keep entries self-contained:

- One named class
- One minimal pattern (≤10 lines)
- One sentence: how gate 4 catches it
- Link to a real commit, not a hypothetical

PRs that add entries without a real commit behind them will be asked to
either find the commit or wait until they have one.
