# Module 2 — Discovery at Scale

Covers: orienting an AI coding agent in a large, existing, unevenly-documented codebase
— connecting it to source, existing docs, and the bug/defect tracker — *before* writing
a spec against it. This is the module Module 1's exhibit sets up directly: neither of
its prompts knew this platform already had a real notification service sitting next to
where the new code would live, because nothing pointed the agent at it. This module is
that missing step.

`../../../brownfield-project/` is real: EdgeX Foundry (Go, ~120 repos upstream, 5
curated here), edgex-ui-go (Angular), OPC UA .NET Standard (C#). Large enough that
"just read the whole thing" isn't a real option — the skill this module teaches is
knowing which few questions to ask, and where a given question is actually likely to be
answered quickly versus needing real digging.

Steps 1–3 below use Pair 1 (OPC UA Threshold Alerting) as the walking example, since
it's the one with a full, real discovery record to check against
(`discovery-log.md`). Run the same steps against **your own team's assigned pair** from
`../../../brownfield-project/assignment-pool.md` — the specific files will differ, the
questions won't.

**Before Step 1**: confirm your MCP connections are actually live, Atlassian
(Jira + Confluence, primary) and GitHub (secondary, cross-reference) —
`../../../lab/mcp-setup.md` has setup for both, for both Copilot and Claude Code, plus a
verification step for each. Step 3 below depends on Atlassian specifically working, not
just being installed — and on you naming your team's exact Jira project key in every
query, not a vague "search Jira."

## Hands-on

### Step 1 — Ask your agent what already exists, before proposing anything new

Point your agent at `repos/edgex-go` and `repos/edgex-ui-go` (real files, real
directory listings — filesystem/grep access covers this step; Step 3 is where the MCP
connection to GitHub actually gets used). Ask it, cold, without telling it the answer:

1. Does this platform already have something that could raise/store/list alerts or
   notifications?
2. Does the dashboard already have any UI for viewing them?

For each answer, note: *where* it came from (an official doc? a README? source code you
had to read yourself?), and how confident you'd be shipping a spec based on it.

**Checkpoint**: compare your findings and — importantly — your *confidence* against
`../../../brownfield-project/discovery-log.md` Q1 and Q4. Q1 should have been fast and
easy for you too (it's genuinely well documented). Q4 is the one to pay attention to: if
your agent stopped at the first plausible-looking file (`NotificationsComponent`) and
reported "there's a notifications component, looks unfinished," it made the same
incomplete read this project's own spec first made — see the note at the bottom of Q4
for why that's left in on purpose.

### Step 2 — Deliberately explore a place documentation doesn't reach

Pick one under-documented corner — `repos/device-opc-ua/internal/` (mostly no
package-level doc comments) or `repos/opc-ua-dotnet` (a large SDK where the low-level
API is documented but "how do I actually use this for X" mostly isn't). Ask your agent
to explain what a specific piece of code does and why, using only what's in the
repository — no outside search. Then ask it to rate its own confidence.

**Checkpoint**: did your agent's confidence match how well-founded its answer actually
was, or did it sound just as sure about a guess as it did about Q1's documented answer?
That gap — an agent that's equally confident whether it's reading a doc or inventing a
plausible-sounding guess — is the actual risk this step exists to surface. `discovery-log.md`'s
closing section names this directly: nothing tells you in advance which question is a
30-second lookup and which needs real digging.

### Step 3 — Search the issue tracker for precedent before scoping anything

Using your MCP-connected **Atlassian** tool (`../../../lab/mcp-setup.md`, verified before this
step — not the browser, not memory), search **your team's Jira project** (name the exact
project key — see "Be precise about project/space" in `mcp-setup.md`) for your assigned
pair's defect ticket and anything else labeled with your `pair-N` tag. Then, optionally,
cross-reference the original upstream report on GitHub for the full history behind it —
your Jira ticket deliberately only has the symptom, the way a real bug report usually
does; the deeper root-cause story, if there is one, lives in the original issue thread.

**Checkpoint** (Pair 1's example — yours will cite different tickets/issues):
`discovery-log.md` Q5 cross-references
[`edgex-go#1187`](https://github.com/edgexfoundry/edgex-go/issues/1187) (a 2019
performance regression on the exact notification-creation path a later spec's success
criterion depends on) and
[`device-opc-ua#53`](https://github.com/edgexfoundry/device-opc-ua/issues/53) (a 2024
OOM report on the exact service a later feature adds more per-reading work to) — the
same defect your Jira ticket SDDTR-2 describes, symptom-only. Both closed, both old-ish,
neither a blocker — but both real precedent a spec written without this step would have
had no way to know about.

### Step 4 — Produce your one-page service/dependency map

Using what Steps 1–3 turned up, fill in `service-map-template.md` for your team's
assignment — one page, the areas your pair actually touches, not the whole platform.
Include the defect you pulled in and its *real* root cause, not just its symptom.

**Checkpoint**: compare shape (not content — yours covers different services) against
`service-map-example.md`, the same template filled for Pair 1 from this module's own
discovery record. Keep your map — Module 3 references it directly when you write your
constitution.

## Demo talk track (5–6 minutes)

**Live vs. pre-built**: Steps 1–2 are reasonable to run genuinely live if you have time
to spare — the point being made (fast doc lookup vs. slow code-reading vs. false
confidence) comes through with real-time agent output, whatever it happens to say, as
long as you're ready to react to what it actually returns rather than a scripted line.
Step 3's specific issues are worth walking from `discovery-log.md` directly — the value
is in *these two real issues*, not "an agent found some issues," and a live search
might not surface them from a differently-worded query.

1. Open `repos/edgex-go/openapi/support-notifications.yaml` next to
   `discovery-log.md` Q1 — "this one's fast, this is what good documentation buys you."

2. Open `repos/edgex-ui-go/web/src/app/notifications/notifications.component.ts` —
   nearly empty — then, before saying anything, open the sibling
   `notification/notification-list/notification-list.component.ts` and scroll through
   its 300 real lines. "Stop reading after the first file and you'd report this feature
   doesn't exist. It does — one directory over." Then open `spec.md`'s User Story 2 and
   show the corrected paragraph: *this project's own first draft made exactly that
   mistake, in a real, git-committed spec, before it got caught and fixed.*

3. Open `discovery-log.md` Q3 — the acknowledge-endpoint behavior — and walk through why
   it's the hardest kind of finding: not wrong documentation, no documentation, at all,
   on that specific point. Point at the OpenAPI spec's response codes (200/400/500, no
   409) as "a negative fact — the absence of a 409 response is itself the discovery,
   and you only notice an absence if you know to look for it."

4. Close on `discovery-log.md` Q5 — open the two real GitHub issues live in a browser.
   Quote: *"Neither of these blocks anything. That's not the point. The point is a spec
   written without five minutes of searching the tracker has no way to know they
   happened — and 'this exact service already had an OOM report on exactly this kind of
   workload' is not a fact you want to discover after implementation."*

5. Open `service-map-example.md` — one page, three services, one real defect with its
   real (not filed-against) root cause identified. "This is the entire output of this
   module. Not a document about the codebase — a map of exactly the corner of it your
   team is about to touch, and nothing else. Module 3 starts from this, not from a blank
   page."
