# "Spec" — Over-Specified

The entire requirement, as written by a real engineer trying to be thorough:

> Add a column `escalated_at TIMESTAMP NULL` to the `alerts` table. Every 60 seconds, run a background APScheduler job named `escalate_stale_alerts` that executes `SELECT * FROM alerts WHERE status='open' AND severity='critical' AND created_at < NOW() - INTERVAL 30 MINUTE AND escalated_at IS NULL`. For each row, execute `UPDATE alerts SET severity='critical-escalated', escalated_at=NOW() WHERE id=:id` inside a transaction, then call `requests.post('http://internal-pager/api/v1/page', json={"alert_id": row.id})` synchronously within the same job iteration.

This is precise, unambiguous, and testable — and it's not a specification. It's an implementation plan wearing a spec's name. See `output-from-over-specified.py` for what happens when it's implemented exactly as written, and `../comparison.md` for the critique.
