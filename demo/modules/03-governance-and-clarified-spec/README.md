# Module 3 — Establishing Governance and Writing a Clarified Specification (Demo)

Covers: encoding project/per-service principles as a constitution, informed by
discovery; writing EARS-style requirements from both a feature request and a real
defect; the clarify pass; and where this fits inside a team's existing SDLC.

Participant hands-on material for this module: `../../../lab/modules/03-governance-and-clarified-spec/README.md`.
This file is the presenter-facing talk track only.

## Demo talk track (6–7 minutes)

**Live vs. pre-built**: Step 1 is reasonable live if you have a volunteer team's real
service map in hand. Steps 2–3 should walk from the two real checkpoint specs — the
specific ambiguities each spec's `clarify-log.md` (in
`../../../brownfield-project/specs/001-opcua-threshold-alerting/` and
`.../specs/defect-001-device-opc-ua-oom/`) records are the point, and a live clarify
pass might not surface the same ones.

1. Open `../../../brownfield-project/.specify/memory/constitution.md`, point at
   Principle IV specifically — *"extend `support-notifications`, don't invent a
   parallel alert store"* — and tie it back to Module 1's Exhibit B, which did exactly
   the thing this principle forbids, because nothing in that exercise's prompt pointed
   at what already existed.

2. Open `../../../brownfield-project/specs/001-opcua-threshold-alerting/spec.md`'s
   Clarifications section, walk all three questions, then open
   `../../../brownfield-project/specs/defect-001-device-opc-ua-oom/spec.md`'s "Why this
   is filed against `device-opc-ua` but likely fixed elsewhere" note. Quote: *"A feature
   spec asks what should exist. A defect spec asks what's actually true right now,
   which is a different and often harder question — the report tells you where the
   pain was felt, not where the fix lives."*

3. Close on the SDLC-mapping paragraph at the top of the hands-on guide. *"Nothing
   you're doing this week replaces your existing process. Requirements and design
   didn't go away — they're the constitution and the spec, now something an agent can
   be checked against instead of a document nobody reopens after kickoff."*
