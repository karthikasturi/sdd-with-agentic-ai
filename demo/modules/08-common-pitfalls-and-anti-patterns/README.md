# Module 8 — Common Pitfalls & Anti-Patterns (Demo)

Covers: over-specifying vs. under-specifying; token and cost tradeoffs; case studies in
spec-driven workflows that succeeded and failed at scale.

Participant hands-on material for this module: `../../../lab/modules/08-common-pitfalls-and-anti-patterns/README.md`.
This file is the presenter-facing talk track only.

## Demo talk track (5–6 minutes)

**Live vs. pre-built**: walk the exhibit from the real files — the specific citation
against this project's own real `spec.md` is the point, not a generic
"over-specification is bad" claim a live example might not land as concretely. Every
exhibit file referenced below (by name alone from here on) lives in
`../../../lab/modules/08-common-pitfalls-and-anti-patterns/escalation-antipattern/`.

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
