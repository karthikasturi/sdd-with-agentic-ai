from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Alert, AlertEvent, Equipment, Reading, ThresholdConfig
from app.schemas import ReadingIn, ReadingResult

router = APIRouter()


@router.post("/readings", response_model=ReadingResult, status_code=201)
def submit_reading(payload: ReadingIn, db: Session = Depends(get_db)):
    # FR-004: reject readings for equipment that was never registered
    equipment = db.get(Equipment, payload.equipment_id)
    if not equipment:
        raise HTTPException(status_code=404, detail="equipment not registered")

    # FR-003: record the reading (FR-005's non-numeric/missing rejection is
    # enforced by ReadingIn's Pydantic schema before this handler ever runs)
    reading = Reading(equipment_id=equipment.id, value=payload.value)
    db.add(reading)
    db.commit()
    db.refresh(reading)

    thresholds = db.get(ThresholdConfig, equipment.type)
    severity = _evaluate_severity(db, equipment, reading, thresholds)

    alert_created: Optional[str] = None
    if severity and _raise_alert_if_not_duplicate(db, equipment, reading, severity):
        alert_created = severity

    return ReadingResult(reading_id=reading.id, alert_raised=alert_created)


def _evaluate_severity(
    db: Session, equipment: Equipment, reading: Reading, thresholds: ThresholdConfig
) -> Optional[str]:
    # FR-007: critical crosses alert immediately, no debounce
    if reading.value >= thresholds.critical:
        return "critical"

    if reading.value >= thresholds.warning:
        # FR-014: warning-tier requires 2 consecutive warning-band readings
        previous = (
            db.query(Reading)
            .filter(Reading.equipment_id == equipment.id, Reading.id < reading.id)
            .order_by(Reading.id.desc())
            .first()
        )
        if previous is not None and thresholds.warning <= previous.value < thresholds.critical:
            return "warning"

    return None


def _raise_alert_if_not_duplicate(
    db: Session, equipment: Equipment, reading: Reading, severity: str
) -> bool:
    # FR-015: don't create a second open alert of the same severity for the
    # same equipment while one is already open
    existing_open = (
        db.query(Alert)
        .filter(
            Alert.equipment_id == equipment.id,
            Alert.severity == severity,
            Alert.status == "open",
        )
        .first()
    )
    if existing_open:
        return False

    alert = Alert(
        equipment_id=equipment.id,
        reading_id=reading.id,
        severity=severity,
        status="open",
    )
    db.add(alert)
    db.commit()
    db.refresh(alert)

    # Principle V / FR-012: the "raised" transition is itself a history entry,
    # not just the Alert row's initial status
    db.add(AlertEvent(alert_id=alert.id, from_status=None, to_status="open", actor=None))
    db.commit()
    return True
