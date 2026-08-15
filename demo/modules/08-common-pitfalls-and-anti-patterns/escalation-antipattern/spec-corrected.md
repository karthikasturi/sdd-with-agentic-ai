# Feature Specification: Alert Escalation (Corrected)

## Requirements

- **FR-016**: IF a CRITICAL-severity Notification remains unacknowledged for 30
  minutes, THEN THE system SHALL set its `status` to `ESCALATED` — an existing value in
  `support-notifications`' own `Notification.status` enum (`NEW`/`PROCESSED`/`ESCALATED`,
  confirmed in `repos/edgex-go/openapi/support-notifications.yaml`), not a new field or
  a new table.
- **FR-017**: A Notification SHALL escalate at most once — a second 30-minute window
  passing on an already-escalated Notification SHALL NOT re-trigger the transition or
  send a duplicate notification.
- **FR-018**: Every escalation SHALL be recorded as a status-transition event, consistent
  with constitution Principle VI (Observability & Auditability) — same mechanism already
  used for the raised→acknowledged transition, not a separate audit path.

## Assumptions

- CRITICAL-only for v1, matching the severity scope this feature already established.
- No paging or external notification integration — this repeats
  `../../../../brownfield-project/specs/001-opcua-threshold-alerting/spec.md`'s existing
  Assumptions section verbatim on purpose (note the extra `../` — this file is nested one
  level deeper, inside `escalation-antipattern/`, than the module READMEs that use
  `../../../`): *"Paging/external notification channels (email, SMS, on-call tooling) are
  out of scope — `support-notifications`'s existing `Subscription`/channel mechanism
  already covers that concern if/when it's needed, and is not modified by this
  feature."* Escalation changes a Notification's status; it does not, by itself, page
  anyone — wiring `ESCALATED` notifications to an actual subscription/channel is a
  separate, later feature, deliberately.

## Why this is the corrected version

States trigger (30 min unacknowledged CRITICAL), effect (existing `ESCALATED` status,
existing audit mechanism), and boundary (at-most-once, no paging) — and stops there.
*How* it gets scheduled, what package runs the check, which file the code lives in —
all plan-stage decisions, left to `plan.md`, not decided here.
