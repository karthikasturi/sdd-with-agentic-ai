# Tool Reference: GitHub Copilot ↔ Claude Code

Same spec-driven workflow, two tools, different command syntax. Use whichever column
matches what your team has access to — every hands-on step in this course works
identically either way. Both are real, installed integrations, not approximated: Spec
Kit's own scaffold installs both sets of commands side by side
(`brownfield-project/.claude/skills/` and, once you run `specify init` yourself with
`--integration copilot`, the equivalent Copilot prompt files); OpenSpec's does the same
(`.claude/commands/opsx/` vs. `.github/prompts/opsx-*.prompt.md`, both confirmed real by
actually running `openspec init --tools claude,github-copilot` during this course's
prep).

## Spec Kit (GitHub Spec Kit CLI)

| Step | Claude Code | GitHub Copilot |
|---|---|---|
| Governance | `/speckit-constitution` | `/speckit.constitution` |
| Spec | `/speckit-specify` | `/speckit.specify` |
| Clarify | `/speckit-clarify` | `/speckit.clarify` |
| Plan | `/speckit-plan` | `/speckit.plan` |
| Tasks | `/speckit-tasks` | `/speckit.tasks` |
| Checklist | `/speckit-checklist` | `/speckit.checklist` |
| Analyze | `/speckit-analyze` | `/speckit.analyze` |
| Implement | `/speckit-implement` | `/speckit.implement` |
| Converge (assess codebase, append remaining tasks) | `/speckit-converge` | `/speckit.converge` |
| Tasks → GitHub Issues | `/speckit-taskstoissues` | `/speckit.taskstoissues` |

Claude Code: hyphenated. GitHub Copilot: dot-separated. Same underlying command either
way — Spec Kit's installer generates both from one source.

## OpenSpec CLI

| Step | Claude Code | GitHub Copilot |
|---|---|---|
| Propose a change | `/opsx:propose "idea"` | `/opsx-propose "idea"` |
| Explore before proposing | `/opsx:explore` | `/opsx-explore` |
| Apply an approved change | `/opsx:apply` | `/opsx-apply` |
| Archive a completed change | `/opsx:archive` | `/opsx-archive` |
| Sync specs after a change | `/opsx:sync` | `/opsx-sync` |
| Update an in-progress change | `/opsx:update` | `/opsx-update` |

Claude Code: colon-separated. GitHub Copilot: hyphenated. Confirmed by actually running
`npx @fission-ai/openspec@latest init --tools claude,github-copilot` — this table is the
real output, not a guess at naming convention.

## Scaffolding commands (run once per team project, not per-feature)

| Tool | Spec Kit | OpenSpec |
|---|---|---|
| Claude Code | `uvx --from git+https://github.com/github/spec-kit.git specify init --here --integration claude` | `npx @fission-ai/openspec@latest init --tools claude .` |
| GitHub Copilot | `uvx --from git+https://github.com/github/spec-kit.git specify init --here --integration copilot` | `npx @fission-ai/openspec@latest init --tools github-copilot .` |

Both frameworks can be scaffolded into the same project side by side — Module 1's
hands-on has you do exactly that, to compare `specs/` against `openspec/` directly.
