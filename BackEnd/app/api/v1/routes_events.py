from fastapi import APIRouter, HTTPException
from app.services.plausibility_engine import validate_event

router = APIRouter()

events_db = []  # temporary in-memory list for MVP

@router.post("/record")
def record_event(event: dict):
    result = validate_event(event)
    event["is_valid"] = result["is_valid"]
    event["anomaly_reason"] = result["reason"]

    events_db.append(event)
    return {"status": "success", "validation": result}
