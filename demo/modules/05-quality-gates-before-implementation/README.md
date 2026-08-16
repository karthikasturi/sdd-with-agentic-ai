# Module 5 — Quality Gates Before Implementation

Covers: generating and running a requirements checklist (a "unit test suite for
requirements"); the analyze cross-artifact consistency pass; budgeting agent token/cost
usage across a plan; and where security, compliance, and code-coverage checks fit as
additional gates — before any implementation code exists.

`../../../brownfield-project/specs/001-opcua-threshold-alerting/checklist.md` and
`analyze-report.md` carry **two** real findings each caught something genuine: one from
the original pass (a missing requirement), one added on Day 2 specifically for this
module (a missing security statement). Both were fixed in the actual artifacts, not
just noted and left broken.

## Hands-on

### Step 1 — Generate and run a checklist

Run your checklist step (`/speckit-checklist` / `/speckit.checklist` — see
`../../../lab/tool-reference.md`) against your spec. Read every item — don't just check the
boxes that auto-passed.

**Checkpoint**: `checklist.md` has one item that failed on first pass — CHK004,
duplicate-alert suppression, resolved by adding FR-015 directly to `spec.md`. Did your
checklist surface anything comparable? If it came back all-green on the first try, look
harder at CHK004's category (alert/notification lifecycle: "what happens when the
condition keeps recurring?") — it's a real gap, not manufactured for this exercise.

### Step 2 — Run analyze

Run your cross-artifact consistency check (`/speckit-analyze` / `/speckit.analyze`)
across spec, plan, and tasks.

**Checkpoint**: `analyze-report.md` documents a real HIGH-severity finding (F1) about a
plan that assumed a shared platform endpoint enforced something it doesn't — confirmed
by reading that endpoint's actual source and its own OpenAPI contract, not guessed.
Resolve your own findings the same way: fix the artifact, don't just note it and move on.

### Step 3 — Add a security/compliance or code-coverage checklist item

Add at least one checklist item that specifically checks a security, compliance, or
code-coverage concern — not just functional correctness.

**Checkpoint**: `checklist.md`'s "Security, Compliance & Code Coverage" section (added
Day 2, after the original pass) has two: CHK016 asks whether the plan states its new
HTTP boundaries' auth posture — it originally **failed**, for real; see Finding 2 and
the "Security & Auth Path" section it caused to be added to `plan.md`. CHK017 asks
whether new code's test coverage holds up against this repo's existing baseline —
verified with a real command, not asserted: `go test ./internal/threshold/... -cover`
returns 94.3%, against the pre-existing `internal/driver` package's 38.4% in the same
repo. Run the same command yourself against your own new code before checking this item
off — a coverage claim nobody ran is not a checked item.

### Step 4 — Implement one task end-to-end, only after every gate clears

Pick one task from `tasks.md` that clears all the gates above, and implement it for
real — test first, watch it fail, then make it pass.

**Checkpoint**: `../../../brownfield-project/repos/device-opc-ua/internal/threshold/`
has exactly this: `evaluator.go` and `evaluator_test.go`, real Go, real tests (8 of
them), covering the critical-immediate path, the warning-debounce path, the
unconfigured-resource path, the invalid-reading path, and the duplicate-suppression
path — one per relevant FR. Run them:

```
cd ../../../brownfield-project/repos/device-opc-ua
go test ./internal/threshold/... -v
```

## Token & cost budgeting

Every gate above costs real tokens and real time before a single line of production
code exists. The honest case for that cost isn't abstract — it's sitting in this
feature's own artifacts: Finding 1 (checklist) and Finding 2 (analyze, this module) each
took a few minutes and a short paragraph to catch and fix *before* implementation.
Finding 1's gap, uncaught, would have shipped a Notification-flooding bug discoverable
only under sustained load — the exact shape of failure `device-opc-ua#53` (Module 2)
already showed this platform has paid for once for real. Finding 2's gap, uncaught,
would have shipped with no reviewable statement of its own auth posture, discoverable
only by an auditor or an incident, not a reviewer. Budget checklist and analyze passes
as a fixed, small cost per feature — the alternative isn't zero cost, it's the same cost
paid later, at a worse time, by someone with less context than the person who just wrote
the plan.

## Demo talk track (6–7 minutes)

1. Open `checklist.md`, scroll to Finding 1 — spec never said what happens when the same
   condition keeps recurring; show the fix, FR-015. *"Unit test suite for requirements —
   run against the spec, not the code."*

2. Open `analyze-report.md`'s F1 finding, then `plan.md` Decision 2 it caused. *"Checklist
   audits the spec against itself. Analyze audits spec, plan, and tasks against each
   other and against the constitution. Different failure classes, different gate."*

3. Open Finding 2 — the security gap, added specifically for this module. Read the note
   about the code comment that already had the right answer. *"The right answer existing
   somewhere is not the same as the right answer being reviewable before the code
   exists. That's what this whole module is actually for."*

4. Run `go test ./internal/threshold/... -cover` live, point at 94.3% next to
   `internal/driver`'s 38.4% in the same terminal. *"Not 'we wrote tests' — a number,
   next to this exact repo's own existing bar, checked the same way a reviewer would
   check it."*
