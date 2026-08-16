# MCP Server Setup — GitHub Copilot (primary) & Claude Code (secondary)

Module 2 (Discovery at Scale) needs your agent connected to the bug/defect tracker and
to design documentation, alongside the code itself — that's what "MCP-connected design
documentation and code" means in the course objectives. Two servers matter here:

- **Atlassian MCP (Jira + Confluence)** — the actual tracker and wiki this course's
  content is prepared for (`jira-content.md`/`confluence-content.md` in
  `brownfield-project/`, matching your team's real day-to-day tooling). **This is the
  primary tool Module 2 uses in this delivery** — and Modules 4 and the Capstone use it
  again, write side, to sync tasks into Jira and publish the review trail to Confluence.
  The server exposes real read *and* write tools for both products (create/update Jira
  issues, create/update Confluence pages — see Atlassian's own
  [Supported tools](https://support.atlassian.com/atlassian-rovo-mcp-server/docs/supported-tools/)
  reference), scoped by whatever your Atlassian account can already do — no separate
  write-scope setup beyond the OAuth login below.
- **GitHub MCP** — the curated repos' own real issue history (`device-opc-ua#53` and
  friends) lives on GitHub. Secondary — useful for cross-referencing the original
  upstream report behind a Jira ticket if you want the full history.

Both sections below are sourced from current official documentation, cited inline, not
guessed at. Neither was end-to-end tested by me in this environment (no MCP tool access
here) — run the verification steps before Module 2 depends on either.

## Important: two separate configs, not one

If you use **both** GitHub Copilot and Claude Code in VS Code, you configure MCP
**twice** per server — Copilot and Claude Code don't share config, even in the same VS
Code window:

| Tool | Config location | Used by |
|---|---|---|
| GitHub Copilot (VS Code) | `.vscode/mcp.json` (workspace) or VS Code's global `mcp.json` | VS Code's own Copilot Chat/Agent mode |
| Claude Code (CLI **and** VS Code extension) | `.mcp.json` at project root, or `~/.claude/settings.json` (user-level) | Both the CLI and the VS Code extension — the extension runs the CLI underneath, so one setup covers both |

Setting up one does **not** configure the other. This is a real, currently-open point of
confusion (see `anthropics/claude-code` issue #47344, a feature request asking for them
to be unified) — not a mistake you made if a server you set up doesn't show up in the
other tool. Applies identically to both servers below.

---

## Atlassian MCP (Jira + Confluence) — primary tool

Atlassian's **official, hosted, remote** MCP server — GA since February 2026, Claude as
its first official launch partner. No local install, no Docker container:

```
https://mcp.atlassian.com/v1/mcp/authv2
```
Transport: `http`. Sourced from Atlassian's own `atlassian/atlassian-mcp-server` repo
and support docs (`support.atlassian.com/atlassian-rovo-mcp-server`), verified live
during this course's prep, not guessed at.

**Critical, given how this content gets used**: this server authenticates against your
**entire** Atlassian Cloud account via OAuth — it is not scoped to one Jira project or
Confluence space at setup time. Project/space precision has to happen in **every
prompt**, not once at config time. See "Be precise about project/space," below — this
is the single most important section in this document.

### Copilot (VS Code)

**Easiest**: click the official install badge from Atlassian's GitHub repo, or in VS
Code: Extensions panel → search `@mcp atlassian` → Install → trust → OAuth sign-in →
verify via Command Palette → **MCP: List Servers**.

**Manual**, in `.vscode/mcp.json`:
```json
{
  "servers": {
    "atlassian": {
      "type": "http",
      "url": "https://mcp.atlassian.com/v1/mcp/authv2"
    }
  }
}
```

### Claude Code (CLI + extension — one setup, both)

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

### Verify Atlassian MCP

Ask your agent: *"Using the Atlassian MCP tool, search the Jira project
`[your project key]` for issues labeled `pair-1` and summarize what you find."* You
should get back something matching `jira-content.md`'s SDDTR-1/SDDTR-2 content (or
whatever your instance's actual tickets say) — not a generic "I don't have access" or a
plausible-sounding invention. Do the same for Confluence: *"Search the
`[your space key]` Confluence space for a page about platform architecture."*

**Also verify write access now, not in Module 4 for the first time**: ask your agent to
create one throwaway Jira issue (any summary, e.g. "MCP write test — delete me") in your
project, then open it in a browser to confirm it's really there. Delete it once
confirmed. Module 4 and the Capstone both depend on write access actually working —
better to find out it doesn't during setup than mid-module.

---

## Be precise about project/space — every time

Because one Atlassian MCP connection can see everything your account has access to
across Jira and Confluence, **always name the exact project key or space key in your
prompt** — "search Jira" alone lets the agent search everywhere you have access,
including real, unrelated projects if this is a shared corporate Atlassian instance.
Compare:

- ❌ *"Find open bugs related to notifications."*
- ✅ *"Find open bugs labeled `pair-2` in Jira project `[your training project key]`."*

The first version might return something from a completely different, real project by
coincidence of wording. The second can't. This matters more than it sounds like it
should — an agent with broad access and a vague instruction will do exactly what you
asked, just not exactly what you meant.

---

## GitHub MCP — secondary, cross-reference tool

GitHub's official, hosted, remote MCP server:
```
https://api.githubcopilot.com/mcp/
```
Sourced from `docs.github.com/en/copilot/how-tos/provide-context/use-mcp-in-your-ide/set-up-the-github-mcp-server`
and `github/github-mcp-server`'s `docs/remote-server.md`.

### Copilot (VS Code)
1. Extensions panel → search `@mcp github` → Install → trust → OAuth sign-in.
2. Verify: Command Palette → **MCP: List Servers** → `github` running.

Manual, in `.vscode/mcp.json`:
```json
{ "servers": { "github": { "type": "http", "url": "https://api.githubcopilot.com/mcp/" } } }
```

### Claude Code (CLI + extension)
```
claude mcp add --transport http github https://api.githubcopilot.com/mcp/ --scope project
```
PAT alternative: `--header "Authorization: Bearer <your-token>"` — generate one at
GitHub → Settings → Developer settings → Personal access tokens → **Fine-grained
tokens**, resource owner your account, repository access **Public repositories
(read-only)** (every repo this course uses is public — `edgexfoundry/*`,
`OPCFoundation/UA-.NETStandard`).

**Verify**: `claude mcp list` should show `github` connected. Ask your agent to fetch
`edgexfoundry/device-opc-ua#53` and confirm the summary matches the real issue (OOM
after ~11 hours, retention not reclaiming space) — not hallucinated.

Unauthenticated GitHub API access works too, but rate-limits hard and fast.

---

## Troubleshooting

- **VS Code shows 0 servers after adding one**: reload the window
  (`Developer: Reload Window` in the Command Palette).
- **`claude mcp list` shows a server but "unreachable"**: re-run the `add` command; auth
  may have expired or never completed — re-run `/mcp` inside a session to re-auth.
- **Atlassian results include something from an unrelated project**: you weren't
  specific enough in the prompt — see "Be precise about project/space" above. This is
  the connection working correctly, doing exactly what a vague prompt asked for.
- **Results look plausible but wrong**: worse than an obvious failure — always
  cross-check one real fact (a ticket, a page, an issue) directly in the browser before
  trusting an MCP-sourced answer for anything you're about to put in a spec.
