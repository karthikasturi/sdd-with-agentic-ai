# Module 7 — Multi-Agent Workflows & Team Adoption

Covers: coordinating multiple agents/subagents across a task graph and when to
parallelize vs. sequence work; repository conventions — a `specs/` subdirectory per
service, linking specs to issues and pull requests; and governance — reviewing agent
actions before execution, managing secrets and permissions, keeping an audit trail
across teams and toolchains.

`../../../brownfield-project/delegation-transcript.md` is a real delegation, not staged:
User Story 1 (Go) was built in one work session; User Story 3 (Angular) was handed to a
second, independent pass with a defined scope boundary, then reviewed independently —
5/5 real tests, verified via `ng test` in an actual headless browser, not assumed.

## Hands-on

### Step 1 — Propose and review a plan before delegating anything

Before delegating, look at your own carried-forward `tasks.md`. Pick the next
multi-step increment — the part of your feature you haven't built yet. Write down, in
your own words, what you'd tell a second agent to build, and what it needs so it
doesn't have to guess: which files to pattern-match style against, which spec sections
matter, what's explicitly out of scope.

**Checkpoint**: compare your scoping note against `delegation-transcript.md`'s "What
was delegated" section — notice it names four specific things (spec sections, contract,
plan reasoning, existing code to match) *and* an explicit negative scope boundary
("do not touch..."). A delegation brief with only the first half tends to produce work
that's individually fine and collectively inconsistent with everything around it.

### Step 2 — Delegate a focused sub-task

Delegate that increment to a second agent instance (a fresh session/context, not a
continuation of the one that did your earlier work). Give it exactly what Step 1
produced.

**Checkpoint**: no fixed answer here — this is your own project's next increment. But
notice, once it comes back, whether you can independently verify its claims the way
`delegation-transcript.md` does (real `go test`/`ng test` output, not "should work").
If you can't independently verify a delegated agent's own summary, that's worth noticing
before you accept it, not after.

### Step 3 — Critique the delegated output yourself, before reading any answer key

Before comparing notes with anyone, review your delegated agent's output independently.
Ask what happens under conditions your tests don't create — concurrent access, unusual
timing, partial failures — a different question than "do the tests pass."

**Checkpoint**: compare against `delegation-transcript.md`'s "What the delegate didn't
flag" section — a real TOCTOU race in the acknowledge flow, whose reasoning already
existed as a code comment but was never surfaced as an open risk in the delegate's own
summary. Same shape as checklist Finding 2 (Module 5): the right answer existing
somewhere is not the same as it being reviewable without someone specifically going and
finding it.

See `../../../demo/modules/07-multi-agent-workflows-and-team-adoption/README.md` for
this module's presenter/demo talk track — not needed to complete the hands-on above.
