# Spec-Driven Development Package — Day 1 Ready

**Day 1 (Modules 1–3) is complete and real.** Days 2–3 (Modules 4–8) are the next pass —
see `legacy-python-poc/SUPERSEDED.md` for the original build this replaces, and the
plan history for what's deferred and why.

## Structure

```
demo/
  README.md                    this file
  tool-reference.md            GitHub Copilot ↔ Claude Code command mapping (Spec Kit + OpenSpec)
  modules/
    01-vibe-coding-vs-spec-driven/   team formation, both frameworks scaffolded, vibe-coding exhibit
    02-discovery-at-scale/           MCP-style discovery, service/dependency map
    03-governance-and-clarified-spec/  constitution + two specs (feature + defect) + clarify
    04-08/                        not yet built — Day 2/3
  legacy-python-poc/            the original single-feature Python version, archived
```

The reference codebase lives in the separate `../brownfield-project/` repo (EdgeX
Foundry [Go] + edgex-ui-go [Angular] + OPC UA .NET Standard [C#]) — real, currently
maintained open source, not synthetic. `../brownfield-project/assignment-pool.md` has
the 6 real feature+defect pairs teams draw from starting Module 1; Pair 1 (OPC UA
Threshold Alerting + `device-opc-ua#53`) is fully worked end to end and doubles as the
instructor's reference throughout.

## How Day 1 actually flows

1. **Module 1**: teams form, claim a pair from the assignment pool, scaffold both Spec
   Kit and OpenSpec side by side, then see ad hoc prompting fail on a self-contained
   exhibit (Go, real, runs).
2. **Module 2**: teams orient in their pair's actual codebase area — real documentation
   quality varies (well-documented core, undocumented internals), real GitHub issue
   history for precedent — and produce a one-page service/dependency map.
3. **Module 3**: teams write a constitution from that map, spec *and clarify* both
   halves of their pair (feature + defect), then choose one to carry forward. The other
   is set aside for Module 8 and the Capstone.

Every checkpoint in Modules 1–3 points at something real: a working Go implementation
with real tests, real git history showing a corrected mistake, real GitHub issues, a
real OpenSpec scaffold actually run during prep — not staged output.

## Status

- [x] Modules 1–3, assignment pool, Tool Reference handout, defect-side worked spec.
- [ ] Modules 4–8 guides.
- [ ] Teaching exhibits for Modules 5–7 (flawed-change, escalation-antipattern, delegation-transcript).
- [ ] `review-trail.html` rebuild.
- [ ] Angular acknowledge-button code (`repos/edgex-ui-go`, in progress, uncommitted) — Module 5-era, not blocking Day 1.
