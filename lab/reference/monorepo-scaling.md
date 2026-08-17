# Reference: Scaling SDD and Copilot Customization to a Large Monorepo

This course's own reference project (`brownfield-project/`) is one cohesive set of 5
related repos, deliberately kept as separate submodules rather than one flattened
tree (see its `README.md`, "Why this shape"). **The client's own real production repo
is different in kind**: one large monorepo, GB-scale, 50-100+ modules as plain folders
— this is raw pain point #2 from training, still unaddressed as of this note. Both
Spec Kit and GitHub Copilot have real, officially-documented answers for that shape —
neither is "just do what this course's reference project does, but bigger." This doc
is those answers, verified against primary sources, not assumed.

## Part A — Where specs live at monorepo scale

Spec Kit's own [monorepo guide](https://github.github.com/spec-kit/guides/monorepo.html)
is explicit and directly usable:

- `specs/` is always a **sibling** of `.specify/`, never nested inside it — true at
  any scale.
- **The supported pattern for a monorepo is one independent Spec Kit project per
  module** — each gets its own `.specify/` + `specs/` pair, living deep inside that
  module's own directory, not centralized at the repo root:

  ```
  monorepo/
  ├── .git/                       # one shared git repository
  ├── services/
  │   ├── billing/
  │   │   └── .specify/           # billing's own Spec Kit project
  │   │       ├── memory/constitution.md
  │   │       └── specs/001-...
  │   └── inventory/
  │       └── .specify/           # inventory's own Spec Kit project
  │           └── specs/001-...
  └── ...50-100+ more modules, each the same shape
  ```

- Initialize each module independently: `specify init services/billing --integration
  copilot`.
- **Feature numbering is independent per module** — `services/billing/specs/001-...`
  and `services/inventory/specs/001-...` can both exist; there's no collision because
  numbering is scoped to the nearest `.specify/`, not the whole repo.
- **Root resolution prefers the nearest `.specify/` over the git top-level** — running
  a `/speckit.*` command from inside `services/billing/` scopes correctly on its own,
  no extra configuration needed.
- **From the repo root**, target a specific module without `cd`-ing in:
  `SPECIFY_INIT_DIR=services/billing specify workflow list`. This **hard-fails** if
  the path doesn't contain `.specify/` — it does not silently fall back to a different
  module or the root, which matters once there are 50+ real places a typo could send
  a spec.
- **No built-in constitution inheritance.** If 50-100 modules should share some base
  governance (e.g. "every service logs via the shared observability package"), Spec
  Kit doesn't wire that for you — someone has to decide how a shared constitution gets
  referenced from each module's own `constitution.md` and maintain that by hand.
- Git branches are still repo-wide (one shared `.git`) even though spec *artifacts*
  are module-scoped — branch naming/ownership across 50-100 modules needs its own
  convention, Spec Kit doesn't impose one.

**Why this course's reference project doesn't demonstrate this pattern directly**:
`brownfield-project` uses one shared root-level `specs/` because its 5 repos are
genuinely one product surface for this course's purposes (a single assignment pool,
one constitution's worth of shared convention). A 50-100 module monorepo is the
opposite case — many independently-owned surfaces sharing one git history — which is
exactly what the per-module `.specify/` pattern above is for.

## Part B — Where Copilot customization files live at monorepo scale

Not one uniform answer — it depends which file type, verified directly against
GitHub's docs (not a search summary — one aggregated summary during this research
claimed something the primary source contradicted):

| File | Can it live deep/nested in a module? |
|---|---|
| `.github/copilot-instructions.md` | **No.** Repo-root only. |
| `.github/instructions/*.instructions.md` | **No** for the file's own location (must sit under root `.github/instructions/`) — but its `applyTo` glob **can target** any deep path. The file stays centralized; its reach doesn't. |
| `.github/skills/`, `.claude/skills/`, `.agents/skills/`, `~/.copilot/skills/` | Fixed standard locations only (see `tool-reference.md`) — not documented to support nesting elsewhere. |
| **`AGENTS.md`** | **Yes** — the one format actually built for this. Discovered at the repo root, the current working directory, intermediate directories between them, and any directory nested in the path of a file being worked on. |

**`AGENTS.md` is the real mechanism for "each module keeps its own local guidance,
co-located with its own code"** — but two caveats, verified against a real open
GitHub issue rather than the docs page's idealized description:

- **VS Code** gates full recursive nested discovery behind an **experimental
  setting**, `chat.useNestedAgentsMdFiles` — off by default. Without it, VS Code's
  behavior is closer to the CLI's (below), not full workspace-wide recursion.
- **The Copilot CLI** currently discovers `AGENTS.md` files only along the path from
  the **current working directory** up to the git root — not a full recursive scan of
  every subfolder regardless of where you're standing (open feature request,
  [copilot-cli#3051](https://github.com/github/copilot-cli/issues/3051), unresolved
  as of this writing). In practice: reliable if someone is actually `cd`'d into or
  editing a file inside the module in question; not reliable if they're working from
  the repo root against a deeply nested file.

### Decision guide

- **Guidance that's true for the whole monorepo, rarely changes, short**: root
  `.github/copilot-instructions.md`. (Per-2-page guidance — see `tool-reference.md`.)
- **Guidance scoped to a specific tech stack or module, but you want it centrally
  maintained/reviewed**: root `.github/instructions/<name>.instructions.md` with an
  `applyTo` glob targeting that module's path — this is what
  `brownfield-project/.github/instructions/` does for this course's 3 tech stacks.
- **Guidance a module team should own and edit themselves, co-located with their own
  code, without needing repo-root write access**: `AGENTS.md` inside that module's own
  directory — accept the CLI/VS Code-setting caveats above, or pair it with a root
  `.instructions.md` as a fallback for anyone hitting the gap.

## Sources

- [Spec Kit monorepo guide](https://github.github.com/spec-kit/guides/monorepo.html)
- [GitHub Copilot repository custom instructions](https://docs.github.com/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot)
- [GitHub Copilot CLI custom instructions (AGENTS.md discovery rules)](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-custom-instructions)
- [copilot-cli#3051 — nested AGENTS.md discovery, open as of this writing](https://github.com/github/copilot-cli/issues/3051)

All verified directly against these pages on 2026-08-18, not carried over from
training-data assumptions — check them again if this reference gets reused for a
future cohort, since Copilot's customization surface has been changing quickly.
