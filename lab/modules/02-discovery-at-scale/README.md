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
`../../mcp-setup.md` has setup and a verification step for each. Step 3 below depends
on Atlassian specifically working, not just being installed — and on you naming your
team's exact Jira project key in every query, not a vague "search Jira."

**Two ready-to-use prompt templates** turn Steps 1–3 below into a single copy-pasteable
prompt instead of something you compose yourself: `discovery-prompt-doc-assisted.md`
(your MCP connections are live, you have a real ticket to start from) and
`discovery-prompt-zero-doc.md` (no working documentation at all — Step 2 below is
exactly this case). Use whichever matches what you're actually facing; they ask
different questions on purpose, not the same questions with different framing.

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
API is documented but "how do I actually use this for X" mostly isn't). This is exactly
what `discovery-prompt-zero-doc.md` is for — use it here instead of composing your own
prompt; it produces a Service Boundary Card worth keeping, not just an answer to read
once and discard. Then ask your agent to rate its own confidence.

**Checkpoint**: did your agent's confidence match how well-founded its answer actually
was, or did it sound just as sure about a guess as it did about Q1's documented answer?
That gap — an agent that's equally confident whether it's reading a doc or inventing a
plausible-sounding guess — is the actual risk this step exists to surface. `discovery-log.md`'s
closing section names this directly: nothing tells you in advance which question is a
30-second lookup and which needs real digging.

### Step 3 — Search the issue tracker for precedent before scoping anything

Using your MCP-connected **Atlassian** tool (`../../mcp-setup.md`, verified before this
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

### Step 5 — Set up your team's persistent workspace

Everything from here through the Capstone needs a real place to live — not the
throwaway scratch directory from Module 1 Step 2 (that was a one-time comparison, meant
to be discarded), and not the shared read-only `brownfield-project` clone from Day 0
either. Fork `brownfield-project` itself to your own (or your team's) GitHub account:

```
gh repo fork Siemens-training/brownfield-project --clone=false
git clone https://github.com/<your-account>/brownfield-project.git my-team-work
cd my-team-work
git submodule update --init --recursive --depth 100
```

This fork **is** your team's real workspace from now on:
- Save your filled-in `service-map.md` from Step 4 here (anywhere sensible — e.g. a new
  `team-notes/` folder at the root).
- Module 3's constitution and specs (`/speckit.constitution`, `/speckit.specify`) run
  **here**, at this fork's root — `.specify/` and Spec Kit's commands are already
  scaffolded (this fork inherited them from `brownfield-project`), so there's no
  `specify init` to re-run. Your new spec becomes `specs/002-...` (or whatever number
  Spec Kit assigns), sitting alongside the untouched instructor reference
  (`specs/001-opcua-threshold-alerting/`, `specs/defect-001-device-opc-ua-oom/`) — don't
  edit those, they're your checkpoints, not your starting point.
- Your actual **code** changes happen inside `repos/<your-repo>/` in this same
  checkout — `setup-guide.md`'s note on forking the specific curated repo(s) your pair
  touches (separately from this) still applies; add that fork as a second remote inside
  `repos/<your-repo>/` and push there.
- This fork is what you'll share for Capstone submission — "your team's repo/branch"
  means this one.

**Checkpoint**: `git log --oneline -1` inside your fork should show it's genuinely
yours (your own remote, not `Siemens-training`'s). If your team has multiple members,
agree now on who pushes where — one shared fork with everyone pushing to it, or one
member's fork as the team's canonical copy with others opening PRs into it. Either
works; not deciding now is what causes conflicts in Module 4.

See `../../../demo/modules/02-discovery-at-scale/README.md` for this module's
presenter/demo talk track — not needed to complete the hands-on above.
