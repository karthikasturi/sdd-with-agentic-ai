# The CODERS Framework — A Layered Prompt Structure for Code Generation

CO-STAR (Context, Objective, Style, Tone, Audience, Response format) is a well-known
layered prompt framework — but it was built for *content* writing. Half its layers
don't transfer: code doesn't have a "Tone," and "Audience" means something different
when the reader is a compiler and a code reviewer, not a person. What actually breaks a
code-generation prompt is a different set of gaps — and this course already has two
real, verified exhibits that show exactly which ones (see "Worked example," below).

**CODERS** is that same layered idea, rebuilt for code generation specifically:

| Layer | Question it forces you to answer | What happens when it's missing |
|---|---|---|
| **C**ontext | What already exists nearby — a service, a module, a convention — that this needs to fit next to, reuse, or avoid duplicating? | The agent builds a plausible parallel version of something that already exists. Not a wording problem — no amount of care elsewhere in the prompt fixes this one. |
| **O**bjective | What's the one concrete, testable behavior being asked for — stated as an outcome, not a verb? | The agent picks a plausible-sounding interpretation and commits to it silently (a global threshold instead of per-type, because "raise an alert if something looks wrong" never said which). |
| **D**one | What specific inputs/scenarios prove this works — including the edge cases and the negative cases? | Code that looks right and passes a shallow smoke test while being genuinely broken (a status-code check that never notices an acknowledgment silently failed to persist). |
| **E**xclusions | What must the agent explicitly *not* add, touch, or infer? | Uninvited scope: a paging integration nobody asked for, a "helpful" refactor of surrounding code, a new dependency. |
| **R**euse | Which existing conventions, patterns, or utilities in *this* codebase should new code extend rather than reinvent? | Idiomatic-looking code that ignores the codebase's own patterns — technically fine in isolation, a real review burden in context. (Not applicable to a from-scratch greenfield ask — critical for anything brownfield.) |
| **S**hape | What should the output actually look like — how many files, what structure, tests included or not? | One undifferentiated file with no separation between concerns, nothing a reviewer could approve or reject piece by piece. |

## Core-4 vs. full CODERS

Not every prompt needs all six layers spelled out. Use **C-O-D-E** (Context,
Objective, Done, Exclusions) as the minimum bar for *any* code-generation prompt —
these four are the ones whose absence causes silent, hard-to-catch failures. Add
**R** and **S** once the ask is big enough that structure and codebase conventions
actually matter — anything touching more than a trivial, single-function change,
and essentially everything in a brownfield codebase.

## Worked example — this course's own exhibits, re-read through CODERS

`vibe-coding-exhibit/PROMPT.md` and `PROMPT-ADVANCED.md` (Module 1) are real,
unedited, both verified to build and run. Read against CODERS, the difference between
them — and the one gap *neither* closes — becomes precise instead of just "the second
one is better":

| Layer | `PROMPT.md` (naive) | `PROMPT-ADVANCED.md` (better) |
|---|---|---|
| Context | Absent | **Still absent** |
| Objective | Vague ("if something looks wrong") | Present (per-resource thresholds, explicit rejection rules) |
| Done | Absent | Partial (acknowledge-once specified; recurring-alert dedup still unasked) |
| Exclusions | Absent | Present ("don't add any external integrations I didn't ask for") |
| Reuse | N/A (greenfield exhibit) | N/A (greenfield exhibit) |
| Shape | Absent | Present ("structure the code across a few files") |

Four layers explain four of `NOTES.md`'s real findings directly: no Exclusions →
`notifyPager`'s uninvited call; no Shape → the unreviewable one-file diff; no Done →
the acknowledge-bug a status-code-only smoke test misses; vague Objective → the
hardcoded global threshold.

**The one row that doesn't improve between the two prompts is the interesting one.**
Context is absent in *both* — and no amount of care in the other five layers fixes
that, because nothing in either prompt ever pointed the agent at the fact that this
course's real codebase (EdgeX Foundry) already ships `support-notifications`, built to
do exactly this job. That's `NOTES.md`'s own conclusion, independently reached: "that's
not a prompt-wording problem... that's what Module 2 (Discovery at Scale) exists to
fix." CODERS' Context layer is a formal name for the thing this course already
identified as the one gap a well-written prompt structurally can't close on its own —
it can remind you to *ask* the question, but answering it needs a real discovery pass,
not better wording.

## Template — copy this, fill every layer in before sending the prompt

```
## Context
[What exists nearby that this needs to fit next to, extend, or avoid duplicating?
Name the specific service/module/file if you know it — if you don't know, that's a
signal to run a discovery pass first, not to leave this blank.]

## Objective
[The one concrete, testable behavior wanted. State it as an outcome: "reject a
reading for equipment that isn't registered, with an explicit error" — not "handle
invalid readings properly."]

## Done
[The specific scenarios that prove this works, including at least one edge case and
one negative case. If you can't name a test case for it, you probably can't verify
the agent got it right either.]

## Exclusions
[What must NOT be added, touched, or inferred? Be explicit even about things that
seem obvious — "no new external integrations," "don't modify files outside X," "no
new dependencies without asking."]

## Reuse (skip if genuinely greenfield)
[Existing conventions/patterns/utilities in this codebase that new code should
extend, not reinvent.]

## Shape
[Expected output structure: how many files, where they go, tests included, format
of the response.]
```

## Where this sits relative to Spec-Driven Development

CODERS is not a competing practice — it's one rung of rigor *below* a full spec, for
the asks that don't warrant the full SDD lifecycle: a single function, a small
self-contained fix, something you'd genuinely finish in one prompt either way. The
moment an ask needs more than one prompt, touches more than one file with real
interdependencies, or the answer to Context is "I'm not sure" rather than a specific
citation — that's the signal to run a real discovery pass (Module 2) and write a spec
(Module 3), not to keep adding CODERS layers to compensate. A spec is what CODERS
looks like once every layer gets the full rigor treatment: Context becomes a service
map, Objective becomes EARS-format requirements, Done becomes a checklist and
acceptance criteria, Exclusions becomes the spec's own explicit non-goals section.

**Natural next step, not yet built out**: once a CODERS prompt gets reused more than
once or twice, it's a candidate for turning into a real Agent Skill (`SKILL.md`) so
Copilot invokes it automatically instead of it being retyped each time — see
`../tool-reference.md`'s "Customization file locations" section for where skills live.
