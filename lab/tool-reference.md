# Tool Reference: GitHub Copilot (primary) + Claude Code (secondary)

GitHub Copilot is this course's primary tool — set up first, already the one with a
confirmed working Atlassian MCP connection (see `mcp-setup.md`). Claude Code follows the
same spec-driven workflow with different command syntax, documented here as the
secondary path for teams using it instead. Every hands-on step in this course works
identically either way — use whichever column matches what your team has access to.

Both are real, installed integrations, not approximated: Spec Kit's own scaffold
installs both sets of commands side by side (once you run `specify init` with
`--integration copilot`, and separately with `--integration claude`,
`brownfield-project/.claude/skills/` shows the Claude Code side); OpenSpec's does the
same (`.github/prompts/opsx-*.prompt.md` vs. `.claude/commands/opsx/`, both confirmed
real by actually running `openspec init --tools claude,github-copilot` during this
course's prep).

## Spec Kit (GitHub Spec Kit CLI)

| Step | GitHub Copilot | Claude Code |
|---|---|---|
| Governance | `/speckit.constitution` | `/speckit-constitution` |
| Spec | `/speckit.specify` | `/speckit-specify` |
| Clarify | `/speckit.clarify` | `/speckit-clarify` |
| Plan | `/speckit.plan` | `/speckit-plan` |
| Tasks | `/speckit.tasks` | `/speckit-tasks` |
| Checklist | `/speckit.checklist` | `/speckit-checklist` |
| Analyze | `/speckit.analyze` | `/speckit-analyze` |
| Implement | `/speckit.implement` | `/speckit-implement` |
| Converge (assess codebase, append remaining tasks) | `/speckit.converge` | `/speckit-converge` |
| Tasks → GitHub Issues | `/speckit.taskstoissues` | `/speckit-taskstoissues` |

GitHub Copilot: dot-separated. Claude Code: hyphenated. Same underlying command either
way — Spec Kit's installer generates both from one source.

## OpenSpec CLI

| Step | GitHub Copilot | Claude Code |
|---|---|---|
| Propose a change | `/opsx-propose "idea"` | `/opsx:propose "idea"` |
| Explore before proposing | `/opsx-explore` | `/opsx:explore` |
| Apply an approved change | `/opsx-apply` | `/opsx:apply` |
| Archive a completed change | `/opsx-archive` | `/opsx:archive` |
| Sync specs after a change | `/opsx-sync` | `/opsx:sync` |
| Update an in-progress change | `/opsx-update` | `/opsx:update` |

GitHub Copilot: hyphenated. Claude Code: colon-separated. Confirmed by actually running
`npx @fission-ai/openspec@latest init --tools claude,github-copilot` — this table is the
real output, not a guess at naming convention.

## Scaffolding commands (run once per team project, not per-feature)

| Tool | Spec Kit | OpenSpec |
|---|---|---|
| GitHub Copilot | `uvx --from git+https://github.com/github/spec-kit.git specify init --here --integration copilot` | `npx @fission-ai/openspec@latest init --tools github-copilot .` |
| Claude Code | `uvx --from git+https://github.com/github/spec-kit.git specify init --here --integration claude` | `npx @fission-ai/openspec@latest init --tools claude .` |

Both frameworks can be scaffolded into the same project side by side — Module 1's
hands-on has you do exactly that, to compare `specs/` against `openspec/` directly.
