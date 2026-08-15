# T009 [P] [US1] Contract test POST /readings — unregistered/invalid input (FR-004, FR-005)
# T010 [P] [US1] Integration test — critical reading raises alert immediately (FR-007, SC-001, SC-004)
# T011 [P] [US1] Integration test — warning reading requires 2 consecutive readings (FR-014)
# T024 [P] [US1] Integration test — duplicate critical alert suppressed (FR-015)

from app.models import Alert


def _register(client, equipment_id="eq-1", equipment_type="compressor"):
    client.post(
        "/equipment",
        json={"id": equipment_id, "name": "Test Unit", "type": equipment_type},
    )


def test_reading_for_unregistered_equipment_rejected(client):
    response = client.post("/readings", json={"equipment_id": "ghost", "value": 10})

    assert response.status_code == 404


def test_reading_with_non_numeric_value_rejected(client):
    _register(client)

    response = client.post("/readings", json={"equipment_id": "eq-1", "value": "not-a-number"})

    assert response.status_code == 422


def test_safe_reading_raises_no_alert(client):
    _register(client)

    response = client.post("/readings", json={"equipment_id": "eq-1", "value": 10})

    assert response.status_code == 201
    assert response.json()["alert_raised"] is None


def test_critical_reading_raises_alert_immediately(client):
    _register(client)

    response = client.post("/readings", json={"equipment_id": "eq-1", "value": 150})

    body = response.json()
    assert body["alert_raised"] == "critical"
    assert body["reading_id"] is not None


def test_single_warning_reading_does_not_alert(client):
    _register(client)

    response = client.post("/readings", json={"equipment_id": "eq-1", "value": 85})

    assert response.json()["alert_raised"] is None


def test_two_consecutive_warning_readings_alert(client):
    _register(client)

    client.post("/readings", json={"equipment_id": "eq-1", "value": 85})
    response = client.post("/readings", json={"equipment_id": "eq-1", "value": 86})

    assert response.json()["alert_raised"] == "warning"


def test_warning_reading_followed_by_safe_reading_does_not_alert(client):
    _register(client)

    client.post("/readings", json={"equipment_id": "eq-1", "value": 85})
    response = client.post("/readings", json={"equipment_id": "eq-1", "value": 10})

    assert response.json()["alert_raised"] is None


def test_duplicate_critical_alert_suppressed(client, db_session):
    _register(client)

    first = client.post("/readings", json={"equipment_id": "eq-1", "value": 150})
    second = client.post("/readings", json={"equipment_id": "eq-1", "value": 160})

    assert first.json()["alert_raised"] == "critical"
    assert second.json()["alert_raised"] is None  # FR-015: duplicate suppressed

    open_critical_alerts = (
        db_session.query(Alert)
        .filter(Alert.equipment_id == "eq-1", Alert.severity == "critical", Alert.status == "open")
        .all()
    )
    assert len(open_critical_alerts) == 1
