# Module 7 — Common Pitfalls & Anti-Patterns

Covers: over-specifying vs. under-specifying, why a thin constitution or a skipped clarify pass usually shows up here first, token/cost tradeoffs, and case studies.

## Hands-on

### Step 1 — Critique two flawed specs

Open `escalation-antipattern/spec-under-specified.md` and `spec-over-specified.md`. Both describe the same small feature (alert escalation). Before reading `output-from-*.py` or `comparison.md`, write down what you think will go wrong with each one, specifically — not "it's vague" or "it's too detailed," but what an implementer would actually be forced to invent, or what an over-specified version would actually lock in prematurely.

**Checkpoint**: Compare your predictions against `comparison.md`. Pay attention to the over-specified example's specific failure: it accidentally re-introduces an external paging integration that `../../project/specs/001-equipment-health-monitoring/spec.md` already ruled out of scope — a concrete example of why "more detail" isn't automatically safer than "less detail."

### Step 2 — Rewrite and compare

Look at `escalation-antipattern/spec-corrected.md`. Rewrite one of the two flawed versions yourself, in your own words, before reading it — then compare. What did you include that the corrected version left out (or vice versa)?

## Demo talk track (sales / technical evaluation call)

**Suggested time**: 3–4 minutes.

Open `escalation-antipattern/`. Show `spec-under-specified.md` next to `output-from-under-specified.py` — point at the arbitrary `REASONABLE_TIME = timedelta(minutes=15)` and the missing audit trail.

Then `spec-over-specified.md` next to `output-from-over-specified.py` — point at the `requests.post(...)` call to a paging endpoint, and flip to `../../project/specs/001-equipment-health-monitoring/spec.md`'s Assumptions section, which already explicitly ruled that integration out of scope.

*"Same underlying feature. One spec was too thin and let an implementer's first guess become the requirement. The other was too thick and smuggled an unreviewed architecture decision — and a scope violation — into a document that's supposed to be reviewable by a non-technical stakeholder. Neither direction is safe by default."*
