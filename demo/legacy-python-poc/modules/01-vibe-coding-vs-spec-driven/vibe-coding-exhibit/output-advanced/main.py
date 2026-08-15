from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from models import Base, Equipment, Reading, Alert, THRESHOLDS

engine = create_engine("sqlite:///./equipment.db", connect_args={"check_same_thread": False})
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)

app = FastAPI()


class EquipmentIn(BaseModel):
    id: str
    name: str
    type: str

    @field_validator("type")
    @classmethod
    def known_type(cls, v):
        if v not in THRESHOLDS:
            raise ValueError(f"unknown equipment type '{v}'")
        return v


class ReadingIn(BaseModel):
    equipment_id: str
    value: float


class AckIn(BaseModel):
    acknowledged_by: str


@app.post("/equipment", status_code=201)
def register_equipment(payload: EquipmentIn):
    db = SessionLocal()
    if db.get(Equipment, payload.id):
        db.close()
        raise HTTPException(status_code=409, detail="equipment already registered")
    eq = Equipment(id=payload.id, name=payload.name, type=payload.type)
    db.add(eq)
    db.commit()
    db.close()
    return payload


@app.post("/readings", status_code=201)
def submit_reading(payload: ReadingIn):
    db = SessionLocal()
    eq = db.get(Equipment, payload.equipment_id)
    if not eq:
        db.close()
        raise HTTPException(status_code=404, detail="equipment not registered")

    reading = Reading(equipment_id=eq.id, value=payload.value, recorded_at=datetime.utcnow())
    db.add(reading)
    db.commit()
    db.refresh(reading)
    reading_id = reading.id

    thresholds = THRESHOLDS[eq.type]
    severity = None
    if payload.value >= thresholds["critical"]:
        severity = "critical"
    elif payload.value >= thresholds["warning"]:
        severity = "warning"

    if severity:
        alert = Alert(equipment_id=eq.id, reading_id=reading_id, severity=severity, status="open")
        db.add(alert)
        db.commit()

    db.close()
    return {"reading_id": reading_id, "alert_raised": severity}


@app.get("/alerts")
def list_alerts(equipment_id: Optional[str] = None):
    db = SessionLocal()
    query = db.query(Alert).filter(Alert.status == "open")
    if equipment_id:
        query = query.filter(Alert.equipment_id == equipment_id)
    results = [
        {
            "id": a.id,
            "equipment_id": a.equipment_id,
            "severity": a.severity,
            "status": a.status,
            "reading_id": a.reading_id,
        }
        for a in query.all()
    ]
    db.close()
    return results


@app.post("/alerts/{alert_id}/ack")
def acknowledge_alert(alert_id: int, payload: AckIn):
    db = SessionLocal()
    alert = db.get(Alert, alert_id)
    if not alert:
        db.close()
        raise HTTPException(status_code=404, detail="alert not found")
    if alert.status == "acknowledged":
        db.close()
        raise HTTPException(status_code=409, detail="alert already acknowledged")
    alert.status = "acknowledged"
    alert.acknowledged_by = payload.acknowledged_by
    alert.acknowledged_at = datetime.utcnow()
    db.commit()
    db.close()
    return {"status": "acknowledged"}
