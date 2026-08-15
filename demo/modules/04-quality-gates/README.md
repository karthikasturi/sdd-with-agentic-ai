# Module 4 — Quality Gates Before Implementation

Covers: generating and running a requirements checklist, the analyze cross-artifact consistency pass, and implementing one task end-to-end.

## Hands-on

### Step 1 — Generate and run a checklist

Run your checklist step (e.g. `/speckit-checklist`) against your spec. Read every item — don't just check the boxes that were auto-checked.

**Checkpoint**: `../../project/specs/001-equipment-health-monitoring/checklist.md` has one item that failed on first pass (CHK004 — duplicate-alert suppression) and documents the fix (a new FR-015, added directly to `spec.md`). Did your checklist surface anything comparable? If it came back all-green on the first try, look harder at CHK004's category (alert lifecycle: "what happens when the condition keeps recurring?") — it's a real gap, not a manufactured one for this exercise.

### Step 2 — Run analyze

Run your cross-artifact consistency check (e.g. `/speckit-analyze`) across spec, plan, and tasks.

**Checkpoint**: `../../project/specs/001-equipment-health-monitoring/analyze-report.md` has a real HIGH-severity finding (F1): the alert-listing endpoint's response only returned a reading *ID*, not its value — which fails the spec's own success criterion that staff can tell *why* an alert fired without a second lookup. Resolve whatever your analyze pass finds the same way this one was resolved: fix the artifact, don't just note the finding and move on.

### Step 3 — Implement one task end-to-end

Implement the reading-ingestion + threshold-evaluation slice (equipment registration → submit reading → evaluate against threshold → raise alert, including the duplicate-suppression fix from Step 1). Write the test first, watch it fail, then implement.

**Checkpoint**: `../../project/` has a working implementation under `app/` with a full passing test suite under `tests/`. Run it:

```
cd ../../project
pip install -r requirements.txt
pytest tests/ -v
```

You should see the suite pass. Then verify one specific behavior live — that FR-015's dedup actually works, not just that a test claims it does:

```
uvicorn app.main:app --port 8000 &
curl -s -X POST localhost:8000/equipment -d '{"id":"eq-1","name":"Compressor A","type":"compressor"}' -H "Content-Type: application/json"
curl -s -X POST localhost:8000/readings -d '{"equipment_id":"eq-1","value":150}' -H "Content-Type: application/json"
curl -s -X POST localhost:8000/readings -d '{"equipment_id":"eq-1","value":160}' -H "Content-Type: application/json"
```

The second `readings` call should return `"alert_raised": null` — the alert already exists, so no duplicate gets created, even though the reading is still critical.

## Demo talk track (sales / technical evaluation call)

**Suggested time**: 6–7 minutes.

1. Open `../../project/specs/001-equipment-health-monitoring/checklist.md`, point at CHK004 — originally failed. Read Finding 1: the spec never said what happens when the same equipment stays broken across many readings. Show the fix: FR-015. *"This is the 'unit test suite for requirements' idea. It caught a specific missing requirement before a single line of code existed for it."*
2. Open `analyze-report.md`, finding F1. The spec has a success criterion — staff can tell *why* an alert fired without a second lookup — and the API contract violated it. Show `contracts/api.md`'s note that this was corrected after the finding. *"Checklist audits the spec against itself. Analyze audits spec, plan, and tasks against each other. Different failure classes, different gate."*
3. Open `../../project/app/routers/readings.py`. Walk through the threshold evaluation and `_raise_alert_if_not_duplicate` — a direct line back to FR-015. Run it live (commands above) — a passing test suite, then a live curl proving the dedup fix works outside of a test assertion.
