# Module 5 — Quality Gates Before Implementation (Demo)

Covers: generating and running a requirements checklist; the analyze cross-artifact
consistency pass; token/cost budgeting; and where security, compliance, and
code-coverage checks fit as additional gates.

Participant hands-on material for this module: `../../../lab/modules/05-quality-gates-before-implementation/README.md`.
This file is the presenter-facing talk track only.

## Demo talk track (6–7 minutes)

1. Open `../../../brownfield-project/specs/001-opcua-threshold-alerting/checklist.md`,
   scroll to Finding 1 — spec never said what happens when the same condition keeps
   recurring; show the fix, FR-015. *"Unit test suite for requirements — run against
   the spec, not the code."*

2. Open `../../../brownfield-project/specs/001-opcua-threshold-alerting/analyze-report.md`'s
   F1 finding, then the same directory's `plan.md` Decision 2 it caused. *"Checklist audits the spec against
   itself. Analyze audits spec, plan, and tasks against each other and against the
   constitution. Different failure classes, different gate."*

3. Open Finding 2 (in `checklist.md`) — the security gap, added specifically for this
   module. Read the note about the code comment that already had the right answer.
   *"The right answer existing somewhere is not the same as the right answer being
   reviewable before the code exists. That's what this whole module is actually for."*

4. Run `go test ./internal/threshold/... -cover` live (from
   `../../../brownfield-project/repos/device-opc-ua`), point at 94.3% next to
   `internal/driver`'s 38.4% in the same terminal. *"Not 'we wrote tests' — a number,
   next to this exact repo's own existing bar, checked the same way a reviewer would
   check it."*

5. Run `golangci-lint run ./internal/threshold/... ./internal/driver/...` live in the
   same terminal — 0 issues, `gosec` (security linter) included because it's already
   enabled in this repo's own `.golangci.yml`, not a rule this course invented. Then
   open CHK019 in `checklist.md` and run `npm run lint` in `edgex-ui-go/web` to show it
   fail for real — *"the Angular side of this exact feature shipped without a working
   lint gate, because the repo's own gate was never configured. We don't paper over
   that with a fake pass — we write it down. That's what CHK019 is."* If your org runs
   SonarQube/SonarCloud, `edgex-go`'s real `.sonarcloud.properties` is worth pointing at
   here too — same gate role, different tool, whichever your assigned repo actually has.
