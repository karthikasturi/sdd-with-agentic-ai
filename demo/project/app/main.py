from fastapi import FastAPI

from app.db import Base, engine
from app.routers import alerts, equipment, readings
from app.seed import seed_thresholds

Base.metadata.create_all(bind=engine)
seed_thresholds()

app = FastAPI(title="Equipment Health Monitoring Service")

app.include_router(equipment.router)
app.include_router(readings.router)
app.include_router(alerts.router)
