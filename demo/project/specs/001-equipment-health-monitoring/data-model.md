# Phase 1 Data Model: Equipment Health Monitoring & Maintenance Alerts

## Equipment
Maps to spec Key Entity "Equipment".

| Field | Type | Notes |
|---|---|---|
| `id` | string, PK | Equipment identifier, technician-supplied (FR-001) |
| `name` | string | |
| `type` | string | Must be a known type with a threshold entry (FR-001, FR-006) |
| `created_at` | datetime | |

Uniqueness: `id` is the primary key; registering an existing `id` is rejected (FR-002).

## Reading
Maps to spec Key Entity "Sensor Reading".

| Field | Type | Notes |
|---|---|---|
| `id` | integer, PK, autoincrement | |
| `equipment_id` | string, FK → Equipment.id | Rejected if not registered (FR-004) |
| `value` | float | Rejected if missing/non-numeric (FR-005) |
| `recorded_at` | datetime | Server-assigned on receipt |

## Alert
Maps to spec Key Entity "Alert".

| Field | Type | Notes |
|---|---|---|
| `id` | integer, PK, autoincrement | |
| `equipment_id` | string, FK → Equipment.id | |
| `reading_id` | integer, FK → Reading.id, nullable | Null for equipment-offline alerts (FR-013), which aren't triggered by a specific reading |
| `severity` | string enum: `warning`, `critical` | FR-008 |
| `status` | string enum: `open`, `acknowledged` | FR-010 |
| `created_at` | datetime | |

State transitions: `open` → `acknowledged` (FR-010). Re-acknowledging an already-acknowledged alert is rejected (FR-011). Every transition is additionally recorded in `AlertEvent` (below) — the `status` field here is a convenience cache of the most recent event, not the system of record.

## AlertEvent
Not a spec Key Entity by name, but required to satisfy constitution Principle V (Observability & Auditability) and FR-012 (full history of status changes).

| Field | Type | Notes |
|---|---|---|
| `id` | integer, PK, autoincrement | |
| `alert_id` | integer, FK → Alert.id | |
| `from_status` | string, nullable | Null for the initial "raised" event |
| `to_status` | string | e.g. `open`, `acknowledged` |
| `actor` | string, nullable | Acknowledging staff member; null for system-raised events |
| `at` | datetime | |

## ThresholdConfig
Maps to spec Key Entity "Threshold Configuration". Per the revised Decision 1 in `plan.md`, this is a database table, seeded at startup — see `research.md`.

| Field | Type | Notes |
|---|---|---|
| `equipment_type` | string, PK | e.g. `compressor`, `pump`, `conveyor` |
| `warning` | float | |
| `critical` | float | |
