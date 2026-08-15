# Module 1 — From Vibe Coding to Spec-Driven Development

Covers: failure modes of ad hoc AI prompting, SDD principles, the full SDD lifecycle as
a map for the rest of the course, and what makes an AI system "agentic."

`../../../brownfield-project/` is the real reference codebase for the whole course —
EdgeX Foundry (Go) + edgex-ui-go (Angular) + OPC UA .NET Standard (C#), a curated slice
of a real, currently-maintained open-source industrial-IoT platform, not a synthetic
codebase. `../../../brownfield-project/assignment-pool.md` is the backlog every team
draws from starting this module. This module's own hands-on exercise is self-contained
in `vibe-coding-exhibit/`, but Steps 1–2 below set up the real project every later
module builds on.

## Hands-on

### Step 1 — Form your team and get your assignment

Form a team (however your instructor groups you). As a team, claim one unclaimed pair
from `../../../brownfield-project/assignment-pool.md` — each pair has one feature/change
and one known defect, both real and both pointing at a specific area of the curated
codebase. This is what your team carries through the rest of the course: Module 3 has
you spec *both* halves of your pair, then choose one to build; the other comes back in
Module 8.

**Checkpoint**: your team should be able to state, in one sentence each, what your
feature does and what your defect's actual root cause is (not just its symptom) — if you
can't yet, that's fine, Module 2 is where you build that understanding; just confirm
you've claimed a pair and read both linked GitHub issues/descriptions.

### Step 2 — Install and scaffold both frameworks

Confirm your agentic coding tool (GitHub Copilot or Claude Code) is installed and
authenticated in VS Code — see `../../tool-reference.md` for the command mapping between
the two; every hands-on step in this course works with either. Then, in your own scratch
working directory (**not** this repo):

```
mkdir my-team-project && cd my-team-project
uvx --from git+https://github.com/github/spec-kit.git specify init --here --integration claude
npx @fission-ai/openspec@latest init --tools claude .
```

(Swap `claude` for `copilot`/`github-copilot` in both commands if that's your tool — see
`../../tool-reference.md`. These are the real CLIs, the same ones
`../../../brownfield-project/` was scaffolded with, run for real during this course's
own prep to confirm the commands below are accurate.)

**Checkpoint**: you should now have **two** parallel scaffolds in the same project:
Spec Kit's `.specify/` (memory/, templates/, scripts/, workflows/) plus your agent's
commands (`.claude/skills/speckit-*` or Copilot's `.github/prompts/speckit.*`), *and*
OpenSpec's `openspec/` (`changes/`, `specs/`, `config.yaml`) plus its own commands
(`.claude/commands/opsx/` or `.github/prompts/opsx-*.prompt.md`). Compare *structure*,
not content, against `../../../brownfield-project/.specify/` and `.claude/` for Spec
Kit's shape. Note what's structurally different about OpenSpec: no per-feature numbered
directory, one living `specs/` tree plus a `changes/` folder for proposals-in-flight —
this is the "verbose multi-file-per-feature vs. compact delta-based" difference
`../../../SDD-Framework-Comparison_Spec-Kit-vs-OpenSpec.docx` describes, now something
you can see in your own two directories instead of reading about.

### Step 3 — Compare a basic prompt against a better one

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

6. Live-safe: scaffold both frameworks side by side in an empty scratch directory (Step
   2's two commands) and open `.specify/` next to `openspec/`. "Same underlying idea —
   spec before code — two different shapes. Spec Kit: one numbered directory per feature,
   verbose, additive, a historical record. OpenSpec: one living spec, changes proposed as
   deltas, archived once applied." Point at `openspec/changes/archive/` — empty right
   now, but that's where a completed change's delta gets folded back into the living
   spec. Close: "You'll use Spec Kit for the rest of this course because most of you are
   working against an established codebase where the full lifecycle earns its keep — but
   now you've actually run both, not just read a comparison table."
