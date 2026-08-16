# Module 4 — From Clarified Spec to Reviewable Plan (Demo)

Covers: translating a clarified, constitution-aligned spec into a technical plan,
reviewed before any file changes happen; then decomposing it into small, independently
verifiable tasks.

Participant hands-on material for this module: `../../../lab/modules/04-from-clarified-spec-to-reviewable-plan/README.md`.
This file is the presenter-facing talk track only.

## Demo talk track (4–5 minutes)

**Live vs. pre-built**: Step 1 (generating a plan) is fine live if you have a real spec
in hand — any reasonable plan output makes the point. Step 2's specific correction
should walk from the real `plan.md` — the value is in *this* correction and *why* it's
brownfield-shaped, not in "a" correction a live run might or might not surface.

1. Open `../../../brownfield-project/specs/001-opcua-threshold-alerting/plan.md`'s
   Design Decisions section, show the struck-through original
   ("~~Threshold values ... defined as a Go map literal~~"), then the revised version
   right below it. *"`/speckit-plan` will happily generate a plan that hardcodes a value
   in source without flagging it — that's not a constitution violation, it's a
   judgment call. Catching it takes a person reading the plan and asking who has to act
   on this later."*

2. Open the Plan Review Note itself, read the closing paragraph aloud: the correction
   reused an existing mechanism instead of adding a new one — tie back to constitution
   Principle IV and Module 2's discovery work. *"This is what Module 2 buys you later:
   you can't reuse a mechanism you didn't know existed."*

3. Open `../../../brownfield-project/specs/001-opcua-threshold-alerting/tasks.md`'s
   Deferred section. *"One real requirement, explicitly not built, explicitly written
   down why. Compare that to a task that just quietly never got created — from a task
   list alone, you can't always tell the difference. This can."*

4. Close on Step 4 — live if your Atlassian MCP connection is up: ask the agent to
   create one real Jira sub-task from `tasks.md`, then open the story in a browser to
   show it landed. *"Everything so far lived in files in your repo. The tracker your
   team actually works from doesn't know any of it happened until something writes it
   back — this is that write, and we check it the same way we'd check any agent claim:
   not by trusting the summary, by opening the ticket."*
