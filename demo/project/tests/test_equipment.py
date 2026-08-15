# T008 [P] [US1] Contract test POST /equipment (FR-001, FR-002)


def test_register_equipment_success(client):
    response = client.post(
        "/equipment", json={"id": "eq-1", "name": "Compressor A", "type": "compressor"}
    )
    assert response.status_code == 201
    assert response.json() == {"id": "eq-1", "name": "Compressor A", "type": "compressor"}


def test_register_duplicate_equipment_rejected(client):
    client.post("/equipment", json={"id": "eq-1", "name": "Compressor A", "type": "compressor"})

    response = client.post(
        "/equipment", json={"id": "eq-1", "name": "Compressor A (dup)", "type": "compressor"}
    )

    assert response.status_code == 409


def test_register_unknown_equipment_type_rejected(client):
    response = client.post(
        "/equipment", json={"id": "eq-2", "name": "Mystery Machine", "type": "time-machine"}
    )

    assert response.status_code == 422
