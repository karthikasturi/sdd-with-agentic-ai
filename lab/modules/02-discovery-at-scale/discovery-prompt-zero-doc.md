# Discovery Prompt Template — Zero Documentation, Code Only

Use this when there is genuinely **nothing** to lean on beyond the source itself — no
working Jira, no wiki, no README you trust, nothing. This is the harder, more realistic
case for most of a large brownfield estate's corners (Module 2 Step 2 names this
directly), and it asks fundamentally different questions than
`discovery-prompt-doc-assisted.md`: not "what does the documentation say," but "what
can I *prove* from the code alone, and what am I only guessing at."

The deliverable this prompt produces — a **Service Boundary Card** — is meant to be
**kept**, not thrown away after this module. The whole point of doing this work once,
carefully, is that nobody on your team (or a future team touching this area) should
have to re-derive it from scratch. Save the output as
`service-boundary-card-[service-name].md` next to your `service-map.md`.

---

```
You are reverse-engineering the real structure of a service/component in a large
codebase, using ONLY the source code — no README, no doc comment, no wiki page, no
existing architecture diagram is authoritative here, even if one exists. If you read a
doc or comment, treat what it claims as an unverified hypothesis, not a fact, until
you've confirmed it against actual code behavior. Do not propose any implementation —
this is discovery only.

## Scope

Service/component under analysis: [e.g. repos/device-modbus-go, or a single cmd/
binary within repos/edgex-go like cmd/core-command, or a single Angular feature
directory like edgex-ui-go/web/src/app/notifications/]

## Step 1 — Establish the actual boundary first

Before anything else, tell me: what is the real unit of deployment/ownership here — a
single binary, a single package, a single Angular module? In a monorepo, this is not
obvious from directory structure alone. Confirm by checking what actually gets built/
deployed as one artifact (a Dockerfile, a main.go / cmd entry point, an angular.json
project entry) — not by assuming a top-level folder equals a service boundary.

## Step 2 — Real inbound surface (how anything else reaches this)

Find the actual entry points, verified in code, not inferred from naming:
- HTTP routes actually registered (grep for router/mux registration calls, not just
  handler function names — a handler that exists but is never wired to a route is not
  a real entry point).
- Message-bus topics actually subscribed to.
- Exported functions/types that code **outside** this boundary actually imports and
  calls — check real importers with a repo-wide search, don't assume an exported name
  is used just because it's exported.

## Step 3 — Real outbound dependencies

What does this boundary actually call out to — other internal services (HTTP client
calls, not just config that *could* point somewhere), a database, a message bus, other
packages in this repo? For each one, cite the actual call site, not a config file that
merely suggests the possibility.

## Step 4 — Data this boundary owns

What entity/data structure is this the real system of record for — defined, persisted,
and mutated here, not just passed through? If two areas both seem to touch the same
entity, say so explicitly rather than picking one arbitrarily; that ambiguity is itself
a finding.

## Step 5 — Boundary violations (a real finding, not noise)

Flag anything that crosses the boundary you established in Step 1 in a way that looks
wrong — e.g. code here directly importing another service's `internal/` package (a real
smell in Go, since `internal/` exists specifically to prevent that), or a component
reaching past its own service layer straight into another feature's internals. Don't
silently normalize this as "just how the codebase is" — name it.

## For every claim in every step:

- **Cite the exact file, and a line number or function/type name** — never state a
  structural fact about this codebase without one.
- **Separate "verified in code" from "inferred/assumed"** explicitly — if you couldn't
  confirm something (e.g. whether a config value is ever actually set to enable a code
  path), say that plainly rather than presenting a guess as settled.
- **Note what you deliberately did NOT check** and why — this card should tell a future
  reader where the edges of this discovery pass were, not just what's inside them.
```

---

**Output shape** — turn the prompt's findings into this card:

```markdown
# Service Boundary Card — [service/component name]

**Deployment unit**: (what's actually one build/deploy artifact, and how you confirmed it)

## Inbound surface (verified)
| Entry point | Type (HTTP route / topic / exported call) | Citation |
|---|---|---|

## Outbound dependencies (verified)
| Depends on | How (HTTP client / DB / message bus / internal import) | Citation |
|---|---|---|

## Data owned
(entity/struct, where it's defined, where it's persisted)

## Boundary violations found
(or "none found" — an explicit negative is still a finding)

## Verified vs. assumed
- Verified in code:
- Assumed / could not confirm:

## Not checked
(explicitly out of scope for this pass — save the next person from assuming this card is exhaustive)
```

Feed this card's "Data owned" and "Outbound dependencies" rows straight into your
`service-map-template.md` (Step 4) — the card is the evidence, the service map is the
one-page summary your team carries into Module 3.
