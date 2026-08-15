# Tasks: Equipment Health Monitoring & Maintenance Alerts

**Input**: Design documents from `specs/001-equipment-health-monitoring/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/api.md

**Tests**: Included — constitution Principle I (Test-First, NON-NEGOTIABLE) requires a failing test before every implementation task.

## Format: `[ID] [P?] [Story] Description (FR-###)`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to

## Phase 1: Setup

- [ ] T001 Create project structure per plan.md (`app/`, `tests/`)
- [ ] T002 Initialize FastAPI + SQLAlchemy + pytest dependencies in `requirements.txt`
- [ ] T003 [P] Configure pytest (`pytest.ini` or `pyproject.toml` test config)

## Phase 2: Foundational (Blocking Prerequisites)

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [ ] T004 Create SQLAlchemy engine/session setup in `app/db.py`
- [ ] T005 Create `Equipment`, `Reading`, `Alert`, `AlertEvent`, `ThresholdConfig` models in `app/models.py` (data-model.md)
- [ ] T006 Seed `ThresholdConfig` at startup in `app/seed.py` (plan.md Decision 1, revised)
- [ ] T007 Wire FastAPI app + router registration in `app/main.py`

**Checkpoint**: Foundation ready — user story implementation can begin.

## Phase 3: User Story 1 - Automatic alert on an unsafe reading (Priority: P1) 🎯 MVP

**Goal**: A registered equipment's out-of-range reading reliably produces a maintenance alert without manual intervention.

**Independent Test**: Register one equipment, submit a reading known to be out of range, confirm an alert exists.

### Tests for User Story 1 (write first, confirm failing)

- [ ] T008 [P] [US1] Contract test `POST /equipment` — success + duplicate-id rejection in `tests/test_equipment.py` (FR-001, FR-002)
- [ ] T009 [P] [US1] Contract test `POST /readings` — unregistered equipment (404) + invalid value (422) in `tests/test_readings.py` (FR-004, FR-005)
- [ ] T010 [P] [US1] Integration test: critical reading raises alert immediately, referencing the triggering reading in `tests/test_readings.py` (FR-007, SC-001, SC-004)
- [ ] T011 [P] [US1] Integration test: warning reading requires 2 consecutive readings before alerting in `tests/test_readings.py` (FR-014)

### Implementation for User Story 1

- [ ] T012 [US1] Implement `POST /equipment` in `app/routers/equipment.py` (FR-001, FR-002)
- [ ] T013 [US1] Implement `POST /readings` ingestion + input validation in `app/routers/readings.py` (FR-003, FR-004, FR-005)
- [ ] T014 [US1] Implement threshold evaluation (critical immediate, warning debounced) in `app/routers/readings.py` (FR-006, FR-007, FR-008, FR-014) — depends on T012, T013

**Checkpoint**: User Story 1 functional and independently testable.

> **Lab scope note**: T015 (equipment-offline detection, FR-013) and its test are listed in the Deferred section below, not implemented in this exercise — a background/scheduled check is a different implementation shape than the request-driven tasks above, and isn't necessary to demonstrate the checklist/analyze/implement loop. Flagged here rather than silently dropped, per constitution Principle III (Traceable Requirements).

## Phase 4: User Story 2 - Triage open alerts (Priority: P2)

**Goal**: Maintenance staff can see all open alerts, or filter to one equipment.

**Independent Test**: With an open alert present, retrieve the alert list and confirm equipment/severity/reason are visible.

### Tests for User Story 2

- [ ] T016 [P] [US2] Contract test `GET /alerts`, all and filtered by `equipment_id` in `tests/test_alerts.py` (FR-009)

### Implementation for User Story 2

- [ ] T017 [US2] Implement `GET /alerts` in `app/routers/alerts.py`, response embeds the triggering reading's value inline, not just `reading_id` (FR-009, SC-002 — corrected per analyze-report.md finding F1)

**Checkpoint**: User Stories 1 and 2 both work independently.

## Phase 5: User Story 3 - Acknowledge an alert (Priority: P3)

**Goal**: Maintenance staff can acknowledge an open alert exactly once, with the action recorded.

**Independent Test**: With one open alert, acknowledge it, confirm status change and that a repeat acknowledgment is rejected.

### Tests for User Story 3

- [ ] T018 [P] [US3] Contract test `POST /alerts/{id}/ack` — success + duplicate-ack rejection (409) in `tests/test_alerts.py` (FR-010, FR-011)
- [ ] T019 [P] [US3] Integration test: acknowledgment is recorded in `AlertEvent` history, not just as a status overwrite in `tests/test_alerts.py` (FR-012)

### Implementation for User Story 3

- [ ] T020 [US3] Implement `POST /alerts/{id}/ack` + `AlertEvent` logging in `app/routers/alerts.py` (FR-010, FR-011, FR-012)

**Checkpoint**: All in-scope user stories independently functional.

## Deferred (out of scope for this lab pass)

- [ ] T015 [US1] Equipment-offline detection (FR-013) — requires a scheduled/background check, not just request-time logic; deferred beyond this exercise's scope.

## Phase 3 addendum — added after Module 4 checklist (CHK004 finding)

- [ ] T024 [P] [US1] Integration test: a second critical reading while an alert is already open does not create a duplicate open alert in `tests/test_readings.py` (FR-015)
- [ ] T025 [US1] Implement duplicate-alert suppression in the threshold evaluation path in `app/routers/readings.py` (FR-015) — depends on T014

## Phase 6: Polish & Cross-Cutting

- [ ] T022 [P] Run `quickstart.md` validation end-to-end
- [ ] T023 Review implemented code against constitution Principles I–V before calling any task done

## Dependencies

- Setup (Phase 1) → Foundational (Phase 2) → User Stories (Phase 3+, in priority order for this lab)
- Within User Story 1: tests (T008–T011) before implementation (T012–T014); T014 depends on T012 and T013 both existing
- User Stories 2 and 3 depend on Foundational only, not on each other
