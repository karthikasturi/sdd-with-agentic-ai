# Module 6 — Multi-Agent Workflows & Team Adoption

Covers: coordinating multiple agents/subagents across a task graph, repository conventions linking specs to issues/PRs, and governance (reviewing agent actions, permissions, audit trails).

## Hands-on

### Step 1 — Propose and review a plan before execution

Before delegating anything, look at `../../project/specs/001-equipment-health-monitoring/tasks.md`, Phase 4 and Phase 5 (User Story 2 and 3 — alert listing and acknowledgment). Write down, in your own words, what you'd tell a second agent to build, and what you'd need to hand it so it doesn't have to guess (which files to match style against, which spec sections matter, what's explicitly out of scope).

### Step 2 — Delegate a focused sub-task

Delegate implementing User Story 2 and User Story 3 to a second agent instance. Give it the spec sections, the data model, the contract, the existing code to pattern-match, and an explicit scope boundary (don't touch spec/plan/tasks/constitution).

**Checkpoint**: `delegation-transcript.md` documents exactly this delegation, including what the delegated agent got right, what it flagged as uncertain, and — the important part — one real issue an independent reviewer found that the delegated agent did *not* self-report (a concurrency gap in the acknowledge endpoint). Compare your own delegated output against this transcript's review process, not just its code.

### Step 3 — Critique the delegated output yourself

Before reading the transcript, review your own delegated agent's code independently. Ask specifically: what happens under conditions the tests don't create (concurrent requests, unusual timing, partial failures)? That's a different question than "does this pass the tests," and it's the one this module is actually testing.

## Demo talk track (sales / technical evaluation call)

**Suggested time**: 3–4 minutes.

Open `delegation-transcript.md`. Walk through what got delegated (alert listing + acknowledgment), then the four things the delegated agent flagged as uncertain about its own work — three held up under review, one was a minor style note.

Then the actual point: scroll to "What the agent didn't flag." The delegated agent's acknowledge endpoint has a real concurrency gap — two simultaneous requests could both slip past the duplicate-acknowledgment check before either commits.

*"The delegated agent did genuinely good, disciplined work. It just answered a different question than the reviewer needed answered. Delegation changes who writes the code — it doesn't change who's responsible for asking 'what happens under conditions the tests don't create.'"*
