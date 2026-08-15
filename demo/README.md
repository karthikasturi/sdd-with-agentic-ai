# Spec-Driven Development Package — Complete, All 3 Days

**All 8 modules plus the Capstone are built and real.** The original from-scratch
Python/FastAPI version this replaced has been removed (fully superseded, recoverable
from git history if ever needed).

## Structure

```
demo/
  README.md                    this file
  setup-guide.md                Day-0 environment setup — run this before Day 1
  mcp-setup.md                  MCP server setup for Module 2 (Copilot + Claude Code, both configs)
  tool-reference.md            GitHub Copilot ↔ Claude Code command mapping (Spec Kit + OpenSpec)
  modules/
    01-vibe-coding-vs-spec-driven/             team formation, both frameworks scaffolded, vibe-coding exhibit
    02-discovery-at-scale/                     MCP-style discovery, service/dependency map
    03-governance-and-clarified-spec/          constitution + two specs (feature + defect) + clarify
    04-from-clarified-spec-to-reviewable-plan/ plan review + task decomposition
    05-quality-gates-before-implementation/    checklist + analyze + security/coverage + real implementation
    06-reviewing-validating-maintaining/       instructor-provided flawed-change review
    07-multi-agent-workflows-and-team-adoption/  real, verified delegation
    08-common-pitfalls-and-anti-patterns/      escalation-antipattern exhibit
    capstone/                                  closing project — less scaffolding, on purpose
```

The reference codebase lives in the separate `../brownfield-project/` repo (EdgeX
Foundry [Go] + edgex-ui-go [Angular] + OPC UA .NET Standard [C#]) — real, currently
maintained open source, not synthetic. `../brownfield-project/assignment-pool.md` has
the 6 real feature+defect pairs teams draw from starting Module 1; Pair 1 (OPC UA
Threshold Alerting + `device-opc-ua#53`) is fully worked end to end — spec through a
real, tested Go implementation *and* a real, tested Angular implementation — and doubles
as the instructor's reference throughout.

## How the three days flow

**Day 1** — Module 1: teams form, claim a pair, scaffold Spec Kit and OpenSpec side by
side, watch ad hoc prompting fail on a real exhibit. Module 2: orient in the assigned
codebase area (documentation quality genuinely varies), produce a service/dependency
map. Module 3: constitution + two specs (feature and defect) + clarify both + pick one
to carry forward.

**Day 2** — Module 4: plan the carried-forward spec, correct a real architecture
decision. Module 5: checklist and analyze both catch real findings — including a
security-statement gap added specifically for this module and a real, measured
code-coverage number (94.3% vs. this repo's existing 38.4% baseline) — then implement
one task end-to-end. Module 6: review an instructor-provided flawed change that's
genuinely green (9/9 tests) and genuinely wrong — a real Go footgun no automated gate
could catch.

**Day 3** — Module 7: a real, independently-verified delegation (Go built in one
session, Angular delegated to a second, 5/5 tests passing, one real gap an independent
reviewer still caught). Module 8: the same feature specified two wrong ways and one
corrected way, all three outputs real and building; critique and rewrite your team's
own set-aside spec. **Capstone**: the set-aside spec, rewritten, taken through the full
lifecycle for the first time — deliberately less scaffolding than Modules 3–6, plus a
documented review-trail template covering both increments.

Every checkpoint points at something real: working Go *and* Angular implementations
with real tests (verified via `go test` and actual headless-Chrome `ng test` runs, not
assumed), real git history showing corrected mistakes, real GitHub issues, a real
OpenSpec scaffold actually run during prep — not staged output.

## Status

- [x] All 8 modules + Capstone, assignment pool, Tool Reference handout.
- [x] Defect-side worked spec, flawed-change exhibit, delegation transcript,
      escalation-antipattern exhibit — all real, all verified to compile/run.
- [x] Full reference implementation: Go (`device-opc-ua`) and Angular (`edgex-ui-go`),
      both tested and committed on course branches.
- [x] `review-trail.html` rebuild — 10-slide walkthrough (JS/data verified; visual
      render unverifiable in this sandbox, no browser available).
- [x] `setup-guide.md` and `mcp-setup.md` — Day-0 environment and MCP setup.
- [ ] Real GitHub forks for the submodules (currently local branches only) — needed only
      if this goes out to participants who need to push their own commits; not required
      for instructor-led delivery from this machine.
- [ ] .NET SDK / OPC UA reference server (`opc-ua-dotnet`) — the one toolchain piece
      never actually built or run during prep (no .NET SDK in this environment); flagged
      explicitly in `setup-guide.md`, not silently assumed to work.
- [ ] Presentation slide decks — not revisited since the brownfield pivot; likely still
      describe the old single-feature premise. Worth a pass before Day 1 if slides are
      shown alongside these materials.
