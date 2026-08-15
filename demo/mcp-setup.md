# MCP Server Setup — GitHub Copilot & Claude Code

Module 2 (Discovery at Scale) needs your agent connected to the bug/defect tracker
alongside the code itself — that's what "MCP-connected design documentation and code"
means in the course objectives. This course's curated repos live on GitHub, so the
concrete tool is the **GitHub MCP server**. (Your own team's day job likely uses Jira or
Azure DevOps instead — the skill transfers, the specific server doesn't. See the note at
the bottom.)

## The server this course uses

GitHub's **official, hosted, remote** MCP server — no local install, no Docker
container to run yourself:

```
https://api.githubcopilot.com/mcp/
```

Sourced from GitHub's own current docs (`docs.github.com/en/copilot/how-tos/provide-context/use-mcp-in-your-ide/set-up-the-github-mcp-server`)
and the `github/github-mcp-server` repo's `docs/remote-server.md` — not guessed at. One
honest caveat: this setup guide is built from that documentation, not from an
end-to-end connection I ran myself in this environment (no MCP tool access here to test
with). Run the verification step near the bottom before Module 2 actually depends on it.

## Important: two separate configs, not one

If you use **both** GitHub Copilot and Claude Code in VS Code, you need to configure
MCP **twice** — they don't share config, even in the same VS Code window:

| Tool | Config location | Used by |
|---|---|---|
| GitHub Copilot (VS Code) | `.vscode/mcp.json` (workspace) or VS Code's global `mcp.json` | VS Code's own Copilot Chat/Agent mode |
| Claude Code (CLI **and** VS Code extension) | `.mcp.json` at project root, or `~/.claude/settings.json` (user-level) | Both the CLI and the VS Code extension — the extension runs the CLI underneath, so one setup covers both |

Setting up one does **not** configure the other. This is a real, currently-open point of
confusion (see `anthropics/claude-code` issue #47344, a feature request asking for them
to be unified) — not a mistake you made if your first setup doesn't show up in the other
tool.

## Setup: GitHub Copilot (VS Code)

**Easiest — via the UI:**
1. Extensions panel (`Ctrl+Shift+X` / `Cmd+Shift+X`) → search `@mcp github` → Install.
2. Confirm "trust this server" when prompted.
3. Sign in via the one-click OAuth flow (no PAT needed for this path).
4. Verify: Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`) → **MCP: List Servers** →
   `github` should show as running.

**Manual — via config file** (useful for a workspace-level, team-shareable setup):
create `.vscode/mcp.json` in your project root:
```json
{
  "servers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/"
    }
  }
}
```
VS Code will prompt for auth (OAuth or a PAT, your choice) the first time Copilot Chat
tries to use it.

## Setup: Claude Code (CLI and VS Code extension — one setup, both)

In a terminal (the integrated VS Code terminal works fine):
```
claude mcp add --transport http github https://api.githubcopilot.com/mcp/ --scope project
```
- `--scope project` writes to `.mcp.json` at your project root — shareable with your
  team if you commit it (no secrets live in this file; auth happens separately, below).
- Use `--scope user` instead if you want this available across all your projects, not
  tied to one repo.

**Auth**: first real use triggers an OAuth browser sign-in, same flow as Copilot's. If
you'd rather use a PAT directly:
```
claude mcp add --transport http github https://api.githubcopilot.com/mcp/ --header "Authorization: Bearer <your-token>"
```
(see the PAT section below for how to generate `<your-token>`.)

**Verify**:
```
claude mcp list
```
should show `github` as connected. Inside an active Claude Code session, `/mcp` shows
the same thing and lets you inspect what tools the server exposes.

## Generating a GitHub PAT (if you'd rather not use the OAuth browser flow)

1. GitHub → Settings → Developer settings → Personal access tokens → **Fine-grained tokens**.
2. Resource owner: your account. Repository access: **Public repositories (read-only)**
   is sufficient — every repo this course uses (`edgexfoundry/*`, `OPCFoundation/UA-.NETStandard`)
   is public.
3. No account-level permissions needed beyond the default read access this grants.
4. Copy the token once generated — GitHub won't show it again.

Unauthenticated GitHub API access works too, but rate-limits hard and fast — if Module 2
Step 3's issue search starts failing partway through, this is the first thing to check.

## Verify it actually works, before you need it in Module 2

Ask your agent, in plain language: *"Using the GitHub MCP tool, fetch issue #53 from
edgexfoundry/device-opc-ua and summarize it."* You should get back a real summary — OOM
after ~11 hours of sustained data collection, retention policy not reclaiming space (the
same issue `discovery-log.md` and the assignment pool's Pair 1 already reference). If
instead you get a generic "I don't have access to that" or a hallucinated-sounding
summary, the MCP connection isn't actually live — fix it before Module 2, not during it.

## Troubleshooting

- **VS Code shows 0 servers after adding one**: reload the window
  (`Developer: Reload Window` in the Command Palette).
- **`claude mcp list` shows the server but "unreachable"**: re-run the `add` command;
  auth may have expired or never completed.
- **Results look plausible but wrong**: this is worse than an obvious failure — always
  cross-check one real fact against the actual GitHub issue in a browser before trusting
  the MCP path for anything you're about to put in a spec.

## Your own team's tracker isn't GitHub Issues

This course's hands-on uses GitHub Issues because these curated repos are public GitHub
repos. If your actual work uses Jira or Azure DevOps, the same MCP pattern applies —
Atlassian and Microsoft both publish MCP servers for their own trackers — but the setup
commands above are specific to GitHub's server. The transferable lesson from Module 2 is
"connect your agent to wherever your team's known issues actually live," not
"GitHub Issues specifically."
