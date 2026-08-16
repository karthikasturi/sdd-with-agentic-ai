# Notes: What Went Wrong, and What "Better" Still Missed

Both `output/` and `output-advanced/` are real, unedited, and both actually run — every
claim below was verified by building and exercising the binaries, not read off the
source. Verification commands are inline so you can reproduce each one yourself.

## Exhibit A (`output/`) — the one-line prompt

Four failure modes, each with a specific line to point at:

- **Context drift** — `main.go`, `const threshold = 100.0`. One number, applied to every
  reading regardless of equipment or measurement type. The prompt never said what "bad"
  means for a given piece of equipment, so the agent picked something plausible-looking
  and moved on.

- **Hallucinated understanding** — `acknowledgeAlert`, the `for _, alert := range alerts`
  loop. This is real, idiomatic-*looking* Go that compiles cleanly and returns `200 ok`
  — and never acknowledges anything. Ranging over a slice by value gives you a copy of
  each element; `alert.Acknowledged = true` mutates that copy, not `alerts[i]`. Verified
  live:

  ```
  curl -X POST localhost:8080/alerts/ack?id=1   # → 200 "ok"
  curl localhost:8080/alerts                    # → still "acknowledged":false
  ```

  This is the one to sit with: it isn't a typo you'd catch by reading the function name,
  and a smoke test that only checks the HTTP status code (not the actual stored value)
  passes it every time.

- **Silent scope creep** — `notifyPager`, an uninvited call to
  `http://pager.internal/notify`, a URL nobody configured, wrapped in
  `if err != nil { return }`. Nothing in the prompt asked for paging. The failure mode
  isn't that it tried and failed — it's that the failure is invisible; nothing surfaces
  it, ever.

- **Unreviewable diff** — one file, no separation between HTTP handling and business
  logic, no tests, no equipment-uniqueness check, no input validation at all. There's
  nothing here a reviewer could approve or reject piece by piece; it's take-it-or-leave-it.

## Exhibit B (`output-advanced/`) — the more thoughtful prompt

A more specific single prompt produces real, meaningfully better code — verified, not
assumed:

```
curl -X POST localhost:8080/readings -d '{"equipmentId":"ghost", ...}'   # → 404, real check
curl -X POST localhost:8080/alerts/ack?id=1                              # → 200
curl -X POST localhost:8080/alerts/ack?id=1                              # → 409, rejected correctly
```

Per-type thresholds (`models.go`'s `Thresholds` map) replace the global constant.
Unregistered equipment and non-numeric values are rejected explicitly. Acknowledgment is
idempotent-*rejecting*, not idempotent-*accepting* — the exact bug from Exhibit A, fixed
for real this time, with an index-based loop instead of a range-by-value one. No
uninvited integrations. Split across two files instead of one.

**But it still has a real gap, confirmed live:**

```
# three consecutive critical readings for the same equipment
curl -X POST localhost:8080/readings -d '{"equipmentId":"eq-1","type":"temperature","value":96}'
curl -X POST localhost:8080/readings -d '{"equipmentId":"eq-1","type":"temperature","value":97}'
curl -X POST localhost:8080/readings -d '{"equipmentId":"eq-1","type":"temperature","value":98}'
curl localhost:8080/alerts   # → three separate open alerts, not one
```

Nobody asked "what happens when the same problem keeps recurring across many readings?"
— so nothing in the code asks it either. Every out-of-range reading floods a fresh alert.
This is exactly the gap **Module 3's clarify pass** exists to catch, before any code gets
written — not the kind of thing a better prompt reliably prevents on its own, however
carefully worded.

**And there's a second gap, of a different kind, that a better prompt can't fix at all:**
this code doesn't know it's not supposed to exist. Nothing in either prompt mentioned
that this course's actual codebase — EdgeX Foundry — already ships a real, running
notification service (`support-notifications`) built to do exactly this job, or that its
own device service (`device-opc-ua`) already owns the OPC UA subscription this reading
would have come from in real life. A cold prompt, however well written, has no way to
know that, and reinvents a parallel alert store from nothing. That's not a prompt-wording
problem — no amount of detail in *this* prompt would have surfaced it, because nothing in
it ever pointed the agent at the existing codebase. That's what **Module 2 (Discovery at
Scale)** exists to fix: orienting an agent in what's already there, *before* asking it to
build anything, so "does this already exist?" gets asked before the code is written
instead of found later in review.
