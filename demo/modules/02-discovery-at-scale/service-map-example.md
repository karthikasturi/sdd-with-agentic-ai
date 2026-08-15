# Service / Dependency Map — Instructor Example (Pair 1: OPC UA Threshold Alerting)

Filled from real findings already on record in `../../../brownfield-project/discovery-log.md`
— not a new research pass, this is what that document's findings look like repackaged
into the one-page shape each team produces.

## Services in scope

| Service | What it owns / is responsible for | Real dependencies (calls, or is called by) | Doc quality |
|---|---|---|---|
| `device-opc-ua` | Subscribes to OPC UA nodes, publishes readings as EdgeX events | Needs an OPC UA server (documented: Prosys — but see defect below); publishes into EdgeX's event pipeline | Well documented for setup (README), no package-level doc comments in `internal/` (poor) |
| `support-notifications` | Stores/serves Notifications; acknowledge, category/label/status query | Called by any service that wants to raise an alert; called by dashboard for triage | Well documented (official docs + full OpenAPI spec) |
| `edgex-ui-go` (`NotificationListComponent`) | Dashboard triage UI for Notifications | Calls `support-notifications`' REST API directly | Misleading if read incompletely — real list logic is one directory away from the obvious-looking empty component (poor from the outside, fine once found) |

## Data this area owns

`support-notifications` is the system of record for Notifications — category, severity,
content, labels, acknowledged status. Nothing else should invent a parallel alert store.

## Pulled-in defect

- **Issue**: [`device-opc-ua#53`](https://github.com/edgexfoundry/device-opc-ua/issues/53) — OOM after ~11h of sustained collection.
- **Real root cause**: retention policy configured but not actually deleting records — "Prepare to delete 0 readings" in the logs despite millions of stored keys.
- **Which service actually needs to change**: likely `core-data`'s retention mechanism, not `device-opc-ua` itself — the defect is filed where the symptom was observed, not necessarily where the cause lives. See `../../../brownfield-project/specs/defect-001-device-opc-ua-oom/spec.md`.

## Open questions carried forward to Module 3

- Does `support-notifications`'s acknowledge endpoint reject a duplicate acknowledgment? (No — confirmed by reading source + OpenAPI spec, not documented anywhere. Becomes a real constitution/spec decision, not a surprise found during implementation.)
- Extend `device-opc-ua` directly for threshold evaluation, or add a new subscriber service? (Real brownfield-specific question with no greenfield equivalent — resolved in `clarify-log.md` Question 3.)
