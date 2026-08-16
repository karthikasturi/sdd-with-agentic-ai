# Spec-Driven Development Package — Demo & Presenter Material

**This folder is the presenter/demo side of the course.** Hands-on participant material
lives in the sibling `../lab/` folder — setup guides, tool reference, every module's
Hands-on section, and the Capstone's formal requirements all migrated there. Every
module below now contains its Demo talk track only, cross-referencing `../lab/` for the
exhibit files and reference artifacts it walks through.

## Structure

```
demo/
  README.md          this file
  review-trail.html  10-slide presenter walkthrough
  modules/
    01-vibe-coding-vs-spec-driven/             team formation, both frameworks scaffolded, vibe-coding exhibit
    02-discovery-at-scale/                     MCP-style discovery, service/dependency map
    03-governance-and-clarified-spec/          constitution + two specs (feature + defect) + clarify
    04-from-clarified-spec-to-reviewable-plan/ plan review + task decomposition
    05-quality-gates-before-implementation/    checklist + analyze + security/coverage + real implementation
    06-reviewing-validating-maintaining/       instructor-provided flawed-change review
    07-multi-agent-workflows-and-team-adoption/  real, verified delegation
    08-common-pitfalls-and-anti-patterns/      escalation-antipattern exhibit
    (capstone/ has moved — see ../lab/capstone/)

../lab/               participant-facing hands-on material: setup-guide.md, mcp-setup.md,
                       tool-reference.md, modules/01-08/README.md (Hands-on sections +
                       exhibit files), capstone/ (requirements.md + hands-on.md)
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
- [x] `../lab/setup-guide.md` and `../lab/mcp-setup.md` — Day-0 environment and MCP
      setup, now living in `lab/` alongside the rest of the hands-on material.
- [x] Hands-on/demo-talk-track split for Modules 1–8 and the Capstone — complete;
      every cross-reference (76 across the repo) verified to resolve after the move.
- [ ] Real GitHub forks for the submodules (currently local branches only) — needed only
      if this goes out to participants who need to push their own commits; not required
      for instructor-led delivery from this machine.
- [ ] .NET SDK / OPC UA reference server (`opc-ua-dotnet`) — the one toolchain piece
      never actually built or run during prep (no .NET SDK in this environment); flagged
      explicitly in `setup-guide.md`, not silently assumed to work.
- [ ] Presentation slide decks — not revisited since the brownfield pivot; likely still
      describe the old single-feature premise. Worth a pass before Day 1 if slides are
      shown alongside these materials.
