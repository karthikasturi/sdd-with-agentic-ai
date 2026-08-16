# Comparison: Same Feature, Two Wrong Directions

Both `output-from-under-specified.go` and `output-from-over-specified.go` build clean —
verified with `go build`, not assumed. Both are real problems anyway.

## Under-specified

- `REASONABLE_TIME = 15 * time.Minute` — arbitrary. The spec said "a reasonable time";
  the agent picked a number nobody could object to, because nobody gave it anything to
  compare against.
- Applies to *every* severity, not just CRITICAL — the spec said "alerts," not "critical
  alerts," so nothing narrowed the scope.
- Destructively overwrites `Severity`, never touches `Status` — the platform's own
  Notification schema already has an `ESCALATED` status value for exactly this. Nothing
  in the spec told the agent it existed, so it invented a different mechanism instead
  of using the one already there — the same root failure `spec.md`'s User Story 2
  correction (Module 3) documents for this project's own history, one level up.
- No idempotency guard — fires again every time the check runs, for as long as the
  alert stays unacknowledged. Same shape as checklist Finding 1 (Module 5), the
  duplicate-flooding gap, recurring because nothing here says otherwise.

## Over-specified

- Bypasses the existing `status: ESCALATED` value entirely in favor of a new
  `escalationState` table — violates constitution Principle IV (Convention
  Conformance) directly: a parallel mechanism next to one that already exists.
- Introduces `github.com/robfig/cron/v3` — a real, resolvable dependency, confirmed via
  `go mod tidy`, but never vetted or justified in any `research.md`, because the "spec"
  skipped straight past the point where that justification would live.
- Makes an unconditional external POST to a paging endpoint — directly contradicting
  this project's own real `spec.md`, which already states: *"Paging/external
  notification channels (email, SMS, on-call tooling) are out of scope —
  `support-notifications`'s existing `Subscription`/channel mechanism already covers
  that concern if/when it's needed, and is not modified by this feature."* Not a
  hypothetical scope violation — a citation against a real, already-written file.

## Corrected

`spec-corrected.md` states trigger, effect, and boundary, then stops. The effect it
names — `status: ESCALATED` — is the value that was already sitting in the schema the
whole time; the corrected version's only real insight is *reading the schema before
writing the requirement*, not writing a cleverer requirement.

## Takeaway

Neither failure direction is "more detail is safer" or "less detail is safer" in the
abstract. Under-specification let an implementer's first guess silently become the
requirement, three separate times, in three different ways. Over-specification smuggled
an architecture decision and a scope violation past review inside a document that's
supposed to be reviewable by someone who isn't reading Go signatures. Both directions
produced code that builds, runs, and would pass a shallow read — same shape of risk this
whole course has been pointing at since Module 1's first exhibit, now with a spec that
had already been through clarify once, in Module 3, for the *other* half of this
project's own real work.
