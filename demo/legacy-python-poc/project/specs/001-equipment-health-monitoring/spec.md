# Feature Specification: Equipment Health Monitoring & Maintenance Alerts

**Feature Branch**: `001-equipment-health-monitoring`

**Created**: 2026-08-04

**Status**: Draft

**Input**: User description: "Build a service that ingests sensor readings from industrial equipment (temperature, vibration, runtime hours), evaluates each reading against configurable thresholds for that equipment's type, and raises a maintenance alert when a reading indicates a problem. Maintenance staff need to see open alerts, see which equipment they're for, and acknowledge them once they've been picked up. Field technicians register equipment before it starts sending readings."

## Clarifications

### Session 2026-08-04

- Q: Should prolonged silence from a piece of equipment (no readings received at all) itself be treated as a condition that raises an alert? → A: Yes — treated as an "equipment offline" warning-severity alert, raised once 60 minutes pass with no reading received from that equipment.
- Q: Should a single out-of-range reading raise an alert immediately, or does it need to persist across multiple readings first? → A: Depends on severity — a critical-level reading alerts immediately on first occurrence; a warning-level reading requires 2 consecutive out-of-range readings before an alert is raised, to filter out momentary sensor noise.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Automatic alert on an unsafe reading (Priority: P1)

A piece of registered equipment sends in a sensor reading that falls outside the safe range for its equipment type. The system evaluates the reading immediately and raises a maintenance alert without anyone having to notice the bad reading manually.

**Why this priority**: This is the entire point of the service — if a bad reading doesn't reliably produce an alert, nothing downstream matters.

**Independent Test**: Register one piece of equipment, submit a single reading known to be out of range for its type, and confirm an alert exists for that equipment immediately after.

**Acceptance Scenarios**:

1. **Given** a registered piece of equipment with a defined threshold for its type, **When** a reading arrives that exceeds that threshold, **Then** a maintenance alert is created for that equipment, referencing the triggering reading.
2. **Given** a registered piece of equipment, **When** a reading arrives within the safe range for its type, **Then** no alert is created.

---

### User Story 2 - Triage open alerts (Priority: P2)

A maintenance staff member reviews all currently open alerts, and can see, for each one, which equipment it's for and why it was raised, so they can decide what to act on first.

**Why this priority**: An alert nobody can see or make sense of has no operational value — this is what turns a raised alert into a workable queue.

**Independent Test**: With at least one open alert in the system, retrieve the list of open alerts and confirm each entry identifies its equipment and the condition that triggered it.

**Acceptance Scenarios**:

1. **Given** multiple pieces of equipment each with open alerts, **When** a maintenance staff member requests the full list of open alerts, **Then** every open alert is returned with its equipment identifier, severity, and triggering reason.
2. **Given** a specific piece of equipment, **When** a maintenance staff member requests alerts for that equipment only, **Then** only alerts belonging to that equipment are returned.

---

### User Story 3 - Acknowledge an alert (Priority: P3)

A maintenance staff member picks up an open alert and marks it acknowledged, so the rest of the team can see it's being handled and it doesn't get worked twice.

**Why this priority**: Valuable for team coordination once triage (Story 2) exists, but the service is still useful without it — alerts are just harder to coordinate on.

**Independent Test**: With one open alert in the system, acknowledge it and confirm its status changes and the change is retrievable afterward.

**Acceptance Scenarios**:

1. **Given** an open alert, **When** a maintenance staff member acknowledges it, **Then** the alert's status changes to acknowledged and records who acknowledged it and when.
2. **Given** an alert that has already been acknowledged, **When** someone attempts to acknowledge it again, **Then** the system rejects the duplicate action with a clear message rather than silently accepting it.

---

### Edge Cases

