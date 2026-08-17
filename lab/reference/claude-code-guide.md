# Reference: Claude Code

Nobody in this cohort is using Claude Code — GitHub Copilot is the only tool in play,
and the rest of `lab/` is written that way, with no dual-notation clutter. This file is
where all the Claude Code material moved to, kept for two reasons: `brownfield-project/`
itself was actually scaffolded and built with Claude Code during this course's prep
(`.claude/skills/` in its root is real, not hypothetical), and a future cohort running
this same course with Claude Code participants shouldn't have to reconstruct this from
scratch. If neither applies to you, you don't need this file.

Everything below was real and verified at the time it was written — same rigor bar as
the rest of this course's material, just not exercised by this cohort.

## Command mapping — Spec Kit

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

## Command mapping — OpenSpec CLI

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

Both frameworks can be scaffolded into the same project side by side — that's how
`brownfield-project/` itself was built, and how Module 1's hands-on has *this* cohort
do it too, just with `copilot` in both commands instead of `claude`.

Both are real, installed integrations, not approximated: Spec Kit's own scaffold
installs both sets of commands (`--integration copilot` vs. `--integration claude`,
`brownfield-project/.claude/skills/` shows the Claude Code side); OpenSpec's does the
same (`.github/prompts/opsx-*.prompt.md` vs. `.claude/commands/opsx/`).

## Editor and agent setup

Claude Code CLI, installed and authenticated, plus its VS Code extension if you want the
in-editor experience. `brownfield-project/.claude/skills/` and `.claude/commands/opsx/`
are what this produces once scaffolded.

## MCP setup — two separate configs, not one

If a team runs **both** GitHub Copilot and Claude Code in VS Code, MCP has to be
configured **twice** per server — Copilot and Claude Code don't share config, even in
the same VS Code window:

| Tool | Config location | Used by |
|---|---|---|
| GitHub Copilot (VS Code) | `.vscode/mcp.json` (workspace) or VS Code's global `mcp.json` | VS Code's own Copilot Chat/Agent mode |
| Claude Code (CLI **and** VS Code extension) | `.mcp.json` at project root, or `~/.claude/settings.json` (user-level) | Both the CLI and the VS Code extension — the extension runs the CLI underneath, so one setup covers both |

Setting up one does **not** configure the other. This is a real, currently-open point of
confusion (see `anthropics/claude-code` issue #47344, a feature request asking for them
to be unified) — not a mistake, if a server set up in one tool doesn't show up in the
other. Applies identically to both servers below.

### Atlassian MCP (Jira + Confluence) — Claude Code

```
claude mcp add --transport http atlassian https://mcp.atlassian.com/v1/mcp/authv2 --scope project
```
Then authenticate: inside a Claude Code session, run `/mcp`, select `atlassian`, and
complete the OAuth flow. `--scope project` writes to `.mcp.json` at your project root
(shareable, no secrets in the file itself — auth is separate, browser-based).

**API token alternative** (if OAuth isn't available in your environment): Atlassian
account → Security → API tokens → create one → pass it via `--header` on the `add`
command. Requires admin enablement in some Atlassian Cloud orgs — OAuth is the primary,
recommended path.

### GitHub MCP — Claude Code

```
claude mcp add --transport http github https://api.githubcopilot.com/mcp/ --scope project
```
PAT alternative: `--header "Authorization: Bearer <your-token>"` — generate one at
GitHub → Settings → Developer settings → Personal access tokens → **Fine-grained
tokens**, resource owner your account, repository access **Public repositories
(read-only)** (every repo this course uses is public — `edgexfoundry/*`,
`OPCFoundation/UA-.NETStandard`).

**Verify**: `claude mcp list` should show the server connected (`atlassian` or `github`)
— re-run `/mcp` inside a session if auth expired or never completed. Ask your agent to
fetch `edgexfoundry/device-opc-ua#53` and confirm the summary matches the real issue
(OOM after ~11 hours, retention not reclaiming space) — not hallucinated.

See `../mcp-setup.md` for the Copilot instructions this cohort actually uses, and for
the "be precise about project/space" guidance, which applies identically to both tools.
