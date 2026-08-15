# Module 7 — Over-/Under-Specification Comparison

Same underlying need — escalate an alert nobody's acted on — written three ways, with what each one actually produces.

## Under-specified (`escalation-antipattern/spec-under-specified.md`)

One sentence, three undefined terms ("handled," "reasonable time," "escalated"). The implementation in `escalation-antipattern/output-from-under-specified.py` had to silently resolve every one of them:

- **`REASONABLE_TIME = timedelta(minutes=15)`** — a number nobody chose, now load-bearing.
- **Applies to every open alert**, not just critical ones — a scope decision nobody made, buried in a `.filter()` clause.
- **"Escalated" means overwriting `severity` to `"critical"`** — destroys the alert's original severity, and does it with a plain field assignment, no `AlertEvent` recorded. That's a direct, silent violation of constitution Principle V (every status transition recorded with actor/timestamp/prior-state) — not because anyone decided to skip auditability, but because nothing in the one-sentence spec ever raised the question.
- **No idempotency guard** — on a scheduled job, this re-"escalates" (re-commits a write to) the same stale alert on every tick, forever.

This is the same failure mode as Module 1's vibe-coding exhibits, one level up: an under-specified requirement doesn't fail to compile or fail a test — it just gets an answer, silently, from whoever implements it first. Multiplied across a team, "reasonable time" means something different in every engineer's head until someone actually asks.

## Over-specified (`escalation-antipattern/spec-over-specified.md`)

The opposite failure, and arguably the more expensive one because it *looks* rigorous. `escalation-antipattern/output-from-over-specified.py` implements it exactly as written, and in doing so:

- **Bypasses the ORM models** the rest of the codebase uses (`app/models.py`) in favor of raw SQL strings — breaking constitution Principle IV's API/architecture consistency, because the "spec" dictated table and column names directly instead of describing behavior.
- **Introduces an unvetted dependency** (APScheduler) and a new architecture pattern (background scheduler thread) that never went through `plan.md`'s research/rationale process — there's no `research.md` entry justifying "why APScheduler over an existing pattern," because the spec pre-empted the decision plan.md exists to make.
- **Directly contradicts this project's own spec.** `../../project/specs/001-equipment-health-monitoring/spec.md`'s Assumptions section already states: *"paging or external notification integrations... are explicitly out of scope for this feature and would need their own spec."* The over-specified version reintroduces exactly the scope this project already, deliberately, excluded — because whoever wrote it was solving the problem in plan-mode and writing it down as if it were a requirement, so nobody ever checked it against the actual spec's boundaries.

Over-specification isn't safer than under-specification. It just fails later and more expensively — usually in review, or worse, in production, once someone notices the paging integration nobody approved.

## Corrected (`escalation-antipattern/spec-corrected.md`)

States the trigger (30 minutes, critical-only), the effect (a visible, one-time, auditable state transition), and the boundary (no paging — inherited from this feature's existing Assumptions, not re-litigated) — and stops there. `plan.md` is where "background job vs. event-driven," "which library," and "how to extend the severity representation" actually get decided, with tradeoffs visible and reviewable on their own, instead of smuggled into a document that's supposed to be readable by a non-technical stakeholder.

## Takeaway

Both failure directions come from the same root cause: skipping the actual judgment call and letting either an implementer's first guess (under-specified) or a spec-writer's premature architecture decision (over-specified) fill the gap unreviewed. The corrected version isn't "more detail" or "less detail" — it's detail about the right thing (behavior and boundaries) and silence about the wrong thing (implementation), which is exactly the line Module 1's "avoid HOW, focus on WHAT and WHY" guidance draws, and exactly what a thin constitution or a skipped clarify pass tends to blur first.
