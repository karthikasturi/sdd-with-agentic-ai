# Specification Analysis Report: Equipment Health Monitoring & Maintenance Alerts

**Scope**: `spec.md`, `plan.md`, `tasks.md`, cross-checked against `.specify/memory/constitution.md`. Read-only — no files modified by this pass.

| ID | Category | Severity | Location(s) | Summary | Recommendation |
|----|----------|----------|-------------|---------|----------------|
| F1 | Inconsistency | HIGH | contracts/api.md (`GET /alerts`), spec.md SC-002 | SC-002 requires staff to identify *why* an alert fired "without consulting any source outside the alert itself." The `GET /alerts` response only includes `reading_id` — a foreign key — not the triggering reading's value. A staff member still has to look up the reading separately, which is exactly what SC-002 rules out. | Extend the `GET /alerts` response to embed the triggering reading's value (and measurement type) inline, not just its ID. Update `contracts/api.md` and task T017 accordingly before implementing. |
| C1 | Coverage Gap | MEDIUM | spec.md FR-013, tasks.md (Deferred) | FR-013 (equipment-offline alert) has no active implementation task in this pass — only a deferred placeholder (T015). Explicitly flagged, not silently dropped, but it means User Story 1 as currently scoped for implementation does not fully satisfy its own spec. | Acceptable for this lab exercise if explicitly scoped out of the current milestone (as it is); track T015 for a follow-up pass before calling FR-013 done. Do not let "deferred" quietly become "forgotten." |
| L1 | Style | LOW | tasks.md | Task ID sequence has a gap (T021 is absent) after the Module 4 amendment replaced a placeholder with T024/T025 instead of reusing the number. Harmless, but renumber on the next revision for readability. | Low priority; fix opportunistically. |

**Coverage Summary Table:**

| Requirement Key | Has Task? | Task IDs | Notes |
|---|---|---|---|
| FR-001 (register equipment) | Yes | T012 | |
| FR-002 (reject duplicate id) | Yes | T012, T008 | |
| FR-003 (record reading) | Yes | T013 | |
| FR-004 (reject unregistered equipment) | Yes | T009, T013 | |
| FR-005 (reject invalid value) | Yes | T009, T013 | |
| FR-006 (evaluate against threshold) | Yes | T014 | |
| FR-007 (critical alert, immediate) | Yes | T010, T014 | |
| FR-008 (two severities) | Yes | T014 | |
| FR-009 (list/filter alerts) | Yes | T016, T017 | See F1 — coverage exists but response shape is incomplete relative to SC-002 |
| FR-010 (acknowledge alert) | Yes | T018, T020 | |
| FR-011 (reject duplicate ack) | Yes | T018, T020 | |
| FR-012 (full status history) | Yes | T019, T020 | |
| FR-013 (equipment offline) | No (deferred) | T015 (deferred) | See C1 |
| FR-014 (warning debounce) | Yes | T011, T014 | |
| FR-015 (duplicate-alert suppression) | Yes | T024, T025 | Added post-checklist (CHK004) |
| SC-001 (critical alert <1s) | Partial | T010 | T010 confirms the alert exists; no task asserts the 1-second bound explicitly. Low-risk given synchronous evaluation (research.md), not elevated to a finding. |
| SC-002 (self-contained alert reason) | Yes (after fix) | T017 | Originally no coverage — see F1. `contracts/api.md` and T017 corrected to embed `reading_value` inline. |
| SC-003 (no silent discards) | Yes | T009, T013 | |
| SC-004 (100% alert-to-reading traceability) | Yes | T010 | |

**Constitution Alignment Issues:** None found. All five principles checked against spec/plan/tasks pass (see `plan.md` Constitution Check table); Principle I's "PASS" is asserted at the task-structure level (tests precede implementation in every phase) — actual red-before-green discipline still needs verifying during implementation, not just at task-ordering review.

**Unmapped Tasks:** T001–T003 (setup), T004–T007 (foundational), T022–T023 (polish) — expected; infrastructure/process tasks don't map to individual FRs.

**Metrics:**

- Total Functional Requirements: 15
- Total Success Criteria: 4
- Total Tasks: 24
- Requirement Coverage: 14/15 FR fully covered, 1 explicitly deferred (93% active / 100% accounted-for)
- Success Criteria Coverage: 3/4 fully covered, 1 with a real gap (F1)
- Ambiguity Count: 0 (clarify pass already resolved the two markers that existed)
- Duplication Count: 0
- Critical Issues Count: 0
- High Issues Count: 1 (F1)

## Next Actions

No CRITICAL issues — implementation is not blocked. F1 (HIGH) should be resolved before implementing T017, since fixing the response shape after the fact means revisiting both the contract and its test. Recommended order:

1. Update `contracts/api.md` and `data-model.md` read-side notes to reflect the embedded reading value (F1).
2. Proceed to `/speckit-implement` for User Story 1 (T012–T014, T024–T025) — this is the slice implemented in this lab, see Module 4 hands-on.
3. Track FR-013 (C1) for a follow-up pass; do not mark it done by omission.

Would you like remediation edits drafted for F1 before implementation? — For this lab, yes: `contracts/api.md` and `data-model.md` have already been updated to close F1 (see below), so the implemented task reflects the corrected contract, not the flawed one this report caught.
