# Quickstart Validation: Equipment Health Monitoring & Maintenance Alerts

## Prerequisites

```
pip install -r requirements.txt
```

## Run

```
uvicorn app.main:app --reload
```

## Validate User Story 1 (P1) — automatic alert on an unsafe reading

```
curl -s -X POST localhost:8000/equipment \
  -H "Content-Type: application/json" \
  -d '{"id":"eq-1","name":"Compressor A","type":"compressor"}'

curl -s -X POST localhost:8000/readings \
  -H "Content-Type: application/json" \
  -d '{"equipment_id":"eq-1","value":150}'
```

Expected: second call returns `"alert_raised": "critical"`.

## Validate User Story 2 (P2) — triage open alerts

```
curl -s localhost:8000/alerts
curl -s "localhost:8000/alerts?equipment_id=eq-1"
```

Expected: the alert from above appears in both, with `equipment_id`, `severity`, and `reading_id` populated.

## Validate User Story 3 (P3) — acknowledge an alert

```
curl -s -X POST localhost:8000/alerts/1/ack \
  -H "Content-Type: application/json" \
  -d '{"acknowledged_by":"tech-42"}'

curl -s -X POST localhost:8000/alerts/1/ack \
  -H "Content-Type: application/json" \
  -d '{"acknowledged_by":"tech-42"}'
```

Expected: first call returns `{"status": "acknowledged"}`; second call returns 409.

See `contracts/api.md` for full request/response shapes and `data-model.md` for the underlying schema.
