# Exhibits A & B — What Went Wrong, and Why It Was Predictable

Exhibit A is real, unedited output from the one-line prompt in `PROMPT.md`. It runs (`python3 -m py_compile output/main.py` passes), and on the surface it looks like a reasonable first draft. Every issue below is one of the four failure modes Module 1 names for ad hoc prompting — none of them are exotic; they're the default outcome of skipping spec, plan, and review.

## Context drift
The prompt said "if something's wrong we should alert someone." Nothing defined *wrong* per equipment type, so the agent picked one hardcoded number for every kind of equipment:

```python
if r.value > 100:
```
`output/main.py:37`

A vibration sensor and a temperature sensor now share a threshold that means nothing for either of them. There was no spec to drift from — the agent's own first guess *became* the requirement, silently.

## Hallucinated API
```python
@app.post("/alerts/{alert_id}/ack")
def ack_alert(alert_id: str):
    for a in alerts_db:
        if a.get("id") == alert_id:
```
`output/main.py:60-63`

`Alert` (line 20) never defines an `id` field. This endpoint is permanently dead — `a.get("id")` is always `None`, so no alert can ever be acknowledged. It would pass a syntax check, pass a smoke test that only checks for HTTP 200, and sit in production silently doing nothing. A code reviewer skimming the diff for "does an ack endpoint exist" would check it off.

## Silent scope creep
Nothing in the prompt asked for email notifications. The agent decided "someone should get notified" and added an SMTP integration pointed at a domain it invented (`smtp.company.com`), then swallowed every failure from it:

```python
except Exception:
    pass  # not critical, alert is already saved above
```
`output/main.py:47-49`

This is worse than doing nothing: it looks like notification coverage exists, so nobody builds the real thing, and every failure of the fake one disappears without a trace.

## Unreviewable diff
One file, no tests, no separation between models/routes/notification logic, equipment registration with no uniqueness check, readings accepted for equipment IDs that were never registered. A reviewer gets one large diff with no acceptance criteria to check it against — so review degrades into "does this look roughly right," which is exactly how the ack-endpoint bug above would get merged.

## Exhibit B — a genuinely better prompt, still not enough

`PROMPT-ADVANCED.md` and `output-advanced/` are what happens when the person writing the prompt actually thinks about the problem first: per-equipment-type thresholds instead of one hardcoded number, real 404/409 error handling, real Pydantic validation, real persistence (SQLite via SQLAlchemy), models split from routes, and an idempotent acknowledge endpoint that actually works (unlike Exhibit A's dead one). It runs end-to-end — verified live: register equipment, submit readings, get alerts, double-acknowledge correctly rejected with 409.

It still has two real gaps, confirmed by actually running it:

- **No duplicate-alert suppression.** Three consecutive critical readings from the same equipment produce three separate open alerts for the same underlying problem — nobody thought to ask "what if it stays broken?" in the single prompt that produced this.
- **No debounce on warning-level readings.** One momentary blip above the warning threshold raises an alert immediately — there was no mechanism forcing anyone to consider "is a single noisy reading enough, or should it require a pattern?"

Both gaps are the same *shape* of problem Exhibit A had — ambiguity nobody was forced to resolve — just one layer more subtle because everything obvious got handled this time. `../../02-governance-and-clarified-spec/README.md` shows the same domain going through an actual clarify pass, where exactly these two questions get asked and answered on the record instead of silently defaulting to "whatever the first draft happened to do."

## The point
None of this required a bad agent or a bad prompt-writer. It's the structurally expected output of asking for a feature with no constitution to set standards, no spec to pin down "wrong" per equipment type, no plan to make the notification decision explicit, and no checklist/analyze gate to catch what's missing before it ships. A better single prompt (Exhibit B) closes the *obvious* gaps. It takes a dedicated clarify step to close the ones that only surface once you ask "what happens when this keeps happening?" — see `../../02-governance-and-clarified-spec/README.md`.
