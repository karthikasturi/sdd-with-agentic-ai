# Requirements Quality Checklist: Equipment Health Monitoring & Maintenance Alerts

**Purpose**: Validate that `spec.md` is complete, unambiguous, and consistent before implementation — a "unit test suite for requirements," run against the spec itself, not the code.
**Created**: 2026-08-05
**Feature**: [spec.md](./spec.md)

## Alert Lifecycle Coverage

- [x] CHK001 Every alert state (open, acknowledged) has a requirement governing the transition into it (FR-007, FR-010)
- [x] CHK002 Duplicate acknowledgment is explicitly rejected, not silently accepted (FR-011)
- [x] CHK003 Every alert is traceable to the specific condition that raised it (FR-007, FR-013, FR-014; SC-004)
- [x] CHK004 The spec defines what happens when the *same underlying condition* keeps recurring (e.g., equipment stays critical across many consecutive readings) — **originally FAILED, resolved via FR-015; see Finding 1 below**

## Data Integrity

- [x] CHK005 Invalid input (unregistered equipment, malformed reading) is explicitly rejected, never silently dropped (FR-004, FR-005 — constitution Principle II)
- [x] CHK006 Duplicate equipment registration is explicitly rejected, not silently overwritten (FR-002)

## Ambiguity & Testability

- [x] CHK007 No `[NEEDS CLARIFICATION]` markers remain (resolved via clarify pass, see clarify-log.md)
- [x] CHK008 Every functional requirement uses EARS phrasing (WHEN/IF... THE system SHALL...) and is independently testable
- [x] CHK009 Severity tiers (warning, critical) have distinct, non-overlapping trigger conditions (FR-007, FR-014)

## Scope Boundaries

- [x] CHK010 Out-of-scope items are explicit, not left to inference (Assumptions: no external notification integrations, single-tier permissions)
- [x] CHK011 Threshold configuration ownership (per equipment type vs. per unit) is explicit (Assumptions)

## Success Criteria

- [x] CHK012 Every success criterion is measurable and technology-agnostic (SC-001 through SC-004)
- [x] CHK013 Latency-sensitive criteria account for the severity-dependent debounce behavior established in clarify (SC-001 scoped to critical-severity only)

---

## Finding 1 (CHK004 — FAIL)

`spec.md` defines how an alert gets raised and acknowledged, but never states what happens if the underlying problem doesn't go away. As currently specified, `tasks.md` T021 flags this as a known placeholder rather than a real requirement — meaning if implementation had proceeded without this checklist pass, User Story 1's MVP slice would have shipped able to flood the alert queue from Module 6's exact scenario used to demonstrate this in `vibe-coding-exhibit/NOTES.md` (Exhibit B's unlimited-duplicate-alerts gap) — the same gap, just one stage further down the pipeline where it's more expensive to catch.

**Resolution**: Added FR-015 to `spec.md` — an equipment already carrying an open alert of a given severity does not get a second open alert of that severity from further out-of-range readings. Promoted `tasks.md` T021 from a deferred placeholder to a real implementation task (T021 → T025, Phase 3). Re-run of this checklist item after the fix: **PASS**.
