# Module 6 — Multi-Agent Delegation Transcript

## What was delegated

A second agent instance (a fresh session, no memory of anything built in Modules 1–5) was handed a single, scoped implementation task: implement User Story 2 (`GET /alerts`, T016–T017) and User Story 3 (acknowledge, T018–T020) — the two remaining stories from `project/specs/001-equipment-health-monitoring/tasks.md`. The delegating prompt pointed it at the constitution, the spec's FR-009 through FR-012, `data-model.md`, `contracts/api.md`, `tasks.md`, and the existing implemented code to match style against. It was explicitly told not to touch spec/plan/tasks/constitution, and not to implement anything beyond those two stories.

This is the real division of labor the outline describes: the primary session stays on governance and integration; the delegated agent gets a bounded, well-specified slice with the artifacts it needs to do the work without guessing.

## What came back

- `app/routers/alerts.py` (`GET /alerts`, `POST /alerts/{alert_id}/ack`)
- New schemas in `app/schemas.py`
- Router registered in `app/main.py`
- A fix in `app/routers/readings.py`: the agent noticed the "raised" `AlertEvent` was never actually being written when an alert is created (only the acknowledgment transition was going to be recorded), and added it — correctly reasoning that an alert with only an "acknowledged" event and no "raised" event has an incomplete history, which violates constitution Principle V.
- `tests/test_alerts.py` — 9 new tests
- Self-reported 4 judgment calls where the spec/contract text didn't fully disambiguate its choice (see below)

**Independently verified, not taken on faith**: read every changed file directly, then re-ran `pytest tests/ -v` myself. 20/20 passing — 11 pre-existing, 9 new. Workspace clean afterward (no stray `__pycache__`, `.pytest_cache`, or `equipment_health.db`).

## Reviewing the self-reported judgment calls

The delegated agent flagged four decisions it wasn't fully certain about. Working through them as the reviewer:

1. **`GET /alerts` returns open alerts only.** The agent flagged this as an interpretive choice. On inspection it isn't really ambiguous — FR-009's actual text is "retrieve all *currently open* alerts," so filtering to `status == "open"` is the correct reading, not a guess. Worth noting as a case where appropriate caution ("flag anything not airtight") produced a non-issue — that's a fine failure mode for an agent to have, better than the reverse.
2. **Nullable `reading_value`/`reading_id` via outer join**, anticipating FR-013's not-yet-implemented equipment-offline alerts (which have no triggering reading). Correct against `data-model.md` as written, not scope creep — it's implementing the documented schema, not adding behavior. Approved as-is.
3. **Two separate `db.commit()` calls** in `readings.py`'s alert-creation path (one for the Alert insert, one for the new AlertEvent insert) instead of batching into one. Minor — would request a single commit in a normal PR review for cleanliness, but not blocking, and not a correctness issue in a single-request context.
4. **Duplicate-ack check reads `Alert.status` rather than querying `AlertEvent`.** `data-model.md` explicitly designates `status` as a maintained cache, so reading it is the documented pattern, not a shortcut. Approved.

## What the agent didn't flag — found in independent review

**Acknowledge is not concurrency-safe.** `acknowledge_alert` reads `alert.status`, branches on it, then later sets `alert.status = "acknowledged"` and commits — there's no row lock or optimistic version check between the read and the write. Under genuinely concurrent requests (two maintenance staff racing to acknowledge the same alert at the same moment), both could read `status == "open"` before either commits, and both would then write an `AlertEvent` and set the status — producing two acknowledgment events for one alert, exactly the duplicate the endpoint exists to prevent. The test suite doesn't catch this because `TestClient` requests execute sequentially, one at a time; the race only exists under real concurrent load.

This is the kind of gap that's genuinely easy to miss — it doesn't show up in a code read unless you're specifically asking "what happens if two of these land at the same instant," and no automated gate in this pipeline (tests, checklist, analyze) would surface it, since it's not a spec/plan/tasks inconsistency and the existing tests are all correctness-under-sequential-execution, not concurrency tests.

**Decision**: Not fixed in this pass. Filed as a follow-up rather than blocking — this is a real bug for a production deployment, but the demo/pilot scope declared in `plan.md`'s Technical Context ("not designed for high-volume production ingestion in this revision") makes it a reasonable, explicitly-triaged deferral rather than a silent gap. The distinction matters: this is written down, not dropped.

## The point of this exercise

The delegated agent did good, disciplined work and was honest about its own uncertainty — three of its four self-flagged judgment calls held up under review, and the fourth was a minor style nit. But it still missed something a reviewer thinking about *operational conditions the tests don't exercise* caught. Multi-agent delegation doesn't remove the need for review; it changes what the reviewer is checking for. A subagent with the same context as the one that wrote code will usually make similar assumptions to the one that reviews it, so the questions worth asking are less "did it follow the spec" (it clearly did) and more "what's true under conditions this test suite doesn't create."
