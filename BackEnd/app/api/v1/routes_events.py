from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import Optional
from datetime import datetime
from app.db.session import get_db
from app.db.models import Event, Animal, Facility, User
from app.services.plausibility_engine import validate_event

router = APIRouter()

@router.post("/", status_code=201)
def create_event(payload: dict, db: Session = Depends(get_db)):
    """Create a new event with validation"""
    animal_id = payload.get("animal_id")
    if not animal_id:
        raise HTTPException(status_code=400, detail="animal_id is required")
    
    animal = db.query(Animal).filter(Animal.id == animal_id).first()
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    
    # Validate event
    result = validate_event(payload)
    
    event = Event(
        event_type=payload.get("event_type"),
        animal_id=animal_id,
        actor_id=payload.get("actor_id"),
        facility_id=payload.get("facility_id"),
        event_metadata=payload.get("metadata", ""),
        is_valid=result["is_valid"],
        anomaly_reason=result.get("reason"),
        timestamp=datetime.utcnow()
    )
    
    db.add(event)
    db.commit()
    db.refresh(event)
    
    return {
        "status": "success",
        "event": {
            "id": event.id,
            "event_type": event.event_type,
            "animal_id": event.animal_id,
            "timestamp": str(event.timestamp),
            "is_valid": event.is_valid,
            "anomaly_reason": event.anomaly_reason
        },
        "validation": result
    }

@router.post("/record")
def record_event(event: dict, db: Session = Depends(get_db)):
    """Legacy endpoint - redirects to create_event"""
    return create_event(event, db)

@router.get("/")
def list_events(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    event_type: Optional[str] = None,
    animal_id: Optional[int] = None,
    facility_id: Optional[int] = None,
    is_valid: Optional[bool] = None
):
    """List events with filtering and pagination"""
    query = db.query(Event)
    
    if event_type:
        query = query.filter(Event.event_type == event_type)
    if animal_id:
        query = query.filter(Event.animal_id == animal_id)
    if facility_id:
        query = query.filter(Event.facility_id == facility_id)
    if is_valid is not None:
        query = query.filter(Event.is_valid == is_valid)
    
    total = query.count()
    events = query.order_by(desc(Event.timestamp)).offset(skip).limit(limit).all()
    
    result = []
    for e in events:
        result.append({
            "id": e.id,
            "event_type": e.event_type,
            "animal_id": e.animal_id,
            "actor_id": e.actor_id,
            "facility_id": e.facility_id,
            "timestamp": str(e.timestamp),
            "is_valid": e.is_valid,
            "anomaly_reason": e.anomaly_reason,
            "metadata": e.event_metadata
        })
    
    return {"events": result, "total": total, "skip": skip, "limit": limit}

@router.get("/types")
def list_event_types(db: Session = Depends(get_db)):
    """Get distinct list of all event types"""
    types = db.query(Event.event_type).distinct().all()
    return {"event_types": [t[0] for t in types if t[0]]}

@router.get("/anomalies")
def list_anomalies(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
):
    """Get all events marked as anomalies"""
    query = db.query(Event).filter(Event.is_valid == False)
    total = query.count()
    events = query.order_by(desc(Event.timestamp)).offset(skip).limit(limit).all()
    
    result = []
    for e in events:
        animal = db.query(Animal).filter(Animal.id == e.animal_id).first()
        result.append({
            "id": e.id,
            "event_type": e.event_type,
            "animal": {
                "id": animal.id,
                "name": animal.name,
                "tag_id": animal.tag_id
            } if animal else None,
            "timestamp": str(e.timestamp),
            "anomaly_reason": e.anomaly_reason,
            "metadata": e.event_metadata
        })
    
    return {"anomalies": result, "total": total}

@router.get("/stats")
def get_event_statistics(db: Session = Depends(get_db)):
    """Get event statistics"""
    total_events = db.query(func.count(Event.id)).scalar()
    valid_events = db.query(func.count(Event.id)).filter(Event.is_valid == True).scalar()
    anomalies = db.query(func.count(Event.id)).filter(Event.is_valid == False).scalar()
    
    by_type = db.query(Event.event_type, func.count(Event.id)).group_by(Event.event_type).all()
    
    return {
        "total_events": total_events,
        "valid_events": valid_events,
        "anomalies": anomalies,
        "by_type": [{"event_type": t, "count": c} for t, c in by_type]
    }

@router.get("/{event_id}")
def get_event(event_id: int, db: Session = Depends(get_db)):
    """Get a specific event with related information"""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    animal = db.query(Animal).filter(Animal.id == event.animal_id).first()
    facility = db.query(Facility).filter(Facility.id == event.facility_id).first() if event.facility_id else None
    actor = db.query(User).filter(User.id == event.actor_id).first() if event.actor_id else None
    
    return {
        "id": event.id,
        "event_type": event.event_type,
        "timestamp": str(event.timestamp),
        "is_valid": event.is_valid,
        "anomaly_reason": event.anomaly_reason,
        "metadata": event.event_metadata,
        "animal": {
            "id": animal.id,
            "name": animal.name,
            "species": animal.species,
            "tag_id": animal.tag_id
        } if animal else None,
        "facility": {
            "id": facility.id,
            "name": facility.name,
            "location": facility.location
        } if facility else None,
        "actor": {
            "id": actor.id,
            "username": actor.username,
            "role": actor.role
        } if actor else None
    }
