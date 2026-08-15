from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

THRESHOLDS = {
    "compressor": {"warning": 80.0, "critical": 100.0},
    "pump": {"warning": 60.0, "critical": 85.0},
    "conveyor": {"warning": 70.0, "critical": 95.0},
}


class Equipment(Base):
    __tablename__ = "equipment"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)


class Reading(Base):
    __tablename__ = "readings"
    id = Column(Integer, primary_key=True, autoincrement=True)
    equipment_id = Column(String, ForeignKey("equipment.id"), nullable=False)
    value = Column(Float, nullable=False)
    recorded_at = Column(DateTime, default=datetime.utcnow)


class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    equipment_id = Column(String, ForeignKey("equipment.id"), nullable=False)
    reading_id = Column(Integer, ForeignKey("readings.id"), nullable=False)
    severity = Column(String, nullable=False)
    status = Column(String, default="open")
    acknowledged_by = Column(String, nullable=True)
    acknowledged_at = Column(DateTime, nullable=True)
