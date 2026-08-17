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

## Hands-on

### Step 1 — Write a constitution from what you actually found

Do this in your team's fork from Module 2 Step 5 (`my-team-work/`, or whatever you
named it) — not a new directory. Using your team's `service-map.md` from Module 2,
write a constitution for the area your assignment touches. Encode what you found — real
conventions already in use (naming, error-handling patterns, existing services to
extend rather than duplicate) — not a generic best-practices list you'd write for a
greenfield project. Use `/speckit.constitution` (see `../../tool-reference.md`) rather than hand-editing the
template.

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

Draft a spec for your pair's **feature**, and a separate spec for your pair's **defect**
— same EARS-style requirement format for both, but notice they read differently: a
feature spec describes new desired behavior from scratch; a defect spec describes
*correct* behavior against a symptom you didn't choose (see
`defect-001-device-opc-ua-oom/spec.md`'s "Problem Statement" section — there's no
equivalent section in a feature spec). Run a clarify pass (`/speckit.clarify`) on
**both** — this is where your service-map.md's discovery
actually gets folded in, since the raw ticket text alone won't mention it.

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
