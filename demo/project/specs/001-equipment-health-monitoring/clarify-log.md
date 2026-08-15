# Clarify Pass — Presenter Transcript

`spec.md` already contains the canonical `## Clarifications` record. This file reproduces the actual exchange in the format `/speckit-clarify` presents it in, for walking a live audience through *why* each question got asked and what changed as a result — this is the moment in the demo that's hardest to fake with a hand-written spec.

---

## Question 1: Equipment Silence

**Question:** If a piece of equipment stops sending readings entirely, should that silence itself be treated as something worth alerting on?

**Why it matters**: Without an answer, "equipment goes quiet" and "equipment is healthy and idle" look identical to the system — a dead sensor or a network dropout would be invisible until someone happened to notice manually.

**Recommended:** Option A — industrial monitoring systems treat prolonged silence as its own failure mode (a "dead man's switch"), and it costs nothing to implement alongside threshold evaluation.

| Option | Description |
|--------|-------------|
| A | Treat prolonged silence as a warning-severity "equipment offline" alert after a configurable window |
| B | Do not alert on silence — only evaluate readings that actually arrive |
| Short | Provide a different short answer |

**Answer given**: A, with the window set to 60 minutes.

**Spec sections touched**: Edge Cases, Functional Requirements (new FR-013).

---

## Question 2: Single Reading vs. Consecutive Readings

**Question:** Should one out-of-range reading raise an alert immediately, or should it need to happen a few times in a row first?

**Why it matters**: Sensors on physical equipment produce occasional noise. Alert on every single blip and maintenance staff start ignoring alerts; require too much confirmation and a genuinely dangerous reading sits unflagged.

**Recommended:** Option C — split the behavior by severity, so genuinely dangerous readings still alert instantly while routine sensor noise doesn't create alert fatigue.

| Option | Description |
|--------|-------------|
| A | Always alert on the first out-of-range reading |
| B | Always require 2 consecutive out-of-range readings before alerting |
| C | Critical-level readings alert immediately; warning-level readings require 2 consecutive readings |
| Short | Provide a different short answer |

**Answer given**: C.

**Spec sections touched**: Functional Requirements (FR-007 narrowed to critical-only, new FR-014 for the warning-tier debounce rule), Success Criteria (SC-001 narrowed to critical-severity to stay accurate now that warning-severity has a different latency profile).

---

## Why this is the point of the exercise

Neither question is exotic — a competent engineer reading the original one-line feature description would eventually hit both in code review, after something was already built the wrong way. Catching them here costs two short answers and a few edited sentences. Catching them after `/speckit-implement` costs a rewritten threshold-evaluation path and a re-reviewed PR. This is the same gap Exhibit A (`vibe-coding-exhibit/`) fell into blind — it hardcoded a single global threshold and never considered either question, because nothing forced it to.
