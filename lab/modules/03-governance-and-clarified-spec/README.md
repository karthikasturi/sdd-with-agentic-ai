# Module 3 — Establishing Governance and Writing a Clarified Specification

Covers: encoding project/per-service principles as a constitution, informed by what
Module 2's discovery actually found (not invented from scratch); writing EARS-style
requirements from **both** a feature request and a real defect; the clarify pass; and
where this all sits inside the SDLC your team already runs.

**Where this fits your existing SDLC** (not a separate process replacing it): the
constitution and a clarified spec are your requirements-and-design stage. The plan and
tasks you'll write in Module 4 are technical design and iteration planning. Checklist and
analyze (Module 5) are QA and test planning. Implement (also Module 5) is development.
Review plus living documentation (Module 6) are code review, QA, and maintenance. Nothing
here is a new lifecycle bolted onto your existing one — it's your existing one, made
explicit and agent-checkable at every stage.

`../../../brownfield-project/specs/001-opcua-threshold-alerting/` (the feature half of
Pair 1) and `../../../brownfield-project/specs/defect-001-device-opc-ua-oom/` (its
defect half) are the two real, complete checkpoints for this module — one feature spec,
one defect spec, same as what your team produces below.

**Working in a much larger monorepo day to day** (50-100+ modules, not this course's
5 curated repos)? `../../reference/monorepo-scaling.md` covers where Spec Kit actually
recommends specs live at that scale — a single root-level `specs/` (what this course
uses) isn't the documented pattern once you're past a handful of independently-owned
modules.

## Hands-on

### Step 1 — Write a constitution from what you actually found

Do this in your team's fork from Module 2 Step 5 (`my-team-work/`, or whatever you
named it) — not a new directory. Using your team's `service-map.md` from Module 2,
write a constitution for the area your assignment touches. Encode what you found — real
conventions already in use (naming, error-handling patterns, existing services to
extend rather than duplicate) — not a generic best-practices list you'd write for a
greenfield project. Use `/speckit.constitution` (see `../../tool-reference.md`) rather than hand-editing the
template.

**Sample input** (illustrative — shaped from Pair 1's real `service-map.md` findings,
not a literal transcript; yours should read the same way but cite *your* pair's
actual findings, not this text):

```
/speckit.constitution Our service map shows this feature extends device-opc-ua,
which already uses the device-sdk-go/v4 framework and the gopcua/opcua client
library — no alternative library should be introduced. It integrates with EdgeX's
existing support-notifications service rather than a new alert store. Establish
principles for: test-first development matching this repo's existing table-driven
Go test style; never silently dropping, coercing, or defaulting an invalid OPC UA
reading; every requirement traces to an approved spec ID, with scope creep treated
as a review-blocking finding; new code MUST follow the target repo's existing
conventions (device-sdk-go interfaces, extending support-notifications) rather than
introducing a parallel pattern, since this is brownfield work, not greenfield;
typed request/response models only, matching EdgeX's existing
deviceName/resourceName/profileName field-naming conventions; and every alert
state transition logged with actor, timestamp, and prior state.
```

Notice what makes this a *brownfield* input, not a greenfield one: it names specific
real things Module 2 found (`device-sdk-go/v4`, `support-notifications`, EdgeX's
field-naming convention) instead of generic principles an agent would invent with no
codebase context at all. If your own input doesn't cite anything specific from your
`service-map.md`, that's the same gap the Step 1 checkpoint below is looking for.

**Checkpoint**: compare against
`../../../brownfield-project/.specify/memory/constitution.md`. Don't expect to match it
— it covers a different area — but check specifically for Principle IV (Convention
Conformance): does your constitution name a specific existing pattern your area should
follow, the way Principle IV names "extend `support-notifications`, don't invent a
parallel alert store"? A constitution that only says generic things like "write tests"
and "handle errors" hasn't actually used Module 2's discovery yet.

### Step 2 — Draft two specs, clarify both

**Input for each `/speckit.specify` call is your pair's actual assigned text, not a
free invention**: your Jira ticket's Description field (SDDTR-N, pulled in Module 2
Step 3 — e.g. *"Evaluate subscribed OPC UA readings against per-resource thresholds and
raise EdgeX Notifications when a reading crosses one..."*) if your Atlassian MCP
connection is live, or the matching paragraph in
`../../../brownfield-project/assignment-pool.md` otherwise — same content either way,
Jira's is just the symptom-only/no-root-cause version for the defect side. Paste that
text as the argument to `/speckit.specify`, once for the feature,
once for the defect — don't retype it from memory or summarize it down, the point is
starting from what was actually assigned, the way a real ticket would.

