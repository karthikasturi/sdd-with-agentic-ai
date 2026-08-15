# Superseded — kept for reference only

This directory (`demo/legacy-python-poc/`) is the **first version** of this course's
hands-on package: a small, from-scratch Python/FastAPI "equipment health monitoring"
service, built to demonstrate the full spec-driven lifecycle on a greenfield toy project.

It was superseded on 2026-08-15 in favor of a brownfield reference base
(`../../brownfield-project/` — EdgeX Foundry [Go] + edgex-ui-go [Angular] + OPC UA
.NET Standard [C#]), so the hands-on material matches the client's actual stack and
gives participants real, large-codebase scale to work in instead of a synthetic toy.
See `../../../.claudep/plans/velvet-drifting-piglet.md` in your Claude Code plan history,
or ask Claude, for the full rationale.

**Nothing here is deleted or wrong** — the lifecycle it demonstrates (constitution →
specify → clarify → plan → tasks → checklist → analyze → implement) and the pattern each
module README follows (Hands-on steps with checkpoints + a Demo talk track script) are
exactly what the new material reuses. This is kept as:
- a smaller, simpler comparison example if a participant or reviewer wants to see the
  same lifecycle on an easier, single-language, single-repo project first;
- a fallback if anything in the brownfield rebuild isn't ready in time.

Original contents, unchanged:
- `project/` — the finished reference implementation (Python/FastAPI/SQLAlchemy).
- `modules/01-07/` — the original 7 module hands-on + demo-talk-track guides.
- `review-trail.html` — the original interactive command-reference walkthrough.
- `README.md` — the original package overview.
