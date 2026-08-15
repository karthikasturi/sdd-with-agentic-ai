# Implementation attempt from spec-under-specified.md:
# "Alerts that aren't handled in a reasonable time should get escalated
#  so nothing falls through the cracks."
#
# Nothing here was specified: what counts as "handled," how long is
# "reasonable," what "escalated" actually means, whether this applies to
# every severity or just critical, or whether it can happen more than once
# per alert. Every one of those got silently decided below, by whoever
# happened to implement it first.

from datetime import datetime, timedelta

REASONABLE_TIME = timedelta(minutes=15)  # picked arbitrarily -- nobody said 15


def escalate_stale_alerts(db_session, now=None):
    now = now or datetime.utcnow()

    stale_alerts = (
        db_session.query(Alert)
        .filter(Alert.status == "open")  # applies to every severity, not just critical
        .all()
    )

    for alert in stale_alerts:
        if now - alert.created_at > REASONABLE_TIME:
            alert.severity = "critical"  # "escalated" silently redefined as "overwrite to critical"
            db_session.commit()
            # no idempotency guard: this function is meant to run on a
            # schedule, so an alert that's been stale for 3 hours gets
            # re-"escalated" on every single tick -- committing a write,
            # every time, forever, for as long as it stays unacknowledged
