# Spec-Driven Development Package — Demo + Actual Training

**Status: rebuild in progress.** This package is being rebuilt against a real brownfield
reference base (`../brownfield-project/`) instead of the original from-scratch Python toy.
See `legacy-python-poc/SUPERSEDED.md` for what changed and why.

## What will live here (per the approved rebuild plan)

```
demo/
  README.md                    this file — full package overview, rewritten last
  review-trail.html            interactive walkthrough, rebuilt against the new modules
  modules/
    01-vibe-coding-vs-spec-driven/
    02-discovery-at-scale/            NEW — not in the original 7
    03-governance-and-clarified-spec/
    04-plan-and-tasks/
    05-quality-gates/
    06-review-and-maintain/
    07-multi-agent-delegation/
    08-anti-patterns/
  legacy-python-poc/            the original version, archived intact — see SUPERSEDED.md
```

The reference project itself now lives in the separate `brownfield-project/` repo
(EdgeX Foundry [Go] + edgex-ui-go [Angular] + OPC UA .NET Standard [C#]), not inside
`demo/`, since it's meant to read like a real product's source, not course collateral.

## Build order

1. Reference implementation in `brownfield-project/` (constitution, spec, plan, tasks,
   checklist, analyze, one implemented user story) — **in progress**.
2. The 8 module guides above, each checkpointed against artifacts from step 1.
3. Teaching exhibits (vibe-coding exhibit, flawed-change review, escalation anti-pattern
   trio, delegation transcript).
4. `review-trail.html`, last, once the content above is stable.

Full package overview (the equivalent of the original `demo/README.md`) gets rewritten
once modules 1–8 exist.
