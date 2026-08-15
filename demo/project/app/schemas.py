from typing import Optional

from pydantic import BaseModel, ConfigDict


class EquipmentIn(BaseModel):
    id: str
    name: str
    type: str


class EquipmentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    type: str


class ReadingIn(BaseModel):
    equipment_id: str
    value: float


class ReadingResult(BaseModel):
    reading_id: int
    alert_raised: Optional[str] = None


class AlertOut(BaseModel):
    id: int
    equipment_id: str
    severity: str
    status: str
    reading_id: Optional[int] = None
    reading_value: Optional[float] = None


class AlertAckIn(BaseModel):
    acknowledged_by: str


class AlertAckOut(BaseModel):
    status: str
