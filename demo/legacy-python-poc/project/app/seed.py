from app.db import SessionLocal
from app.models import ThresholdConfig

INITIAL_THRESHOLDS = {
    "compressor": {"warning": 80.0, "critical": 100.0},
    "pump": {"warning": 60.0, "critical": 85.0},
    "conveyor": {"warning": 70.0, "critical": 95.0},
}


def seed_thresholds():
    db = SessionLocal()
    try:
        for equipment_type, values in INITIAL_THRESHOLDS.items():
            existing = db.get(ThresholdConfig, equipment_type)
            if existing is None:
                db.add(
                    ThresholdConfig(
                        equipment_type=equipment_type,
                        warning=values["warning"],
                        critical=values["critical"],
                    )
                )
        db.commit()
    finally:
        db.close()
