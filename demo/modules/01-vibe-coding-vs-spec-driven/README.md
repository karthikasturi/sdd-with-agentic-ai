# Module 1 — From Vibe Coding to Spec-Driven Development (Demo)

Covers: failure modes of ad hoc AI prompting, SDD principles, the full SDD lifecycle as
a map for the rest of the course, and what makes an AI system "agentic."

Participant hands-on material for this module: `../../../lab/modules/01-vibe-coding-vs-spec-driven/README.md`.
This file is the presenter-facing talk track only.

`../../../brownfield-project/` is the real reference codebase for the whole course —
EdgeX Foundry (Go) + edgex-ui-go (Angular) + OPC UA .NET Standard (C#), a curated slice
of a real, currently-maintained open-source industrial-IoT platform, not a synthetic
codebase.

## Demo talk track (5–6 minutes)

**Live vs. pre-built**: Steps 1 and 3 below are safe to run genuinely live if you want
the credibility of "watch me do it right now" — low stakes, low variance, a few minutes
each. Steps 2 and 4 depend on specific output (the exact silent bug, the exact remaining
gap) — walk through the pre-built exhibit for those instead of re-running the prompts
live; an LLM re-run is not guaranteed to reproduce the same mistake twice, and the point
of this module is those *specific* mistakes, not "a" mistake. Every exhibit file
referenced below (by name alone from here on) lives in
`../../../lab/modules/01-vibe-coding-vs-spec-driven/vibe-coding-exhibit/`.

1. Open `PROMPT.md`, then `output/main.go` side by side — "the entire input was three
   sentences. No spec. No constitution. Empty directory." Point at `const threshold =
   100.0` — one number, every reading, every equipment type, no exceptions. Then scroll
   to `acknowledgeAlert`'s `for _, alert := range alerts` loop. "This compiles. It
   returns 200. It runs. It never acknowledges a single alert" — run the live curl
   sequence from `NOTES.md` and show the field staying `false`. "A smoke test that only
   checks the status code passes this every time."

2. Open `NOTES.md`, name the four failure modes on screen:
   **context drift, hallucinated understanding, silent scope creep, unreviewable
   diffs** — this is the vocabulary for the rest of the course.

3. Open `PROMPT-ADVANCED.md` next to `output-advanced/main.go` —
   real, working, better code: per-type thresholds, a 404 on unregistered equipment, an
   idempotent-*rejecting* acknowledge endpoint this time. Then run three consecutive
   critical readings live and show three separate alerts instead of one. Quote: *"A
   better prompt closes the obvious gaps. It takes a dedicated process to close the ones
   that only surface once you ask 'what happens when this keeps happening?'"* — that's
   Module 3.

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

6. Live-safe: scaffold both frameworks side by side in an empty scratch directory
   (`../../../lab/tool-reference.md`'s two commands) and open `.specify/` next to
   `openspec/`. "Same underlying idea — spec before code — two different shapes. Spec
   Kit: one numbered directory per feature, verbose, additive, a historical record.
   OpenSpec: one living spec, changes proposed as deltas, archived once applied." Point
   at `openspec/changes/archive/` — empty right now, but that's where a completed
   change's delta gets folded back into the living spec. Close: "You'll use Spec Kit for
   the rest of this course because most of you are working against an established
   codebase where the full lifecycle earns its keep — but now you've actually run both,
   not just read a comparison table."
