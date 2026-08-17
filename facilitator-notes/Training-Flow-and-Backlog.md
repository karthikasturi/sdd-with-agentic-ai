# Training Flow & Backlog

Facilitator-side notes, separate from the slide decks. This is where the flow, the reasoning behind
deviations from the plan, and everything captured mid-training gets tracked, so it doesn't only live
in one facilitator's head or get lost between sessions.

## Guiding principle

"Operation successful, patient failure" is the failure mode this training is designed to avoid.
Delivering the planned syllabus on schedule is not the goal. The goal is that participants leave able
to do their actual jobs better, specifically: using GitHub Copilot, prompts, agents, and skills
effectively, with spec-driven development as the structure that ties it together, not a competing
practice bolted on top.

Two working rules that came out of Module 1:

1. Treat client-reported experience level as a claim about frequency of use, not depth of
   understanding. Years of using Copilot through org-provided, pre-built prompts and agents does not
   teach someone how those prompts and agents work underneath. Assume the team doesn't know what they
   claim to know, verify live, rather than the opposite.
2. The audience spans multiple teams (engineering, QA, security, DevOps) with different day-to-day
   needs. Rigid, tool-specific scripted content doesn't serve all of them. Concepts need to be taught
   at the level of the underlying mental model, then connected to each team's own tools, on the fly
   where needed.

## Confirmed corrections, act on before Module 2

**Tracker tool is Jazz, not Jira.** The Module 2 discovery exercise, the Lab Environment doc's
"Atlassian Cloud trial" plan, and the draft `jira-content.md` seed tickets all currently assume
Jira/Confluence. This needs to be revisited before Module 2 runs: confirm whether an MCP
connector exists for Jazz (IBM/HCL Engineering Lifecycle Management), and if not, decide on a
fallback (manual context instead of live MCP, or a generic REST-based connector). Not yet fixed,
flagging as the most time-sensitive item on this list since Module 2 is next.

## Module 1 baseline gap, now addressed

Participants had 1-2 years of Copilot use but had never encountered `.instructions.md`, didn't have
a working model for how Copilot decides to call a tool, and thought of prompts/agents as things
someone else in the org builds for them, not something with an underlying structure. This had to be
covered live, unscripted, on Day 1.

Fix: a short primer deck (Module 0, 10 slides), delivered before Module 1, covering: how Copilot uses
tools and context, why `.instructions.md` exists, a directional before/after visual of what structure
changes (iterations, first-attempt accuracy, token cost, context window pressure), the prompt to
prompt-template to agent to skill mental model, the context-window tradeoff, a practical
compaction/handoff technique for long chats, and a bridge slide connecting it to SDD's "the spec is the
most rigorous prompt template your team will write" thesis. Built, validated, and QA'd:
`presentation/Module-0_Foundations-Before-Spec-Driven-Development.pptx` (+ matching `.pdf`).

## Scope note: Claude Code content

This team only has GitHub Copilot; Claude Code isn't part of their toolchain. **Done 2026-08-18**:
all dual-tool notation removed from `lab/`, Claude Code material consolidated into
`lab/reference/claude-code-guide.md` (kept, not deleted — useful if a future cohort has Claude Code
access, and `brownfield-project/` itself was actually scaffolded with Claude Code during prep so the
content is real, not hypothetical).

Also added while doing this pass, per direct request: real `brownfield-project/.github/copilot-instructions.md`
plus per-module path-scoped `.github/instructions/*.instructions.md` files (go-services, angular-ui,
opc-ua-dotnet-submodule) — none of the 5 curated repos had these before except `opc-ua-dotnet`'s own
real upstream one. **New gap found while building these, not yet closed** (held as not urgent for
now): the Copilot CLI walks up from cwd to the nearest git root, and each of the 5 repos under
`repos/` is its own real git submodule with its own `.git` — so a participant who `cd`s into
`repos/edgex-go/` and runs `copilot` there won't see the root-level path-scoped instructions files at
all (no git-boundary crossing). VS Code Copilot Chat, opened as one folder, isn't affected. Two
candidate fixes discussed, neither executed yet: add a thin per-submodule
`.github/copilot-instructions.md` that points back to the root content, or just document the
CLI-from-repo-root requirement in `setup-guide.md`.

## Researched answers

### Does Copilot recognize `.github` outside the repo root?

