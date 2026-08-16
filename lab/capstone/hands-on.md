# Capstone Project

Not a module — the closing project. Take the spec your team set aside on Day 1
(Module 3), rewritten in Module 8, through the full lifecycle **for the first time**:
plan, tasks, checklist, analyze, implement — applying everything practiced on your
other increment across the week, now with deliberately less scaffolding than Modules
3–6 gave you. No numbered checkpoints below telling you what file to compare against;
that's the point.

## What "less guidance" means here, concretely

Every module through Day 2 paired your hands-on step with a checkpoint against a real,
pre-built reference. The Capstone doesn't, on purpose — by now your team has been
through constitution, spec, clarify, plan, tasks, checklist, analyze, implement, and
review once already, on your carried-forward increment. Run the same lifecycle on your
second increment using your own judgment about what "good" looks like, not a reference
file.

If you want a sanity check anyway: `../../brownfield-project/specs/001-opcua-threshold-alerting/`
is the instructor's own full lifecycle, start to finish, real code and real tests
included — not shaped like your spec, but the same *process* applied to completion.

## Documented review trail

One document, covering **both** increments (the one you carried through Modules 4–7,
and this one), referencing Modules 2–6's practices by name. Structure:

```markdown
# Review Trail: [Team Name]

## Increment 1 — [feature/defect name] (Modules 3-7)
- Discovery findings that shaped the constitution (Module 2)
- Clarify questions and answers (Module 3)
- Plan decisions corrected on review, and why (Module 4)
- Checklist/analyze findings, resolved (Module 5)
- What a human review caught that gates didn't, if anything (Module 6)

## Increment 2 — [the Capstone spec] (this week, less guidance)
- Same five headings, filled in for real, without a reference file to check against
- What was different about doing this the second time, with less scaffolding

## What we'd do differently next time
```

This mirrors how `checklist.md` and `analyze-report.md`'s real Findings 1 and 2 (Module
5) are written — not "we ran a checklist," but the specific thing it caught and how it
got fixed. A review trail that only says gates were run, without saying what they
found, isn't a review trail.

## Publish the review trail to Confluence

A review trail sitting only as a file in your repo is exactly the kind of documentation
Module 2 taught you to distrust by default — recall Q3/Q4 in `discovery-log.md`: things
that exist but aren't where anyone would think to look aren't meaningfully documented.
Close that loop on your own team's work. Using your **Atlassian MCP** connection (the
same one, write side, Module 4 used for the Jira sync), ask your agent to publish this
document as a new Confluence page under your team's space — a child page of whatever
your team's Module 2 architecture notes landed under, if you made one, so a teammate
starting from Confluence can actually find it via normal navigation, not just because
they already knew to look in the repo.

**Checkpoint**: open the page in a browser, not just the agent's confirmation. Does it
read like `confluence-content.md`'s real pages (concrete, specific, sourced) or like a
generic status update? The same bar Module 5 set for Findings — specific beats generic
— applies here too.

## Team presentation

Present your project's evolution from Day 1 through both increments — not just the
finished code. What changed between your Day 1 spec and your Module 8 rewrite, and why?
Where did automated gates catch something, and where did a human catch something gates
couldn't? What would your team's constitution look like different if you were starting
over today, knowing what you know now? Peer and instructor feedback follows, then
wrap-up.