- What happens when a reading arrives for an equipment identifier that was never registered? (Rejected outright — see FR-004.)
- What happens when a reading's value is missing, non-numeric, or otherwise malformed? (Rejected outright — see FR-005.)
- What happens when a piece of equipment stops sending readings entirely? Resolved by clarification — see FR-013.
- What happens when a single reading is only momentarily out of range? Resolved by clarification — see FR-014.
- What happens when two readings for the same equipment arrive with identical or out-of-order timestamps? (Both are stored; ordering for evaluation purposes follows arrival order, not timestamp — see Assumptions.)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: WHEN a field technician submits equipment details (identifier, name, equipment type), THE system SHALL register the equipment and make it eligible to receive readings.
- **FR-002**: THE system SHALL reject registration of equipment whose identifier is already registered, rather than silently overwriting the existing record.
- **FR-003**: WHEN a sensor reading is submitted for a registered piece of equipment, THE system SHALL record the reading with the equipment it belongs to and the time it was received.
- **FR-004**: WHEN a sensor reading is submitted for an equipment identifier that is not registered, THE system SHALL reject the reading with an explicit error rather than storing it.
- **FR-005**: WHEN a submitted reading's value is missing, non-numeric, or outside the physically valid range for its measurement type, THE system SHALL reject the reading with an explicit error rather than storing or evaluating it.
- **FR-006**: WHEN a valid reading is recorded, THE system SHALL evaluate it against the threshold configuration for that equipment's type.
- **FR-007**: IF a reading's value crosses the equipment type's critical threshold, THEN THE system SHALL create a critical-severity maintenance alert immediately, referencing the equipment and the triggering reading.
- **FR-008**: THE system SHALL support at least two alert severities (warning and critical) based on how far a reading exceeds its threshold, per equipment type configuration.
- **FR-009**: THE system SHALL allow a maintenance staff member to retrieve all currently open alerts, and to filter that list to a single piece of equipment.
- **FR-010**: WHEN a maintenance staff member acknowledges an open alert, THE system SHALL change its status to acknowledged and record the acknowledging actor and timestamp.
- **FR-011**: IF an already-acknowledged alert is submitted for acknowledgment again, THEN THE system SHALL reject the action with an explicit error rather than silently accepting it.
- **FR-012**: THE system SHALL preserve every alert's full history of status changes (raised, acknowledged, and any later transitions) rather than overwriting prior state.
- **FR-013**: IF a registered piece of equipment has not had a reading recorded for 60 consecutive minutes, THEN THE system SHALL raise a warning-severity "equipment offline" alert for it.
- **FR-014**: IF a reading's value crosses the equipment type's warning threshold (but not its critical threshold), THEN THE system SHALL create a warning-severity alert only once 2 consecutive readings from that equipment have crossed the warning threshold.
- **FR-015**: IF a piece of equipment already has an open alert of a given severity, THEN THE system SHALL NOT create a second open alert of that same severity for that equipment — subsequent out-of-range readings while an alert is open are attributed to the existing alert, not used to raise a duplicate.

### Key Entities

- **Equipment**: A registered piece of industrial equipment. Identified by a unique equipment identifier; has a name and an equipment type that determines which threshold configuration applies to its readings.
- **Sensor Reading**: A single measurement submitted for a piece of equipment — a numeric value, a measurement type (e.g., temperature, vibration, runtime hours), and the time it was recorded.
- **Threshold Configuration**: Per-equipment-type boundaries that define what counts as a warning-level or critical-level reading.
- **Alert**: A maintenance alert raised for a piece of equipment because a reading crossed its threshold. Has a severity, a status (open, acknowledged, or a later resolution state), the reading that triggered it, and a full history of status changes.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A critical-severity out-of-range reading results in a retrievable alert in under 1 second of the reading being submitted.
- **SC-002**: A maintenance staff member can identify which equipment needs attention, and why, without consulting any source outside the alert itself.
- **SC-003**: No sensor reading submitted for a registered piece of equipment is ever silently discarded — every rejection is visible to the submitter as an explicit error.
- **SC-004**: The system correctly attributes 100% of alerts to the specific reading that triggered them, verifiable by an operator for any given alert.

## Assumptions

- Threshold configuration is defined per equipment type, not per individual piece of equipment, for the initial version.
- Two severities (warning, critical) are sufficient for v1; a wider severity scale is out of scope unless a later spec revision calls for it.
- Acknowledgment is tracked in-system only; paging or external notification integrations (email, SMS, on-call tooling) are explicitly out of scope for this feature and would need their own spec.
- Readings are evaluated in the order they are received, not reordered by their reported timestamp, since out-of-order delivery from field equipment is expected and re-sequencing is not required for correct alerting.
- Only field technicians register equipment and only maintenance staff triage/acknowledge alerts; finer-grained permissions between these roles are out of scope for v1.
