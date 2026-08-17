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

## Customization file locations — not just the defaults

Beyond what Spec Kit/OpenSpec scaffold for you, Copilot itself reads a few kinds of
customization file, each from more than one possible location — useful if your org
already has conventions for where this stuff lives:

| Kind | Repo-level location(s) | Personal/global location(s) |
|---|---|---|
| Custom instructions | `.github/copilot-instructions.md` (repo-wide), `.github/instructions/*.instructions.md` (path-scoped, `applyTo` frontmatter) | — |
| Agent Skills (`SKILL.md`) | `.github/skills/`, `.claude/skills/`, `.agents/skills/` (any one repo can use whichever) | `~/.copilot/skills/`, `~/.agents/skills/` |
| Agent files (`.agent.md`) | `.github/agents/` | — |
| Prompt files (`.prompt.md`) | `.github/prompts/` | — |

Verified directly against
[GitHub's own agent-skills docs](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills),
not assumed.

**Prompt files vs. Agent Skills**: prompt files still work — they're not deprecated —
but they're manually invoked (you type `/name`), single-file, and IDE-only. Agent
Skills are model-invoked (Copilot decides on its own when to use one) and also run on
the Copilot cloud agent and CLI, not just in-editor. If you're about to invest in a
large prompt-file library, know that the ecosystem's direction is skills, not more
prompt files — worth designing new reusable instructions as a skill from the start
rather than migrating later.
