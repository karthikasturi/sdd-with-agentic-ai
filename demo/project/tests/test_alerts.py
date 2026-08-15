# T016 [P] [US2] Contract test GET /alerts, all and filtered by equipment_id (FR-009)
# T018 [P] [US3] Contract test POST /alerts/{id}/ack — success + duplicate-ack rejection (FR-010, FR-011)
# T019 [P] [US3] Integration test — acknowledgment recorded in AlertEvent history (FR-012)

from app.models import Alert, AlertEvent


def _register(client, equipment_id="eq-1", equipment_type="compressor"):
    client.post(
        "/equipment",
        json={"id": equipment_id, "name": "Test Unit", "type": equipment_type},
    )


def _raise_critical_alert(client, equipment_id="eq-1", value=150):
    return client.post("/readings", json={"equipment_id": equipment_id, "value": value}).json()


def _first_alert_id(client, equipment_id=None):
    params = {"equipment_id": equipment_id} if equipment_id else {}
    return client.get("/alerts", params=params).json()[0]["id"]


def test_list_alerts_returns_equipment_severity_and_reading_value(client):
    _register(client)
    reading = _raise_critical_alert(client)

    response = client.get("/alerts")

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    alert = body[0]
    assert alert["equipment_id"] == "eq-1"
    assert alert["severity"] == "critical"
    assert alert["status"] == "open"
    assert alert["reading_id"] == reading["reading_id"]
    # FR-009/SC-002 (F1 fix): reading_value embedded inline, not just reading_id
    assert alert["reading_value"] == 150


def test_list_alerts_filtered_by_equipment_id(client):
    _register(client, equipment_id="eq-1")
    _register(client, equipment_id="eq-2")
    _raise_critical_alert(client, equipment_id="eq-1")
    _raise_critical_alert(client, equipment_id="eq-2")

    response = client.get("/alerts", params={"equipment_id": "eq-1"})

    body = response.json()
    assert len(body) == 1
    assert body[0]["equipment_id"] == "eq-1"


def test_list_alerts_with_no_open_alerts_returns_empty_list(client):
    _register(client)
    client.post("/readings", json={"equipment_id": "eq-1", "value": 10})

    response = client.get("/alerts")

    assert response.status_code == 200
    assert response.json() == []


def test_list_alerts_excludes_acknowledged_alerts(client):
    _register(client)
    _raise_critical_alert(client)
    alert_id = _first_alert_id(client)

    client.post(f"/alerts/{alert_id}/ack", json={"acknowledged_by": "tech-1"})
    response = client.get("/alerts")

    # FR-009: the listing is the open-alert queue, not the full alert history
    assert response.json() == []


def test_acknowledge_alert_success(client, db_session):
    _register(client)
    _raise_critical_alert(client)
    alert_id = _first_alert_id(client)

    response = client.post(f"/alerts/{alert_id}/ack", json={"acknowledged_by": "tech-1"})

    assert response.status_code == 200
    assert response.json() == {"status": "acknowledged"}

    stored = db_session.get(Alert, alert_id)
    assert stored.status == "acknowledged"


def test_acknowledge_nonexistent_alert_rejected(client):
    response = client.post("/alerts/999/ack", json={"acknowledged_by": "tech-1"})

    assert response.status_code == 404


def test_duplicate_acknowledge_rejected(client, db_session):
    _register(client)
    _raise_critical_alert(client)
    alert_id = _first_alert_id(client)

    first = client.post(f"/alerts/{alert_id}/ack", json={"acknowledged_by": "tech-1"})
    second = client.post(f"/alerts/{alert_id}/ack", json={"acknowledged_by": "tech-2"})

    assert first.status_code == 200
    assert second.status_code == 409

    # FR-011: rejection must leave the original acknowledgment untouched
    stored = db_session.get(Alert, alert_id)
    assert stored.status == "acknowledged"


def test_acknowledgment_recorded_in_alert_event_history(client, db_session):
    _register(client)
    _raise_critical_alert(client)
    alert_id = _first_alert_id(client)

    client.post(f"/alerts/{alert_id}/ack", json={"acknowledged_by": "tech-1"})

    events = (
        db_session.query(AlertEvent)
        .filter(AlertEvent.alert_id == alert_id)
        .order_by(AlertEvent.id)
        .all()
    )
    # FR-012 / Principle V: full history, not a mutated status field —
    # the "raised" event and the "acknowledged" event both persist
    assert len(events) == 2

    raised, acknowledged = events
    assert raised.from_status is None
    assert raised.to_status == "open"

    assert acknowledged.from_status == "open"
    assert acknowledged.to_status == "acknowledged"
    assert acknowledged.actor == "tech-1"


def test_duplicate_acknowledge_does_not_create_second_event(client, db_session):
    _register(client)
    _raise_critical_alert(client)
    alert_id = _first_alert_id(client)

    client.post(f"/alerts/{alert_id}/ack", json={"acknowledged_by": "tech-1"})
    client.post(f"/alerts/{alert_id}/ack", json={"acknowledged_by": "tech-2"})

    events = db_session.query(AlertEvent).filter(AlertEvent.alert_id == alert_id).all()

    # the rejected duplicate attempt must not leave a second event behind
    assert len(events) == 2
