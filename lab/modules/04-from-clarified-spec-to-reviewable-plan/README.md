# Module 4 — From Clarified Spec to Reviewable Plan

Covers: translating a clarified, constitution-aligned spec into a technical plan —
architecture choices, constraints, non-functional requirements — using a plan/preview
mode that produces something reviewable before any file changes happen; then
decomposing that plan into small, independently verifiable tasks.

This is the module where your team's Day 1 decision (which of your two specs to carry
forward) starts to matter operationally — everything from here through Module 7 works
on the one spec you picked, not both.

`../../../brownfield-project/specs/001-opcua-threshold-alerting/plan.md` and `tasks.md`
are the real checkpoints — including a genuine corrected decision, not a clean first
draft presented as if it were right the first time.

## Hands-on

### Step 1 — Generate a plan

Run your plan-generation step (`/speckit-plan` / `/speckit.plan` — see
`../../tool-reference.md`) against your Day-1 spec (the one your team chose to carry
forward, post-clarify). Review it **line by line as a team** before accepting it — Step
2 depends on someone having actually read it, not skimmed it.

**Checkpoint**: you should have `plan.md`, `research.md`, `data-model.md`,
`quickstart.md`, and `contracts/api.md`. Compare structure against
`../../../brownfield-project/specs/001-opcua-threshold-alerting/`.

### Step 2 — Edit the plan to correct a decision

Read your plan's technical decisions with one question in mind: if something in here
turns out to be wrong six months from now, who has to act, and what do they need to do?
Find at least one decision your team disagrees with — an architecture choice, a scope
call, a place it took the easy option — and correct it, documenting *why* directly in
the plan.

**Checkpoint**: read `plan.md`'s "Plan Review Note." The first draft of that plan's
Decision 1 put threshold values in a Go map literal inside the source file — cheap, but
means an engineer has to edit code and redeploy to change one number, for a system whose
entire premise is that non-engineers act on its output. The correction moved thresholds
onto the device profile — a mechanism that already existed for exactly this — instead of
inventing a new one. Notice what makes this a *brownfield* correction specifically: the
fix isn't "add a database table" (what the same mistake's correction looked like in an
earlier, greenfield version of this course) — it's "use what's already there." If your
own correction adds something new where something existing would have done the job,
look again before moving on.

### Step 3 — Decompose into tasks

Run task decomposition (`/speckit-tasks` / `/speckit.tasks`). For at least three tasks,
confirm out loud which requirement ID each one maps to.

**Checkpoint**: compare against `tasks.md`. Every implementation task there cites an
FR-###; if yours don't, ask why the task exists. Notice the "Deferred" section — one
real requirement (node/equipment going silent) is explicitly *not* built in this pass,
flagged with a reason, not silently dropped. A deferred task and a forgotten task look
identical in a task list unless the deferral is written down — that's the difference
this section exists to preserve.

See `../../../demo/modules/04-from-clarified-spec-to-reviewable-plan/README.md` for
this module's presenter/demo talk track — not needed to complete the hands-on above.
