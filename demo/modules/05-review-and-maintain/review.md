# Module 5 Review Exercise — Findings

## The change under review

`flawed-change/readings_patch_excerpt.py` — a candidate change adding physically-valid-range enforcement to `POST /readings`, closing the half of FR-005 that Module 4's implementation left open (Module 4 only enforced "missing/non-numeric," via Pydantic's type system; "outside the physically valid range for its measurement type" was never actually built).

**Status when this reached review**: full test suite green — 11 existing tests plus the new `test_out_of_range_reading_is_handled` in `flawed-change/test_readings_range_excerpt.py`, 12/12 passing. Verified directly, not asserted secondhand.

## What automated gates already checked — and correctly passed

- **Tests**: All green, including a new test that specifically targets this code path.
- **Checklist / analyze** (Module 4): Not applicable here — those gates run against `spec.md`/`plan.md`/`tasks.md` *before* implementation. This flaw is purely in code that conforms to the letter of a correct spec while violating it in behavior. Neither gate ever reads implementation code, so neither one *could* have caught this — that's the point of this exercise, not a defect in either gate.

## What a human reviewer should catch

Read the actual line: `value = max(low, min(value, high))`. FR-005 says out-of-range readings must be **rejected with an explicit error, rather than storing or evaluating them**. This code does the opposite of reject — it silently clamps the value to the boundary and stores *that*, not what was submitted. A reading of `99999` on a compressor gets silently persisted as `500.0`. Verified live:

```
API response: {'reading_id': 1, 'alert_raised': 'critical'}
Submitted value: 99999
Actually stored value: 500.0
```

The caller has no way to know their input was altered — the response doesn't echo the value back, and the 201 status code reads as success. This is a direct violation of constitution **Principle II (Explicit Data Integrity, NON-NEGOTIABLE)**: "The system MUST NOT silently drop, coerce, default, or fabricate any sensor reading... Invalid or out-of-range input MUST be rejected with an explicit 4xx error."

The test that shipped with the change is technically well-formed — it just never asks the one question that would have caught this: *what actually got stored?* It confirms the endpoint didn't crash, not that it did the right thing.

## Why this matters beyond one bug

This is Exhibit A and Exhibit B's exact failure mode (`../01-vibe-coding-vs-spec-driven/vibe-coding-exhibit/NOTES.md`) recurring one stage later in the pipeline: an ambiguity about "what happens on bad input" quietly resolved by whatever the implementation happened to do, because nothing forced the question to be asked out loud. The difference is that this time it happened *after* a correct spec, a passing checklist, and a clean analyze report — proving those gates narrow the failure surface, they don't eliminate it. Human review of actual behavior against the actual requirement is still load-bearing.

## Remediation

1. **Reject the change as submitted.** `value` must be validated and rejected with a 422 (matching the existing pattern for non-numeric input), never silently altered.
2. **Constitution amendment** (this repo, real change — see `../../project/.specify/memory/constitution.md` v1.1.0): Principle I now explicitly requires that tests assert the specific behavior a requirement mandates, not just a status code, closing the gap that let `test_out_of_range_reading_is_handled` pass while testing the wrong thing.
3. **Correct implementation** is left as an exercise: raise `HTTPException(422)` when a value falls outside `VALID_RANGES`, symmetric with the existing unregistered-equipment (404) and unknown-type (422) handling in `../../project/app/routers/`.
