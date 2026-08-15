# API Contract: Equipment Health Monitoring & Maintenance Alerts

## `POST /equipment`
Registers a piece of equipment. FR-001, FR-002.

- Request: `{ "id": string, "name": string, "type": string }`
- 201: echoes the registered equipment
- 409: `id` already registered
- 422: unknown `type` (no threshold configuration for it)

## `POST /readings`
Submits a sensor reading and triggers threshold evaluation. FR-003 through FR-007, FR-014.

- Request: `{ "equipment_id": string, "value": number }`
- 201: `{ "reading_id": integer, "alert_raised": "warning" | "critical" | null }`
- 404: `equipment_id` not registered (FR-004)
- 422: `value` missing/non-numeric (FR-005)

## `GET /alerts`
Lists open alerts, optionally filtered by equipment. FR-009, SC-002.

- Query param: `equipment_id` (optional)
- 200: list of `{ id, equipment_id, severity, status, reading_id, reading_value }` — `reading_value` is embedded inline (not just the foreign key) so a staff member can see *why* the alert fired without a second lookup, per SC-002. Corrected here after `analyze-report.md` finding F1; the original draft only returned `reading_id`.

## `POST /alerts/{alert_id}/ack`
Acknowledges an open alert. FR-010, FR-011.

- Request: `{ "acknowledged_by": string }`
- 200: `{ "status": "acknowledged" }`
- 404: alert not found
- 409: alert already acknowledged
