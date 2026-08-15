<!--
Sync Impact Report
- Version change: 1.0.0 → 1.1.0
- Modified principles: I. Test-First — added a sentence closing a gap found
  during Module 5 review (see review/module5-flawed-review.md): a test that
  only asserts a status code, not the specific behavior the requirement
  mandates, let a silent-data-tampering change reach a fully green suite.
- Added sections: none
- Removed sections: none
- Follow-up TODOs: none

Prior report (1.0.0, superseded):
- Version change: TEMPLATE → 1.0.0 (initial ratification)
- Modified principles: n/a (initial adoption)
- Added sections: Core Principles (I–V), Technology & Architecture Constraints,
  Development Workflow & Quality Gates, Governance
- Removed sections: none
- Follow-up TODOs: none
-->

# Equipment Health Monitoring Service Constitution

## Core Principles

### I. Test-First (NON-NEGOTIABLE)
Every endpoint and business rule is defined by a failing test before implementation
begins. Red-Green-Refactor is enforced: write the test from the requirement's
acceptance criteria, watch it fail, implement the minimum code to pass it, then
refactor. A task is not complete until its test suite passes and demonstrably maps
to the requirement ID it implements. Tests MUST assert the specific behavior a
requirement mandates — e.g., a rejection returns the documented error code *and*
leaves the rejected data unstored/unaltered — not merely that a response was
returned or a status code matched. A test that would still pass if the
implementation silently did the wrong thing is not sufficient coverage.

### II. Explicit Data Integrity (NON-NEGOTIABLE)
The system MUST NOT silently drop, coerce, default, or fabricate any sensor
reading, alert, or equipment record. Invalid or out-of-range input MUST be
rejected with an explicit 4xx error and a machine-readable reason. Any exception
raised while processing equipment data MUST propagate or be logged with full
context — bare `except` blocks that swallow errors are prohibited.

### III. Traceable Requirements
Every implemented endpoint, field, and business rule MUST trace to a requirement
ID in an approved spec (`specs/<feature>/spec.md`). Code that exists to satisfy a
need not captured in the spec is scope creep and MUST be rejected in review or
folded back into the spec first.

### IV. API Contract Discipline
All API boundaries MUST use Pydantic models for request and response validation —
no raw dict pass-through. Resource and field naming MUST be consistent across
endpoints (an equipment identifier is always `equipment_id`, never interchangeably
`id`/`eq_id`/`device_id`). Breaking changes to a response schema require a version
bump and a migration note in the plan.

### V. Observability & Auditability
Every alert state transition (raised, acknowledged, resolved, escalated) MUST be
recorded with actor, timestamp, and prior state — an unlogged state change did not
happen, for audit purposes. Structured logging is required for all threshold
evaluations and notification attempts, including failures; failures MUST be
visible, never silently absorbed.

## Technology & Architecture Constraints

- Backend: Python 3.11+, FastAPI for the HTTP layer, Pydantic v2 for schema
  validation.
- Persistence: SQLAlchemy ORM; SQLite for local/demo use, schema MUST remain
  Postgres-compatible for a production migration.
- No global mutable state (e.g., in-module lists) standing in for persistence once
  a feature moves past initial scaffolding.
- Dependencies are added only when a task requires them; no speculative
  libraries.

## Development Workflow & Quality Gates

- Every feature follows the full lifecycle: constitution → specify → clarify →
  plan → tasks → checklist → analyze → implement. Skipping clarify or analyze on
  a non-trivial feature requires an explicit, documented justification in the
  plan.
- Pull requests MUST reference the requirement ID(s) and task ID(s) they
  implement.
- A task is "done" only when its acceptance criteria have been demonstrated
  against a running instance, not merely when its unit tests pass in isolation.
- Checklist and analyze findings MUST be resolved, or explicitly deferred with a
  written rationale, before implementation begins on the affected task.

## Governance

This constitution supersedes ad hoc engineering preference where the two
conflict. Amendments require a documented rationale for the change and a version
bump per semantic versioning: MAJOR for backward-incompatible principle removals
or redefinitions, MINOR for new principles or materially expanded guidance, PATCH
for clarifications and wording fixes. Every `/speckit-analyze` pass MUST check
spec, plan, and tasks for compliance with these principles and report violations
as findings, not warnings to be silently accepted.

**Version**: 1.1.0 | **Ratified**: 2026-08-04 | **Last Amended**: 2026-08-05
