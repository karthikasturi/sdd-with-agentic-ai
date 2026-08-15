from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Equipment, ThresholdConfig
from app.schemas import EquipmentIn, EquipmentOut

router = APIRouter()


@router.post("/equipment", response_model=EquipmentOut, status_code=201)
def register_equipment(payload: EquipmentIn, db: Session = Depends(get_db)):
    # FR-002: reject registration of an equipment id that's already registered
    if db.get(Equipment, payload.id):
        raise HTTPException(status_code=409, detail="equipment already registered")

    # FR-006 depends on a known threshold configuration existing for the type
    if db.get(ThresholdConfig, payload.type) is None:
        raise HTTPException(status_code=422, detail=f"unknown equipment type '{payload.type}'")

    equipment = Equipment(id=payload.id, name=payload.name, type=payload.type)
    db.add(equipment)
    db.commit()
    db.refresh(equipment)
    return equipment
