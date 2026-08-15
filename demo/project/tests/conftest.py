import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import Base, get_db
from app.main import app
from app.models import ThresholdConfig
from app.seed import INITIAL_THRESHOLDS


@pytest.fixture()
def test_session_factory():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    seed_db = session_factory()
    for equipment_type, values in INITIAL_THRESHOLDS.items():
        seed_db.add(
            ThresholdConfig(
                equipment_type=equipment_type,
                warning=values["warning"],
                critical=values["critical"],
            )
        )
    seed_db.commit()
    seed_db.close()

    yield session_factory


@pytest.fixture()
def client(test_session_factory):
    def override_get_db():
        db = test_session_factory()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture()
def db_session(test_session_factory):
    session = test_session_factory()
    yield session
    session.close()
