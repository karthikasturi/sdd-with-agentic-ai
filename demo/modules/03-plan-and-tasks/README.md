# Module 3 — From Clarified Spec to Reviewable Plan

Covers: translating a clarified spec into a technical plan, using a plan/preview mode before any file changes, and task decomposition.

## Hands-on

### Step 1 — Generate a plan

Run your plan-generation step (e.g. `/speckit-plan`) against your Module 2 spec. Review it **line by line before accepting it** — the outline's instruction here is not decorative; Step 2 depends on you actually reading it.

**Checkpoint**: You should have `plan.md`, `research.md`, `data-model.md`, `quickstart.md`, and `contracts/api.md`. Compare structure against `../../project/specs/001-equipment-health-monitoring/`.

### Step 2 — Edit the plan to correct a decision

Look specifically at how your plan decided to store threshold configuration. Ask: if a threshold value turns out to be wrong six months from now, who has to act, and what do they need to do?

Edit your plan to fix whatever you find objectionable — don't just accept the first draft. Write down *why* you changed it, in the plan itself.

**Checkpoint**: Read `../../project/specs/001-equipment-health-monitoring/plan.md`'s "Plan Review Note" section. It documents exactly this correction (hardcoded thresholds → a database table) with the operational reasoning. Your reasoning doesn't need to match — but you should have *some* documented reasoning for a decision you changed.

### Step 3 — Decompose into tasks

Run your task-decomposition step (e.g. `/speckit-tasks`). For at least 3 tasks, confirm out loud (to a partner, or in your own notes) which specific FR-### each one maps to.

**Checkpoint**: Compare against `../../project/specs/001-equipment-health-monitoring/tasks.md` — every implementation task cites an FR number. If any of your tasks don't map to a requirement, ask why that task exists.

## Demo talk track (sales / technical evaluation call)

**Suggested time**: 3–4 minutes.

Open `../../project/specs/001-equipment-health-monitoring/plan.md`, scroll to "Plan Review Note." Read it aloud: the first draft hardcoded alert thresholds in source code — cheap to build, but means an engineer has to redeploy the service to fix one number, for a system whose entire premise is that *non-engineers* act on its output.

*"This is what 'review the plan before accepting it' actually looks like. Nothing here was technically wrong — it would have worked. It just would have been an operational trap six months from now. That's not a bug an automated gate catches. It takes a person reading the plan and asking 'who has to act on this later?'"*
