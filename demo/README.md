# Spec-Driven Development Package — Days 1–2 Ready

**Days 1–2 (Modules 1–6) are complete and real.** Day 3 (Modules 7–8) is the next pass.
The original from-scratch Python/FastAPI version this replaced has been removed
(fully superseded, recoverable from git history if ever needed).

## Structure

```
demo/
  README.md                    this file
  tool-reference.md            GitHub Copilot ↔ Claude Code command mapping (Spec Kit + OpenSpec)
  modules/
    01-vibe-coding-vs-spec-driven/            team formation, both frameworks scaffolded, vibe-coding exhibit
    02-discovery-at-scale/                    MCP-style discovery, service/dependency map
    03-governance-and-clarified-spec/         constitution + two specs (feature + defect) + clarify
    04-from-clarified-spec-to-reviewable-plan/  plan review + task decomposition
    05-quality-gates-before-implementation/   checklist + analyze + security/coverage + real implementation
    06-reviewing-validating-maintaining/      instructor-provided flawed-change review
    07-08/                                    not yet built — Day 3
```

The reference codebase lives in the separate `../brownfield-project/` repo (EdgeX
Foundry [Go] + edgex-ui-go [Angular] + OPC UA .NET Standard [C#]) — real, currently
maintained open source, not synthetic. `../brownfield-project/assignment-pool.md` has
the 6 real feature+defect pairs teams draw from starting Module 1; Pair 1 (OPC UA
Threshold Alerting + `device-opc-ua#53`) is fully worked end to end and doubles as the
instructor's reference throughout.

## How Days 1–2 actually flow

1. **Module 1**: teams form, claim a pair from the assignment pool, scaffold both Spec
   Kit and OpenSpec side by side, then see ad hoc prompting fail on a self-contained
   exhibit (Go, real, runs).
2. **Module 2**: teams orient in their pair's actual codebase area — real documentation
   quality varies (well-documented core, undocumented internals), real GitHub issue
   history for precedent — and produce a one-page service/dependency map.
3. **Module 3**: teams write a constitution from that map, spec *and clarify* both
   halves of their pair (feature + defect), then choose one to carry forward. The other
   is set aside for Module 8 and the Capstone.
4. **Module 4**: plan the carried-forward spec, correct a real architecture decision
   (a genuine, git-committed correction, not staged), decompose into tasks.
5. **Module 5**: checklist and analyze both catch real findings (one from the original
   pass, one added specifically for this module — a missing security statement);
   add a security/coverage checklist item, verified with a real `go test -cover` number
   against this repo's own existing baseline; implement one task end-to-end for real.
6. **Module 6**: review an instructor-provided flawed change that's genuinely green
   (9/9 tests) and genuinely wrong — a real Go footgun (an untyped constant silently
   meaning nanoseconds, not minutes) that no automated gate could have caught, then
   apply the same lens to your own Module 5 work.

Every checkpoint points at something real: working Go implementations with real tests,
real git history showing corrected mistakes, real GitHub issues, a real OpenSpec
scaffold actually run during prep — not staged output.

## Status

- [x] Modules 1–6, assignment pool, Tool Reference handout, defect-side worked spec,
      flawed-change exhibit.
- [ ] Modules 7–8 guides (Day 3).
- [ ] Teaching exhibits for Module 8 (escalation-antipattern), delegation-transcript for Module 7.
- [ ] `review-trail.html` rebuild.
- [ ] Angular acknowledge-button code (`repos/edgex-ui-go`, in progress, uncommitted) —
      not blocking Days 1–2's checkpoints, since Module 5's "implement one task
      end-to-end" checkpoint is satisfied by the Go side alone.
