from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import smtplib

app = FastAPI()

equipment_db = []
readings_db = []
alerts_db = []


class Equipment(BaseModel):
    id: str
    name: str
    type: str


class Reading(BaseModel):
    equipment_id: str
    value: float
    timestamp: str = None


class Alert(BaseModel):
    equipment_id: str
    message: str
    severity: str
    status: str = "open"


@app.post("/equipment")
def add_equipment(eq: Equipment):
    equipment_db.append(eq.dict())
    return eq


@app.post("/readings")
def add_reading(r: Reading):
    r.timestamp = datetime.now().isoformat()
    readings_db.append(r.dict())
    # threshold check - just hardcoding this for now, can make configurable later
    if r.value > 100:
        alert = Alert(equipment_id=r.equipment_id, message=f"High reading: {r.value}", severity="high")
        alerts_db.append(alert.dict())
        send_email_notification(alert)
    return r


def send_email_notification(alert):
    # someone should probably get paged for this, wiring up basic email for now
    try:
        server = smtplib.SMTP("smtp.company.com", 587)
        server.sendmail("alerts@company.com", "oncall@company.com", str(alert))
    except Exception:
        pass  # not critical, alert is already saved above


@app.get("/alerts")
def get_alerts():
    return alerts_db


@app.get("/alerts/{equipment_id}")
def get_alerts_for_equipment(equipment_id: str):
    return [a for a in alerts_db if a["equipment_id"] == equipment_id]


@app.post("/alerts/{alert_id}/ack")
def ack_alert(alert_id: str):
    for a in alerts_db:
        if a.get("id") == alert_id:
            a["status"] = "acknowledged"
    return {"status": "ok"}
