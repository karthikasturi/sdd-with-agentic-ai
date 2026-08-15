# Implementation Plan: Equipment Health Monitoring & Maintenance Alerts

**Branch**: `001-equipment-health-monitoring` | **Date**: 2026-08-05 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/001-equipment-health-monitoring/spec.md`

## Summary

A FastAPI service that registers equipment, ingests sensor readings, evaluates each reading against per-equipment-type thresholds, and raises/tracks maintenance alerts through acknowledgment. Primary requirement (FR-006/FR-007/FR-014): threshold evaluation happens synchronously as part of reading ingestion, so a critical alert is retrievable within the same second the triggering reading was submitted (SC-001).

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: FastAPI, Pydantic v2, SQLAlchemy

**Storage**: SQLite (file-based), via SQLAlchemy ORM — schema kept Postgres-compatible per constitution's Technology & Architecture Constraints.

**Testing**: pytest, with FastAPI's `TestClient`

**Target Platform**: Linux server (containerized deployment out of scope for this feature; not addressed here)

**Project Type**: Single web service

**Performance Goals**: Critical-severity alert retrievable within 1 second of the triggering reading (SC-001)

**Constraints**: No silent data loss on invalid input (constitution Principle II); every alert traceable to its triggering reading (SC-004)

**Scale/Scope**: Demo/pilot scale — not designed for high-volume production ingestion in this revision

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Check | Status |
|---|---|---|
| I. Test-First | Every task in `tasks.md` writes a failing test before implementation | PASS (enforced at task level) |
| II. Explicit Data Integrity | FR-004/FR-005 reject invalid input explicitly; no bare `except` swallowing planned | PASS |
| III. Traceable Requirements | Every endpoint below maps to an FR-### | PASS |
| IV. API Contract Discipline | All request/response bodies are Pydantic models; `equipment_id` used consistently | PASS |
| V. Observability & Auditability | Alert status transitions logged via a dedicated event table (see Data Model) | PASS |

No violations requiring justification — Complexity Tracking table omitted.

## Project Structure

### Documentation (this feature)

```text
specs/001-equipment-health-monitoring/
├── spec.md
├── clarify-log.md
├── plan.md              # this file
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── api.md
└── tasks.md
```

### Source Code (repository root)

```text
app/
├── __init__.py
├── main.py           # FastAPI app, route registration
├── models.py          # SQLAlchemy models, incl. ThresholdConfig (Decision 1, revised)
├── schemas.py          # Pydantic request/response models
├── seed.py             # seeds ThresholdConfig at startup with initial values
└── routers/
    ├── equipment.py
    ├── readings.py
    └── alerts.py

tests/
├── test_equipment.py
├── test_readings.py
└── test_alerts.py
```

**Structure Decision**: Single service, no separate frontend/mobile — matches the "Single project" default option. Routers split by resource to keep each file reviewable in isolation, per constitution's Traceable Requirements principle (a reviewer can open `routers/readings.py` and check it purely against FR-003 through FR-007/FR-013/FR-014 without wading through alert-acknowledgment logic).

## Design Decisions

### Decision 1: Threshold configuration storage (REVISED — see Plan Review Note)

~~Threshold values (warning/critical per equipment type) are defined as a Python module-level constant in `app/thresholds.py`, not a database table. Rationale: fewer moving parts for the initial version, no migration needed, and thresholds are not expected to change often.~~

**Revised**: Threshold values are stored in a `ThresholdConfig` database table (equipment type, warning value, critical value), seeded at startup with the same initial values that were previously hardcoded. See Plan Review Note below for why this changed.

## Plan Review Note (Day 2, Module 3 hands-on)

The first draft of Decision 1 hardcoded thresholds in source code. On review, that decision was rejected: this is a maintenance-alerting system for physical industrial equipment — the entire premise of Story 1 (`spec.md`) is that maintenance staff, not engineers, are the ones acting on alert output. If a threshold is measured wrong or a new equipment type is added, requiring an engineer to edit `thresholds.py` and redeploy the service to change one number is a real operational bottleneck, not a hypothetical one. Storing thresholds in the database costs one small table and no runtime API in this revision (still no admin *endpoint* — that's still out of scope per `research.md`'s alternatives-considered — but the value is no longer welded to a source file, so a follow-up feature to make it staff-editable doesn't require a schema migration later).

This is the kind of decision `/speckit-plan` will happily generate without flagging, because it isn't a constitution violation — it's a scope/judgment call, and it takes a human read-through, not an automated gate, to catch it. That's the point of this exercise.

## Complexity Tracking

*No entries — no constitution violations requiring justification.*
