# Exhibit B — A Better Prompt, Still Not a Spec

Same exercise as Exhibit A, but this time the prompt is written by someone who actually thought about the problem for a few minutes before typing — still just one message, still no persisted spec, no clarify pass, no gates.

> Build a FastAPI service for tracking industrial equipment health. Equipment gets registered with an id, name, and type. Each equipment type should have its own configurable warning and critical thresholds — don't hardcode a single global number. When a reading comes in for unregistered equipment, reject it with a 404 instead of silently accepting it. Validate that reading values are numeric. When a reading crosses a threshold, create an alert with a severity (warning or critical) referencing the reading and equipment. Let maintenance staff list open alerts, optionally filtered by equipment, and acknowledge an alert by id — acknowledging twice should be rejected, not silently ignored. Use SQLAlchemy with SQLite so data isn't lost between restarts. Write it with proper Pydantic models, not raw dicts, and keep routes in a separate file from models.

Output is in `output-advanced/`. It's a real, meaningful step up from Exhibit A — and it still isn't enough. `NOTES.md` covers why.
