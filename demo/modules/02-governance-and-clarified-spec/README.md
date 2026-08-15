# Module 2 — Establishing Governance and Writing a Clarified Specification

Covers: the constitution as project governance, EARS-style requirement structuring, and the clarify pass.

All checkpoints below reference `../../project/` — the finished, real answer key.

## Hands-on

### Step 1 — Write a constitution

In your own Spec Kit project (continuing from Module 1, not this repo), write a constitution encoding engineering standards for your codebase: testing requirements, data-integrity rules (what happens instead of silently dropping bad input), API consistency rules, and anything else you consider non-negotiable. Use your tool's constitution skill/command if it has one (e.g. `/speckit-constitution`) rather than hand-editing the template.

**Checkpoint**: Compare against `../../project/.specify/memory/constitution.md`. You don't need to match it — check whether you covered data integrity (what happens on bad input) and naming/contract consistency. If you didn't, ask why not: what would it have taken to think of that requirement one hour into the project versus one week in, after the bug shipped?

### Step 2 — Draft a spec for the equipment monitoring feature

Feature description to use: *"Build a service that ingests sensor readings from industrial equipment (temperature, vibration, runtime hours), evaluates each reading against configurable thresholds for that equipment's type, and raises a maintenance alert when a reading indicates a problem. Maintenance staff need to see open alerts, see which equipment they're for, and acknowledge them once they've been picked up. Field technicians register equipment before it starts sending readings."*

Run your spec-drafting step against that description (e.g. `/speckit-specify`).

**Checkpoint**: Compare structure (not content) against `../../project/specs/001-equipment-health-monitoring/spec.md` — same section headings, EARS-style requirements ("WHEN... THE system SHALL...")?

### Step 3 — Run a clarify pass, then a peer review

Run your clarify step (e.g. `/speckit-clarify`) against your own spec and answer honestly, based on your own judgment.

Then **swap specs with a partner**. Spend 5 minutes reading each other's spec cold and note anything ambiguous, untestable, or missing — without looking at what your own clarify pass caught.

**Checkpoint / discussion**:
- What did the automated clarify pass catch that you didn't think to specify yourself?
- What did your partner catch that clarify *didn't* ask about?
- Compare both against `../../project/specs/001-equipment-health-monitoring/spec.md`'s `## Clarifications` section — it resolves two specific ambiguities (equipment going silent, and single-reading vs. consecutive-reading alerting). Did either of you land on the same questions?

This exercise shows clarify and human peer review catch *different* things — neither replaces the other. Module 5 comes back to this from the other direction.

## Demo talk track (sales / technical evaluation call)

**Suggested time**: 5–6 minutes.

1. Open `../../project/.specify/memory/constitution.md`. Point at Principle II (Explicit Data Integrity — "MUST NOT silently drop, coerce, default, or fabricate") and Principle IV (API Contract Discipline — consistent field naming). *"Go back to the vibe-coded output from Module 1 — the dead ack endpoint, the swallowed SMTP exception. Every one of those violates a principle written down right here, before a single line of feature code exists."*
2. Open `../../project/specs/001-equipment-health-monitoring/spec.md`, scroll to Functional Requirements. Read FR-004/FR-005 aloud. *"Compare that to the vibe-coded version, which stored anything sent to it with zero validation. This is what 'testable and unambiguous' looks like on paper."*
3. Scroll to the `## Clarifications` section — walk through both Q&A pairs, then flip to FR-007/FR-013/FR-014 and show exactly where each answer landed in the requirements. *"Neither question is exotic. A competent engineer hits both eventually — usually in code review, after something's already built the wrong way once. Clarify catches them for the price of two short answers, before implementation exists."*
