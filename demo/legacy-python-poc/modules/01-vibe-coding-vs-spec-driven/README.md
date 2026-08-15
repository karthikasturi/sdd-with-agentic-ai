# Module 1 — From Vibe Coding to Spec-Driven Development

Covers: failure modes of ad hoc AI prompting, SDD principles, the full SDD lifecycle as a map for the rest of the course, and what makes an AI system "agentic."

`project/` (two levels up) is the instructor/reference answer key for the whole course — its final state, not a per-module snapshot. This module doesn't touch it; everything here is self-contained in `vibe-coding-exhibit/`.

## Hands-on

### Step 1 — Install and scaffold

Confirm your agentic coding tool is installed and working. Then, in your own scratch working directory (not this repo):

```
mkdir my-equipment-project && cd my-equipment-project
uvx --from git+https://github.com/github/spec-kit.git specify init --here --integration claude
```

(Swap `--integration claude` for your tool's integration name if different — run `specify check` to see supported integrations.) This is the real GitHub Spec Kit CLI — the same one `project/` was built with — not a course-specific tool.

**Checkpoint**: You should have a `.specify/` directory and your agent's command/skill integration installed (e.g. `.claude/skills/speckit-*`). Compare the *structure* against `../../project/.specify/` and `../../project/.claude/` — content will differ (that comes in Module 2), structure should match.

### Step 2 — Compare a basic prompt against a better one

Feed the prompt in `vibe-coding-exhibit/PROMPT.md` to your agent, cold, in a separate empty scratch directory — no constitution, no spec. Then do the same with `vibe-coding-exhibit/PROMPT-ADVANCED.md`.

**Checkpoint**: Compare both outputs against `vibe-coding-exhibit/output/` and `vibe-coding-exhibit/output-advanced/`. The second prompt should produce meaningfully better code — real validation, per-equipment-type thresholds, working error handling. Now look for what's *still* missing in both: neither handles equipment that stops reporting, neither prevents duplicate alerts from repeated bad readings. Read `vibe-coding-exhibit/NOTES.md` for the full breakdown — this gap is the setup for Module 2.

## What's in `vibe-coding-exhibit/`

- `PROMPT.md` + `output/` — a naive one-line prompt and its real, unedited output.
- `PROMPT-ADVANCED.md` + `output-advanced/` — a genuinely better, more thoughtful prompt and its real output (runs end-to-end, verified live).
- `NOTES.md` — the critique: what went wrong in each, mapped to the four failure modes below, plus what a better prompt fixes and what it still can't.

## Demo talk track (sales / technical evaluation call)

**Suggested time**: 5–6 minutes.

1. Open `vibe-coding-exhibit/PROMPT.md`, then `output/main.py`. *"This is the entire input — one line, no spec. Here's what came back."* Scroll to line 37 (`if r.value > 100:`) — one hardcoded number pretending to be a real threshold for every equipment type. Then lines 60–63, the acknowledge endpoint — `Alert` never defines an `id` field, so this endpoint is permanently dead code. It'll pass a smoke test. It'll pass a skim review. It will never work.
2. Open `NOTES.md` and name the four failure modes on screen: **context drift, hallucinated APIs, silent scope creep, unreviewable diffs**. This is the "why" for the entire rest of the course — every later stage exists to catch one of these four things before it ships.
3. Open `PROMPT-ADVANCED.md` next to `output-advanced/main.py` — show it's real, working, meaningfully better code. Then point at what's still missing (no dedup, no debounce) even here. *"A better prompt closes the obvious gaps. It takes a dedicated process to close the ones that only surface once you ask 'what happens when this keeps happening?'"*
4. Open `../../project/.claude/skills/` and show the installed Spec Kit skills: `speckit-constitution`, `speckit-specify`, `speckit-clarify`, `speckit-plan`, `speckit-tasks`, `speckit-checklist`, `speckit-analyze`, `speckit-implement` — this *is* the lifecycle, installed as real, runnable tooling.

Close: *"Everything from here forward is the same domain, going through that lifecycle instead."*
