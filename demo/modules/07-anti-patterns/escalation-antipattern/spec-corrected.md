# Spec — Corrected

**FR-016**: IF a critical-severity alert remains open and unacknowledged for 30 minutes, THEN THE system SHALL escalate it by transitioning it to a distinct "escalated" state, visible in the same alert listing used for triage (FR-009).

**FR-017**: Escalation SHALL happen at most once per alert — re-evaluating an already-escalated alert MUST NOT create a duplicate transition or duplicate notification.

**FR-018**: The escalation transition MUST be recorded in the alert's status history per constitution Principle V, the same as any other status change (FR-012).

**Assumptions**: Escalation only applies to critical-severity alerts for v1 — warning-severity alerts are not escalated. Paging/notification on escalation is out of scope, per this spec's existing Assumption that external notification integrations require their own spec.

## Why this is the corrected version, not just a shorter one

It states *what* (a one-time, auditable state transition, visible where staff already look) and *why* (nothing stays silently unacknowledged forever), the same way `spec-under-specified.md` should have but didn't — the 30-minute window and "critical only" scope are concrete and testable, not left for an implementer to invent. And it states nothing about *how* — no table, no scheduler, no library, no integration target — leaving that entirely to `plan.md`, which is where "background job vs. event-driven check," "APScheduler vs. cron," and "how to represent the new state without breaking the existing severity enum" actually get decided, with the tradeoffs visible and reviewable, instead of buried in prose that reads like a requirement but functions as an unreviewed architecture decision.

Notably, `spec-over-specified.md`'s central defect — the out-of-scope paging integration — doesn't even need a debate under this version: it's excluded by inheriting this feature's own existing Assumptions, the same way `spec-under-specified.md`'s implementer would have had to guess whether to add one and probably would have guessed wrong, exactly like the vibe-coding exhibit's uninvited SMTP integration (`vibe-coding-exhibit/NOTES.md`) did on Day 1. A wider spec surface doesn't need to be re-litigated feature by feature once the constitution and prior Assumptions actually get read as governing context, not boilerplate.
