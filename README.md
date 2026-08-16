# Spec-Driven Development with Agentic AI

A team-based, 3-day training course on spec-driven development with AI coding agents
(GitHub Copilot and Claude Code) — constitution through implementation and review,
taught against a real brownfield codebase, not a toy example.

## What's in this repo

```
course-outline/    the official course outline (duration, objectives, per-module outline)
presentation/       slide decks, one per module (PDF; .pptx gitignored, ask for those separately)
assessment/         pre/post-assessment quizzes (gitignored — ask for these separately)
demo/               the actual hands-on package — start here
```

**Start with [`demo/README.md`](demo/README.md)** — it's the real entry point: how the
three days flow, module by module, and what's real vs. what's still in progress.

## Before Day 1

- [`lab/setup-guide.md`](lab/setup-guide.md) — toolchains, the reference project
  clone, a smoke test. Run this first.
- [`lab/mcp-setup.md`](lab/mcp-setup.md) — MCP server setup (GitHub Copilot primary,
  Claude Code as a secondary guide) for Atlassian Jira/Confluence and GitHub.
- [`lab/tool-reference.md`](lab/tool-reference.md) — command mapping between the two
  tools, for every hands-on step.

## Hands-on vs. demo material

- **`lab/`** — everything a participant actually does: setup, MCP config, tool
  reference, every module's hands-on steps and exhibit files, and the Capstone's formal
  requirements. This is what you work from during the live course.
- **`demo/`** — the presenter-facing material: each module's "Demo talk track" script,
  and `review-trail.html`, for a sales/evaluation walkthrough. Not needed to run the
  hands-on labs themselves.

## The reference codebase

The actual project teams work in — EdgeX Foundry (Go), edgex-ui-go (Angular), and OPC
UA .NET Standard (C#), a curated slice of a real, currently-maintained open-source
industrial-IoT platform — lives in a **separate companion repo**, not in this one:
[`Siemens-training/brownfield-project`](https://github.com/Siemens-training/brownfield-project)
(public). It's meant to read like a real product's source, not course collateral —
`lab/setup-guide.md` §4 has the real clone command, verified against a genuinely fresh
clone.

## How the three days flow

**Day 1** (Modules 1–3): teams form, claim a real feature+defect pair, scaffold Spec Kit
and OpenSpec, orient in the codebase, write a constitution, spec and clarify both halves
of their pair.

**Day 2** (Modules 4–6): plan the carried-forward spec, clear checklist/analyze gates,
implement one task end-to-end, then review an instructor-provided flawed change that
passes every automated gate and is still wrong.

**Day 3** (Modules 7–8 + Capstone): a real, independently-verified multi-agent
delegation; the same feature specified two wrong ways and one corrected way; then the
set-aside spec taken through the full lifecycle for the first time, with deliberately
less scaffolding than the earlier modules.

Every checkpoint in this course points at something real — working code with real
tests, real git history showing corrected mistakes, real GitHub issues — not staged
output. See `demo/README.md` for the full breakdown.
