# Tool Reference: GitHub Copilot

GitHub Copilot is this cohort's only tool — every hands-on step in this course is
written for it directly, no dual-notation to translate. (If you're revisiting this
course with Claude Code instead, or setting it up alongside Copilot, see
`reference/claude-code-guide.md` — it has the equivalent command mapping and was real
and verified, just not what this batch uses.)

Spec Kit's own scaffold installs the full command set once you run `specify init` with
`--integration copilot`; OpenSpec's does the same via
`openspec init --tools github-copilot` — both confirmed real by actually running them
during this course's prep, not approximated.

## Spec Kit (GitHub Spec Kit CLI)

| Step | Command |
|---|---|
| Governance | `/speckit.constitution` |
| Spec | `/speckit.specify` |
| Clarify | `/speckit.clarify` |
| Plan | `/speckit.plan` |
| Tasks | `/speckit.tasks` |
| Checklist | `/speckit.checklist` |
| Analyze | `/speckit.analyze` |
| Implement | `/speckit.implement` |
| Converge (assess codebase, append remaining tasks) | `/speckit.converge` |
| Tasks → GitHub Issues | `/speckit.taskstoissues` |

## OpenSpec CLI

| Step | Command |
|---|---|
| Propose a change | `/opsx-propose "idea"` |
| Explore before proposing | `/opsx-explore` |
| Apply an approved change | `/opsx-apply` |
| Archive a completed change | `/opsx-archive` |
| Sync specs after a change | `/opsx-sync` |
| Update an in-progress change | `/opsx-update` |

Confirmed by actually running `npx @fission-ai/openspec@latest init --tools claude,github-copilot`
during this course's prep — this table is the real output, not a guess at naming
convention.

## Scaffolding commands (run once per team project, not per-feature)

| Framework | Command |
|---|---|
| Spec Kit | `uvx --from git+https://github.com/github/spec-kit.git specify init --here --integration copilot` |
| OpenSpec | `npx @fission-ai/openspec@latest init --tools github-copilot .` |

Both frameworks can be scaffolded into the same project side by side — Module 1's
hands-on has you do exactly that, to compare `specs/` against `openspec/` directly.