**Sample input — real, not illustrative**: this is Pair 1's actual `SDDTR-1`/`SDDTR-2`
ticket text (`jira-content.md`), the real input that produced the checkpoint specs
below. Yours will be your own pair's text from `assignment-pool.md`, but the shape —
paste the ticket verbatim, nothing more — is exactly this:

```
/speckit.specify Evaluate subscribed OPC UA readings against per-resource
thresholds and raise EdgeX Notifications when a reading crosses one. Staff should
be able to see and acknowledge these from the dashboard.
```

```
/speckit.specify Collecting data from a simulated OPC UA server via device-opc-ua
results in an out-of-memory condition after approximately 11 hours, even with a
retention policy configured: RETENTION_ENABLED: true, RETENTION_INTERVAL: 10s,
RETENTION_MAXCAP: 10, RETENTION_MINCAP: 5. Redis key count exceeded 10 million
before the crash. Debug logs show "Prepare to delete 0 readings" on every
retention pass, despite the growing key count — possibly the retention cleanup
isn't actually running, but I haven't confirmed that.
```

Notice the defect input is symptom-only — no root cause, no "the fix is X." That's
real, not simplified for the course: a bug report reads like this before anyone's
investigated it. Finding the actual root cause (a retention-interval/cap mismatch,
not a broken cleanup routine) is what your defect spec and its clarify pass are for
— see the checkpoint below, not this input.

Draft a spec for your pair's **feature**, and a separate spec for your pair's **defect**
— same EARS-style requirement format for both, but notice they read differently: a
feature spec describes new desired behavior from scratch; a defect spec describes
*correct* behavior against a symptom you didn't choose (see
`defect-001-device-opc-ua-oom/spec.md`'s "Problem Statement" section — there's no
equivalent section in a feature spec). Run a clarify pass (`/speckit.clarify`) on
**both** — this is where your service-map.md's discovery
actually gets folded in, since the raw ticket text alone won't mention it.

**What running `/speckit.clarify` actually looks like**: unlike `/speckit.specify`,
it takes no text argument — you run it bare, and your agent asks you a short series
of numbered questions, each with lettered options, one at a time. You answer with a
letter (or write your own if none fit). Real excerpt, Pair 1's feature spec (full
transcript: `../../../brownfield-project/specs/001-opcua-threshold-alerting/clarify-log.md`):

```
/speckit.clarify

Question 1 of 3 — Node Silence
If a subscribed OPC UA node stops reporting new values entirely, should that
silence itself be treated as something worth alerting on?

  A) Treat prolonged silence as a MINOR-severity "node offline" Notification
     after a configurable window
  B) Do not alert on silence — only evaluate readings that actually arrive
  Short) Provide a different short answer

Your answer: A, with the window set to 60 minutes
```

Three real questions came out of Pair 1's feature clarify pass this way — not
because the spec was written carelessly, but because a one-line ticket genuinely
can't anticipate them. Expect the same for yours: if `/speckit.clarify` comes back
with zero questions on a spec built from a paragraph-level ticket, that's usually a
sign the spec glossed over ambiguity rather than resolved it — look again before
treating "no questions" as a good sign.

**Checkpoint**: feature half — compare structure against `spec.md` and the ambiguities
you found against `clarify-log.md` (three real ones there: equipment/node going silent,
single-vs-consecutive-reading debounce, and a brownfield-specific one — extend an
existing service or add a new one). Defect half — compare against
`defect-001-device-opc-ua-oom/spec.md` and its `clarify-log.md` (two real ones: is the
cap per-device or global, what happens to ingestion during a slow retention pass). If
your defect spec doesn't have a "why is this filed here but maybe fixed elsewhere"
question anywhere in it, look again — that question is usually there once you actually
read the code the defect touches, not just its title.

### Step 3 — Choose one to carry forward

As a team, pick **one** of your two specs to take through Modules 4–7. Write down, in
one paragraph, *why* — not just "it seemed more interesting." Good reasons tend to be
about which one you can actually verify end-to-end in the time available, not which one
sounds more impressive. Set the other aside, unmodified — you'll rewrite it in Module 8
with a few days of hindsight, then take it through the full lifecycle for the first time
in the Capstone.

**Checkpoint**: no file to compare against here — this decision is yours, and the two
specs behind it are both real either way. The thing to avoid: picking the feature every
time because defects feel like someone else's mess. A defect spec, planned and
implemented properly, is exactly as real a demonstration of this lifecycle as a feature
is — that's the point of pairing them.

See `../../../demo/modules/03-governance-and-clarified-spec/README.md` for this
module's presenter/demo talk track — not needed to complete the hands-on above.
