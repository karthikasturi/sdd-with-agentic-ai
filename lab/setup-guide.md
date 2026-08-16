# Day-0 Setup Guide

Do this **before** Day 1 — Module 1 starts with team formation and scaffolding, not
toolchain installs. Everything below was verified against this course's actual curated
repos during prep (versions shown are what was actually tested, not just what's
generally recommended), except where marked otherwise.

## 1. Core tools

| Tool | Version tested | Check |
|---|---|---|
| Git | any recent version | `git --version` |
| Go | 1.25+ (repos target 1.25; a 1.26 toolchain built and ran everything cleanly during prep) | `go version` |
| Node.js | 22.x (tested: 22.23.1) | `node --version` |
| npm | 10.x (tested: 10.9.8) | `npm --version` |
| `uv` / `uvx` | 0.11+ (tested: 0.11.30) — installs the GitHub Spec Kit CLI | `uv --version` |
| .NET SDK | 8.0+ | `dotnet --version` |
| Google Chrome (or Chromium) | any recent version — needed to run `edgex-ui-go`'s real Angular tests headlessly | `google-chrome --version` |

**Honest gap**: everything above except the .NET SDK row was actually installed and
exercised for real during this course's prep — Go builds/tests, Angular
`npm install`+`ng test`, `uv`-installed Spec Kit, all run and verified. The .NET SDK
was **not** available in the prep environment, so the OPC UA reference server
(`opc-ua-dotnet/samples/ConsoleReferenceServer`, used by Pairs 1 and 5 in the
assignment pool) has never actually been built or run. Confirm this works on your own
machine before Day 1 if your team's pair depends on it:
```
cd brownfield-project/repos/opc-ua-dotnet
dotnet build samples/ConsoleReferenceServer
```
If this doesn't build cleanly, flag it — it's the one piece of this course's toolchain
that's still unverified.

## 2. Editor and agent

- **VS Code**, current version.
- **GitHub Copilot** extension (licensed/provisioned) — **and/or**
- **Claude Code CLI**, installed and authenticated, plus its VS Code extension if you
  want the in-editor experience.

Whichever tool(s) your team has access to, `tool-reference.md` has the full command
mapping so every hands-on step works the same either way.

## 3. MCP servers

Required for Module 2. Full instructions, including a real gotcha (Copilot and Claude
Code use separate MCP configs even in the same VS Code window): `mcp-setup.md`.

## 4. Clone the reference project

```
git clone https://github.com/Siemens-training/brownfield-project.git
cd brownfield-project
git submodule update --init --recursive --depth 100
```

This pulls the 5 curated repos (`edgex-go`, `device-modbus-go`, `device-opc-ua`,
`edgex-ui-go`, `opc-ua-dotnet`) as submodules, shallow-cloned. Two of them
(`device-opc-ua`, `edgex-ui-go`) resolve from `Siemens-training` forks carrying this
course's own `course/opcua-threshold-alerting` branch — the actual worked reference
implementation, not just the vanilla upstream code. The other three point at real
upstream directly since they're used unmodified. Verified against a genuinely fresh
clone during prep: `go test ./internal/threshold/... -cover` passes at 94.3%
immediately after clone, no extra steps. `README.md` and `assignment-pool.md` at the
repo root are your starting points.

## 5. Spec Kit and OpenSpec CLIs

Both get scaffolded live during Module 1 — nothing to pre-install beyond `uv`/`uvx` and
`npm` above (both CLIs run via `uvx`/`npx`, no separate install step). If you want to
confirm they work ahead of time:
```
uvx --from git+https://github.com/github/spec-kit.git specify --help
npx --yes @fission-ai/openspec@latest --version
```

## 6. Smoke test — run this the night before, not during Module 1

```
git --version && go version && node --version && npm --version && uv --version
cd brownfield-project && git submodule status   # should list all 5, no errors
cd repos/device-opc-ua && go build ./... && go test ./...   # should pass clean
cd ../edgex-ui-go/web && npm install --no-audit --no-fund   # takes ~15-20s once cached
```

If all of that runs clean, your machine is ready for Day 1.
