from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey

from app.db import Base


def utcnow():
    return datetime.now(timezone.utc)


class Equipment(Base):
    __tablename__ = "equipment"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    created_at = Column(DateTime, default=utcnow)


class ThresholdConfig(Base):
    __tablename__ = "threshold_config"

    equipment_type = Column(String, primary_key=True)
    warning = Column(Float, nullable=False)
    critical = Column(Float, nullable=False)


class Reading(Base):
    __tablename__ = "readings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    equipment_id = Column(String, ForeignKey("equipment.id"), nullable=False)
    value = Column(Float, nullable=False)
    recorded_at = Column(DateTime, default=utcnow)


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    equipment_id = Column(String, ForeignKey("equipment.id"), nullable=False)
    reading_id = Column(Integer, ForeignKey("readings.id"), nullable=True)
    severity = Column(String, nullable=False)
    status = Column(String, nullable=False, default="open")
    created_at = Column(DateTime, default=utcnow)


class AlertEvent(Base):
    __tablename__ = "alert_events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    alert_id = Column(Integer, ForeignKey("alerts.id"), nullable=False)
    from_status = Column(String, nullable=True)
    to_status = Column(String, nullable=False)
    actor = Column(String, nullable=True)
    at = Column(DateTime, default=utcnow)
