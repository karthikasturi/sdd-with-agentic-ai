# Discovery Prompt Template — Documentation/MCP-Assisted

Use this when your MCP connections (Atlassian, GitHub — `../../mcp-setup.md`) are live
and you have a real ticket to start from. This is Steps 1–3 of this module's hands-on,
written as one copy-pasteable prompt instead of three separate asks — paste it as-is
into your agent, filling in the bracketed placeholders first.

If you have **no** working documentation to lean on — no Jira, no wiki, nothing beyond
the code itself — use `discovery-prompt-zero-doc.md` instead. Don't run this one and
just skip the parts that don't apply; the zero-doc template asks fundamentally
different questions.

---

```
You are helping me understand an existing, large, real codebase before I write a spec
against it. Do not propose any implementation yet — this is discovery only.

## Context

- Codebase: EdgeX Foundry brownfield estate at [repo root, e.g. repos/edgex-go and
  repos/edgex-ui-go]
- My assignment: [paste your Jira ticket's Description field verbatim, or the matching
  paragraph from assignment-pool.md if Jira isn't live yet — feature or defect, one at
  a time]
- Jira project key: [your project key] — Confluence space key: [your space key]

## What I need you to find, in order

1. **Does something like this already exist?** Search the codebase (not just names that
   sound related — read enough to be sure) for existing functionality that overlaps
   with what I'm about to ask for. Don't assume the absence of an obvious name means
   the capability doesn't exist under a different one.

2. **What does the real API/data contract already say?** If there's an OpenAPI spec,
   proto file, or equivalent for the area this touches, read it directly — don't infer
   the contract from a UI screen or a doc's prose summary alone.

3. **Search Jira project `[your project key]`** for anything else labeled with my
   assignment's tag (`pair-N`) or mentioning the same service/component. Then,
   optionally, cross-reference the original upstream GitHub issue for the deeper
   history — a Jira ticket here deliberately only states the symptom, not the root
   cause, the way a real bug report usually does.

4. **Search Confluence space `[your space key]`** for any architecture or "how this
   area works" page relevant to what I'm touching.

## For every finding, tell me:

- **What you found**, with a real citation (a specific file path and, where relevant,
  a line/function name — or a specific Jira/Confluence page/issue ID). Never state a
  finding without saying where it came from.
- **How confident you are**, and *why* — "I read the actual handler function" is a
  different confidence level than "I inferred this from a variable name." Say which one
  it is.
- **How you found it** — official doc, README, source code you had to read yourself, an
  MCP query. This matters as much as the answer: I want to know which questions were
  fast lookups and which needed real digging, not just the final answers.

## Before you finish

List anything you searched for and could **not** find an answer to, explicitly — an
honest "I don't know, here's what I tried" is more useful to me than a plausible-
sounding guess presented with the same confidence as something you actually verified.
```

---

**After running this**: capture the results in `service-map-template.md` (Step 4) —
this prompt's output is raw material, not the deliverable itself. Compare your process
against `discovery-log.md` if you want to see what a full, real run of this same
methodology produced for Pair 1.
