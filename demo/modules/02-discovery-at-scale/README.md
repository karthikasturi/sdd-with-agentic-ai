# Module 2 — Discovery at Scale (Demo)

Covers: orienting an AI coding agent in a large, existing, unevenly-documented codebase
— connecting it to source, existing docs, and the bug/defect tracker — *before* writing
a spec against it.

Participant hands-on material for this module: `../../../lab/modules/02-discovery-at-scale/README.md`.
This file is the presenter-facing talk track only.

## Demo talk track (5–6 minutes)

**Live vs. pre-built**: Steps 1–2 are reasonable to run genuinely live if you have time
to spare — the point being made (fast doc lookup vs. slow code-reading vs. false
confidence) comes through with real-time agent output, whatever it happens to say, as
long as you're ready to react to what it actually returns rather than a scripted line.
Step 3's specific issues are worth walking from `../../../brownfield-project/discovery-log.md`
directly — the value is in *these two real issues*, not "an agent found some issues,"
and a live search might not surface them from a differently-worded query.

1. Open `repos/edgex-go/openapi/support-notifications.yaml` next to
   `../../../brownfield-project/discovery-log.md` Q1 — "this one's fast, this is what
   good documentation buys you."

2. Open `repos/edgex-ui-go/web/src/app/notifications/notifications.component.ts` —
   nearly empty — then, before saying anything, open the sibling
   `notification/notification-list/notification-list.component.ts` and scroll through
   its 300 real lines. "Stop reading after the first file and you'd report this feature
   doesn't exist. It does — one directory over." Then open
   `../../../brownfield-project/specs/001-opcua-threshold-alerting/spec.md`'s User
   Story 2 and show the corrected paragraph: *this project's own first draft made
   exactly that mistake, in a real, git-committed spec, before it got caught and fixed.*

3. Open `discovery-log.md` Q3 — the acknowledge-endpoint behavior — and walk through why
   it's the hardest kind of finding: not wrong documentation, no documentation, at all,
   on that specific point. Point at the OpenAPI spec's response codes (200/400/500, no
   409) as "a negative fact — the absence of a 409 response is itself the discovery,
   and you only notice an absence if you know to look for it."

4. Close on `discovery-log.md` Q5 — open the two real GitHub issues live in a browser.
   Quote: *"Neither of these blocks anything. That's not the point. The point is a spec
   written without five minutes of searching the tracker has no way to know they
   happened — and 'this exact service already had an OOM report on exactly this kind of
   workload' is not a fact you want to discover after implementation."*

5. Open `../../../lab/modules/02-discovery-at-scale/service-map-example.md` — one page,
   three services, one real defect with its real (not filed-against) root cause
   identified. "This is the entire output of this module. Not a document about the
   codebase — a map of exactly the corner of it your team is about to touch, and
   nothing else. Module 3 starts from this, not from a blank page."
