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

See `../../../demo/modules/08-common-pitfalls-and-anti-patterns/README.md` for this
module's presenter/demo talk track — not needed to complete the hands-on above. Next:
`../../capstone/` (formal requirements + walkthrough).
