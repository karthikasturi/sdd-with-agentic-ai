from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Alert, AlertEvent, Reading
from app.schemas import AlertAckIn, AlertAckOut, AlertOut

router = APIRouter()


@router.get("/alerts", response_model=list[AlertOut])
def list_alerts(equipment_id: Optional[str] = None, db: Session = Depends(get_db)):
    # FR-009: currently open alerts, optionally filtered to one equipment
    query = (
        db.query(Alert, Reading.value)
        .outerjoin(Reading, Alert.reading_id == Reading.id)
        .filter(Alert.status == "open")
    )
    if equipment_id is not None:
        query = query.filter(Alert.equipment_id == equipment_id)

    # SC-002 / F1: reading_value is embedded inline so the alert is
    # self-explanatory without a second lookup against /readings
    return [
        AlertOut(
            id=alert.id,
            equipment_id=alert.equipment_id,
            severity=alert.severity,
            status=alert.status,
            reading_id=alert.reading_id,
            reading_value=reading_value,
        )
        for alert, reading_value in query.all()
    ]


@router.post("/alerts/{alert_id}/ack", response_model=AlertAckOut)
def acknowledge_alert(alert_id: int, payload: AlertAckIn, db: Session = Depends(get_db)):
    alert = db.get(Alert, alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="alert not found")

    # FR-011: reject re-acknowledging an already-acknowledged alert
    if alert.status == "acknowledged":
        raise HTTPException(status_code=409, detail="alert already acknowledged")

    # FR-010, FR-012, Principle V: the transition is recorded as its own
    # AlertEvent row (actor, prior state, timestamp) — Alert.status is only
    # updated alongside it as a convenience cache, never in place of it
    db.add(
        AlertEvent(
            alert_id=alert.id,
            from_status=alert.status,
            to_status="acknowledged",
            actor=payload.acknowledged_by,
        )
    )
    alert.status = "acknowledged"
    db.commit()

    return AlertAckOut(status="acknowledged")
