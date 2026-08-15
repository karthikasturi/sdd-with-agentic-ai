# Module 8 — Common Pitfalls & Anti-Patterns

Covers: over-specifying vs. under-specifying, and why a thin constitution or a skipped
clarify pass usually shows up here first; token and cost tradeoffs; case studies in
spec-driven workflows that succeeded and failed at scale.

`escalation-antipattern/` is the instructor exhibit: the same small feature (alert
escalation, a natural next increment on top of this course's own real threshold-alerting
work) specified two wrong ways and one corrected way, all three Go outputs real and
verified to build.

Your own hands-on work this module is on **your team's set-aside spec** from Day 1 —
the half of your assignment pair (Module 3) you didn't carry forward. For the
instructor's own pair, that's `../../../brownfield-project/specs/defect-001-device-opc-ua-oom/spec.md`
— useful as a worked example of what "rewrite with hindsight" looks like, even though
your team's set-aside spec covers different ground.

## Hands-on

### Step 1 — Critique the exhibit before your own spec

Open `escalation-antipattern/spec-under-specified.md` and `spec-over-specified.md` —
both describe the same feature. Before reading the Go outputs or `comparison.md`, write
down specifically what you think will go wrong with each — not "it's vague" or "it's
too detailed," but what an implementer would actually be forced to invent, or what an
over-specified version would actually lock in prematurely.

**Checkpoint**: compare your predictions against `comparison.md`. Pay attention to the
over-specified example's specific failure: it reintroduces a paging integration that
this project's own real `spec.md` already ruled out of scope — a concrete instance of
"more detail" not being automatically safer than "less detail."

### Step 2 — Critique your own set-aside spec

Now do the same to the spec your team set aside on Day 1 (Module 3) — the half of your
pair you didn't build. With a few days of hindsight from actually building its
counterpart, is it under-specified, over-specified, or does it hold up? Be specific,
the way `comparison.md` is specific.

**Checkpoint**: no external answer key — this is your own team's spec. The instructor
example: `defect-001-device-opc-ua-oom/spec.md`'s Assumptions section explicitly scoped
out a related question (ingestion backpressure during a slow retention pass) rather than
folding it in — on rereading with hindsight, is that still the right boundary, or did
building the *other* half of the pair reveal something that changes the answer?

### Step 3 — Rewrite it and re-run it

Rewrite your set-aside spec based on Step 2's findings. Re-run it through your agentic
coding tool and compare the output against what a first pass at this spec would likely
have produced.

**Checkpoint**: you're not comparing against a pre-built answer here on purpose — this
is the Day-1-to-now arc the Capstone measures. Keep both versions; the Capstone's
documented review trail references the difference directly.

## Demo talk track (5–6 minutes)

**Live vs. pre-built**: walk `escalation-antipattern/` from the real files — the specific
citation against this project's own real `spec.md` is the point, not a generic "over-
specification is bad" claim a live example might not land as concretely.

1. Open `spec-under-specified.md` next to `output-from-under-specified.go` — point at
   `REASONABLE_TIME = 15 * time.Minute`, arbitrary, and the destructive `n.Severity =
   "CRITICAL"` overwrite that never touches the platform's own existing `ESCALATED`
   status value. *"The schema already had the field this needed. Nothing in the spec
   told the agent to look for it."*

2. Open `spec-over-specified.md` next to `output-from-over-specified.go` — point at the
   unconditional POST to `pager.internal`, then flip to
   `../../../brownfield-project/specs/001-opcua-threshold-alerting/spec.md`'s
   Assumptions section and read the paging line aloud. *"Not a hypothetical violation.
   A citation against a file that already exists, that this exact course built, three
   modules ago."*

3. Close on token/cost: *"Every gate this course has run — clarify, checklist, analyze,
   review — cost tokens and time before code existed. Finding 1 and Finding 2, back in
   Module 5, are the receipts: a few minutes each, versus what either gap would have
   cost found after merge. That's the actual case for the cost, not a slide about
   ROI — two things that really happened, in this exact feature's own history."*
