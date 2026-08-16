# Capstone Project — Requirements

Formal requirements for the closing project. `hands-on.md` in this same folder is the
participant-facing walkthrough (what to do, why less scaffolding is deliberate, the
review-trail template); this document is the deliverables/evaluation spec — what gets
produced, by when, and what "done" means.

## Description

Each team takes the spec they **set aside on Day 1** (Module 3) — rewritten in Module 8
with a few days of hindsight — through the full spec-driven lifecycle **for the first
time**: plan, tasks, checklist, analyze, implement. This is the one increment each team
builds with deliberately less scaffolding than Modules 3–6 provided for their
carried-forward increment — no pre-built reference file to checkpoint against, only
their own judgment and everything practiced across the week.

## Details

| | |
|---|---|
| **When** | Day 3, after Module 8, closing the course |
| **Starting artifact** | The team's own rewritten spec from Module 8 (the half of their assignment pair *not* carried through Modules 4–7) |
| **What's different from Modules 4–7** | No numbered checkpoints, no pre-built reference file for this specific spec — the instructor's own full lifecycle (`brownfield-project/specs/001-opcua-threshold-alerting/`) is available only as a *process* sanity check, not an answer key for this team's spec |
| **Team composition** | Same team as Days 1–2 |

## Modules used (practices this exercise draws on)

| Module | What gets reapplied |
|---|---|
| 2 — Discovery at Scale | Already done for the original pair; revisit only if the rewrite in Module 8 changed scope enough to need it |
| 3 — Governance & Clarified Spec | The spec itself is the Module 8 rewrite; no fresh clarify pass required unless the team finds a new ambiguity |
| 4 — Plan & Tasks | Generate and **review** a plan — same "correct at least one decision" bar as Module 4, applied without a template to compare against |
| 5 — Quality Gates | Checklist + analyze, both run for real, findings resolved not just noted; implement at least one task end-to-end with tests passing |
| 6 — Review & Maintain | Apply the same reviewer's-eye lens to your **own** capstone implementation that Module 6 taught on an instructor-provided exhibit |
| 7 — Multi-Agent (optional) | Delegate a sub-task if the team's capstone scope benefits from it — not required, but the pattern is available |

## Repos / areas used

Whichever of the 5 curated repos (`edgex-go`, `device-modbus-go`, `device-opc-ua`,
`edgex-ui-go`, `opc-ua-dotnet`) the team's **set-aside** spec touches — see
`../../brownfield-project/assignment-pool.md` for each pair's area. This may be a
different repo than the team's Modules 4–7 increment touched; that's expected, not a
scope violation.

## Requirements per team (deliverables)

1. **Rewritten spec + clarify-log** — already produced in Module 8; carried into the
   Capstone as the starting point, not redone.
2. **`plan.md`** — generated and reviewed by the team; at least one decision explicitly
   corrected and documented, the same standard `plan.md`'s own Plan Review Note sets
   for the instructor's reference.
3. **`tasks.md`** — decomposed from the plan, each task traceable to a requirement ID.
4. **`checklist.md` + `analyze-report.md`** — both run for real; every finding either
   resolved in the artifacts or explicitly deferred with a written reason (not silently
   dropped — same standard as `tasks.md`'s own Deferred section throughout this course).
5. **Working implementation, at least one task, end-to-end** — test written first,
   watched failing, then passing. Same bar Module 5 set: a real green test the team can
   run and show, not a claim.
6. **Documented review trail** covering **both** increments (template in
   `hands-on.md`) — specific findings and how they got fixed, referencing Modules 2–6 by
   name, not "we ran the gates."
7. **Team presentation** — the project's evolution from Day 1 through both increments;
   see `hands-on.md` for discussion points to prepare.

## Evaluation criteria

Not a pass/fail gate on any single item — evaluated as a whole, weighted toward the
review trail and presentation being *specific*, the same way this course's own Findings
1 and 2 are specific:

- **Completeness**: all 7 deliverables above present, not partially skipped.
- **Traceability**: every task maps to a requirement; every checklist/analyze finding
  has a documented resolution, not just a checked box.
- **Honesty of the review trail**: does it read like `checklist.md`'s real Finding 1/2
  (a specific gap, a specific fix) or like a generic "gates were run" summary? The
  former is the bar.
- **Judgment shown in the plan review**: is the corrected decision (requirement 2)
  substantive, or cosmetic?
- **Working code**: does the implemented task's test actually pass, live, when run?

## Submission

Share the team's repo/branch and the review-trail document with your instructor before
presenting. Presentation format and duration: confirm with your instructor — this
document doesn't fix one, since that's a scheduling detail, not a content requirement.
