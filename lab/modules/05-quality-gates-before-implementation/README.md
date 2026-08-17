# Module 5 — Quality Gates Before Implementation

Covers: generating and running a requirements checklist (a "unit test suite for
requirements"); the analyze cross-artifact consistency pass; budgeting agent token/cost
usage across a plan; and where security, compliance, and code-coverage checks fit as
additional gates — before any implementation code exists.

`../../../brownfield-project/specs/001-opcua-threshold-alerting/checklist.md` and
`analyze-report.md` carry **two** real findings each caught something genuine: one from
the original pass (a missing requirement), one added on Day 2 specifically for this
module (a missing security statement). Both were fixed in the actual artifacts, not
just noted and left broken.

## Hands-on

### Step 1 — Generate and run a checklist

Run your checklist step (`/speckit.checklist` — see `../../tool-reference.md`) against
your spec. Read every item — don't just check the
boxes that auto-passed.

**Checkpoint**: `checklist.md` has one item that failed on first pass — CHK004,
duplicate-alert suppression, resolved by adding FR-015 directly to `spec.md`. Did your
checklist surface anything comparable? If it came back all-green on the first try, look
harder at CHK004's category (alert/notification lifecycle: "what happens when the
condition keeps recurring?") — it's a real gap, not manufactured for this exercise.

### Step 2 — Run analyze

Run your cross-artifact consistency check (`/speckit.analyze`) across spec, plan, and
tasks.

**Checkpoint**: `analyze-report.md` documents a real HIGH-severity finding (F1) about a
plan that assumed a shared platform endpoint enforced something it doesn't — confirmed
by reading that endpoint's actual source and its own OpenAPI contract, not guessed.
Resolve your own findings the same way: fix the artifact, don't just note it and move on.

### Step 3 — Add a security/compliance or code-coverage checklist item

Add at least one checklist item that specifically checks a security, compliance, or
code-coverage concern — not just functional correctness.

**Checkpoint**: `checklist.md`'s "Security, Compliance & Code Coverage" section (added
Day 2, after the original pass) has four. CHK016 asks whether the plan states its new
HTTP boundaries' auth posture — it originally **failed**, for real; see Finding 2 and
the "Security & Auth Path" section it caused to be added to `plan.md`. CHK017 asks
whether new code's test coverage holds up against this repo's existing baseline —
verified with a real command, not asserted: `go test ./internal/threshold/... -cover`
returns 94.3%, against the pre-existing `internal/driver` package's 38.4% in the same
repo. CHK018 asks whether new/changed code passes the *repository's own* configured
static-analysis gate — verified: `golangci-lint run ./internal/threshold/...
./internal/driver/...` (this repo's real `.golangci.yml`, `gosec` enabled), 0 issues.
CHK019 is the honest counterpart: when a repo's own gate for a different toolchain
doesn't actually run — `edgex-ui-go`'s `npm run lint` fails outright, no ESLint
schematic configured upstream — that gets written down, not silently skipped.

Run the equivalent commands yourself against your own new code before checking any of
these off — for Go code, whichever repo your pair touches:
```
cd ../../../brownfield-project/repos/<your-repo>
go test ./... -cover
golangci-lint run ./...   # install: go install github.com/golangci/golangci-lint/v2/cmd/golangci-lint@latest
```
If your repo has its own `.golangci.yml` or `.sonarcloud.properties`, use its actual
configured rules, not a generic default — the point of CHK018 is "passes *this
repository's* bar," the same brownfield-conformance principle Module 4's plan-review
step applies to architecture decisions. If your repo's linter isn't configured at all
(check for `.golangci.yml`; Angular repos need `@angular-eslint/schematics` installed
before `ng lint` works), that's a CHK019, not a blocker — write it down and move on. A
coverage or lint claim nobody actually ran is not a checked item.

### Step 4 — Implement one task end-to-end, only after every gate clears

Pick one task from `tasks.md` that clears all the gates above, and implement it for
real — test first, watch it fail, then make it pass.

**Checkpoint**: `../../../brownfield-project/repos/device-opc-ua/internal/threshold/`
has exactly this: `evaluator.go` and `evaluator_test.go`, real Go, real tests (8 of
them), covering the critical-immediate path, the warning-debounce path, the
unconfigured-resource path, the invalid-reading path, and the duplicate-suppression
path — one per relevant FR. Run them:

```
cd ../../../brownfield-project/repos/device-opc-ua
go test ./internal/threshold/... -v
```

## Token & cost budgeting

Every gate above costs real tokens and real time before a single line of production
code exists. The honest case for that cost isn't abstract — it's sitting in this
feature's own artifacts: Finding 1 (checklist) and Finding 2 (analyze, this module) each
took a few minutes and a short paragraph to catch and fix *before* implementation.
Finding 1's gap, uncaught, would have shipped a Notification-flooding bug discoverable
only under sustained load — the exact shape of failure `device-opc-ua#53` (Module 2)
already showed this platform has paid for once for real. Finding 2's gap, uncaught,
would have shipped with no reviewable statement of its own auth posture, discoverable
only by an auditor or an incident, not a reviewer. Budget checklist and analyze passes
as a fixed, small cost per feature — the alternative isn't zero cost, it's the same cost
paid later, at a worse time, by someone with less context than the person who just wrote
the plan.

See `../../../demo/modules/05-quality-gates-before-implementation/README.md` for this
module's presenter/demo talk track — not needed to complete the hands-on above.
