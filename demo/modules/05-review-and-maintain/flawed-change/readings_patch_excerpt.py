# Candidate change: a second engineer picks up the still-open part of FR-005
# ("outside the physically valid range for its measurement type" — Day 2 only
# implemented the non-numeric/missing half via Pydantic). This is the diff
# they proposed against app/routers/readings.py. It cleared:
#   - CI (full test suite, including the new test in test_readings_range.py)
#   - A skim review that checks "does this add range validation? yes."
# It should not have cleared human review. See module5-flawed-review.md.

router = ...  # unchanged

VALID_RANGES = {
    "compressor": (0.0, 500.0),
    "pump": (0.0, 500.0),
    "conveyor": (0.0, 500.0),
}


def submit_reading(payload, db):
    equipment = db.get(Equipment, payload.equipment_id)
    if not equipment:
        raise HTTPException(status_code=404, detail="equipment not registered")

    # FR-005: keep readings within the physically valid range for the sensor
    value = payload.value
    low, high = VALID_RANGES.get(equipment.type, (0.0, 500.0))
    if value < low or value > high:
        value = max(low, min(value, high))  # <-- the actual bug is this line

    reading = Reading(equipment_id=equipment.id, value=value)
    db.add(reading)
    # ...unchanged from here down
