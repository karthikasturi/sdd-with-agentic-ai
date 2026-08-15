# Implementation that follows spec-over-specified.md literally. There's
# nothing left to design here -- the "spec" already dictated the schema
# change, the scheduling library, the SQL, and the integration target. The
# plan phase never happened; this document IS the plan, mislabeled.

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import requests
from sqlalchemy import text

scheduler = BackgroundScheduler()


def escalate_stale_alerts(engine):
    cutoff = datetime.utcnow() - timedelta(minutes=30)
    with engine.begin() as conn:
        rows = conn.execute(
            text(
                "SELECT * FROM alerts WHERE status='open' AND severity='critical' "
                "AND created_at < :cutoff AND escalated_at IS NULL"
            ),
            {"cutoff": cutoff},
        ).fetchall()

        for row in rows:
            conn.execute(
                text(
                    "UPDATE alerts SET severity='critical-escalated', escalated_at=:now "
                    "WHERE id=:id"
                ),
                {"now": datetime.utcnow(), "id": row.id},
            )
            # spec.md's own Assumptions section rules this out: "paging or
            # external notification integrations... are explicitly out of
            # scope for this feature and would need their own spec." The
            # "spec" that generated this code contradicts the project's
            # actual spec.
            requests.post("http://internal-pager/api/v1/page", json={"alert_id": row.id})


scheduler.add_job(lambda: escalate_stale_alerts(engine), "interval", seconds=60)
scheduler.start()
