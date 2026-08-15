# The test that shipped alongside the change in readings_patch_excerpt.py.
# It's real — copy it into tests/ next to test_readings.py and it passes,
# together with the entire existing suite (12/12 green). Verified.


def _register(client, equipment_id="eq-1", equipment_type="compressor"):
    client.post(
        "/equipment",
        json={"id": equipment_id, "name": "Test Unit", "type": equipment_type},
    )


def test_out_of_range_reading_is_handled(client):
    _register(client)

    response = client.post("/readings", json={"equipment_id": "eq-1", "value": 99999})

    assert response.status_code == 201
    # Note what's missing: no assertion anywhere on what value actually got
    # stored. The test confirms the endpoint "handled" an out-of-range
    # reading without crashing — it never checks whether "handled" means
    # "rejected" (what FR-005 requires) or "silently altered" (what the
    # implementation actually does).