`.github/copilot-instructions.md` is read from the repository root; that's the one location Copilot
Chat, the coding agent, and Copilot code review all check automatically. In a VS Code **multi-root**
workspace, Copilot currently does **not** read `.github/copilot-instructions.md` from each root, a real
limitation for a monorepo opened as multiple workspace folders. The Copilot **CLI** behaves
differently: it walks up from your working directory to the git root, so nested `.github/` content
per package/service is picked up there. For scoping instructions to part of a monorepo without
relying on that CLI behavior, the supported pattern is a root-level
`.github/instructions/<name>.instructions.md` file with an `applyTo` glob (e.g.
`repos/device-opc-ua/**`), not a separate `.github` folder inside each submodule.
[Repository custom instructions](https://docs.github.com/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot) ·
[Multi-root workspace discussion](https://github.com/orgs/community/discussions/155450) ·
[Monorepo discussion](https://github.com/orgs/community/discussions/179916)

This is directly relevant to the brownfield project repo (five submodules under `repos/`): don't plan
on per-submodule `.github` folders working in VS Code chat the way they do in the CLI.

### Skill / prompt / agent locations other than the default

This turned out to already be more flexible than assumed. Agent files live in `.github/agents/`.
Skills are genuinely configurable: for a single repo, `.github/skills`, `.claude/skills`, or
`.agents/skills` all work; for skills shared across a person's own projects,
`~/.copilot/skills` or `~/.agents/skills`. Prompt files (`.github/prompts/*.prompt.md`) still work but
are being phased out in favor of agent skills going forward, worth mentioning to anyone about to invest
in building a large prompt-file library.
[Adding agent skills](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills) ·
[Copilot customization overview](https://blog.cloud-eng.nl/2025/12/22/copilot-customization/) ·
[Prompt files to skills migration](https://startdebugging.net/2026/07/migrate-copilot-prompt-files-to-agent-skills/)

## Corrections captured during Module 0 review

- The brownfield project repo's five components are **plain folders in one repo**, not git
  submodules, contrary to what the `repos/` README currently says. This actually simplifies the
  `.github/instructions/*.instructions.md` + `applyTo` glob guidance above: no submodule boundary to
  worry about, pure path-based scoping within a single repo. The `repos/` README and this document's
  earlier `.github` research note both need a follow-up correction pass.
- This same "plain folders, not submodules" shape is also how the client's real monorepo is
  structured (pain point 2 below: GB-scale, 50-100+ modules as folders), so the brownfield project's
  corrected structure is actually a closer match to their real environment than previously described.

## Claude Code equivalent: CLAUDE.md, researched for the reference material

Findings are genuinely mixed, worth knowing before writing any Claude Code reference content: one
source reports large accuracy gains from a well-optimized CLAUDE.md (test accuracy up double digits
in one benchmark), but an ETH Zurich study found LLM-generated context files could reduce success
rate by 3% while increasing cost 20%, with developer-written files showing a modest +4%. Separately,
long, bloated context is its own risk, the "lost in the middle" effect, where models attend poorly to
the center of a long context, with accuracy drops reported past 30% on some benchmarks. Net lesson,
already folded into Module 0's stats slide as a caveat: structure helps only when it's disciplined and
kept lean, not by default just for existing.

## The 4/6-layer prompting framework request

Some participants asked for a structured prompting framework (they referenced "4/6 layer"), with real
production examples, followed by a simple hands-on exercise: write a prompt template, then convert it
into an agent. **Built 2026-08-18**: `lab/reference/codegen-prompt-framework.md` — CODERS (Context,
Objective, Done, Exclusions, Reuse, Shape), a CO-STAR-style layered framework rebuilt specifically for
code-generation prompts rather than content writing. Retrofit-mapped against the real Module 1
exhibits (`PROMPT.md`/`PROMPT-ADVANCED.md`) as a worked example — the mapping independently confirms
`NOTES.md`'s own finding that Context is the one layer neither prompt closes, which is exactly why
Module 2 exists. Framed explicitly as one rung of rigor below a full spec (Context → service map,
Objective → EARS requirements, etc.), not a competing practice. Pointer added to Module 1's README
right after the exhibit comparison step.

**Not yet done**: the hands-on "convert a CODERS prompt into an Agent Skill" exercise, and the
question of whether this needs its own add-on session (near Module 7) or stays a reference doc teams
discover organically via the Module 1 pointer. `tool-reference.md`'s new "Customization file
locations" section (skills/agents/prompts) is the prerequisite piece for that exercise and is done;
the exercise itself isn't designed yet.

## Open design question

How do prompt/agent/skill artifacts fit alongside spec-driven development without competing with it or
turning into a second, parallel curriculum? Working answer to test with the group: a spec is the
highest-rigor form of a prompt template, constitution/spec/plan are what you get when you apply the
same "reusable, reviewed, structured ask" idea all the way to production-grade discipline. Skills and
agents are the execution layer that acts on a spec once it exists. This framing is what the primer
deck's bridge slide uses; worth testing whether it actually lands with the room before building more
content on top of it.

## Raw pain points captured from participants (for future module design, not yet actioned individually)

1. Avoid unnecessary code generation, agents doing more than asked.
2. Repo sizes in the gigabytes, monorepos with 50-100+ modules (this is exactly the scale the
   EdgeX-based brownfield project was chosen to mirror, so later modules already touch this; worth
   calling that connection out explicitly during Module 2).
3. Context management (now covered at the mental-model level in the primer deck; may need a deeper
   pass later for the monorepo-scale case specifically).
4. Projects running for decades, long-lived legacy code.
5. Refactoring, how SDD and agents change the calculus for refactor work specifically.
6. A structured way of working with GitHub Copilot day to day (partially covered by the primer deck).
7. Token cost optimization (covered at the mental-model level in the primer deck; may want a deeper
   pass with real numbers later).
8. Best practices broken out per functional team (QA, security, DevOps), not just for engineers.
9. "Spec placeholder", meaning unconfirmed, need to ask the participant who raised it what they meant
   before building anything against this one.
10. Skill/prompt/agent placeholder locations other than the defaults, answered above, worth folding
    into the primer deck or the Tool Reference handout as a quick-reference addition.

## Module 0 v2: stats correction and citation check

A third-party summary claimed developer-written `.instructions.md`/AGENTS.md files give a "4% to 5%"
absolute task-success improvement, citing arXiv:2602.11988. Read the primary source directly: the actual
number is +2.4% on average, and the paper reports this is **not statistically significant** (p = 21%).
LLM-generated files cost 20-23% more with a small, also not significant, success-rate drop. The "CCAPI
Engineering Analytics" source offered alongside it turned out to be AI-generated marketing content for an
API reseller, not a real study, it does not actually contain the numbers attributed to it and was not used.
A second, genuinely relevant paper was found in the process: arXiv:2601.20404 (Lulla et al.), which measures
AGENTS.md presence against 124 real PRs and reports a 28.64% lower median runtime and 16.58% lower output
token consumption, comparable task completion. Module 0 v2 now cites the correct 2.4% figure (labeled "not
significant"), and clearly separates that measured data from illustrative/unverified estimates (token
caching, output-token pricing multiples) rather than presenting them as fact. Lesson for future stats
slides: always read the primary source text directly, a citation attached to a claim doesn't mean the
citation supports that specific number.

## Module 0 v2: LibreOffice line-rendering bug found and fixed

The new "Two Layers" (SDD vs. execution layer) diagram uses arrows between a 4-box row and a 3-box row.
Arrows pointing right rendered fine; arrows pointing left (negative-width line shapes with `flipH`) were
silently dropped by LibreOffice's PDF export, confirmed by pixel-sampling the rendered page. Fix: stopped
normalizing line shapes to positive width via `flipH`/`flipV` and instead let the shape's `x/y/w/h` carry
the vector's own sign directly, PowerPoint and LibreOffice both handle that correctly. Worth remembering
for any future diagram primitive in this deck system that draws a line pointing up-left or down-left.

## Backlog / TODO tracking

- [x] Convert course outline to PDF.
- [x] Build the Module 0 primer deck, including the before/after impact visual (iterations, accuracy,
      token cost, context window) and the context compaction/handoff technique, both raised as asks
      during the review.
- [x] Research whether Copilot reads `.github` outside the repo root.
- [x] Research configurable skill/prompt/agent locations.
- [x] Write a reusable "why / concept / gap" prompt for scoping future modules, see
      `Future-Prompt_Why-Concept-Gap-Check.md`.
- [ ] Resolve Jazz vs. Jira tracker integration for Module 2 (time-sensitive). **Researched
      2026-08-18**: no official IBM MCP server exists for Jazz/ELM/EWM/RTC/DOORS Next (checked
      `IBM/mcp` directly), and no community OSLC-MCP connector exists either. Generic
      OpenAPI-to-MCP bridge tools are real and mature, but EWM/RTC's REST API has no clean
      published OpenAPI spec to bridge from — building one isn't a same-day job. Nothing here is
      buildable before teams reach Module 2. Recommendation: generalize Module 2/3's existing Jira
      fallback language ("MCP if live, otherwise the ticket text directly") to any tracker,
      Jazz included, rather than asserting Atlassian MCP as verified-required — not yet executed,
      pending go-ahead.
- [x] Decide and execute the Claude Code reference-folder separation. **Done 2026-08-18** — all
      dual Copilot/Claude notation removed from `lab/`, Claude Code content moved to
      `lab/reference/claude-code-guide.md`.
- [x] Design the 4/6-layer prompting framework itself. **Done 2026-08-18** — CODERS framework, see
      `lab/reference/codegen-prompt-framework.md`.
- [ ] Design the create-a-template-then-convert-to-an-agent-skill hands-on exercise, and decide
      whether it needs its own add-on session or stays discoverable via the Module 1 pointer.
- [ ] Clarify the "spec placeholder" ask with whoever raised it. (Needs the room, not something to
      resolve from notes alone.)
- [ ] Decide how, and whether, to fold items 1, 2, 4, 5, 8 above into existing modules versus a
      separate advanced session.
- [x] Update the Tool Reference handout with the skill/prompt/agent location findings above.
      **Done 2026-08-18** — re-verified against GitHub's own agent-skills docs directly (not just
      this note) before writing; one correction: prompt files aren't deprecated, just superseded
      in practice by Agent Skills — worded that way in `tool-reference.md` now.
- [x] ~~Correct the brownfield project's `repos/` README: plain folders, not git submodules.~~
      **Struck 2026-08-18** — verified directly (`.gitmodules`, gitlinks, separate `.git` per
      path all confirmed real), this premise was wrong. The README has correctly described real
      submodules since commit `dc75469` (2026-08-16), before this note was written. Likely a live
      misread of GitHub's web UI, not an actual repo issue.
- [ ] Decide which of the 10 raw pain points get woven into the existing Module 1-8 decks vs. handled
      as facilitator best-practice talking points vs. a separate advanced session. Proposed mapping
      pending review, see chat.
