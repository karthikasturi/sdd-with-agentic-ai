# Module 7 — Multi-Agent Workflows & Team Adoption (Demo)

Covers: coordinating multiple agents/subagents across a task graph; repository
conventions linking specs to issues and pull requests; governance — reviewing agent
actions, permissions, audit trails.

Participant hands-on material for this module: `../../../lab/modules/07-multi-agent-workflows-and-team-adoption/README.md`.
This file is the presenter-facing talk track only.

## Demo talk track (5–6 minutes)

**Live vs. pre-built**: Step 1's scoping discussion is fine live. Step 3 should walk
from the real transcript — the specific gap it documents (a code comment that never made
it into a summary) is the point, not "a" gap a fresh delegation might or might not
produce.

1. Open `../../../brownfield-project/delegation-transcript.md`'s "What came back" list,
   then run the real verification commands live (`go test`, `ng test`) — *"Not 'the
   agent said it works.' A number, from a real test run, that anyone reviewing this
   could reproduce themselves."*

2. Walk the three self-reported judgment calls — *"Good delegated work flags its own
   uncertainty. This is what that looks like: specific, each one independently
   reviewable, not a blanket 'let me know if anything looks off.'"*

3. Close on the TOCTOU race. *"The delegated agent did genuinely good, disciplined
   work — three flagged judgment calls, 5/5 real passing tests, and it even wrote down
   the exact right reasoning about this race condition, in a comment, unprompted. It
   just never told anyone at review time. Delegation changes who writes the code. It
   doesn't change who's responsible for asking what a passing test suite doesn't prove —
   and it doesn't automatically surface what the delegate already knew but didn't say
   out loud."*
