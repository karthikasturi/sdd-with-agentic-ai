# Phase 0 Research: Equipment Health Monitoring & Maintenance Alerts

## Threshold storage

- **Decision** (revised during plan review — see `plan.md` Plan Review Note): Store per-equipment-type thresholds in a `ThresholdConfig` database table, seeded at startup.
- **Rationale**: The original draft used a Python module constant for simplicity. Plan review rejected that: this system exists so maintenance staff — not engineers — can act on alerts, and welding threshold values to a source file means any correction requires an engineer and a redeploy. A table costs one migration and removes that dependency, without yet building a full admin API (still deferred — see alternatives below).
- **Alternatives considered**: Python module constant (original draft — rejected, operational bottleneck); full admin endpoint for runtime editing (deferred — no requirement in `spec.md` calls for it yet; the table alone is enough to unblock a future feature without a later schema migration).

## Synchronous vs. asynchronous threshold evaluation

- **Decision**: Evaluate thresholds synchronously, inside the `POST /readings` request, before responding.
- **Rationale**: SC-001 requires a critical alert to be retrievable within 1 second of the triggering reading. A background job (queue + worker) adds latency and infrastructure for no benefit at this scale.
- **Alternatives considered**: Async queue-based evaluation — rejected as unnecessary complexity for the demo/pilot scale in Technical Context.

## Persistence

- **Decision**: SQLite via SQLAlchemy, single file.
- **Rationale**: Constitution mandates SQLAlchemy + Postgres-compatible schema; SQLite is the lightest option that satisfies both for a demo/pilot deployment.
- **Alternatives considered**: In-memory store — explicitly prohibited by constitution's Technology & Architecture Constraints once a feature moves past initial scaffolding.

## Alert history / auditability

- **Decision**: A dedicated `alert_events` table records every status transition (from_status, to_status, actor, timestamp), rather than only tracking current status on the `alerts` row.
- **Rationale**: Constitution Principle V requires every alert state transition to be recorded with actor, timestamp, and prior state. A single mutable `status` column would satisfy FR-010 but not the audit trail Principle V requires.
- **Alternatives considered**: Status field only, no event log — rejected, fails constitution compliance.
