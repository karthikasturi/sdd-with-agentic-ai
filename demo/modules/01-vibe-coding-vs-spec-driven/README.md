# Module 1 — From Vibe Coding to Spec-Driven Development

Covers: failure modes of ad hoc AI prompting, SDD principles, the full SDD lifecycle as
a map for the rest of the course, and what makes an AI system "agentic."

`../../../brownfield-project/` is the real reference implementation for the whole
course — EdgeX Foundry (Go) + edgex-ui-go (Angular) + OPC UA .NET Standard (C#), a
curated slice of a real, currently-maintained open-source industrial-IoT platform, not a
synthetic codebase. This module doesn't touch it directly — everything hands-on here is
self-contained in `vibe-coding-exhibit/` — but Step 1 below checks your own scratch
scaffold against its real `.specify/`/`.claude/` structure.

## Hands-on

### Step 1 — Install and scaffold

Confirm your agentic coding tool is installed and working. Then, in your own scratch
working directory (**not** this repo):

```
mkdir my-scratch-project && cd my-scratch-project
uvx --from git+https://github.com/github/spec-kit.git specify init --here --integration claude
```

(Swap `--integration claude` for your tool — this is the real GitHub Spec Kit CLI,
the same one `../../../brownfield-project/` was scaffolded with.)

**Checkpoint**: you should have a `.specify/` directory (memory/, templates/, scripts/,
workflows/) and your agent's command/skill integration (e.g. `.claude/skills/speckit-*`).
Compare *structure*, not content, against `../../../brownfield-project/.specify/` and
`../../../brownfield-project/.claude/` — that scaffold is real, produced by running this
exact command, not hand-written to look right.

### Step 2 — Compare a basic prompt against a better one

In a second scratch directory (still empty, still no spec, no constitution), feed your
agent `vibe-coding-exhibit/PROMPT.md` cold. Then, in a third empty directory, feed it
`vibe-coding-exhibit/PROMPT-ADVANCED.md`.

**Checkpoint**: compare your two outputs against `vibe-coding-exhibit/output/` and
`output-advanced/`. Both exhibits are real, unedited agent output, and both genuinely
build and run — try them:

```
cd vibe-coding-exhibit/output && go build -o /tmp/exhibit-a . && /tmp/exhibit-a
# in another terminal:
curl -X POST localhost:8080/equipment -d '{"id":"eq-1","name":"Compressor A"}'
curl -X POST localhost:8080/readings -d '{"equipmentId":"eq-1","value":150}'
curl -X POST localhost:8080/alerts/ack?id=1
curl localhost:8080/alerts   # look closely at "acknowledged" — see NOTES.md
```

Your second (more careful) prompt's output should be meaningfully better than your
first — real per-type validation, working idempotent acknowledgment. Then look for what's
**still** missing, even in the better one: read `NOTES.md` for the full breakdown,
including one gap a better prompt can fix and one it structurally can't. That second gap
is the one worth sitting with before Module 2.

## Demo talk track (5–6 minutes)

**Live vs. pre-built**: Steps 1 and 3 below are safe to run genuinely live if you want
the credibility of "watch me do it right now" — low stakes, low variance, a few minutes
each. Steps 2 and 4 depend on specific output (the exact silent bug, the exact remaining
gap) — walk through the pre-built exhibit for those instead of re-running the prompts
live; an LLM re-run is not guaranteed to reproduce the same mistake twice, and the point
of this module is those *specific* mistakes, not "a" mistake.

1. Open `PROMPT.md`, then `output/main.go` side by side — "the entire input was three
   sentences. No spec. No constitution. Empty directory." Point at `const threshold =
   100.0` — one number, every reading, every equipment type, no exceptions. Then scroll
   to `acknowledgeAlert`'s `for _, alert := range alerts` loop. "This compiles. It
   returns 200. It runs. It never acknowledges a single alert" — run the live curl
   sequence from NOTES.md and show the field staying `false`. "A smoke test that only
   checks the status code passes this every time."

2. Open `NOTES.md`, name the four failure modes on screen: **context drift, hallucinated
   understanding, silent scope creep, unreviewable diffs** — this is the vocabulary for
   the rest of the course.

3. Open `PROMPT-ADVANCED.md` next to `output-advanced/main.go` — real, working, better
   code: per-type thresholds, a 404 on unregistered equipment, an idempotent-*rejecting*
   acknowledge endpoint this time. Then run three consecutive critical readings live and
   show three separate alerts instead of one. Quote: *"A better prompt closes the obvious
   gaps. It takes a dedicated process to close the ones that only surface once you ask
   'what happens when this keeps happening?'"* — that's Module 3.

4. Then the second gap: "neither prompt knew this codebase already has a real
   notification service sitting right next to where this code would actually live.
   No amount of prompt detail fixes that — the agent was never pointed at it." That's
   Module 2, not Module 3: *orienting* an agent in a large existing codebase is a
   different problem from *specifying* a feature clearly, and this course treats them as
   two separate stages for exactly that reason.

5. Open `../../../brownfield-project/.claude/skills/` and show the installed Spec Kit
   skills: `speckit-constitution`, `speckit-specify`, `speckit-clarify`, `speckit-plan`,
   `speckit-tasks`, `speckit-checklist`, `speckit-analyze`, `speckit-implement` —
   "this *is* the lifecycle, installed as real, runnable tooling, against a real
   codebase." Then open `../../../brownfield-project/README.md` and point at the scale:
   EdgeX Foundry alone ships 17 deployable services in one repo, before counting the
   other three. "Everything from here forward is the same domain, going through that
   lifecycle instead — at a scale a hand-picked toy example never could have shown you."
