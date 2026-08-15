# Module 5 — Reviewing, Validating, and Maintaining Agent Output

Covers: human-in-the-loop checkpoints even after automated gates pass, recognizing hallucinations/unsafe changes/weak assumptions gates won't catch, and managing spec drift.

## Hands-on

### Step 1 — Review a flawed change

Open `flawed-change/readings_patch_excerpt.py` and its accompanying test, `flawed-change/test_readings_range_excerpt.py`. This candidate change closes a real gap (FR-005's "physically valid range" check was never built in Module 4's implementation) — and it passes the entire test suite, 12/12 green.

Before reading `review.md`, try to find the bug yourself. Ask: what does this code do to a reading of `99999`? What does the test actually verify?

**Checkpoint**: Compare your findings to `review.md`. The core issue: the code clamps out-of-range values to a boundary and silently stores the clamped value — directly violating constitution Principle II ("MUST NOT silently drop, coerce, default, or fabricate") and the letter of FR-005 ("reject... rather than storing"). No automated gate could have caught this: checklist and analyze both run against spec/plan/tasks, never against implementation code. Only a human reading the actual line `value = max(low, min(value, high))` against the actual requirement catches it.

### Step 2 — Close the gap

`../../project/.specify/memory/constitution.md` was amended to v1.1.0 as a direct result of this finding — Principle I now requires tests to assert the *specific* behavior a requirement mandates, not just a status code. Read the amendment and the Sync Impact Report at the top of the file.

**Discussion**: Would this amendment have prevented the flawed test from being written? Would it have prevented the flawed *implementation*? (It's meant to catch the first, not guarantee the second — human review is still load-bearing even after this fix.)

## Demo talk track (sales / technical evaluation call)

**Suggested time**: 4–5 minutes. This is the highest-leverage moment in the whole demo.

Open `flawed-change/readings_patch_excerpt.py` — a candidate change, plus its own test, both real. Run the numbers: 12/12 tests pass, including the new one.

Then point at one line: `value = max(low, min(value, high))`. Open `review.md` for the live-verified proof — a submitted value of `99999` gets silently stored as `500.0`, and the caller has zero way to know.

*"Checklist and analyze both run against documents — spec, plan, tasks. Neither one ever reads implementation code. A fully green test suite passed this. It took a human reading one line against the actual requirement to catch it. That's not a gap in the tooling — it's the reason human review stays in this loop at all, even after every automated gate is green."*

Close by opening `../../project/.specify/memory/constitution.md` — show the v1.1.0 amendment at the top, triggered directly by this finding.
